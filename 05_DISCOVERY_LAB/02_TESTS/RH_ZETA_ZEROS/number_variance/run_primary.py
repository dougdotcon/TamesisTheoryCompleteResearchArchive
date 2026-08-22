"""
ANALISE PRIMARIA -- roda o desenho travado em DESIGN.json sobre o dado
REAL de zeros1.txt e zeros3.txt. NENHUM parametro e reajustado depois de
ver o resultado. zeros4.txt (holdout selado) NAO e tocado por este
script.

Implementa exatamente a Secao 7 do PREREGISTRATION.md (regra ternaria).
"""
import json
import time
from pathlib import Path

import numpy as np

from estimator import (N_absolute, local_density, block_number_variance,
                        model_A, sieve_primes, prime_power_terms,
                        model_B_exact, model_B_bounded, bound_k_ge2_tail_beyond)

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"

REJECT_Z = 3.0
ACCEPT_Z = 2.0


def load_zeros1():
    vals = np.array([float(x) for x in open(DATA_DIR / "zeros1.txt").read().split()])
    assert len(vals) == 100000
    return vals


def load_offset_file(path, expected_n=10000):
    offsets = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            offsets.append(float(line))
        except ValueError:
            continue
    offsets = np.array(offsets)
    assert len(offsets) == expected_n
    assert np.all(np.diff(offsets) > 0)
    return offsets


def analyze_dataset(name, x, T, design_entry, model_B_fn, log):
    xr = design_entry["x_range"]
    rows = []
    for g in design_entry["grid"]:
        if not g["usable"]:
            continue
        L = g["L"]
        B_target = g["B"]
        edges = np.linspace(x[0], x[-1], B_target + 1)
        out = block_number_variance(x, edges, L, min_block_width_factor=3.0)
        mA = float(model_A(L))
        mB = model_B_fn(L)  # dict {"point":..} ou {"lower":..,"upper":..}
        if out["V_hat"] is None:
            log(f"  [{name}] L={L:9.2f} (mult={g['mult']}): dado insuficiente apos filtragem de blocos")
            continue
        Vhat, SE = out["V_hat"], out["SE"]
        zA = (Vhat - mA) / SE if SE and SE > 0 else float("nan")
        if "point" in mB:
            zB = (Vhat - mB["point"]) / SE if SE and SE > 0 else float("nan")
        else:
            if mB["lower"] <= Vhat <= mB["upper"]:
                zB = 0.0
            else:
                nearest = mB["lower"] if Vhat < mB["lower"] else mB["upper"]
                zB = (Vhat - nearest) / SE if SE and SE > 0 else float("nan")
        row = {"mult": g["mult"], "L": L, "B_used": out["n_blocks_used"],
               "B_dropped": out["n_blocks_dropped"], "V_hat": Vhat, "SE": SE,
               "model_A": mA, "model_B": mB, "z_A": zA, "z_B": zB,
               "proven_corollary_1_4_3": g["proven_corollary_1_4_3"]}
        rows.append(row)
        log(f"  [{name}] L={L:9.2f} (mult={g['mult']:5.1f}, B={out['n_blocks_used']:3d})  "
            f"V_hat={Vhat:8.4f}  SE={SE:7.4f}  model_A={mA:7.4f} (z_A={zA:+7.2f})  "
            f"model_B={mB}  (z_B={zB:+7.2f})")
    return rows


def main():
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    t0 = time.time()
    design = json.load(open(HERE / "DESIGN.json"))
    log(f"[run_primary] inicio {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # --- zeros1 ---
    g1 = load_zeros1()
    x1 = N_absolute(g1)
    x1.sort()
    T1 = float(g1[-1])
    log(f"[zeros1] T={T1:.3f} n={len(g1)}")
    p1 = sieve_primes(int(np.ceil(T1)))
    pk1, logpk1, w1 = prime_power_terms(p1, T1)
    log(f"[zeros1] {len(pk1)} potencias de primos <= T (Modelo B EXATO)")

    def modelB_zeros1(L):
        v = float(model_B_exact(np.array([L]), T1, pk1, logpk1, w1)[0])
        return {"point": v, "exact": True}

    rows1 = analyze_dataset("zeros1", x1, T1, design["datasets"]["zeros1"], modelB_zeros1, log)

    # --- zeros3 ---
    base3 = 267653395647.0
    off3 = load_offset_file(DATA_DIR / "zeros3.txt")
    dens3 = local_density(base3)
    x3 = off3 * dens3
    x3.sort()
    log(f"\n[zeros3] T(base)={base3:.1f} n={len(off3)} density={dens3:.4f}")
    P_CUTOFF3 = design["model_B_P_cutoff"]["zeros3"]
    p3 = sieve_primes(P_CUTOFF3)
    pk3, logpk3, w3 = prime_power_terms(p3, P_CUTOFF3)
    kge2_tail3 = bound_k_ge2_tail_beyond(P_CUTOFF3, base3)
    log(f"[zeros3] {len(pk3)} potencias de primos <= P_cutoff={P_CUTOFF3:.0e} (Modelo B LIMITADO)")

    def modelB_zeros3(L):
        lo, hi = model_B_bounded(np.array([L]), base3, pk3, logpk3, w3, P_CUTOFF3, kge2_tail3)
        return {"lower": float(lo[0]), "upper": float(hi[0]), "exact": False}

    rows3 = analyze_dataset("zeros3", x3, base3, design["datasets"]["zeros3"], modelB_zeros3, log)

    # --- pontos decisivos primarios (maior L usavel de cada dataset) ---
    primary1 = max(rows1, key=lambda r: r["L"])
    primary3 = max(rows3, key=lambda r: r["L"])
    secondary1 = sorted(rows1, key=lambda r: r["L"])[-2] if len(rows1) >= 2 else None
    secondary3 = sorted(rows3, key=lambda r: r["L"])[-2] if len(rows3) >= 2 else None

    log(f"\n=== PONTOS DECISIVOS PRIMARIOS ===")
    log(f"zeros1: L={primary1['L']:.3f}  z_A={primary1['z_A']:+.3f}  z_B={primary1['z_B']:+.3f}")
    log(f"zeros3: L={primary3['L']:.3f}  z_A={primary3['z_A']:+.3f}  z_B={primary3['z_B']:+.3f}")

    zA1, zB1 = primary1["z_A"], primary1["z_B"]
    zA3, zB3 = primary3["z_A"], primary3["z_B"]

    berry_favored = (abs(zA1) >= REJECT_Z and abs(zA3) >= REJECT_Z and
                     abs(zB1) < ACCEPT_Z and abs(zB3) < ACCEPT_Z)
    gue_favored = (abs(zB1) >= REJECT_Z and abs(zB3) >= REJECT_Z and
                   abs(zA1) < ACCEPT_Z and abs(zA3) < ACCEPT_Z)

    if berry_favored:
        verdict, subcase = "BERRY_FAVORED", None
    elif gue_favored:
        verdict, subcase = "GUE_FAVORED", None
    else:
        verdict = "INCONCLUSIVE"
        both_A_rejected = abs(zA1) >= REJECT_Z and abs(zA3) >= REJECT_Z
        both_B_rejected = abs(zB1) >= REJECT_Z and abs(zB3) >= REJECT_Z
        both_A_ok = abs(zA1) < REJECT_Z and abs(zA3) < REJECT_Z
        both_B_ok = abs(zB1) < REJECT_Z and abs(zB3) < REJECT_Z
        # desacordo entre datasets: um dataset rejeita A mas nao B, outro rejeita B mas nao A
        d1_favors_berry = abs(zA1) >= REJECT_Z and abs(zB1) < ACCEPT_Z
        d1_favors_gue = abs(zB1) >= REJECT_Z and abs(zA1) < ACCEPT_Z
        d3_favors_berry = abs(zA3) >= REJECT_Z and abs(zB3) < ACCEPT_Z
        d3_favors_gue = abs(zB3) >= REJECT_Z and abs(zA3) < ACCEPT_Z
        if both_A_rejected and both_B_rejected:
            subcase = "NEITHER_MODEL"
        elif (d1_favors_berry and d3_favors_gue) or (d1_favors_gue and d3_favors_berry):
            subcase = "PARTIAL_DISAGREEMENT"
        elif both_A_ok or both_B_ok:
            subcase = "UNDERPOWERED"
        else:
            subcase = "PARTIAL_DISAGREEMENT"

    log(f"\n*** VEREDITO: {verdict}" + (f" ({subcase})" if subcase else "") + " ***")

    # --- checagens de sanidade (nao decisivas) ---
    def same_sign(a, b):
        return (a >= 0) == (b >= 0)

    s1_pass = True
    if secondary1:
        s1_1 = same_sign(primary1["z_A"], secondary1["z_A"])
        s1_pass = s1_pass and s1_1
        log(f"\n[S1] zeros1: sinal(z_A primario)={'​+' if primary1['z_A']>=0 else '-'} "
            f"vs sinal(z_A secundario, L={secondary1['L']:.1f})="
            f"{'+' if secondary1['z_A']>=0 else '-'}  {'OK' if s1_1 else 'FALHA'}")
    if secondary3:
        s1_3 = same_sign(primary3["z_A"], secondary3["z_A"])
        s1_pass = s1_pass and s1_3
        log(f"[S1] zeros3: sinal(z_A primario)={'+' if primary3['z_A']>=0 else '-'} "
            f"vs sinal(z_A secundario, L={secondary3['L']:.1f})="
            f"{'+' if secondary3['z_A']>=0 else '-'}  {'OK' if s1_3 else 'FALHA'}")

    run_status = "VALID" if s1_pass else "INVALID_RUN"
    log(f"\n[status da rodada] {run_status}")

    result = {
        "design_used": "DESIGN.json (travado antes desta rodada)",
        "zeros1": {"T": T1, "n_zeros": len(g1), "rows": rows1,
                   "primary": primary1, "secondary": secondary1},
        "zeros3": {"T": base3, "n_zeros": len(off3), "rows": rows3,
                   "primary": primary3, "secondary": secondary3, "P_cutoff_model_B": P_CUTOFF3},
        "verdict": verdict, "subcase": subcase, "run_status": run_status,
        "thresholds": {"reject_z": REJECT_Z, "accept_z": ACCEPT_Z},
        "wall_time_s": time.time() - t0,
    }
    log(f"\n[fim] wall_time={result['wall_time_s']:.1f}s")

    json.dump(result, open(HERE / "primary_result.json", "w"), indent=2)
    open(HERE / "primary_run.log", "w").write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
