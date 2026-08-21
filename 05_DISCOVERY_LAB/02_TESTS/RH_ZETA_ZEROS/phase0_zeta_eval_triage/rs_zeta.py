"""
RH-REAL Fase 0 (itens 5/6/10) -- motor de avaliacao de zeta na linha critica.

evidence_level: exploratory_only. NAO e um teste pre-registrado.

Z(t) = e^{i theta(t)} zeta(1/2 + i t)  (funcao de Riemann-Siegel, real),
|Z(t)| = |zeta(1/2+it)|.

Implementacao: formula de Riemann-Siegel, soma principal + correcao C0,
vetorizada em numpy. Fases computadas em np.longdouble (80-bit em x86-64)
para conter o erro de arredondamento de t*log(n) em t grande (~1e11).
Validada contra mpmath (mp.siegelz / mp.zeta) por validate_zeta_eval.py
ANTES de qualquer uso nos itens -- ver validation_zeta_eval.{log,json}.

Nenhum dado embutido/fabricado: tudo aqui e formula classica
(Riemann-Siegel; ver Edwards, "Riemann's Zeta Function", cap. 7).
"""
import numpy as np

TWO_PI = 2.0 * np.pi
LD = np.longdouble
# constantes em precisao estendida via string (nao via float64 -- um 2*pi
# derivado de float64 injetaria erro ~n_voltas*8e-16 ~ 1e-4 na reducao
# mod 2pi em t~1e11; detectado na primeira rodada de validacao)
PI_LD = LD("3.14159265358979323846264338328")
TWO_PI_LD = LD("6.28318530717958647692528676656")


def theta(t):
    """Funcao theta de Riemann-Siegel, expansao assintotica de Stirling:
    theta(t) = t/2 log(t/2pi) - t/2 - pi/8 + 1/(48t) + 7/(5760 t^3) + ...
    Entrada: array float64 ou longdouble; saida: longdouble."""
    t = np.asarray(t, dtype=LD)
    return (t / 2 * np.log(t / TWO_PI_LD) - t / 2 - PI_LD / 8
            + 1 / (48 * t) + 7 / (5760 * t**3))


def _c0(p):
    """Termo de correcao C0(p) = cos(2pi(p^2 - p - 1/16)) / cos(2pi p).
    Zeros do denominador em p=1/4, 3/4 sao removiveis (numerador tambem
    se anula); perto deles avalia-se por media simetrica p +/- 1e-3
    (erro ~1e-6, documentado na nota de triagem)."""
    p = np.asarray(p, dtype=np.float64)
    den = np.cos(TWO_PI * p)
    num = np.cos(TWO_PI * (p * p - p - 0.0625))
    out = np.empty_like(p)
    bad = np.abs(den) < 1e-4
    ok = ~bad
    out[ok] = num[ok] / den[ok]
    if np.any(bad):
        # media simetrica dos dois lados (zero removivel do denominador)
        left = np.cos(TWO_PI * ((p[bad] - 1e-3)**2 - (p[bad] - 1e-3) - 0.0625)) \
            / np.cos(TWO_PI * (p[bad] - 1e-3))
        right = np.cos(TWO_PI * ((p[bad] + 1e-3)**2 - (p[bad] + 1e-3) - 0.0625)) \
            / np.cos(TWO_PI * (p[bad] + 1e-3))
        out[bad] = 0.5 * (left + right)
    return out


def Z_chunk(t):
    """Z(t) para um chunk 1-D de valores t (todos >= ~30). Retorna float64."""
    t = np.asarray(t, dtype=np.float64)
    a = np.sqrt(t / TWO_PI)                    # sqrt(t/2pi)
    N = np.floor(a).astype(np.int64)
    Nmax = int(N.max())
    n = np.arange(1, Nmax + 1)
    logn = np.log(n).astype(LD)
    # fase em longdouble: theta(t) - t*log n, reduzida mod 2pi antes do cos
    th = theta(t)                              # (m,) longdouble
    tl = np.asarray(t, dtype=LD)
    phase = th[:, None] - tl[:, None] * logn[None, :]
    phase = np.remainder(phase, TWO_PI_LD).astype(np.float64)
    terms = np.cos(phase) / np.sqrt(n)[None, :]
    mask = (n[None, :] <= N[:, None])
    main = 2.0 * np.sum(terms * mask, axis=1)
    p = (a - N).astype(np.float64)
    corr = ((-1.0) ** (N - 1)) * (t / TWO_PI) ** (-0.25) * _c0(p)
    return main + corr


def Z(t, chunk_elems=int(3e7)):
    """Z(t) para array 1-D arbitrario; processa em chunks limitados a
    ~chunk_elems entradas de matriz (memoria/velocidade)."""
    t = np.asarray(t, dtype=np.float64)
    out = np.empty_like(t)
    i = 0
    m = len(t)
    while i < m:
        # tamanho de chunk pelo N local (t assumido ~mesma ordem de grandeza)
        Nloc = max(int(np.sqrt(t[i] / TWO_PI)) + 1, 1)
        step = max(int(chunk_elems // Nloc), 1)
        j = min(i + step, m)
        out[i:j] = Z_chunk(t[i:j])
        i = j
    return out
