"""
Referee script 03 -- independent check that the Teorema-R/Corolario-4.2
combination (Theorem W) is genuinely VACUOUS at fixed gamma>0 (c=gamma*n),
confirming the predecessor front's diagnosis that ATTEMPT.md explicitly
states it does "not dispute". Also confirms the contrast with the window
regime (c_n = o(n)), where the same bound DOES -> 0 (see ref01, ref02).

Built from the prose formulas only (Teorema R, Corolario 4.2). No .py
file of this front or any front in its lineage was opened.
"""
import mpmath as mp

mp.mp.dps = 50
a_star = mp.sqrt(mp.pi) * (1/mp.sqrt(2) - mp.mpf(1)/2)
kappa_B = mp.mpf('0.2805')

def L(c):
    c = mp.mpf(c)
    return (mp.sqrt(mp.pi)/2) * c**mp.mpf('-0.5') - mp.e**(-c) / (2*c)

def B(n, c):
    n = mp.mpf(n); c = mp.mpf(c)
    return (a_star*mp.sqrt(c) + kappa_B) / (n * L(c))

print("=== Confirm Theorem-W route IS vacuous (B does not -> 0) at fixed gamma>0 (c=gamma*n) ===")
for gamma in [mp.mpf('0.1'), mp.mpf('0.3'), mp.mpf('0.7')]:
    print(f"-- gamma={gamma} --")
    for n in [10**2, 10**4, 10**8, 10**16, 10**32]:
        c = gamma*mp.mpf(n)
        b = B(n, c)
        print(f"   n=10^{int(mp.log10(n))}  B(n,gamma n) = {mp.nstr(b,10)}")
    print()

print("Observation: B(n,gamma n) converges to a nonzero constant as n->infty for")
print("every fixed gamma>0 tested (0.1, 0.3, 0.7) -- it does NOT vanish. This")
print("independently confirms the predecessor's diagnosis (not disputed by the")
print("target ATTEMPT.md) that the Teorema-R route is structurally vacuous for")
print("fixed gamma>0, in sharp contrast to its behaviour inside the named window")
print("and under the 'bonus' hypothesis c_n->infty, c_n=o(n) (see ref01/ref02),")
print("where the same quantity provably -> 0.")
