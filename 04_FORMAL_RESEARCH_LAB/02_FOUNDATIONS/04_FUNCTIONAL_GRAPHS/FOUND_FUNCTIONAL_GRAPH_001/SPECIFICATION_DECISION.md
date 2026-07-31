---
document_id: FFG-SPECIFICATION-DECISION
work_item_id: FOUND-FUNCTIONAL-GRAPH-001
decision: A_FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY
gate: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION
---

# FOUND-FUNCTIONAL-GRAPH-001 — Decisão da especificação

## Decisão

```text
A. FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY
```

## Checklist de `READY`

| Exigência | Estado |
|---|---|
| `IterReachable` definida | sim — `DEFINITIONS.md` |
| `EventuallyMeets` definida | sim |
| diferença para `MutuallyReachable` explicitada | sim — `COMPONENT_NOTIONS.md`, `FFG-CE-004` |
| componente escolhido | sim — `EventuallyMeets`, vinculante |
| `periodicPts` auditada | sim — `∃ n > 0` por definição |
| `periodicOrbit` auditada | sim — `Cycle α`, sem `DecidableEq`, noncomputável |
| teorema principal formulado | sim — `FFG-MAIN-001/002` |
| unicidade corretamente interpretada | sim — órbita, não representante |
| limite de entrada avaliado | sim — `mu < card X` em `FFG-MAIN-002` |
| `DecidableEq` auditada | sim — **não necessária no núcleo** |
| contraexemplos planejados | sim — seis |
| gaps registrados | sim — catorze |
| `SimpleGraph` diferida | sim — `FFG-GAP-012` |
| novidade delimitada | sim — `NONE`, vinculante |
| nenhuma prova executada | sim — 0 arquivos Lean |

## As quatro decisões que este gate travou

### 1. Componente é `EventuallyMeets`

Não `MutuallyReachable`. O contraexemplo `a → c ← b`, `c → c` mostra que a
segunda separa em três classes o que geometricamente é uma estrutura só.

### 2. Um único nome para a relação

`EventuallyMeets`. `SameFunctionalComponent` foi **rejeitado** como segundo
nome — inclusive na forma `abbrev`, porque dois nomes públicos para o mesmo
predicado duplicam a superfície de API sem ganho.

### 3. Unicidade é igualdade de órbitas

`Function.periodicOrbit f q = Function.periodicOrbit f p`. O representante
`p` **não** é único e **não** é canônico. `FFG-CE-005` exibe dois pontos
periódicos distintos com a mesma órbita.

### 4. Orientação fixada

```text
o primeiro argumento de EventuallyMeets vai para o lado ESQUERDO da
igualdade de orbitas.
```

Consistente em `FFG-CYCLE-001` e em `FFG-MAIN-001`.

## Duas correções da própria especificação

### Assinatura rejeitada de `exists_recurrent_reachable`

A forma com `∃ μ p : ℕ × X` foi descartada: o par é artificial, obriga a
escrever `p.2` e não acrescenta informação, já que `p` é determinado por
`f^[μ] x`. Adotada a alternativa limpa, que o próprio gate recomendou.

### Previsão sobre `DecidableEq` refutada

O gate de portfólio registrou, em `FFG-GAP-008`, a previsão de que
`DecidableEq X` provavelmente **seria** necessária aqui, ao contrário de
`FOUND-SEMIGROUP-002`. A leitura da fonte **refutou** isso para o núcleo:
`Dynamics/PeriodicPts/Defs.lean:57` não a declara, e nenhum lema de
`periodicOrbit` a acrescenta.

Registro a refutação em vez de silenciá-la: era uma previsão explícita, e
ela errou.

## Um achado que muda o plano de contraexemplos

`periodicOrbit` está em `noncomputable section`. Logo `decide` **não** se
aplica a igualdade de órbitas. Não bloqueia o núcleo — nenhum teorema
`CORE` decide igualdade de ciclos —, mas obriga `FFG-CE-005` a usar
`periodicOrbit_apply_iterate_eq`. Registrado em `FFG-GAP-011`.

## Por que a revisão vem antes da formalização

Porque a decisão de §1 é a única difícil de reverter. Uma definição errada
de componente congelada em Lean contaminaria `componentSet`, o teorema
principal e os seis contraexemplos. O custo de revisar agora é uma leitura;
o custo de reverter depois seria refazer a frente.

## Próxima ação

```yaml
authorized_action: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_AUTHORIZED
```

**Formalização não autorizada.**
