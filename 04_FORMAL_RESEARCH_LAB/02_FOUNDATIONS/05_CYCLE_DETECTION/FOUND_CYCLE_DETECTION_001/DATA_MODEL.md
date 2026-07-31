---
document_id: FCD-DATA-MODEL
structure_frozen: true
---

# Modelo de dados

## Estrutura executável

```lean
structure CycleWitness where
  prefixIndex : ℕ
  period : ℕ
```

Dois naturais. **Nada mais.**

## Campos rejeitados

| Campo | Decisão | Motivo |
|---|---|---|
| `entryPoint : X` | **rejeitado** | derivável por `f^[w.prefixIndex] x₀`; armazená-lo cria estado redundante e força a estrutura a depender de `X` |
| provas dentro da estrutura | **rejeitado** | tornaria a estrutura dependente de `f` e de `x₀`, e misturaria dado com evidência |
| `isMinimal : Bool` | **rejeitado** | minimalidade não está autorizada |
| `cycle : List X` | **rejeitado** | lista ordenada do ciclo está diferida |

Consequência desejada: `CycleWitness` **não é parametrizada por `X`**. É um
par de naturais, e portanto `DecidableEq`, `Repr` e igualdade estrutural
vêm de graça.

## Semântica dos campos — vinculante

```text
prefixIndex eh o indice-base de uma colisao certificada.
```

**Não** se afirma que `prefixIndex` é o menor índice de entrada no ciclo. O
nome `entryIndex` **não deve ser usado** enquanto a minimalidade não
estiver formalizada — ele carrega a conotação de "o ponto onde a cauda
termina", que é precisamente o que não foi provado.

```text
period significa periodo positivo testemunhado,
nao necessariamente periodo minimo.
```

**Não** chamar `period` de `minimalPeriod`. `Function.minimalPeriod` existe
na Mathlib e significa outra coisa; confundi-los seria um erro de nome com
consequência matemática.

## Predicado proposicional

```lean
def CycleWitness.Valid
    {X : Type*}
    [Fintype X]
    (f : X → X)
    (x : X)
    (w : CycleWitness) : Prop :=
  w.prefixIndex < Fintype.card X ∧
  0 < w.period ∧
  w.prefixIndex + w.period ≤ Fintype.card X ∧
  f^[w.prefixIndex + w.period] x =
    f^[w.prefixIndex] x
```

## Auditoria: `Fintype.card X` dentro de `Valid` ou como parâmetro?

Decisão: **permanece dentro de `Valid`**, com `[Fintype X]` no binder.

Justificativa:

1. `Valid` é o contrato **público** que os consumidores dos teoremas
   querem ler; a cota em `card X` faz parte do enunciado que interessa.
2. A conclusão de `exists_bounded_iterate_collision` já está escrita em
   termos de `Fintype.card X`. Manter a mesma forma faz a completude ser
   um transporte direto, sem lema de reindexação.
3. A generalidade que se perderia é recuperada onde ela realmente importa:
   `cycleCandidates` recebe `n : ℕ` **arbitrário** e
   `mem_cycleCandidates_iff` é enunciado para `n` arbitrário, sem
   `Fintype`. A separação fica limpa — a lista fala de `n`, o contrato
   fala de `card X`.
4. `Valid` **não** exige `DecidableEq X`. Ver `COMPUTABILITY_BOUNDARY.md`.

Fallback, caso a prova revele atrito: introduzir um auxiliar
`CycleWitness.ValidAt (n : ℕ) (f) (x) (w)` sem `Fintype`, definir
`Valid := ValidAt (Fintype.card X)` e provar a equivalência por `rfl`.
Registrado em `CD-GAP-002`; **não** adotado por antecipação.

## Relação com a estrutura sugerida no gate de portfólio

O gate de seleção sugeriu `CycleDetectionResult` com três campos,
incluindo `entryPoint`, e registrou explicitamente que a estrutura **não
estava congelada**. Esta especificação a reduz a dois campos e a renomeia
para `CycleWitness`, porque `Result` sugere resposta final e `Witness`
sugere certificado — que é o que de fato é.
