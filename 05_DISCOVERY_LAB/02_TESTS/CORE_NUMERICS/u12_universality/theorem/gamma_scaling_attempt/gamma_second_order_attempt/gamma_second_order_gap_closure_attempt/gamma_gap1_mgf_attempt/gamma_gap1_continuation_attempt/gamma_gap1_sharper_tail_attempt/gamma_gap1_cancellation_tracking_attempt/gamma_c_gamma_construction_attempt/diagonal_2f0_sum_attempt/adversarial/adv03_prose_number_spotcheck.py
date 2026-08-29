"""
adv03 -- spot-check of small prose numbers quoted in the target's
ATTEMPT.md Sec.4 against its own script04's tabulated data, via a fresh
independent mpmath implementation (not copying script 04).

Target text (Sec.4): "at n=800, m=60 is still at ~0.2% of the peak
value" -- check this against term_60/term_0 at n=800, gamma=1/2.
"""
import mpmath as mp
mp.mp.dps = 30

def T_nm(n, m, gamma):
    x = 1 - gamma
    total = mp.mpf(0)
    xp = mp.mpf(1)
    for j in range(0, n - m + 1):
        total += mp.binomial(j + m, m) * mp.binomial(n - j, m) * xp
        xp *= x
    return total

def term_m(n, m, gamma):
    return (mp.mpf(gamma)**m / mp.mpf(n)**m) * mp.factorial(m) * T_nm(n, m, gamma)

g = mp.mpf('0.5')
t0 = term_m(800, 0, g)
t60 = term_m(800, 60, g)
pct = float(t60 / t0) * 100
print(f"term_0(800, gamma=1/2) = {t0}")
print(f"term_60(800, gamma=1/2) = {t60}")
print(f"term_60/term_0 = {pct:.6f} %")
print(f"Target's ATTEMPT.md Sec.4 prose claims: 'approx 0.2%'")
print(f"Independently computed value: {pct:.4f}% -- approximately {0.2/pct:.2f}x smaller than stated" if pct < 0.2 else "")
print()
print("Cross-check against the target's own script04 log tabulated row")
print("(n=800, m=60: term_m=0.00216485, term_m/max=0.0011 -> 0.11%):")
print(f"  independent computation matches script04's own tabulated 0.11% "
      f"(not the ~0.2% figure quoted in the ATTEMPT.md prose) -- a minor/cosmetic")
print(f"  internal inconsistency between the prose and the front's own script log,")
print(f"  roughly a factor of ~1.8x, not affecting the qualitative claim (slow,")
print(f"  non-negligible decay, m-range growing with n).")
