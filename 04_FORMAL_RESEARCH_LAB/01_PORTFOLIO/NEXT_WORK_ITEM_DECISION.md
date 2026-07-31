---
document_id: NEXT-WORK-ITEM-DECISION
work_item_id: FOUND-FUNCTIONAL-GRAPH-001
status: SCOPED
decided_at: 2026-07-31
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED
---

# FOUND-FUNCTIONAL-GRAPH-001 — decisão e escopo preliminar

> **Escopo apenas.** Nenhum teorema é especificado definitivamente aqui.
> Nenhum arquivo Lean foi criado. Nenhuma prova foi executada.

## Identificação

```yaml
work_item_id: FOUND-FUNCTIONAL-GRAPH-001
title: "Finite Functional Graph Decomposition"
track: foundations
status: SCOPED
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Dados centrais

```text
X : tipo finito
f : X → X
```

Um **grafo funcional** é o grafo dirigido em que cada estado tem
exatamente uma aresta de saída, `x → f x`. É a mesma estrutura já estudada
em `FOUND-SEMIGROUP-002` na Camada C — o que muda é a pergunta: lá se
perguntava sobre **uma trajetória**; aqui se pergunta sobre a **estrutura
global** do grafo.

## Conceitos candidatos

```text
trajetoria
alcancabilidade por iteracao
alcancabilidade mutua
estado periodico
estado eventualmente periodico
estado transitorio
estado recorrente
ciclo
bacia de atracao
distancia ate o ciclo
componente funcional
```

Aviso de nível, herdado de `FOUND-SEMIGROUP-002`: *alcançabilidade por
iteração de `f`* **não** é a mesma coisa que `Reachable` da Camada A, que
quantifica sobre todo o monoide. Se a nova frente reutilizar `Reachable`,
terá de instanciá-lo com o monoide livre de um gerador — e isso é uma
decisão de especificação, não um dado.

## Resultado estrutural candidato

> Cada componente de um grafo funcional finito contém um ciclo dirigido, e
> todo estado do componente alcança esse ciclo após um número finito de
> iterações.

Este enunciado é **consequência direta** de `exists_eventual_period`, já
verificado: o ciclo é a órbita de `f^[μ] x`, e a distância até ele é
limitada por `μ < card X`.

## Resultado mais forte — **não autorizado**

> Cada componente conexa do grafo funcional possui exatamente **um** ciclo
> dirigido, com árvores direcionadas entrando nesse ciclo.

```yaml
status: NOT_AUTHORIZED_BEFORE_SPECIFICATION
```

Motivo: a unicidade depende inteiramente de qual noção de "componente" for
adotada — componente fracamente conexa do grafo dirigido, ou classe de
alcançabilidade mútua, ou bacia de um ciclo. As três dão enunciados
diferentes, e uma delas torna a afirmação trivial por definição. Decidir
isso é trabalho da especificação (`FFG-GAP-002`, `FFG-GAP-004`).

## Dependências reutilizadas

```yaml
from_FOUND-SEMIGROUP-002:
  - exists_eventual_period
  - exists_bounded_iterate_collision
  - periodic_tail_of_collision
  - collision_propagates
  - Reachable            # se instanciado com monoide livre de um gerador
  - CE-001..CE-005       # como referencia de estilo e de limites
from_Mathlib:
  - Fintype, Fintype.card
  - DecidableEq, decide
  - Function.iterate, Function.iterate_add_apply
  - Function.IsPeriodicPt, Function.IsFixedPt
  - Fintype.exists_ne_map_eq_of_card_lt
```

Nenhuma dependência nova de biblioteca externa é prevista.

## Gaps iniciais

```yaml
FFG-GAP-001:
  title: representação do grafo funcional sem dependência excessiva da API de grafos
  note: >
    A API de grafos da Mathlib (SimpleGraph) eh NAO DIRIGIDA e nao serve
    diretamente. Decidir entre: (a) trabalhar so com f e iterate, sem
    objeto "grafo"; (b) Quiver; (c) Rel. A opcao (a) eh a mais provavel.
  status: OPEN

FFG-GAP-002:
  title: definição correta de componente funcional
  note: "tres candidatos incompativeis; escolher um e registrar o custo"
  status: OPEN
  blocking: "bloqueia o resultado forte"

FFG-GAP-003:
  title: equivalência entre alcançabilidade mútua e pertencimento ao mesmo ciclo
  status: OPEN

FFG-GAP-004:
  title: existência versus unicidade do ciclo por componente
  status: OPEN
  blocking: "bloqueia o resultado forte"

FFG-GAP-005:
  title: definição de estado recorrente
  note: "recorrente = periodico? = na imagem de toda iterada? nao sao equivalentes a priori"
  status: OPEN

FFG-GAP-006:
  title: definição e limites da distância até o ciclo
  note: "candidato natural: o menor mu; exige minimalidade, adiada em FSG2-GAP-004b"
  status: OPEN

FFG-GAP-007:
  title: representação de árvores de entrada
  status: OPEN

FFG-GAP-008:
  title: dependência de DecidableEq e escolhas finitas
  note: >
    Em FOUND-SEMIGROUP-002, DecidableEq X provou-se ociosa. Aqui pode NAO
    ser: definir "o menor mu" ou decidir pertencimento a ciclo tende a
    exigi-la. Verificar em vez de presumir.
  status: OPEN

FFG-GAP-009:
  title: reutilização da periodicidade eventual já formalizada
  status: OPEN

FFG-GAP-010:
  title: fronteira entre teorema padrão e aplicações de software
  status: OPEN
```

## Contraexemplos planejados

Todos classificados `COUNTEREXAMPLE_TO_OVERGENERALIZATION`.

```yaml
FFG-CE-001:
  refutes: "todo grafo funcional finito possui um unico ciclo global"
  sketch: "dois pontos fixos desconectados"

FFG-CE-002:
  refutes: "todo estado eh periodico desde o instante inicial"
  sketch: "cauda longa antes do ciclo; reaproveita a forma de CE-003"

FFG-CE-003:
  refutes: "todo comportamento recorrente termina em ponto fixo"
  sketch: "ciclo de comprimento 2 ou 3"

FFG-CE-004:
  refutes: "a trajetoria anterior ao ciclo eh unica para toda a bacia"
  sketch: "dois ramos distintos entrando no mesmo ciclo"

FFG-CE-005:
  refutes: "igualdade de periodo implica pertencimento ao mesmo componente"
  sketch: "dois pontos fixos distintos, ambos de periodo 1"
```

## Aplicações mapeadas — conceitualmente

```text
maquinas de estado
workflows
pipelines de processamento
parsers
sistemas de retry
deteccao de loops
jogos deterministicos finitos
automatos
agentes discretos
auditoria de transicoes
```

**Nenhuma integração foi implementada.** E, como já registrado em
`FOUND-SEMIGROUP-002`:

```text
A reutilizacao em software NAO transforma o resultado matematico padrao
em descoberta cientifica.
```

## Limites vinculantes

Proibido conectar esta frente a:

```text
TRI; TDTR; teoria de tudo; tempo fisico; entropia fisica;
mecanica quantica; cosmologia; Hipotese de Riemann; Hilbert-Polya;
qualquer conjectura Clay.
```

Proibido afirmar:

```text
nova lei universal; nova teoria de dinamica;
descoberta matematica; descoberta fisica.
```

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

A decomposição de grafos funcionais em ciclos com árvores de entrada é
material padrão, presente em qualquer tratamento de "rho shape" de
iteração finita. O valor é **formal e de reutilização**, não de
descoberta.

## Próximo passo autorizado

```yaml
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED
```

Preparar a especificação. **Nenhuma formalização autorizada. Nenhum
arquivo Lean.**
