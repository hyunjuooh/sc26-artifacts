#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <limits.h>
#include <float.h>
#include <math.h>

#ifndef ITERS
#define ITERS 30
#endif

// Structure to hold a single measurement's data with timings for each iteration
struct Measurement {
    int target;
    double* times; 
    int is_inter; // 0 for intra, 1 for inter
};

// Records timing for each of the memcpy iterations
static void run_memcpy_iters(char *dst, const char *src, size_t n, double* timings) {
    for (int i = 0; i < ITERS; i++) {
        double t0 = MPI_Wtime();
        memcpy(dst, src, n);
        double t1 = MPI_Wtime();
        timings[i] = t1 - t0;
    }
}

// Records timing for each of the MPI_Get iterations
static void run_get_iters(MPI_Win win, int target, void *dst, size_t n, double* timings) {
    for (int i = 0; i < ITERS; i++) {
        double t0 = MPI_Wtime();
        
        MPI_Win_lock(MPI_LOCK_SHARED, target, 0, win);
        MPI_Get(dst, (int)n, MPI_BYTE, target, 0, (int)n, MPI_BYTE, win);
        MPI_Win_flush(target, win);
        MPI_Win_unlock(target, win);
        
        double t1 = MPI_Wtime();
        timings[i] = t1 - t0;
    }
}

int main(int argc, char **argv) {
    MPI_Init(&argc, &argv);

    int wrank, wsize;
    MPI_Comm_rank(MPI_COMM_WORLD, &wrank);
    MPI_Comm_size(MPI_COMM_WORLD, &wsize);

    const char* output_dir = ".";
    size_t defaults[] = { 1048576 }; // 1 MiB default
    size_t *sizes = NULL;
    int n_sizes = 0;
    size_t* temp_sizes = (size_t*)malloc(argc * sizeof(size_t));

    // The execution requires a directory and a payload size
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-d") == 0) {
            if (i + 1 < argc) {
                output_dir = argv[i + 1];
                i++; 
            } else {
                if (wrank == 0) fprintf(stderr, "Error: -d flag requires a directory path.\n");
                MPI_Abort(MPI_COMM_WORLD, 1);
            }
        } else {
            temp_sizes[n_sizes] = (size_t)strtoull(argv[i], NULL, 10);
            if (temp_sizes[n_sizes] == 0) temp_sizes[n_sizes] = 1;
            n_sizes++;
        }
    }

    if (n_sizes > 0) {
        sizes = (size_t*)malloc(n_sizes * sizeof(size_t));
        memcpy(sizes, temp_sizes, n_sizes * sizeof(size_t));
    } else {
        sizes = defaults;
        n_sizes = 1;
    }
    
    free(temp_sizes);


    // Create a node-local communicator to identify ranks on the same node
    MPI_Comm shm_comm;
    MPI_Comm_split_type(MPI_COMM_WORLD, MPI_COMM_TYPE_SHARED, 0, MPI_INFO_NULL, &shm_comm);
    
    int nrank, nsize;
    MPI_Comm_rank(shm_comm, &nrank);
    MPI_Comm_size(shm_comm, &nsize);

    // Gather all hostnames to all ranks
    char myhost[MPI_MAX_PROCESSOR_NAME];
    int mylen = 0;
    MPI_Get_processor_name(myhost, &mylen);

    int maxlen = 0;
    MPI_Allreduce(&mylen, &maxlen, 1, MPI_INT, MPI_MAX, MPI_COMM_WORLD);
    if (maxlen < 1) maxlen = MPI_MAX_PROCESSOR_NAME;

    char *allhosts = (char*)calloc((size_t)wsize * (maxlen + 1), 1);
    char *sendbuf = (char*)calloc(maxlen + 1, 1);
    strncpy(sendbuf, myhost, (size_t)maxlen);

    MPI_Allgather(sendbuf, maxlen + 1, MPI_CHAR, allhosts, maxlen + 1, MPI_CHAR, MPI_COMM_WORLD);

    int num_nodes = 0;
    if (wrank == 0) {
        char *prev_host = "";
        for(int r=0; r<wsize; ++r) {
            if (strncmp(prev_host, allhosts + r*(maxlen+1), maxlen+1) != 0) {
                num_nodes++;
                prev_host = allhosts + r*(maxlen+1);
            }
        }
        printf("# Job configuration:\n");
        printf("#   World size: %d processes\n", wsize);
        printf("#   Node count: %d nodes (%d processes/node)\n", num_nodes, nsize);
        printf("# Writing timing data to directory '%s'...\n", output_dir);
        fflush(stdout);
    }
    // Broadcast the number of nodes so all ranks know if inter-node comm is possible
    MPI_Bcast(&num_nodes, 1, MPI_INT, 0, MPI_COMM_WORLD);

    // Main loop iterating through each payload size
    for (int si = 0; si < n_sizes; ++si) {
        size_t N = sizes[si];
        if (N > (size_t)INT_MAX) {
            if (wrank == 0) fprintf(stderr, "# ERROR: Message size %zu exceeds INT_MAX\n", N);
            continue;
        }
        
        MPI_Win shm_win;
        void *shm_base = NULL;
        MPI_Aint shm_sz = (nrank == 0) ? (MPI_Aint)N : 0;
        MPI_Win_allocate_shared(shm_sz, 1, MPI_INFO_NULL, shm_comm, &shm_base, &shm_win);
        if (nrank == 0) memset(shm_base, 0, N);
        
        void *src_ptr = NULL;
        if (nsize > 1) {
            int disp_unit; MPI_Aint qsz;
            MPI_Win_shared_query(shm_win, 0, &qsz, &disp_unit, &src_ptr);
        }

        MPI_Win world_win;
        void *world_base = NULL;
        MPI_Win_allocate((MPI_Aint)N, 1, MPI_INFO_NULL, MPI_COMM_WORLD, &world_base, &world_win);
        if (world_base) memset(world_base, 0, N);
        
        char *buf = (char *)malloc(N);

        MPI_Barrier(MPI_COMM_WORLD);

        // Measuring memcpy performance
        double* memcpy_timings = malloc(ITERS * sizeof(double));
        int memcpy_measured = 0;
        if (nsize >= 2 && nrank == 1 && src_ptr) {
            run_memcpy_iters(buf, (const char*)src_ptr, N, memcpy_timings);
            memcpy_measured = 1;
        }
        
        struct Measurement* measurements = malloc(2 * sizeof(struct Measurement));
        int measurement_count = 0;

        // Find one intra-node rank and measure intra-node performance
        if (nsize > 1) {
            int intra_target = -1;
            for (int i = 1; i < wsize; ++i) {
                int potential_target = (wrank + i) % wsize;
                if (strncmp(myhost, allhosts + potential_target * (maxlen + 1), maxlen) == 0) {
                    intra_target = potential_target;
                    break;
                }
            }
            if (intra_target != -1) {
                measurements[measurement_count].times = malloc(ITERS * sizeof(double));
                run_get_iters(world_win, intra_target, buf, N, measurements[measurement_count].times);
                measurements[measurement_count].target = intra_target;
                measurements[measurement_count].is_inter = 0;
                measurement_count++;
            }
        }

        // Find one inter-node rank and measure inter-node performance
        if (num_nodes > 1) {
            int inter_target = -1;
            for (int i = 1; i < wsize; ++i) {
                int potential_target = (wrank + i) % wsize;
                if (strncmp(myhost, allhosts + potential_target * (maxlen + 1), maxlen) != 0) {
                    inter_target = potential_target;
                    break;
                }
            }
            if (inter_target != -1) {
                measurements[measurement_count].times = malloc(ITERS * sizeof(double));
                run_get_iters(world_win, inter_target, buf, N, measurements[measurement_count].times);
                measurements[measurement_count].target = inter_target;
                measurements[measurement_count].is_inter = 1;
                measurement_count++;
            }
        }

        // Only the first and middle rank on each node will write their MPI_Get timing files.
        if (nrank == 0 || nrank == nsize / 2) {
            char filename[256];
            FILE *fp_intra = NULL;
            FILE *fp_inter = NULL;

            // Open files based on what was measured
            for (int i = 0; i < measurement_count; ++i) {
                if (measurements[i].is_inter) {
                    sprintf(filename, "%s/rank%d_inter_mpiget.csv", output_dir, wrank);
                    fp_inter = fopen(filename, "w");
                    if (fp_inter) fprintf(fp_inter, "time_s\n");
                } else {
                    sprintf(filename, "%s/rank%d_intra_mpiget.csv", output_dir, wrank);
                    fp_intra = fopen(filename, "w");
                    if (fp_intra) fprintf(fp_intra, "time_s\n");
                }
            }

            // Write data to the opened files
            for (int i = 0; i < measurement_count; ++i) {
                for (int j = 0; j < ITERS; ++j) {
                    if (measurements[i].is_inter) {
                        if (fp_inter) fprintf(fp_inter, "%.9e\n", measurements[i].times[j]);
                    } else {
                        if (fp_intra) fprintf(fp_intra, "%.9e\n", measurements[i].times[j]);
                    }
                }
            }

            if (fp_intra) fclose(fp_intra);
            if (fp_inter) fclose(fp_inter);
        }
        
        // The rank that performed the memcpy test writes its file
        if (memcpy_measured) {
            char filename[256];
            sprintf(filename, "%s/rank%d_memcpy.csv", output_dir, wrank);
            FILE *fp_mem = fopen(filename, "w");
            if (fp_mem) {
                fprintf(fp_mem, "time_s\n");
                for (int i = 0; i < ITERS; ++i) {
                    fprintf(fp_mem, "%.9e\n", memcpy_timings[i]);
                }
                fclose(fp_mem);
            }
        }
        
        // Free memory for measurements
        for (int i = 0; i < measurement_count; ++i) {
            free(measurements[i].times);
        }
        free(measurements);
        free(memcpy_timings);

        // Cleanup for this iteration.
        free(buf);
        MPI_Win_free(&shm_win);
        MPI_Win_free(&world_win);
        MPI_Barrier(MPI_COMM_WORLD);
    }

    if (wrank == 0) {
        printf("# Benchmark complete.\n");
    }

    if (sizes != defaults) free(sizes);
    free(sendbuf);
    free(allhosts);
    MPI_Comm_free(&shm_comm);
    MPI_Finalize();
    return 0;
}