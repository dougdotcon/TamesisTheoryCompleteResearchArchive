---
document_id: RT-REVIEW-DECISION
decision: A_ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_APPROVED
---

# Decisão da revisão

```text
A. ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_APPROVED
```

## Critérios

| Critério | Estado |
|---|---|
| `RawTransitionTable` mínima | um campo; cinco rejeitados |
| `Valid` decidível | `#synth` em três tabelas |
| tabela vazia separada da consulta | `ok` + `initialStateOutOfBounds 0 0` |
| `ValidatedTransitionTable` garante fechamento | campo `closed` |
| `step` total por construção | tipo não admite escape; `step_val` por `rfl` |
| `run?` sem fallback | `run? 1 999 = none` |
| **`run?_eq_iterate_step` com prova viável** | **compila** |
| detector apenas reutilizado | `detectCycle?` é uma linha |
| witness interpretado na tabela bruta | `detectCycle?_raw_repeat` compila |
| precedência dos erros congelada | dois teoremas + teste `#[1] 100` |
| `internalDetectorFailure` defensivo | ramo mantido; impossibilidade derivável |
| soundness e completeness coerentes | transporte dependente evitado por desenho |
| nenhuma entrada corrigida | sem `mod`, `clamp`, `getD`, fallback |
| nenhum parsing externo | núcleo recebe `Array Nat` |
| novidade zero | `NONE` / `NONE` |

Nenhuma das vinte e uma condições de `NEEDS_CORRECTIVE_PATCH` ocorreu.

## O que esta revisão acrescentou

1. **Demonstração de viabilidade.** O probe compilou com zero erros,
   incluindo os dois teoremas que a especificação apontava como risco.
   `run?_eq_iterate_step` deixa de ser plano e passa a ser fato
   reproduzível.
2. **Três detalhes congelados** na prova central: quantificador no
   enunciado em vez de `generalizing`; dois `show` obrigatórios; variante
   `iterate_succ_apply`.
3. **Padrão das provas de precedência**, com as três abordagens que
   falham documentadas para não serem repetidas.
4. **Correção da auditoria de API**: `getElem?_pos` e
   `Array.getElem?_eq_getElem` existem; apenas `Array.getElem?` como
   constante não existe.
5. **Coerções `Fin`/`Nat` explícitas** em todos os enunciados públicos.

## Riscos restantes

```text
BAIXO   as provas foram demonstradas em ambiente descartavel, nao no
        repositorio; nomes e namespaces mudarao

MEDIO   analyzeTransitionTable_sound e _complete NAO foram demonstradas
        no probe — apenas planejadas. Sao as duas unicas obrigacoes
        centrais ainda sem evidencia executavel.
```

O segundo risco é o que a formalização deve atacar primeiro. A estratégia
registrada — trabalhar com `⟨raw.next, hRaw⟩` para evitar transporte
dependente — é a mitigação.

## Estado final

```yaml
work_status: READY
specification_status: APPROVED
authorized_action: ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_AUTHORIZED
```

Extração, CLI, JSON, integração, diagnóstico detalhado, totalização do
detector anterior e Floyd permanecem **não autorizados**.

## Próxima ação

Formalizar a validação da tabela e do estado inicial, a função total sobre
`Fin n`, a correspondência de iterações, a aplicação do detector e a API
dinâmica baseada em `Except`.

A formalização **não** começa neste gate.
