#!/usr/bin/env python3
"""
ADVERSARIAL / INDEPENDENT re-implementation of the (P,Q)-family recursion
for the abstract M-CLUST(b) floor process, built ENTIRELY from the prose
of ATTEMPT.md Section 0 and Section 1.1 (the PDE system of record, the
recursion of record, and the author's own prose description of how the
(P,Q) ansatz closes the b_k ODE) -- NO .py script from this front, wave-16,
or wave-14 was opened, read, or imported, per mandate.

This referee independently re-derives (on paper, reproduced in the docstring
below) the recursion from the PDE system BEFORE writing any code, then
implements the closed-form (P,Q)-family solve from scratch.

=====================================================================
INDEPENDENT RE-DERIVATION OF THE RECURSION FROM THE PDE (referee's own)
=====================================================================
PDE system of record (ATTEMPT.md Sec.0, citing wave-14 Sec.5):
    dPhi/ds - dPhi/dg = c(Phi - W)
    dPsi/ds            = c(Psi - W)
    W = g*Avg_g[Phi] + (1-s-g)*Psi ,  Avg_g[Phi] = (1/g) int_0^g Phi dg'
    Phi(s,0) = 1

Write Phi(s,g) = sum_k a_k(s) g^k  (a_0=1 forced by Phi(s,0)=1),
      Psi(s,g) = sum_k b_k(s) g^k  (b_0 = 0, forced below).

Avg_g[Phi] = (1/g) int_0^g sum_k a_k g'^k dg' = sum_k a_k g^k/(k+1).
g*Avg_g[Phi] = sum_k a_k g^{k+1}/(k+1) = sum_{j>=1} [a_{j-1}/j] g^j.
g*Psi = sum_k b_k g^{k+1} = sum_{j>=1} b_{j-1} g^j.
So W = sum_{j>=1} [a_{j-1}/j] g^j + (1-s)*sum_k b_k g^k - sum_{j>=1} b_{j-1} g^j
     = sum_j w_j g^j ,  w_0 = (1-s) b_0 ,
       w_j = a_{j-1}/j + (1-s) b_j - b_{j-1}   (j>=1).
[If b_0=0 then w_0=0 -- consistent with the recursion of record having no
 j=0 case listed.]

dPhi/dg = sum_k k a_k g^{k-1} = sum_k (k+1) a_{k+1} g^k.
dPhi/ds = sum_k a_k'(s) g^k.
PDE: sum a_k' g^k - sum (k+1)a_{k+1} g^k = c sum (a_k - w_k) g^k
 => (k+1) a_{k+1} = a_k' - c a_k + c w_k
 => a_{k+1} = [a_k' - c a_k + c w_k]/(k+1).           <-- MATCHES record.

dPsi/ds = c(Psi-W): sum b_k' g^k = c sum (b_k - w_k) g^k
 => b_k' = c b_k - c w_k = c b_k - c[a_{k-1}/k + (1-s)b_k - b_{k-1}]
         = c s b_k - c a_{k-1}/k + c b_{k-1}   (using 1-(1-s)=s)
 => b_k' - c s b_k = -c a_{k-1}/k + c b_{k-1}.        <-- MATCHES record.

(k=0 case of the b-recursion: b_0' = c s b_0, so b_0 = const * e^{c s^2/2};
 the ONLY bounded solution is b_0=0, forced -- this is the origin of the
 "bounded branch" instruction and is consistent with b_1 = psi1 being the
 FIRST nonzero b-coefficient in the record.)

CONFIRMED: the stated recursion follows directly and uniquely from the
stated PDE system. This referee did not need to (and was not asked to)
re-derive the PDE system itself from anything further upstream -- it is
accepted per mandate as an established, wave-14/16-proved input.
=====================================================================

FRESH (P,Q)-FAMILY IMPLEMENTATION (referee's own, from ATTEMPT.md Sec 1.1
prose only):

E(s) := erfcx(s*sqrt(c/2)).  Identity (referee-verified below, independently,
via erfcx'(z) = 2z*erfcx(z) - 2/sqrt(pi) and the chain rule):
    E'(s) = c*s*E(s) - sc ,   sc := sqrt(2c/pi).

Every a_k, b_k is represented as a pair of polynomials (P,Q) in s, meaning
value = P(s) + Q(s)*E(s). This ansatz is closed under:
  - d/ds:            (P+QE)' = (P' - sc*Q) + (Q' + c*s*Q)*E
  - mult by (1-s):    (1-s)(P+QE) = (1-s)P + (1-s)Q * E
  - linear combos:    trivial
  - "integrate the b_k ODE": b_k' - c*s*b_k = A(s) + B(s)*E(s), for
    polynomial A, B, is solved by b_k = U(s) + V(s)*E(s) with
       V' = B                      => V = integral(B) + kappa  (kappa free)
       U' - c*s*U = A + sc*V =: R  => match s^j coefficients:
           (j+1) u_{j+1} - c*u_{j-1} = r_j   for all j>=0 (u_{-1}:=0)
       Since -c*s*U must dominate U' in top degree, deg(R) = deg(U)+1 =: D+1.
       Solve DESCENDING: j = D+1, D, ..., 1 gives u_D, u_{D-1}, ..., u_0
       (using u_{j+1}=0 for j+1>D as the top boundary condition), leaving
       the j=0 equation u_1 = r_0 UNUSED by the descending pass (since it
       relates index 1 to index -1, and u_1 is already pinned by the
       descending pass whenever D>=1) -- this PINS kappa:
           r_0 = A_0 + sc*(Vbase_0 + kappa) = A_0 + sc*kappa   [Vbase_0=0
           always, since integral(B) has no constant term]
        => kappa = (u_1 - A_0) / sc.

This closed-form solve is EXACT (no numerical ODE integration, no
truncation beyond finite polynomial degree) at whatever precision the
scalar arithmetic (c, sc, and all coefficients) is carried at.
"""
import sys, time, json
import mpmath as mp

# ---------- polynomial helpers (lists of mpf, index i = coeff of s^i) ----------

def ptrim(A):
    A = list(A)
    while len(A) > 1 and A[-1] == 0:
        A.pop()
    if len(A) == 0:
        A = [mp.mpf(0)]
    return A

def padd(A, B):
    n = max(len(A), len(B))
    out = [mp.mpf(0)] * n
    for i, a in enumerate(A):
        out[i] += a
    for i, b in enumerate(B):
        out[i] += b
    return out

def pscale(A, s):
    return [a * s for a in A]

def psub(A, B):
    return padd(A, pscale(B, -1))

def pderiv(A):
    if len(A) <= 1:
        return [mp.mpf(0)]
    return [A[i] * i for i in range(1, len(A))]

def pshift(A):  # multiply by s
    return [mp.mpf(0)] + list(A)

def pmul_1ms(A):  # multiply by (1-s)
    return psub(A, pshift(A))

def pintegral(A):  # antiderivative with zero constant term
    return [mp.mpf(0)] + [A[i] / (i + 1) for i in range(len(A))]

def erfcx(z):
    # scaled complementary error function; mpmath has no builtin erfcx.
    # erfc() is computed to full relative precision by mpmath even for
    # large z (asymptotic/continued-fraction internally, not via 1-erf),
    # and mpf multiplication does not lose relative precision to magnitude,
    # so erfc(z)*exp(z^2) is accurate to full working precision.
    return mp.erfc(z) * mp.exp(z * z)

def peval(A, x):
    # Horner
    r = mp.mpf(0)
    for a in reversed(A):
        r = r * x + a
    return r

# ---------- combined (P,Q) element operations ----------

def comb_add(E1, E2):
    P1, Q1 = E1; P2, Q2 = E2
    return (padd(P1, P2), padd(Q1, Q2))

def comb_scale(E1, s):
    P1, Q1 = E1
    return (pscale(P1, s), pscale(Q1, s))

def comb_sub(E1, E2):
    return comb_add(E1, comb_scale(E2, -1))

def comb_mul_1ms(E1):
    P1, Q1 = E1
    return (pmul_1ms(P1), pmul_1ms(Q1))

def comb_deriv(E1, c, sc):
    P, Q = E1
    newP = psub(pderiv(P), pscale(Q, sc))
    newQ = padd(pderiv(Q), pscale(pshift(Q), c))
    return (newP, newQ)

def comb_eval(E1, s, c):
    P, Q = E1
    Es = erfcx(s * mp.sqrt(c / 2))
    return peval(P, s) + peval(Q, s) * Es

# ---------- the b_k ODE solve: b' - c*s*b = A + B*E ----------

def solve_ode(A, B, c, sc):
    Vbase = pintegral(B)
    R = padd(A, pscale(Vbase, sc))
    Rt = ptrim(R)
    if all(x == 0 for x in Rt):
        D = -1
    else:
        D = len(Rt) - 1 - 1  # degR - 1
    if D < 0:
        u = [mp.mpf(0)]
        u1 = mp.mpf(0)
    else:
        u_arr = [mp.mpf(0)] * (D + 2)  # indices 0..D+1 ; index D+1 stays 0
        for j in range(D + 1, 0, -1):
            ujp1 = u_arr[j + 1] if (j + 1) <= (D + 1) else mp.mpf(0)
            rj = Rt[j] if j < len(Rt) else mp.mpf(0)
            u_arr[j - 1] = ((j + 1) * ujp1 - rj) / c
        u = u_arr[0:D + 1]
        u1 = u[1] if len(u) > 1 else mp.mpf(0)
    A0 = A[0] if len(A) > 0 else mp.mpf(0)
    kappa = (u1 - A0) / sc
    V = list(Vbase)
    if len(V) == 0:
        V = [mp.mpf(0)]
    V[0] = V[0] + kappa
    U = u if len(u) > 0 else [mp.mpf(0)]
    return (ptrim(U), ptrim(V))

# ---------- build the family up to order K ----------

def build_family(c, K):
    c = mp.mpf(c)
    sc = mp.sqrt(2 * c / mp.pi)
    ONE = ([mp.mpf(1)], [mp.mpf(0)])
    a = [ONE]  # a[0]
    a.append(([-c], [mp.mpf(0)]))  # a[1] = -c
    b = [([mp.mpf(0)], [mp.mpf(0)])]  # b[0] = 0
    b.append(([mp.mpf(0)], [mp.sqrt(mp.pi * c / 2)]))  # b[1] = sqrt(pi c/2) * E

    zero = ([mp.mpf(0)], [mp.mpf(0)])

    for j in range(1, K):
        # w_j = a_{j-1}/j + (1-s) b_j - b_{j-1}
        bjm1 = b[j - 1] if (j - 1) >= 0 else zero
        term1 = comb_scale(a[j - 1], mp.mpf(1) / j)
        term2 = comb_mul_1ms(b[j])
        w_j = comb_sub(comb_add(term1, term2), bjm1)

        # a_{j+1} = [a_j' - c a_j + c w_j] / (j+1)
        ajp = comb_deriv(a[j], c, sc)
        rhs = comb_sub(comb_add(ajp, comb_scale(w_j, c)), comb_scale(a[j], c))
        a_next = comb_scale(rhs, mp.mpf(1) / (j + 1))
        a.append(a_next)

        # b_{j+1} solves: b' - c s b = -c a_j/(j+1) + c b_j
        Acoef = comb_scale(a[j], -c / (j + 1))
        Bcoef = comb_scale(b[j], c)
        RHS = comb_add(Acoef, Bcoef)  # (P,Q) form; A=P-part, B=Q-part
        Ppart, Qpart = RHS
        U, V = solve_ode(Ppart, Qpart, c, sc)
        b.append((U, V))

    return a, b


if __name__ == "__main__":
    print("smoke test placeholder")
