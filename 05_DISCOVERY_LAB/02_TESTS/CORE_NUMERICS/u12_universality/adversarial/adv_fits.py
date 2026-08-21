"""Fits: M1 exponent (archive mirror protocol + bootstrap CI),
M2 model comparison (weighted chi2 / AIC), M3 deviation-vs-n analysis."""
import json
import numpy as np
from scipy.optimize import curve_fit, minimize_scalar

with open("adv_results.json") as fh:
    R = json.load(fh)
with open("adv_continuum.json") as fh:
    CONT = json.load(fh)

OUT = {}

# ---------------- M1: exponent, mirror protocol ----------------
m1 = R["M1"]
cs = np.array([r["c"] for r in m1])
phis = np.array([r["phi_mean"] for r in m1])
samples = [np.array(r["samples"]) for r in m1]

model = lambda c, a: (1 + c) ** (-a)
popt, pcov = curve_fit(model, cs, phis, p0=[0.5])
alpha_hat, alpha_sig = float(popt[0]), float(np.sqrt(pcov[0][0]))

rng = np.random.default_rng(np.random.SeedSequence(555000111))
B = 4000
boots = np.empty(B)
for b in range(B):
    means = np.array([s[rng.integers(0, len(s), len(s))].mean() for s in samples])
    try:
        pb, _ = curve_fit(model, cs, means, p0=[alpha_hat])
        boots[b] = pb[0]
    except RuntimeError:
        boots[b] = np.nan
boots = boots[~np.isnan(boots)]
ci = np.percentile(boots, [2.5, 97.5])
OUT["M1_fit"] = dict(alpha=alpha_hat, sigma_curvefit=alpha_sig,
                     ci95_bootstrap=[float(ci[0]), float(ci[1])],
                     B=len(boots))
print(f"M1 exponent (mirror protocol, n=2000 unweighted): alpha={alpha_hat:.4f} "
      f"+- {alpha_sig:.4f} (curve_fit), bootstrap CI95=[{ci[0]:.4f},{ci[1]:.4f}]")

# ---------------- M2: model comparison ----------------
m2 = R["M2"]
c2 = np.array([r["c"] for r in m2])
y = np.array([r["phi_mean"] for r in m2])
s = np.array([r["sem"] for r in m2])


def chi2_of(pred):
    return float(np.sum(((y - pred) / s) ** 2))


def fit_1param(fun, lo, hi):
    res = minimize_scalar(lambda t: chi2_of(fun(t)), bounds=(lo, hi),
                          method="bounded", options=dict(xatol=1e-10))
    return float(res.x), float(res.fun)


models = {}
# U_1/2 fixed
models["U12_fixed"] = dict(k=0, chi2=chi2_of((1 + c2) ** -0.5), param=None)
# U_1/2 free alpha
a, ch = fit_1param(lambda t: (1 + c2) ** (-t), 0.01, 5)
models["U12_free_alpha"] = dict(k=1, chi2=ch, param=a)
# U_0 threshold: 1 if c<c*, b if c>=c* (scan partitions; b = weighted mean)
best = None
for i in range(len(c2) + 1):
    # cells [0:i) below threshold (model=1), cells [i:] at plateau b
    lowmask = np.zeros(len(c2), dtype=bool)
    lowmask[:i] = True
    chi_low = float(np.sum(((y[lowmask] - 1) / s[lowmask]) ** 2))
    if i < len(c2):
        w = 1 / s[~lowmask] ** 2
        b = float(np.sum(w * y[~lowmask]) / np.sum(w))
        chi_hi = float(np.sum(((y[~lowmask] - b) / s[~lowmask]) ** 2))
    else:
        b, chi_hi = None, 0.0
    tot = chi_low + chi_hi
    if best is None or tot < best[0]:
        best = (tot, i, b)
models["U0_threshold"] = dict(k=2, chi2=best[0], param=dict(split_index=best[1], b=best[2]))
# U_1 exponential exp(-lam c)
lam, ch = fit_1param(lambda t: np.exp(-t * c2), 1e-6, 10)
models["U1_exp_free"] = dict(k=1, chi2=ch, param=lam)
models["U1_exp_literal"] = dict(k=0, chi2=chi2_of(np.exp(-c2)), param=None)
# U_2 (1+beta c)^-2
beta, ch = fit_1param(lambda t: (1 + t * c2) ** -2.0, 1e-6, 10)
models["U2_lindblad_free"] = dict(k=1, chi2=ch, param=beta)
models["U2_lindblad_literal"] = dict(k=0, chi2=chi2_of((1 + c2) ** -2.0), param=None)
# U_inf 1/(1+c^m)
mm, ch = fit_1param(lambda t: 1 / (1 + c2 ** t), 0.01, 10)
models["Uinf_free"] = dict(k=1, chi2=ch, param=mm)

aic0 = models["U12_fixed"]["chi2"] + 0
for name, rec in models.items():
    rec["aic"] = rec["chi2"] + 2 * rec["k"]
    rec["delta_aic_vs_U12fixed"] = rec["aic"] - aic0
    print(f"M2 {name:22s} k={rec['k']} chi2={rec['chi2']:10.2f} AIC={rec['aic']:10.2f} "
          f"dAIC={rec['delta_aic_vs_U12fixed']:+10.2f} param={rec['param']}")
OUT["M2_models"] = models

# chi2 p-value of U12 fixed on this grid (7 dof)
from scipy.stats import chi2 as chi2dist
OUT["M2_U12fixed_pvalue"] = float(chi2dist.sf(models["U12_fixed"]["chi2"], 7))
print(f"M2 U12_fixed chi2 p-value (7 dof): {OUT['M2_U12fixed_pvalue']:.3e}")

# ---------------- M3: deviations vs n ----------------
m3 = R.get("M3", [])
OUT["M3"] = []
cont_by_c = {r["c"]: r for r in CONT}
for cval in (0.5, 50.0):
    rows = [r for r in m3 if r["c"] == cval]
    print(f"\nM3 c={cval}: theorem={(1+cval)**-0.5:.6f} "
          f"continuum={cont_by_c[cval]['phi_inf']:.6f}±{cont_by_c[cval]['sem']:.6f}")
    chi2_vs_theorem = 0.0
    chi2_vs_cont = 0.0
    for r in rows:
        zt = r["dev"] / r["sem"]
        zc = (r["phi_mean"] - cont_by_c[cval]["phi_inf"]) / np.hypot(r["sem"], cont_by_c[cval]["sem"])
        chi2_vs_theorem += zt ** 2
        chi2_vs_cont += zc ** 2
        print(f"  n={r['n']:6d} N={r['N']:5d} phi={r['phi_mean']:.6f}±{r['sem']:.6f} "
              f"dev_theorem={r['dev']:+.6f} ({zt:+.1f}σ)  dev_continuum={r['phi_mean']-cont_by_c[cval]['phi_inf']:+.6f} ({zc:+.1f}σ)")
        OUT["M3"].append(dict(r, z_theorem=zt, z_continuum=zc))
    dof = len(rows)
    p_t = float(chi2dist.sf(chi2_vs_theorem, dof))
    p_c = float(chi2dist.sf(chi2_vs_cont, dof))
    print(f"  chi2 vs theorem: {chi2_vs_theorem:.1f} (dof={dof}, p={p_t:.3e})")
    print(f"  chi2 vs continuum-limit: {chi2_vs_cont:.1f} (dof={dof}, p={p_c:.3e})")
    OUT[f"M3_c{cval}_chi2_theorem"] = dict(chi2=chi2_vs_theorem, dof=dof, p=p_t)
    OUT[f"M3_c{cval}_chi2_continuum"] = dict(chi2=chi2_vs_cont, dof=dof, p=p_c)

with open("adv_fits.json", "w") as fh:
    json.dump(OUT, fh, indent=2, default=float)
print("\nsaved adv_fits.json")
