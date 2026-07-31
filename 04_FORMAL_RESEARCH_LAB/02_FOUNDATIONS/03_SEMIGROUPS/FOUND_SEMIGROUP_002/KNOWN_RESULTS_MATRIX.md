---
document_id: FSG2-KNOWN-RESULTS-MATRIX
bibliographic_audit: NOT_AUDITED
---

# FOUND-SEMIGROUP-002 — Matriz de resultados conhecidos

## Aviso de método

Este laboratório **não obteve nem auditou** fonte primária alguma de teoria
de semigrupos ou de dinâmica discreta finita (`FSG2-GAP-009`, herdado de
`FOUND-SG-GAP-003`). A coluna "estado na literatura" abaixo reflete
**conhecimento geral elementar**, não auditoria bibliográfica.

Consequência vinculante:

```text
Nenhuma afirmacao de prioridade historica pode ser feita.
Nenhuma atribuicao a autor especifico pode ser feita.
Nenhuma citacao pode ser apresentada como fonte de enunciado.
```

## Matriz

| Resultado | Estado na literatura | Estado na Mathlib fixada | Estado aqui |
|---|---|---|---|
| Alcançabilidade é reflexiva e transitiva | elementar | `mem_orbit_self`, `mem_orbit_of_mem_orbit` (parcial) | a formalizar (`FSG2-REACH-001/002`) |
| Órbita de uma ação | padrão | `MulAction.orbit` — **existe** | reutilizar |
| Alcançabilidade ⟺ pertinência à órbita | definicional | `mem_orbit_iff` é `Iff.rfl` | reutilizar |
| Invariante constante em órbitas | elementar | não localizado nesta forma | a formalizar (`FSG2-INV-001`) |
| Iteração = potência da ação | padrão | `smul_iterate_apply` — **existe** | reutilizar |
| Casa dos pombos em tipos finitos | elementar | `Fintype.exists_ne_map_eq_of_card_lt` | reutilizar |
| Ponto periódico, ponto fixo, período minimal | padrão | `IsPeriodicPt`, `IsFixedPt`, `minimalPeriod` | reutilizar com cautela |
| **Periodicidade eventual em conjunto finito** | **elementar e antigo** | **ausente** | **a formalizar localmente** |
| Decomposição única cauda + ciclo | padrão | não localizado | **adiado** (`FSG2-GAP-004b`) |
| Detecção de ciclo (tortoise and hare) | algoritmo clássico | fora de escopo | não pertence a esta frente |

## O achado que importa

A busca por `preperiodic`, `eventuallyPeriodic` e `eventually_periodic` em
todo o Mathlib da revisão fixada devolveu **zero ocorrências**. A ausência
**não** significa que o resultado seja novo — significa que é curto demais
e específico demais de cada aplicação para ter virado API compartilhada.

`Function.IsPeriodicPt f n x := f^[n] x = x` exige retorno ao ponto
**inicial**. Isso é periodicidade estrita, não eventual. A distinção é
exatamente o conteúdo de `CE-003` e a razão de `FSG2-PER-004` existir.

## Posição em relação a `FOUND-SEMIGROUP-001`

| Propriedade | `C3` (FOUND-SG) | Geral (FSG2) |
|---|---|---|
| ação fiel | sim (FOUND-SG-012) | **não** — `CE-004` |
| ação transitiva | sim (FOUND-SG-013) | **não** — `CE-002` |
| alcançabilidade simétrica | sim (é grupo) | **não** — `CE-001` |
| toda órbita sem cauda | sim | **não** — `CE-003` |

Quatro propriedades que valem em `C3` e falham em geral. É precisamente por
isso que `C3` **não** serve como caso de teste do alvo: ele é bom demais.
Usá-lo como evidência de generalidade seria o erro que
`NOVELTY_BOUNDARY.md` proíbe.
