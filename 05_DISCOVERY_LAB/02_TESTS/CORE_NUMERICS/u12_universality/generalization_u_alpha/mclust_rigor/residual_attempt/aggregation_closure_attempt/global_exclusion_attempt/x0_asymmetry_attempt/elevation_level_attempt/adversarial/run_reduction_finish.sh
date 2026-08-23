#!/bin/bash
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
for i in 12 14 15 16 17; do
  echo $i
done | xargs -P 4 -I{} sh -c 'python3 ref2_reduction.py {} > logs/red_{}.log 2>&1'
echo ALLDONE > logs/red_finish_ALLDONE
