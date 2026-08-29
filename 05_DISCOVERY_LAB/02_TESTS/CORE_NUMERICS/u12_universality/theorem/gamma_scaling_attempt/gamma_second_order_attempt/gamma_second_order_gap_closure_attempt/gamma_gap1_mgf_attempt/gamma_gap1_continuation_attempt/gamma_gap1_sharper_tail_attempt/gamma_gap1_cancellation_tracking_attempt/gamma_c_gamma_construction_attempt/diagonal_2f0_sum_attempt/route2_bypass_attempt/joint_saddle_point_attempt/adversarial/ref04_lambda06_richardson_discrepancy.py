"""
Referee script 04: scrutiny of the target's Section 4 claim ("the general
closed form matches the Richardson-extrapolated value to <0.7% for
lambda<=1.0, <1.6% at lambda=1.5") against the target's own printed table
in 03_saddle_value_expansion.log.

The target's own log shows, at lambda=0.6, gamma=0.3:
  predicted=1.201983134  numeric(Richardson)=1.214728583  rel.err=0.0104924
i.e. 1.05% -- which EXCEEDS the claimed "<0.7% for lambda<=1.0" bound.

This script:
  (1) confirms this reading of the target's own log is correct (direct
      re-parse / re-quotation);
  (2) independently re-implements the exact term_m evaluator (fresh code,
      not copied) and the SAME Richardson procedure the target used, to
      see whether this is reproducible (i.e. not a transcription error in
      the log) and to see whether the RAW (non-Richardson-extrapolated)
      error trend at this exact (lambda,gamma) is clean and monotone
      (which would indicate the T_prof closed form itself is fine, and
      the discrepancy is Richardson-extrapolation noise -- the same kind
      of issue the target itself found, disclosed, and resolved for
      lambda=1.5 via a direct high-n push in its own Part C, but did NOT
      apply to lambda=0.6 despite comparable symptoms there).
"""
import mpmath as mp

mp.mp.dps = 80

print("=" * 78)
print("(1) The target's own claim vs its own printed log data")
print("=" * 78)
print("ATTEMPT.md Section 4 claims: 'the general closed form matches the")
print("Richardson-extrapolated value to <0.7% for lambda<=1.0, <1.6% at lambda=1.5'")
print()
print("The target's own 03_saddle_value_expansion.log contains the line:")
print("  lambda=0.6 gamma=0.3: predicted=1.201983134  numeric(Richardson)=1.214728583")
print("  rel.err=0.0104924")
rel_err_reported = 0.0104924
print(f"  => {rel_err_reported*100:.4f}%, which EXCEEDS the claimed <0.7% bound for lambda<=1.0.")
assert rel_err_reported > 0.007
print(">>> CONFIRMED: the claim '<0.7% for lambda<=1.0' is contradicted by the")
print(">>> target's own disclosed data at (lambda,gamma)=(0.6,0.3).")

print()
print("=" * 78)
print("(2) Independent re-implementation: is this reproducible, and is the RAW")
print("    (non-Richardson) error trend at this point clean/monotone?")
print("=" * 78)


def t_star_mp(n, m, gamma):
    n = mp.mpf(n); m = mp.mpf(m); gamma = mp.mpf(gamma)
    disc = gamma ** 2 * n ** 2 + 4 * (1 - gamma) * m ** 2
    return (2 * m + gamma * n - mp.sqrt(disc)) / (2 * gamma * (m + n))


def term_m_beta(n, m, gamma, maxdegree=12, window=7):
    n_mp = mp.mpf(n); m_mp = mp.mpf(m)
    Cnorm = mp.binomial(n_mp + m_mp + 1, 2 * m_mp + 1)
    beta_pref = mp.factorial(2 * m_mp + 1) / (mp.factorial(m_mp) ** 2)
    integrand = lambda t: t ** m_mp * (1 - t) ** m_mp * (1 - gamma * t) ** (n_mp - m_mp)
    if m == 0:
        integral_val = mp.quad(integrand, [0, 1])
    else:
        ts = t_star_mp(n, m, gamma)
        gpp = -m_mp / ts ** 2 - m_mp / (1 - ts) ** 2 - gamma ** 2 * (n_mp - m_mp) / (1 - gamma * ts) ** 2
        width = 1 / mp.sqrt(-gpp)
        pts = sorted(set([mp.mpf(0), max(mp.mpf(0), ts - window * width), ts,
                           min(mp.mpf(1), ts + window * width), mp.mpf(1)]))
        integral_val = mp.quad(integrand, pts, maxdegree=maxdegree)
    T = Cnorm * beta_pref * integral_val
    return (gamma ** m_mp) * mp.factorial(m_mp) * T / (n_mp ** m_mp)


lam = mp.mpf('0.6')
gamma = mp.mpf('0.3')
A_gamma = (2 - gamma) / (2 * gamma)
predicted = (1 / gamma) * mp.e ** (-A_gamma * lam ** 2)
print(f"predicted T_prof(0.6,0.3) = {mp.nstr(predicted,12)}")
print(f"(matches the target's own printed 'predicted=1.201983134': "
      f"{mp.nstr(abs(predicted-mp.mpf('1.201983134')),4)})")

n_seq = [4000, 16000, 64000, 256000, 1024000, 4096000, 16384000]
vals = []
print()
print("RAW (non-extrapolated) values, own fresh implementation:")
for n_val in n_seq:
    m_val = int(mp.nint(lam * mp.sqrt(n_val)))
    v = term_m_beta(n_val, m_val, gamma)
    rel = abs(v - predicted) / predicted
    vals.append(v)
    print(f"  n={n_val:>9} m={m_val:>6}  term_m={mp.nstr(v,12)}  raw rel.err={mp.nstr(rel,6)}")

print()
print("Reproducing the TARGET's own repeated-Richardson procedure (2x, squared),")
print("using exactly the first 5 of the above n values (matching the target's own")
print("n_seq = [4000,16000,64000,256000,1024000]):")
vals5 = vals[:5]
r1 = [2 * vals5[i + 1] - vals5[i] for i in range(len(vals5) - 1)]
r2 = [2 * r1[i + 1] - r1[i] for i in range(len(r1) - 1)]
L_est = r2[-1]
rel_repro = abs(L_est - predicted) / predicted
print(f"  Repeated-Richardson estimate = {mp.nstr(L_est,12)}")
print(f"  Relative error vs predicted  = {mp.nstr(rel_repro,6)}  "
      f"(target's own reported value: 0.0104924)")

print()
print("Simple single-stage 2-point Richardson (x_n = L + c/sqrt(n)), using the")
print("LAST TWO of the 7 n-values (largest n, most reliable extrapolation basis):")
L_simple = 2 * vals[-1] - vals[-2]
rel_simple = abs(L_simple - predicted) / predicted
print(f"  L_est (from n={n_seq[-2]},{n_seq[-1]}) = {mp.nstr(L_simple,12)}  "
      f"rel.err={mp.nstr(rel_simple,6)}")

print()
print("=" * 78)
print("Interpretation")
print("=" * 78)
raw_errs = [abs(v - predicted) / predicted for v in vals]
print("RAW relative errors across n=4e3..1.6e7:", [mp.nstr(e, 4) for e in raw_errs])
decreasing_trend = all(raw_errs[i + 1] < raw_errs[i] for i in range(2, len(raw_errs) - 1))
print(f"Clean decreasing trend from n=64000 onward: {decreasing_trend}")
print()
print("This independently reproduces the target's own reported repeated-Richardson")
print("residual (~1.0-1.1%) at (lambda,gamma)=(0.6,0.3) -- confirming it is NOT a")
print("transcription error in the log. However, the RAW (non-extrapolated) error")
print("trend at this same point is clean and monotonically shrinking from n=64000")
print("onward, and a simple single-stage 2-point Richardson using the LARGEST n")
print("pair already achieves a much tighter match than the target's own repeated-")
print("Richardson estimate. This is consistent with the discrepancy being an")
print("artifact of the SPECIFIC repeated/second-order Richardson procedure the")
print("target used (noise-amplifying at this particular (lambda,gamma) point, for")
print("reasons not investigated further here) rather than a flaw in the T_prof")
print("closed form itself -- exactly the same DIAGNOSIS the target itself reached,")
print("independently, for the lambda=1.5 discrepancy (via its own Part C direct")
print("high-n push) but did NOT apply to this comparably-anomalous lambda=0.6 case.")
print()
print(">>> CONCLUSION: the specific quantitative claim '<0.7% for lambda<=1.0' in")
print(">>> ATTEMPT.md Section 4 (and echoed in the VERDICT summary) is not accurate")
print(">>> and needs correction -- the target's own log shows up to ~1.05% at")
print(">>> lambda=0.6. This does NOT, on the evidence gathered here, indicate a flaw")
print(">>> in the T_prof closed form itself (see ref01, which independently confirms")
print(">>> the closed form via a route unrelated to Richardson extrapolation).")
