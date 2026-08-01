---
document_id: ENC-AXIOM-FOOTPRINT-REVIEW
supersedes: ENC-AXIOM-BOUNDARY
stage: SPECIFICATION_REVIEW
decision: ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT
---

# Revisão da pegada axiomática

## Onde a pegada **não** está

```text
CertifiedFiniteEncoding.encode_injective    does not depend on any axioms
CertifiedFiniteEncoding.encode_surjective   does not depend on any axioms
CertifiedFiniteEncoding.encodedStep         does not depend on any axioms
```

Toda a camada de codificação é **livre de axiomas**. Medido no probe de
revisão. A especificação relatava a pegada como uniforme desde o início;
isto **corrige** aquela leitura: as três primeiras declarações não
dependem de nada.

## Onde ela começa

```text
PRIMEIRA declaracao com [propext, Classical.choice, Quot.sound]:
  buildTransitionTable
```

E a razão é única e localizável: o campo `closed` usa
`Array.getElem_ofFn`.

```text
Array.ofFn           [propext]
Array.size_ofFn      [propext]
Array.getElem_ofFn   [propext, Classical.choice, Quot.sound]
```

Daí em diante a pegada propaga pelo **tipo**, não pela prova: até
`buildTransitionTable_size`, cujo próprio argumento é `Array.size_ofFn`
(`[propext]`), herda os três axiomas porque seu enunciado menciona
`buildTransitionTable`.

## Rota B — tentada e medida

```lean
theorem sizeB1 (f : Fin n → Nat) : (Array.ofFn f).size = n := rfl
```

```text
error: Not a definitional equality: the left-hand side
  (Array.ofFn f).size
is not definitionally equal to the right-hand side
  n
```

```lean
theorem getB1 (f : Fin n → Nat) (i : Nat) (h : i < (Array.ofFn f).size) :
    (Array.ofFn f)[i] = f ⟨i, Array.size_ofFn ▸ h⟩ := rfl
```

Também falhou, já no `▸`.

**Mas**, com tamanho literal, as duas passam:

```lean
example (f : Fin 3 → Nat) : (Array.ofFn f).size = 3 := rfl                      -- PASSA
example (f : Fin 3 → Nat) : (Array.ofFn f)[1]'(by simp) = f ⟨1, by decide⟩ := rfl -- PASSA
```

Conclusão exata: `Array.ofFn` é definida por um laço, e a redução só
fecha quando `n` é um literal. A API da frente é **polimórfica em `n`**,
logo a rota leve não existe para ela. Não é preferência de estilo: é
impossibilidade medida.

## O argumento decisivo

```text
analyzeTransitionTable            [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_sound      [propext, Classical.choice, Quot.sound]
analyzeTransitionTable_complete   [propext, Classical.choice, Quot.sound]
```

A **definição** reutilizada do runtime adapter já carrega os três
axiomas, herdados de `Fintype.card` pelo detector. Mesmo que a prova de
`closed` ficasse mais leve, `analyzeEncodedSystem` e seus dois teoremas
centrais continuariam exatamente onde estão.

Em contraste, o que o adaptador tem de mais leve foi preservado:

```text
ValidatedTransitionTable.step                 [propext, Quot.sound]
ValidatedTransitionTable.toRaw_valid          [propext, Quot.sound]
ValidatedTransitionTable.run?_eq_iterate_step [propext, Quot.sound]
Function.Semiconj.iterate_right               [propext]
Fin.cast, Fin.ext, Option.some.inj,
  Function.LeftInverse.injective              NENHUM
```

## Decisão

```yaml
decision: ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT
```

Critérios do gate, todos verificados por execução:

```text
buildTransitionTable permanece computavel      SIM
#eval funciona                                 SIM, sete modelos
nenhuma definicao eh noncomputable             SIM
nenhum Classical.choose no codigo              SIM, grep zero
nenhuma escolha classica produz o Array        SIM
a alternativa leve eh fragil ou inviavel       INVIAVEL para n generico
```

Não se abre frente para remover axiomas infraestruturais. Mathlib não é
modificada.

## A regra do laboratório, pela quinta vez

```text
a presenca infraestrutural de propext, Classical.choice e Quot.sound
nao bloqueia se:
  nenhuma definicao for noncomputable;
  #eval funcionar;
  nenhum Classical.choose produzir dado.
```

A novidade desta medição é que agora se sabe **exatamente** em qual
declaração a pegada entra, e por qual lema.


---

## Correção de validação — `ENC-VAL-001`

As medições deste documento permanecem **válidas e inalteradas**. O que
mudou foi onde os experimentos negativos vivem.

```yaml
negative_experiments:
  route: DEFINITIONAL_ARRAY_OF_FN_PROOF
  status: REJECTED_BY_PROBE
  included_in_mandatory_probe: false
  rerun_required: false
  preserved_in: este documento
```

As tentativas registradas na seção *"Rota B — tentada e medida"** são
evidência histórica. Elas **não** são reexecutadas e **não** pertencem a
nenhum probe obrigatório. A pegada axiomática foi reconfirmada em um
probe limpo, com `exit 0`, cujos números são idênticos aos aqui
registrados.
