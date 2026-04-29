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

# Build the evaluation code
cc -o intra_inter_performance_test intra_inter_performance_test.c 

# Execution command
srun -N 4 -n 128 --ntasks-per-node=32 --cpu-bind=cores ./intra_inter_performance_test -d results/ 268435456