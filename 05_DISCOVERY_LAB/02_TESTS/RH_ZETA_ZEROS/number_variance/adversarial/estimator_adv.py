"""
Estimador adversarial de V(L;x), construido do zero SOMENTE a partir da
definicao matematica no PREREGISTRATION.md / DESIGN.json (nao copiado de
estimator.py do primario, que nao foi lido antes deste arquivo estar pronto).

Definicoes (Secao 1.1 do pre-registro, identicas ao paper arXiv:2211.14918,
Sec 1.4, verificado por fetch direto nesta sessao):

  N(E) := E/(2*pi) * (log(E/(2*pi)) - 1) + 7/8      (Riemann-von Mangoldt)
  x_m := N(gamma_m)                                  (zero renormalizado)
  n(L;y) := # de x_m em [y-L/2, y+L/2]                (funcao em escada de y)
  V(L;x) := (1/dx) * integral_{x-dx/2}^{x+dx/2} [n(L;y)-L]^2 dy

Esquema de blocos (Secao 2 do pre-registro):
  - range observado particionado em B blocos de largura uniforme via
    np.linspace(x_min, x_max, B+1)
  - dentro do bloco [a,b], y varia so no interior [a+L/2, b-L/2]
  - blocos com largura < 3L descartados
  - V_hat(L) = media dos V_i (um por bloco)
  - SE(L) = desvio padrao entre blocos (ddof=1) / sqrt(B)
"""
import numpy as np


def N_riemann_von_mangoldt(E):
    """N(E) = E/(2pi)*(log(E/2pi)-1) + 7/8, formula exata (eq 1.1 do paper,
    a parte principal, sem o termo S(E))."""
    E = np.asarray(E, dtype=np.float64)
    return E / (2.0 * np.pi) * (np.log(E / (2.0 * np.pi)) - 1.0) + 7.0 / 8.0


def N_prime(E):
    """N'(E) = (1/2pi) * log(E/2pi) -- densidade local, usada para
    linearizacao local em datasets de offset (zeros3/zeros4)."""
    return np.log(E / (2.0 * np.pi)) / (2.0 * np.pi)


def _exact_window_integral_single_block(x_sorted, a, b, L):
    """
    Computa exatamente:
        integral_{a}^{b} [n(L;y) - L]^2 dy
    onde n(L;y) = numero de pontos de x_sorted em [y-L/2, y+L/2],
    y variando em [a,b] (a=block_lo+L/2, b=block_hi-L/2, o interior).

    x_sorted: array ordenado de todas as posicoes renormalizadas (pode conter
    pontos fora de [a-L/2-eps, b+L/2+eps]; filtramos por indice).

    Metodo: n(L;y) e uma funcao em escada com saltos em:
      - y = x_m - L/2 : n aumenta em 1 (o ponto x_m entra pela direita)
      - y = x_m + L/2 : n diminui em 1 (o ponto x_m sai pela esquerda)
    Reunimos todos os eventos de quebra que caem estritamente dentro de
    (a,b), ordenamos, e calculamos n(L;y) constante entre quebras
    consecutivas (incluindo os extremos a e b), integrando [n-L]^2 * largura
    exatamente por trecho.
    """
    if b <= a:
        return 0.0, 0.0

    # n(L; a) = numero de x_m com x_m - L/2 <= a < x_m + L/2
    #         = numero de x_m em (a - L/2, a + L/2]... mas para consistencia
    # de fronteira usamos convencao unica: um ponto x_m contribui ao
    # intervalo [x_m - L/2, x_m + L/2) (janela fechada a esquerda, aberta a
    # direita) -- convencao arbitraria mas CONSISTENTE, aplicada em todo
    # lugar (evento de entrada em y=x_m-L/2 inclusive, saida em y=x_m+L/2
    # exclusive). Isso evita contagem dupla/omissao em coincidencias exatas.
    lo = np.searchsorted(x_sorted, a - L / 2.0, side="right")
    hi = np.searchsorted(x_sorted, a + L / 2.0, side="right")
    n0 = hi - lo  # numero de x_m com x_m - L/2 <= a  AND  x_m + L/2 > a
    # (x_m - L/2 <= a  <=>  x_m <= a+L/2 ; x_m + L/2 > a <=> x_m > a - L/2)

    # eventos dentro de (a,b): entradas (x_m - L/2, +1) para x_m em (a+L/2, b+L/2]
    #                          saidas   (x_m + L/2, -1) para x_m em (a-L/2, b-L/2]
    # restrito a evento estritamente dentro de (a,b] ou [a,b) conforme a convencao.
    entry_lo_idx = np.searchsorted(x_sorted, a + L / 2.0, side="right")
    entry_hi_idx = np.searchsorted(x_sorted, b + L / 2.0, side="right")
    entries = x_sorted[entry_lo_idx:entry_hi_idx] - L / 2.0

    exit_lo_idx = np.searchsorted(x_sorted, a - L / 2.0, side="right")
    exit_hi_idx = np.searchsorted(x_sorted, b - L / 2.0, side="right")
    exits = x_sorted[exit_lo_idx:exit_hi_idx] + L / 2.0

    events = np.concatenate([
        np.column_stack([entries, np.full(entries.shape, 1, dtype=np.int64)]),
        np.column_stack([exits, np.full(exits.shape, -1, dtype=np.int64)]),
    ]) if (entries.size or exits.size) else np.empty((0, 2))

    if events.size:
        order = np.argsort(events[:, 0], kind="stable")
        events = events[order]

    # integrar
    total = 0.0
    y_prev = a
    n_cur = n0
    for y_evt, delta in events:
        if y_evt > b:
            break
        if y_evt > y_prev:
            width = y_evt - y_prev
            total += (n_cur - L) ** 2 * width
        n_cur += int(delta)
        y_prev = y_evt
    if b > y_prev:
        total += (n_cur - L) ** 2 * (b - y_prev)

    dx = b - a
    return total, dx


def block_number_variance(x, L, B):
    """
    x: array de posicoes renormalizadas (nao precisa estar ordenado).
    L: largura da janela.
    B: numero de blocos.

    Retorna dict com V_hat, SE, n_blocks_used, per_block_V (lista).
    """
    x_sorted = np.sort(np.asarray(x, dtype=np.float64))
    x_min, x_max = x_sorted[0], x_sorted[-1]
    edges = np.linspace(x_min, x_max, B + 1)

    per_block_V = []
    for i in range(B):
        blo, bhi = edges[i], edges[i + 1]
        block_width = bhi - blo
        if block_width < 3.0 * L:
            continue  # descartado (Secao 2 do pre-registro)
        a = blo + L / 2.0
        b = bhi - L / 2.0
        if b <= a:
            continue
        integral, dx = _exact_window_integral_single_block(x_sorted, a, b, L)
        V_i = integral / dx
        per_block_V.append(V_i)

    per_block_V = np.array(per_block_V, dtype=np.float64)
    n_used = per_block_V.size
    if n_used == 0:
        return dict(V_hat=float("nan"), SE=float("nan"), n_blocks_used=0,
                     per_block_V=[])
    V_hat = float(np.mean(per_block_V))
    if n_used > 1:
        SE = float(np.std(per_block_V, ddof=1) / np.sqrt(n_used))
    else:
        SE = float("nan")
    return dict(V_hat=V_hat, SE=SE, n_blocks_used=int(n_used),
                per_block_V=per_block_V.tolist())


def brute_force_number_variance(x, L, a, b, resolution):
    """
    Cross-check por forca bruta: integra numericamente (grade fina,
    resolucao = passo de y) [n(L;y)-L]^2 sobre [a,b] via soma de Riemann
    (ponto medio), usando busca binaria simples para n(L;y) em cada ponto de
    grade. Independente do metodo exato por quebra de pontos.
    """
    x_sorted = np.sort(np.asarray(x, dtype=np.float64))
    n_steps = max(int(np.ceil((b - a) / resolution)), 1)
    ys = a + (np.arange(n_steps) + 0.5) * (b - a) / n_steps
    # n(L;y) com a MESMA convencao de fronteira: [y-L/2, y+L/2)
    lo_idx = np.searchsorted(x_sorted, ys - L / 2.0, side="left")
    hi_idx = np.searchsorted(x_sorted, ys + L / 2.0, side="left")
    n_vals = hi_idx - lo_idx
    integrand = (n_vals - L) ** 2
    integral = np.sum(integrand) * (b - a) / n_steps
    return integral / (b - a)


# ---------------------------------------------------------------------------
# Modelo A (Berry 1988, Conjectura 1.4.1(a) -- regime GUE ingenuo estendido)
# ---------------------------------------------------------------------------
from scipy.special import sici  # sici(x) -> (Si(x), Ci(x))
import math

EULER_GAMMA = 0.5772156649015328606065120900824024310421593359399235988057672348849


def model_A(L):
    """V_A(L) = (1/pi^2)*[log(2piL) - Ci(2piL) - 2piL*Si(2piL) + pi^2*L
                            - cos(2piL) + 1 + gamma0]"""
    L = np.asarray(L, dtype=np.float64)
    arg = 2.0 * np.pi * L
    Si, Ci = sici(arg)
    val = (np.log(arg) - Ci - 2.0 * np.pi * L * Si + (np.pi ** 2) * L
           - np.cos(arg) + 1.0 + EULER_GAMMA)
    return val / (np.pi ** 2)


# ---------------------------------------------------------------------------
# Modelo B (Berry 1988, Conjectura 1.4.1(b) -- correcao de primos)
# ---------------------------------------------------------------------------

def sieve_primes(n_max):
    """Crivo de Eratostenes vetorizado, retorna array de primos <= n_max."""
    if n_max < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(n_max + 1, dtype=bool)
    sieve[0:2] = False
    for p in range(2, int(n_max ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p:: p] = False
    return np.nonzero(sieve)[0]


def model_B_exact(L, T, logT, prime_powers_pk, prime_powers_k, prime_powers_logp):
    """
    V_B(L) = (1/pi^2) * [ sum_{p^k<=T} (1/(k^2 p^k)) * (1 - cos(2*pi*L*k*logp/logT)) + 1 ]

    usando a identidade Lambda(p^k)^2/(p^k log^2(p^k)) = 1/(k^2 p^k)
    (log(p^k) = k*log p  =>  Lambda(p^k)^2 = (log p)^2 ; denom = p^k * k^2 (log p)^2
     => razao = 1/(k^2 p^k), independente de log p -- confirmado abaixo por
     re-derivacao simbolica simples).

    prime_powers_pk: array de p^k (float64, pode overflow para T grande -- soh
                      usado para zeros1 onde T ~ 7.5e4).
    prime_powers_k, prime_powers_logp: arrays paralelos.
    """
    L = float(L)
    weight = 1.0 / (prime_powers_k ** 2 * prime_powers_pk)
    phase = 2.0 * np.pi * L * prime_powers_k * prime_powers_logp / logT
    s = np.sum(weight * (1.0 - np.cos(phase)))
    return (s + 1.0) / (np.pi ** 2)


def model_B_bounded_zeros3(L, T, logT, P_cutoff, primes_up_to_cutoff):
    """
    Cota bilateral para zeros3 (T grande, nao enumeramos todos os primos).

    Termo p^k <= P_cutoff: exato (sieve vetorizado ate P_cutoff), calculado de
    forma VETORIZADA: k=1 sobre TODOS os primos <= P_cutoff (11M+ primos, um
    loop Python seria proibitivamente lento); k>=2 exige p<=sqrt(P_cutoff)
    (~1650 primos), la sim um loop Python pequeno e barato.
    Cauda k=1, P_cutoff < p <= T: 0 <= sum 1/p <= 2*[cota Mertens] (cada termo
      da soma B tem peso 1/p * (1-cos(...)) em [0,2/p], entao a soma da cauda
      esta em [0, 2*sum_{P_cutoff<p<=T} 1/p]).
      Mertens: |sum_{p<=x} 1/p - loglog(x) - M| <= 4/log(x+1) + 2/(x log x),
      M = 0.2614972128476427837554268386086958590515666482611992...
      (constante de Meissel-Mertens).
    Cauda k>=2 alem de P_cutoff: <= 1/P_cutoff (serie geometrica majorada).

    Retorna (V_lower, V_upper).
    """
    M_MERTENS = 0.26149721284764278375542683860869585905156664826119
    L = float(L)

    primes_f = primes_up_to_cutoff.astype(np.float64)
    logp_all = np.log(primes_f)

    # termo k=1, vetorizado sobre TODOS os primos <= P_cutoff
    weight_k1 = 1.0 / primes_f
    phase_k1 = 2.0 * np.pi * L * 1.0 * logp_all / logT
    term_k1 = float(np.sum(weight_k1 * (1.0 - np.cos(phase_k1))))

    # termo k>=2, loop pequeno sobre primos <= sqrt(P_cutoff)
    sqrt_cutoff = int(math.isqrt(int(P_cutoff))) + 1
    small_mask = primes_up_to_cutoff <= sqrt_cutoff
    small_primes = primes_up_to_cutoff[small_mask]
    term_k_ge2 = 0.0
    for p in small_primes:
        p = int(p)
        logp = math.log(p)
        pk = p * p
        k = 2
        while pk <= P_cutoff:
            weight = 1.0 / (k * k * pk)
            phase = 2.0 * np.pi * L * k * logp / logT
            term_k_ge2 += weight * (1.0 - math.cos(phase))
            if pk > P_cutoff / p:
                break
            pk *= p
            k += 1

    exact_sum = term_k1 + term_k_ge2

    # cauda k=1: P_cutoff < p <= T
    def mertens_sum_upto(x):
        return math.log(math.log(x)) + M_MERTENS

    def mertens_bound(x):
        return 4.0 / math.log(x + 1.0) + 2.0 / (x * math.log(x))

    S_upto_T = mertens_sum_upto(T)
    S_upto_Pc = mertens_sum_upto(P_cutoff)
    # soma pontual entre os dois somatorios de Mertens (aproximacao central)
    tail_central = S_upto_T - S_upto_Pc
    tail_err = mertens_bound(T) + mertens_bound(P_cutoff)
    tail_k1_upper = 2.0 * max(tail_central + tail_err, 0.0)
    tail_k1_lower = 0.0  # cada termo eh nao-negativo, cota inferior trivial

    # cauda k>=2 alem de P_cutoff
    tail_k2_bound = 1.0 / P_cutoff

    V_lower = (exact_sum + tail_k1_lower + 0.0 + 1.0) / (np.pi ** 2)
    V_upper = (exact_sum + tail_k1_upper + tail_k2_bound + 1.0) / (np.pi ** 2)
    return V_lower, V_upper
