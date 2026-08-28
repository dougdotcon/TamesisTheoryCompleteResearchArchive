"""
ADVERSARIAL SCRIPT 1 -- Fresh, from-scratch re-derivation and cross-check
of:
  (A) true Definition-4 brute force (ground truth), general K,
  (B) the "raw" unconditional CDF via Proposition S + elementary lattice
      count (Estagio 41's Proposition S, cited from THEOREM.md prose --
      NOT read from any .py file),
  (C) the exchangeability-reduced S_r formula the target ATTEMPT.md's
      Section 3 claims,
  (D) the three already-proved closed forms D1 (K=1), D2 (K=2), D3 (K=3).

Written entirely from scratch by the adversarial referee, without reading
any .py file from the target front or any ancestor front. All arithmetic
exact (Python Fraction / int), no floating point.
"""
import itertools
from fractions import Fraction
from math import comb, factorial

# ---------------------------------------------------------------------
# (A) True Definition-4 brute force (ground truth)
# ---------------------------------------------------------------------

def cyclic_points(f, n):
    """Standard O(n) functional-graph cyclic-node detector."""
    color = [0] * n  # 0=white,1=gray,2=black
    is_cyclic = [False] * n
    for start in range(n):
        if color[start] != 0:
            continue
        path = []
        x = start
        while color[x] == 0:
            color[x] = 1
            path.append(x)
            x = f[x]
        if color[x] == 1:
            idx = path.index(x)
            for node in path[idx:]:
                is_cyclic[node] = True
        for node in path:
            color[node] = 2
    return is_cyclic


def bruteforce_cdf(n, K):
    """Exact P(T<=k) for every k=0..n, true Definition 4, K reroute
    sources fixed at {0,...,K-1}. Returns list of Fraction, length n+1."""
    counts = [0] * (n + 1)
    total = 0
    for pi in itertools.permutations(range(n)):
        for U in itertools.product(range(n), repeat=K):
            f = list(pi)
            for i in range(K):
                f[i] = U[i]
            ic = cyclic_points(f, n)
            T = sum(ic)
            counts[T] += 1
            total += 1
    cdf = []
    running = 0
    for k in range(n + 1):
        running += counts[k]
        cdf.append(Fraction(running, total))
    return cdf, total


# ---------------------------------------------------------------------
# (B) Raw unconditional CDF via Proposition S + elementary lattice count
# ---------------------------------------------------------------------

def count_le(Ls, t):
    """Count_r(L_1,...,L_r; t) := #{v in Z^r : 1<=v_i<=L_i, sum v_i<=t}.
    Computed by DP convolution (bounded, exact integer counts), NOT by
    brute enumeration of all v-tuples (too slow for larger L)."""
    r = len(Ls)
    if r == 0:
        return 1 if t >= 0 else 0
    maxS = sum(Ls)
    # dp[s] = number of ways to choose v_1..v_j with 1<=v_i<=L_i summing to s
    dp = [0] * (maxS + 1)
    dp[0] = 1
    cur_max = 0
    for L in Ls:
        new_max = cur_max + L
        ndp = [0] * (maxS + 1)
        # prefix sums of dp over window [s-L, s-1]
        prefix = [0] * (maxS + 2)
        for s in range(maxS + 1):
            prefix[s + 1] = prefix[s] + dp[s]
        for s in range(1, new_max + 1):
            lo = max(0, s - L)
            hi = s - 1
            if hi < 0:
                continue
            ndp[s] = prefix[hi + 1] - prefix[lo]
        dp = ndp
        cur_max = new_max
    tt = min(t, maxS)
    if tt < 0:
        return 0
    return sum(dp[0:tt + 1])


def compositions_of_gaps(n, K):
    """Yield (L_0,...,L_{K-1}, O) uniform over compositions of n-K into
    K+1 nonnegative gap-parts (g_0,...,g_{K-1},O), L_s=g_s+1.
    Equivalently L_i>=1 (i=0..K-1), O>=0, sum L_i + O = n."""
    # stars and bars over gaps g_0..g_{K-1},O >= 0 summing to n-K
    total = n - K
    if K == 0:
        yield (O,) if False else None
        return
    def rec(remaining, parts_left):
        if parts_left == 1:
            yield (remaining,)
            return
        for g in range(remaining + 1):
            for rest in rec(remaining - g, parts_left - 1):
                yield (g,) + rest
    for gaps_and_O in rec(total, K + 1):
        gaps = gaps_and_O[:K]
        O = gaps_and_O[K]
        Ls = tuple(g + 1 for g in gaps)
        yield Ls, O


def prop_S(Ls, O, n, A):
    """P(S=A|L) via Estagio 41's K-free Proposition S, cited from
    THEOREM.md prose:
      P(S=A) = |A|! * prod_{a in A} p_a * (p_D + sum_{a in A} p_a)
    p_a = L_a/n, p_D = O/n. Returns exact Fraction."""
    m = len(A)
    prod_p = Fraction(1, 1)
    sum_p = Fraction(0, 1)
    for a in A:
        pa = Fraction(Ls[a], n)
        prod_p *= pa
        sum_p += pa
    pD = Fraction(O, n)
    return factorial(m) * prod_p * (pD + sum_p)


def raw_unconditional_cdf(n, K, k):
    """Section-1-style setup: average over the composition simplex of
    sum_{A subseteq {0,...,K-1}} P(S=A|L) * Count_{|A|}(L_A;k-O) /
    prod_{a in A} L_a.
    Built fresh from Proposition S + the elementary lattice count, with
    NO reference to the target front's own reduction (Section 3)."""
    subsets = []
    idxs = list(range(K))
    for r in range(K + 1):
        subsets.extend(itertools.combinations(idxs, r))
    total_num = Fraction(0, 1)
    ncomps = 0
    for Ls, O in compositions_of_gaps(n, K):
        ncomps += 1
        t = k - O
        term_sum = Fraction(0, 1)
        for A in subsets:
            r = len(A)
            LA = tuple(Ls[a] for a in A)
            prodL = 1
            for x in LA:
                prodL *= x
            cnt = count_le(LA, t)
            ps = prop_S(Ls, O, n, A)
            if r == 0:
                # empty subset: Count_0(;t) = 1 if t>=0 else 0, prod=1 (empty product)
                term = ps * cnt
            else:
                term = ps * Fraction(cnt, prodL)
            term_sum += term
        total_num += term_sum
    assert ncomps == comb(n, K), (ncomps, comb(n, K))
    return total_num / ncomps


# ---------------------------------------------------------------------
# (C) Exchangeability-reduced S_r formula (re-derived from scratch from
#     Prop S + the algebraic cancellation, per the target ATTEMPT.md's
#     own stated Section 3 claim -- re-derived, not copied from any code)
# ---------------------------------------------------------------------

def S_r_raw(n, K, k, r):
    """S_r(n,K,k) := sum over the FULL composition simplex of
       (O+Sigma) * Count_r(L_0,...,L_{r-1} ; k-O),  Sigma := L_0+...+L_{r-1}
    Computed by direct enumeration of the composition simplex (own,
    independent implementation)."""
    total = Fraction(0, 1)
    for Ls, O in compositions_of_gaps(n, K):
        rep = Ls[:r]
        Sigma = sum(rep)
        t = k - O
        cnt = count_le(rep, t)
        total += (O + Sigma) * cnt
    return total


def exchangeability_cdf(n, K, k):
    """P(T<=k) = (1/C(n,K)) * sum_{r=0}^K C(K,r) * r!/n^{r+1} * S_r(n,K,k)
    -- the exchangeability reduction claimed in the target's Section 2/3,
    re-derived here purely algebraically from Proposition S (see the
    derivation note in this script's header/docstring above) and cross-
    checked against the raw per-subset engine (B)."""
    total = Fraction(0, 1)
    for r in range(K + 1):
        Sr = S_r_raw(n, K, k, r)
        total += Fraction(comb(K, r) * factorial(r), n ** (r + 1)) * Sr
    return total / comb(n, K)


# ---------------------------------------------------------------------
# (D) The three already-proved closed forms
# ---------------------------------------------------------------------

def D1(n, k):
    return Fraction(k * (k + 1), n ** 2)


def D2(n, k):
    num = k * (k + 1) * (2 * n**2 - 3 * n + k - k**2)
    den = n**3 * (n - 1)
    return Fraction(num, den)


def D3(n, k):
    num = k*(k+1)*(k**4 - 4*k**3 - (3*n**2-9*n-5)*k**2 + (3*n**2-11*n-2)*k
                    + (3*n**4-12*n**3+12*n**2+2*n))
    den = n**4 * (n-1) * (n-2)
    return Fraction(num, den)


if __name__ == "__main__":
    print("=" * 70)
    print("PART 1: raw (B) vs exchangeability-reduced (C), general K,")
    print("  K=4,5,6, several n,k -- both built fully independently from")
    print("  scratch by the adversarial referee.")
    print("=" * 70)
    all_ok = True
    cases = []
    for K in (4, 5, 6):
        for n in range(K + 1, K + 5):
            for k in range(0, n + 1):
                cases.append((n, K, k))
    for (n, K, k) in cases:
        b = raw_unconditional_cdf(n, K, k)
        c = exchangeability_cdf(n, K, k)
        ok = (b == c)
        all_ok &= ok
        if not ok:
            print(f"  MISMATCH n={n} K={K} k={k}: raw={b} exch={c}")
    print(f"Checked {len(cases)} (n,K,k) triples, K in (4,5,6).")
    print("ALL MATCH (raw vs exchangeability-reduced):", all_ok)

    print()
    print("=" * 70)
    print("PART 2: raw/exchangeability vs D1/D2/D3, sample re-check")
    print("=" * 70)
    ok2 = True
    for n in range(3, 9):
        for k in range(0, n):
            c1 = exchangeability_cdf(n, 1, k)
            d1 = D1(n, k)
            if c1 != d1:
                ok2 = False
                print("D1 mismatch", n, k, c1, d1)
            c2 = exchangeability_cdf(n, 2, k)
            d2 = D2(n, k)
            if c2 != d2:
                ok2 = False
                print("D2 mismatch", n, k, c2, d2)
            if n >= 3:
                c3 = exchangeability_cdf(n, 3, k)
                d3 = D3(n, k)
                if c3 != d3:
                    ok2 = False
                    print("D3 mismatch", n, k, c3, d3)
    print("D1/D2/D3 cross-check ALL MATCH:", ok2)

    print()
    print("=" * 70)
    print("PART 3: true Definition-4 brute force (ground truth) vs")
    print("  raw (B) and exchangeability-reduced (C), at (n,K) pairs")
    print("  BEYOND what the target front's own brute force covered")
    print("  (front covered (4,1),(4,2),(5,2),(5,3),(6,3) for Section 1,")
    print("  and (5,2),(6,3) for Section 3's S_r check).")
    print("=" * 70)
    new_pairs = [(5, 4), (6, 4), (7, 3)]
    for (n, K) in new_pairs:
        print(f"--- (n,K)=({n},{K}) ---")
        cdf_bf, total = bruteforce_cdf(n, K)
        print(f"  total configurations: {total}")
        ok3 = True
        for k in range(0, n + 1):
            b = raw_unconditional_cdf(n, K, k)
            c = exchangeability_cdf(n, K, k)
            bf = cdf_bf[k]
            if not (b == c == bf):
                ok3 = False
                print(f"  MISMATCH k={k}: raw={b} exch={c} bruteforce={bf}")
        print(f"  ALL k=0..{n} MATCH (raw, exchangeability, bruteforce):", ok3)
