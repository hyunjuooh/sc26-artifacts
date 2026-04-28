#!/bin/bash -l
#SBATCH --nodes=4
#SBATCH --time=00:30:00
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --account=<account>
#SBATCH -J <job_name>
#SBATCH -o o%j.<job_name>.out
#SBATCH -e o%j.<job_name>.out

N_NODE=4
SERVER_PPN=2
PPN=4
NFILE=840
TOTALFILE=$((NFILE * N_NODE))
NSERVER=$((SERVER_PPN * N_NODE))
NCLIENT=$((PPN * N_NODE))

echo "Starting tasks..."

# Required environment variables
export HDF5_DIR=/path/to/your/hdf5
export LD_LIBRARY_PATH=$HDF5_DIR/lib:$LD_LIBRARY_PATH
export DATA_DIR=/path/to/your/data

srun -n $NCLIENT --ntasks-per-node=4 --ntasks-per-socket=4 -c 16 --overlap ./generator $TOTALFILE

# sleep 10

srun -n $NCLIENT --ntasks-per-node=4 --ntasks-per-socket=4 -c 16 --overlap ./hdf5_reader_epoch5 $TOTALFILE >> trainingio_hdf5_4node.txt

echo "Script tasks completed."

