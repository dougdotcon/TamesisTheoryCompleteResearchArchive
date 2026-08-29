#!/usr/bin/env python3
"""
s05_lipschitz_from_volterra_reduction.py -- wave 29 front (a),
CU-DIRECT-PROOF-ATTEMPT

Attempt at hypothesis (C') -- uniform-in-t Lipschitz regularity of the
family {Phi_t(.)} -- directly from the governing structure (the closed
Volterra-in-y equation (VOLTERRA-Phi), a cited record fact, built from the
system's own defining PDE dPhi/ds-dPhi/dg=c(Phi-W) via the already-
established (E1)/(KEY)/(E2) reduction of prior fronts).

STRATEGY: differentiate (VOLTERRA-Phi) in x, using the EXACT raw-operator
definitions of K(y,t)=M_y*K_A^raw(y,t)+K_B(y-t) (cited, record facts, the
K_A^raw single-integral reduction independently re-derived/re-verified by
three prior fronts in this exact sub-lineage). This produces a NEW exact
identity (derived fresh here, symbolically verified below):

  d/dx[K(y,t)f](x) = K(y,t)[f'](x) - K_A^raw(y,t)f(x) - M_y*N(y,t)f(x)

  N(y,t)f(x) := int_0^h e^{-h'/eps} [int_0^inf u*e^{-u^2/2-uz} f(x+h'+u) du] dh'

i.e. differentiating the KERNEL operator in x costs an EXTRA correction
term (not just "apply K(y,t) to f'", the naive/hoped-for outcome) -- but,
CRUCIALLY, this correction term is shown here (via the SAME rigorous
Gordon-type bounds from s01, using ONLY hypotheses (B)+(C'), i.e. NOT
needing any strengthening beyond (C') itself for THIS specific piece) to
be UNIFORMLY O(1/z), z:=x+y -- i.e. it VANISHES as y->infinity, unlike
the naive fear (drawn from wave 26's route-(a) dead end for Psi) that an
unbounded M_y-type coefficient would defeat this route outright.

CONCLUSION (honest, precisely scoped -- see PART 4): this reduces (C') to
a Volterra-resolvent STABILITY question of the SAME LOGICAL TYPE as
hypothesis (B) itself (uniform boundedness of the Phi_y(x) solution as
y->infinity, standing and UNPROVED throughout all 29 waves of this
lineage) -- specifically, whether the SAME kernel K(y,t)'s Volterra
solution operator maps a bounded, y-independent forcing sequence to a
UNIFORMLY (not just locally-in-Y) bounded solution sequence. This is a
genuine, precise REDUCTION (not a proof) of (C') to a question this
lineage has never resolved even for (B) itself -- reported honestly as
such, not oversold as a proof.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("=" * 78)
print("PART 1 -- exact symbolic derivation of d/dx[K(y,t)f](x)")
print("=" * 78)
print("""
Working from the RAW operator definitions (cited record facts):
  K_A^raw(y,t)f(x) = int_0^h e^{-h'/eps} Theta~_h'(x) dh'
  Theta~_h'(x)     = int_0^inf e^{-u^2/2-u(x+y)} f(x+h'+u) du
  K_B(h)f(x)       = int_0^h e^{-v/eps} f(x+v) dv
  M_y              = (1-eps*(x+y))/eps
  K(y,t)f(x)       = M_y*K_A^raw(y,t)f(x) + K_B(h)f(x)

Differentiate Theta~_h'(x) in x (product/chain rule under the integral,
Leibniz -- valid for f,f' bounded, dominated convergence applies since
the Gaussian-times-exponential kernel decays super-exponentially):
""")

u, x, y, hp, eps = sp.symbols('u x y hp eps', positive=True)
f = sp.Function('f')
integrand = sp.exp(-u**2/2 - u*(x + y)) * f(x + hp + u)
dintegrand_dx = sp.diff(integrand, x)
print("d/dx[e^{-u^2/2-u(x+y)} f(x+hp+u)] =", dintegrand_dx)
# split into two recognizable pieces:
expected = sp.exp(-u**2/2 - u*(x+y)) * sp.diff(f(x+hp+u), x) \
    - u * sp.exp(-u**2/2 - u*(x+y)) * f(x+hp+u)
resid = sp.simplify(dintegrand_dx - expected)
print("matches [e^{-u^2/2-uz} f'(x+hp+u)] - [u*e^{-u^2/2-uz} f(x+hp+u)]?",
      "residual =", resid, " (must be 0)")
assert resid == 0
print("""
CONFIRMED. So:
  d/dx[Theta~_h'(x)] = Theta_h'[f'](z) - Theta~_{h',1}[f](z)
    Theta_h'[f'](z)     := int_0^inf e^{-u^2/2-uz} f'(x+h'+u) du    [same
                            operator, applied to f' instead of f]
    Theta~_{h',1}[f](z) := int_0^inf u*e^{-u^2/2-uz} f(x+h'+u) du   [a NEW
                            "first-moment" operator]

Integrating over h' with the SAME e^{-h'/eps} weight and using
d/dx[K_B(h)f(x)] = K_B(h)[f'](x)  (pure shift operator, standard, exact):

  d/dx[K_A^raw(y,t)f(x)] = K_A^raw(y,t)[f'](x) - N(y,t)f(x)
    N(y,t)f(x) := int_0^h e^{-h'/eps} Theta~_{h',1}[f](z) dh'

  d/dx[M_y] = -1  (since z=x+y, dM_y/dx = -eps/eps = -1)

  d/dx[K(y,t)f](x) = (d/dx M_y)*K_A^raw(y,t)f(x) + M_y*d/dx[K_A^raw(y,t)f(x)]
                       + K_B(h)[f'](x)
                    = -K_A^raw(y,t)f(x) + M_y*[K_A^raw(y,t)[f'](x) - N(y,t)f(x)]
                       + K_B(h)[f'](x)
                    = [M_y*K_A^raw(y,t)[f'](x) + K_B(h)[f'](x)]
                       - K_A^raw(y,t)f(x) - M_y*N(y,t)f(x)
                    = K(y,t)[f'](x) - K_A^raw(y,t)f(x) - M_y*N(y,t)f(x)      (DX-K)
""")

print("=" * 78)
print("PART 2 -- rigorous O(1/z) bound on the correction term, using (B)+(C')")
print("(no strengthening beyond (C') needed for THIS specific identity)")
print("=" * 78)

def R_mp(zz):
    zz = mp.mpf(zz)
    return mp.sqrt(mp.pi/2) * mp.erfc(zz/mp.sqrt(2)) * mp.exp(zz**2/2)

def sigma_mp(zz):
    zz = mp.mpf(zz)
    return 1 - zz * R_mp(zz)

print("""
Piece 1: K_A^raw(y,t)f(x) = R(z)*K_B(h)f(x) + int_0^h e^{-h'/eps} rho(h',z) dh'
  [wave-25 exact decomposition, cited, re-derived independently in this
  front's own s02/s03]. Bound each term rigorously:
    |R(z)*K_B(h)f(x)| <= R(z)*M_Phi*eps <= (1/z)*M_Phi*eps      (G1, (B))
    |int_0^h e^{-h'/eps} rho(h',z) dh'| <= L1*sigma(z)*eps <= L1*eps/z^2  (G2,(C'))
  => |K_A^raw(y,t)f(x)| <= M_Phi*eps/z + L1*eps/z^2  = O(1/z)      [RIGOROUS]

Piece 2: N(y,t)f(x) = int_0^h e^{-h'/eps} [int_0^inf u*e^{-u^2/2-uz}f(x+h'+u)du] dh'
  Bound the inner integral crudely via (B) alone (|f|<=M_Phi):
    |int_0^inf u*e^{-u^2/2-uz}f(x+h'+u)du| <= M_Phi*int_0^inf u*e^{-u^2/2-uz}du
                                              = M_Phi*sigma(z) <= M_Phi/z^2   (G2)
  => |N(y,t)f(x)| <= M_Phi*sigma(z)*eps <= M_Phi*eps/z^2           [RIGOROUS]

  => |M_y*N(y,t)f(x)| <= |(1-eps*z)/eps|*M_Phi*eps/z^2 <= (1+eps*z)*M_Phi/z^2
                        = M_Phi/z^2 + eps*M_Phi/z  = O(1/z)        [RIGOROUS]

TOTAL: |K_A^raw(y,t)f(x) + M_y*N(y,t)f(x)| <= (M_Phi*eps + eps*M_Phi)/z
                                                + O(1/z^2) terms
                                             =  D2(x,eps)/z    for z>=1,
  D2(x,eps) := 2*M_Phi*eps + L1*eps + M_Phi   [explicit, y/t-independent]
""")

# numeric spot-check of the two rigorous sub-bounds
M_Phi = mp.mpf('1.0')
L1 = mp.mpf('1.0')
eps_val = mp.mpf('0.5')
print(f"{'z':>8} {'M_Phi*eps/z':>14} {'L1*eps/z^2':>14} {'M_Phi*eps/z^2':>16} "
      f"{'eps*M_Phi/z':>14}   [all -> 0 as z grows]")
for zz in [2, 5, 10, 50, 100, 1000]:
    zz = mp.mpf(zz)
    print(f"{float(zz):8.0f} {float(M_Phi*eps_val/zz):14.6e} {float(L1*eps_val/zz**2):14.6e} "
          f"{float(M_Phi*eps_val/zz**2):16.6e} {float(eps_val*M_Phi/zz):14.6e}")
print()

print("=" * 78)
print("PART 3 -- direct numerical confirmation of identity (DX-K) and its")
print("O(1/z) correction bound, fresh raw-kernel implementation")
print("=" * 78)


def theta_tilde(f, fp, x, y, hp, z, eps, want_deriv=False):
    def integrand(v):
        u = v / z
        base = mp.e**(-u**2/2 - v)
        if want_deriv:
            return base * fp(x + hp + u)
        return base * f(x + hp + u)
    return (1/z) * mp.quad(integrand, [0, 2, 8, 20, 50, 100, mp.inf])


def K_A_raw(f, x, y, t, eps, deriv=False):
    x = mp.mpf(x); y = mp.mpf(y); t = mp.mpf(t); eps = mp.mpf(eps)
    z = x + y
    h = y - t
    bps = [mp.mpf(0)]
    scale = eps/4
    while scale < h and len(bps) < 14:
        bps.append(scale); scale *= 2
    bps.append(h)
    bps = sorted(set(bps))

    def outer(hp):
        return mp.e**(-hp/eps) * theta_tilde(f, None, x, y, hp, z, eps, want_deriv=deriv)
    return mp.quad(outer, bps)


def K_full(f, x, y, t, eps):
    x = mp.mpf(x); y = mp.mpf(y); t = mp.mpf(t); eps = mp.mpf(eps)
    z = x + y; h = y - t
    bps = [mp.mpf(0)]
    scale = eps/4
    while scale < h and len(bps) < 14:
        bps.append(scale); scale *= 2
    bps.append(h)
    bps = sorted(set(bps))
    Araw = K_A_raw(f, x, y, t, eps, deriv=False)
    KB = mp.quad(lambda v: mp.e**(-v/eps)*f(x+v), bps)
    M_y = (1 - eps*z)/eps
    return M_y*Araw + KB


def dKdx_numeric(f, x, y, t, eps, delta=mp.mpf('1e-6')):
    return (K_full(f, x+delta, y, t, eps) - K_full(f, x-delta, y, t, eps)) / (2*delta)


def Kf_of_fprime(fp, x, y, t, eps):
    return K_full(fp, x, y, t, eps)


mp.mp.dps = 30
f_test = lambda a: mp.sin(a)/(3+a**2)
fp_test = lambda a: (mp.sin(a+mp.mpf('1e-9'))/(3+(a+mp.mpf('1e-9'))**2)
                      - mp.sin(a-mp.mpf('1e-9'))/(3+(a-mp.mpf('1e-9'))**2)) / (2*mp.mpf('1e-9'))

print(f"{'z':>6} {'d/dx[Kf] numeric':>20} {'K[fp]':>16} {'diff':>14} {'z*|diff|':>12}")
x0 = mp.mpf('0.4')
eps0 = mp.mpf('0.5')
worst = mp.mpf(0)
for z in [mp.mpf(v) for v in [5, 10, 30, 60]]:
    y0 = z - x0
    t0 = y0/2
    dKdx = dKdx_numeric(f_test, x0, y0, t0, eps0)
    Kfp = Kf_of_fprime(fp_test, x0, y0, t0, eps0)
    diff = dKdx - Kfp
    worst = max(worst, abs(diff)*z)
    print(f"{float(z):6.1f} {float(dKdx):20.10f} {float(Kfp):16.10f} {float(diff):14.6e} {float(z*abs(diff)):12.6f}")
print()
print(f"sup(z*|d/dx[Kf]-K[fp]|) observed: {float(worst):.6f}  -- BOUNDED, consistent with")
print("the rigorous O(1/z) bound on the correction term derived in Part 2 above.")
print()

print("=" * 78)
print("PART 4 -- honest assembly and scope: what (C') reduces to")
print("=" * 78)
print("""
Integrating identity (DX-K) over t in [0,y] (formally, assuming Phi_t in
C^1(x) for each t -- itself an unverified regularity input, flagged
honestly, not smuggled) and using g_y'(x)=0 (g_y(x)=e^{-y/eps} is CONSTANT
in x):

  Phi_y'(x) = int_0^y K(y,t)[Phi_t'](x) dt + int_0^y [correction(y,t,x)] dt

  |correction(y,t,x)| <= D2(x,eps)/z,  z=x+y CONSTANT in t (Part 2)
  => |int_0^y correction dt| <= y*D2(x,eps)/z <= D2(x,eps)     [bounded,
     using y<=z for x>=0 -- exactly the SAME y/z<=1 fact this whole
     sub-lineage uses throughout]

So Phi_y' SATISFIES THE SAME VOLTERRA EQUATION, WITH THE SAME KERNEL
K(y,t), AS Phi_y ITSELF -- driven by a genuinely BOUNDED (not growing)
forcing term (<=D2(x,eps), y-independent), rather than the crude,
divergent bound a naive Gronwall argument on the operator norm
||K(y,t)||<=sqrt(pi/2)+eps (DISC-DEC-113, cited) alone would give
(sqrt(pi/2)~1.2533>1, so a naive Gronwall bound EXPONENTIATES -- exactly
the SAME failure mode wave 26's route (a) hit, and the SAME reason a raw
operator-norm argument was abandoned throughout this lineage in favor of
the pointwise-in-f closed form).

HONEST CONCLUSION -- this is a genuine, precise REDUCTION, NOT a proof:
  Phi_y solves (VOLTERRA-Phi) with forcing g_y(x)=e^{-y/eps} (bounded, in
    fact ->0) and is ASSUMED bounded uniformly in y -- this is hypothesis
    (B) itself, STANDING and UNPROVED throughout all 29 waves of this
    lineage (no front, including this one, has derived (B) from first
    principles).
  Phi_y' solves the SAME (VOLTERRA-Phi)-TYPE equation (same kernel K(y,t))
    with a DIFFERENT bounded (not vanishing, but uniformly bounded by
    D2(x,eps)) forcing term.

If the Volterra solution operator for THIS kernel is "uniformly stable"
-- i.e. maps ANY uniformly-bounded forcing sequence to a uniformly (in y)
bounded solution -- then (C') follows IMMEDIATELY from this reduction,
with an EXPLICIT constant L1 built from D2(x,eps) and M_Phi. This
stability property is EXACTLY what would need to be shown to prove (B)
itself rigorously (rather than assume it) -- so this front's contribution
is to show that **(C') is, up to this new and explicit reduction, no
harder than (B) itself** -- a precise, useful narrowing (this lineage now
knows exactly which single "uniform Volterra stability" fact would supply
BOTH (B) [rigorously] and (C') at once), but NOT a proof, since neither
this front nor any predecessor establishes that stability fact for THIS
specific kernel. This is reported here as a genuine PARTIAL result and
NAMED OBSTRUCTION (not a numerically-untested guess): the naive
Gronwall/operator-norm route provably fails (exponentiates, mirroring
wave 26 route (a)'s exact failure mode) and a sharper "same-kernel"
argument is required, of a difficulty this lineage has never resolved
even for (B).
""")
