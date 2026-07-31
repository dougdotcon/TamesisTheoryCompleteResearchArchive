---
document_id: PR-AFTER-RUNTIME-ADAPTER
gate: PORTFOLIO_REVIEW
reviewed_at_commit: 861dc6bf24b4e1f8da88af138554556e644a3b49
decision: A_PORTFOLIO_REVIEW_APPROVED_CERTIFIED_STATE_ENCODING_SELECTED
selected_work_item: ENG-FINITE-STATE-ENCODING-001
alternatives_compared: 6
---

# Revisão de portfólio após o adaptador de runtime

## O que o laboratório passou a ter

```text
Array Nat
    -> validacao estrutural, sem correcao silenciosa
    -> Fin n -> Fin n, total por construcao
    -> detector certificado
    -> CycleWitness
    -> repeticao PROVADA sobre o Array original
```

Quatro frentes encerradas sustentam essa cadeia:
`FOUND-SEMIGROUP-002`, `FOUND-FUNCTIONAL-GRAPH-001`,
`FOUND-CYCLE-DETECTION-001` e `ENG-FINITE-STATE-RUNTIME-001`. Todas com
`work_status: VERIFIED`, `result_review: APPROVED` e
`extension_status: NOT_AUTHORIZED`. `RH-NOGO-001` permanece
`FROZEN_PARTIAL_RESULT`, `NOT_AUTHORIZED`, `NO_EXECUTION`.

## A limitação central

Não é desempenho. Não é CLI. Não é JSON.

```text
A tabela eh analisada corretamente,
mas nao existe prova de que ela representa o sistema que a originou.
```

Isto está registrado como `RT-GAP-017`, `OPEN_DEFERRED`, com a nota
literal: *"a frente valida e interpreta uma tabela; ela NÃO prova que a
tabela representa corretamente um sistema externo."*

A entrada do adaptador é um `Array Nat` **anônimo**. Nada no laboratório
diz de onde ele veio. Um erro de codificação — dois estados mapeados no
mesmo índice, uma transição registrada no destino errado — produz uma
tabela perfeitamente válida, um certificado perfeitamente correto e uma
conclusão **falsa** sobre o sistema real.

Extrair, empacotar em CLI e ler JSON amplifica esse buraco em vez de
fechá-lo: constrói distribuição sobre um contrato semântico ausente.

## A distinção que decide o gate

```text
o adaptador prova algo sobre A TABELA;
falta provar algo sobre A RELACAO entre a tabela e o sistema.
```

Existem exatamente duas rotas para essa relação:

| Rota | O que exige | O que entrega |
|---|---|---|
| **codificação certificada** | uma bijeção fornecida, com leis inversas | correspondência **exata**; nenhum ciclo espúrio |
| **abstração e simulação** | uma relação de simulação | correspondência **parcial**; ciclos espúrios possíveis |

A primeira é o caso em que a resposta é *sim, exatamente*. A segunda é o
caso em que a resposta é *talvez, e o contraexemplo é difícil*. Um
laboratório que prioriza resultados parciais verdadeiros começa pela
primeira — e a segunda passa a ter, então, um alvo de comparação
formalizado.

## Alternativas comparadas

Seis, na matriz completa em `NEXT_TARGET_COMPARISON_MATRIX.md`:

```text
A  ENG-FINITE-STATE-ENCODING-001      codificacao certificada
B  ENG-LEAN-NATIVE-EXTRACTION-001     extracao nativa isolada
C  ENG-FINITE-STATE-CLI-001           CLI e formato externo
D  ENG-FINITE-STATE-DIAGNOSTICS-001   diagnostico detalhado
E  FOUND-FINITE-ABSTRACTION-001       abstracoes e simulacao
F  nova frente matematica independente
```

## Decisão

```text
A. PORTFOLIO_REVIEW_APPROVED_CERTIFIED_STATE_ENCODING_SELECTED
```

As dez condições da regra de decisão foram verificadas uma a uma, e
**todas** passaram — inclusive as três que dependiam de auditoria de API
no checkout. Nenhuma stop condition material foi disparada.

## Por que não as outras

- **B** e **C** distribuem uma garantia que ainda não existe. Sem
  contrato semântico, uma CLI correta produz respostas corretas sobre a
  tabela errada. E `C` depende de `B`, que hoje não tem consumidor.
- **D** é útil e barato, mas é conforto operacional: `RT-GAP-022` não
  impede uso nenhum, e nada no laboratório passa a ser possível.
- **E** é a frente mais interessante cientificamente e a mais perigosa
  agora. Ciclo abstrato **não** implica ciclo concreto, e enunciar isso
  errado é exatamente a classe de erro que o laboratório existe para
  evitar. Com `A` pronta, `E` ganha o caso exato como referência.
- **F** volta à matemática aberta sem produto verificável em trinta dias
  e sem fechar a lacuna que temos em mãos.

## Fronteira epistemológica vinculante

```text
Uma codificacao certificada prova correspondencia entre um sistema
formal TIPADO e sua tabela.

Ela NAO prova que um sistema fisico, servico, workflow ou programa
real foi modelado corretamente.

Essa prova continua pertencendo ao adaptador especifico da aplicacao.
```

`RT-GAP-017` **não** será fechado por esta frente no caso geral. Ele será
fechado apenas no recorte em que o sistema já é um objeto Lean tipado.
Essa distinção é o produto científico do gate, e não pode ser apagada
depois.

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Codificar um tipo finito como `Fin n` é rotina desde os anos 1950.
Nenhum algoritmo novo, nenhum modelo de computação novo, nenhuma teoria
de autômatos nova. O que se acrescenta é a **prova de que a codificação
preserva a dinâmica** dentro da cadeia já verificada.

## O que este gate NÃO fez

```text
nao executou a frente selecionada;
nao criou arquivo Lean;
nao criou prova;
nao executou lake build;
nao implementou CLI, parser, extracao, Floyd ou integracao;
nao modificou o runtime adapter;
nao reabriu frente encerrada;
nao tocou RH-NOGO-001.
```
