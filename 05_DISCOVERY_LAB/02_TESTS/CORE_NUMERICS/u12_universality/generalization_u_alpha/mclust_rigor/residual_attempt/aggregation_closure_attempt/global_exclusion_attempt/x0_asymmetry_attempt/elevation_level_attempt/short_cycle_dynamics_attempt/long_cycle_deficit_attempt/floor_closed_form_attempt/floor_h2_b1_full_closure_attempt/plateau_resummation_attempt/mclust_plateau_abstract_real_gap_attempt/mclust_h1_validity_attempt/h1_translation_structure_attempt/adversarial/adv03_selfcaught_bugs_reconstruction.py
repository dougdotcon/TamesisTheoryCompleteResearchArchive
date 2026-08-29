"""
adv03_selfcaught_bugs_reconstruction.py

INDEPENDENT ADVERSARIAL CHECK -- H1-TRANSLATION-STRUCTURE-ATTEMPT referee
check, claim 5 (the two self-disclosed bugs). This script does NOT merely
re-read the target's s02/s05 logs -- it independently RECONSTRUCTS, from
the mathematical description of each bug given in ATTEMPT.md Sec 4.2/4.3,
the WRONG version of each computation, to confirm (a) the wrong version
really does produce an incorrect/inconsistent result of the kind described,
and (b) the corrected version matches this referee's own independently
re-derived closed form (see REFEREE_REPORT.md and adv01/adv02).

Bug 1 (Sec 4.2, s02): prose-only error -- an earlier draft's COMMENTARY
claimed c(z) ~ -1 - 1/(eps*z) + ... (wrong sign) and claimed the 1/z^2 term
vanishes. The underlying sympy series computation was claimed to be correct
throughout; only the prose was wrong. Checked here: does the correct
sympy-derived series in fact have the SIGN and z^-2 coefficient the
corrected prose claims (+1/(eps*z), and a nonzero, exactly +1, z^-2 term)?

Bug 2 (Sec 4.3, s05): a genuine algebraic slip -- an earlier version wrote
the leading behavior of (1-eps*z)/eps as "-1/(eps*delta)" (i.e. ~ -z/eps)
instead of the correct "-1/delta" (~-z, no extra 1/eps factor), where
delta:=1/z. Checked here: does the WRONG version really fail to cancel the
K_B(h)f(x)/eps terms (nonzero, dimensionally-inconsistent KB coefficient),
while the CORRECTED version cancels EXACTLY, matching what this referee
independently re-derived by hand (see REFEREE_REPORT.md)?

No randomness. Exact symbolic algebra (sympy) throughout.
"""

import sympy as sp

print("=" * 78)
print("BUG 1 RECONSTRUCTION (Sec 4.2): sign/vanishing-term claim about c(z)")
print("=" * 78)

z, eps = sp.symbols('z eps', positive=True)
N = 6
# Same coefficient recursion as this referee's own by-hand derivation
# (REFEREE_REPORT.md): R(z) ~ sum_n c_n / z^{2n+1}, c_0=1, c_n=-(2n-1)c_{n-1}
c = [sp.Integer(1)]
for n in range(1, N):
    c.append(-(2 * n - 1) * c[-1])
print("R(z) Mills-ratio series coefficients c_0..c_5 =", c)

R_series = sum(c[n] * z ** (-(2 * n + 1)) for n in range(N))
c_of_z_series = sp.expand(R_series / eps - z * R_series)
z0 = c_of_z_series.coeff(z, 0)
zm1 = c_of_z_series.coeff(z, -1)
zm2 = c_of_z_series.coeff(z, -2)
print(f"\nCorrect series: c(z) = {z0} + ({zm1})/z + ({zm2})/z^2 + ...")

# The WRONG prose claim (as described in ATTEMPT.md): "-1/(eps*z)" (wrong
# sign) and "z^-2 term vanishes" (i.e. zm2 == 0).
wrong_claim_sign = -1 / eps   # WRONG claimed coefficient of 1/z
wrong_claim_zm2_is_zero = True

print(f"\nWrong prose claim (as described): 1/z coefficient = {wrong_claim_sign}, "
      f"1/z^2 coefficient = 0")
print(f"Actual sympy-derived series:       1/z coefficient = {zm1}, "
      f"1/z^2 coefficient = {zm2}")

sign_claim_wrong = sp.simplify(zm1 - wrong_claim_sign) != 0
zm2_claim_wrong = sp.simplify(zm2) != 0
print(f"\nIs the wrong prose claim's sign actually wrong (disagrees with the "
      f"correct series)? {sign_claim_wrong}")
print(f"Is the wrong prose claim's 'z^-2 term vanishes' actually wrong "
      f"(zm2 != 0)? {zm2_claim_wrong}")
assert sign_claim_wrong and zm2_claim_wrong, \
    "Bug 1 reconstruction: the described error does not actually contradict the correct series"
assert sp.simplify(zm1 - 1 / eps) == 0, "corrected claim (+1/(eps*z)) should match"
assert sp.simplify(zm2 - 1) == 0, "corrected claim (z^-2 coefficient = +1) should match"
print("\n=> CONFIRMED genuine: the described WRONG prose (negative sign, vanishing")
print("   z^-2 term) is indeed contradicted by the correct sympy-derived series;")
print("   the CORRECTED claim (+1/(eps*z), and +1/z^2, not 0) matches the correct")
print("   series exactly, and independently matches this referee's own by-hand")
print("   derivation (REFEREE_REPORT.md). Bug 1 is a genuine, correctly-diagnosed,")
print("   correctly-fixed error (prose-only, as claimed -- the underlying")
print("   computation was never wrong).")

print()
print("=" * 78)
print("BUG 2 RECONSTRUCTION (Sec 4.3): (1-eps*z)/eps leading-order scaling slip")
print("=" * 78)

delta = sp.symbols('delta', positive=True)  # delta := 1/z
KB, fx, fxh, h = sp.symbols('KB fx fxh h', real=True)
IBPresult = sp.exp(-h / eps) * fxh - fx + KB / eps  # exact IBP result (Sec 4.3, Step 3)

term1 = (delta / eps) * KB  # from c(z)+1 ~ delta/eps (s02, PROVED, unaffected by bug 2)

print("""
Two candidate leading-order behaviors of (1-eps*z)/eps as z->infinity
(eps FIXED), tested against each other:
  CORRECT:  (1-eps*z)/eps = 1/eps - z  ~  -z         (the FIXED constant
            1/eps is dominated by the UNBOUNDED -z term)          = -1/delta
  WRONG:    an earlier draft claimed (1-eps*z)/eps ~ -1/(eps*delta) = -z/eps
            (an extra, spurious 1/eps factor)
""")

term2_correct = (-1 / delta) * (delta ** 2 * IBPresult)
term2_wrong = (-1 / (eps * delta)) * (delta ** 2 * IBPresult)

for label, term2 in [("CORRECT (-1/delta)", term2_correct),
                      ("WRONG (-1/(eps*delta))", term2_wrong)]:
    total = sp.expand(term1 + sp.expand(term2))
    KB_coeff = sp.expand(total).coeff(delta, 1).coeff(KB, 1)
    print(f"  Using {label}: KB coefficient at order delta^1 = {sp.simplify(KB_coeff)}")

KB_coeff_wrong = sp.expand(sp.expand(term1 + sp.expand(term2_wrong))).coeff(delta, 1).coeff(KB, 1)
KB_coeff_correct = sp.expand(sp.expand(term1 + sp.expand(term2_correct))).coeff(delta, 1).coeff(KB, 1)

assert sp.simplify(KB_coeff_wrong) != 0, \
    "Bug 2 reconstruction: the described wrong scaling should NOT cancel, but it did"
assert sp.simplify(KB_coeff_correct) == 0, \
    "Bug 2 reconstruction: the corrected scaling should cancel exactly, but it did not"
print(f"\n=> CONFIRMED genuine: the WRONG scaling leaves a NONZERO, "
      f"dimensionally-inconsistent")
print(f"   KB coefficient ({sp.simplify(KB_coeff_wrong)}) -- exactly matching ATTEMPT.md's own")
print(f"   description ('KB_coeff = 1/eps - 1/eps**2, manifestly nonzero and")
print(f"   dimensionally inconsistent in eps-power'). The CORRECTED scaling gives")
print(f"   an EXACT 0, matching this referee's own independent by-hand derivation")
print(f"   (REFEREE_REPORT.md) of the same cancellation via the B0/eps - B1")
print(f"   integration-by-parts route.")

total_correct = sp.expand(term1 + sp.expand(term2_correct))
print(f"\nFinal corrected leading-order result (delta^1 = 1/z term, KB terms")
print(f"removed since they cancel): {sp.simplify(total_correct.subs(KB, 0))}")
print("Matches the claimed closed form K(y,t)f(x) ~ [f(x)-e^{-h/eps}f(x+h)]/z")
print("(here in delta=1/z units): delta*(fx - e^{-h/eps}*fxh).")

print()
print("=" * 78)
print("SUMMARY")
print("=" * 78)
print("""
Both self-disclosed bugs are GENUINE (independently reconstructed and
confirmed, not taken on faith), CORRECTLY DIAGNOSED (the described wrong
version really does produce the described inconsistent/nonzero result), and
CORRECTLY FIXED (the corrected version matches both the target's own final
formula and this referee's own fully independent by-hand re-derivation).

One documentation-precision note (see REFEREE_REPORT.md for full
discussion): the front's own executive summary states both bugs were
"caught by the front's OWN symbolic verification scripts failing their own
assertions" -- true for Bug 2 (s05's own `assert ... == 0` genuinely fails
on the wrong version, confirmed above), but Bug 1 (s02) is described in
Sec 4.2 itself as a PROSE-only error caught by noticing the commentary
contradicted the script's own already-correct printed series (the
corroborating `assert` statements were added AFTER the fix, not the
mechanism that caught it) -- a minor inaccuracy in how the executive
summary characterizes the catch-mechanism for Bug 1 specifically, not in
the mathematical content of either bug or its fix.
""")
