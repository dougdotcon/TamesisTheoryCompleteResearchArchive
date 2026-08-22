"""Modelo de injecao de companheira oculta -- Chae (2023) Eqs. 11-13,
verificadas verbatim por fetch direto do fonte LaTeX nesta sessao
(ver ../PROVENANCE_CHAE_EQS.md Secao 3). Parte do pipeline de
auto-calibracao de f_multi -- SPARC-FMULTI-STAGE1 (DISC-DEC-023).

Diferenca em relacao a ../../analysis/hidden_companion_check_v2.py (que
reimplementa o MESMO modelo de injecao, mas para um teste de plausibilidade
POS-HOC com f_multi FIXO varrido na faixa da literatura): as funcoes aqui
sao VETORIZADAS sobre uma dimensao extra de realizacao Monte Carlo
(shape (n_mc, n_sys), nao so' (n_sys,)) -- necessario porque a
auto-calibracao exige, por definicao, sortear uma injecao de companheira
INDEPENDENTE a cada realizacao MC (nao uma unica injecao fixa reusada em
todos os n_mc draws), exatamente como o texto de Chae especifica ("For
randomly selected f_multi x N_binary systems, close companion(s) is(are)
assigned" -- por REALIZACAO, nao uma vez so').

Todas as formulas abaixo sao identicas em conteudo as ja usadas e
adversarialmente checadas em hidden_companion_check_v2.py -- nenhuma
reformulacao do modelo fisico, so' vetorizacao sobre n_mc.
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------
# Constantes do modelo (identicas as ja usadas e aceitas em
# hidden_companion_check_v2.py -- ver METHODOLOGY_ADDENDUM.md Secao 1a
# para a justificativa de cada escolha)
# ---------------------------------------------------------------------
GAMMA_M = -0.7          # Eq. 13, Tokovinin (2008) -- ver Secao 1a do addendum
DELTA_MAG_RANGE = (0.0, 12.0)   # Eq. 13, faixa LITERAL do Artigo A (0<=dM_G<=12).
                                  # hidden_companion_check_v2.py usava (0.01,5.0)
                                  # como aproximacao pratica -- aqui usamos a
                                  # faixa EXATA do artigo (protegida numericamente
                                  # por um piso em delta_mag, ver sample_delta_mag).
ALPHA_MASS_LUM = 3.5    # expoente L ~ M^alpha, mesmo valor usado por Chae
                          # (texto perto da Eq. 20/eq:rphot) e ja usado sem
                          # alteracao pelas checagens adversariais anteriores.

_DELTA_MAG_FLOOR = 1e-3  # piso numerico para evitar B(kappa) indefinido/kappa=1
                           # exatamente no limite delta_mag->0 (probabilidade
                           # de medida zero, protecao numerica apenas)


def sample_delta_mag(shape, rng: np.random.Generator,
                      gamma_M: float = GAMMA_M,
                      mag_range: tuple[float, float] = DELTA_MAG_RANGE) -> np.ndarray:
    """Eq. 13: p(dM_G;gamma_M) = (1+gamma_M)*(dM_G/12)^gamma_M em [0,12].

    Amostragem por inversao de CDF fechada. CDF(x) = (x/12)^(1+gamma_M) em
    [0,12] (para gamma_M>-1, caso de Chae com gamma_M=-0.7). Inversao:
    x = 12 * U^(1/(1+gamma_M)).

    `shape` pode ser (n_sys,) ou (n_mc,n_sys) -- qualquer shape de array
    numpy e' aceito, a formula e' elementwise.
    """
    lo, hi = mag_range
    g1 = 1.0 + gamma_M
    u = rng.random(shape)
    delta_mag = hi * (u ** (1.0 / g1))
    delta_mag = np.clip(delta_mag, max(lo, _DELTA_MAG_FLOOR), hi)
    return delta_mag


def kappa_from_delta_mag(delta_mag: np.ndarray) -> np.ndarray:
    """Eq. 12: kappa = 1/(1+10^(-0.4*dM_G)) -- fracao de luminosidade do
    hospedeiro (>=0.5 sempre, pois dM_G=mag(companheira)-mag(hospedeiro)>=0
    por construcao de sample_delta_mag)."""
    return 1.0 / (1.0 + 10.0 ** (-0.4 * delta_mag))


def B_of_kappa(kappa: np.ndarray, alpha: float = ALPHA_MASS_LUM) -> np.ndarray:
    """Fator de inflacao de massa B(kappa) = kappa^(1/alpha) + (1-kappa)^(1/alpha) >= 1.

    Derivado (nao uma equacao numerada isolada de Chae -- ver
    PROVENANCE_CHAE_EQS.md Secao 4 / METHODOLOGY_ADDENDUM.md Secao 1a item 5)
    da Eq. 11 (magnitudes host/companheira dado kappa) + a relacao
    massa-luminosidade L~M^alpha que o proprio Artigo A usa (alpha=3.5,
    texto perto da Eq. 20). Se a massa catalogada de um componente e'
    inferida da luz COMBINADA (hospedeiro+companheira oculta) tratada como
    uma unica estrela, mas a massa VERDADEIRA e' a soma das massas
    individuais (cada uma inferida de sua propria luz), entao:

        M_cat = mass_from_L(L_total) ~ L_total^(1/alpha)
        M_true = mass_from_L(kappa*L_total) + mass_from_L((1-kappa)*L_total)
               ~ L_total^(1/alpha) * [kappa^(1/alpha) + (1-kappa)^(1/alpha)]
               = M_cat * B(kappa)

    B(kappa)>=1 sempre (concavidade de x->x^(1/alpha) para alpha>1, por
    desigualdade de potencias/Jensen) -- massa catalogada SEMPRE subestima
    a massa verdadeira quando ha' companheira nao resolvida.
    """
    return kappa ** (1.0 / alpha) + (1.0 - kappa) ** (1.0 / alpha)


def photocenter_beta(kappa: np.ndarray, alpha: float = ALPHA_MASS_LUM) -> np.ndarray:
    """Fracao de deslocamento fotocentro-baricentro da sub-componente
    MINORITARIA (fracao de luz kappa<=0.5 por construcao aqui -- kappa e'
    sempre a fracao do HOSPEDEIRO/componente mais brilhante, entao a
    minoritaria e' 1-kappa; mas a formula abaixo e' escrita para a
    fracao de massa/luz da sub-componente de interesse, mesma convencao
    ja usada em hidden_companion_check_v2.py::photocenter_beta):

        beta = fracao_de_massa_minoritaria - fracao_de_luz_minoritaria
             = (1-kappa)^(1/alpha)/B(kappa) - (1-kappa)
    """
    B = B_of_kappa(kappa, alpha)
    minority_light_frac = 1.0 - kappa
    minority_mass_frac = (1.0 - kappa) ** (1.0 / alpha) / B
    return minority_mass_frac - minority_light_frac


def sample_companion_injection_mc(M1_cat: np.ndarray, M2_cat: np.ndarray,
                                   f_multi: float, n_mc: int,
                                   rng: np.random.Generator,
                                   gamma_M: float = GAMMA_M,
                                   alpha: float = ALPHA_MASS_LUM):
    """Sorteia UMA injecao de companheira INDEPENDENTE por realizacao MC
    (shape (n_mc,n_sys) em todos os retornos) -- Chae Sec.3.4 item 1:
    "For randomly selected f_multi x N_binary systems, close companion(s)
    is(are) assigned ... All the components ... are assigned masses and
    fixed for both real data and mock data."  (a fixacao real/mock
    acontece NO CHAMADOR, que reusa o MESMO M1_true/M2_true retornado aqui
    para computar g_N em ambos os ramos -- ver selfcal_pipeline.py).

    Retorna dict com M1_true, M2_true (n_mc,n_sys) e diagnosticos.
    """
    M1_cat = np.asarray(M1_cat, dtype=np.float64)
    M2_cat = np.asarray(M2_cat, dtype=np.float64)
    n_sys = M1_cat.shape[0]
    shape = (n_mc, n_sys)

    u_has = rng.random(shape)
    has_multi = u_has < f_multi
    u_which = rng.random(shape)
    affects_bright = has_multi & (u_which < 0.40)
    affects_faint = has_multi & (u_which >= 0.40) & (u_which < 0.70)
    affects_both = has_multi & (u_which >= 0.70)

    mask1 = affects_bright | affects_both
    mask2 = affects_faint | affects_both

    delta_mag_1 = sample_delta_mag(shape, rng, gamma_M)
    delta_mag_2 = sample_delta_mag(shape, rng, gamma_M)
    kappa_1 = kappa_from_delta_mag(delta_mag_1)
    kappa_2 = kappa_from_delta_mag(delta_mag_2)
    B1 = B_of_kappa(kappa_1, alpha)
    B2 = B_of_kappa(kappa_2, alpha)

    M1_true = np.where(mask1, M1_cat[None, :] * B1, M1_cat[None, :])
    M2_true = np.where(mask2, M2_cat[None, :] * B2, M2_cat[None, :])
    M1_true = np.broadcast_to(M1_true, shape).copy()
    M2_true = np.broadcast_to(M2_true, shape).copy()

    return {
        "M1_true": M1_true, "M2_true": M2_true,
        "Mtot_true": M1_true + M2_true,
        "has_multi": has_multi,
        "mask1": mask1, "mask2": mask2,
        "kappa_1": kappa_1, "kappa_2": kappa_2,
        "frac_has_multi": float(has_multi.mean()),
    }
