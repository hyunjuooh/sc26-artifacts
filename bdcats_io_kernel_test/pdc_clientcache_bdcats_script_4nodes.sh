#!/bin/bash -l
#SBATCH --nodes=4
#SBATCH --time=00:10:00
#SBATCH --constraint=cpu
#SBATCH --qos=regular
#SBATCH --account=<account>
#SBATCH -J <job_name>
#SBATCH -o o%j.<job_name>.out
#SBATCH -e o%j.<job_name>.out

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

# Build the evaluation code
cc -I${PDC_DIR}/include -L${PDC_DIR}/lib -o pdc_vpicio vpic_io_data_generation/pdc_vpicio.c -lpdc
cc -I${PDC_DIR}/include -L${PDC_DIR}/lib -o pdc_bdcats bdcats_io_test/pdc_bdcats_test.c -lpdc

N_NODE=4
PPN=32
NCLIENT=$((PPN * N_NODE))

echo "Starting bdcats test"

for i in {1..1}; do
        # Start the pdc server
        srun -N $N_NODE -n $N_NODE --ntasks-per-node=1 -c 4  --cpu_bind=cores --overlap /path/to/your/installed/pdc_server  &

    	sleep 5

        # Generate the data
        srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN -c 2 --cpu_bind=cores --overlap pdc_vpicio 16777216
        
        sleep 50

        # Execute bdcats test
        srun -N $N_NODE -n $NCLIENT --ntasks-per-node=$PPN --ntasks-per-socket=$PPN -c 1 --cpu-bind=cores --overlap pdc_bdcats_clientcache 16777216 1 3 >> bdcats_pdc_clientcache_4nodes.txt
        
        sleep 2
        
        srun -N $N_NODE -n $N_NODE --ntasks-per-node=1 -c 4 --cpu_bind=cores --overlap /path/to/your/installed/close_server
done

echo "Script tasks completed."

