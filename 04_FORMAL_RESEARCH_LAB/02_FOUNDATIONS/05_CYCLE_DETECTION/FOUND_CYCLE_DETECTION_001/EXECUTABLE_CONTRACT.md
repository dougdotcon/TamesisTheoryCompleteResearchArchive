---
document_id: FCD-EXECUTABLE-CONTRACT
executable_predicate: OPTION_A_DECIDE
---

# Contrato executável

## Predicado executável — decisão

Duas opções foram auditadas.

### Opção A — `Decidable` direto

```lean
decide (CycleWitness.Valid f x w)
```

### Opção B — predicado booleano separado

```lean
def CycleWitness.validB [DecidableEq X] (f : X → X) (x : X)
    (w : CycleWitness) : Bool
```

com uma ponte `validB_eq_true_iff`.

### Decisão: **Opção A**

Verificado na sonda temporária que, com `DecidableEq X` disponível, a
instância existe e é encontrada por `inferInstance`:

```lean
example (f : Bool → Bool) (m l : ℕ) :
    Decidable (m < Fintype.card Bool ∧ 0 < l ∧ m + l ≤ Fintype.card Bool ∧
      f^[m + l] true = f^[m] true) :=
  inferInstance
```

A instância se monta a partir de `Nat.decLt`, `instDecidableAnd` e a
`DecidableEq X` do usuário. Não há razão para duplicar o predicado.

Consequência: **`Bool` e `Prop` não são congelados simultaneamente.**
Existe uma única definição — `Valid`, proposicional — e a forma booleana é
`decide` aplicado a ela, com `decide_eq_true_eq` como única ponte, já
existente na biblioteca.

`validB` fica registrado como `NOT_NEEDED`. Se a formalização revelar que
`decide` gera um termo grande demais para avaliar confortavelmente, a
Opção B volta como fallback — registrado em `CD-GAP-002`, não adotado por
antecipação.

## Detector parcial

```lean
def detectCycleWitness?
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    Option CycleWitness
```

Comportamento:

```text
procurar em cycleCandidates (Fintype.card X);
retornar o primeiro candidato valido;
retornar none somente se nenhum certificado for encontrado.
```

Forma candidata:

```text
List.find? (fun w => decide (CycleWitness.Valid f x w))
           (cycleCandidates (Fintype.card X))
```

## Proibições do detector

```text
NAO decidir igualdade de Function.periodicOrbit;
NAO usar Classical.choice;
NAO usar funcao noncomputable;
NAO depender de SimpleGraph;
NAO construir um quociente;
NAO repetir o pigeonhole.
```

`Function.periodicOrbit` é **noncomputável** e vive em `Cycle X`. O
detector compara **estados**, isto é, elementos de `X`, para os quais
`DecidableEq X` foi fornecida. Nenhuma decidibilidade sobre `Cycle X` é
assumida, requerida ou construída.

## Totalização

```lean
def detectCycleWitness
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    CycleWitness
```

Rota candidata: `detectCycleWitness? ` + `detectCycleWitness?_complete` +
`Option.get`.

Cinco condições de autorização:

| Condição | Estado |
|---|---|
| o corpo continuar computável | **plausível** — a prova entra apenas como argumento `Prop` de `Option.get`, e provas são apagadas |
| nenhum `Classical.choice` nas dependências executáveis | **plausível** — o `∃` da completude é consumido em nível `Prop`, nunca projetado para dado |
| `#eval` funcionar em tipos concretos | **NÃO VERIFICADO** — só é verificável implementando, o que este gate proíbe |
| a prova ser apagada durante extração | **plausível** pelo mesmo motivo |
| o resultado não receber marca `noncomputable` | **plausível** |

Como uma das cinco condições **não pôde ser verificada** dentro dos
limites deste gate:

```yaml
total_wrapper:
  status: DEFERRED
  reason: >
    a condicao "#eval funcionar em tipos concretos" so pode ser checada
    implementando o detector, o que este gate proibe. As outras quatro
    condicoes tem argumento favoravel registrado. A decisao final cabe ao
    gate de formalizacao.
```

**A API pública inicial permanece baseada em `Option`.**
`detectCycleWitness` fica em `OPTIONAL_CORE`, não em `CORE`.

`Classical.choose` **não** será usado em nenhuma hipótese. A distinção que
sustenta a rota é: usar `Classical.choice` para **provar** uma proposição
é inócuo computacionalmente; usá-lo para **produzir dado** torna a
definição `noncomputable`. Aqui ele nunca produz dado.
