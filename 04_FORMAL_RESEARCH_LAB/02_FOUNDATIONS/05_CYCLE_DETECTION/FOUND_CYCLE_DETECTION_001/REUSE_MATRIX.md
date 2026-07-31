---
document_id: FCD-REUSE-MATRIX
integrations_created: 0
---

# Matriz de reutilização

Três camadas devem ser distinguidas, e a diferença entre elas é o núcleo
desta matriz:

```text
uso DENTRO do Lean          disponivel hoje
uso APOS extracao           nao autorizado; CD-GAP-014
uso em SISTEMAS REAIS       nao autorizado; nenhuma integracao existe
```

| Aplicação | Classificação | Dentro do Lean | Após extração | Sistemas reais |
|---|---|---|---|---|
| detecção de loops | `DIRECT_REUSE` | sim — é literalmente o que o detector faz | requer extração | não autorizado |
| autômatos determinísticos | `DIRECT_REUSE` | sim, se o tipo de estados for `Fintype` com `DecidableEq` | requer extração | não autorizado |
| máquinas de estado | `REQUIRES_ADAPTER` | a transição precisa virar `f : X → X` total | requer extração | não autorizado |
| auditoria de transições | `REQUIRES_ADAPTER` | precisa de um adaptador do log para `f` | requer extração | não autorizado |
| parsers | `REQUIRES_ADAPTER` | o estado do parser raramente é `Fintype` | requer extração | não autorizado |
| pipelines | `REQUIRES_ADAPTER` | idem; e as etapas costumam ter efeitos | requer extração | não autorizado |
| retries | `REQUIRES_ADAPTER` | o estado inclui tempo, que não é finito | requer extração | não autorizado |
| workflows | `REQUIRES_ADAPTER` | idem | requer extração | não autorizado |
| jogos finitos | `CONCEPTUAL_ONLY` | jogos têm mais de um agente; `f : X → X` não os modela | — | — |
| agentes discretos | `CONCEPTUAL_ONLY` | idem, salvo agente único e determinístico | — | — |

```text
DIRECT_REUSE       2
REQUIRES_ADAPTER   6
CONCEPTUAL_ONLY    2
OUT_OF_SCOPE       0
```

## As duas hipóteses que governam a reutilização

```text
Fintype X       o espaco de estados precisa ser finito E conhecido
DecidableEq X   estados precisam ser comparaveis por igualdade
```

A maior parte dos "espaços de estado" de software real falha na primeira:
um parser com pilha, um pipeline com timestamps ou um workflow com
identificadores não são `Fintype`. É por isso que seis das dez aplicações
são `REQUIRES_ADAPTER` e não `DIRECT_REUSE` — o adaptador, na prática, é
uma **abstração finita** do estado, e a correção dessa abstração não é
fornecida por esta frente.

## Custo prático

`CD-GAP-019` permanece aberto: o detector recompõe as iteradas para cada
par candidato, sem memoização. Para `card X` pequeno isso é irrelevante;
para `card X` grande, a busca limitada é a implementação errada — e é
exatamente por isso que Floyd e Brent existem, ambos **não autorizados**
nesta versão.

## Nenhuma integração

```text
integracoes criadas          0
binarios                     0
alvos executaveis do Lake    0
APIs externas                0
```

E, pela quarta vez neste laboratório: reutilização em software não
transforma resultado padrão em descoberta científica.
