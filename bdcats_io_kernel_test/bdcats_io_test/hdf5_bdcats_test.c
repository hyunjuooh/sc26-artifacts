/****** Copyright Notice ***
 *
 * PIOK - Parallel I/O Kernels - VPIC-IO, VORPAL-IO, and GCRM-IO, Copyright
 * (c) 2015, The Regents of the University of California, through Lawrence
 * Berkeley National Laboratory (subject to receipt of any required
 * approvals from the U.S. Dept. of Energy).  All rights reserved.
 *
 * If you have questions about your rights to use or distribute this
 * software, please contact Berkeley Lab's Innovation & Partnerships Office
 * at  IPO@lbl.gov.
 *
 * NOTICE.  This Software was developed under funding from the U.S.
 * Department of Energy and the U.S. Government consequently retains
 * certain rights. As such, the U.S. Government has been granted for itself
 * and others acting on its behalf a paid-up, nonexclusive, irrevocable,
 * worldwide license in the Software to reproduce, distribute copies to the
 * public, prepare derivative works, and perform publicly and display
 * publicly, and to permit other to do so.
 *
 ****************************/

/**
 *
 * Email questions to SByna@lbl.gov
 * Scientific Data Management Research Group
 * Lawrence Berkeley National Laboratory
 *
*/

// Description: This is a simple benchmark based on VPIC's I/O interface
//		Each process reads a specified number of particles into
//		a hdf5 output file using only HDF5 calls
// Author:	Suren Byna <SByna@lbl.gov>
//		Lawrence Berkeley National Laboratory, Berkeley, CA
// Created:	in 2011
// Modified:	01/06/2014 --> Removed all H5Part calls and using HDF5 calls
//          	02/19/2019 --> Add option to read multiple timesteps of data - Tang

#include <math.h>
#include <hdf5.h>
#include <stdlib.h>
#include <sys/time.h>
#include <stdio.h>
#include <mpi.h>
#include <inttypes.h>
#include <unistd.h> // for sleep


// A simple timer based on gettimeofday

#define DTYPE float

extern struct timeval start_time[7];
extern float elapse[7];
#define timer_on(id) gettimeofday (&start_time[id], NULL)
#define timer_off(id) 	\
		{	\
		     struct timeval result, now; \
		     gettimeofday (&now, NULL);  \
		     timeval_subtract(&result, &now, &start_time[id]);	\
		     elapse[id] += result.tv_sec+ (DTYPE) (result.tv_usec)/1000000.;	\
		}

#define timer_msg(id, msg) \
	printf("%f seconds elapsed in %s\n", (DTYPE)(elapse[id]), msg);  \

#define timer_reset(id) elapse[id] = 0

/* Subtract the `struct timeval' values X and Y,
   storing the result in RESULT.
   Return 1 if the difference is negative, otherwise 0.  */

int
timeval_subtract (struct timeval *result, struct timeval *x, struct timeval *y)
{
    /* Perform the carry for the later subtraction by updating y. */
    if (x->tv_usec < y->tv_usec) {
        int nsec = (y->tv_usec - x->tv_usec) / 1000000 + 1;
        y->tv_usec -= 1000000 * nsec;
        y->tv_sec += nsec;
    }
    if (x->tv_usec - y->tv_usec > 1000000) {
        int nsec = (y->tv_usec - x->tv_usec) / 1000000;
        y->tv_usec += 1000000 * nsec;
        y->tv_sec -= nsec;
    }

    /* Compute the time remaining to wait.
       tv_usec is certainly positive. */
    result->tv_sec = x->tv_sec - y->tv_sec;
    result->tv_usec = x->tv_usec - y->tv_usec;

    /* Return 1 if result is negative. */
    return x->tv_sec < y->tv_sec;
}

struct timeval start_time[7];
float elapse[7];

// HDF5 specific declerations
herr_t ierr;

// Variables and dimensions
uint64_t numparticles = 8388608;	// 8  meg particles per process
uint64_t total_particles, offset, cache_offset;

float *x, *y, *z;
float *px, *py, *pz;
int *id1, *id2;

// Uniform random number
inline double uniform_random_number()
{
    return (((double)rand())/((double)(RAND_MAX)));
}

void print_data(int n)
{
    int i;
    for (i = 0; i < n; i++)
        printf("%f %f %f %d %d %f %f %f\n", x[i], y[i], z[i], id1[i], id2[i], px[i], py[i], pz[i]);
}

void open_h5_datasets(int rank, hid_t loc, hid_t *dset_ids)
{
    dset_ids[0] = H5Dopen2(loc, "x", H5P_DEFAULT);
    dset_ids[1] = H5Dopen2(loc, "y", H5P_DEFAULT);
    dset_ids[2] = H5Dopen2(loc, "z", H5P_DEFAULT);
    dset_ids[3] = H5Dopen2(loc, "id1", H5P_DEFAULT);
    dset_ids[4] = H5Dopen2(loc, "id2", H5P_DEFAULT);
    dset_ids[5] = H5Dopen2(loc, "px", H5P_DEFAULT);
    dset_ids[6] = H5Dopen2(loc, "py", H5P_DEFAULT);
    dset_ids[7] = H5Dopen2(loc, "pz", H5P_DEFAULT);

    if (rank == 0) printf ("Opened 8 datasets \n");
}

void close_h5_datasets(int rank, hid_t *dset_ids)
{
    int i;
    for (i = 0; i < 8; i++)
        H5Dclose(dset_ids[i]);
    if (rank == 0) printf ("Closed 8 datasets \n");
}

// Create HDF5 file and read data
void read_h5_data(int rank, hid_t *dset_ids, hid_t filespace, hid_t memspace, hid_t dxpl_id)
{
    ierr = H5Dread(dset_ids[0], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, x);
    if (rank == 0) printf ("Read variable 1 \n");

    ierr = H5Dread(dset_ids[1], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, y);

    ierr = H5Dread(dset_ids[2], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, z);

    ierr = H5Dread(dset_ids[3], H5T_NATIVE_INT, memspace, filespace, dxpl_id, id1);

    ierr = H5Dread(dset_ids[4], H5T_NATIVE_INT, memspace, filespace, dxpl_id, id2);

    ierr = H5Dread(dset_ids[5], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, px);

    ierr = H5Dread(dset_ids[6], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, py);

    ierr = H5Dread(dset_ids[7], H5T_NATIVE_FLOAT, memspace, filespace, dxpl_id, pz);

    if (rank == 0) printf ("  Read 8 variable completed\n");

    //print_data(3);
}

void
shuffle(int *arr, int n)
{
    for (int i = n - 1; i > 0; i--) {
        int j   = rand() % (i + 1);
        int tmp = arr[i];
        arr[i]  = arr[j];
        arr[j]  = tmp;
    }
}

void print_usage(char *name)
{
    printf("Usage: %s /path/to/file #timestep sleep_sec #particles num_transfer_request pattern\n", name);
}

int main (int argc, char* argv[])
{
    int my_rank, num_procs, nts, i, sleep_time;
    hid_t file_id, grp, dset_ids[8], dxpl_id;
    hid_t filespace, filespace_cache, memspace, memspace_cache;
    hid_t fapl;
    int    num_transfer_request = 0, access_pattern = 0, random_offset = 0;
    char grp_name[128];
    uint64_t my_size;
    int *rank_arr;

    int mpi_thread_lvl_provided = -1;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &mpi_thread_lvl_provided);
    MPI_Comm_rank (MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size (MPI_COMM_WORLD, &num_procs);

    char *file_name = argv[1];

    if(argc < 3) {
        print_usage(argv[0]);
        return 0;
    }

    nts = atoi(argv[2]);
    if (nts <= 0) {
        print_usage(argv[0]);
        return 0;
    }

    sleep_time = atoi(argv[3]);
    if (sleep_time < 0) {
        print_usage(argv[0]);
        return 0;
    }

    numparticles = atoll(argv[4]);
    if (numparticles <= 0) {
        print_usage(argv[0]);
        return 0;
    }

    num_transfer_request = atoi(argv[5]);
    if (num_transfer_request <= 0) {
        print_usage(argv[0]);
        return 0;
    }
    my_size = numparticles / num_transfer_request;

    access_pattern = atoi(argv[6]);
    if (access_pattern <= 0) {
        print_usage(argv[0]);
        return 0;
    }

    if (my_rank == 0) {
	printf("Reading %" PRIu64 " particles with %d requests and pattern %d.\n", 
		numparticles, num_transfer_request, access_pattern);
    }

    x=(float*)malloc(numparticles*sizeof(double));
    y=(float*)malloc(numparticles*sizeof(double));
    z=(float*)malloc(numparticles*sizeof(double));

    px=(float*)malloc(numparticles*sizeof(double));
    py=(float*)malloc(numparticles*sizeof(double));
    pz=(float*)malloc(numparticles*sizeof(double));

    id1=(int*)malloc(numparticles*sizeof(int));
    id2=(int*)malloc(numparticles*sizeof(int));

    rank_arr = (int *)malloc(num_procs * sizeof(int));

    if (access_pattern == 1) {
        offset = my_rank * numparticles;
    }
    else if (access_pattern == 2) {
        offset = my_rank * numparticles + my_size;
    }
    else if (access_pattern == 3) {
        if (my_rank == 0) {
            for (i = 0; i < num_procs; i++) {
                rank_arr[i] = i;
            }
            shuffle(rank_arr, num_procs);
        }
        MPI_Scatter(rank_arr, 1, MPI_INT, &random_offset, 1, MPI_INT, 0, MPI_COMM_WORLD);
        // offset = random_offset * numparticles;
        offset = my_rank * numparticles;
        cache_offset = random_offset * numparticles;
    }

    /* Set up FAPL */
    if((fapl = H5Pcreate(H5P_FILE_ACCESS)) < 0)
        goto error;
    if(H5Pset_fapl_mpio(fapl, MPI_COMM_WORLD, MPI_INFO_NULL) < 0)
        goto error;

    MPI_Barrier (MPI_COMM_WORLD);
    timer_on (0);

    /* Open file */
    file_id = H5Fopen(file_name, H5F_ACC_RDONLY, fapl);
    if(file_id < 0) {
        printf("Error with opening file [%s]!\n", file_name);
        goto done;
    }

    if (my_rank == 0)
        printf ("Opened HDF5 file ... [%s]\n", file_name);

    total_particles = numparticles * num_procs;
    filespace = H5Screate_simple(1, (hsize_t *) &total_particles, NULL);
    memspace =  H5Screate_simple(1, (hsize_t *) &my_size, NULL);

    filespace_cache = H5Screate_simple(1, (hsize_t *) &total_particles, NULL);
    memspace_cache =  H5Screate_simple(1, (hsize_t *) &numparticles, NULL);

    //H5Pset_dxpl_mpio(fapl, H5FD_MPIO_COLLECTIVE);
    /* printf("Rank %d:  first read selects offset %llu, size %llu\n", my_rank, offset, numparticles); */
    /* printf("Rank %d: second read selects offset %llu, size %llu\n", my_rank, offset, my_size); */
    H5Sselect_hyperslab(filespace, H5S_SELECT_SET, (hsize_t *) &offset, NULL, (hsize_t *) &my_size, NULL);
    H5Sselect_hyperslab(filespace_cache, H5S_SELECT_SET, (hsize_t *) &cache_offset, NULL, (hsize_t *) &numparticles, NULL);

    dxpl_id = H5Pcreate(H5P_DATASET_XFER);
    // H5Pset_dxpl_mpio(dxpl_id, H5FD_MPIO_COLLECTIVE);
    H5Pset_dxpl_mpio(dxpl_id, H5FD_MPIO_INDEPENDENT);

    MPI_Barrier (MPI_COMM_WORLD);
    timer_on (1);

    for (i = 0; i < nts; i++) {
        sprintf(grp_name, "Timestep_%d", i);
        grp = H5Gopen(file_id, grp_name, H5P_DEFAULT);

        timer_reset(2);
        timer_on (2);
        
    	timer_reset(3);
    	timer_on (3);
            
    	open_h5_datasets(my_rank, grp, dset_ids);
    	
    	timer_off(3);

        if (my_rank == 0)
            printf ("Reading %s and cache ... \n", grp_name);
        /* read_h5_data_to_cache(my_rank, dset_ids, filespace_cache, memspace_cache, dxpl_id); */
        
    	timer_reset(4);
    	timer_on (4);
    	
    	read_h5_data(my_rank, dset_ids, filespace_cache, memspace_cache, dxpl_id);
	
    	MPI_Barrier(MPI_COMM_WORLD);
    	timer_off(4);

        if (i != 0) {
            if (my_rank == 0) printf ("  sleep for %ds\n", sleep_time);
            sleep(sleep_time);
        }

        if (my_rank == 0)
            printf ("Reading %s ... \n", grp_name);
        /* read_h5_data_from_cache(my_rank, dset_ids, filespace, memspace, dxpl_id); */
        
    	timer_reset (5);
    	timer_on (5);
    
    	read_h5_data(my_rank, dset_ids, filespace, memspace, dxpl_id);
    	timer_off(5);
    
    	timer_reset (6);
    	timer_on (6);

        close_h5_datasets(my_rank, dset_ids);

        H5Gclose(grp);
        MPI_Barrier(MPI_COMM_WORLD);
	
    	timer_off(6);	
    	timer_off(2);
        
        if (my_rank == 0) {
            timer_msg (2, "read 1 timestep data - total time");
	    timer_msg (3, "read 1 timestep data - open_h5_datasets");
	    timer_msg (4, "read 1 timestep data - initial read time");
	    timer_msg (5, "read 1 timestep data - read with cache");
	    timer_msg (6, "read 1 timestep data - close_h5_datasets");
	}
    }

    MPI_Barrier (MPI_COMM_WORLD);
    timer_off (1);

    H5Sclose(memspace);
    H5Sclose(filespace);
    H5Sclose(memspace_cache);
    H5Sclose(filespace_cache);
    H5Pclose(dxpl_id);
    H5Pclose(fapl);
    H5Fclose(file_id);

    MPI_Barrier (MPI_COMM_WORLD);
    timer_off (0);
    if (my_rank == 0)
    {
        printf ("\nTiming results\n");
        printf("Total sleep time %ds\n", sleep_time*(nts-1));
        timer_msg (1, "just reading data");
        timer_msg (0, "opening, reading, closing file");
        printf ("\n");
    }

    for (int j = 0; j < numparticles; ++j) {
        if (id1[j] != j) {
            printf("[Rank %d] id1 wrong value %d!=%d @ line %d\n", my_rank, id1[j], j, __LINE__);
            break;
        }
        if (id2[j] != j * 2) {
            printf("[Rank %d] id2 wrong value %d!=%d @ line %d\n", my_rank, id2[j], j * 2, __LINE__);
            break;
        }
    }


    free(x);
    free(y);
    free(z);
    free(px);
    free(py);
    free(pz);
    free(id1);
    free(id2);
    free(rank_arr);

error:
    H5E_BEGIN_TRY {
        H5Fclose(file_id);
        H5Pclose(fapl);
    } H5E_END_TRY;

done:
    H5close();
    MPI_Finalize();

    return 0;
}
