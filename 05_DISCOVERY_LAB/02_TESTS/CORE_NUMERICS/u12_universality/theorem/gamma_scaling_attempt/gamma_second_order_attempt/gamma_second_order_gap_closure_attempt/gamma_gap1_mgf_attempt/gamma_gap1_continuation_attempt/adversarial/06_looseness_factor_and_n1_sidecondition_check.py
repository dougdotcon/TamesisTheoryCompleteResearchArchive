"""
Adversarial referee script 06.

(A) Independent check of the target's Sec.4 Step 3 narrative claim that
the "looseness factor" lambdahat(gamma)/lambda(gamma) lies "between 3
(gamma=1) and ~4.67 (gamma->0)". Both lambda(gamma) (Sec.3 of target,
independently confirmed in script 01) and lambdahat(gamma) (Sec.4 Step 3
of target, independently confirmed as Ghat's exact leading asymptotic in
script 03) are used exactly as the target itself defines them.

(B) Side-condition sanity check: does K_max(n_1(gamma),gamma) <= n_1(gamma)/2
actually hold at the target's own claimed n_1(gamma) := ceil(16384/beta^2)?
"""
import mpmath as mp

mp.mp.dps = 50


def beta_of(g):
    return g * (2 - g) / 2


def lam_of(g):
    return 4 * (3 - 2 * g) / (g * (2 - g))


def lamhat_of(g):
    return 16 * (mp.mpf(7) / 4 - g) / beta_of(g)


def Kmax_of(n, g):
    b = beta_of(g)
    return 4 * mp.sqrt(n * mp.log(n) / b)


def n1_of(g):
    b = beta_of(g)
    return mp.ceil(16384 / b ** 2)


print("(A) Check of the target's claimed 'looseness factor lambdahat/lambda")
print("    between 3 (gamma=1) and ~4.67 (gamma->0)', Sec.4 Step 3 narrative:")
for g in [mp.mpf('0.0001'), mp.mpf('0.01'), mp.mpf('0.1'), mp.mpf('0.5'),
          mp.mpf('0.9'), mp.mpf('0.99'), mp.mpf('0.9999'), mp.mpf('1')]:
    lam = lam_of(g)
    lamhat = lamhat_of(g)
    print(f"  gamma={float(g):.4f}: lambda={float(lam):.6f}  "
          f"lambdahat={float(lamhat):.6f}  ratio={float(lamhat / lam):.6f}")

print("\n=> True ratio at gamma=1 is 6.0 (NOT 3, as the ATTEMPT.md text states);")
print("   true ratio as gamma->0+ is 14/3=4.6667 (this part IS correctly")
print("   stated). True range is approx [4.667, 6.0], INCREASING in gamma,")
print("   not 'between 3 (gamma=1) and ~4.67 (gamma->0)' (which implies the")
print("   opposite direction) as the document states.")
print("   NOTE: this ratio is a purely descriptive number; lambdahat(gamma)")
print("   itself (independently confirmed exact in script 03) is what is")
print("   actually used downstream to build C0(gamma), C(gamma), Ghat, and")
print("   the whole n_0(gamma) table -- all independently confirmed correct")
print("   in scripts 03-04 regardless of this one narrative slip.")

print("\n(B) Side-condition check: is K_max(n_1(gamma),gamma) <= n_1(gamma)/2 ?")
for g in [mp.mpf('0.99'), mp.mpf('0.5'), mp.mpf('0.1'), mp.mpf('0.01')]:
    n1 = n1_of(g)
    Km = Kmax_of(n1, g)
    ok = Km <= n1 / 2
    print(f"  gamma={float(g):.2f}: n1={int(n1)}  K_max(n1)={float(Km):.2f}  "
          f"n1/2={float(n1) / 2:.2f}  K_max<=n1/2? {ok}")
    assert ok
