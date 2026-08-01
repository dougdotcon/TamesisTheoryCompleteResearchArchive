---
document_id: PR-NEXT-TARGET-COMPARISON-AFTER-ENCODING
alternatives: 7
scale: [LOW, MODERATE, HIGH, VERY_HIGH, EXTREME]
---

# Matriz de comparação

## Resumo

| | A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|---|
| custo formal | MODERATE | MODERATE | LOW | MODERATE | LOW | LOW | EXTREME |
| valor de engenharia | MODERATE | LOW | MODERATE | HIGH | MODERATE | LOW | LOW |
| valor científico | **HIGH** | LOW | LOW | LOW | LOW | LOW | VERY_HIGH |
| valor de governança | LOW | LOW | LOW | LOW | LOW | **MODERATE** | LOW |
| reutilização verificada | **VERY_HIGH** | HIGH | HIGH | MODERATE | HIGH | LOW | LOW |
| risco de enunciado falso | **LOW** | MODERATE | LOW | MODERATE | LOW | LOW | EXTREME |
| risco de acoplamento | LOW | **HIGH** | MODERATE | HIGH | MODERATE | LOW | LOW |
| risco de expansão | MODERATE | LOW | MODERATE | VERY_HIGH | LOW | LOW | EXTREME |
| PoC em 30 dias | **YES** | PARTIAL | PARTIAL | NO | YES | YES | NO |
| produto visível | NO | NO | PARTIAL | YES | YES | NO | NO |
| lacuna fechada | **GAP-B, GAP-C** | GAP-D | GAP-E | GAP-F | GAP-G | GAP-H | nenhuma |

## A — abstração finita certificada e reflexão

```yaml
work_item_candidate: FOUND-FINITE-ABSTRACTION-001
track: FOUNDATIONS
primary_gap_closed: "GAP-B e GAP-C: abstracoes muitos-para-um e ciclos espurios"
formal_cost: MODERATE
engineering_value: MODERATE
scientific_value: HIGH
governance_value: LOW
reuse_of_verified_artifacts: VERY_HIGH
mathlib_readiness: HIGH
external_dependencies: none
counterexample_access: VERY_HIGH
risk_of_false_statement: LOW
risk_of_scope_expansion: MODERATE
risk_of_implementation_coupling: LOW
thirty_day_poc: YES
user_visible_product: NO
capability_created: >
  o laboratorio passa a dizer, com prova, o que uma abstracao finita
  PRESERVA e o que ela DESTROI, e sob qual hipotese o destruido pode ser
  recuperado.
reasons_to_select: >
  eh a unica alternativa que ataca a lacuna cientifica restante; o
  resultado fraco e o contraexemplo ja compilaram; a condicao de reflexao
  eh nao tautologica, verificavel pelo consumidor e equivalente a
  Set.InjOn sobre a orbita; nao exige finitude de C nem DecidableEq C;
  reutiliza analyzeEncodedSystem_sound sem tocar a frente anterior.
reasons_to_reject: >
  nao entrega produto visivel; a condicao de reflexao continua sendo
  obrigacao de quem modela o sistema.
```

## B — invariância do witness sob recodificação

```yaml
work_item_candidate: ENG-FINITE-STATE-REENCODING-001
track: engineering_foundation
primary_gap_closed: "GAP-D, ENC-GAP-020"
formal_cost: MODERATE
engineering_value: LOW
scientific_value: LOW
governance_value: LOW
reuse_of_verified_artifacts: HIGH
mathlib_readiness: HIGH
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: MODERATE
risk_of_scope_expansion: LOW
risk_of_implementation_coupling: HIGH
thirty_day_poc: PARTIAL
user_visible_product: NO
capability_created: "comparar dois witnesses do mesmo sistema"
reasons_to_select: "produto estreito, fecha uma lacuna nomeada"
reasons_to_reject: >
  a igualdade do witness CONCRETO depende da ordem de enumeracao de
  cycleCandidates; prova-la abriria o detector, que quatro frentes
  trataram como caixa-preta verificada. O que eh invariante — a validade
  semantica — ja eh a soundness. O risco de acoplamento eh o mais alto
  das sete.
```

## C — extração nativa

```yaml
work_item_candidate: ENG-LEAN-NATIVE-EXTRACTION-001
track: engineering_infrastructure
primary_gap_closed: "GAP-E, RT-GAP-013"
formal_cost: LOW
engineering_value: MODERATE
scientific_value: LOW
governance_value: LOW
reuse_of_verified_artifacts: HIGH
mathlib_readiness: HIGH
external_dependencies: "lake executable, backend nativo"
counterexample_access: MODERATE
risk_of_false_statement: LOW
risk_of_scope_expansion: MODERATE
risk_of_implementation_coupling: MODERATE
thirty_day_poc: PARTIAL
user_visible_product: PARTIAL
capability_created: "rodar a analise fora do decide"
reasons_to_select: "custo baixo; primeiro passo operacional"
reasons_to_reject: >
  sem parser a entrada continua construida dentro do programa, e sem o
  caso muitos-para-um a garantia distribuida continua restrita ao caso
  exato. Nao escolher extracao apenas porque produz binario visivel.
```

## D — CLI e parser

```yaml
work_item_candidate: ENG-FINITE-STATE-CLI-001
track: engineering_product
primary_gap_closed: "GAP-F, RT-GAP-014, RT-GAP-015"
formal_cost: MODERATE
engineering_value: HIGH
scientific_value: LOW
governance_value: LOW
reuse_of_verified_artifacts: MODERATE
mathlib_readiness: MODERATE
external_dependencies: "parser, formato, IO"
counterexample_access: MODERATE
risk_of_false_statement: MODERATE
risk_of_scope_expansion: VERY_HIGH
risk_of_implementation_coupling: HIGH
thirty_day_poc: NO
user_visible_product: YES
capability_created: "receber sistema de fora"
reasons_to_select: "eh o que parece util a um observador externo"
reasons_to_reject: >
  depende de C, que nao existe; introduz IO e um modelo de erro paralelo;
  e o produtor da entrada continua sem prova. Nao escolher CLI antes de
  uma rota de extracao.
```

## E — diagnóstico detalhado

```yaml
work_item_candidate: ENG-FINITE-STATE-DIAGNOSTICS-001
track: engineering_product
primary_gap_closed: "GAP-G, RT-GAP-022"
formal_cost: LOW
engineering_value: MODERATE
scientific_value: LOW
governance_value: LOW
reuse_of_verified_artifacts: HIGH
mathlib_readiness: HIGH
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: LOW
risk_of_scope_expansion: LOW
risk_of_implementation_coupling: MODERATE
thirty_day_poc: YES
user_visible_product: YES
capability_created: "mensagem de erro melhor"
reasons_to_select: "barato e seguro"
reasons_to_reject: >
  altera o modelo de erro de uma frente encerrada, exige segunda busca e
  teoremas de correcao dessa busca. Nada no laboratorio passa a ser
  possivel.
```

## F — integridade YAML de front matter

```yaml
work_item_candidate: LAB-GOV-YAML-FRONT-MATTER-001
track: governance
primary_gap_closed: "GAP-H"
formal_cost: LOW
engineering_value: LOW
scientific_value: LOW
governance_value: MODERATE
reuse_of_verified_artifacts: LOW
mathlib_readiness: "nao aplicavel"
external_dependencies: none
counterexample_access: HIGH
risk_of_false_statement: LOW
risk_of_scope_expansion: LOW
risk_of_implementation_coupling: LOW
thirty_day_poc: YES
user_visible_product: NO
capability_created: "cobertura de duplicatas em front matter Markdown"
reasons_to_select: "custo baixo; a lacuna eh real e foi registrada pelo proprio laboratorio"
reasons_to_reject: >
  a auditoria exigida pelo gate NAO encontrou risco concreto e imediato.
  Medido: 429 arquivos Markdown, 277 com front matter YAML, ZERO com
  chave duplicada. O bloco de LAB_STATE.md, unico YAML-em-Markdown de que
  a governanca depende para decidir, tambem esta limpo, conferido na
  mesma fatia que o labctl carrega. Sem risco imediato, a alternativa nao
  tem prioridade sobre a lacuna cientifica.
```

### A auditoria, com números

```text
markdown_files                    429
com_front_matter                  277
com_duplicatas_no_front_matter      0
markdown consumidos pelo labctl     7
LAB_STATE.md, bloco carregado     sem duplicatas
```

A lacuna permanece **real**: o scanner integral seleciona por extensão
`.yaml`/`.yml` e, por construção, não vê YAML embutido em `.md`. O que a
auditoria mostra é que hoje ela não está sendo explorada.

## G — nova frente matemática independente

```yaml
work_item_candidate: "NS-PRESSURE-001 / PVSNP-PHYS-001 / YM-LIMIT-001 / HODGE-CDK-001 / BSD-HYP-MATRIX-001 / RH-NOGO-001 / TOE-INTERFACE-001"
track: millennium_or_toe
primary_gap_closed: nenhuma
formal_cost: EXTREME
engineering_value: LOW
scientific_value: VERY_HIGH
governance_value: LOW
reuse_of_verified_artifacts: LOW
mathlib_readiness: "LOW a MODERATE"
external_dependencies: "bibliografia primaria extensa"
counterexample_access: LOW
risk_of_false_statement: EXTREME
risk_of_scope_expansion: EXTREME
risk_of_implementation_coupling: LOW
thirty_day_poc: NO
user_visible_product: NO
capability_created: nenhuma no curto prazo
reasons_to_select: "retorno maximo em caso de sucesso"
reasons_to_reject: >
  nenhum produto verificavel em trinta dias; infraestrutura insuficiente
  nas frentes P3 e P4; RH-NOGO-001 permanece congelada por decisao
  propria; e a lacuna concreta que o laboratorio acabou de isolar ficaria
  aberta.
```

## Regra de decisão — as doze condições

| # | Condição | Verificação | Resultado |
|---|---|---|---|
| 1 | não existe work item equivalente | 15 ids na fila; nenhum com `ABSTRACTION` | **PASS** |
| 2 | `Semiconj` prova a correspondência de iteradas | `abstract_iterate`, `[propext]` | **PASS, compilado** |
| 3 | a soundness fraca termina em igualdade entre abstrações | conclusão é `abstract … = abstract …` | **PASS, compilado** |
| 4 | existe contraexemplo simples à reflexão ingênua | `naive_cycle_reflection_is_false`, **sem axiomas** | **PASS, compilado** |
| 5 | existe condição explícita e verificável de reflexão | `OrbitSeparating` | **PASS, compilado** |
| 6 | a condição não é consequência automática da semiconjugação | `boolToUnit_not_orbitSeparating`, **sem axiomas** | **PASS, compilado** |
| 7 | reutiliza `analyzeEncodedSystem_sound` sem modificar a frente | probe consome a API; `git status` do Lean vazio | **PASS** |
| 8 | nenhuma integração externa necessária | os probes só usam `Bool`, `Unit`, `Fin 4` | **PASS** |
| 9 | não é preciso assumir `C` finito | `C : Type*` sem `Fintype` | **PASS, compilado** |
| 10 | não é preciso assumir `DecidableEq C` | nenhuma instância exigida | **PASS, compilado** |
| 11 | PoC de 30 dias plausível | 1 definição, ~8 teoremas, 0 bibliografia | **PASS** |
| 12 | novidade permanece `NONE` | material clássico de métodos formais | **PASS** |

Doze de doze. Oito verificadas por compilação.
