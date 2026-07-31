---
document_id: FCD-TOTALIZATION-DECISION
total_wrapper_status: DEFERRED
classification: OPTIONAL_CORE_PENDING_EXECUTION_TEST
---

# Decisão sobre a totalização

## API garantida da v1

```text
Option CycleWitness
```

Isto é definitivo para a primeira versão.

## Estado do wrapper total

```yaml
total_wrapper:
  status: DEFERRED
  classification: OPTIONAL_CORE_PENDING_EXECUTION_TEST
```

## Os sete critérios

| Critério | Estado | Evidência |
|---|---|---|
| sem `Classical.choose` | **confirmado** | não aparece em parte alguma do desenho |
| sem `noncomputable` | **confirmado** | nenhuma definição precisou da marca |
| sem axioma | **confirmado no sentido operacional** | ver `COMPUTABILITY_REVIEW.md`: a pegada vem de `Fintype.card` e não impede execução |
| sem fallback arbitrário | **confirmado** | `Option.get` não tem ramo `none`; `getD` com certificado falso está **proibido** |
| `#eval` funciona em exemplos concretos | **parcialmente confirmado** | ver abaixo |
| código compilado não precisa calcular a prova | **confirmado** | `Option.get` recebe a prova como argumento `Prop`, apagado na compilação |
| ramo `none` logicamente impossível e apagável | **confirmado** | `Option.get` elimina o ramo por construção |

## O critério parcialmente confirmado

O probe avaliou o **mecanismo**:

```lean
def probeTotal {X : Type*} [Fintype X] [DecidableEq X] (f : X → X) (x : X)
    (h : (detectCycleWitness? f x).isSome = true) : CycleWitness :=
  (detectCycleWitness? f x).get h
```

com a hipótese fornecida por `by decide` em casos concretos. Resultados:

```text
probeTotal fNot true   ->  <0,2>
probeTotal f4   0      ->  <2,2>
probeTotal f3   0      ->  <2,1>
```

**`Option.get` avalia.** O que **não** foi testado é a mesma avaliação com
a prova vinda de `detectCycleWitness?_complete` — porque provar a
completude exigiria provar um teorema central, o que este gate proíbe no
probe.

Como o teorema é uma `Prop` e provas são apagadas, o risco residual é
baixo. Mas *baixo* não é *confirmado*, e a regra do gate é explícita:

```text
Se qualquer item nao puder ser confirmado neste gate: DEFERRED.
```

## Consequência

```text
detectCycleWitness        OPTIONAL_CORE
detectCycleWitness_valid  OPTIONAL_CORE
CD-GAP-017                OPEN_DEFERRED
```

A decisão final cabe ao gate de formalização, que poderá provar a
completude e avaliar o wrapper de verdade. **Isso não bloqueia a
aprovação da especificação.**

## Proibições

```text
NAO usar Option.getD com certificado padrao falso.
NAO usar Classical.choose.
NAO marcar o wrapper como noncomputable para "resolver" o problema.
NAO tornar a API total obrigatoria na v1.
```

Um `getD ⟨0, 1⟩` devolveria um certificado **inválido** em um caso que
nunca ocorre — mas o tipo deixaria de garantir validade, e
`detectCycleWitness_valid` se tornaria improvável. É por isso que está
proibido, não por estilo.
