---
document_id: RT-SPECIFICATION-DECISION
decision: A_ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_READY
---

# Decisão da especificação

```text
A. ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_READY
```

## Critérios

| Critério | Estado |
|---|---|
| `RawTransitionTable` congelada | um campo, `Array Nat` |
| `Valid` congelada | formulação por `Fin`, decidível |
| política da tabela vazia congelada | estruturalmente válida, consulta rejeitada |
| `ValidatedTransitionTable` congelada | estrutura nomeada, com `closed` |
| erro dinâmico congelado | três construtores, `deriving` completo |
| validação executável planejada | `dite` sobre `Valid`, sem tocar no array |
| validação do início planejada | `dite` sobre `<`, preserva `start` |
| `step` total planejado | `⟨t.next[i], t.closed i⟩` |
| semântica `run?` planejada | recursão com `Option`, sem fallback |
| ponte de iterações coerente | variante de `iterate` **auditada** |
| aplicação do detector por API | uma linha, sem cópia |
| interpretação bruta do witness | `detectCycle?_raw_repeat` |
| `analyzeTransitionTable` planejada | `do` sobre `Except`, quatro ramos |
| soundness e completeness planejadas | quatro pares |
| sem módulo, clamp ou fallback | proibido em quatro documentos |
| sem totalização implícita | `Option` preservado dentro da camada |
| sem parsing externo | o núcleo recebe `Array Nat` |
| gaps registrados | 22 |
| novidade zero preservada | `NONE` / `NONE` |
| nenhuma implementação permanente | 0 arquivos Lean |

## Decisões tomadas nesta especificação

Quatro que o gate deixou em aberto:

1. **`stateCount` não será criado.** Duplicaria `next.size` sob um segundo
   nome público. A alternativa — adotá-lo em toda parte — foi registrada.
2. **`toRaw` será público.** É a única forma de enunciar os dois teoremas
   centrais, que falam da tabela original.
3. **`step?_eq_some_step` é `CORE`, não opcional.** A indução de
   `run?_eq_iterate_step` depende dele para o `bind` reduzir.
4. **A variante de iteração é `Function.iterate_succ_apply`**, não a
   linha. `run?` aplica um passo e recorre; a contagem externa consome o
   passo **interno**. Auditado, não presumido.

## Evidência de viabilidade

A versão descartável do probe implementou o pipeline inteiro e avaliou
**treze** casos, todos com o resultado previsto — incluindo os três de
erro e os quatro que reproduzem os modelos já verificados no detector.
`step_val` fechou por `rfl`. A instância decidível foi sintetizada.

Isso não é prova; é evidência forte de que a arquitetura **pode** ser
formalizada sem criar uma segunda teoria de execução paralela.

## O risco que a revisão deve examinar

```text
run?_eq_iterate_step eh o unico teorema da frente cuja prova nao eh
mecanica.
```

Se a indução exigir generalização adicional ou lemas de coerção `Fin`/`Nat`
não previstos, o custo cresce. É o ponto onde a especificação está mais
exposta, e o gate de revisão deve olhá-lo primeiro.

## Próximo passo

```yaml
authorized_action: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_AUTHORIZED
```

Revisar a validade da tabela, a construção da função sobre `Fin n`, a
correspondência entre execução bruta e iteração tipada, e a API dinâmica
baseada em `Except`.

**Nenhuma formalização autorizada. Nenhum arquivo Lean. Nenhuma extração,
CLI, JSON ou integração.**
