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
export LD_LIBRARY_PATH=$HDF5_DIR/lib:$LD_LIBRARY_PATH

N_NODE=4
PPN=32
NCLIENT=$((PPN * N_NODE))

echo "Starting bdcats test"

# Create a path for your hdf5 data
mkdir -p /path/to/your/data

# Set the stripe size for the directory (for Lustre file system environments)
lfs setstripe -c 32 /path/to/your/data

for i in {1..1}; do
    srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN -c 2 --cpu_bind=cores --overlap vpic_hdf5 /path/to/your/data/hdf5_file.hdf5 1 0 16777216 

    sleep 2 

    srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN -c 2 --cpu_bind=cores --overlap bdcats_hdf5 /path/to/your/data/hdf5_file.hdf5 1 0 16777216 1 3 >> bdcats_hdf5_4nodes.txt
done

echo "Script tasks completed."

