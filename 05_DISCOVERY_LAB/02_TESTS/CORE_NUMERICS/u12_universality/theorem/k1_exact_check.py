import itertools
from fractions import Fraction

def cyclic_count(f, n):
    # f: dict 1..n -> 1..n
    cnt = 0
    for x in range(1, n+1):
        y = f[x]
        steps = 0
        seen_x_again = False
        cur = x
        for _ in range(n+2):
            cur = f[cur]
            steps += 1
            if cur == x:
                seen_x_again = True
                break
        if seen_x_again:
            cnt += 1
    return cnt

for n in range(1, 8):
    total = Fraction(0)
    count = 0
    istar = 1
    for perm in itertools.permutations(range(1, n+1)):
        pi = {i+1: perm[i] for i in range(n)}
        for U in range(1, n+1):
            f = dict(pi)
            f[istar] = U
            c = cyclic_count(f, n)
            total += Fraction(c, n)
            count += 1
    phi = total / count
    formula = Fraction(2,3) + Fraction(1, 3*n*n)
    print(n, phi, formula, phi == formula)
