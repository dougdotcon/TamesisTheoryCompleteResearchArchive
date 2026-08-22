"""
VALIDACAO (c) -- PODER DE DISCRIMINACAO do desenho travado (mesma
grade B(L)/factor/min_B da analise primaria real), verificado ANTES de
tocar dado real de zeta.

O alvo do teste real e "Modelo A (GUE, cresce ~log L) vs Modelo B
(Berry, satura/cresce muito mais devagar em L grande)". Construir um
substituto sintetico FIEL a formula exata de Berry (soma sobre
potencias de primos) exigiria simular um processo pontual com
correlacoes de longo alcance desenhadas para casar aquela soma
especifica -- fora do escopo viavel neste orcamento de tempo. Em vez
disso, usamos um substituto DECLARADO E HONESTO com a MESMA assinatura
QUALITATIVA que distingue os dois modelos (variancia do numero
SATURA/limitada em L grande, em vez de crescer tipo log L): uma rede
("lattice") de espacamento 1 com jitter i.i.d. limitado,
x_m = m + eps_m, eps_m ~ Uniform(-w,w).

Fato classico de teoria de processos pontuais (hiperuniformidade de
classe I / "jittered lattice"): para uma rede com jitter i.i.d.
limitado, a variancia do numero em janela de comprimento L e dominada
so pelas DUAS bordas da janela (os pontos do interior nunca cruzam a
borda desde que o jitter nao exceda meio espacamento) -- por isso
V(L) SATURA para uma CONSTANTE quando L cresce, em vez de crescer como
o log(L) do GUE. Verificado EMPIRICAMENTE abaixo com o proprio
estimador (nao so afirmado de memoria).

Este e um PROXY declarado, nao uma simulacao literal da formula de
Berry -- documentado honestamente como tal. Seu papel e mostrar que,
no NIVEL DE RUIDO REAL do desenho travado (mesmo numero de pontos e
mesma contagem de blocos B(L) que sera usado nos dados reais de
zeros1/zeros3), o teste tem poder para rejeitar o Modelo A quando a
verdade e QUALITATIVAMENTE do tipo "satura" -- condicao necessaria
para que a analise primaria real tenha alguma chance de distinguir os
modelos, dado que a separacao Modelo A vs Modelo B observada no piloto
exploratorio (REVIEW.md) e da MESMA natureza qualitativa (achatamento).

Sem dado real de zeta tocado.
"""
import json
import time
from pathlib import Path

import numpy as np

from estimator import model_A, block_number_variance, _exact_window_integral

HERE = Path(__file__).resolve().parent
SEED = 20260822_03

# escalas e L primarios EXATAMENTE como o desenho real (declarados em
# design_metadata.json / DESIGN.json -- nao ajustados depois de ver
# resultado real)
SCENARIOS = [
    {"name": "zeros1_scale", "M": 100_000, "L_primary": 2155.044, "B_target": 11, "n_replicas": 10},
    {"name": "zeros3_scale", "M": 10_000, "L_primary": 210.504, "B_target": 11, "n_replicas": 10},
]
JITTER_W = 0.45
FACTOR = 4.0


def make_jittered_lattice(rng, M, w):
    eps = rng.uniform(-w, w, size=M)
    x = np.arange(1, M + 1, dtype=float) + eps
    x.sort()  # jitter pode reordenar vizinhos raramente; contagem em janela nao exige ordem "de nascimento"
    return x


def main():
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    t0 = time.time()
    log(f"[validate_power_saturating] JITTER_W={JITTER_W} seed_base={SEED}")

    # --- checagem preliminar: o processo realmente satura (nao cresce tipo log L)? ---
    rng0 = np.random.default_rng(SEED)
    x0 = make_jittered_lattice(rng0, 50_000, JITTER_W)
    x_range0 = x0[-1] - x0[0]
    sat_grid = [5, 20, 80, 320, 1000, 3000]
    log("\n[checagem preliminar] V(L) do processo jittered-lattice (janela unica, M=50000):")
    sat_curve = {}
    for L in sat_grid:
        y_lo, y_hi = x0[0] + L / 2, x0[-1] - L / 2
        integral, span = _exact_window_integral(x0, y_lo, y_hi, L)
        v = integral / span
        sat_curve[str(L)] = v
        log(f"    L={L:6d}  V={v:.4f}   (model_A(L)={model_A(L):.4f}, cresce; saturando? ver padrao abaixo)")
    saturates = sat_curve[str(sat_grid[-1])] < 2 * sat_curve[str(sat_grid[len(sat_grid) // 2])]
    log(f"  [avaliacao] razao V(L=3000)/V(L=80) = {sat_curve[str(sat_grid[-1])]/sat_curve[str(sat_grid[2])]:.3f} "
        f"(GUE/model_A daria razao log(3000)/log(80) ~ {np.log(2*np.pi*3000)/np.log(2*np.pi*80):.3f} -- "
        f"se a razao empirica for MUITO menor, confirma saturacao qualitativa)")

    result = {"jitter_w": JITTER_W, "seed_base": SEED, "saturation_curve_single_window": sat_curve,
              "scenarios": {}}

    all_scenarios_ok = True
    for sc in SCENARIOS:
        name, M, L, B_target, n_rep = sc["name"], sc["M"], sc["L_primary"], sc["B_target"], sc["n_replicas"]
        log(f"\n[cenario {name}] M={M} L_primary={L} B_target(declarado)={B_target} n_replicas={n_rep}")
        z_list = []
        for r in range(n_rep):
            rng = np.random.default_rng(SEED + 100 + r)
            x = make_jittered_lattice(rng, M, JITTER_W)
            x_range = x[-1] - x[0]
            B_use = max(10, int(np.floor(x_range / (FACTOR * L))))
            edges = np.linspace(x[0], x[-1], B_use + 1)
            out = block_number_variance(x, edges, L, min_block_width_factor=3.0)
            if out["V_hat"] is None or out["SE"] is None or out["SE"] == 0:
                continue
            mA = float(model_A(L))
            z = (out["V_hat"] - mA) / out["SE"]
            z_list.append(z)
            log(f"    replica {r}: B_used={out['n_blocks_used']}  V_hat={out['V_hat']:.4f}  "
                f"SE={out['SE']:.4f}  model_A={mA:.4f}  z={z:+.2f}")
        z_arr = np.array(z_list)
        frac_reject = float(np.mean(np.abs(z_arr) >= 3.0))
        result["scenarios"][name] = {
            "M": M, "L_primary": L, "n_replicas_completed": len(z_arr),
            "z_values": z_arr.tolist(), "mean_z": float(np.mean(z_arr)),
            "frac_replicas_rejecting_model_A_at_3sigma": frac_reject,
        }
        ok = frac_reject >= 0.8  # poder projetado minimo declarado: >=80% das replicas rejeitam GUE a 3 sigma
        all_scenarios_ok = all_scenarios_ok and ok
        log(f"  [resultado {name}] media(z)={np.mean(z_arr):+.2f}  "
            f"fracao rejeitando Modelo A a 3sigma={frac_reject:.2f}  {'PASS(poder>=80%)' if ok else 'FAIL'}")

    result["all_pass"] = bool(all_scenarios_ok)
    result["wall_time_s"] = time.time() - t0
    log(f"\n[RESULTADO FINAL] all_pass={result['all_pass']}  wall_time={result['wall_time_s']:.1f}s")

    json.dump(result, open(HERE / "validation_power_saturating.json", "w"), indent=2)
    open(HERE / "validation_power_saturating.log", "w").write("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
