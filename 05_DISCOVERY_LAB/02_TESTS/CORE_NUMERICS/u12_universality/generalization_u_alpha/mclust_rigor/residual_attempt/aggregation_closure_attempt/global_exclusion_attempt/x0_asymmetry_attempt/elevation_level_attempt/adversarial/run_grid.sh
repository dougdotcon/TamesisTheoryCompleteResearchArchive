#!/bin/bash
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for i in $(seq 0 23); do echo $i; done | xargs -P 2 -I{} sh -c 'python3 ref2_grid.py {} > logs/grid_{}.log 2>&1'
echo ALLDONE > logs/grid_ALLDONE
