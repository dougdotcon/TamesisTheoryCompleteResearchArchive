# Definições — YM-LIMIT-001

Status anterior: `NOT_FORMALIZED`. Esta rodada formaliza apenas o vocabulário
mínimo necessário para enunciar o teorema de insuficiência desta auditoria —
não define a medida de Yang–Mills completa em \(\mathbb R^4\).

Convenção: cada item lista (a) a noção informal usada na literatura,
(b) a definição de trabalho adotada aqui, (c) se foi ou não formalizada em
Lean nesta rodada.

## D1 — Rede e acoplamento

- **Informal**: rede hipercúbica \(\Lambda_a \subset \mathbb R^4\) de
  espaçamento \(a>0\), volume finito \(L\), medida de Wilson
  \(\mu_{a,L}\) com ação \(S_W\) e acoplamento \(\beta = 1/g^2\).
- **Trabalho aqui**: não formalizada. Tratada apenas como rótulo de índice
  de uma família \(\{\mu_{a,L}\}\) — ver D3.
- **Lean nesta rodada**: não.

## D2 — Gap de volume finito \(m(a,L)\)

- **Informal**: diferença entre o menor autovalor não nulo do Hamiltoniano
  de transferência em volume finito e o estado fundamental.
- **Trabalho aqui**: tratado como um número real positivo indexado por
  \(n\) (substituto abstrato de \((a,L)\)), sem construir o operador que o
  produz. Ver `toyFiniteVolumeGap` em `FORMAL/InsufficiencyToyModel.lean`.
- **Lean nesta rodada**: sim, no nível do substituto abstrato (não do
  operador físico).

## D3 — Tightness (apertamento) de uma família de medidas

- **Informal (Prokhorov)**: uma família \(\{\mu_n\}\) de medidas de
  probabilidade num espaço métrico completo separável é *tight* (apertada)
  se para todo \(\varepsilon>0\) existe compacto \(K\) tal que
  \(\mu_n(K^c) < \varepsilon\) para todo \(n\). Prokhorov: tightness
  \(\Rightarrow\) toda subsequência tem subsequência fracamente
  convergente (recíproca também vale em espaço métrico completo separável).
  Ver seção "Verificado" em `REVIEWS/AUDIT_REPORT.md`.
- **Trabalho aqui**: usada apenas na forma do seu análogo elementar em
  \(\mathbb R\) — toda sequência limitada tem subsequência convergente
  (Bolzano–Weierstrass), que é o caso especial de Prokhorov em espaço
  compacto. Não formalizamos tightness genérica de medidas de rede.
- **Lean nesta rodada**: não formalizada como enunciado geral; usada
  implicitamente no contraexemplo (`toyGap`, ambos os limites de
  subsequência existem porque a sequência é limitada).

## D4 — Limite contínuo subsequencial vs. teoria limite única

- **Limite subsequencial**: existe \(\phi:\mathbb N\to\mathbb N\)
  estritamente crescente e \(\mu\) tais que
  \(\mu_{\phi(n)} \rightharpoonup \mu\) (convergência fraca).
- **Teoria limite única**: existe um único \(\mu\) tal que
  \(\mu_n \rightharpoonup \mu\) — isto é, **toda** subsequência converge
  para o mesmo limite, não apenas alguma subsequência.
- Esta distinção é o objeto central desta auditoria (ver `stop_condition`
  em `PROOF_SKETCH.md`): tightness garante o primeiro, não o segundo.
- **Lean nesta rodada**: sim, ver `toyGap_no_unique_continuum_limit`.

## D5 — Gap uniforme e sobrevivência do gap no limite

- **Gap uniforme**: \(\inf_{n} m_n \ge c > 0\), com \(c\) independente de
  \(n\).
- **Sobrevivência do gap**: se \(H_n \to H\) em algum sentido de
  convergência de operadores, o gap espectral de \(H\) satisfaz
  \(\mathrm{gap}(H) \ge c\).
- A literatura de análise espectral (ver `REVIEWS/AUDIT_REPORT.md`,
  seção Verificado) estabelece que sob convergência **forte de
  resolvente**, o espectro do limite não pode *expandir*, mas pode
  *contrair repentinamente* — ou seja, gap uniforme nos aproximantes não
  implica gap no limite sem hipótese adicional.
- **Lean nesta rodada**: sim, no nível abstrato/numérico —
  `toyFiniteVolumeGap_not_uniform` mostra que gap positivo em cada \(n\)
  não implica gap uniforme; não formalizamos o operador de multiplicação
  do contraexemplo espectral completo (ver `COUNTEREXAMPLES/`), que fica
  registrado como não tentado em Lean nesta rodada.

## O que este documento NÃO faz

Não define a medida de Yang–Mills, o Hamiltoniano de transferência físico,
os axiomas de Osterwalder–Schrader/Wightman, nem qualquer objeto do
enunciado clássico do problema do milênio. Ver `OFFICIAL_STATEMENT.md`
para o enunciado clássico intacto.
