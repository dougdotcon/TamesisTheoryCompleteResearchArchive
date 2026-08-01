---
document_id: ENC-REUSE-MATRIX
integrations_created: 0
---

# Matriz de reutilização

Três camadas, e a distância entre elas é o conteúdo desta matriz:

```text
uso DENTRO do Lean            disponivel hoje
uso APOS extracao             NAO autorizado
uso INTEGRADO a sistemas      NAO autorizado
```

| Aplicação | Antes da frente | Agora | Após extração | Integrado |
|---|---|---|---|---|
| configurações finitas | `DIRECT_WITH_ARRAY` | **`DIRECT_TYPED`** | requer extração | não autorizado |
| autômatos | `DIRECT_WITH_ARRAY` | **`DIRECT_TYPED`** | requer extração | não autorizado |
| máquinas de estado | `DIRECT_WITH_ARRAY` | **`DIRECT_TYPED`** | requer extração | não autorizado |
| auditoria de transições | `REQUIRES_STATE_ENCODING` | **`REQUIRES_CERTIFIED_ENCODING`** | requer extração | não autorizado |
| workflows | `REQUIRES_STATE_ENCODING` | **`REQUIRES_CERTIFIED_ENCODING`** | requer extração | não autorizado |
| retries | `REQUIRES_STATE_ENCODING` | **`REQUIRES_CERTIFIED_ENCODING`** | requer extração | não autorizado |
| parsers | `REQUIRES_ABSTRACTION_PROOF` | inalterado | requer extração | não autorizado |
| pipelines | `REQUIRES_ABSTRACTION_PROOF` | inalterado | requer extração | não autorizado |
| agentes determinísticos | `REQUIRES_ABSTRACTION_PROOF` | inalterado | requer extração | não autorizado |
| jogos | `CONCEPTUAL_ONLY` | inalterado | — | — |

```text
DIRECT_TYPED                  3
REQUIRES_CERTIFIED_ENCODING   3
REQUIRES_ABSTRACTION_PROOF    3
CONCEPTUAL_ONLY               1
```

## O que mudou, exatamente

Antes, quem tinha o sistema em Lean precisava **construir a tabela à mão**
e não tinha teorema ligando uma coisa à outra. As três primeiras linhas
mudaram de "direto com `Array`" para "direto com o tipo": agora se fornece
`encode`, `decode`, as duas leis e `stepS`, e a tabela é construída **e
provada correspondente**.

As três seguintes melhoraram de "precisa codificar estados" para "precisa
de uma codificação **certificada**" — o requisito ficou mais preciso, não
mais fácil: continua sendo obrigação de quem modela produzir `encode`,
`decode` e as leis.

As três últimas **não** melhoraram, e a razão é a mesma de antes: o
espaço de estados real não é finito nem conhecido, e nenhuma codificação
pode ser fornecida.

## O registro obrigatório

```text
A frente prova que a tabela construida corresponde ao SISTEMA TIPADO
que forneceu a codificacao.

Ela NAO prova que esse sistema tipado representa corretamente um
programa, servico, workflow, agente ou processo fisico.
```

Essa obrigação pertence a quem produz a abstração. `ENC-GAP-019`
permanece aberto, e provavelmente permanecerá.

## Custo prático herdado

O detector recompõe as iteradas para cada par candidato, sem memoização.
Agora há um custo adicional visível: `Array.ofFn` percorre o domínio
inteiro na construção. Nenhum dos dois foi formalizado —
`complexity_model: NOT_FORMALIZED`.

## Nenhuma integração

```text
integracoes criadas   0
binarios              0
alvos executaveis     0
parsers               0
APIs externas         0
```

E, pela sétima vez neste laboratório: reutilização em software não
transforma resultado padrão em descoberta científica.
