---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-BOOL-TO-UNIT
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
category: TEST_ONLY
naive_cycle_reflection: FALSE
counterexample_orbit_separating: FALSE
---

# Contraexemplo `BOOL_TO_UNIT`

## Os três objetos

```lean
def concreteStep : Bool → Bool :=
  Bool.not

def abstractStep : Unit → Unit :=
  id

def forgetBool : Bool → Unit :=
  fun _ => ()
```

## A semiconjugação vale

```lean
example :
    Function.Semiconj
      forgetBool
      concreteStep
      abstractStep := by
  intro b
  cases b <;> rfl
```

Sem axiomas.

## A recorrência abstrata vale

```lean
example :
    forgetBool (concreteStep false) =
      forgetBool false := by
  rfl
```

Período abstrato `1`.

## A recorrência concreta NÃO vale

```lean
example :
    concreteStep false ≠ false := by
  decide
```

## A codificação explícita

```lean
def unitEncoding : CertifiedFiniteEncoding Unit 1 where
  encode := fun _ => ⟨0, by decide⟩
  decode := fun _ => ()
  decode_encode := fun _ => rfl
  encode_decode := by decide
```

Sem axiomas.

## A análise abstrata executa

```lean
example :
    analyzeAbstractSystem
      boolToUnitAbstraction unitEncoding false
      = .ok ⟨0, 1⟩ := by decide
```

Witness compatível com repetição abstrata de período `1`. O valor
concreto `⟨0, 1⟩` é **observação de teste**, não claim: nada é afirmado
sobre minimalidade ou unicidade.

## O que o contraexemplo demonstra

```text
semiconjugacao
+ ciclo abstrato
≠
ciclo concreto automatico
```

Ele **não** é falha da semiconjugação. Ele exibe exatamente a perda de
informação que uma abstração existe para produzir, e mede a força exata
do resultado observacional.

## Registro

```yaml
naive_cycle_reflection:
  status: FALSE
  counterexample: BOOL_TO_UNIT

counterexample_orbit_separating:
  status: FALSE
```
