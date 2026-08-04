---
document_id: FOUND-BISIMULATION-BOUNDARY-001-DATA-MODEL
work_item_id: FOUND-BISIMULATION-BOUNDARY-001
---

# Modelo — três proposições, nenhum dado novo

A frente **não** introduz estrutura de dado. Tudo é `Prop` sobre funções
que já existem.

## As definições

```lean
def Simulates (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, abstract (stepC c) = stepA (abstract c)

def Reflects (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  ∀ c : C, ∃ c' : C, stepC c = c' ∧ abstract c' = stepA (abstract c)

def Bisimulation (abstract : C → A) (stepC : C → C) (stepA : A → A) : Prop :=
  Simulates abstract stepC stepA ∧ Reflects abstract stepC stepA
```

## Por que `Reflects` conserva o `∃`

Escrever

```lean
def Reflects … := ∀ c, abstract (stepC c) = stepA (abstract c)   -- ERRADO
```

tornaria `reflects_iff_simulates` verdadeiro por `Iff.rfl` e o colapso
seria **uma tautologia disfarçada de teorema**.

A forma com `∃ c', stepC c = c' ∧ …` é a transcrição fiel da condição
zag de bissimulação. O conteúdo do resultado é precisamente que, sob
determinismo e totalidade, essa existencial não oferece escolha.

Torná-la trivial por definição dispararia `STOP-BIS-002`.

## Por que não há estrutura

```text
nenhuma structure
nenhum campo
nenhum dado executavel
nenhuma instancia
```

A frente anterior já tem `CertifiedFiniteAbstraction`, que carrega
`abstract` e a prova de `Semiconj`. Criar uma segunda estrutura para
carregar a mesma informação sob outro nome seria duplicação — e o
teorema de colapso diz exatamente que seria a **mesma** informação.

## Typeclasses

```text
sobre C   nenhuma
sobre A   nenhuma
```

`C` e `A` permanecem `Type*` sem instância, como na frente anterior.
