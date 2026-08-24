"""
Independent check (built from scratch, not reading odd_part.py or the
referee's abel_identities.py): brute-force S_{2k-1}(N,m) vs the recursion
stated in the target ATTEMPT.md (Section 0, item 2), for k=9,10
(powers 17,19) -- the specific gap flagged in the target document's own
Section 6.

Recursion as literally quoted in ATTEMPT.md:
  S_{2k-1}(N,m) = (N-2m)^{2k-2}(m+1)C(N,m+1)
                  + 2N * sum_{s odd, 1<=s<=2k-3} C(2k-2,s) S_s(N-1,m-1)
  base case S_1(N,m) = (m+1) C(N,m+1)

Brute force definition (also from ATTEMPT.md's citation, Part 1 of the
wave-14 referee report):
  S_{2k-1}(N,m) = sum_{i=0}^{m} (N-2i)^{2k-1} * C(N,i)
"""
from fractions import Fraction
from math import comb

def S_bruteforce(power, N, m):
    # power must be odd
    total = 0
    for i in range(0, m+1):
        total += (N - 2*i)**power * comb(N, i)
    return total

_cache = {}
def S_recursion(power, N, m):
    # power odd, power=2k-1
    if power == 1:
        if m < -1:
            return 0
        if m == -1:
            return 0
        return (m+1)*comb(N, m+1)
    key = (power, N, m)
    if key in _cache:
        return _cache[key]
    if m < 0:
        _cache[key] = 0
        return 0
    n = power - 1  # even, = 2k-2
    term1 = (N - 2*m)**n * (m+1) * comb(N, m+1)
    tail = 0
    for s in range(1, n-1+1, 2):  # odd s, 1 <= s <= 2k-3 = n-1
        tail += comb(n, s) * S_recursion(s, N-1, m-1)
    val = term1 + 2*N*tail
    _cache[key] = val
    return val

def run():
    mismatches = 0
    checks = 0
    for k in (9, 10, 12):
        power = 2*k - 1
        for N in range(1, 41):
            for m in range(-1, N+1):
                bf = S_bruteforce(power, N, m) if m >= 0 else 0
                rec = S_recursion(power, N, m)
                checks += 1
                if bf != rec:
                    mismatches += 1
                    print(f"MISMATCH k={k} power={power} N={N} m={m}: bruteforce={bf} recursion={rec}")
    print(f"k=9,10 (powers 17,19): {checks} checks, {mismatches} mismatches")

if __name__ == "__main__":
    run()
