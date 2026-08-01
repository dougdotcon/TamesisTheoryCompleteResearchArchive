---
document_id: ENC-LEAN-API-AUDIT
probes: 2
probes_removed: true
lake_build_executed: false
---

# Auditoria de API Lean

Dois probes descartáveis em `/tmp`, ambos exit `0` na versão final, ambos
removidos.

## APIs auditadas

```yaml
- concept: construcao do array
  exact_signature: "Array.ofFn : {α} → {n : ℕ} → (Fin n → α) → Array α"
  source_file: "Init/Data/Array/Basic.lean:331"
  classification: API_FOUND
  usable: true
  computability_notes: "computavel; #eval usado sete vezes no probe"
  axiom_notes: "[propext]"
  cast_notes: "size NAO eh sintaticamente n; ver ARRAY_SIZE_AND_CAST_POLICY"
  fallback: "Array.mk sobre List, mais custoso e sem lema de leitura direto"

- concept: tamanho
  exact_signature: "Array.size_ofFn : (Array.ofFn f).size = n"
  source_file: "Init/Data/Array/Lemmas.lean:4254"
  classification: API_FOUND
  usable: true
  axiom_notes: "[propext]"
  cast_notes: "aceito em modo TERMO por defeq; rejeitado por rw dentro de motivo dependente"
  fallback: none

- concept: leitura
  exact_signature: "Array.getElem_ofFn (h : i < (Array.ofFn f).size) : (Array.ofFn f)[i] = f ⟨i, ⋯⟩"
  source_file: "Init/Data/Array/Lemmas.lean:4282"
  classification: API_FOUND
  usable: true
  axiom_notes: "[propext, Classical.choice, Quot.sound]"
  cast_notes: >
    enunciado sobre indice Nat com prova explicita; NAO casa com getElem
    indexado por Fin sem um show intermediario
  fallback: none

- concept: transporte de indice
  exact_signature: "Fin.cast (h : n = m) (i : Fin n) : Fin m"
  source_file: nucleo
  classification: API_FOUND
  usable: true
  axiom_notes: nenhum
  cast_notes: "preserva val definicionalmente — tableIndex_val eh rfl"
  fallback: "Fin.mk explicito com a prova transportada"

- concept: limite intrinseco
  exact_signature: "Fin.isLt : ∀ (self : Fin n), ↑self < n"
  source_file: nucleo
  classification: API_FOUND
  usable: true
  axiom_notes: nenhum
  fallback: none

- concept: extensionalidade
  exact_signature: "Fin.ext : ↑a = ↑b → a = b"
  source_file: nucleo
  classification: API_FOUND
  usable: true
  cast_notes: "usado em table_step_commutes e na soundness"
  fallback: "Fin.val_injective"

- concept: injetividade por inversa a esquerda
  exact_signature: "Function.LeftInverse.injective : LeftInverse g f → Injective f"
  source_file: Mathlib/Logic/Function/Basic.lean
  classification: API_FOUND
  usable: true
  cast_notes: "decode_encode casa diretamente com LeftInverse decode encode"
  fallback: "prova manual em duas linhas"

- concept: sobrejetividade por inversa a direita
  exact_signature: "Function.RightInverse.surjective : RightInverse g f → Surjective f"
  source_file: Mathlib/Logic/Function/Basic.lean
  classification: API_FOUND
  usable: true
  fallback: none

- concept: semiconjugacao
  exact_signature: "Function.Semiconj : (α → β) → (α → α) → (β → β) → Prop"
  source_file: Mathlib/Logic/Function/Conjugate.lean
  classification: API_FOUND
  usable: true
  cast_notes: "Semiconj f ga gb significa ∀ x, f (ga x) = gb (f x) — orientacao inversa da comutacao"
  fallback: none

- concept: iteradas da semiconjugacao
  exact_signature: "Function.Semiconj.iterate_right : Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]"
  source_file: Mathlib/Logic/Function/Conjugate.lean
  classification: API_FOUND
  usable: true
  axiom_notes: "[propext]"
  cast_notes: "eh a forma exata necessaria; dispensa inducao manual"
  fallback: "inducao com Function.iterate_succ_apply, como na frente anterior"

- concept: semiconjugacao a esquerda
  exact_signature: "Function.Semiconj.iterate_left : (∀ n, Semiconj f (g n) (g (n+1))) → ∀ n k, Semiconj f^[n] (g k) (g (n+k))"
  source_file: Mathlib/Logic/Function/Conjugate.lean
  classification: API_FOUND
  usable: false
  cast_notes: "familia indexada; forma diferente da necessaria"
  fallback: none

- concept: iteracao
  exact_signature: "Nat.iterate : (α → α) → ℕ → α → α, notacao f^[n]"
  source_file: nucleo
  classification: API_FOUND
  usable: true
  cast_notes: "Function.iterate NAO existe como identificador"
  fallback: none

- concept: passo de iteracao
  exact_signature: "Function.iterate_succ_apply (f) (n) (x) : f^[n.succ] x = f^[n] (f x)"
  source_file: Mathlib/Logic/Function/Iterate.lean
  classification: API_FOUND
  usable: "nao necessario nesta frente"
  cast_notes: "a variante com apostrofo tem orientacao inversa"
  fallback: none

- concept: injetividade de some
  exact_signature: "Option.some.inj : some a = some b → a = b"
  source_file: nucleo
  classification: API_FOUND
  usable: true
  fallback: "Option.some_injective"

- concept: injetividade de ok
  exact_signature: "Except.ok.inj : Except.ok a = Except.ok b → a = b"
  source_file: nucleo
  classification: API_FOUND
  usable: "nao necessario; a soundness passa por analyzeTransitionTable_sound"
  fallback: none

- concept: exclusao de construtores de Except
  exact_signature: "Except.noConfusion"
  source_file: nucleo
  classification: PARTIAL_API
  usable: false
  cast_notes: >
    aplicacao direta falhou no probe por incompatibilidade de universo;
    simp fecha o objetivo em uma linha
  fallback: "simp"

- concept: equivalencia com Fin por Fintype
  exact_signature: "Fintype.equivFin (α) [Fintype α] : α ≃ Fin (Fintype.card α)"
  source_file: "Mathlib/Data/Fintype/EquivFin.lean:80"
  classification: API_FOUND
  usable: false
  computability_notes: NONCOMPUTAVEL
  axiom_notes: "[propext, Classical.choice, Quot.sound]"
  cast_notes: "rejeitado por decisao de desenho; STOP-ENC-006"
  fallback: "receber encode e decode como campos"

- concept: versao truncada
  exact_signature: "Fintype.truncEquivFin (α) [DecidableEq α] [Fintype α] : Trunc (α ≃ Fin (card α))"
  source_file: Mathlib/Data/Fintype/EquivFin.lean
  classification: API_FOUND
  usable: false
  computability_notes: "Trunc so elimina para Subsingleton"
  fallback: none

- concept: bijecao empacotada
  exact_signature: "Equiv, com symm_apply_apply e apply_symm_apply"
  source_file: Mathlib/Logic/Equiv/Defs.lean
  classification: API_FOUND
  usable: "OPTIONAL_DERIVED_VIEW"
  cast_notes: "toEquiv pode existir como adaptador; fora da cadeia computacional"
  fallback: none
```

## APIs de cast pesquisadas e **não** necessárias

```text
Fin.castOrderIso     nao necessario: nao ha ordem envolvida
Fin.castLE           nao necessario: o tamanho eh igual, nao menor
Fin.castLT           nao necessario
Equiv.cast           nao necessario: o transporte eh de indice, nao de tipo
cast_heq             PROIBIDO: heq nao entra na frente
```

`Fin.cast` sozinho resolve, e resolve preservando `val` por definição.
Nenhuma das quatro alternativas acrescenta algo, e `cast_heq` está
explicitamente fora.

## Nada foi assumido por memória

Todas as assinaturas acima foram lidas de `#check` ou do arquivo-fonte no
checkout. Duas suposições iniciais foram **refutadas** pelo probe: que
`Array.getElem_ofFn` casaria com índice `Fin`, e que `Except.noConfusion`
se aplicaria diretamente.


---

## Revisão — `2066edc`

Medições acrescentadas pela revisão:

```text
Array.ofFn                       [propext]
Array.size_ofFn                  [propext]
Array.getElem_ofFn               [propext, Classical.choice, Quot.sound]
Fin.cast                         NENHUM
Fin.ext                          NENHUM
Option.some.inj                  NENHUM
Function.LeftInverse.injective   NENHUM
Function.RightInverse.surjective NENHUM
Function.Semiconj.iterate_right  [propext]

ValidatedTransitionTable.step                  [propext, Quot.sound]
ValidatedTransitionTable.toRaw_valid           [propext, Quot.sound]
ValidatedTransitionTable.run?_eq_iterate_step  [propext, Quot.sound]
analyzeTransitionTable                         [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_sound                   [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_complete                [propext, Classical.choice, Quot.sound]
```

`Array.size_ofFn` e `Array.getElem_ofFn` continuam **inacessíveis por
`rfl`** para `n` genérico; passam apenas com tamanho literal.
