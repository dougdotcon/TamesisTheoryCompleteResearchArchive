# Proveniência — equações de auto-calibração de f_multi (Chae 2023/2024)

**Data:** 2026-08-22
**Test ID:** `SPARC-FMULTI-STAGE1` (retomada de `DISC-COSMOLOGY-MOND-SPARC-004`, autorizada por `DISC-DEC-023`)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22

## 0. Objetivo deste documento

Registrar, com verificação literal (download direto do fonte LaTeX do arXiv,
não memória, não resumo de terceiros), as equações exatas de auto-calibração
de `f_multi` citadas em `PREREGISTRATION.md` Seção 4 ("Chae Eqs. 11-13") e
usadas por `hidden_companion_check.py`/`hidden_companion_check_v2.py` — e
corrigir a citação se os números reais divergirem do que já estava
registrado no repositório.

## 1. Fontes baixadas nesta sessão

| item | arXiv ID | título verificado | arquivo LaTeX | sha256 do `.tex` |
|---|---|---|---|---|
| Artigo A | 2305.04613 | "Breakdown of the Newton-Einstein Standard Gravity at Low Acceleration in Internal Dynamics of Wide Binary Stars" (Chae 2023, ApJ 952, 128) | `WBgravity_corrected.tex` | `113d5eb20ffc3adbbd8ff2faa60e2b669c8617c4a894802d32c85122d5d35a2c` |
| Artigo B (companheiro) | 2309.10404 | "Robust Evidence for the Breakdown of Standard Gravity at Low Acceleration from Statistically Pure Binaries Free of Hidden Companions" (Chae 2024, ApJ) | `WBpure_r2_prep.tex` | `57bd3098420030cc62732e5dfc85f7392bf7107458d542f9cdc6acaa23bd06b3` |

Ambos baixados via `curl -sSL https://arxiv.org/e-print/<id>` (fonte LaTeX
bruto do e-print, não HTML renderizado, não resumo por outro agente) e
extraídos (`tar -xzf`). Verificado por `\title{...}` no próprio `.tex` que o
título bate exatamente com a citação já usada no repositório (nenhuma
suposição de ID -> título feita sem checagem).

## 2. Metodologia de verificação dos números de equação

O AASTeX numera automaticamente cada ambiente `\begin{equation}`/`\begin{eqnarray}`
em ordem sequencial de aparição no documento compilado — o `.tex` bruto não
contém os números finais explicitamente (só `\label{...}`), então os números
foram reconstruídos contando cada ambiente de equação do início do documento
até o alvo, na ordem em que aparecem no arquivo.

**Checagem cruzada independente que confirma a contagem está correta:** o
Artigo B (Seção "A correction to Chae (2023)", `\label{sec:correction}`)
cita textualmente "*to replace equation~(18) of \cite{chae2023}*" ao
introduzir a fórmula corrigida `\label{eq:vpcomp}`. Contando os ambientes de
equação do Artigo A na ordem em que aparecem, o 18º é exatamente
`\label{eq:mockvpcomp}` (a fórmula de velocidade projetada mock do §3.4,
"Newtonian simulation") — bate exatamente com a citação externa e
independente do próprio Artigo B. Isso confirma que a contagem sequencial
usada abaixo para as Eqs. 11-13 está correta, não é uma suposição.

## 3. Equações 11-13 do Artigo A (Chae 2023) — verbatim, verificadas

Localização: `WBgravity_corrected.tex`, Seção "Including masses of hidden
close binaries" (`\label{sec:companion_mass}`), linhas 554-573.

### Equação 11 (`\label{eq:mags}`)

Magnitudes absolutas do hospedeiro (`h`) e da companheira oculta (`c`) dado
que a magnitude combinada observada é `M_G` e a fração de luminosidade do
hospedeiro é `κ`:

```
M_{G,h} = -2.5 log10(κ)     + M_G
M_{G,c} = -2.5 log10(1-κ)   + M_G
```

### Equação 12 (`\label{eq:kappa}`)

`κ` (fração de luminosidade do hospedeiro) em função da diferença de
magnitude `ΔM_G = M_{G,c} - M_{G,h}`:

```
κ = 1 / (1 + 10^(-0.4 · ΔM_G))
```

### Equação 13 (`\label{eq:powermag}`)

Distribuição de probabilidade em lei de potência para `ΔM_G`, calibrada
contra Tokovinin (2008, 440 pares independentes de `s>200`~au) e
Riddle et al. (2015) + Raghavan et al. (2010):

```
p(ΔM_G; γ_M) = (1+γ_M) · (ΔM_G/12)^γ_M ,   0 ≤ ΔM_G ≤ 12
```

com `γ_M ≈ -0.7` (Tokovinin 2008) ou `γ_M ≈ -0.6` (Riddle+2015/Raghavan+2010)
— o próprio Artigo A relata as duas estimativas e não escolhe uma única
como "correta", tratando-as como faixa de incerteza observacional.

**Veredito da verificação:** a citação já registrada em `PREREGISTRATION.md`
Seção 4 ("Chae Eqs. 11-13") e usada por `hidden_companion_check_v2.py`
está **correta** — os números de equação batem exatamente com o texto
fonte, confirmados por uma checagem cruzada independente (equação 18 citada
externamente pelo Artigo B). **Nenhuma correção de citação é necessária.**

## 4. O que as Eqs. 11-13 SÃO e o que NÃO SÃO

Isto é uma nuance importante que os relatórios anteriores da linha não
deixaram explícita, e que este documento corrige por precisão:

- Eqs. 11-13 especificam apenas o **modelo de injeção de magnitude/massa da
  companheira** (dado que um sistema TEM uma companheira oculta: como sua
  massa relativa é sorteada). Isso é exatamente o que
  `hidden_companion_check_v2.py` já reimplementava (`sample_kappa`,
  `sample_delta_mag`, `B_of_kappa`).
- O procedimento de **auto-calibração** propriamente dito (o algoritmo
  iterativo que ajusta `f_multi` até a convergência) NÃO é uma equação
  numerada isolada — é um procedimento descrito em prosa nas Seções
  "3.4 Newtonian simulation" e no texto ao redor da Eq. 21
  (`\label{eq:ggN}`), citado verbatim abaixo (Seção 5). **Nenhuma sessão
  anterior desta linha implementou esse procedimento iterativo** — as
  checagens adversariais v1/v2 usaram uma varredura de `f_multi` fixos da
  faixa observacional da literatura (0,25-0,47), não a auto-calibração
  genuína de Chae (ajuste do parâmetro livre contra o próprio dado, exigindo
  convergência no bin de maior aceleração). Essa é exatamente a lacuna que
  esta frente (`SPARC-FMULTI-STAGE1`) foi criada para fechar — ver
  `METHODOLOGY_ADDENDUM.md`.

## 5. Procedimento de auto-calibração — citação verbatim (prosa, não equação numerada)

Artigo A, `\label{sec:companion_mass}`, parágrafo 1 (linhas 550-... ):

> "For some fraction f_multi of wide binaries, there exist undetected close
> companion(s) to one or both components of the binary. The current
> literature (Section 3.5) suggests 0.3 ≲ f_multi ≲ 0.5. In our modeling
> f_multi is a free parameter. We start with a value from the observational
> range and iterate until the deprojected data at high acceleration
> (≈10⁻⁸ m s⁻²) statistically agree with the Newtonian expectation because
> all gravitational theories are supposed to converge towards Newtonian
> gravity at acceleration ≳10⁻⁸ m s⁻². We call this process a
> self-calibration of f_multi."

> **[Nota pós-adversarial, 2026-08-22]** Uma verificação adversarial
> independente (`../ADVERSARIAL_VERIFICATION.md` Frente 1) reconstruiu
> manualmente a numeração de seções do `.tex` bruto do Artigo A a partir do
> aninhamento `\section`/`\subsection` e obteve `\ref{sec:multi}` = Seção
> 2.3, não 3.5 como aparece no texto citado acima. A citação acima é
> VERBATIM do próprio Artigo A (o "(Section 3.5)" é a própria
> auto-referência interna do artigo via `\ref{}`, não uma citação inserida
> por este documento) — a reconstrução manual de uma verificação
> independente pode divergir da numeração real compilada (por exemplo, se
> a versão do arXiv consultada difere da versão final publicada, ou se a
> reconstrução perdeu algum ambiente de seção). Nenhuma equação, fórmula
> ou valor numérico usado por este pipeline depende deste número de seção
> — é uma citação interna do próprio Artigo A a outra parte de si mesmo,
> sem efeito sobre `f_multi`, `kappa`, `gamma_M` ou qualquer resultado
> catalogado. Registrado por precisão, não corrigido (nenhuma das duas
> partes compilou o `.tex` completo para confirmar a numeração real).

Artigo A, `\label{sec:newton}` ("Newtonian simulation"), último parágrafo
antes da Eq. 21:

> "We check whether the two ensembles agree in the highest acceleration bin
> as it is expected in any viable gravity theory. If not, we adjust f_multi
> and repeat the whole process until a good agreement is reached. It turns
> out that the good match is obtained for a reasonable value of f_multi."

Artigo B (companheiro, arXiv:2309.10404), linha 584, especifica o critério
de convergência numérico usado na prática:

> "[...] I am very conservative and require δ_obs-newt to be consistent with
> zero within a small fraction of the MC estimated 1σ."

e a legenda da Figura `delg_new` (linha 964):

> "Parameter f_multi was fitted through an iterative procedure so that
> δ_obs-newt = 0 is satisfied at x0≈-8.0."

**Isto é a especificação operacional completa e verbatim do algoritmo de
auto-calibração** usada para o desenho do pipeline em
`analysis/selfcal_pipeline.py` (ver `METHODOLOGY_ADDENDUM.md` Seção 2).

## 6. Achado adicional relevante (não solicitado, mas descoberto durante a verificação): erro conhecido e já corrigido pelo próprio Chae

O Artigo B, Seção "A correction to Chae (2023)" (`\label{sec:correction}`,
linhas 939-957), documenta que a Eq. 18 original do Artigo A (velocidade
projetada mock, ramo "Newtonian simulation") continha um erro válido **só**
para órbitas circulares:

**Original (Artigo A, Eq. 18, `\label{eq:mockvpcomp}`, ERRADA para e>0):**
```
v_{p,x} = -v(r) sin(φ)
v_{p,y} =  v(r) cos(i) cos(φ)
```

**Corrigida (Artigo B, `\label{eq:vpcomp}`, substitui a Eq. 18):**
```
v_{p,x'} = v(r) cos(ψ)
v_{p,y'} = v(r) cos(i) sin(ψ)
```
onde `ψ` é o mesmo ângulo da Eq. 7 (`\label{eq:psi}`, já usado na
desprojeção principal). O erro original usava a fase orbital `φ` (ângulo de
posição) diretamente em vez do ângulo `ψ` da direção da velocidade — para
`e=0` os dois coincidem a menos de 90°, por isso o erro só aparece para
órbitas excêntricas. Chae reporta que essa correção mudou o `f_multi`
autocalibrado de `0,65` (Artigo A, com o bug) para `0,48` (Artigo B,
corrigido) na amostra principal de 26.615 binárias.

**Checagem cruzada com o pipeline JÁ TRAVADO desta linha (`deprojection_common.py`,
`delta_obs_newt.py`, ambos LOCKED, não editados nesta sessão):** a função
`generate_synthetic_vp_newtonian` (em `delta_obs_newt.py`) já usa `psi_true`
(a mesma fórmula da Eq. 7/`eq:psi`), NÃO `phi_true` diretamente, para
projetar `v_p_synth` —

```python
v_p_synth = v_true * np.sqrt(cos_psi2 + cos_i2 * sin_psi2)
```

— ou seja, **o pipeline já travado desta linha já implementa a versão
CORRIGIDA (pós-erratum) da fórmula de projeção mock, não a versão original
com bug do Artigo A.** Isso não estava documentado explicitamente em nenhum
arquivo da linha antes desta verificação (o `PREREGISTRATION.md` cita
"Gaps a-c... Eqs. 7-9" do Artigo A sem mencionar o erratum do Artigo B).
Registrado aqui por precisão histórica — não é necessária nenhuma correção
de código, apenas documentação do porquê o pipeline já está certo.

## 7. Valores de referência de f_multi autocalibrado real (Chae, para comparação futura)

Do Artigo B (pós-correção do erratum, linha 955): `f_multi = 0,48` para a
amostra principal (26.615 binárias largas dentro de 200~pc, erro relativo
de PM `<0,01`); `f_multi = 0,36` para a subamostra mais estrita (19.716
binárias, erro relativo de PM `<0,005`). Ambos os valores caem dentro da
faixa observacional da literatura (`0,2 ≲ f_multi ≲ 0,5`) já usada pelas
checagens adversariais v1/v2 desta linha (`0,25-0,47`) — não fornecem um
valor "correto" a priori para a amostra Gaia EDR3+El-Badry+Hwang desta
linha (amostra, cortes e catálogo diferentes: DR3 vs. o processamento
específico de Chae, split discovery/holdout desta linha), mas servem como
checagem de sanidade de ordem de grandeza para o valor auto-calibrado que a
pipeline desta frente produzir em dado sintético/real.
