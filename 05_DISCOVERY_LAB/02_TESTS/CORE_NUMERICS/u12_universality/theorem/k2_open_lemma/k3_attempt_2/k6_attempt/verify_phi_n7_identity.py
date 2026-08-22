"""
ATTEMPT.md Sec.1.2 check 4: at the minimal case n=K+1=7 (only one non-source point
exists), the exact closed forms for psi_n^{(6)} and psi_n^{(6),R} turn out to coincide
exactly, so phi_n^{(6)} (via Lemma A) equals psi_n^{(6)} itself at this one n -- cross-
checked here symbolically, and matches fast_phi_bruteforce.py's raw brute force
(355081/823543) to the digit.
"""
import sympy as sp

n = sp.symbols('n', positive=True)
psiR6 = (1586*n**6 + 4458*n**5 + 6915*n**4 + 8055*n**3 + 6496*n**2 + 3204*n + 720)/(5544*n**6)
psi6 = (2048*n**6 + 3072*n**5 + 4293*n**4 + 4638*n**3 + 3529*n**2 + 1662*n + 360)/(6006*n**6)

print("psiR6 at n=7:", psiR6.subs(n, 7))
print("psi6 at n=7: ", psi6.subs(n, 7))

phi6_at_7 = sp.Rational(6, 7) * psiR6.subs(n, 7) + sp.Rational(1, 7) * psi6.subs(n, 7)
print("phi6 at n=7 via Lemma A:", phi6_at_7)

bruteforce_value = sp.Rational(355081, 823543)
print("fast_phi_bruteforce.py raw brute force at n=7:", bruteforce_value)
print("match:", phi6_at_7 == bruteforce_value == psi6.subs(n, 7) == psiR6.subs(n, 7))
