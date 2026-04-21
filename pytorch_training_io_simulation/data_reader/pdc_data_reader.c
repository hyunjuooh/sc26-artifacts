#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>
#include <time.h>
#include <sys/time.h>
#include <math.h>
#include <inttypes.h>
#include "pdc.h"

#define NUM_SAMPLES_PER_FILE 1
#define RECORD_LENGTH_BYTES 104857600

#define DIM1 10240
#define DIM2 10240

#define NUM_EPOCHS 5
#define BASE_SEED 42

static uint64_t rand_state;

void set_seed(uint64_t seed) {
    rand_state = seed;
}

uint32_t get_rand() {
    rand_state = rand_state * 6364136223846793005ULL + 1;
    return (uint32_t)(rand_state >> 32);
}

void shuffle_indices(int* array, int n, uint64_t seed) {
    set_seed(seed);
    for (int i = n - 1; i > 0; i--) {
        int j = get_rand() % (i + 1);
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

int main(int argc, char** argv) {
    int rank, size;
    
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Initialize PDC
    pdcid_t pdc_id = PDCinit("pdc");
    
    if (pdc_id < 0) {
        if (rank == 0) fprintf(stderr, "Failed to initialize PDC.\n");
        MPI_Abort(MPI_COMM_WORLD, 1);
    }

    if (argc != 2) {
        if (rank == 0) fprintf(stderr, "Usage: %s <total_files>\n", argv[0]);
        PDCclose(pdc_id);
        MPI_Finalize();
        return 1;
    }

    const char *data_dir = getenv("DATA_DIR");
    if (!data_dir) data_dir = "../data_generator/pdc_data_dir";
    
    int total_files = atoi(argv[1]);
    if (total_files <= 0) {
        if (rank == 0) fprintf(stderr, "Error: total_files must be greater than 0.\n");
        PDCclose(pdc_id);
        MPI_Finalize();
        return 1;
    }

    // Dynamic global sample calculation
    int total_global_samples = total_files * NUM_SAMPLES_PER_FILE;
    int* global_indices = (int *) malloc(total_global_samples * sizeof(int));
    for (int i = 0; i < total_global_samples; i++) {
        global_indices[i] = i;
    }

    // Local buffer for reading data
    uint8_t* data_buffer = (uint8_t *) malloc((size_t)RECORD_LENGTH_BYTES * sizeof(uint8_t));
    int* label_buffer = (int *) malloc(NUM_SAMPLES_PER_FILE * sizeof(int)); 

    MPI_Barrier(MPI_COMM_WORLD);
    
    if (rank == 0) {
        printf("--- Starting DLIO UNet3D PDC Reader Benchmark ---\n");
        printf("Ranks: %d | Epochs: %d | Total Files: %d\n", size, NUM_EPOCHS, total_files);
        printf("Parallelly reading 'records' [%d, %d, %d]\n", 1, DIM1, DIM2);
    }
    
    double total_benchmark_start = MPI_Wtime();

    for (int epoch = 0; epoch < NUM_EPOCHS; epoch++) {
        // Shuffle indices with fixed seed
        shuffle_indices(global_indices, total_global_samples, BASE_SEED + epoch);

        double epoch_start = MPI_Wtime();

        for (int i = rank; i < total_global_samples; i += size) {
            int current_global_idx = global_indices[i];
            
            int target_file_idx = current_global_idx / NUM_SAMPLES_PER_FILE;
            int local_sample_idx = current_global_idx % NUM_SAMPLES_PER_FILE; 

            // Define PDC object names
            char rec_filename[512];
            sprintf(rec_filename, "%s/dataset_%d", data_dir, target_file_idx); 

            double sample_start_time = MPI_Wtime();

            // Open container
            pdcid_t cont_id = PDCcont_open(rec_filename, pdc_id);
            
            // Open objects
            pdcid_t rec_obj_id = PDCobj_open(rec_filename, pdc_id);

            // Create record region (following the same offset and dimension as generator)
            uint64_t dims[3] = {1, DIM1, DIM2}; 
            uint64_t offset[3] = {0, 0, 0};
            uint64_t offset_length[3] = {1, DIM1, DIM2};
            
            pdcid_t rec_local_reg = PDCregion_create(3, offset, offset_length);
            pdcid_t rec_remote_reg = PDCregion_create(3, offset, offset_length);


            // Create transfer request
            pdcid_t transfer_request_record = PDCregion_transfer_create(data_buffer, PDC_READ, rec_obj_id, rec_local_reg, rec_remote_reg);

            PDCregion_transfer_start(transfer_request_record);

            PDCregion_transfer_wait(transfer_request_record);
    
            PDCregion_transfer_close(transfer_request_record);

            // if (rank == 0)
            //     printf("data_buffer[100]: %u\n", data_buffer[100]);
            
            double sample_end_time = MPI_Wtime();
            double sample_duration = sample_end_time - sample_start_time;


            printf("[RANK %d | EPOCH %d] Read Sample %d in %.4f sec\n", rank, epoch + 1, current_global_idx, sample_duration);

            memset(data_buffer, 0, (size_t)RECORD_LENGTH_BYTES);

            // if (rank == 0)
            //     printf("data_buffer[100]: %u\n", data_buffer[100]);

            // Region close
            PDCregion_close(rec_local_reg);
            PDCregion_close(rec_remote_reg);
    
            // Object close
            PDCobj_close(rec_obj_id);
    
            // Container and property close
            PDCcont_close(cont_id);
        }

        MPI_Barrier(MPI_COMM_WORLD);
        double epoch_end = MPI_Wtime();
        
        if (rank == 0) {
            double epoch_time = epoch_end - epoch_start;
            printf("Epoch %d Complete | Time: %.4f sec\n", epoch + 1, epoch_time);
        }
    }

    double total_benchmark_end = MPI_Wtime();

    // Cleanup memory
    free(data_buffer);
    free(label_buffer);
    free(global_indices);

    if (rank == 0) {
        printf("\nTotal Benchmark Time: %.4f sec\n", total_benchmark_end - total_benchmark_start);
    }

    PDCclose(pdc_id);
    MPI_Finalize();
    return 0;
}