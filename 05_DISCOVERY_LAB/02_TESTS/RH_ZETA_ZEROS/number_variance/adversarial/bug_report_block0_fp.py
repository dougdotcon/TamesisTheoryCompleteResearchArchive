"""
BUG (terceiro, encontrado nesta reproducao adversarial): coincidencia de
fronteira ponto-flutuante em estimator.py::_exact_window_integral, bloco 0
(o bloco cuja borda inferior `a` coincide EXATAMENTE, bit a bit, com o menor
dado do dataset -- sempre o caso, pois block_edges = np.linspace(x_min, x_max,
B+1) faz edges[0]=x_min por construcao).

CAUSA RAIZ: block_number_variance (estimator.py) computa
    y_lo = a + L/2.0
e passa y_lo para _exact_window_integral, que la dentro recomputa
    n0 = count(x <= y_lo + L/2) - count(x <= y_lo - L/2)
Ou seja, o codigo tenta recuperar `a` fazendo `(a + L/2) - L/2`. Em ponto
flutuante IEEE754 isso NAO devolve `a` exatamente em geral (erro de
arredondamento de ~1 ULP). Quando esse erro faz `(y_lo - L/2)` cair
LIGEIRAMENTE ABAIXO do valor real de `a` (ao inves de igual ou acima), o
ponto x_min (que e exatamente `a`) passa a ser contado como "<= y_lo - L/2"
mesmo sem realmente sê-lo pela definicao do problema -- na pratica, o efeito
liquido e que x_min fica erroneamente INCLUIDO em n0 quando deveria estar
EXCLUIDO (ele "sai" da janela exatamente no instante y=y_lo, entao para
y>y_lo, infinitesimalmente, ele nao deveria mais contar). Isso infla n(L;y)
em +1 permanentemente ATRAVES DE TODO O BLOCO (nenhum evento compensador
"-1" aparece na lista de eventos, porque a saida desse ponto especifico
acontece EXATAMENTE em y_lo, fora do dominio de integracao aberto (y_lo,y_hi)
usado pelo resto do algoritmo).

A direcao do erro de arredondamento (se cai acima ou abaixo do valor exato)
depende dos bits especificos de `a` e `L` -- efetivamente um "cara ou coroa"
determinístico mas imprevisivel a priori. Por isso o bug aparece em ALGUNS
pontos da grade e nao em outros (15 de 23 no total, incluindo o ponto
decisivo primario de zeros3 mas NAO o de zeros1).

Este script reproduz o bug de forma MINIMA e autocontida, sem depender de
nenhum dado real, e mostra a correcao (evitar o round-trip: usar `a - L/2`
diretamente ao inves de `(a+L/2) - L/2`).
"""
import numpy as np
import sys

sys.path.insert(0, "..")
from estimator import _exact_window_integral  # so leitura/diagnostico, nao copia de logica nova

# Constroi um caso minimo onde a coincidencia acontece por construcao:
# um ponto EXATAMENTE em a, mais uma rede regular ao redor, e um L cujo
# arredondamento (a+L/2)-L/2 < a (mesma direcao do caso real zeros3).
rng = np.random.default_rng(0)

found_example = None
for trial in range(200000):
    a = rng.uniform(1.0, 1000.0)
    L = rng.uniform(1.0, 500.0)
    y_lo = a + L / 2.0
    recovered = y_lo - L / 2.0
    if recovered < a:
        found_example = (a, L, recovered, recovered - a)
        break

a, L, recovered, err = found_example
print(f"Exemplo minimo: a={a!r}  L={L!r}")
print(f"  (a + L/2) - L/2 = {recovered!r}  (deveria ser == a)")
print(f"  erro = {err:.3e} (ULP-scale, negativo)")

# monta um dataset sintetico: ponto EXATAMENTE em `a`, mais uma rede regular
# de espacamento 1 acima dele, cobrindo alguns L de largura.
N = 2000
x = a + np.arange(N, dtype=np.float64) * 1.0  # x[0] == a exatamente

y_lo = a + L / 2.0
y_hi = a + 400.0  # janela de integracao qualquer, bem maior que L

# metodo do primario (com o round-trip que causa o bug)
integral_bug, span = _exact_window_integral(x, y_lo, y_hi, L)
V_bug = integral_bug / span

# metodo CORRIGIDO: usar `a` diretamente em vez de recompor via y_lo - L/2.
def exact_window_integral_fixed(x_sorted, a_direct, y_lo, y_hi, L):
    breaks_up = x_sorted - L / 2.0
    breaks_dn = x_sorted + L / 2.0
    mask_up = (breaks_up > y_lo) & (breaks_up < y_hi)
    mask_dn = (breaks_dn > y_lo) & (breaks_dn < y_hi)
    bpts = np.concatenate([breaks_up[mask_up], breaks_dn[mask_dn]])
    deltas = np.concatenate([np.ones(mask_up.sum()), -np.ones(mask_dn.sum())])
    order = np.argsort(bpts, kind="mergesort")
    bpts, deltas = bpts[order], deltas[order]
    # CORRECAO: usa a_direct (o valor original do bloco), nao y_lo - L/2
    n0 = int(np.searchsorted(x_sorted, a_direct + L, side="right") -
              np.searchsorted(x_sorted, a_direct, side="right"))
    grid = np.concatenate([[y_lo], bpts, [y_hi]])
    vals = np.empty(len(grid) - 1)
    vals[0] = n0
    cur = n0
    for i, d in enumerate(deltas):
        cur += d
        vals[i + 1] = cur
    widths = np.diff(grid)
    integral = float(np.sum((vals - L) ** 2 * widths))
    return integral, float(y_hi - y_lo)


integral_fixed, span2 = exact_window_integral_fixed(x, a, y_lo, y_hi, L)
V_fixed = integral_fixed / span2

# ground truth: contagem literal (fechada) numa grade ultrafina
n_steps = 4_000_000
ys = np.linspace(y_lo, y_hi, n_steps)
lo_idx = np.searchsorted(x, ys - L / 2, side="left")
hi_idx = np.searchsorted(x, ys + L / 2, side="right")
counts = hi_idx - lo_idx
V_bruteforce = float(np.sum((counts - L) ** 2)) * (y_hi - y_lo) / n_steps / (y_hi - y_lo)

print(f"\nV (metodo do primario, com bug)     = {V_bug:.6f}")
print(f"V (metodo corrigido, sem round-trip) = {V_fixed:.6f}")
print(f"V (brute-force, grade ultrafina)     = {V_bruteforce:.6f}")
print(f"\nDiferenca bug vs correto: {V_bug - V_fixed:+.6f} "
      f"({'BUG CONFIRMADO' if abs(V_bug - V_fixed) > 1e-6 else 'sem diferenca detectavel'})")

import json
with open("bug_report_block0_fp.json", "w") as f:
    json.dump(dict(a=a, L=L, recovered=recovered, err=err,
                     V_bug=V_bug, V_fixed=V_fixed, V_bruteforce=V_bruteforce,
                     diff=V_bug - V_fixed), f, indent=2)
