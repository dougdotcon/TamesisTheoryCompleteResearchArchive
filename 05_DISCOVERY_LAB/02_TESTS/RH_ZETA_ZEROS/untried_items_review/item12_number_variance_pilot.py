"""
PILOT (NOT a preregistration) -- item 12 do levantamento original de
2026-08-12 ("variancia do numero / rigidez GUE"), reconstruido via
literatura verificada nesta sessao como o objeto padrao "number variance"
de zeros de zeta, Sigma^2(L) / V(L;x), Berry (1988) + prova condicional
recente (Lugar-Milinovich-Quesada-Herrera, arXiv:2211.14918, 2022).

evidence_level: exploratory_only. NAO produz nenhuma alegacao travada.
Objetivo: (a) computar a variancia do numero empirica V(L) para os tres
datasets reais ja em ../data/ (zeros1, zeros3, zeros4); (b) comparar
contra o Modelo A (formula fechada de Berry para o regime universal,
eq 1.19/Conjectura 1.4.1(a) do paper acima, que coincide com a formula
GUE-RMT de variancia do numero); (c) para zeros1 (T pequeno, T~75000),
computar tambem o Modelo B EXATO (Conjectura 1.4.1(b), soma sobre
primeiras potencias de primos) -- para zeros3/zeros4 (T~10^11/10^20) o
Modelo B e computado apenas de forma TRUNCADA (primos <= 10^7),
explicitamente rotulado como sub-estimativa, nao um teste real.

Sem dado fabricado. Falha de leitura de arquivo e erro fatal.
"""
import json
from pathlib import Path

import numpy as np
from scipy.special import sici

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "data"
GAMMA0 = 0.5772156649015329  # Euler-Mascheroni


def load_zeros1():
    vals = np.array([float(x) for x in open(DATA_DIR / "zeros1.txt").read().split()])
    assert len(vals) == 100000
    return vals


def load_offset_file(path, base, expected_n=10000):
    """zeros3.txt / zeros4.txt: linhas de cabecalho em prosa + N valores
    numericos (offsets de `base`). Le todas as linhas, tenta float() em
    cada uma, mantem so as que funcionam -- robusto ao numero exato de
    linhas de cabecalho/rodape sem assumir uma contagem fixa."""
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
    assert len(offsets) == expected_n, f"{path}: esperado {expected_n}, achado {len(offsets)}"
    assert np.all(np.diff(offsets) > 0), f"{path}: offsets deveriam estar em ordem crescente"
    return offsets, float(base)


def renormalize_absolute(gammas):
    """x_m = N(gamma_m), N(E) = E/(2pi) (log(E/(2pi)) - 1) + 7/8 -- espacamento
    medio exatamente 1 (Riemann-von Mangoldt, termo principal)."""
    return gammas / (2 * np.pi) * (np.log(gammas / (2 * np.pi)) - 1) + 7 / 8


def renormalize_local(offsets, base):
    """Para janelas estreitas (offset << base): x_m = offset_m * density(base),
    density(E) = N'(E) = (1/2pi) log(E/(2pi)) -- linear, erro de 2a ordem
    ~ offset^2 / (4 pi base) desprezivel (ver justificativa no REVIEW.md)."""
    density = (1 / (2 * np.pi)) * np.log(base / (2 * np.pi))
    return offsets * density, density


def empirical_number_variance(x, L_grid, min_windows=30):
    """V(L) empirico: janelas deslizantes de comprimento L (passo L/4),
    conta de pontos por janela, variancia dessa contagem sobre as janelas.
    Retorna None para L onde ha menos que min_windows janelas disponiveis
    (dado insuficiente -- nao inventa numero)."""
    x = np.sort(x)
    xmin, xmax = x[0], x[-1]
    out = {}
    for L in L_grid:
        stride = L / 4.0
        starts = np.arange(xmin, xmax - L, stride)
        if len(starts) < min_windows:
            out[float(L)] = None
            continue
        lo_idx = np.searchsorted(x, starts, side="left")
        hi_idx = np.searchsorted(x, starts + L, side="left")
        counts = hi_idx - lo_idx
        out[float(L)] = {
            "n_windows": int(len(starts)),
            "mean_count": float(np.mean(counts)),
            "expected_count": float(L),
            "variance": float(np.var(counts)),
        }
    return out


def model_a_berry_universal(L):
    """Eq. 1.19 (1o colchete) / Conjectura 1.4.1(a) de arXiv:2211.14918 --
    formula fechada de Berry que COINCIDE com a variancia de autovalores
    GUE no regime universal. Esta e a extrapolacao "so GUE" (Modelo A,
    concorrente nomeado) quando avaliada tambem fora do regime universal."""
    x = 2 * np.pi * L
    si, ci = sici(x)
    bracket = np.log(x) - ci - x * si + np.pi**2 * L - np.cos(x) + 1 + GAMMA0
    return bracket / np.pi**2


def model_b_berry_nonuniversal_exact(delta_grid, T, primes_cache):
    """Conjectura 1.4.1(b) / agora Corolario 1.4.3 (teorema condicional a
    RH + Chan 2004) de arXiv:2211.14918 -- soma EXATA sobre potencias de
    primos n=p^k <= T. So viavel exatamente quando T e pequeno o bastante
    para enumerar todos os primos <= T (aqui: zeros1, T~75000)."""
    logT = np.log(T)
    ns, logns, Lambda2 = primes_cache
    out = {}
    for delta in delta_grid:
        cos_term = np.cos(2 * np.pi * delta * logns / logT)
        s = np.sum((Lambda2 / (ns * logns**2)) * (1 - cos_term))
        out[float(delta)] = float((s + 1) / np.pi**2)
    return out


def model_b_truncated(delta_grid, T, P_cutoff, note_key):
    """Versao TRUNCADA de 1.4.1(b): soma so sobre potencias de primos
    n=p^k <= P_cutoff << T (nao ate T, inviavel para T~1e11/1e20). Reporta
    explicitamente como sub-estimativa -- NAO um valor do modelo real."""
    from sympy import primerange

    ns_list = []
    Lambda2_list = []
    for p in primerange(2, P_cutoff):
        k = 1
        pk = p
        while pk <= P_cutoff:
            ns_list.append(pk)
            Lambda2_list.append(np.log(p) ** 2)
            k += 1
            pk *= p
    ns = np.array(ns_list, dtype=float)
    Lambda2 = np.array(Lambda2_list, dtype=float)
    logns = np.log(ns)
    logT = np.log(T)
    out = {}
    for delta in delta_grid:
        cos_term = np.cos(2 * np.pi * delta * logns / logT)
        s = np.sum((Lambda2 / (ns * logns**2)) * (1 - cos_term))
        out[float(delta)] = float((s + 1) / np.pi**2)
    # estimativa de fracao capturada da soma "+1" divergente lenta:
    # Sum_{p<=P} 1/p ~ loglog P + M (Mertens); Sum_{p<=T} 1/p ~ loglog T + M
    M = 0.2614972128
    captured_vs_full_k1_sum = (np.log(np.log(P_cutoff)) + M) / (np.log(np.log(T)) + M)
    return out, {"P_cutoff": P_cutoff, "estimated_fraction_of_k1_prime_sum_captured": float(captured_vs_full_k1_sum), "note": note_key}


def build_prime_power_cache(T_int):
    from sympy import primerange
    ns_list, Lambda2_list = [], []
    for p in primerange(2, T_int + 1):
        k, pk = 1, p
        while pk <= T_int:
            ns_list.append(pk)
            Lambda2_list.append(np.log(p) ** 2)
            k += 1
            pk *= p
    ns = np.array(ns_list, dtype=float)
    return ns, np.log(ns), np.array(Lambda2_list, dtype=float)


def main():
    result = {"evidence_level": "exploratory_only", "note": "PILOT de viabilidade, nao pre-registro. Ver REVIEW.md."}

    # ---- zeros1: T pequeno, Modelo B exato viavel ----
    g1 = load_zeros1()
    x1 = renormalize_absolute(g1)
    T1 = float(g1[-1])
    L_grid_1 = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
    emp1 = empirical_number_variance(x1, L_grid_1)
    modelA_1 = {str(L): model_a_berry_universal(L) for L in L_grid_1}
    primes_cache_1 = build_prime_power_cache(int(np.ceil(T1)))
    modelB_1 = model_b_berry_nonuniversal_exact(L_grid_1, T1, primes_cache_1)
    logT1 = np.log(T1)
    result["zeros1"] = {
        "n_zeros": len(g1), "T_max": T1, "logT": float(logT1),
        "universal_regime_L_upper_bound_o(logT)": float(logT1),
        "empirical": emp1, "model_A_berry_universal": modelA_1,
        "model_B_berry_nonuniversal_EXACT": modelB_1,
        "n_prime_powers_used_model_B": int(len(primes_cache_1[0])),
    }
    print(f"[zeros1] T={T1:.1f} logT={logT1:.3f} n_zeros={len(g1)}")
    for L in L_grid_1:
        e = emp1[str(L)] if str(L) in emp1 else emp1[float(L)]
        e = emp1[float(L)]
        a = modelA_1[str(L)]
        b = modelB_1[float(L)]
        if e is None:
            print(f"  L={L:6.0f}: dado insuficiente (poucas janelas)")
        else:
            print(f"  L={L:6.0f}: V_emp={e['variance']:8.4f}  A(GUE)={a:8.4f}  B(Berry+primos)={b:8.4f}  (delta_emp-A={e['variance']-a:+.4f})")

    # ---- zeros3: T~2.68e11, Modelo B so truncado ----
    off3, base3 = load_offset_file(DATA_DIR / "zeros3.txt", 267653395647.0, 10000)
    x3, density3 = renormalize_local(off3, base3)
    T3 = base3
    logT3 = np.log(T3)
    L_grid_3 = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 1500]
    emp3 = empirical_number_variance(x3, L_grid_3, min_windows=10)
    modelA_3 = {str(L): model_a_berry_universal(L) for L in L_grid_3}
    modelB_3, modelB_3_meta = model_b_truncated(L_grid_3, T3, P_cutoff=10_000_000, note_key="zeros3_truncated_1e7")
    result["zeros3"] = {
        "n_zeros": len(off3), "base": base3, "T_effective": T3, "logT": float(logT3),
        "local_density": float(density3),
        "empirical": emp3, "model_A_berry_universal": modelA_3,
        "model_B_berry_nonuniversal_TRUNCATED": modelB_3, "model_B_truncation_meta": modelB_3_meta,
    }
    print(f"\n[zeros3] T~{T3:.3e} logT={logT3:.3f} n_zeros={len(off3)} (Modelo B truncado, primos<=1e7, fracao estimada da soma k=1 capturada: {modelB_3_meta['estimated_fraction_of_k1_prime_sum_captured']:.3f})")
    for L in L_grid_3:
        e = emp3[float(L)]
        a = modelA_3[str(L)]
        b = modelB_3[float(L)]
        if e is None:
            print(f"  L={L:6.0f}: dado insuficiente (poucas janelas)")
        else:
            print(f"  L={L:6.0f}: V_emp={e['variance']:8.4f}  A(GUE)={a:8.4f}  B(trunc)={b:8.4f}  (delta_emp-A={e['variance']-a:+.4f})")

    # ---- zeros4: T~1.44e20, Modelo B so truncado ----
    off4, base4 = load_offset_file(DATA_DIR / "zeros4.txt", 144176897509546973000.0, 10000)
    x4, density4 = renormalize_local(off4, base4)
    T4 = base4
    logT4 = np.log(T4)
    L_grid_4 = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 1500]
    emp4 = empirical_number_variance(x4, L_grid_4, min_windows=10)
    modelA_4 = {str(L): model_a_berry_universal(L) for L in L_grid_4}
    modelB_4, modelB_4_meta = model_b_truncated(L_grid_4, T4, P_cutoff=10_000_000, note_key="zeros4_truncated_1e7")
    result["zeros4"] = {
        "n_zeros": len(off4), "base": base4, "T_effective": T4, "logT": float(logT4),
        "local_density": float(density4),
        "empirical": emp4, "model_A_berry_universal": modelA_4,
        "model_B_berry_nonuniversal_TRUNCATED": modelB_4, "model_B_truncation_meta": modelB_4_meta,
    }
    print(f"\n[zeros4] T~{T4:.3e} logT={logT4:.3f} n_zeros={len(off4)} (Modelo B truncado, primos<=1e7, fracao estimada da soma k=1 capturada: {modelB_4_meta['estimated_fraction_of_k1_prime_sum_captured']:.3f})")
    for L in L_grid_4:
        e = emp4[float(L)]
        a = modelA_4[str(L)]
        b = modelB_4[float(L)]
        if e is None:
            print(f"  L={L:6.0f}: dado insuficiente (poucas janelas)")
        else:
            print(f"  L={L:6.0f}: V_emp={e['variance']:8.4f}  A(GUE)={a:8.4f}  B(trunc)={b:8.4f}  (delta_emp-A={e['variance']-a:+.4f})")

    out_path = HERE / "item12_number_variance_pilot_result.json"
    json.dump(result, open(out_path, "w"), indent=2)
    print(f"\n[fim] Resultado salvo em {out_path}")


if __name__ == "__main__":
    main()
