# Resultado alvo — YM-LIMIT-001

## Enunciado clássico (Clay Mathematics Institute, intacto)

> "Yang–Mills Existence and Mass Gap. Prove that for any compact simple
> gauge group G, a non-trivial quantum Yang–Mills theory exists on
> \(\mathbb R^4\) and has a mass gap \(\Delta > 0\)."

Fonte: [Clay Mathematics Institute — Yang-Mills & the Mass Gap](https://www.claymath.org/millennium/yang-mills-the-maths-gap/)
(verificado via WebSearch nesta sessão, 2026-08-09). Este enunciado **não**
é alterado, aproximado ou substituído por linguagem Tamesis em nenhum
outro arquivo desta frente — onde reformulações aparecem, o enunciado
clássico está sempre ao lado.

## Reformulação do escopo desta auditoria (linguagem Tamesis, ao lado do
## enunciado clássico, não no lugar dele)

Esta frente **não tenta** provar o enunciado acima. `YM-LIMIT-001` tenta
responder uma pergunta estritamente mais estreita, definida pelo
`target_statement` do work item:

> Determinar quais hipóteses adicionais (além de tightness da família de
> medidas de rede e gap positivo em cada volume finito) são necessárias
> para que um limite contínuo/infravermelho de uma construção candidata
> produza (i) uma única teoria limite e (ii) um gap de massa que sobrevive
> a esse limite.

## Produto esperado desta rodada

Um dos dois, não ambos necessariamente:

- **Teorema de insuficiência**: mostrar formalmente que as hipóteses
  tipicamente citadas (tightness + gap de volume finito positivo) não
  implicam logicamente (i) nem (ii) acima, sem hipótese adicional
  explícita.
- **Contraexemplo abstrato**: uma construção matemática concreta (não
  necessariamente de Yang–Mills real) que satisfaz as hipóteses dadas e
  viola a conclusão.

Esta rodada produz **ambos**, no nível abstrato/de análise real —
ver `PROOF_SKETCH.md`, `COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md` e
`FORMAL/InsufficiencyToyModel.lean`.

## O que este resultado NÃO afirma

- Não afirma que a teoria de Yang–Mills real (rede de Wilson, ação
  \(S_W\), grupo \(SU(N)\)) de fato falha em ter limite único ou gap —
  apenas que a *cadeia de hipóteses* comumente citada, por si, não prova
  isso.
- Não resolve, não aproxima, nem declara "quase resolvido" o problema do
  milênio.
- Não confunde uma subsequência convergente (garantida por
  Prokhorov/Bolzano–Weierstrass sob tightness) com a existência de uma
  única teoria limite — este é precisamente o erro que o `stop_condition`
  desta frente proíbe, e que o contraexemplo `toyGap` em
  `FORMAL/InsufficiencyToyModel.lean` torna explícito e comprovado.
