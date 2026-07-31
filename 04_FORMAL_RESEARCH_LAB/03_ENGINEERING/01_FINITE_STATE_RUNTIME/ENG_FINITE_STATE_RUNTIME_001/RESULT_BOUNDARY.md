---
document_id: RT-RESULT-BOUNDARY
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# Fronteira do resultado

```text
Foi formalizado:

- RawTransitionTable sobre Array Nat;
- validade estrutural decidível;
- tabela vazia como estruturalmente válida;
- validação sem correção silenciosa;
- validação separada do estado inicial;
- ValidatedTransitionTable;
- função total Fin n → Fin n;
- semântica bruta step? e run?;
- correspondência entre run? e Nat.iterate;
- reutilização do detector certificado;
- interpretação do witness sobre a tabela original;
- API dinâmica baseada em Except;
- soundness e completeness;
- precedência dos erros;
- impossibilidade de internalDetectorFailure para entradas válidas;
- testes executáveis.

Não foi formalizado:

- diagnóstico detalhado do primeiro destino inválido;
- CLI;
- JSON;
- CSV;
- parsing de arquivo;
- rede;
- integração com sistemas reais;
- prova de correção da abstração externa;
- extração de produto;
- Floyd;
- Brent;
- tabela visitada;
- totalização do detector;
- minimalidade;
- complexidade formal;
- benchmark;
- novidade matemática ou algorítmica.
```

## O que o laboratório passou a ter

**A primeira API que aceita diretamente uma estrutura de dados dinâmica e
preserva uma cadeia formal completa até o certificado.**

```text
Array Nat  ->  validacao  ->  Fin n -> Fin n  ->  detector  ->  witness
                                                                  |
                              repeticao provada sobre o Array original
```

O consumidor fornece `Array Nat` e `Nat`. **Zero typeclasses.**

## A proibição que governa a arquitetura

```text
destinos invalidos sao REJEITADOS, nunca corrigidos.
```

Dois teoremas tornam isso impossível de esconder:
`validateTransitionTable_sound` força a tabela devolvida a ser a mesma, e
`validateStart_sound` força o índice devolvido a ter o valor pedido.

## A ressalva que a frente não apaga

```text
converter um sistema real para uma tabela finita eh uma ABSTRACAO;
a correcao dessa abstracao NAO eh fornecida por esta frente.
```

O adaptador garante que **a tabela dada** é analisada corretamente. Que a
tabela **represente** o sistema real é responsabilidade de quem a
produziu. `RT-GAP-017` permanece aberto, e provavelmente permanecerá.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Uma tabela de transições é a representação mais banal de um autômato
determinístico; validar limites é verificação de índices; construir
`Fin n → Fin n` é aplicação rotineira de tipos dependentes. Nada disso é
novo. O que a frente acrescenta é **conectar** as três coisas a um
detector cuja correção e completude já eram teoremas, e provar que a
conexão preserva a dinâmica.
