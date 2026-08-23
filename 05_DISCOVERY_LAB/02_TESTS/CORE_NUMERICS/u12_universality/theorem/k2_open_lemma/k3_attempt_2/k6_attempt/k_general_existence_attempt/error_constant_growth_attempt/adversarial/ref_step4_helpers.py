"""Exact D*_r(b) = H_r(1,b) via MY OWN general-b closed form (STEP 4)."""

from fractions import Fraction as Fr
from math import factorial


def _E(v, beta):
    return (3 * v ** 4 + (Fr(9, 2) * beta ** 2 - 3 * beta - 3) * v ** 2
            + (Fr(3, 16) * beta ** 4 - Fr(1, 4) * beta ** 3
               - Fr(3, 4) * beta ** 2 + beta))


def dstar_exact(r, b):
    beta = Fr(b + 1)
    N = 2 * r + b + 1
    Phi = Fr(factorial(r) * factorial(r + b), factorial(N)) * 2 ** N
    bracket = (Fr(3 * N * (3 * N - 2), 16)
               + (Fr(9, 2) * beta ** 2 - 3 * beta - 3) * Fr(N, 4)
               + (Fr(3, 16) * beta ** 4 - Fr(1, 4) * beta ** 3
                  - Fr(3, 4) * beta ** 2 + beta))
    even = Phi * bracket / 48
    for j in range(1, b + 1):
        v = Fr(j) - beta / 2
        pref = Fr(factorial(r) * factorial(r + b),
                  factorial(r + j) * factorial(r + b + 1 - j))
        even -= _E(v, beta) * pref / 48
    odd = -Fr(3 * b + 2, 24) * r - Fr(b * (3 * b + 1) * (b + 2), 48)
    return even + odd
