"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- VALIDACAO (a), pre-lock: lado iid/REM.

Modelo nulo iid/REM em altura finita (discretizacoes DECLARADAS; a v1 e a
canonica do pre-registro, v2/v3 sao variantes de sensibilidade):
  v1 (canonica): n_T = log(T/2pi) valores iid N(0, sigma^2),
                 sigma^2 = (1/2) log log T   (variancia de Selberg em t~T)
  v2: n_T = log(T/2pi), sigma^2 = (1/2) log log(T/2pi)
  v3: n_T = log T,      sigma^2 = (1/2) log log T
Extensao continua para n nao-inteiro: F_max(x) = Phi(x/sigma)^n.

Derivacao (registrada p/ auditoria): E[max] ~ sigma*sqrt(2 ln n)
- sigma*(ln ln n + ln 4pi)/(2 sqrt(2 ln n)); com sigma^2=(1/2)loglogT e
n~logT isso da loglogT - (1/4)logloglogT + O(1) -- o coeficiente -1/4 do
modelo iid/REM.

CRITERIOS DE ACEITE (fixados ANTES de rodar):
  A1 (recuperacao assintotica): inclinacao WLS da curva EXATA v1 sobre
      alturas gigantes L=logT em {1e3,1e4,1e5,1e6,1e7} deve estar a
      menos de 0.05 de -0.25 (e se aproximar monotonicamente).
  A2 (vies do estimador): em R=400 replicas sinteticas do desenho travado
      (M por altura, pesos EMPIRICOS 1/(sd^2/M) como na analise real),
      |media(inclinacoes) - p_iid_v1| <= 3*sd(inclinacoes)/sqrt(R).
  A3 (cobertura): fracao de replicas com |inclinacao - p_iid_v1| <=
      1.96*EP_rep dentro de [0.917, 0.983] (3 sigma binomial de 0.95).
Se qualquer criterio falhar: log preservado como *_FAILED.log, corrigir
para frente (precedente: validation_zeta_eval_run1_FAILED.log).

Saida: p_iid_{v1,v2,v3} (inclinacoes efetivas de altura finita no desenho,
pesos de DESENHO), curvas exatas por altura, resultado A1-A3.
"""
import json
import time
from pathlib import Path

import numpy as np
from scipy.special import log_ndtr, ndtri
from scipy.integrate import quad
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
SEED_SIM = 31415926
R_REPS = 400
LOG2PI = float(np.log(2 * np.pi))


def m_of_n(n):
    """E[max de n iid N(0,1)] via F^n = exp(n*logPhi); n real > 0."""
    def integrand(u):
        # x * d/dx [Phi^n] = x * n * Phi^(n-1) * phi
        return u * n * np.exp((n - 1) * log_ndtr(u)) * norm.pdf(u)
    lo, hi = -12.0, 15.0
    val, _ = quad(integrand, lo, hi, limit=200)
    return val


def curves(design):
    heights = design["heights_primary"]
    out = {}
    for variant in ["v1", "v2", "v3"]:
        mu = []
        for T in heights:
            llT = np.log(np.log(T))
            ll2pi = np.log(np.log(T) - LOG2PI)
            n = (np.log(T) - LOG2PI) if variant in ("v1", "v2") else np.log(T)
            s2 = 0.5 * (llT if variant in ("v1", "v3") else ll2pi)
            mu.append(float(np.sqrt(s2) * m_of_n(n)))
        out[variant] = mu
    return out


def wls_slope(y, x, w):
    X = np.vstack([np.ones_like(x), x]).T
    XtWX = X.T @ (w[:, None] * X)
    beta = np.linalg.solve(XtWX, X.T @ (w * y))
    cov = np.linalg.inv(XtWX)
    return float(beta[1]), float(np.sqrt(cov[1, 1]))


def main():
    t_start = time.time()
    design = json.load(open(HERE / "DESIGN.json"))
    heights = design["heights_primary"]
    Ms = np.array([design["M"][f"{T:.0e}"] for T in heights])
    sd_proj = np.array([design["sd_projected_per_height"][f"{T:.0e}"]
                        for T in heights])
    x = np.array([np.log(np.log(np.log(T))) for T in heights])
    ll = np.array([np.log(np.log(T)) for T in heights])
    w_design = Ms / sd_proj**2

    log_lines = []

    # --- A1: recuperacao assintotica da curva exata v1 (em L = log T) ---
    slopes_asym = []
    for Lc in [1e3, 1e4, 1e5, 1e6, 1e7]:
        Ls = Lc * np.array([1.0, 3.0, 10.0])  # 3 pontos por decada-ancora
        mus, xs, lls_ = [], [], []
        for L in Ls:
            n = L - LOG2PI
            s2 = 0.5 * np.log(L)
            mus.append(np.sqrt(s2) * m_of_n(n))
            lls_.append(np.log(L))
            xs.append(np.log(np.log(L)))
        y = np.array(mus) - np.array(lls_)
        s, _ = wls_slope(y, np.array(xs), np.ones(3))
        slopes_asym.append(s)
        log_lines.append(f"A1: L~{Lc:.0e}: inclinacao exata v1 = {s:+.4f}")
    a1_final = slopes_asym[-1]
    diffs = np.abs(np.array(slopes_asym) + 0.25)
    a1_pass = (abs(a1_final + 0.25) < 0.05) and np.all(np.diff(diffs) <= 1e-6)
    log_lines.append(f"A1 {'PASS' if a1_pass else 'FAIL'}: "
                     f"inclinacao@L=1e7 = {a1_final:+.4f} (alvo -0.25 +-0.05), "
                     f"aproximacao monotona: {bool(np.all(np.diff(diffs) <= 1e-6))}")

    # --- curvas exatas nas alturas do desenho + p_iid por variante ---
    cur = curves(design)
    p = {}
    for v, mu in cur.items():
        s, se = wls_slope(np.array(mu) - ll, x, w_design)
        p[v] = {"slope": s, "se_numeric": se}
        log_lines.append(f"p_iid_{v} (pesos de desenho) = {s:+.4f}")

    # --- A2/A3: simulacao do desenho completo, R replicas ---
    rng = np.random.default_rng(SEED_SIM)
    mu_v1 = np.array(cur["v1"])
    n_v1 = np.array([np.log(T) - LOG2PI for T in heights])
    s_v1 = np.array([np.sqrt(0.5 * np.log(np.log(T))) for T in heights])
    slopes, ses = np.empty(R_REPS), np.empty(R_REPS)
    for r in range(R_REPS):
        means, sds = np.empty(len(heights)), np.empty(len(heights))
        for i, T in enumerate(heights):
            u = rng.random(Ms[i])
            mx = s_v1[i] * ndtri(np.exp(np.log(u) / n_v1[i]))
            means[i] = mx.mean()
            sds[i] = mx.std(ddof=1)
        w_emp = Ms / sds**2
        slopes[r], ses[r] = wls_slope(means - ll, x, w_emp)
    p_true = p["v1"]["slope"]
    bias = float(slopes.mean() - p_true)
    tol_a2 = 3 * float(slopes.std(ddof=1)) / np.sqrt(R_REPS)
    a2_pass = abs(bias) <= tol_a2
    cover = float(np.mean(np.abs(slopes - p_true) <= 1.96 * ses))
    a3_pass = 0.917 <= cover <= 0.983
    log_lines.append(f"A2 {'PASS' if a2_pass else 'FAIL'}: vies = {bias:+.5f} "
                     f"(tol 3*EP = {tol_a2:.5f}); sd(inclinacoes) = "
                     f"{slopes.std(ddof=1):.4f}; media(EP_rep) = {ses.mean():.4f}")
    log_lines.append(f"A3 {'PASS' if a3_pass else 'FAIL'}: cobertura 95% = "
                     f"{cover:.3f} (aceite [0.917, 0.983])")

    all_pass = a1_pass and a2_pass and a3_pass
    out = {
        "seed_sim": SEED_SIM, "R_reps": R_REPS,
        "asymptotic_check_slopes": slopes_asym, "A1_pass": bool(a1_pass),
        "exact_curves_mu_by_variant": cur,
        "p_iid_by_variant": p,
        "sim_bias": bias, "sim_sd_slopes": float(slopes.std(ddof=1)),
        "sim_mean_se": float(ses.mean()),
        "A2_pass": bool(a2_pass), "coverage": cover, "A3_pass": bool(a3_pass),
        "ALL_PASS": bool(all_pass),
        "runtime_seconds": time.time() - t_start,
    }
    json.dump(out, open(HERE / "validation_iid_null.json", "w"), indent=2)
    tag = "" if all_pass else "_FAILED"
    (HERE / f"validation_iid_null{tag}.log").write_text(
        "validacao (a) iid/REM -- "
        + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n"
        + "\n".join(log_lines) + f"\nALL_PASS={all_pass}\n")
    for ln in log_lines:
        print(ln)
    print(f"[validate_iid] ALL_PASS={all_pass} "
          f"({time.time()-t_start:.0f}s)")


if __name__ == "__main__":
    main()
