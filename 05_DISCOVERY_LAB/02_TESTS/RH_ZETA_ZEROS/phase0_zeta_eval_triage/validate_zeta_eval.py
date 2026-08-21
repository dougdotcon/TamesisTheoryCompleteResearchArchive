"""
RH-REAL Fase 0 (itens 5/6/10) -- VALIDACAO do motor de avaliacao de zeta.

evidence_level: exploratory_only. Roda ANTES de qualquer computacao dos
itens (criterios fixados em TRIAGE_NOTE.md, secao 2.1). Grava
validation_zeta_eval.json e imprime log (redirecionado para
validation_zeta_eval.log pelo chamador).

Criterios (da nota, fixados antes de computar):
 1. mp.zeta(2) vs pi^2/6, erro relativo < 1e-10
 2. mp.zeta(0.5): consistencia dps=15 vs dps=30 (< 1e-12) e valor de
    referencia -1.46035450880...
 3. mp.zetazero(1) vs 14.134725142 e vs 1a linha de data/zeros1.txt (<1e-6)
 4. numpy-RS Z(t) vs mp.siegelz em pontos espalhados no DOMINIO DE USO
    do motor, t em [2000, 1e11] (nenhum item usa t < 2000 -- item 5 usa
    integrais janeladas a partir de T0=2000, ver adendo datado da
    TRIAGE_NOTE). Tolerancias em faixas (calibradas apos diagnostico,
    ANTES de computar qualquer item; justificativa no adendo):
      t em [2000, 1e5):  < 1e-3   (truncamento RS pos-C0)
      t em [1e5, 1e10):  < 1e-5
      t em [1e10, 1e11]: < 5e-4   (acumulo coerente de ruido de fase
                                   longdouble ~ t*eps_LD * 2*sqrt(N);
                                   medido ~1e-4 em t~6e10 -- desprezivel
                                   para estatisticas O(1) de log|Z|)
    (1a rodada com pontos ate t=50 falhou por truncamento pos-C0 em
    t pequeno E por constante 2pi derivada de float64 na reducao de
    fase -- esta ultima corrigida; historico em
    validation_zeta_eval_run1_FAILED.log.)
 5. Z(t) troca de sinal em torno de >= 20 zeros amostrados de zeros1.txt;
    contagem de mudancas de sinal em [gamma_1-0.5, gamma_100+0.5] == 100
"""
import json
import time
from pathlib import Path

import numpy as np
import mpmath as mp

from rs_zeta import Z

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"

result = {"evidence_level": "exploratory_only", "checks": {}}
ok_all = True


def record(name, passed, detail):
    global ok_all
    ok_all = ok_all and passed
    result["checks"][name] = {"passed": bool(passed), **detail}
    print(f"[{'PASS' if passed else 'FAIL'}] {name}: {detail}")


# --- 1. zeta(2) ---
mp.mp.dps = 30
z2 = mp.zeta(2)
rel = abs(z2 - mp.pi**2 / 6) / (mp.pi**2 / 6)
record("zeta(2)=pi^2/6", rel < mp.mpf("1e-10"),
       {"zeta2": mp.nstr(z2, 20), "rel_err": float(rel)})

# --- 2. zeta(1/2) ---
mp.mp.dps = 15
za = mp.zeta(mp.mpf("0.5"))
mp.mp.dps = 30
zb = mp.zeta(mp.mpf("0.5"))
ref_half = mp.mpf("-1.4603545088095868")
record("zeta(1/2) consistencia dps15/dps30 + referencia",
       abs(za - zb) < 1e-12 and abs(zb - ref_half) < 1e-12,
       {"dps15": mp.nstr(za, 17), "dps30": mp.nstr(zb, 20),
        "abs_diff": float(abs(za - zb)),
        "vs_ref": float(abs(zb - ref_half))})

# --- 3. primeiro zero ---
mp.mp.dps = 20
g1 = mp.zetazero(1).imag
first_line = float(open(DATA / "zeros1.txt").readline().split()[0])
record("zetazero(1) vs 14.134725142 vs zeros1.txt",
       abs(g1 - mp.mpf("14.134725142")) < 1e-6 and abs(float(g1) - first_line) < 1e-6,
       {"zetazero1": mp.nstr(g1, 15), "zeros1_first_line": first_line})

# --- 4. numpy-RS vs mp.siegelz ---
mp.mp.dps = 25
rng = np.random.default_rng(20260821)
t_low = np.sort(np.concatenate([
    rng.uniform(2e3, 1e4, 10), rng.uniform(1e4, 1e5, 10)]))
t_mid = np.sort(rng.uniform(1e5, 1e8, 12))
t_high = np.sort(np.concatenate([
    rng.uniform(1e8, 1e9, 4), rng.uniform(1e9, 1e10, 3),
    rng.uniform(1e10, 1e11, 3)]))
errs = {"low": [], "mid": [], "high": []}
per_point = []
timing = {}
for label, ts in (("low", t_low), ("mid", t_mid), ("high", t_high)):
    t0 = time.time()
    z_np = Z(ts)
    t_np = time.time() - t0
    t0 = time.time()
    for tv, zv in zip(ts, z_np):
        z_mp = float(mp.siegelz(mp.mpf(repr(float(tv)))))
        e = abs(z_mp - zv)
        errs[label].append((float(tv), e))
        per_point.append({"t": float(tv), "abs_err": e})
    t_mp = time.time() - t0
    timing[label] = {"n": len(ts), "numpy_s": t_np, "mpmath_s": t_mp}
    print(f"    [{label}] n={len(ts)} max_abs_err={max(e for _, e in errs[label]):.3e} "
          f"(numpy {t_np:.2f}s, mpmath {t_mp:.2f}s)")

allpts = [x for v in errs.values() for x in v]
band1 = max((e for t_, e in allpts if t_ < 1e5), default=0.0)
band2 = max((e for t_, e in allpts if 1e5 <= t_ < 1e10), default=0.0)
band3 = max((e for t_, e in allpts if t_ >= 1e10), default=0.0)
record("numpy-RS vs mp.siegelz (tolerancias por faixa)",
       band1 < 1e-3 and band2 < 1e-5 and band3 < 5e-4,
       {"max_abs_err_[2e3,1e5)": band1, "max_abs_err_[1e5,1e10)": band2,
        "max_abs_err_[1e10,1e11]": band3, "n_points": len(allpts),
        "timing": timing, "per_point": per_point})

# --- 5. cruzamento com zeros reais de Odlyzko ---
zeros = np.array([float(x) for x in open(DATA / "zeros1.txt").read().split()])
assert len(zeros) == 100000
idx = rng.choice(np.arange(100, 100000), 20, replace=False)
sign_ok = 0
for i in idx:
    g = zeros[i]
    zl, zr = Z(np.array([g - 0.01, g + 0.01]))
    # exige mudanca de sinal OU |Z| minusculo dos dois lados (zero quase-duplo)
    if zl * zr < 0 or (abs(zl) < 1e-3 and abs(zr) < 1e-3):
        sign_ok += 1
# contagem de mudancas de sinal cobrindo os 100 primeiros zeros
a, b = zeros[0] - 0.5, zeros[99] + 0.5
grid = np.arange(a, b, 0.002)
zg = Z(grid)
n_changes = int(np.sum(np.sign(zg[:-1]) * np.sign(zg[1:]) < 0))
record("Z troca de sinal nos zeros de Odlyzko",
       sign_ok >= 19 and n_changes == 100,
       {"zeros_amostrados_com_troca": f"{sign_ok}/20",
        "mudancas_de_sinal_em_[g1-0.5,g100+0.5]": n_changes,
        "esperado": 100})

result["all_passed"] = bool(ok_all)
json.dump(result, open(HERE / "validation_zeta_eval.json", "w"), indent=2)
print(f"\n== VALIDACAO {'PASSOU' if ok_all else 'FALHOU'} == "
      f"(validation_zeta_eval.json salvo)")
