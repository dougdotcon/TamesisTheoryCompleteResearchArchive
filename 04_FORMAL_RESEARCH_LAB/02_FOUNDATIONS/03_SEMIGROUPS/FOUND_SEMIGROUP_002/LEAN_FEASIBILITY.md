---
document_id: FSG2-LEAN-FEASIBILITY
mathlib_rev: 79d0395a1825a6264ad5d269e35e60537518955e
mathlib_tag: v4.33.0-rc1
method: leitura direta das fontes no checkout fixado (rg/grep + sed)
proofs_executed: 0
lean_files_created: 0
builds_executed: 0
---

# FOUND-SEMIGROUP-002 — Viabilidade Lean

Todos os nomes abaixo foram **lidos na fonte**, não presumidos. Cada linha
traz arquivo e assinatura literal.

```yaml
- concept: orbita de uma acao
  candidate_api: MulAction.orbit
  source_file: Mathlib/GroupTheory/GroupAction/Defs.lean:49
  signature: "def orbit (a : α) := Set.range fun m : γ => m • a"
  reusable: true
  limitations: >
    Devolve Set α, nao Finset. Requer [Monoid M] [MulAction M α] no
    contexto declarado no arquivo.
  fallback_local_definition: nenhum necessario
  classification: API_FOUND

- concept: ponte alcancabilidade <-> orbita
  candidate_api: MulAction.mem_orbit_iff
  source_file: Mathlib/GroupTheory/GroupAction/Defs.lean
  signature: "theorem mem_orbit_iff {a₁ a₂ : α} : a₂ ∈ orbit γ a₁ ↔ ∃ x : γ, x • a₁ = a₂ := Iff.rfl"
  reusable: true
  limitations: nenhuma
  note: >
    Eh literalmente Iff.rfl. FSG2-ORBIT-001 deve custar zero.
  classification: API_FOUND

- concept: reflexividade da alcancabilidade
  candidate_api: MulAction.mem_orbit_self
  source_file: Mathlib/GroupTheory/GroupAction/Defs.lean
  signature: "theorem mem_orbit_self (a : α) : a ∈ orbit M a := ⟨1, by simp⟩"
  reusable: true
  classification: API_FOUND

- concept: fechamento da orbita sob a acao
  candidate_api: MulAction.mem_orbit_of_mem_orbit
  source_file: Mathlib/GroupTheory/GroupAction/Defs.lean
  signature: "theorem mem_orbit_of_mem_orbit (m : M) (h : a₂ ∈ orbit M a₁) : m • a₂ ∈ orbit M a₁"
  reusable: true
  limitations: >
    Nao eh exatamente a transitividade de Reachable; eh o caso particular
    em que o segundo passo eh um unico elemento. FSG2-REACH-002 continua
    sendo um enunciado proprio, provado por mul_smul.
  classification: PARTIAL_API

- concept: identidade iteracao <-> potencia da acao
  candidate_api: smul_iterate / smul_iterate_apply
  source_file: Mathlib/Algebra/Group/Action/Defs.lean:432,437
  signature: |
    theorem smul_iterate (a : M) : ∀ n : ℕ, (a • · : α → α)^[n] = (a ^ n • ·)
    lemma smul_iterate_apply (a : M) (n : ℕ) (x : α) : (a • ·)^[n] x = a ^ n • x
  reusable: true
  limitations: nenhuma
  note: >
    RESOLVE FSG2-GAP-003 integralmente. A especificacao previa que este
    lema poderia nao existir; ele existe, com o nome smul_iterate_apply.
  classification: API_FOUND

- concept: principio da casa dos pombos (Fintype)
  candidate_api: Fintype.exists_ne_map_eq_of_card_lt
  source_file: Mathlib/Data/Fintype/Pigeonhole.lean:~44
  signature: >
    theorem exists_ne_map_eq_of_card_lt (f : α → β)
      (h : Fintype.card β < Fintype.card α) : ∃ x y, x ≠ y ∧ f x = f y
  reusable: true
  limitations: >
    Devolve x ≠ y, NAO x < y. A ordenacao dos indices fica por conta da
    prova local (lt_or_gt_of_ne). Exige [Fintype α] [Fintype β].
  classification: API_FOUND

- concept: pigeonhole com limitantes explicitos
  candidate_api: Finset.exists_ne_map_eq_of_card_lt_of_maps_to
  source_file: Mathlib/Data/Finset/Card.lean:451
  signature: >
    theorem exists_ne_map_eq_of_card_lt_of_maps_to (hc : #t < #s)
      {f : α → β} (hf : Set.MapsTo f s t) : ∃ x ∈ s, ∃ y ∈ s, x ≠ y ∧ f x = f y
  reusable: true
  limitations: >
    Alternativa a versao Fintype quando se quiser trabalhar com
    Finset.range (card X + 1) em vez de Fin (card X + 1). A escolha entre
    as duas fica para a execucao; ambas dao os mesmos limitantes.
  classification: API_FOUND

- concept: ponto periodico
  candidate_api: Function.IsPeriodicPt
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:62
  signature: "def IsPeriodicPt (f : α → α) (n : ℕ) (x : α) := IsFixedPt f^[n] x"
  reusable: true
  limitations: >
    Eh periodicidade DESDE n = 0 (f^[n] x = x), nao periodicidade
    eventual. Serve para FSG2-PER-004, aplicada ao ponto f^[mu] x, NAO a x.
  classification: API_FOUND

- concept: ponto fixo
  candidate_api: Function.IsFixedPt
  source_file: Mathlib/Logic/Function/Defs.lean:173
  signature: "def IsFixedPt (f : α → α) (x : α) := f x = x"
  reusable: true
  classification: API_FOUND

- concept: periodo minimal
  candidate_api: Function.minimalPeriod
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:245
  signature: >
    def minimalPeriod (f : α → α) (x : α) :=
      if h : x ∈ periodicPts f then Nat.find h else 0
  reusable: false
  limitations: >
    ARMADILHA. Devolve 0 quando x nao eh periodico. Num sistema com cauda
    (CE-003) o estado inicial nao eh periodico e minimalPeriod devolve 0.
    NAO usar como "periodo eventual". Ver FSG2-GAP-002b.
  fallback_local_definition: >
    O periodo eventual sai de FSG2-PER-002; a conexao com a API oficial eh
    FSG2-PER-004, aplicada ao ponto f^[mu] x.
  classification: PARTIAL_API

- concept: periodo de uma acao de monoide
  candidate_api: MulAction.period
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:~552
  signature: "noncomputable def period (m : M) (a : α) : ℕ := minimalPeriod (fun x => m • x) a"
  reusable: false
  limitations: >
    Herda a mesma armadilha de minimalPeriod: devolve 0 fora do conjunto
    periodicPts. Util apenas quando ja se sabe que o ponto eh periodico.
  classification: PARTIAL_API

- concept: periodicidade eventual / preperiodicidade
  candidate_api: null
  source_file: null
  signature: null
  reusable: false
  limitations: >
    Busca por "preperiodic", "eventuallyPeriodic" e "eventually_periodic"
    em todo o Mathlib do checkout fixado: ZERO ocorrencias.
  fallback_local_definition: >
    O enunciado FSG2-PER-002 sera local. Ele eh curto e nao exige teoria
    nova: pigeonhole + aritmetica de indices.
  classification: NOT_FOUND

- concept: decomposicao cauda + ciclo
  candidate_api: Function.periodicOrbit / Function.periodicPts
  source_file: Mathlib/Dynamics/PeriodicPts/Defs.lean:199,401
  signature: |
    def periodicPts (f : α → α) : Set α := ...
    def periodicOrbit (f : α → α) (x : α) : Cycle α := ...
  reusable: parcial
  limitations: >
    Descrevem a orbita de pontos JA periodicos. Nao ha API para a cauda
    nem para a unicidade do par (mu, lam). Nao auditado em profundidade
    neste gate.
  classification: NAME_UNCERTAIN

- concept: aritmetica de iteracao
  candidate_api: Function.iterate_add_apply
  source_file: usado em Mathlib/Order/Hom/Order.lean:138 e outros
  signature: "f^[m + n] x = f^[m] (f^[n] x)"
  reusable: true
  limitations: >
    A declaracao esta em Lean core / Batteries, nao no corpo do Mathlib;
    confirmada apenas pelos USOS no Mathlib, nao pela declaracao original.
    A assinatura acima eh a forma usada nesses call sites.
  classification: NAME_UNCERTAIN
```

## Resumo

| Classificação | Itens |
|---|---|
| `API_FOUND` | 8 |
| `PARTIAL_API` | 3 |
| `NOT_FOUND` | 1 |
| `NAME_UNCERTAIN` | 2 |

## Conclusão de viabilidade

O único item `NOT_FOUND` é o próprio alvo — e isso é esperado, não um
bloqueio: a periodicidade eventual não está na Mathlib porque é um
enunciado curto que cada projeto formula à sua maneira. A prova depende de
`Fintype.exists_ne_map_eq_of_card_lt` e de aritmética de índices, ambas
disponíveis.

**Nenhum arquivo Lean foi criado. Nenhuma prova foi executada. Nenhum
`lake build` foi disparado neste gate.**

Os dois itens `NAME_UNCERTAIN` devem ser confirmados por `#check` no
primeiro arquivo da execução, antes de qualquer prova depender deles.
