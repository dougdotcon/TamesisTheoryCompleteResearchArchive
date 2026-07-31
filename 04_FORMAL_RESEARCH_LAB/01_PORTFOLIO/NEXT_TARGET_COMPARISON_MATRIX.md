---
document_id: PR-NEXT-TARGET-COMPARISON-MATRIX
alternatives: 6
scale: [LOW, MODERATE, HIGH, VERY_HIGH, EXTREME]
---

# Matriz de comparação

## Resumo

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| custo formal | MODERATE | LOW | MODERATE | LOW | VERY_HIGH | EXTREME |
| valor de engenharia | HIGH | MODERATE | HIGH | MODERATE | MODERATE | LOW |
| valor científico | MODERATE | LOW | LOW | LOW | HIGH | VERY_HIGH |
| reutilização verificada | VERY_HIGH | HIGH | MODERATE | HIGH | MODERATE | LOW |
| risco de enunciado falso | LOW | LOW | MODERATE | LOW | **HIGH** | **EXTREME** |
| risco de expansão de escopo | LOW | MODERATE | **VERY_HIGH** | LOW | HIGH | EXTREME |
| PoC em 30 dias | **YES** | PARTIAL | NO | YES | NO | NO |
| lacuna fechada | **RT-GAP-017 (recorte tipado)** | RT-GAP-013 | RT-GAP-014/015 | RT-GAP-022 | RT-GAP-017 (geral) | nenhuma |

## A — codificação certificada de estados

```yaml
work_item_candidate: ENG-FINITE-STATE-ENCODING-001
track: engineering_foundation
formal_cost: MODERATE
engineering_value: HIGH
scientific_value: MODERATE
reuse_of_verified_artifacts: VERY_HIGH
mathlib_readiness: HIGH
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: LOW
risk_of_scope_expansion: LOW
thirty_day_poc: YES
capability_created: >
  o laboratorio passa a conseguir partir de um sistema Lean tipado e
  chegar a um certificado interpretado NO SISTEMA, e nao apenas na
  tabela.
current_gap_closed: >
  RT-GAP-017, no recorte em que o sistema ja eh um objeto formal
  tipado com codificacao fornecida.
reasons_to_select: >
  eh a unica alternativa que ataca a lacuna semantica; reutiliza o
  adaptador inteiro sem modifica-lo; nao depende de extracao, parser,
  rede ou sistema externo; a bijetividade elimina ciclos espurios por
  construcao; Array.ofFn, size_ofFn, getElem_ofFn e
  Function.Semiconj.iterate_right existem e foram medidos.
reasons_to_reject: >
  nao entrega nada visivel ao usuario final; exige que o consumidor
  forneca encode/decode em vez de deriva-los.
```

## B — extração nativa isolada

```yaml
work_item_candidate: ENG-LEAN-NATIVE-EXTRACTION-001
track: engineering_infrastructure
formal_cost: LOW
engineering_value: MODERATE
scientific_value: LOW
reuse_of_verified_artifacts: HIGH
mathlib_readiness: HIGH
external_dependencies: "lake executable, toolchain nativo"
counterexample_access: MODERATE
risk_of_false_statement: LOW
risk_of_scope_expansion: MODERATE
thirty_day_poc: PARTIAL
capability_created: "rodar analyzeTransitionTable fora do #eval"
current_gap_closed: RT-GAP-013
reasons_to_select: "custo baixo; RT-GAP-013 eh concreto"
reasons_to_reject: >
  sem parser nao ha entrada real, e sem contrato semantico a saida nao
  significa mais do que ja significa; distribuir binario amplifica a
  lacuna de RT-GAP-017 em vez de fecha-la; a representacao de Array Nat
  no runtime nativo ainda nao foi auditada; confiar apenas em #eval como
  evidencia de comportamento nativo eh justamente o risco.
```

## C — CLI e formato externo

```yaml
work_item_candidate: ENG-FINITE-STATE-CLI-001
track: engineering_product
formal_cost: MODERATE
engineering_value: HIGH
scientific_value: LOW
reuse_of_verified_artifacts: MODERATE
mathlib_readiness: MODERATE
external_dependencies: "parser, formato textual ou JSON, IO"
counterexample_access: MODERATE
risk_of_false_statement: MODERATE
risk_of_scope_expansion: VERY_HIGH
thirty_day_poc: NO
capability_created: "receber tabela de fora"
current_gap_closed: "RT-GAP-014 e RT-GAP-015"
reasons_to_select: "eh o que parece util a um observador externo"
reasons_to_reject: >
  depende de B, que nao existe; introduz IO e um modelo de erro paralelo
  ao RuntimeCycleError; o produtor da tabela continua sem prova nenhuma,
  de modo que a CLI seria uma garantia formal aplicada a um dado sem
  procedencia; risco alto de misturar parsing com o nucleo formal, o que
  ja eh proibicao vigente do laboratorio.
```

## D — diagnóstico detalhado

```yaml
work_item_candidate: ENG-FINITE-STATE-DIAGNOSTICS-001
track: engineering_product
formal_cost: LOW
engineering_value: MODERATE
scientific_value: LOW
reuse_of_verified_artifacts: HIGH
mathlib_readiness: HIGH
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: LOW
risk_of_scope_expansion: LOW
thirty_day_poc: YES
capability_created: "mensagem de erro melhor"
current_gap_closed: RT-GAP-022
reasons_to_select: "barato, seguro, compativel com a API atual"
reasons_to_reject: >
  incremento cientifico proximo de zero; exige uma segunda busca sobre a
  tabela e teoremas adicionais de correcao dessa busca, isto eh, custo
  formal real por conforto operacional; nada no laboratorio passa a ser
  possivel.
```

## E — abstrações e simulação

```yaml
work_item_candidate: FOUND-FINITE-ABSTRACTION-001
track: foundations
formal_cost: VERY_HIGH
engineering_value: MODERATE
scientific_value: HIGH
reuse_of_verified_artifacts: MODERATE
mathlib_readiness: MODERATE
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: HIGH
risk_of_scope_expansion: HIGH
thirty_day_poc: NO
capability_created: "relacionar sistemas infinitos ou grandes a modelos finitos"
current_gap_closed: "RT-GAP-017, no caso geral"
reasons_to_select: "eh a resposta completa a lacuna semantica"
reasons_to_reject: >
  ciclo na abstracao NAO implica ciclo no concreto — a direcao util eh
  justamente a que falha sem hipoteses fortes; exige simulacao,
  bissimulacao e uma teoria de ciclos espurios; risco alto de enunciar um
  teorema forte e falso; sem o caso exato de A formalizado, falta ate o
  ponto de comparacao para saber o que a abstracao perde.
```

## F — nova frente matemática independente

```yaml
work_item_candidate: "NS-PRESSURE-001 / PVSNP-PHYS-001 / YM-LIMIT-001 / HODGE-CDK-001 / BSD-HYP-MATRIX-001 / TOE-INTERFACE-001"
track: millennium_or_toe
formal_cost: EXTREME
engineering_value: LOW
scientific_value: VERY_HIGH
reuse_of_verified_artifacts: LOW
mathlib_readiness: "LOW a MODERATE, conforme a frente"
external_dependencies: "bibliografia primaria extensa"
counterexample_access: LOW
risk_of_false_statement: EXTREME
risk_of_scope_expansion: EXTREME
thirty_day_poc: NO
capability_created: nenhuma no curto prazo
current_gap_closed: nenhuma
reasons_to_select: "retorno cientifico maximo em caso de sucesso"
reasons_to_reject: >
  nenhum produto verificavel em trinta dias; infraestrutura Mathlib
  insuficiente nas frentes P3 e P4; risco epistemologico maximo; e
  deixaria aberta a lacuna concreta que o laboratorio acabou de
  identificar em seu proprio trabalho.
```

## Regra de decisão — as dez condições

| # | Condição | Verificação | Resultado |
|---|---|---|---|
| 1 | não existe work item equivalente | `grep` em `01_PORTFOLIO/` e `LAB_STATE.md`; 14 itens na fila | **PASS** |
| 2 | reutiliza o adaptador sem modificá-lo | consome `RawTransitionTable` e `analyzeTransitionTable`, ambos públicos e congelados | **PASS** |
| 3 | separa codificação de parsing externo | `encode`/`decode` são funções Lean; nenhum `IO` | **PASS** |
| 4 | nenhuma escolha clássica produz dado | garantido ao **receber** a codificação como campo; `Fintype.equivFin` é `noncomputable` e fica proibido para produzir dados | **PASS**, com `STOP-ENC-006` |
| 5 | rota plausível com `encode`/`decode` e leis inversas | `Equiv` existe; `symm_apply_apply` e `apply_symm_apply` medidos | **PASS** |
| 6 | `Array.ofFn` ou equivalente existe | `Array.ofFn`, `Array.size_ofFn`, `Array.getElem_ofFn` — todos `API_FOUND` | **PASS** |
| 7 | comutação de um passo formalizável | `getElem_ofFn` dá `(ofFn f)[i] = f ⟨i, _⟩`; `decode_encode` fecha | **PASS** |
| 8 | correspondência de iteradas é corolário | `Function.Semiconj.iterate_right`, axiomas `[propext]` | **PASS, mais forte que o previsto** |
| 9 | nenhuma afirmação sobre sistema externo real | o alvo é `stepS : S → S`, um objeto Lean | **PASS** |
| 10 | PoC de 30 dias viável | 1 estrutura, ~3 definições, ~8 teoremas, sem bibliografia | **PASS** |

Dez de dez. Nenhuma stop condition material disparada.
