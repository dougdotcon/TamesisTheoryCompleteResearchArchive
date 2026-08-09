# Resultado — Teorema de insuficiência (YM-LIMIT-001)

## Status

`PARTIAL_RESULT` no sentido do laboratório: um teorema formal (abstrato)
de insuficiência, com dois contraexemplos verificados na estrutura lógica
(um formalizado em Lean, um em prosa matemática elementar não formalizada
nesta rodada), e um terceiro contraexemplo (espectral) apenas em prosa.
Não é, e não pretende ser, um passo em direção à resolução do problema do
milênio (`AGENTS.md`).

## Enunciado formal (nível abstrato)

> Sejam \((a_n)_{n\in\mathbb N} \subset \mathbb R_{>0}\) e a hipótese de
> que \((a_n)\) é limitada (tight). Então, em geral:
>
> **(i)** \((a_n)\) admite subsequência convergente (Bolzano–Weierstrass,
> caso especial de Prokhorov em espaço compacto), **mas não** converge
> necessariamente — logo não define uma "teoria limite" única sem
> hipótese adicional de unicidade da subsequência.
>
> **(ii)** \(\forall n,\ a_n > 0\) **não implica** \(\inf_n a_n > 0\) —
> logo positividade do gap em cada volume finito não implica, sozinha,
> gap uniforme (e, a fortiori, não implica gap no limite).

## Prova

Por contraexemplo, construtiva, em ambos os casos:

- (i) refutado por `toyGap` (gap uniforme ≥ 2, mas subsequências pares e
  ímpares convergem para valores diferentes, 2 e 3): lema
  `YMLimit001.Toy.toyGap_no_unique_continuum_limit` em
  `../FORMAL/InsufficiencyToyModel.lean`.
- (ii) refutado por `toyFiniteVolumeGap = 1/(n+1)` (positivo em cada `n`,
  ínfimo zero): lema
  `YMLimit001.Toy.finite_volume_gap_does_not_survive_without_uniform_bound`
  no mesmo arquivo.

Detalhes matemáticos completos, incluindo o terceiro contraexemplo
(espectral, não formalizado em Lean) em
`../COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md`.

## Corolário para a leitura de YM-LIMIT-001

A cadeia de hipóteses "tightness da família de medidas de rede + gap de
volume finito positivo" — tal como usada informalmente na literatura
secundária resumida em `ANALISE_CRITICA_YM.md` — **não constitui prova**
de que:

1. existe uma única teoria de Yang–Mills contínua (requer hipótese de
   unicidade adicional, não derivável de tightness sozinha);
2. o gap sobrevive ao limite contínuo (requer \(\inf_{a,L} m(a,L) > 0\)
   como hipótese explícita, mais um modo de convergência de operador
   forte o suficiente para que o espectro não "contraia" — ver
   contraexemplo 3).

Isto **não é novo** como diagnóstico qualitativo — o documento legado já
apontava os mesmos dois gaps informalmente. A contribuição desta rodada é
tornar a insuficiência **verificável formalmente** no nível da estrutura
lógica abstrata (Lean, sem `sorry`), separando claramente o que foi
demonstrado (a estrutura lógica é insuficiente) do que permanece
inteiramente aberto (se a teoria de Yang–Mills real, com as hipóteses
adicionais corretas, de fato tem limite único e gap — pergunta que esta
frente não tenta responder).

## O que NÃO se afirma

- Não se afirma que a teoria de Yang–Mills não tem mass gap.
- Não se afirma que a construção de Balaban, Osterwalder–Schrader, ou
  qualquer resultado citado esteja errado — apenas que a *cadeia de
  inferência* entre eles, como costuma ser apresentada, tem um elo que
  não é uma implicação lógica válida sem hipótese adicional.
- Não se afirma "quase resolvido" nem se atribui uma porcentagem de
  completude ao problema do milênio.
