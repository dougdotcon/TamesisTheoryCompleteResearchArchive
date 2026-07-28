---
schema: tamesis-formal-benchmark-specification/1
work_item_id: LAB-BENCH-001
gate: LAB_BENCHMARK_FORMALIZATION_PREPARATION_AUTHORIZED
preparation_status: PARTIAL
execution_status: NOT_STARTED
verification_status: NOT_STARTED
research_authorized: false
---

# LAB-BENCH-001 — Especificação do benchmark formal

## Objetivo

Validar que a infraestrutura do laboratório consegue representar e compilar
matemática elementar conhecida, com rastreabilidade entre requisitos,
arquivos Lean e resultados de build. O benchmark mede o processo; não mede
originalidade matemática.

## Escopo

O benchmark deverá cobrir:

- definições e estruturas pequenas;
- relações e funções tipadas;
- identidade e composição;
- lemas elementares conhecidos;
- imports e namespaces isolados;
- um uso mínimo e controlado de Mathlib;
- testes de compilação e importação;
- contagem zero de `sorry`, `admit`, `axiom` local e `unsafe`;
- rastreabilidade entre cada requisito e seu arquivo Lean.

## Não-objetivos

- produzir matemática nova;
- formalizar TRI, TDTR, `M_c`, TOE ou qualquer claim histórica;
- iniciar `RH-NOGO-001` ou outra frente Clay;
- reproduzir a prova de Perelman;
- tratar smoke test, Python ou ausência de contraexemplo como teorema;
- promover evidência `F` ou `C` para `T`.

## Resultados conhecidos selecionados

Os resultados são deliberadamente elementares:

1. leis de identidade para composição de funções;
2. associatividade da composição de funções;
3. identidade e associatividade para uma composição relacional finita
   explicitamente definida;
4. construção e projeção de uma estrutura pequena de estado;
5. igualdade decidível para um tipo enumerado finito;
6. pertencimento a um singleton de `Finset`, como teste controlado de Mathlib;
7. importação do módulo raiz e uso dos lemas em um arquivo de testes.

Esses itens são exercícios de infraestrutura. Nenhum deles é uma descoberta
do Programa Tamesis.

## Dependências Lean e Mathlib

| Dependência | Requisito canônico | Estado atual |
|---|---|---|
| Lean | `leanprover/lean4:v4.32.2` resolvido por `lean-toolchain` e Elan | `PARTIAL`: executa somente pelo diretório `.tmp` |
| Lake | versão compatível resolvida pelo mesmo toolchain | `PARTIAL`: `5.0.0-src+f3b06c7` no `.tmp` |
| Elan | shim estável no PATH e toolchain definitivo | `PARTIAL`: Elan 4.2.3 existe, mas shims não estão no PATH desta sessão |
| Mathlib | revisão exata fixada no manifesto | `NOT_STARTED`: pacote ausente |
| manifesto | `lake-manifest.json` versionado e com hashes resolvidos | `PARTIAL`: existe, mas `packages` está vazio |

O benchmark não pode ser executado enquanto a revisão exata de Mathlib não
estiver fixada. Não é permitido usar `latest`, uma revisão flutuante ou um
diretório `.tmp` como configuração reprodutível.

## Arquivos Lean previstos

Somente após autorização de execução:

```text
05_FORMAL/lean/TamesisLab/Benchmark/Core.lean
05_FORMAL/lean/TamesisLab/Benchmark/Structures.lean
05_FORMAL/lean/TamesisLab/Benchmark/Relations.lean
05_FORMAL/lean/TamesisLab/Benchmark/MathlibInterop.lean
05_FORMAL/lean/TamesisLab/Benchmark.lean
05_FORMAL/lean/Tests/Benchmark.lean
```

O smoke test existente não substitui esses arquivos.

## Testes previstos

1. `elan show` resolve exatamente o identificador declarado.
2. `elan which lean` e `elan which lake` apontam para um toolchain definitivo.
3. `lean --version` e `lake --version` funcionam pelos shims.
4. `lake build` compila os módulos do benchmark.
5. o arquivo de testes importa `TamesisLab.Benchmark`.
6. a busca por tokens proibidos retorna zero.
7. o manifesto contém a revisão exata de Mathlib.
8. cada requisito `BENCH-*` possui arquivo e evidência associados.
9. nenhum arquivo fora de `04_FORMAL_RESEARCH_LAB/` é modificado.

## Critérios de sucesso

- toolchain definitivo resolvido por Elan, sem dependência de `.tmp`;
- revisão Mathlib exata e manifesto reproduzível;
- todos os arquivos previstos compilam;
- todas as verificações previstas passam;
- zero `sorry`, `admit`, `axiom` local e `unsafe`;
- matriz de rastreabilidade completa;
- sessão imutável registra comandos, versões, hashes e resultados;
- nenhuma claim de pesquisa é criada ou promovida.

## Critérios de falha

- ferramenta resolvida somente por caminho temporário;
- Mathlib sem revisão fixada;
- import flutuante ou não reproduzível;
- erro de compilação ou teste;
- token proibido;
- ausência de evidência rastreável;
- mudança no legado;
- qualquer tentativa de iniciar pesquisa Clay.

## Stop conditions

Interromper imediatamente se:

- a instalação definitiva do toolchain não puder ser confirmada;
- a revisão Mathlib não puder ser fixada;
- um resultado exigir axioma local, `sorry`, `admit` ou `unsafe`;
- o escopo deixar de ser matemática elementar conhecida;
- houver alteração fora da camada formal;
- alguém interpretar o benchmark como validação de TRI, TDTR, TOE ou Clay.

## Evidências obrigatórias

| ID | Evidência | Artefato esperado |
|---|---|---|
| BENCH-ENV-001 | versões de Elan, Lean e Lake | sessão de execução |
| BENCH-ENV-002 | resolução por shims e toolchain definitivo | sessão de execução |
| BENCH-DEP-001 | revisão Mathlib e hash do manifesto | `lake-manifest.json` + sessão |
| BENCH-DEF-001 | definições/estruturas compiladas | `Benchmark/Structures.lean` |
| BENCH-FUN-001 | identidade e composição compiladas | `Benchmark/Core.lean` |
| BENCH-REL-001 | relações e composição compiladas | `Benchmark/Relations.lean` |
| BENCH-MATHLIB-001 | uso controlado de Mathlib | `Benchmark/MathlibInterop.lean` |
| BENCH-TEST-001 | import e testes compilados | `Tests/Benchmark.lean` |
| BENCH-SAFE-001 | zero tokens proibidos | saída registrada |
| BENCH-SCOPE-001 | zero alterações legadas/promotions | `labctl validate` |

## Estado do gate

A especificação está registrada, mas a preparação operacional permanece
`PARTIAL` devido ao toolchain temporário e à revisão Mathlib não fixada.
Execução e verificação continuam `NOT_STARTED`.

