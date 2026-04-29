#!/bin/bash -l
#SBATCH --nodes=4
#SBATCH --time=00:05:00
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --account=<account>
#SBATCH -J <job_name>
#SBATCH -o o%j.<job_name>.out
#SBATCH -e o%j.<job_name>.out

echo "Starting tasks..."

# Required environment variables
export HDF5_DIR=/path/to/your/hdf5
export ABT_DIR=/path/to/your/argobots
export HDF5_VOL_DIR=/path/to/your/vol-cache

export HDF5_PLUGIN_PATH=$HDF5_VOL_DIR/lib
export HDF5_VOL_CONNECTOR="cache_ext config=/path/to/your/config_1.cfg;under_vol=512;under_info={under_vol=0;under_info={}};"
export LD_LIBRARY_PATH=$ABT_DIR/lib:$HDF5_DIR/lib:$HDF5_PLUGIN_PATH:$LD_LIBRARY_PATH

export HDF5_ROOT=/path/to/your/hdf5
export HDF5_CACHE_RD=yes
export HDF5_CACHE_WR=no

# Build the evaluation code
cc -I${HDF5_DIR}/include -L${HDF5_DIR}/lib -o vpic_hdf5 vpic_io_data_generation/hdf5_vpicio.c -lhdf5
cc -I${HDF5_DIR}/include -L${HDF5_DIR}/lib -o bdcats_hdf5_cachevol bdcats_io_test/hdf5_bdcats_test.c -lhdf5

N_NODE=4 # Number of nodes
PPN=32 # Number of processes per node
NCLIENT=$((PPN * N_NODE))

echo "Starting bdcats test"

# Create a path for your hdf5 data
mkdir -p /path/to/your/data

# Set the stripe size for the directory (for Lustre file system environments)
lfs setstripe -c 32 /path/to/your/data

for i in {1..1}; do
    srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN -c 2 --cpu_bind=cores --overlap vpic_hdf5 /path/to/your/data/hdf5_file.hdf5 1 0 16777216 

    sleep 2 

    srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN -c 2 --cpu_bind=cores --overlap bdcats_hdf5_cachevol /path/to/your/data/hdf5_file.hdf5 1 0 16777216 1 3 >> bdcats_cachevol_4nodes.txt
done

echo "Script tasks completed."

