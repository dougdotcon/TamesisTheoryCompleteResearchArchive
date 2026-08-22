"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- checagens de sanidade S1/S2 da Secao 6
do PREREGISTRATION.md (mecanicas, nao alteram a regra; decidem apenas entre
veredito VALIDO e INVALID_RUN).

S1: nas alturas 1e5, 1e7, 1e9, |mean(M*)_novo - mean(M*)_triagem| <
    4*sqrt(EP_novo^2 + EP_triagem^2)  (ambos corrigidos de vies de grade;
    triagem: item10_fhk_result.json, seed distinto 20260821).
S2: sd empirico por altura em [0.3, 0.9].

Nota de processo (honesta): estas checagens estao declaradas na Secao 6 do
pre-registro mas nao foram embutidas em run_primary.py (escrito antes do
texto final do lock); este script as executa exatamente como declaradas,
imediatamente apos a analise, sem tocar na regra de decisao.
"""
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TRIAGE = HERE.parent / "phase0_zeta_eval_triage" / "item10_fhk_result.json"


def main():
    pr = json.load(open(HERE / "primary_result.json"))
    tr = json.load(open(TRIAGE))
    tri = {r["T"]: r for r in tr["heights"]}
    rows, s1_ok = [], True
    for r in pr["rows"]:
        T = r["T"]
        if T not in tri:
            continue
        t = tri[T]
        mean_tri = t["mean_max_log_absZ"] + t["grid_bias_256_vs_1024_mean"]
        se_tri = t["se_mean"]
        diff = r["mean_max_corrected"] - mean_tri
        tol = 4 * np.sqrt(r["se_total"] ** 2 + se_tri ** 2)
        ok = bool(abs(diff) < tol)
        s1_ok &= ok
        rows.append({"T": T, "mean_new": r["mean_max_corrected"],
                     "mean_triage_corr": mean_tri, "diff": diff,
                     "tol_4sigma": tol, "pass": ok})
        print(f"S1 T={T:.0e}: diff={diff:+.4f} tol={tol:.4f} "
              f"{'PASS' if ok else 'FAIL'}")
    sds = [r["sd"] for r in pr["rows"]]
    s2_ok = bool(min(sds) >= 0.3 and max(sds) <= 0.9)
    print(f"S2: sd range [{min(sds):.3f}, {max(sds):.3f}] "
          f"{'PASS' if s2_ok else 'FAIL'}")
    status = "VALID" if (s1_ok and s2_ok) else "INVALID_RUN"
    print(f"STATUS: {status} -> veredito da regra travada "
          f"{'mantido' if status == 'VALID' else 'RETIDO'}")
    json.dump({"S1_rows": rows, "S1_pass": bool(s1_ok), "S2_sds": sds,
               "S2_pass": s2_ok, "run_status": status},
              open(HERE / "sanity_checks.json", "w"), indent=2)


if __name__ == "__main__":
    main()
