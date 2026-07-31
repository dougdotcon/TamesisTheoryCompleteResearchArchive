---
document_id: FSG2-RESULT-BOUNDARY
status: BINDING
---

# FOUND-SEMIGROUP-002 — Fronteira do resultado

## Registro literal

```text
Foi provado:

- alcançabilidade é reflexiva e transitiva;
- invariantes completos são preservados por alcançabilidade;
- toda trajetória de uma função em um tipo finito é eventualmente
  periódica, com os limites formalizados;
- a iteração de um elemento de monoide em um tipo finito é
  eventualmente periódica;
- propriedades especiais de C3 falham em ações finitas gerais.

Não foi provado:

- unicidade da cauda;
- minimalidade do período;
- decomposição canônica completa;
- classificação de todas as ações finitas;
- qualquer resultado sobre sistemas infinitos;
- qualquer resultado físico;
- TRI ou TDTR;
- novidade matemática.
```

## Leitura obrigatória da última linha do bloco "foi provado"

A frase

> propriedades especiais de C3 falham em ações finitas gerais

significa **exatamente**:

```text
Para cada uma das quatro propriedades, EXISTE um contraexemplo:
uma acao finita de monoide na qual aquela propriedade falha.
```

e **não**:

```text
Todas as quatro propriedades falham SIMULTANEAMENTE em toda acao finita.
```

A leitura errada seria falsa: em `C3` as quatro valem ao mesmo tempo.
Cada contraexemplo refuta a **universalidade** de uma propriedade, um a um.

## Correção registrada sobre invariância

A redação da especificação dizia que `IsInvariantUnder a` seria
"estritamente mais fraca" que `IsInvariant`. **Como afirmação universal,
isso é falso.** O que está provado é apenas:

```text
IsInvariant I  ==>  IsInvariantUnder a I,   para todo a.   [IsInvariant.under]
```

A recíproca **não** é enunciada nem negada em geral. Ela é falsa em ações
apropriadas e **verdadeira** quando `a` gera `M` — caso em que as duas
noções coincidem. Nenhuma afirmação de estrita fraqueza uniforme é feita.

## Novidade

```yaml
mathematical_novelty: NONE
```

Periodicidade eventual de uma função em conjunto finito é o **princípio da
casa dos pombos**. Alcançabilidade reflexiva e transitiva é a definição de
preorder. Nada aqui é descoberta.

O valor é: formalização reutilizável, separação explícita das três camadas,
ponte auditada com a API da Mathlib (incluindo a armadilha do
`minimalPeriod`), e contraexemplos que impedem sobregeneralização.

## Proibido afirmar

```text
nova teoria;
descoberta;
fisica;
tempo;
entropia;
TRI;
TDTR;
teoria de tudo.
```

## Tabela do que dizer

| ❌ Não escrever | ✅ Escrever |
|---|---|
| "Provamos que todo sistema discreto entra em ciclo" | "Formalizamos que toda função sobre um tipo finito é eventualmente periódica" |
| "O período do sistema é λ" | "O período **daquela órbita** é λ; ele depende do estado inicial" |
| "C3 mostra que a dinâmica é cíclica" | "C3 é um exemplo; `CE-001`–`CE-004` refutam a generalização de suas propriedades" |
| "Invariância sob um gerador é mais fraca" | "Invariância total implica invariância sob cada gerador; a recíproca pode falhar, mas não universalmente" |
| "Refutamos a simetria com o grafo de `f`" | "Refutamos a simetria com uma **ação de monoide**; o grafo de `f` refutaria apenas a alcançabilidade por aquele gerador" |
| "Isto fundamenta TRI/TDTR" | "Nenhuma ponte com TRI/TDTR foi construída" |

## Bibliografia

`FSG2-GAP-009` permanece `NOT_AUDITED`: nenhuma fonte primária de teoria de
semigrupos ou dinâmica discreta foi obtida por este laboratório. Portanto
**nenhuma afirmação de prioridade histórica ou atribuição a autor é
permitida**.
