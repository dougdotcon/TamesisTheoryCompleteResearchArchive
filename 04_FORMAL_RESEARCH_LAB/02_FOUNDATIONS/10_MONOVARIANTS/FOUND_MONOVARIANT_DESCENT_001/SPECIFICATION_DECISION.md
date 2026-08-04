---
document_id: FOUND-MONOVARIANT-DESCENT-001-SPECIFICATION-DECISION
work_item_id: FOUND-MONOVARIANT-DESCENT-001
signatures_frozen: true
public_declarations: 7
private_helpers: 1
test_only_declarations: 2
tests: 2
typeclasses_required: 0
measure_codomain: Nat
probe_exit: 0
---

# Decisão de especificação — assinaturas congeladas

Todas já compilaram em probe descartável, `exit 0`, árvore intocada.

## Módulos

```text
Foundations/Monovariants/Definitions.lean      Monovariant e a descida
Foundations/Monovariants/WitnessBounds.lean    recuperacao de 0 < period
Foundations/Monovariants/ReflectionLimit.lean  o teorema negativo
Foundations/Monovariants/Instance.lean         TEST_ONLY, as duas negacoes
```

## As sete públicas

### Definitions.lean — 1 definição, 3 teoremas

```lean
def Monovariant (measure : C → Nat) (stepC : C → C) : Prop :=
  ∀ c : C, measure (stepC c) < measure c

theorem Monovariant.iterate_lt (h : Monovariant measure stepC) :
    ∀ k : Nat, 0 < k → ∀ c : C, measure ((stepC^[k]) c) < measure c

theorem Monovariant.no_periodic_point (h : Monovariant measure stepC)
    (hk : 0 < k) (c : C) : (stepC^[k]) c ≠ c

theorem Monovariant.not_reachable_self (h : Monovariant measure stepC) (c : C) :
    ¬ ∃ k : Nat, 0 < k ∧ (stepC^[k]) c = c
```

### WitnessBounds.lean — 2 teoremas, 1 auxiliar privado

```lean
theorem analyzeTransitionTable_period_pos
    (h : analyzeTransitionTable raw start = .ok w) : 0 < w.period

theorem analyzeAbstractSystem_period_pos
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    0 < witness.period
```

O auxiliar `reduce'` é **privado** e reproduz, com API exclusivamente
pública, a redução que `FiniteStateRuntime` mantém privada. Reproduzir
uma redução de cinco linhas **não** é reimplementar o detector, e a
duplicação está declarada aqui em vez de escondida.

### ReflectionLimit.lean — 1 teorema

```lean
theorem monovariant_not_orbitSeparating
    (hmono : Monovariant measure stepC)
    (h : analyzeAbstractSystem abstraction encoding start = .ok witness) :
    ¬ OrbitSeparating abstraction.abstract stepC start
```

**A declaração central.** Nenhuma hipótese que o consumidor precise
inventar: `0 < period` vem de `WitnessBounds.lean`.

## As duas TEST_ONLY e os dois testes

```lean
def downStep (p : Nat × Nat) : Nat × Nat := (p.1 + 1, p.2 + 1)
def strictDown (k : Nat) : Nat := k - 1

theorem downStep_not_monovariant :
    ¬ Monovariant (fun p : Nat × Nat => p.1) downStep
theorem strictDown_not_monovariant :
    ¬ Monovariant (fun k : Nat => k) strictDown
```

`strictDown_not_monovariant` é o registro que importa: `Nat` é bem
fundado e ainda assim `k - 1` **não** é monovariante, porque falha em
zero. **Boa fundação do contradomínio não substitui decrescimento
estrito.**

## Contagem congelada

```text
publicas             7   (1 definicao, 6 teoremas)
auxiliar privado     1
TEST_ONLY residentes 2   (definicoes)
testes               2   (teoremas)
```

## Recorte

```text
medida               Nat, e so Nat
ordens gerais        NAO AUTORIZADAS
WellFoundedRelation  NAO AUTORIZADO
ordinais             NAO AUTORIZADOS
finitude de C        NAO exigida
typeclasses          ZERO
```

## Pegada esperada

```text
Monovariant.iterate_lt            propext, Quot.sound
Monovariant.no_periodic_point     propext, Quot.sound
analyzeAbstractSystem_period_pos  propext, Classical.choice, Quot.sound
monovariant_not_orbitSeparating   propext, Classical.choice, Quot.sound
```

`Classical.choice` entra **apenas** no que atravessa
`analyzeEncodedSystem` — pegada infraestrutural já aceita, cuja remoção é
explicitamente proibida.

## O que NÃO é afirmado

```text
que monovariante seja NECESSARIO para ausencia de ciclo
que boa fundacao baste
que a ferramenta decida qualquer coisa
que exista monovariante quando nao ha ciclo
terminacao de programas, ordinais, sistemas nao deterministicos
```
