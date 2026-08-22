"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- ANALISE PRIMARIA pre-registrada.
Executar SOMENTE depois do lock de PREREGISTRATION.md (secoes 4-6 de la
definem tudo o que este script implementa; nenhuma constante escondida:
curvas calibradas e correcoes de grade sao lidas dos JSONs de validacao
travados).

Modos:
  python3 run_primary.py compute --budget S   processa fatias pendentes de
      100 intervalos ate esgotar ~S segundos de parede (checkpoint por
      fatia em primary_slices/); re-invocar ate imprimir ALL_DONE.
  python3 run_primary.py analyze              agrega, aplica correcoes de
      grade travadas, roda a WLS e o veredito trinario TRAVADO; escreve
      primary_result.json + primary_run.log.

Offsets do teste real: por altura T (indice k na ordem declarada),
rng = default_rng(20260822*100 + k), starts = rng.uniform(T, 2T, M_T),
ordenados. Banda [T, 2T] e DISJUNTA das bandas descartaveis [2T+10, 2.1T]
usadas pelo piloto de tempo (seed 99991111) e pela calibracao de grade
(seed 77770707).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
SLICES = HERE / "primary_slices"
SEED_BASE = 20260822
LEN = 2 * np.pi
GRID = 512
SLICE_SIZE = 100


def load_design():
    d = json.load(open(HERE / "DESIGN.json"))
    heights = d["heights_primary"]
    M = {T: d["M"][f"{T:.0e}"] for T in heights}
    return d, heights, M


def starts_for(T, k, M):
    rng = np.random.default_rng(SEED_BASE * 100 + k)
    return np.sort(rng.uniform(T, 2 * T, M))


def max_grid(starts, npts=GRID):
    offs = np.arange(npts) * (LEN / npts)
    out = np.empty(len(starts))
    block = max(1, int(3e7 / (npts * np.sqrt(starts[0] / LEN))))
    for i in range(0, len(starts), block):
        s = starts[i:i + block]
        ts = (s[:, None] + offs[None, :]).ravel()
        z = Z(ts).reshape(len(s), npts)
        out[i:i + block] = np.log(np.max(np.abs(z), axis=1))
    return out


def pending_slices(heights, M):
    todo = []
    for k, T in enumerate(heights):
        for i0 in range(0, M[T], SLICE_SIZE):
            i1 = min(i0 + SLICE_SIZE, M[T])
            f = SLICES / f"h{k}_{i0}_{i1}.npy"
            if not f.exists():
                todo.append((k, T, i0, i1, f))
    return todo


def compute(budget):
    SLICES.mkdir(exist_ok=True)
    _, heights, M = load_design()
    todo = pending_slices(heights, M)
    if not todo:
        print("ALL_DONE")
        return
    t0 = time.time()
    for k, T, i0, i1, f in todo:
        st = starts_for(T, k, M[T])[i0:i1]
        mx = max_grid(st)
        tmp = f.with_suffix(".tmp.npy")
        np.save(tmp, mx)
        tmp.rename(f)
        el = time.time() - t0
        print(f"slice h{k} T={T:.0e} [{i0}:{i1}] ok ({el:.0f}s decorridos)",
              flush=True)
        # estimativa do custo da proxima fatia ~ custo medio da altura atual
        if el > budget:
            print(f"BUDGET_REACHED ({el:.0f}s) -- re-invocar")
            return
    print("ALL_DONE")


def wls(y, x, w):
    X = np.vstack([np.ones_like(x), x]).T
    XtWX = X.T @ (w[:, None] * X)
    beta = np.linalg.solve(XtWX, X.T @ (w * y))
    cov = np.linalg.inv(XtWX)
    resid = y - X @ beta
    chi2 = float(np.sum(w * resid**2))
    return beta, cov, chi2, resid


def analyze():
    design, heights, M = load_design()
    todo = pending_slices(heights, M)
    if todo:
        print(f"faltam {len(todo)} fatias -- rode compute primeiro")
        sys.exit(1)
    gb = json.load(open(HERE / "validation_grid_bias.json"))
    corr = {r["T"]: (r["correction_c"], r["se_c"]) for r in gb["rows"]}
    iid = json.load(open(HERE / "validation_iid_null.json"))
    cue = json.load(open(HERE / "validation_cue.json"))
    p_models = {
        "iid_v1": (iid["p_iid_by_variant"]["v1"]["slope"], 0.0),
        "iid_v2": (iid["p_iid_by_variant"]["v2"]["slope"], 0.0),
        "iid_v3": (iid["p_iid_by_variant"]["v3"]["slope"], 0.0),
        "cue_v1": (cue["p_cue_by_variant"]["v1"]["slope"],
                   cue["p_cue_by_variant"]["v1"]["se_mc"]),
        "cue_v2": (cue["p_cue_by_variant"]["v2"]["slope"],
                   cue["p_cue_by_variant"]["v2"]["se_mc"]),
    }

    log = []
    rows = []
    ys, ses_y, xs, lls = [], [], [], []
    for k, T in enumerate(heights):
        mx = np.concatenate([
            np.load(SLICES / f"h{k}_{i0}_{min(i0+SLICE_SIZE, M[T])}.npy")
            for i0 in range(0, M[T], SLICE_SIZE)])
        assert len(mx) == M[T]
        c, se_c = corr[T]
        mean_c = float(mx.mean() + c)
        sd = float(mx.std(ddof=1))
        se = float(np.sqrt(sd**2 / M[T] + se_c**2))
        llT = float(np.log(np.log(T)))
        lllT = float(np.log(np.log(np.log(T))))
        rows.append({"T": T, "M": M[T], "mean_max_raw": float(mx.mean()),
                     "grid_correction": c, "mean_max_corrected": mean_c,
                     "sd": sd, "se_total": se, "loglogT": llT,
                     "logloglogT": lllT})
        ys.append(mean_c - llT)
        ses_y.append(se)
        xs.append(lllT)
        lls.append(llT)
        log.append(f"T={T:.0e}: M={M[T]} mean(M*)corr={mean_c:.4f} sd={sd:.4f} "
                   f"se={se:.4f} y={mean_c-llT:+.4f}")
    y = np.array(ys)
    x = np.array(xs)
    w = 1.0 / np.array(ses_y) ** 2
    beta, cov, chi2, resid = wls(y, x, w)
    slope, se_slope = float(beta[1]), float(np.sqrt(cov[1, 1]))
    log.append(f"WLS: inclinacao = {slope:+.4f} +- {se_slope:.4f} | "
               f"chi2(5 gl) = {chi2:.2f}")

    z = {}
    for name, (p, se_p) in p_models.items():
        z[name] = float((slope - p) / np.sqrt(se_slope**2 + se_p**2))
        log.append(f"  z vs {name} (p={p:+.4f}): {z[name]:+.2f}")

    # ---- veredito trinario TRAVADO (PREREGISTRATION.md secao 6) ----
    fhk = (abs(z["cue_v1"]) < 3 and abs(z["iid_v1"]) >= 5
           and abs(z["iid_v2"]) >= 5 and abs(z["iid_v3"]) >= 3)
    iidv = (abs(z["iid_v1"]) < 3 and abs(z["cue_v1"]) >= 5
            and abs(z["cue_v2"]) >= 3)
    if fhk and not iidv:
        verdict = "FHK_FAVORED"
    elif iidv and not fhk:
        verdict = "IID_FAVORED"
    else:
        verdict = "INCONCLUSIVE"
    sub = ""
    if verdict == "INCONCLUSIVE":
        if abs(z["cue_v1"]) >= 3 and abs(z["iid_v1"]) >= 3:
            sub = "NEITHER_MODEL (ambas as curvas canonicas rejeitadas a 3 sigma)"
        elif abs(z["cue_v1"]) < 3 and abs(z["iid_v1"]) < 3:
            sub = "UNDERPOWERED (ambas as curvas canonicas compativeis)"
        else:
            sub = "PARTIAL (exclusao de um lado sem os requisitos completos do outro)"
    # descritor secundario (continuidade com a triagem): z vs assintoticos
    z_asym = {"fhk_-0.75": float((slope + 0.75) / se_slope),
              "rem_-0.25": float((slope + 0.25) / se_slope)}
    log.append(f"VEREDITO (regra travada): {verdict}" + (f" [{sub}]" if sub else ""))
    log.append(f"descritor secundario (assintoticos): z vs -0.75: "
               f"{z_asym['fhk_-0.75']:+.2f}; z vs -0.25: {z_asym['rem_-0.25']:+.2f}")

    out = {"locked_rule": "PREREGISTRATION.md secao 6", "rows": rows,
           "slope": slope, "se_slope": se_slope, "chi2_5dof": chi2,
           "residuals": resid.tolist(), "z_calibrated": z,
           "p_models": {k: list(v) for k, v in p_models.items()},
           "z_asymptotic_secondary": z_asym,
           "verdict": verdict, "inconclusive_subcase": sub,
           "holdout_1e11": "SEALED (nao computado nesta analise)"}
    json.dump(out, open(HERE / "primary_result.json", "w"), indent=2)
    (HERE / "primary_run.log").write_text(
        "analise primaria -- "
        + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n"
        + "\n".join(log) + "\n")
    for ln in log:
        print(ln)


if __name__ == "__main__":
    if sys.argv[1] == "compute":
        budget = float(sys.argv[sys.argv.index("--budget") + 1]) \
            if "--budget" in sys.argv else 500.0
        compute(budget)
    elif sys.argv[1] == "analyze":
        analyze()
    else:
        raise SystemExit("uso: run_primary.py compute [--budget S] | analyze")
