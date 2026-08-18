"""Pipeline vetorizada de desprojecao 3D via Monte Carlo orbital
(metodo primario de Chae 2023, ApJ 952, 128) para
DISC-COSMOLOGY-MOND-SPARC-004.

Implementa EXATAMENTE os Gaps (a)-(e) da Secao 4 de PREREGISTRATION.md.
Tudo vetorizado em numpy sobre arrays de shape (n_mc, n_sys) -- nenhum
laco Python por sistema em nenhuma etapa (amostragem de excentricidade,
solucao da equacao de Kepler, desprojecao).

Unidades: todas as quantidades fisicas de entrada/saida desta pipeline
sao SI (metros, kg, m/s, m/s^2) -- conversao AU->m e Msun->kg deve ser
feita pelo chamador (constantes AU_M, MSUN_KG fornecidas abaixo, iguais
as ja usadas em ../../COSMOLOGY_WIDE_BINARIES/analysis/).

===========================================================================
Gap (a) -- amostragem de excentricidade por sistema
===========================================================================
Para cada sistema:
  - Se `dpm_sig>3` E `e`/`e0`/`e1` do catalogo de Hwang nao-NaN E `e<0.99`
    (mesmo caso-limite de Chae): amostrar de uma Gaussiana truncada
    ASSIMETRICA ("split normal") em [0.001, 0.999], centrada em `e`
    (mediana), com sigma=e1-e para o lado ACIMA da mediana e sigma=e-e0
    para o lado ABAIXO -- regra exata declarada por Chae (Artigo A,
    linha 506), citada literalmente em PREREGISTRATION.md Gap (a).
  - Caso contrario: amostrar de p(e;alpha)=(1+alpha)*e^alpha em (0,1),
    usando o `alpha` ja tabulado por Hwang para aquele par (inversao de
    CDF fechada: e = U^(1/(alpha+1))).

===========================================================================
Gap (b) -- graus de liberdade orbitais marginalizados
===========================================================================
  - i ~ p(i)=sin(i) em (0,pi/2) (orientacao isotropica). Inversao de CDF
    fechada: CDF(i)=1-cos(i) => i=arccos(1-U).
  - phi0 ~ U(0,2pi) (longitude do periastro).
  - t ~ U(0,T); fase orbital phi obtida resolvendo
    t \\propto \\int_{phi0}^{phi} dphi'/(1+e cos phi')^2
    (equacao de Kepler, PREREGISTRATION.md Gap b, formula LITERAL, sem
    deslocar o integrando por phi0).

    Reducao a forma fechada usada aqui (para evitar quadratura numerica
    por sistema, mantendo tudo vetorizado): a identidade padrao de
    mecanica celeste dM/dnu=(1-e^2)^(3/2)/(1+e*cos nu)^2 (nu=anomalia
    verdadeira, M=anomalia media) implica, por integracao direta com
    nu:=phi' (a MESMA variavel de integracao do Gap b, sem deslocamento):

        \\int_{phi0}^{phi} dphi'/(1+e cos phi')^2
            = [M(phi) - M(phi0)] / (1-e^2)^(3/2)

    onde M(x) para qualquer x e' a funcao "anomalia media a partir de
    anomalia verdadeira x" padrao (M(x)=E(x)-e*sin(E(x)),
    E(x)=2*atan2(sqrt(1-e)*sin(x/2), sqrt(1+e)*cos(x/2))). O periodo
    completo corresponde a integral sobre um ciclo completo de 2pi em
    M, C=2pi/(1-e^2)^(3/2). Logo a condicao t/T=tau~U(0,1) vira:

        M(phi) = M(phi0) + tau*2*pi   (mod 2*pi)

    resolvida para `phi` via inversao padrao da equacao de Kepler
    (E - e*sinE = M_target, Newton-Raphson vetorizado em numpy;
    phi = anomalia verdadeira de E). Isso e' EXATO (nao aproximado) --
    apenas evita quadratura numerica ao usar a antiderivada fechada
    conhecida da mesma integral, com Newton-Raphson usado exatamente
    onde a equacao de Kepler exige (nao ha solucao fechada para E).
    phi0 permanece presente explicitamente no calculo (M(phi0) e'
    computado a partir dele, nao descartado), preservando fidelidade
    literal a formula do Gap (b) mesmo que, por um argumento de
    invariancia por rotacao modulo 2*pi, o resultado final de `phi`
    acabe sendo estatisticamente independente do valor especifico de
    phi0 amostrado (checado numericamente em
    analysis/validate_synthetic_newtonian.py).

===========================================================================
Gap (c) -- formulas de desprojecao (Eqs 7-9 de Chae 2023)
===========================================================================
    psi = atan2(-(cos(phi)+e*cos(phi0)), (sin(phi)+e*sin(phi0)))
    r = s / sqrt(cos(phi)^2 + cos(i)^2*sin(phi)^2)
    v = v_p / sqrt(cos(psi)^2 + cos(i)^2*sin(psi)^2)

(usa-se atan2 em vez de atan simples por robustez numerica quando o
denominador se aproxima de zero -- irrelevante para o resultado final
porque so' cos(psi)^2 e sin(psi)^2 sao usados a jusante, que sao
invariantes por psi -> psi+pi, a mesma ambiguidade de sinal que atan()
simples ja teria.)

===========================================================================
Gap (d) -- estatistica por sistema
===========================================================================
    g_N = G*M_tot / r^2   (Newtoniana, SI)
    g = v^2 / r           (cinematica, SI)

===========================================================================
Gap (e) -- protocolo Monte Carlo
===========================================================================
N_MC realizacoes completas e independentes da amostra inteira, cada uma
com seu proprio sorteio de (e, i, phi0, t) por sistema -- shape de saida
(n_mc, n_sys). Bootstrap de 1000 replicas sobre os sistemas (reamostrando
UM dos n_mc valores ja computados por sistema por replica) e' feito a
JUSANTE desta pipeline (nao aqui), conforme Gap (e) item 3 da
PREREGISTRATION.md.
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------
# Constantes fisicas (identicas as ja usadas em
# ../../COSMOLOGY_WIDE_BINARIES/analysis/*.py -- nao redefinidas)
# ---------------------------------------------------------------------
G_SI = 6.67430e-11          # m^3 kg^-1 s^-2
MSUN_KG = 1.98892e30        # kg
AU_M = 1.495978707e11       # m
MAS_YR_TO_KM_S_PER_PC = 4.74047e-3  # fator mu[mas/yr]*d[pc] -> km/s (Chae 2023 Eq.4)

_ECC_LO, _ECC_HI = 0.001, 0.999  # limites de truncamento do Gap (a)


# ---------------------------------------------------------------------
# Kepler: anomalia verdadeira <-> anomalia media, Newton-Raphson vetorizado
# ---------------------------------------------------------------------

def _true_to_mean_anomaly(nu: np.ndarray, e: np.ndarray) -> np.ndarray:
    """M(nu) = E(nu) - e*sin(E(nu)), forma fechada (sem iteracao)."""
    E = 2.0 * np.arctan2(np.sqrt(1.0 - e) * np.sin(nu / 2.0),
                          np.sqrt(1.0 + e) * np.cos(nu / 2.0))
    return E - e * np.sin(E)


def _solve_kepler_E(M: np.ndarray, e: np.ndarray, tol: float = 1e-12,
                     max_iter: int = 50) -> np.ndarray:
    """Resolve E - e*sin(E) = M para E, Newton-Raphson vetorizado em numpy,
    com correcao de 3a ordem (Newton-Raphson-Halley / "metodo de Danby",
    Danby 1988 -- extensao padrao de Newton-Raphson em mecanica celeste)
    para garantir convergencia robusta ate e=0.999 sem divergir por
    overshoot: Newton-Raphson simples (1a ordem) diverge para uma fracao
    pequena mas nao-desprezivel de (M,e) proximos do periastro em
    excentricidades altas (f'=1-e*cos(E) proximo de zero), confirmado
    empiricamente nesta sessao (RuntimeError de nao-convergencia com
    Newton puro em teste de fumaca). A correcao de 3a ordem usa f'' e
    f''' (tambem calculados em forma fechada, sem quadratura) para
    amortecer o passo perto da singularidade -- ainda e' um metodo de
    raiz de Newton, apenas com ordem de convergencia mais alta e maior
    raio de convergencia, nao uma mudanca de algoritmo.

    Sem laco Python por sistema/realizacao em nenhuma iteracao -- cada
    iteracao do laco `for` (sobre o NUMERO DE ITERACOES do metodo, nao
    sobre sistemas) atualiza o array (n_mc, n_sys) inteiro de uma vez.
    """
    E = M + np.sign(np.sin(M)) * 0.85 * e  # chute inicial robusto (Danby)
    for _ in range(max_iter):
        sinE, cosE = np.sin(E), np.cos(E)
        f = E - e * sinE - M
        if np.max(np.abs(f)) < tol:
            break
        fp = 1.0 - e * cosE
        fpp = e * sinE
        fppp = e * cosE
        d1 = -f / fp
        d2 = -f / (fp + 0.5 * d1 * fpp)
        d3 = -f / (fp + 0.5 * d2 * fpp + d2 ** 2 * fppp / 6.0)
        E = E + d3
    else:
        f = E - e * np.sin(E) - M
        if np.max(np.abs(f)) >= tol:
            raise RuntimeError(
                f"Solucao da equacao de Kepler nao convergiu em "
                f"{max_iter} iteracoes (residuo max |f|={np.max(np.abs(f)):.3e})"
            )
    return E


def _mean_to_true_anomaly(M: np.ndarray, e: np.ndarray) -> np.ndarray:
    E = _solve_kepler_E(M, e)
    return 2.0 * np.arctan2(np.sqrt(1.0 + e) * np.sin(E / 2.0),
                             np.sqrt(1.0 - e) * np.cos(E / 2.0))


# ---------------------------------------------------------------------
# Gap (a): amostragem de excentricidade
# ---------------------------------------------------------------------

def sample_eccentricity(e_m: np.ndarray, e_lo: np.ndarray, e_hi: np.ndarray,
                         alpha: np.ndarray, dpm_sig: np.ndarray,
                         n_mc: int, rng: np.random.Generator):
    """Gap (a). Retorna (e_sample, use_individual).

    e_sample: array (n_mc, n_sys) float64, excentricidade amostrada,
      truncada em [0.001, 0.999] em ambos os ramos.
    use_individual: array (n_sys,) bool, True onde o par usou o ramo da
      Gaussiana truncada individual (dpm_sig>3, e/e0/e1 validos, e<0.99),
      False onde usou o fallback populacional p(e;alpha).
    """
    e_m = np.asarray(e_m, dtype=np.float64)
    e_lo = np.asarray(e_lo, dtype=np.float64)
    e_hi = np.asarray(e_hi, dtype=np.float64)
    alpha = np.asarray(alpha, dtype=np.float64)
    dpm_sig = np.asarray(dpm_sig, dtype=np.float64)
    n_sys = e_m.shape[0]

    use_individual = (
        (dpm_sig > 3)
        & np.isfinite(e_m) & np.isfinite(e_lo) & np.isfinite(e_hi)
        & (e_m < 0.99)
    )

    # ---- ramo 1: split-normal truncada em [0.001,0.999] ----
    # sigma_hi/sigma_lo minimos de 1e-6 evitam divisao por zero no caso
    # degenerado e0==e==e1 (nao observado nos dados reais, ver
    # PROVENANCE_HWANG.md, mas protegido aqui por robustez).
    sigma_hi = np.clip(e_hi - e_m, 1e-6, None)
    sigma_lo = np.clip(e_m - e_lo, 1e-6, None)
    p_hi = sigma_hi / (sigma_lo + sigma_hi)  # massa de probabilidade acima da mediana

    side_hi = rng.random((n_mc, n_sys)) < p_hi[None, :]

    # amostragem por inversao de CDF de meia-normal truncada, via
    # scipy.special.ndtr/ndtri (ufuncs vetorizados, sem laco Python)
    from scipy.special import ndtr, ndtri

    u_hi = rng.random((n_mc, n_sys))
    b_hi = (_ECC_HI - e_m) / sigma_hi          # limite superior padronizado
    phi_b_hi = ndtr(b_hi)[None, :]
    z_hi = ndtri(0.5 + u_hi * (phi_b_hi - 0.5))
    e_draw_hi = e_m[None, :] + sigma_hi[None, :] * z_hi

    u_lo = rng.random((n_mc, n_sys))
    a_lo = (_ECC_LO - e_m) / sigma_lo          # limite inferior padronizado
    phi_a_lo = ndtr(a_lo)[None, :]
    z_lo = ndtri(phi_a_lo + u_lo * (0.5 - phi_a_lo))
    e_draw_lo = e_m[None, :] + sigma_lo[None, :] * z_lo

    e_individual = np.where(side_hi, e_draw_hi, e_draw_lo)

    # ---- ramo 2: fallback populacional p(e;alpha)=(1+alpha)*e^alpha ----
    # CDF(e) = e^(alpha+1) em (0,1) => inversao fechada e = U^(1/(alpha+1))
    u_fb = rng.random((n_mc, n_sys))
    e_fallback = u_fb ** (1.0 / (alpha[None, :] + 1.0))

    e_sample = np.where(use_individual[None, :], e_individual, e_fallback)
    e_sample = np.clip(e_sample, _ECC_LO, _ECC_HI)
    return e_sample, use_individual


# ---------------------------------------------------------------------
# Gap (b): graus de liberdade orbitais + solucao da equacao de Kepler
# ---------------------------------------------------------------------

def sample_orbital_geometry(e_sample: np.ndarray, rng: np.random.Generator):
    """Gap (b). Recebe e_sample (n_mc, n_sys) ja amostrado (Gap a).

    Retorna (i, phi0, phi), cada um shape (n_mc, n_sys):
      i    -- inclinacao, i~sin(i) em (0,pi/2)
      phi0 -- longitude do periastro, phi0~U(0,2pi)
      phi  -- fase orbital no instante de observacao, resolvida da
              equacao de Kepler conforme derivacao no docstring do
              modulo (Newton-Raphson vetorizado, sem laco por sistema).
    """
    shape = e_sample.shape

    i = np.arccos(1.0 - rng.random(shape))          # p(i)=sin(i), (0,pi/2)
    phi0 = rng.random(shape) * 2.0 * np.pi           # U(0,2pi)
    tau = rng.random(shape)                          # t/T ~ U(0,1)

    M0 = _true_to_mean_anomaly(phi0, e_sample)
    M_target = np.mod(M0 + tau * 2.0 * np.pi, 2.0 * np.pi)
    phi = np.mod(_mean_to_true_anomaly(M_target, e_sample), 2.0 * np.pi)

    return i, phi0, phi


# ---------------------------------------------------------------------
# Gap (c): formulas de desprojecao
# ---------------------------------------------------------------------

def deproject(s: np.ndarray, v_p: np.ndarray, e_sample: np.ndarray,
              i: np.ndarray, phi0: np.ndarray, phi: np.ndarray):
    """Gap (c), Eqs. 7-9 de Chae (2023). s, v_p: shape (n_sys,) SI
    (broadcast contra e_sample/i/phi0/phi de shape (n_mc,n_sys)).

    Retorna (r, v), cada um (n_mc, n_sys), SI.
    """
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)
    cos_i2 = np.cos(i) ** 2

    numer = -(cos_phi + e_sample * np.cos(phi0))
    denom = sin_phi + e_sample * np.sin(phi0)
    psi = np.arctan2(numer, denom)
    cos_psi2 = np.cos(psi) ** 2
    sin_psi2 = np.sin(psi) ** 2

    r = s[None, :] / np.sqrt(cos_phi ** 2 + cos_i2 * sin_phi ** 2)
    v = v_p[None, :] / np.sqrt(cos_psi2 + cos_i2 * sin_psi2)
    return r, v


# ---------------------------------------------------------------------
# Gap (d) + (e): pipeline completa
# ---------------------------------------------------------------------

def run_mc_deprojection(s: np.ndarray, v_p: np.ndarray, M_tot: np.ndarray,
                         e_m: np.ndarray, e_lo: np.ndarray, e_hi: np.ndarray,
                         alpha: np.ndarray, dpm_sig: np.ndarray,
                         n_mc: int = 200, seed: int = 12345) -> dict:
    """Pipeline vetorizada completa de desprojecao 3D via Monte Carlo
    (Gaps a-e da PREREGISTRATION.md Secao 4).

    Parametros (todos os arrays SI, shape (n_sys,)):
      s       -- separacao projetada observada [m]
      v_p     -- velocidade relativa projetada observada [m/s]
      M_tot   -- massa total do sistema [kg]
      e_m, e_lo, e_hi -- excentricidade mediana/e0/e1 do catalogo de
                  Hwang (podem ter NaN -- tratado pelo Gap a)
      alpha   -- indice da distribuicao populacional p(e;alpha), ja
                  tabulado por Hwang (sem NaN esperado)
      dpm_sig -- significancia de deteccao de movimento relativo (Hwang)
      n_mc    -- numero de realizacoes Monte Carlo completas (Gap e,
                  N_MC=200 no pre-registro)
      seed    -- semente do gerador (numpy Generator PCG64)

    Retorna dict com arrays shape (n_mc, n_sys) (exceto onde indicado):
      'log_g_ratio'       -- log10(g/g_N), a estatistica primaria
      'g', 'gN'           -- aceleracoes cinematica/Newtoniana [SI]
      'r', 'v'            -- separacao/velocidade 3D desprojetadas [SI]
      'e_sample'          -- excentricidade amostrada por realizacao
      'i', 'phi0', 'phi'  -- geometria orbital amostrada
      'use_individual_ecc' -- (n_sys,) bool, Gap (a) ramo 1 vs 2
      'n_mc', 'seed'      -- metadados de reproducibilidade
    """
    s = np.asarray(s, dtype=np.float64)
    v_p = np.asarray(v_p, dtype=np.float64)
    M_tot = np.asarray(M_tot, dtype=np.float64)
    n_sys = s.shape[0]
    for name, arr in (("v_p", v_p), ("M_tot", M_tot), ("e_m", e_m),
                       ("e_lo", e_lo), ("e_hi", e_hi), ("alpha", alpha),
                       ("dpm_sig", dpm_sig)):
        if np.asarray(arr).shape[0] != n_sys:
            raise ValueError(f"{name} tem tamanho diferente de s ({n_sys})")

    rng = np.random.default_rng(seed)

    e_sample, use_individual = sample_eccentricity(
        e_m, e_lo, e_hi, alpha, dpm_sig, n_mc, rng)
    i, phi0, phi = sample_orbital_geometry(e_sample, rng)
    r, v = deproject(s, v_p, e_sample, i, phi0, phi)

    gN = G_SI * M_tot[None, :] / r ** 2
    g = v ** 2 / r
    log_g_ratio = np.log10(g / gN)

    return {
        "log_g_ratio": log_g_ratio,
        "g": g,
        "gN": gN,
        "r": r,
        "v": v,
        "e_sample": e_sample,
        "i": i,
        "phi0": phi0,
        "phi": phi,
        "use_individual_ecc": use_individual,
        "n_mc": n_mc,
        "seed": seed,
    }
