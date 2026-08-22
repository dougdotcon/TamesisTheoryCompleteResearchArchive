import itertools
from fractions import Fraction
import time

def cyclic_count(f, n):
    cnt = 0
    for x in range(1, n+1):
        cur = x
        found = False
        for _ in range(n+1):
            cur = f[cur]
            if cur == x:
                found = True
                break
        if found:
            cnt += 1
    return cnt

for n in range(2, 9):
    t0=time.time()
    total = Fraction(0)
    count = 0
    i1, i2 = 1, 2
    for perm in itertools.permutations(range(1, n+1)):
        pi = {i+1: perm[i] for i in range(n)}
        for U1 in range(1, n+1):
            for U2 in range(1, n+1):
                f = dict(pi)
                f[i1] = U1
                f[i2] = U2
                c = cyclic_count(f, n)
                total += Fraction(c, n)
                count += 1
    phi = total / count
    wallis = Fraction(8,15)
    dev = phi - wallis
    print(n, phi, float(phi), "dev=", dev, float(dev), "n^2*dev=", float(dev)*n*n, "time", round(time.time()-t0,1))
