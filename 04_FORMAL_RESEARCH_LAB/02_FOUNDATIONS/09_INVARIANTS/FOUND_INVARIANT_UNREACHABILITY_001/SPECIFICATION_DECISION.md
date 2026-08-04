---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-SPECIFICATION-DECISION
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
signatures_frozen: true
public_declarations: 8
test_only_declarations: 2
typeclasses_required: 0
requires_fintype_concrete: false
requires_decidable_eq_concrete: false
probe_exit: 0
---

# Decisão de especificação — assinaturas congeladas

Todas as assinaturas abaixo **já compilaram** em probe descartável, com
`exit 0` e árvore versionada intocada. Congelá-las não é aposta.

## Módulos

```text
Foundations/Invariants/Definitions.lean     Invariant, Reachable, a ponte
Foundations/Invariants/Unreachability.lean  a ferramenta e a composicao
Foundations/Invariants/CollapseLimit.lean   o teorema negativo
Foundations/Invariants/Instance.lean        TEST_ONLY, a instancia infinita
```

## As oito declarações públicas

### Definitions.lean

```lean
def Invariant (abstract : C → A) (stepC : C → C) : Prop :=
  ∀ c : C, abstract (stepC c) = abstract c

theorem Invariant.semiconj (h : Invariant abstract stepC) :
    Function.Semiconj abstract stepC id

theorem Invariant.iterate (h : Invariant abstract stepC) (k : Nat) (c : C) :
    abstract ((stepC^[k]) c) = abstract c

def Reachable (stepC : C → C) (x y : C) : Prop := ∃ k : Nat, (stepC^[k]) x = y
```

`Invariant.semiconj` é o termo `h`. Está exposto porque a ponte
definicional é o conteúdo da frente, não um detalhe de implementação.

### Unreachability.lean

```lean
theorem unreachable_of_invariant_ne (h : Invariant abstract stepC)
    (hne : abstract x ≠ abstract y) : ¬ Reachable stepC x y

theorem Invariant.pair (hf : Invariant f stepC) (hg : Invariant g stepC) :
    Invariant (fun c => (f c, g c)) stepC

def invariantAbstraction (h : Invariant abstract stepC) :
    CertifiedFiniteAbstraction C A stepC id
```

### CollapseLimit.lean

```lean
theorem invariant_orbitSeparating_iff_fixedPoint
    (h : Invariant abstract stepC) (start : C) :
    OrbitSeparating abstract stepC start ↔ stepC start = start
```

**A declaração central da frente.** É a única que consome a frente
anterior, e a única que produz um resultado negativo.

## As duas TEST_ONLY, residentes na biblioteca

```lean
def diagStep (p : Int × Int) : Int × Int := (p.1 + 1, p.2 + 1)

theorem diagStep_invariant :
    Invariant (fun p : Int × Int => p.1 - p.2) diagStep
```

Residentes porque `diag_unreachable`, que é teste, as consome. Segue o
precedente de `FiniteStateAbstraction/Counterexample.lean`. Declarado
aqui em vez de escondido na contagem.

## Os testes

```lean
theorem diag_unreachable : ¬ Reachable diagStep (0, 0) (1, 0)

theorem constant_invariant_proves_nothing (stepC : C → C) :
    Invariant (fun _ : C => ()) stepC
```

## Recorte, declarado antes da formalização

```text
determinismo         stepC e funcao TOTAL, como em toda a cadeia
finitude de C        NAO exigida, NAO obtida, NAO mencionada
finitude de A        NAO exigida
DecidableEq          NAO exigida em declaracao nenhuma
Fintype              NAO exigido em declaracao nenhuma
typeclasses          ZERO no nucleo
```

`Int × Int` na instância é escolha deliberada: um tipo **infinito** em
ambas as coordenadas, para que ninguém leia a ferramenta como dependente
de finitude.

## O que NÃO é afirmado

```text
que invariante separador seja NECESSARIO para inalcancabilidade
que exista invariante separador quando ha inalcancabilidade
que a ferramenta decida inalcancabilidade
que invariantes formem reticulado, algebra ou categoria
que exista invariante completo ou universal
que invariantes tenham qualquer relacao com Clay, TOE, fisica ou Riemann
```

## Pegada axiomática esperada

```text
Invariant.iterate                        propext
unreachable_of_invariant_ne              propext
invariant_orbitSeparating_iff_fixedPoint propext, Quot.sound
diag_unreachable                         propext, Quot.sound
```

Medida em probe. `Classical.choice` **não** aparece: a frente não
atravessa `analyzeEncodedSystem`, não há `Array`, tabela nem execução.

## Por que a frente não é extensão da anterior

`FOUND-FINITE-STATE-ABSTRACTION-001` permanece `extension_status:
NOT_AUTHORIZED`. Esta frente **consome** `OrbitSeparating` e
`CertifiedFiniteAbstraction` como API verificada, em namespace novo, sem
tocar em nenhum arquivo daquela frente. É o mesmo padrão das nove
transições anteriores da cadeia.
