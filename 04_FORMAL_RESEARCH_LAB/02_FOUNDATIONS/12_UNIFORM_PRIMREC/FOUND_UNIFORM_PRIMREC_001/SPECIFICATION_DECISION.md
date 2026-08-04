---
document_id: FOUND-UNIFORM-PRIMREC-001-SPECIFICATION-DECISION
work_item_id: FOUND-UNIFORM-PRIMREC-001
signatures_frozen: true
public_declarations: 31
public_definitions: 4
public_theorems: 27
private_helpers: 1
test_only_declarations: 1
tests: 3
declarations_total: 36
count_source: DERIVED_BY_SCRIPT
typeclasses_required: 0
instance_declarations: 0
probe_exit: 0
probe_error_lines: 0
versioned_tree_touched: false
---

# Decisao de especificacao — assinaturas congeladas

Todas compilaram em probe descartavel, `exit 0`, `0` linhas `error:`,
arvore versionada intocada (`git_dirty=0`).

## Modulos

```text
Foundations/UniformPrimrec/Execution.lean    10 publicas
Foundations/UniformPrimrec/Validity.lean      4 publicas
Foundations/UniformPrimrec/Candidates.lean    2 publicas
Foundations/UniformPrimrec/Witness.lean       6 publicas
Foundations/UniformPrimrec/Analysis.lean      9 publicas + 1 privada
Foundations/UniformPrimrec/Instance.lean      1 TEST_ONLY
Foundations/UniformPrimrec.lean               agregador
```

## Execution.lean — a peca que destravou tudo

```lean
theorem primrec_next_toList : Primrec fun t : RawTransitionTable => t.next.toList
theorem primrec_size : Primrec fun t : RawTransitionTable => t.next.size
theorem primrec_witness_pair : Primrec fun w : CycleWitness => (w.baseIndex, w.period)
theorem primrec_baseIndex : Primrec CycleWitness.baseIndex
theorem primrec_period : Primrec CycleWitness.period
theorem primrec_mk : Primrec2 fun b p : Nat => (mk b p : CycleWitness)
theorem primrec_step? : Primrec2 RawTransitionTable.step?
theorem iterate_bind_none (f : Nat -> Option Nat) (k : Nat) :
    (fun o : Option Nat => o.bind f)^[k] none = none
theorem run?_eq_iterate (t : RawTransitionTable) (k state : Nat) :
    t.run? k state = (fun o : Option Nat => o.bind t.step?)^[k] (some state)
theorem primrec_run?_gen {ft fk fs} (ht) (hk) (hs) :
    Primrec fun a => (ft a).run? (fk a) (fs a)
```

`run?_eq_iterate` e **a declaracao central da frente**. Ela reescreve uma
recursao com `Option` como uma iterada, e e o que permite
`Primrec.nat_iterate`. Sem ela nao ha frente.

`primrec_run?_gen` e generica no argumento de entrada de proposito: ela e
aplicada tres vezes em `Analysis.lean` com projecoes diferentes.

## Validity.lean

```lean
def validBool (raw : RawTransitionTable) : Bool
theorem foldr_lt_eq_true (n : Nat) : forall l : List Nat, ...
theorem validBool_iff (raw) : validBool raw = true <-> raw.Valid
theorem primrec_validBool : Primrec validBool
```

`validBool` usa `if` e nao `decide` **de proposito**: `PrimrecPred`
carrega a sua propria instancia de `DecidablePred`, e misturar as duas
formas produz incompatibilidade de instancia que nenhuma tatica resolve.
Registrado em `STOP-UP-005`.

## Candidates.lean

```lean
theorem flatMap_eq_foldr (f : α -> List β) (l : List α) :
    l.flatMap f = l.foldr (fun a acc => f a ++ acc) []
theorem primrec_cycleCandidates : Primrec cycleCandidates
```

O Mathlib nao oferece `Primrec` de `flatMap`; oferece de `foldr`. A ponte
de uma linha entre os dois esta aqui.

## Witness.lean — o casamento

```lean
def RawValid (raw : RawTransitionTable) (start : Nat) (w : CycleWitness) : Prop
def rawValidBool (raw : RawTransitionTable) (start : Nat) (w : CycleWitness) : Bool
theorem rawValidBool_iff : rawValidBool raw start w = true <-> RawValid raw start w
theorem primrec_rawValidBool : Primrec fun q => rawValidBool q.1.1 q.1.2 q.2
theorem valid_iff_rawValid (t) (start : Fin t.next.size) (w) :
    CycleWitness.Valid t.step start w <-> RawValid t.toRaw start w
theorem detectCycle?_eq_raw (t) (start : Fin t.next.size) :
    t.detectCycle? start
      = (cycleCandidates t.next.size).find? (fun w => rawValidBool t.toRaw start w)
```

`RawValid` tem as **mesmas quatro clausulas, na mesma ordem e no mesmo
aninhamento** de `CycleWitness.Valid`. E isso que torna
`valid_iff_rawValid` um transporte e nao uma prova nova.

## Analysis.lean — o fechamento

```lean
def analyzeRaw (raw : RawTransitionTable) (start : Nat) :
    Except RuntimeCycleError CycleWitness
theorem analyzeRaw_eq (raw) (start) :
    analyzeRaw raw start = analyzeTransitionTable raw start
theorem primrec_ok, primrec_error, primrec_initialStateOutOfBounds
theorem primrec_find
theorem primrec_analyzeRaw : Primrec2 analyzeRaw
theorem primrec_analyzeTransitionTable : Primrec2 analyzeTransitionTable
theorem uniformPrimrecStatement_holds : UniformPrimrecStatement
```

`analyze_reduce_u` e o auxiliar **privado**, e e a **quarta** ocorrencia
da reducao do bloco `do`. Declarada, nao escondida — `UP-GAP-002`.

`uniformPrimrecStatement_holds` fecha, por nome, o `def : Prop` que a
ponte deixou registrado sem prova.

## Instance.lean e os 3 testes

```lean
def twoCycle : RawTransitionTable := (mk #[1, 0])          TEST_ONLY
theorem twoCycle_valid : twoCycle.Valid
theorem twoCycle_analysis : analyzeTransitionTable twoCycle 0 = .ok (mk 0 2)
theorem twoCycle_analyzeRaw : analyzeRaw twoCycle 0 = .ok (mk 0 2)
```

Instancia positiva **por avaliacao**: tabela habitada, `size = 2`, os dois
lados do casamento avaliados concretamente e coincidindo.

## Contagem congelada

```text
publicas             31   (4 definicoes, 27 teoremas)
auxiliar privado      1
TEST_ONLY residente   1
testes                3
total                36
```

Derivada por script sobre o probe, com particao conferida.

## Pegada esperada

```text
todas   propext, Classical.choice, Quot.sound
```

Pegada infraestrutural do Mathlib, ja aceita, cuja remocao e proibida.

## O que NAO e afirmado

```text
que exista modelo de custo
que Primrec signifique eficiente
que classe de complexidade esteja definida
que P vs NP tenha sido tocado
```
