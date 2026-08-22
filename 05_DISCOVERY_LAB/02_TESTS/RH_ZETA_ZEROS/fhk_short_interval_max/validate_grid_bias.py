"""
DISC-RH-FHK-SHORT-INTERVAL-MAX-001 -- VALIDACAO (c), pre-lock: vies de grade.

O maximo sobre grade discreta SUBESTIMA o maximo continuo do intervalo. Este
script calibra a correcao por altura em intervalos DESCARTAVEIS (banda
[2T+10, 2.1T], seed 77770707 -- disjunta da banda de teste [T,2T] e distinta
dos offsets do piloto de tempo), comparando grade 512 vs 2048.

DISCIPLINA ANTI-VAZAMENTO: este script registra SOMENTE as diferencas
d_i = max_2048 - max_512 por intervalo (e estatisticas delas) -- NUNCA os
valores dos maximos em si. As diferencas nao carregam informacao util sobre
mean(M*) por altura; nenhuma estatistica de teste e computada aqui.

Correcao pre-declarada (Richardson, vies ~ passo^2):
  vies_512(T) ~ (16/15) * mean(d_i)   [pois d = vies_512 - vies_2048
                                       = vies_512 (1 - 1/16)]
  EP da correcao = (16/15) * sd(d_i)/sqrt(n_cal)
Aplicacao na analise primaria: y_T <- mean(M*_512) + c_T; EP_T^2 <-
sd^2/M + EP(c_T)^2.

CRITERIOS DE ACEITE (fixados ANTES de rodar):
  C1: c_T > 0 (subestimacao) e c_T < 0.02 em todas as alturas;
  C2: contribuicao do gradiente do vies para a inclinacao (WLS das c_T
      sobre logloglogT, pesos de desenho) < 0.05 em modulo -- i.e., mesmo
      sem correcao o vies nao viraria o veredito; como a correcao E
      aplicada, o residuo e de segunda ordem;
  C3: EP(c_T) <= 0.004 em todas as alturas.
Falha => log preservado *_FAILED.log; corrigir para frente.
"""
import json
import time
from pathlib import Path

import numpy as np

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
SEED_CAL = 77770707
LEN = 2 * np.pi
N_CAL = {1e4: 80, 1e5: 80, 1e6: 60, 1e7: 60, 1e8: 24, 1e9: 16, 1e10: 8}


def max_grid(starts, npts):
    offs = np.arange(npts) * (LEN / npts)
    out = np.empty(len(starts))
    block = max(1, int(3e7 / (npts * np.sqrt(starts[0] / LEN))))
    for i in range(0, len(starts), block):
        s = starts[i:i + block]
        ts = (s[:, None] + offs[None, :]).ravel()
        z = Z(ts).reshape(len(s), npts)
        out[i:i + block] = np.log(np.max(np.abs(z), axis=1))
    return out


def main():
    t0 = time.time()
    design = json.load(open(HERE / "DESIGN.json"))
    heights = design["heights_primary"]
    rng = np.random.default_rng(SEED_CAL)
    log_lines, rows = [], []
    for T in heights:
        n = N_CAL[T]
        starts = np.sort(rng.uniform(2 * T + 10, 2.1 * T, n))
        m512 = max_grid(starts, 512)
        m2048 = max_grid(starts, 2048)
        d = m2048 - m512          # somente diferencas sao registradas
        c = (16.0 / 15.0) * float(np.mean(d))
        se_c = (16.0 / 15.0) * float(np.std(d, ddof=1) / np.sqrt(n))
        rows.append({"T": T, "n_cal": n, "correction_c": c, "se_c": se_c,
                     "d_summary": {"mean": float(np.mean(d)),
                                   "sd": float(np.std(d, ddof=1)),
                                   "min": float(np.min(d)),
                                   "max": float(np.max(d))}})
        log_lines.append(f"T={T:.0e}: n={n} c_T={c:+.5f} EP={se_c:.5f}")
        print(log_lines[-1], flush=True)

    cs = np.array([r["correction_c"] for r in rows])
    ses = np.array([r["se_c"] for r in rows])
    c1 = bool(np.all(cs > 0) and np.all(cs < 0.02))
    x = np.array([np.log(np.log(np.log(T))) for T in heights])
    Ms = np.array([design["M"][f"{T:.0e}"] for T in heights])
    sd_proj = np.array([design["sd_projected_per_height"][f"{T:.0e}"]
                        for T in heights])
    w = Ms / sd_proj**2
    X = np.vstack([np.ones_like(x), x]).T
    beta = np.linalg.solve(X.T @ (w[:, None] * X), X.T @ (w * cs))
    grad = float(beta[1])
    c2 = bool(abs(grad) < 0.05)
    c3 = bool(np.all(ses <= 0.004))
    log_lines.append(f"C1 {'PASS' if c1 else 'FAIL'}: 0 < c_T < 0.02 em todas")
    log_lines.append(f"C2 {'PASS' if c2 else 'FAIL'}: gradiente do vies na "
                     f"inclinacao = {grad:+.5f} (aceite |.| < 0.05)")
    log_lines.append(f"C3 {'PASS' if c3 else 'FAIL'}: max EP(c_T) = "
                     f"{ses.max():.5f} (aceite <= 0.004)")
    all_pass = c1 and c2 and c3
    out = {"seed": SEED_CAL,
           "throwaway_band": "[2T+10, 2.1T] (disjoint from test band [T,2T])",
           "note": "somente diferencas max2048-max512 registradas; nenhum "
                   "valor de maximo e persistido (anti-vazamento)",
           "rows": rows, "bias_slope_contribution": grad,
           "C1_pass": c1, "C2_pass": c2, "C3_pass": c3,
           "ALL_PASS": bool(all_pass), "runtime_seconds": time.time() - t0}
    json.dump(out, open(HERE / "validation_grid_bias.json", "w"), indent=2)
    tag = "" if all_pass else "_FAILED"
    (HERE / f"validation_grid_bias{tag}.log").write_text(
        "validacao (c) vies de grade -- "
        + time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n"
        + "\n".join(log_lines) + f"\nALL_PASS={all_pass}\n")
    print(f"[validate_grid_bias] ALL_PASS={all_pass} ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
