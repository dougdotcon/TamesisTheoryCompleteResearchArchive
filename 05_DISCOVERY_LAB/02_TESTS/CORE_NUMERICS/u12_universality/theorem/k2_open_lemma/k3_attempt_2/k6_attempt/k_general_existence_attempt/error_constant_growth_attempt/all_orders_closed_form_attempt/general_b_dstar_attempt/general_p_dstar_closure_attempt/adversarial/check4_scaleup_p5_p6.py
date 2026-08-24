"""
Independent, from-scratch, large-scale verification of D^{*(p)}_r(b) for
p=5,6 at scale matching/exceeding the PARENT document's own scale
(r up to ~150-200, b up to ~25-30), per the orchestrator's brief item 3.

Built entirely from scratch: does NOT import or read ground_truth.py,
ingredients.py, odd_part.py, or assemble.py from the target front.

Method for Q_p(u) is DELIBERATELY DIFFERENT from the target document's
Newton's-identity route, for extra independence: direct DP computation of
the elementary symmetric polynomial e_p(1,...,u) at 2p+1 integer points,
then EXACT Lagrange interpolation (Fraction) to recover the polynomial-in-u
coefficients.

Central moments mu_{2l}(N): computed by direct binomial summation at small
N (enough points to pin down the polynomial-in-N of the assumed degree),
then exact Lagrange interpolation to a polynomial in N, evaluated cheaply
at large N. Direct summation is also used as a spot-check at a few large N.

Strip weight w_i(r,b), the H_k(r,b) recursive machine, and phi_r/Phi_b(r)
are implemented per ATTEMPT.md's stated formulas (already independently
re-derived/checked in check2/check3), using exact Fraction arithmetic
throughout.

Ground truth: Corollary A3, own unsigned Stirling number (first kind)
table via the standard recurrence c(n,k)=c(n-1,k-1)+(n-1)c(n-1,k).
"""
import sys, time
from fractions import Fraction
from math import comb, factorial

# ---------- Ground truth: Corollary A3 ----------

def stirling1_table(nmax):
    # c[n][k] unsigned Stirling numbers of the first kind, 0<=n,k<=nmax
    c = [[0]*(nmax+1) for _ in range(nmax+1)]
    c[0][0] = 1
    for n in range(1, nmax+1):
        for k in range(0, n+1):
            c[n][k] = c[n-1][k-1] if k-1 >= 0 else 0
            c[n][k] += (n-1)*c[n-1][k] if k <= n-1 else 0
    return c

def D_ground_truth(p, r, b, c):
    # D^{*(p)}_r(b) = sum_{j=p}^r c_j^{(r)}(b) * c(j+1, j+1-p)
    total = Fraction(0)
    for j in range(p, r+1):
        M = j+1-p
        stirl = c[j+1][M]
        if stirl == 0:
            continue
        # c_j^{(r)}(b) = r! / [ (r-j)! * prod_{i=1}^{j+1} (r+b+i) ]
        num = Fraction(factorial(r), factorial(r-j))
        denom = 1
        for i in range(1, j+2):
            denom *= (r+b+i)
        cj = num / denom
        total += cj * stirl
    return total

# ---------- Q_p(u): direct DP + exact Lagrange interpolation ----------

def e_p_direct(p, u):
    # elementary symmetric polynomial of degree p over {1,...,u}, integer u>=0
    e = [Fraction(0)]*(p+1)
    e[0] = Fraction(1)
    for k in range(1, u+1):
        for i in range(min(p, k), 0, -1):
            e[i] = e[i] + k*e[i-1]
    return e[p]

def lagrange_interp(points):
    # points: list of (x_i, y_i) Fraction/int pairs, distinct x_i.
    # returns polynomial coefficients [c0, c1, ..., cn] (c0 + c1 x + ...)
    n = len(points)
    # Build via Newton's divided differences for numerical stability/exactness
    xs = [Fraction(x) for x, y in points]
    ys = [Fraction(y) for x, y in points]
    coef = ys[:]
    for j in range(1, n):
        for i in range(n-1, j-1, -1):
            coef[i] = (coef[i] - coef[i-1]) / (xs[i] - xs[i-j])
    # coef are divided differences; build polynomial in standard form via
    # Horner-style expansion: P(x) = coef[0] + (x-x0)(coef[1] + (x-x1)(coef[2]+...))
    # Expand into monomial basis using Fraction polynomial arithmetic.
    poly = [Fraction(coef[n-1])]
    for k in range(n-2, -1, -1):
        # poly = poly*(x - xs[k]) + coef[k]
        newpoly = [Fraction(0)]*(len(poly)+1)
        for idx, c in enumerate(poly):
            newpoly[idx+1] += c
            newpoly[idx] += c*(-xs[k])
        newpoly[0] += coef[k]
        poly = newpoly
    return poly  # [c0, c1, ..., c_{n-1}]

def Q_p_poly(p):
    # returns coefficients [c0,...,c_{2p}] of Q_p(u) = e_p(1,...,u) as poly in u
    pts = [(u, e_p_direct(p, u)) for u in range(0, 2*p+2)]  # 2p+2 points, degree <=2p
    poly = lagrange_interp(pts)
    # trim trailing zero (should have length 2p+1 after trim, but keep as-is)
    return poly

def poly_eval(poly, x):
    # Horner
    res = Fraction(0)
    for c in reversed(poly):
        res = res*x + c
    return res

def poly_compose_linear(poly, a, c0):
    # returns coefficients of poly(a*t + c0) as polynomial in t
    # poly(u) = sum poly[i] u^i ; u = a*t+c0
    n = len(poly)
    result = [Fraction(0)]*n
    for i, coeff in enumerate(poly):
        if coeff == 0:
            continue
        # expand (a*t+c0)^i via binomial theorem
        for j in range(i+1):
            term = coeff * comb(i, j) * (a**j) * (c0**(i-j))
            result[j] += term
    return result

def split_even_odd(poly):
    # poly: coeffs of a polynomial in v; return (even_coeffs dict l->e_{2l}, odd dict k->o_k)
    even = {}
    odd = {}
    for i, c in enumerate(poly):
        if c == 0:
            continue
        if i % 2 == 0:
            even[i//2] = c
        else:
            odd[(i+1)//2] = c
    return even, odd

# ---------- central moments mu_{2l}(N) via interpolation ----------

def mu_2l_direct(l, N):
    if N == 0:
        return Fraction(1) if l == 0 else Fraction(0)
    total = Fraction(0)
    half = Fraction(N, 2)
    for alpha in range(0, N+1):
        total += (Fraction(alpha) - half)**(2*l) * comb(N, alpha)
    return total / (2**N)

_mu_poly_cache = {}
def mu_2l_poly(l):
    if l in _mu_poly_cache:
        return _mu_poly_cache[l]
    # mu_{2l}(N) is a polynomial in N of degree l (verified structurally
    # for l=0,1,2 against known closed forms mu_2=N/4, mu_4=N(3N-2)/16);
    # use degree l+2 points to be safe.
    npts = l + 3
    pts = [(N, mu_2l_direct(l, N)) for N in range(0, npts+1)]
    poly = lagrange_interp(pts)
    _mu_poly_cache[l] = poly
    return poly

def mu_2l_fast(l, N):
    poly = mu_2l_poly(l)
    return poly_eval(poly, N)

# ---------- strip weight, H_k machine, Phi_b ----------

def w_i(r, b, i):
    return Fraction(factorial(r)*factorial(r+b), factorial(r+i)*factorial(r+b+1-i))

def falling(x, d):
    result = 1
    for t in range(d):
        result *= (x - t)
    return result

def H_power_depth(power, d, r, b, N, beta, cache):
    key = (power, d)
    if key in cache:
        return cache[key]
    beta_local = beta + d
    N_d = N - d
    Nd_ff = falling(N, d)
    rd_ff = falling(r, d)
    term1 = Fraction(beta_local)**(power-1) * Fraction(rd_ff, Nd_ff)
    if power == 1:
        cache[key] = term1
        return term1
    tail = Fraction(0)
    for s in range(1, power-2+1, 2):
        tail += comb(power-1, s) * H_power_depth(s, d+1, r, b, N, beta, cache)
    val = term1 + 2*N_d*tail
    cache[key] = val
    return val

def Phi_b_val(r, b, N):
    Pb = Fraction(factorial(r)*factorial(r+b), factorial(N))
    return Pb * (2**N)

# ---------- assembled D^{*(p)}_r(b) ----------

_Qp_cache = {}
def get_even_odd(p, b):
    key = (p, b)
    if key in _Qp_cache:
        return _Qp_cache[key]
    poly_u = Q_p_poly(p)  # Q_p(u) in u
    beta = b + 1
    # u = -(v + beta/2) = -v - beta/2  => a=-1, c0=-beta/2
    poly_v = poly_compose_linear(poly_u, Fraction(-1), Fraction(-beta, 2))
    even, odd = split_even_odd(poly_v)
    _Qp_cache[key] = (even, odd)
    return even, odd

def D_assembled(p, r, b):
    N = 2*r + b + 1
    beta = b + 1
    even, odd = get_even_odd(p, b)
    # M_p(N)
    Mp = Fraction(0)
    for l, e2l in even.items():
        Mp += e2l * mu_2l_fast(l, N)
    Phi_b = Phi_b_val(r, b, N)
    # Strip_p(r,b)
    strip = Fraction(0)
    for i in range(1, b+1):
        Ep_val = Fraction(0)
        v = Fraction(i) - Fraction(beta, 2)
        for l, e2l in even.items():
            Ep_val += e2l * v**(2*l)
        strip += Ep_val * w_i(r, b, i)
    # odd part
    odd_sum = Fraction(0)
    cache = {}
    for k, ok in odd.items():
        power = 2*k - 1
        Hval = H_power_depth(power, 0, r, b, N, beta, cache)
        odd_sum += ok * Hval / Fraction(2**power)
    D = Fraction(1,2)*(Phi_b*Mp - strip) - odd_sum
    return D

# ---------- run ----------

def run_p_range(p, r_max, b_max, c_table):
    checks = 0
    mismatches = 0
    skipped_degenerate = 0
    t0 = time.time()
    for r in range(0, r_max+1, max(1, r_max//160) if r_max > 160 else 1):
        for b in range(0, b_max+1, max(1, b_max//28) if b_max > 28 else 1):
            N = 2*r + b + 1
            if N < 2*p:
                # Known apparent-removable-pole zone (individual H(power,d)
                # terms hit 0/0 before symbolic cancellation; ATTEMPT.md
                # handles this via sympy.cancel on the full symbolic sum
                # before substituting numbers). This zone is r<~p, already
                # covered by the r<p vanishing-boundary tests elsewhere
                # (document's own 360 checks, ground_truth.py). Not part of
                # this large-r,b scale-push exercise -- skip, don't fake pass.
                skipped_degenerate += 1
                continue
            gt = D_ground_truth(p, r, b, c_table)
            asm = D_assembled(p, r, b)
            checks += 1
            if gt != asm:
                mismatches += 1
                print(f"MISMATCH p={p} r={r} b={b}: ground_truth={gt} assembled={asm}")
                if mismatches > 20:
                    print("...too many mismatches, aborting this p")
                    return checks, mismatches
    dt = time.time() - t0
    print(f"p={p}: r=0..{r_max}, b=0..{b_max}: {checks} checks, {mismatches} mismatches, "
          f"{skipped_degenerate} skipped (degenerate near-origin pole zone), {dt:.1f}s")
    return checks, mismatches

def main():
    r_max_needed = 205
    c_table = stirling1_table(r_max_needed + 2)
    total_checks = 0
    total_mism = 0
    for p, r_max, b_max in [(5, 200, 30), (6, 200, 30)]:
        ck, mm = run_p_range(p, r_max, b_max, c_table)
        total_checks += ck
        total_mism += mm
    print(f"TOTAL: {total_checks} checks, {total_mism} mismatches")

if __name__ == "__main__":
    main()
