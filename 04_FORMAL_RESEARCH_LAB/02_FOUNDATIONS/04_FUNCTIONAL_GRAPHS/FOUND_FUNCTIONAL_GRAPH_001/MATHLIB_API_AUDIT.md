---
document_id: FFG-MATHLIB-API-AUDIT
mathlib_tag: v4.33.0-rc1
mathlib_rev: 79d0395a1825a6264ad5d269e35e60537518955e
method: leitura direta das fontes no checkout fixado
lean_files_created: 0
builds_executed: 0
---

# FOUND-FUNCTIONAL-GRAPH-001 — Auditoria da API Mathlib

Todos os nomes abaixo foram **lidos na fonte**, com arquivo e linha.
Nenhum foi presumido.

```yaml
- concept: conjunto de pontos periodicos
  candidate_api: Function.periodicPts
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:198
  exact_signature: "def periodicPts (f : α → α) : Set α := { x | ∃ n > 0, IsPeriodicPt f n x }"
  revision_checked: 79d0395a
  classification: API_FOUND
  reusable: true
  limitations: >
    Nenhuma. O periodo positivo eh exigido PELA DEFINICAO, o que resolve
    diretamente a armadilha de "∃ n, f^[n] x = x" com n = 0.
  fallback: nao necessario

- concept: pertinencia a periodicPts
  candidate_api: Function.mem_periodicPts
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:205
  exact_signature: "theorem mem_periodicPts : x ∈ periodicPts f ↔ ∃ n > 0, IsPeriodicPt f n x := Iff.rfl"
  classification: API_FOUND
  reusable: true

- concept: construtor de pertinencia a periodicPts
  candidate_api: Function.mk_mem_periodicPts
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:202
  exact_signature: "theorem mk_mem_periodicPts (hn : 0 < n) (hx : IsPeriodicPt f n x) : x ∈ periodicPts f"
  classification: API_FOUND
  reusable: true
  limitations: nenhuma
  note: >
    Eh EXATAMENTE o adaptador de exists_eventual_period para periodicPts:
    consome 0 < lam e IsPeriodicPt f lam (f^[mu] x).

- concept: ponto periodico
  candidate_api: Function.IsPeriodicPt
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:62
  exact_signature: "def IsPeriodicPt (f : α → α) (n : ℕ) (x : α) := IsFixedPt f^[n] x"
  classification: API_FOUND
  reusable: true
  limitations: >
    NAO exige n > 0 por si so. Por isso a fonte de "recorrente" eh
    periodicPts, e nao IsPeriodicPt isolada.

- concept: orbita periodica como ciclo
  candidate_api: Function.periodicOrbit
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:401
  exact_signature: "def periodicOrbit (f : α → α) (x : α) : Cycle α := (List.range (minimalPeriod f x)).map fun n => f^[n] x"
  classification: API_FOUND
  reusable: true
  limitations: >
    (1) NAO exige DecidableEq α — confirmado pelo bloco de variaveis
        {α : Type*} {f : α → α} da linha 57.
    (2) Esta dentro de `noncomputable section` (linhas 240-490), logo eh
        NONCOMPUTAVEL. Consequencia pratica: `decide` NAO pode ser usado
        em enunciados sobre igualdade de orbitas. Ver FFG-GAP-011.
    (3) Devolve Cycle.nil para pontos nao periodicos — por isso todos os
        lemas uteis carregam a hipotese `hx : x ∈ periodicPts f`.
  fallback: nao necessario

- concept: invariancia da orbita ao avancar por iteradas
  candidate_api: Function.periodicOrbit_apply_iterate_eq
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:~466
  exact_signature: "theorem periodicOrbit_apply_iterate_eq (hx : x ∈ periodicPts f) (n : ℕ) : periodicOrbit f (f^[n] x) = periodicOrbit f x"
  classification: API_FOUND
  reusable: true
  limitations: nenhuma
  note: >
    LEMA CENTRAL de FFG-CYCLE-001. Permite provar a unicidade da orbita em
    tres passos, SEM aritmetica modular.

- concept: caracterizacao dos membros da orbita
  candidate_api: Function.mem_periodicOrbit_iff
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:429
  exact_signature: "theorem mem_periodicOrbit_iff (hx : x ∈ periodicPts f) : y ∈ periodicOrbit f x ↔ ∃ n, f^[n] x = y"
  classification: API_FOUND
  reusable: true
  note: >
    O lado direito eh LITERALMENTE IterReachable f x y. Base de
    FFG-CYCLE-002.

- concept: o proprio ponto pertence a sua orbita
  candidate_api: Function.self_mem_periodicOrbit
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:445
  exact_signature: "theorem self_mem_periodicOrbit (hx : x ∈ periodicPts f) : x ∈ periodicOrbit f x"
  classification: API_FOUND
  reusable: true

- concept: orbita vazia fora de periodicPts
  candidate_api: Function.periodicOrbit_eq_nil_iff_not_periodic_pt
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:~424
  exact_signature: "theorem periodicOrbit_eq_nil_iff_not_periodic_pt : periodicOrbit f x = Cycle.nil ↔ x ∉ periodicPts f"
  classification: API_FOUND
  reusable: true
  note: "util para separar transitorios de recorrentes nos contraexemplos"

- concept: comprimento da orbita
  candidate_api: Function.periodicOrbit_length
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:~415
  exact_signature: "theorem periodicOrbit_length : (periodicOrbit f x).length = minimalPeriod f x"
  classification: API_FOUND
  reusable: parcial
  limitations: >
    Traz minimalPeriod de volta. Util em FFG-CE-006 (mesmo periodo,
    componentes diferentes), NAO no nucleo.

- concept: periodo minimal
  candidate_api: Function.minimalPeriod
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:245
  exact_signature: "def minimalPeriod (f : α → α) (x : α) := if h : x ∈ periodicPts f then Nat.find h else 0"
  classification: PARTIAL_API
  reusable: false_in_core
  limitations: >
    Devolve 0 fora de periodicPts — mesma armadilha ja registrada em
    FSG2-GAP-002b. NAO usar como "periodo" no nucleo. Aparece apenas
    indiretamente, dentro da definicao de periodicOrbit.

- concept: positividade do periodo minimal
  candidate_api: Function.minimalPeriod_pos_iff_mem_periodicPts
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:280
  exact_signature: "theorem minimalPeriod_pos_iff_mem_periodicPts : 0 < minimalPeriod f x ↔ x ∈ periodicPts f"
  classification: API_FOUND
  reusable: parcial
  note: "ponte segura para minimalPeriod quando ela for necessaria"

- concept: aritmetica de iteracao
  candidate_api: Function.iterate_add_apply
  source_file: Mathlib/Logic/Function/Iterate.lean:76
  exact_signature: "theorem iterate_add_apply (m n : ℕ) (x : α) : f^[m + n] x = f^[m] (f^[n] x)"
  classification: API_FOUND
  reusable: true
  note: >
    Ja localizado e usado em FOUND-SEMIGROUP-002; o NAME_UNCERTAIN daquela
    frente esta definitivamente fechado.

- concept: comutacao de iteradas
  candidate_api: Function.iterate_comm
  source_file: Mathlib/Logic/Function/Iterate.lean:208
  exact_signature: "theorem iterate_comm (f : α → α) (m n : ℕ) : f^[n]^[m] = f^[m]^[n]"
  classification: NOT_NEEDED_IN_CORE
  limitations: >
    Trata de iterada de iterada, nao de f^[m+n]. Nao eh o lema que a
    transitividade precisa — esse eh iterate_add_apply.

- concept: iteracao de funcoes que comutam
  candidate_api: Function.iterate_iterate
  source_file: Mathlib/Logic/Function/Iterate.lean:137
  exact_signature: "theorem iterate_iterate (h : Commute f g) (m n : ℕ) : Commute f^[m] g^[n]"
  classification: NOT_NEEDED_IN_CORE
  note: "o nome sugere composicao de iteradas, mas o conteudo eh sobre Commute"

- concept: tipo ciclo
  candidate_api: Cycle
  source_file: Mathlib/Data/List/Cycle.lean:406
  exact_signature: "def Cycle (α : Type*) : Type _ := Quotient (IsRotated.setoid α)"
  classification: API_FOUND
  reusable: true
  limitations: >
    Igualdade a menos de ROTACAO — exatamente a propriedade desejada.
    DecidableEq (Cycle α) existe apenas com [DecidableEq α]
    (Cycle.lean:482); no nucleo isso NAO eh necessario, pois nenhuma
    igualdade de ciclos precisa ser DECIDIDA, apenas provada.

- concept: grafo simples
  candidate_api: SimpleGraph
  source_file: Mathlib/Combinatorics/SimpleGraph/Basic.lean:93
  exact_signature: "structure SimpleGraph (V : Type u) where"
  classification: DEFERRED_TO_GRAPH_BRIDGE
  reusable: false_in_core
  limitations: "eh NAO DIRIGIDO; ver COMPONENT_NOTIONS.md"

- concept: alcancabilidade em grafo simples
  candidate_api: SimpleGraph.Reachable
  source_file: Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean:52
  exact_signature: "def Reachable (u v : V) : Prop := Nonempty (G.Walk u v)"
  classification: DEFERRED_TO_GRAPH_BRIDGE
  limitations: >
    Homonimo perigoso: NAO eh o IterReachable desta frente nem o Reachable
    de FOUND-SEMIGROUP-002. Tres relacoes distintas com nomes parecidos.

- concept: componente conexa
  candidate_api: SimpleGraph.ConnectedComponent
  source_file: Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean:390
  exact_signature: "def ConnectedComponent := Quot G.Reachable"
  classification: DEFERRED_TO_GRAPH_BRIDGE

- concept: relacao de equivalencia empacotada
  candidate_api: Setoid
  source_file: Mathlib/Data/Setoid/Basic.lean
  classification: NOT_NEEDED_IN_CORE
  limitations: >
    EventuallyMeets depende de f, que nao aparece no tipo X. Uma instancia
    Setoid seria o mesmo erro que FSG2-GAP-006 evitou com Preorder.
    Os tres teoremas MEET-001/002/003 bastam.

- concept: quociente por equivalencia
  candidate_api: Quotient
  classification: NOT_NEEDED_IN_CORE
  note: "contagem de componentes eh explicitamente DEFERRED"
```

## Resumo

| Classificação | Itens |
|---|---|
| `API_FOUND` | 12 |
| `PARTIAL_API` | 1 |
| `NOT_FOUND` | **0** |
| `NAME_UNCERTAIN` | **0** |
| `NOT_NEEDED_IN_CORE` | 4 |
| `DEFERRED_TO_GRAPH_BRIDGE` | 3 |

## Conclusão de viabilidade

**Nenhum item `NOT_FOUND`.** Ao contrário de `FOUND-SEMIGROUP-002`, onde o
alvo (periodicidade eventual) não existia na Mathlib e teve de ser
enunciado localmente, aqui **toda a maquinaria de ciclos já existe**. O
trabalho da frente é conectá-la a `EventuallyMeets` e ao resultado já
verificado da frente anterior.

Três achados que mudam a especificação:

1. **`periodicOrbit` não exige `DecidableEq`** — o núcleo deve precisar
   apenas de `[Fintype X]`. Ver `LEAN_FEASIBILITY.md`.
2. **`periodicOrbit` é noncomputável** — `decide` está indisponível para
   igualdade de órbitas nos contraexemplos. `FFG-GAP-011`.
3. **`periodicOrbit_apply_iterate_eq` dá `FFG-CYCLE-001` em três passos**,
   sem aritmética modular.
