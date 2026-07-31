---
document_id: FFG-LEAN-FEASIBILITY
mathlib_rev: 79d0395a1825a6264ad5d269e35e60537518955e
lean_files_created: 0
lake_builds: 0
---

# FOUND-FUNCTIONAL-GRAPH-001 — Viabilidade Lean

## Decisão sobre `DecidableEq X` — as três camadas

O gate pediu auditoria separada por camada. Resultado:

### Camada proposicional

```text
IterReachable       ∃ n, f^[n] x = y
EventuallyMeets     ∃ m n, f^[m] x = f^[n] y
MutuallyReachable   conjuncao das anteriores
IsRecurrent         pertinencia a periodicPts
IsTransient         negacao
componentSet        Set X
```

Nenhuma exige `DecidableEq X`. São `Prop`/`Set`, não computações.

### Uso de `periodicOrbit`

**Verificado na fonte, não presumido.** O bloco de variáveis de
`Dynamics/PeriodicPts/Defs.lean:57` é

```lean
variable {α : Type*} {β : Type*} {f fa : α → α} {fb : β → β} {x y : α} {m n : ℕ}
```

Sem `[DecidableEq α]`. E `periodicOrbit`, `periodicOrbit_apply_iterate_eq`,
`mem_periodicOrbit_iff`, `self_mem_periodicOrbit` e
`periodicOrbit_length` não a acrescentam.

`DecidableEq (Cycle α)` existe (`Data/List/Cycle.lean:482`) mas **exige**
`[DecidableEq α]` — e no núcleo nenhuma igualdade de ciclos precisa ser
**decidida**, apenas **provada**.

### Camada de distância mínima ou algoritmo executável

Provavelmente exigiria `DecidableEq X` ou escolha não computável. **Está
adiada** (`minimal_entry_time: NOT_AUTHORIZED`), logo não impõe hipótese.

### Conclusão

```yaml
nucleo_exige: "[Fintype X] somente"
decidable_eq_no_nucleo: false
previsao_anterior_refutada: true
```

A previsão registrada em `FFG-GAP-008` no gate de portfólio — de que
`DecidableEq X` provavelmente **seria** necessária aqui, ao contrário de
`FOUND-SEMIGROUP-002` — está **refutada para o núcleo**. A leitura da fonte
mostrou que a API de órbitas periódicas é livre de `DecidableEq`. A
previsão continua plausível apenas para os itens adiados.

Registrar isso importa: era uma previsão explícita, e ela errou.

## Restrição de noncomputabilidade

`periodicOrbit` está dentro de `noncomputable section`
(linhas 240–490). Portanto:

```text
`decide` NAO se aplica a igualdade de orbitas periodicas.
```

Isso **não** bloqueia o núcleo — nenhum teorema `CORE` precisa decidir
igualdade de ciclos. Afeta apenas os contraexemplos, que usarão
`periodicOrbit_apply_iterate_eq`. Registrado em `FFG-GAP-011`.

## Imports previstos

```text
Mathlib.Dynamics.PeriodicPts.Defs
Mathlib.Logic.Function.Iterate
Mathlib.Data.Fintype.Card
TamesisLab.Foundations.FiniteDynamics      (frente anterior, VERIFIED)
```

Mais, apenas nos contraexemplos:

```text
Mathlib.Data.Finset.Insert
Mathlib.Data.Fintype.Defs
```

**Nenhum import de `SimpleGraph`, `Setoid`, `Quotient`, análise, topologia
ou geometria.**

## Custo estimado por bloco

| Bloco | Custo | Base da estimativa |
|---|---|---|
| `IterReachable` + 2 teoremas | trivial | testemunhas diretas |
| `EventuallyMeets` refl/symm | trivial | testemunhas diretas |
| `EventuallyMeets` trans | **moderado** | dois casos, subtração truncada em `ℕ` |
| `componentSet` + 2 corolários | baixo | `Set.ext` mais `MEET-002/003` |
| aliases de recorrência | trivial | `Iff.rfl` |
| `FFG-REC-002` | baixo | `mk_mem_periodicPts` sobre `exists_eventual_period` |
| `FFG-CYCLE-001` | baixo | três reescritas |
| `FFG-CYCLE-002` | baixo | quatro passos |
| `FFG-MAIN-001/002` | baixo | composição |
| seis contraexemplos | moderado | tipos, `Fintype` manual, `decide` |

O único ponto de atrito real é a **transitividade de `EventuallyMeets`**.
Todo o resto é composição ou testemunha direta.

## Riscos

```yaml
- risk: subtracao truncada de N na transitividade
  severity: medium
  mitigation: "omega, e os dois casos explicitos ja escritos em THEOREM_CANDIDATES.md"

- risk: derive handler de Fintype falhar sob imports minimos
  severity: low
  mitigation: "instancias manuais, como em FOUND-SEMIGROUP-002"

- risk: homonimia de Reachable em tres niveis
  severity: medium
  mitigation: >
    IterReachable (esta frente), Reachable (FOUND-SEMIGROUP-002, sobre
    monoide) e SimpleGraph.Reachable (Mathlib, nao dirigido) sao TRES
    relacoes distintas. O nome IterReachable foi escolhido para nao
    colidir; SimpleGraph nao sera importada.

- risk: teorema principal parecer tautologico
  severity: medium
  mitigation: "argumento em COMPONENT_NOTIONS.md; STOP-009"
```

**Nenhum arquivo Lean foi criado. Nenhuma prova executada. Nenhum
`lake build` disparado.**
