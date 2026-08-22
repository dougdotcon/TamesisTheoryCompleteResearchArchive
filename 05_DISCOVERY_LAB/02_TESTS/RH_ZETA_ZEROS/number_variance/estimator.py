"""
DISC-RH-NUMBER-VARIANCE-001 -- biblioteca compartilhada do estimador.

Escrito do zero para este sub-teste (nao e copia do piloto
untried_items_review/item12_number_variance_pilot.py, mas reusa e cita
a mesma fonte primaria -- Lugar, Milinovich & Quesada-Herrera 2022,
arXiv:2211.14918 -- verificada por fetch direto do PDF nesta sessao,
paginas 1-10, nao de memoria).

Formulas verificadas por fetch (nao citadas de memoria):
- N(E) = E/(2pi)*(log(E/(2pi))-1) + 7/8  -- termo principal de
  Riemann-von Mangoldt, eq. (1.1) do paper acima (via Titchmarsh Ch.9).
- V(L;x) = (1/Dx) * integral_{x-Dx/2}^{x+Dx/2} [n(L;y)-L]^2 dy --
  definicao EXATA de Berry (secao 1.4 do paper, paragrafo antes da
  Conjectura 1.4.1), com n(L;y) = numero de zeros renormalizados no
  intervalo [y-L/2, y+L/2].
- Modelo A (regime universal, Conjectura 1.4.1(a), Berry 1988 Eq. (19)
  citada la): V(L;x) ~ (1/pi^2)[log(2piL) - Ci(2piL) - 2piL*Si(2piL)
  + pi^2*L - cos(2piL) + 1 + gamma_0], que o proprio paper diz
  coincidir EXATAMENTE com a variancia do numero de autovalores GUE.
- Modelo B (regime nao-universal, Conjectura 1.4.1(b), agora Corolario
  1.4.3 -- teorema condicional a RH + Conjectura de Chan 2004, valido
  para delta = o(log^{4/3} T)):
  V(L;x) ~ (1/pi^2)[ sum_{n<=T} (Lambda(n)^2/(n*log^2 n))*(1-cos(2pi*L*log(n)/log(T))) + 1 ]
  onde a soma e sobre potencias de primos n=p^k<=T (Lambda(n)=log p se
  n=p^k, 0 caso contrario). Usa-se a identidade algebrica exata (
  derivada e verificada nesta sessao, nao citada):
      Lambda(p^k)^2 / (p^k * log^2(p^k)) = (log p)^2 / (p^k * k^2 * (log p)^2)
                                          = 1 / (k^2 * p^k)
  que simplifica a soma para sum_{p^k<=T} (1/(k^2 p^k)) * (1-cos(theta_{p,k}))
  com theta_{p,k} = 2*pi*L*k*log(p)/log(T).

Sem dado fabricado. Falha de leitura de arquivo e erro fatal.
"""
from __future__ import annotations

import numpy as np
from scipy.special import sici

GAMMA0 = 0.5772156649015329  # Euler-Mascheroni

# ---------------------------------------------------------------------------
# Renormalizacao (Riemann-von Mangoldt, termo principal N(E))
# ---------------------------------------------------------------------------

def N_absolute(E):
    """N(E) = E/(2pi)*(log(E/(2pi))-1) + 7/8 -- formula EXATA (nao
    linearizada). Segura em float64 quando E nao e astronomicamente
    grande (usada so para zeros1, E <= ~75000)."""
    return E / (2 * np.pi) * (np.log(E / (2 * np.pi)) - 1) + 7 / 8


def local_density(base):
    """N'(E) = (1/2pi) log(E/2pi) -- densidade local (derivada exata de
    N_absolute), avaliada na altura-base do dataset."""
    return (1 / (2 * np.pi)) * np.log(base / (2 * np.pi))


def renormalize_local(offsets, base):
    """Linearizacao de N em torno de `base` para offsets << base
    (zeros3, zeros4): x_m = offset_m * N'(base).

    Erro de 2a ordem (derivado e verificado nesta sessao, Taylor de
    N em torno de `base`):
        N(base+off) = N(base) + N'(base)*off + (1/2)*N''(base)*off^2 + O(off^3/base^2)
    com N''(E) = 1/(2*pi*E) (derivada direta de N'(E) acima). Logo o
    erro absoluto de 2a ordem por ponto e:
        err2(off, base) = off^2 / (4*pi*base)
    (constante aditiva N(base) cancela quando comparamos POSICOES
    relativas / contagens em janela -- so a curvatura entra no erro de
    espacamento local)."""
    density = local_density(base)
    x = offsets * density
    max_offset = float(np.max(np.abs(offsets - offsets[0]))) if len(offsets) else 0.0
    err2_bound = (max_offset ** 2) / (4 * np.pi * base)
    return x, density, err2_bound


# ---------------------------------------------------------------------------
# Estimador EXATO de V(L;x) por integracao de funcao escada (piecewise
# constant), sem stride/discretizacao ad hoc.
# ---------------------------------------------------------------------------

def _exact_window_integral(x_sorted, y_lo, y_hi, L):
    """Integral EXATA de [n(L;y)-L]^2 dy para y em [y_lo, y_hi], onde
    n(L;y) = numero de pontos de x_sorted em [y-L/2, y+L/2].

    n(L;y) e uma funcao em escada de y com saltos:
      +1 em y = x_m - L/2  (ponto x_m entra pela borda direita)
      -1 em y = x_m + L/2  (ponto x_m sai pela borda esquerda)
    Os pontos de quebra sao exatamente esses, restritos a [y_lo, y_hi].
    Integracao exata: soma de (valor^2 * comprimento_do_trecho) sobre
    os trechos entre quebras consecutivas.

    x_sorted deve conter TODOS os pontos que podem afetar a janela em
    algum y do intervalo [y_lo,y_hi], ou seja x em
    [y_lo - L/2 - eps, y_hi + L/2 + eps] no minimo -- responsabilidade
    do chamador (aqui: sempre passamos o array completo do bloco).
    """
    if y_hi <= y_lo:
        return 0.0, 0.0
    # pontos de quebra dentro do intervalo de integracao
    breaks_up = x_sorted - L / 2.0   # +1 events
    breaks_dn = x_sorted + L / 2.0   # -1 events
    mask_up = (breaks_up > y_lo) & (breaks_up < y_hi)
    mask_dn = (breaks_dn > y_lo) & (breaks_dn < y_hi)
    bpts = np.concatenate([breaks_up[mask_up], breaks_dn[mask_dn]])
    deltas = np.concatenate([np.ones(mask_up.sum()), -np.ones(mask_dn.sum())])
    order = np.argsort(bpts, kind="mergesort")
    bpts = bpts[order]
    deltas = deltas[order]

    # valor de n(L;y) para y INFINITESIMALMENTE ACIMA de y_lo (nao em
    # y_lo em si): x_m ja "entrou" sse x_m-L/2<=y_lo (<=, consistente
    # com mask_up usar "breaks_up>y_lo" para eventos PENDENTES) e
    # ainda NAO "saiu" sse x_m+L/2>y_lo (>, estrito, consistente com
    # mask_dn usar "breaks_dn>y_lo" para saidas pendentes -- uma saida
    # EXATAMENTE em y_lo ja aconteceu e nao deve ser contada). Ou
    # seja: x_m em (y_lo-L/2, y_lo+L/2]. BUG anterior (corrigido nesta
    # sessao, ver validation_gue_run1_FAILED.log): usava side="left"
    # no limite inferior, incluindo por engano x_m EXATAMENTE em
    # y_lo-L/2 (que deveria ja ter saido) e nunca processava o evento
    # de saida correspondente (excluido do mask por ser <= y_lo), o
    # que inflava n(L;y) em +1 permanentemente a partir dai.
    n0 = int(np.searchsorted(x_sorted, y_lo + L / 2.0, side="right") -
              np.searchsorted(x_sorted, y_lo - L / 2.0, side="right"))

    grid = np.concatenate([[y_lo], bpts, [y_hi]])
    vals = np.empty(len(grid) - 1)
    vals[0] = n0
    cur = n0
    for i, d in enumerate(deltas):
        cur += d
        vals[i + 1] = cur
    widths = np.diff(grid)
    sq = (vals - L) ** 2
    integral = float(np.sum(sq * widths))
    return integral, float(y_hi - y_lo)


def block_number_variance(x_sorted, block_edges, L, min_block_width_factor=3.0):
    """V_hat(L), SE(L) via blocos NAO sobrepostos.

    block_edges: array de bordas [a_0, a_1, ..., a_B] definindo B
    blocos [a_i, a_{i+1}]. Em cada bloco, a janela deslizante y varia
    apenas na sub-regiao INTERIOR [a_i+L/2, a_{i+1}-L/2] (evita efeito
    de borda -- nao inventa dado fora do range observado). Blocos com
    largura < min_block_width_factor*L sao descartados (dado
    insuficiente para esse L, nao um zero forcado).

    Retorna dict com per_block (lista), V_hat, SE, n_blocks_used,
    n_blocks_dropped.
    """
    per_block = []
    for i in range(len(block_edges) - 1):
        a, b = block_edges[i], block_edges[i + 1]
        width = b - a
        if width < min_block_width_factor * L:
            continue
        y_lo, y_hi = a + L / 2.0, b - L / 2.0
        # fatia so os pontos que podem afetar este bloco (evita
        # varrer o array inteiro a cada bloco -- essencial para B
        # grande sobre datasets grandes; ver
        # validation_estimator_bruteforce_run1_FAILED.log / nota de
        # performance no PREREGISTRATION.md)
        lo_idx = np.searchsorted(x_sorted, a - L, side="left")
        hi_idx = np.searchsorted(x_sorted, b + L, side="right")
        x_slice = x_sorted[lo_idx:hi_idx]
        integral, span = _exact_window_integral(x_slice, y_lo, y_hi, L)
        if span <= 0:
            continue
        per_block.append(integral / span)
    per_block = np.array(per_block)
    n_used = len(per_block)
    n_dropped = (len(block_edges) - 1) - n_used
    if n_used == 0:
        return {"V_hat": None, "SE": None, "n_blocks_used": 0,
                "n_blocks_dropped": n_dropped, "per_block": []}
    V_hat = float(np.mean(per_block))
    SE = float(np.std(per_block, ddof=1) / np.sqrt(n_used)) if n_used > 1 else float("nan")
    return {"V_hat": V_hat, "SE": SE, "n_blocks_used": n_used,
            "n_blocks_dropped": n_dropped, "per_block": per_block.tolist()}


# ---------------------------------------------------------------------------
# Modelo A -- regime universal de Berry (== variancia GUE), Conjectura
# 1.4.1(a), formula fechada.
# ---------------------------------------------------------------------------

def model_A(L):
    """Fechada, exata (via scipy.special.sici), avaliavel para
    qualquer L>0. Extrapolacao ingenua ("Modelo A") quando usada fora
    do regime universal L=o(log T)."""
    L = np.asarray(L, dtype=float)
    x = 2 * np.pi * L
    si, ci = sici(x)
    bracket = np.log(x) - ci - x * si + np.pi ** 2 * L - np.cos(x) + 1 + GAMMA0
    return bracket / np.pi ** 2


# ---------------------------------------------------------------------------
# Modelo B -- regime nao-universal, Conjectura 1.4.1(b) / Corolario
# 1.4.3. Soma exata sobre potencias de primos p^k<=T.
# ---------------------------------------------------------------------------

def sieve_primes(n_max):
    """Crivo de Eratostenes vetorizado (numpy), rapido ate ~1e9.
    Retorna array de primos (float64) <= n_max."""
    n_max = int(n_max)
    is_p = np.ones(n_max + 1, dtype=bool)
    is_p[:2] = False
    for i in range(2, int(n_max ** 0.5) + 1):
        if is_p[i]:
            is_p[i * i:: i] = False
    return np.nonzero(is_p)[0].astype(np.float64)


def prime_power_terms(p_array, T_cutoff):
    """Para um array de primos `p_array` (todos <= T_cutoff), gera
    TODAS as potencias p^k <= T_cutoff com peso 1/(k^2 p^k) e
    log(p^k)=k*log(p). Vetorizado por k (nao por primo -- essencial
    para p_array com dezenas de milhoes de elementos): para cada
    k=1,2,...,K_max (K_max = floor(log(T_cutoff)/log(2)), o maior k
    possivel usando o menor primo=2), filtra os primos com p^k<=T_cutoff
    e computa o termo vetorialmente. Retorna (pk, logpk, weight) como
    arrays concatenados (uniao sobre k)."""
    if len(p_array) == 0:
        return (np.array([]), np.array([]), np.array([]))
    K_max = int(np.floor(np.log(T_cutoff) / np.log(2.0))) if T_cutoff >= 2 else 1
    pk_parts, logpk_parts, w_parts = [], [], []
    for k in range(1, K_max + 1):
        # p^k <= T_cutoff  <=>  p <= T_cutoff^(1/k)
        p_max_k = T_cutoff ** (1.0 / k)
        sel = p_array[p_array <= p_max_k]
        if len(sel) == 0:
            break
        pk = sel ** k
        logp = np.log(sel)
        pk_parts.append(pk)
        logpk_parts.append(k * logp)
        w_parts.append(1.0 / (k * k * pk))
    return (np.concatenate(pk_parts), np.concatenate(logpk_parts), np.concatenate(w_parts))


def model_B_exact(L_array, T, pk, logpk, weight):
    """Soma EXATA (sem truncagem) -- viavel quando TODAS as potencias
    de primos <= T foram enumeradas (T pequeno, zeros1)."""
    logT = np.log(T)
    out = np.empty(len(L_array))
    for i, L in enumerate(L_array):
        theta = 2 * np.pi * L * logpk / logT
        s = np.sum(weight * (1 - np.cos(theta)))
        out[i] = (s + 1) / np.pi ** 2
    return out


MERTENS_M = 0.2614972128476427837554268386086958590516  # constante de Meissel-Mertens


def mertens_error_bound(x):
    """Cota de erro EXPLICITA e classica de Mertens (1874) para
    |sum_{p<=x} 1/p - loglog(x) - M| <= 4/log(x+1) + 2/(x log x),
    valida para todo x>=2 (verificada por fetch em
    en.wikipedia.org/wiki/Mertens%27_theorems nesta sessao, citando o
    resultado original de F. Mertens, "Ein Beitrag zur analytischen
    Zahlentheorie", J. Reine Angew. Math. 78 (1874), 46-62 -- cota mais
    fraca mas mais simples/segura que refinamentos posteriores de
    Rosser-Schoenfeld 1962, que exigiriam verificar constantes que nao
    puderam ser confirmadas por fetch direto nesta sessao [tentativa
    falhou, HTTP 503] -- por isso NAO usadas)."""
    x = float(x)
    if x < 2:
        raise ValueError("cota de Mertens exige x>=2")
    return 4.0 / np.log(x + 1) + 2.0 / (x * np.log(x))


def sum_1_over_p_bound(x_lo, x_hi):
    """Cota RIGOROSA (nao heuristica) para sum_{x_lo < p <= x_hi} 1/p,
    via Mertens (1874): a soma verdadeira esta em
    [loglog(x_hi)-loglog(x_lo) - eb_hi - eb_lo,
     loglog(x_hi)-loglog(x_lo) + eb_hi + eb_lo]
    onde eb_* = mertens_error_bound(x_*)."""
    if x_lo < 2:
        x_lo = 2.0
    eb_lo = mertens_error_bound(x_lo)
    eb_hi = mertens_error_bound(x_hi)
    center = np.log(np.log(x_hi)) - np.log(np.log(x_lo))
    margin = eb_lo + eb_hi
    return center - margin, center + margin


def model_B_bounded(L_array, T, pk_cut, logpk_cut, weight_cut, P_cutoff,
                     k_ge2_tail_upper):
    """Modelo B como INTERVALO RIGOROSO [lower, upper] quando so e
    viavel enumerar potencias de primos ate P_cutoff << T.

    - Termo computado exatamente: soma sobre p^k <= P_cutoff (pk_cut
      etc, gerados por prime_power_terms).
    - Cauda k=1 (P_cutoff < p <= T): cada termo peso 1/p, fator
      (1-cos(theta)) em [0,2] -- cota bilateral
      0 <= tail_k1 <= 2 * sum_1_over_p_bound(...)_upper (usa so o lado
      superior da cota de Mertens porque queremos so um envelope
      [computado, computado+cota_max], nunca subtraimos nada nao
      calculado).
    - Cauda k>=2 (potencias de primos > P_cutoff, k>=2): fornecida
      pelo chamador como cota numerica pre-computada
      (k_ge2_tail_upper), tipicamente despicivel (ver
      bound_k_ge2_tail_beyond).

    Retorna (lower_array, upper_array), ambos em unidades de V(L)
    (already divided by pi^2, +1 incluido)."""
    logT = np.log(T)
    tail_center, tail_margin = sum_1_over_p_bound(P_cutoff, T)
    tail_k1_upper = 2.0 * max(tail_center + tail_margin, 0.0)
    # tail_k1_lower = 0 (nao subtraimos: 1-cos(theta)>=0 sempre, entao
    # a cauda so pode ADICIONAR ao computado, nunca diminuir -- por
    # isso lower = computado exatamente, upper = computado + cota max)
    extra_upper = tail_k1_upper + k_ge2_tail_upper

    lowers = np.empty(len(L_array))
    uppers = np.empty(len(L_array))
    for i, L in enumerate(L_array):
        theta = 2 * np.pi * L * logpk_cut / logT
        s = np.sum(weight_cut * (1 - np.cos(theta)))
        lowers[i] = (s + 1) / np.pi ** 2
        uppers[i] = (s + extra_upper + 1) / np.pi ** 2
    return lowers, uppers


def bound_k_ge2_tail_beyond(P_cutoff, T):
    """Cota RIGOROSA e AUTOCONTIDA (sem citar constante externa) para
    sum_{p>P_cutoff, k>=2, p^k<=T} 1/(k^2 p^k).

    Para p fixo, sum_{k>=2} 1/(k^2 p^k) <= sum_{k>=2} 1/p^k = 1/(p(p-1))
    (serie geometrica, cota grosseira via k^2>=1). Somando sobre TODOS
    os primos p>P_cutoff (superconjunto do que realmente aparece, ja
    que exige so p^2<=T, cota ainda mais frouxa mas valida):
        sum_{p>P_cutoff} 1/(p(p-1)) <= sum_{n>P_cutoff} 1/(n(n-1))
                                      = 1/P_cutoff   (telescopica exata)
    (majora primos por todos os inteiros > P_cutoff -- cota valida
    porque 1/(n(n-1))>0 para todo n>=2, entao restringir a primos so
    pode diminuir a soma real, nunca aumentar; a cota por todos os
    inteiros e portanto um majorante seguro)."""
    if P_cutoff < 2:
        raise ValueError("P_cutoff>=2 exigido")
    return 1.0 / P_cutoff
