---
document_id: RT-REUSE-MATRIX
integrations_created: 0
---

# Matriz de reutilização

Três camadas, e a diferença entre elas é o núcleo desta matriz:

```text
uso DENTRO do Lean            disponivel hoje
uso APOS extracao             NAO autorizado
uso INTEGRADO a sistemas      NAO autorizado
```

| Aplicação | Classificação | Dentro do Lean | Após extração | Integrado |
|---|---|---|---|---|
| configurações finitas | `DIRECT_WITH_ARRAY` | a configuração **é** a tabela | requer extração | não autorizado |
| autômatos | `DIRECT_WITH_ARRAY` | estados já numerados | requer extração | não autorizado |
| máquinas de estado | `DIRECT_WITH_ARRAY` | transição total já é `Nat → Nat` | requer extração | não autorizado |
| auditoria de transições | `REQUIRES_STATE_ENCODING` | o log precisa virar tabela | requer extração | não autorizado |
| workflows | `REQUIRES_STATE_ENCODING` | estados precisam de numeração estável | requer extração | não autorizado |
| retries | `REQUIRES_STATE_ENCODING` | o tempo precisa ser abstraído para fora do estado | requer extração | não autorizado |
| parsers | `REQUIRES_ABSTRACTION_PROOF` | pilha e lookahead não são finitos | requer extração | não autorizado |
| pipelines | `REQUIRES_ABSTRACTION_PROOF` | etapas com efeitos e identificadores | requer extração | não autorizado |
| agentes determinísticos | `REQUIRES_ABSTRACTION_PROOF` | o ambiente costuma entrar no estado | requer extração | não autorizado |
| jogos | `CONCEPTUAL_ONLY` | mais de um agente; `f : X → X` não os modela | — | — |

```text
DIRECT_WITH_ARRAY          3
REQUIRES_STATE_ENCODING    3
REQUIRES_ABSTRACTION_PROOF 3
CONCEPTUAL_ONLY            1
OUT_OF_SCOPE               0
```

## O ganho em relação à frente anterior

`FOUND-CYCLE-DETECTION-001` classificava **seis** das dez aplicações como
`REQUIRES_ADAPTER`, porque o detector só aceitava tipos definidos em
compilação. Com o adaptador, **três** passam a ser diretas: quem já tem a
tabela não precisa de mais nada além de `Array Nat` e `Nat`.

As outras seis não melhoraram, e a razão é honesta: o obstáculo delas
nunca foi a interface, e sim o fato de o espaço de estados real não ser
finito nem conhecido.

## O registro obrigatório

```text
O adaptador prova que a tabela fornecida eh analisada corretamente.

Ele NAO prova que a tabela representa corretamente um sistema
externo real.
```

Essa obrigação pertence a quem produz a abstração, ou a uma futura
formalização específica do sistema integrado. `RT-GAP-017` permanece
aberto, e provavelmente permanecerá: prová-la exigiria um modelo formal
do sistema real.

## Custo prático herdado

O detector subjacente recompõe as iteradas para cada par candidato, sem
memoização (`CD-GAP-019`). Para `card X` pequeno é irrelevante; para
grande, a busca limitada é a implementação errada — e é por isso que
Floyd e Brent existem, ambos **não autorizados**.

## Nenhuma integração

```text
integracoes criadas         0
binarios                    0
alvos executaveis do Lake   0
parsers                     0
APIs externas               0
```

E, pela sexta vez neste laboratório: reutilização em software não
transforma resultado padrão em descoberta científica.
