import sys; sys.setrecursionlimit(200000)
from fractions import Fraction as Fr
from math import log
import core as C
print('%5s | %-18s %-18s %-10s %-12s %-12s'%('r','S_r(0)','D*_r(0)','S/D*','S_r/r^1.5','loglog slope'))
prev=prevr=None
for r in list(range(4,60,4))+list(range(60,161,10)):
    n=r+1; ch=C.Chain(n)
    s=abs(C.R_resid(ch,r,n,0))*n*n; d=C.H(r,0).eval(Fr(1))
    fs=float(s)
    sl=(log(fs/prev)/log(r/float(prevr))) if prev else float('nan')
    print('%5d | %-18.9f %-18.9f %-10.5f %-12.7f %-12.6f'%(r,fs,float(d),float(s/d),fs/r**1.5,sl))
    prev,prevr=fs,r
