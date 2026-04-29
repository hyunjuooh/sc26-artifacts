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
export WORK_SPACE=/path/to/your/work_space
export SUPERCOMPUTER=perlmutter

export MERCURY_SRC_DIR=/path/to/your/mercury/source/code
export MERCURY_DIR=/path/to/your/mercury
export PDC_SRC_DIR=/path/to/your/pdc/source/code
export PDC_DIR=/path/to/your/pdc

export LD_LIBRARY_PATH="$MERCURY_DIR/lib:$LD_LIBRARY_PATH"
export PATH="$MERCURY_DIR/include:$MERCURY_DIR/lib:$PATH"
export LD_LIBRARY_PATH="$PDC_DIR/lib:$LD_LIBRARY_PATH"
export PATH="$PDC_DIR/include:$PDC_DIR/lib:$PATH"

export DATA_DIR=/path/to/your/data

# Build the evaluation code
cc -I${PDC_DIR}/include -L${PDC_DIR}/lib -o pdc_generator data_generator/pdc_data_generator.c -lpdc
cc -I${PDC_DIR}/include -L${PDC_DIR}/lib -o pdc_reader_clientcache data_reader/pdc_data_reader_cache.c -lpdc

srun -N $N_NODE -n $NSERVER --ntasks-per-node=$SERVER_PPN -c 4  --cpu_bind=cores --overlap /pscratch/sd/h/hjoh16/pdc_work_space/install/pdc/bin/pdc_server &

sleep 5	

srun -n $NCLIENT --ntasks-per-node=4 --ntasks-per-socket=4 -c 16 --overlap ./pdc_generator $TOTALFILE

sleep 600

srun -n $NCLIENT --ntasks-per-node=4 --ntasks-per-socket=4 -c 16 --overlap ./pdc_reader_clientcache $TOTALFILE >> trainingio_pdc_clientcache_4nodes.txt

srun -N $N_NODE -n $NSERVER --ntasks-per-node=$SERVER_PPN -c 4  --cpu_bind=cores --overlap /pscratch/sd/h/hjoh16/pdc_work_space/install/pdc/bin/close_server

