"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- Fase 0: piloto de VIABILIDADE (SOMENTE
custo/tempo). NAO computa nem registra nenhuma estatistica de teste em altura
nova: os maximos calculados internamente sao DESCARTADOS (apenas o tempo de
parede e registrado).

Intervalos descartaveis ("throwaway"): inicios deterministicos na banda
[2T+10, 2.1T], seed 99991111 -- banda DISJUNTA de [T, 2T], que e a banda de
onde sairao os offsets do teste real (seed distinto, declarado no
pre-registro). Estes offsets ficam EXCLUIDOS do teste real por construcao
(banda diferente). Documentados aqui e no log.

Alturas candidatas primarias: 1e4..1e10 (decadas). 1e11 NAO e tocada nesta
fase: e a altura de holdout selada; seu custo e projetado do piloto ja
preservado da triagem (item10_fhk_max.log: 7.71 s/intervalo a 256 pts) por
escala sqrt(T) e proporcionalidade no numero de pontos de grade.
"""
import json
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
SEED_THROWAWAY = 99991111
HEIGHTS = [1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]
LEN = 2 * np.pi
# n intervalos-descartaveis por altura (so p/ cronometrar; menos nas caras)
N_PILOT = {1e4: 16, 1e5: 16, 1e6: 16, 1e7: 12, 1e8: 8, 1e9: 6, 1e10: 4}
GRIDS = [512, 2048]


def eval_intervals(starts, npts):
    """Avalia Z na grade de npts pontos por intervalo; retorna maximos
    (descartados pelo chamador -- so o tempo importa nesta fase)."""
    offs = np.arange(npts) * (LEN / npts)
    ts = (starts[:, None] + offs[None, :]).ravel()
    z = Z(ts).reshape(len(starts), npts)
    return np.log(np.max(np.abs(z), axis=1))


def main():
    rng = np.random.default_rng(SEED_THROWAWAY)
    out = {"purpose": "timing only -- no test statistic recorded",
           "throwaway_offset_band": "[2T+10, 2.1T] (disjoint from test band [T,2T])",
           "seed_throwaway": SEED_THROWAWAY,
           "grids": GRIDS, "rows": []}
    log = []
    for T in HEIGHTS:
        n = N_PILOT[T]
        starts = np.sort(rng.uniform(2 * T + 10, 2.1 * T, n))
        row = {"T": T, "n_pilot": n, "throwaway_starts": starts.tolist()}
        for g in GRIDS:
            # warmup pequeno para amortizar alocacoes na 1a chamada
            _ = eval_intervals(starts[:1], g)
            t0 = time.time()
            _discard = eval_intervals(starts, g)  # maximos DESCARTADOS
            dt = time.time() - t0
            row[f"sec_per_interval_grid{g}"] = dt / n
        out["rows"].append(row)
        msg = (f"T={T:.0e}: {row['sec_per_interval_grid512']*1000:.1f} ms/int @512 | "
               f"{row['sec_per_interval_grid2048']*1000:.1f} ms/int @2048")
        print(msg)
        log.append(msg)
    # projecao 1e11 (NAO tocada): triagem mediu 7.71 s/int @256 -> escala linear
    # no numero de pontos de grade
    proj_512 = 7.71 * (512 / 256)
    out["holdout_1e11_projection"] = {
        "basis": "triage item10_fhk_max.log pilot: 7.71 s/interval @256 pts",
        "projected_sec_per_interval_grid512": proj_512}
    log.append(f"1e11 (holdout, NAO tocada): projecao {proj_512:.1f} s/int @512 "
               f"(base: piloto da triagem @256)")
    print(log[-1])
    json.dump(out, open(HERE / "phase0_timing.json", "w"), indent=2)
    (HERE / "phase0_timing.log").write_text(
        "phase0 timing pilot -- " + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        + "\nthrowaway band [2T+10, 2.1T], seed 99991111; maxima discarded\n"
        + "\n".join(log) + "\n")
    print("[phase0] salvo phase0_timing.{json,log}")


if __name__ == "__main__":
    main()
