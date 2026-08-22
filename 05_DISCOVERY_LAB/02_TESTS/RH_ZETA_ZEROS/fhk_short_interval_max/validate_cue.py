"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- VALIDACAO (b), pre-lock: lado FHK via
polinomio caracteristico CUE.

Dicionario (declarado; honesto sobre tamanho finito): um intervalo de
comprimento 2pi na altura T contem ~log(T/2pi) zeros; o analogo CUE e uma
matriz de Haar-U(N) com
  v1 (canonica): N_T = log(T/2pi)      v2: N_T = log T
e a estatistica e max_theta log|p_A(e^{i theta})| sobre TODO o circulo
(comprimento 2pi, casando com o intervalo).
FHK (arXiv:1202.4713): E[max] = log N - (3/4) log log N + O(1).

Amostragem: autofases de U ~ Haar via QR de Ginibre complexo com correcao
de fase (Mezzadri, arXiv:math-ph/0609050 -- metodo padrao). log|p| avaliado
em grade de 4096 pontos (>170 pts por espacamento medio em N<=23; vies de
grade residual desprezivel comparado ao EP de MC). E(N) em N inteiro 7..23;
interpolacao linear em N para N_T nao-inteiro (curvatura de E(N) ~ 1/N^2,
erro << EP de MC).

CRITERIOS DE ACEITE (fixados ANTES de rodar):
  B1 (tendencia assintotica): inclinacao WLS de E(N)-logN sobre loglogN em
      N grandes {64,128,256} deve ser < -0.5 (mais perto de -3/4 do que de
      -1/4) -- checagem honesta de que o lado CUE tem a assinatura FHK ja
      em N moderado.
  B2 (precisao): EP de MC propagado para p_cue_v1 < 0.02.
  B3 (sanidade Haar): media de tr(U) sobre as amostras em N=7 com
      |media| < 3/sqrt(R*N/2) ~ compativel com 0 (Haar: E tr U = 0,
      var|trU|^2=1).
Falha => log preservado *_FAILED.log, corrigir para frente.

Saida: E(N) 7..23 (+64,128,256), p_cue_{v1,v2} com EP, sd do maximo por N.
"""
import json
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SEED_CUE = 27182818
N_SMALL = list(range(7, 24))
R_SMALL = 8000
N_LARGE = [64, 128, 256]
R_LARGE = 2000
GRID = 4096
LOG2PI = float(np.log(2 * np.pi))


def haar_eigenphases(N, R, rng):
    """Autofases de R matrizes Haar-U(N) (QR de Ginibre + correcao de fase).
    Retorna (R, N) fases e a media de tr(U) para sanidade."""
    phases = np.empty((R, N))
    trsum = 0.0 + 0.0j
    block = max(1, int(2e7 // (N * N)))
    for i in range(0, R, block):
        b = min(block, R - i)
        A = (rng.standard_normal((b, N, N)) + 1j * rng.standard_normal((b, N, N))) / np.sqrt(2)
        Q, Rm = np.linalg.qr(A)
        d = np.einsum('bii->bi', Rm)
        Q = Q * (d / np.abs(d))[:, None, :]
        ev = np.linalg.eigvals(Q)
        trsum += ev.sum()
        phases[i:i + b] = np.angle(ev)
    return phases, trsum / R


def mean_max_logpoly(phases, grid=GRID):
    """E e sd de max_theta sum_j log|e^{i theta}-e^{i phi_j}| na grade."""
    R, N = phases.shape
    theta = np.arange(grid) * (2 * np.pi / grid)
    mx = np.empty(R)
    block = max(1, int(4e7 // (grid * N)))
    for i in range(0, R, block):
        ph = phases[i:i + block]
        # log|e^{ia}-e^{ib}| = log(2|sin((a-b)/2)|)
        d = 0.5 * (theta[None, :, None] - ph[:, None, :])
        s = np.log(np.abs(2.0 * np.sin(d)))
        mx[i:i + block] = s.sum(axis=2).max(axis=1)
    return float(mx.mean()), float(mx.std(ddof=1)), mx


def wls_slope(y, x, w, yvar=None):
    X = np.vstack([np.ones_like(x), x]).T
    XtWX = X.T @ (w[:, None] * X)
    A = np.linalg.solve(XtWX, (w[:, None] * X).T)   # beta = A @ y
    beta = A @ y
    if yvar is not None:
        var_slope_mc = float((A[1] ** 2 @ yvar))
    else:
        var_slope_mc = float(np.linalg.inv(XtWX)[1, 1])
    return float(beta[1]), np.sqrt(var_slope_mc)


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED_CUE)
    design = json.load(open(HERE / "DESIGN.json"))
    heights = design["heights_primary"]
    Ms = np.array([design["M"][f"{T:.0e}"] for T in heights])
    sd_proj = np.array([design["sd_projected_per_height"][f"{T:.0e}"]
                        for T in heights])
    w_design = Ms / sd_proj**2
    x = np.array([np.log(np.log(np.log(T))) for T in heights])
    ll = np.array([np.log(np.log(T)) for T in heights])

    log_lines = []
    E, SD, SE = {}, {}, {}
    tr_mean_n7 = None
    for N in N_SMALL:
        ph, trm = haar_eigenphases(N, R_SMALL, rng)
        if N == 7:
            tr_mean_n7 = trm
        e, s, _ = mean_max_logpoly(ph)
        E[N], SD[N], SE[N] = e, s, s / np.sqrt(R_SMALL)
        log_lines.append(f"N={N}: E[max]={e:.4f} sd={s:.4f} se={SE[N]:.4f}")
        print(log_lines[-1], flush=True)

    # B1: N grandes
    E_L = {}
    for N in N_LARGE:
        ph, _ = haar_eigenphases(N, R_LARGE, rng)
        e, s, _ = mean_max_logpoly(ph)
        E_L[N] = (e, s / np.sqrt(R_LARGE))
        log_lines.append(f"N={N}: E[max]={e:.4f} se={E_L[N][1]:.4f}")
        print(log_lines[-1], flush=True)
    xl = np.array([np.log(np.log(N)) for N in N_LARGE])
    yl = np.array([E_L[N][0] - np.log(N) for N in N_LARGE])
    b1_slope, _ = wls_slope(yl, xl, np.ones(3))
    b1_pass = b1_slope < -0.5
    log_lines.append(f"B1 {'PASS' if b1_pass else 'FAIL'}: inclinacao CUE em "
                     f"N={{64,128,256}} = {b1_slope:+.4f} (aceite < -0.5; "
                     f"FHK assintotico -0.75)")

    # p_cue por variante: interpolacao linear de E(N) em N_T
    Ns = np.array(N_SMALL, dtype=float)
    Es = np.array([E[N] for N in N_SMALL])
    SEs = np.array([SE[N] for N in N_SMALL])
    p = {}
    for v, NT in [("v1", np.array([np.log(T) - LOG2PI for T in heights])),
                  ("v2", np.array([np.log(T) for T in heights]))]:
        mu = np.interp(NT, Ns, Es)
        # var da interpolacao linear: combinacao dos 2 vizinhos
        idx = np.searchsorted(Ns, NT) - 1
        idx = np.clip(idx, 0, len(Ns) - 2)
        frac = (NT - Ns[idx]) / (Ns[idx + 1] - Ns[idx])
        var_mu = (1 - frac) ** 2 * SEs[idx] ** 2 + frac ** 2 * SEs[idx + 1] ** 2
        s, se_mc = wls_slope(mu - ll, x, w_design, yvar=var_mu)
        p[v] = {"slope": s, "se_mc": float(se_mc), "mu": mu.tolist(),
                "N_T": NT.tolist()}
        log_lines.append(f"p_cue_{v} (pesos de desenho) = {s:+.4f} "
                         f"+- {se_mc:.4f} (MC)")
    b2_pass = bool(p["v1"]["se_mc"] < 0.02)
    log_lines.append(f"B2 {'PASS' if b2_pass else 'FAIL'}: EP MC de p_cue_v1 = "
                     f"{p['v1']['se_mc']:.4f} (aceite < 0.02)")
    b3_tol = 3.0 / np.sqrt(R_SMALL)
    b3_pass = bool(abs(tr_mean_n7) < b3_tol)
    log_lines.append(f"B3 {'PASS' if b3_pass else 'FAIL'}: |media tr U|_N=7 = "
                     f"{abs(tr_mean_n7):.4f} (aceite < {b3_tol:.4f})")

    all_pass = bool(b1_pass and b2_pass and b3_pass)
    out = {"seed": SEED_CUE, "R_small": R_SMALL, "R_large": R_LARGE,
           "grid": GRID,
           "E_by_N": {str(N): [E[N], SD[N], SE[N]] for N in N_SMALL},
           "E_large_N": {str(N): list(E_L[N]) for N in N_LARGE},
           "B1_largeN_slope": b1_slope, "B1_pass": b1_pass,
           "p_cue_by_variant": p, "B2_pass": b2_pass,
           "B3_trU_N7": [float(tr_mean_n7.real), float(tr_mean_n7.imag)],
           "B3_pass": b3_pass, "ALL_PASS": all_pass,
           "runtime_seconds": time.time() - t0}
    json.dump(out, open(HERE / "validation_cue.json", "w"), indent=2)
    tag = "" if all_pass else "_FAILED"
    (HERE / f"validation_cue{tag}.log").write_text(
        "validacao (b) CUE -- "
        + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n"
        + "\n".join(log_lines) + f"\nALL_PASS={all_pass}\n")
    print(f"[validate_cue] ALL_PASS={all_pass} ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
