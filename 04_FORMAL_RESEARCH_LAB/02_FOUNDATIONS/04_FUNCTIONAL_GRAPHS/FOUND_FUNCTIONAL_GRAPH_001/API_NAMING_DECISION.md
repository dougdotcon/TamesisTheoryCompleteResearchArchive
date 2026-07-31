---
document_id: FFG-API-NAMING-DECISION
status: BINDING
gate: FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW
---

# FOUND-FUNCTIONAL-GRAPH-001 — Decisões de nomenclatura da API

## 1. Recorrência — `IsRecurrent` **não** será publicado

A especificação anterior previa

```lean
def IsRecurrent (f : X → X) (x : X) : Prop := x ∈ Function.periodicPts f
def IsTransient (f : X → X) (x : X) : Prop := ¬ IsRecurrent f x
```

**Retirado.** "Recorrência" tem significados mais amplos em dinâmica —
recorrência de Poincaré, recorrência por retorno a vizinhança, recorrência
em cadeias de Markov — e nenhum deles coincide com "ser ponto periódico".
Publicar `IsRecurrent` como sinônimo de ponto periódico seria um alias
semanticamente enganoso.

## Estratégia adotada

```text
Estrategia A, com a clausula condicional resolvida NEGATIVAMENTE.
```

O gate recomendou a Estratégia A, cuja instrução principal é *usar
diretamente `x ∈ Function.periodicPts f` nos teoremas públicos*, e cuja
segunda parte é condicional: definir `IsCyclePoint`/`IsTransientPoint`
**somente se melhorar a leitura**.

Resolvo essa condicional **negativamente**, com uma razão verificável: a
lista `CORE` congelada em `FINAL_SIGNATURES.md` **não usa nenhum dos
dois**. Todos os teoremas públicos escrevem `x ∈ Function.periodicPts f`
ou `x ∉ Function.periodicPts f` diretamente.

```yaml
IsRecurrent:      NAO_PUBLICADO
IsTransient:      NAO_PUBLICADO
IsCyclePoint:     NAO_CRIADO   (condicional resolvida negativamente)
IsTransientPoint: NAO_CRIADO   (idem)
uso_publico:      "x ∈ Function.periodicPts f  e  x ∉ Function.periodicPts f"
```

Consequência prática: nesta resolução, a Estratégia A coincide com a
Estratégia B. Registro a coincidência para que a leitura futura não
suponha que uma terceira via foi inventada.

### Princípio aplicado

O mesmo que adia `componentSet`: **não publicar definição sem uso na API
pública**. `x ∉ Function.periodicPts f` é o idioma da Mathlib, não é mais
longo que `IsTransientPoint f x`, e não introduz um nome que precise ser
aprendido.

### Se a leitura piorar

Se a formalização descobrir que os enunciados ficam ilegíveis sem os
aliases, `IsCyclePoint` e `IsTransientPoint` — **nesses nomes**, nunca
`IsRecurrent` — podem ser criados com equivalência `Iff.rfl`, registrada
como teorema de auditoria. Não é autorização; é a saída registrada.

---

## 2. `SameFunctionalComponent` — não criado

Nem `def`, nem `abbrev`. `EventuallyMeets` é o único nome público da
relação. "Mesmo componente funcional" é a **leitura**, documentada em
`COMPONENT_NOTIONS.md`.

---

## 3. `componentSet` — adiado

```yaml
componentSet:
  status: DEFERRED_API_ALIAS
```

Nenhum teorema `CORE` o utiliza. Mesmo princípio do item 1.

---

## 4. `IterReachable` — nome escolhido para evitar homonímia

Três relações parecidas convivem no laboratório e na Mathlib:

| Nome | Origem | Significado |
|---|---|---|
| `IterReachable` | esta frente | iteração de `f` |
| `Reachable` | `FOUND-SEMIGROUP-002` | ação de monoide, `∃ m, m • x = y` |
| `SimpleGraph.Reachable` | Mathlib | grafo **não dirigido** |

O prefixo `Iter` é deliberado. `SimpleGraph` não será importada no núcleo,
o que elimina a terceira colisão por construção.

---

## 5. `EventuallyMeets.of_iterReachable_left` — não criado

Duplicaria `IterReachable.eventuallyMeets`. Uma direção basta; a simetria
de `EventuallyMeets` cobre o resto.

---

## Resumo da superfície pública

```text
DEFINICOES     IterReachable, MutuallyReachable, EventuallyMeets      3
TEOREMAS CORE  iterReachable_refl/trans, IterReachable.eventuallyMeets,
               eventuallyMeets_refl/symm/trans,
               periodicOrbit_eq_of_eventuallyMeets,
               exists_cyclePoint_reachable_with_bound,
               exists_component_cycle_with_entry_bound              9
OPCIONAL       eventuallyMeets_of_periodicOrbit_eq,
               mutuallyReachable_of_periodicOrbit_eq                2
```

Doze objetos públicos no máximo. Nenhum alias sem uso.
