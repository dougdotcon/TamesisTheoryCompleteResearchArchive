---
document_id: FSG2-NOVELTY-BOUNDARY
status: BINDING
---

# FOUND-SEMIGROUP-002 — Fronteira de novidade

Documento vinculante. Qualquer texto produzido sobre esta frente deve caber
dentro destes limites.

## Registro literal

```text
Os resultados propostos são fatos padrão de dinâmica finita,
ações de monoides e princípio da casa dos pombos.

A eventual periodicidade de uma função em um conjunto finito
não é uma descoberta matemática.

O valor do work item está em:

- formalização reutilizável;
- integração com o laboratório;
- rastreabilidade;
- contraexemplos;
- separação entre órbita, alcançabilidade e periodicidade;
- criação de uma base para modelos discretos futuros.
```

## Proibido afirmar

```text
nova teoria do tempo;
nova teoria da transicao;
validacao de TRI;
validacao de TDTR;
lei universal da dinamica;
resultado fisico;
solucao de problema aberto.
```

## Tabela do que dizer

| ❌ Não escrever | ✅ Escrever |
|---|---|
| "Provamos que todo sistema discreto entra em ciclo" | "Formalizamos que toda função sobre um tipo finito é eventualmente periódica — casa dos pombos" |
| "Descobrimos a estrutura das transições de regime" | "Separamos, em Lean, alcançabilidade, órbita e periodicidade eventual" |
| "O modelo C3 mostra que a dinâmica é cíclica" | "O modelo C3 é um exemplo; `CE-002` e `CE-004` mostram que suas propriedades não são gerais" |
| "Isto fundamenta TRI/TDTR" | "Nenhuma ponte com TRI/TDTR foi construída; ver `FOUND-SG-GAP-004`" |
| "Um novo resultado em sistemas dinâmicos" | "Um núcleo formal padrão, reutilizável" |
| "O período do sistema é λ" | "O período **de uma órbita** é λ; ele depende do estado inicial" |

## Contexto histórico honesto

A afirmação de que uma sequência iterada em conjunto finito deve repetir é
elementar e consta de qualquer texto introdutório de teoria dos números ou
combinatória. Algoritmos que exploram essa estrutura — detecção de ciclo de
Floyd, "tortoise and hare" — são material padrão desde os anos 1960.

Este laboratório **não obteve nem auditou** fonte primária alguma de teoria
de semigrupos ou dinâmica discreta (`FOUND-SG-GAP-003` permanece
`NOT_AUDITED`). Portanto:

```text
Nenhuma afirmacao de prioridade historica pode ser feita.
Nenhuma atribuicao a autor especifico pode ser feita.
O contexto acima eh conhecimento geral, nao resultado de auditoria.
```

## A tentação específica desta frente

O vocabulário do arquivo legado — "regimes", "transições" — convida a ler o
modelo `C3` como se fosse uma teoria física de mudança de estado. Não é. É
um monoide cíclico de três elementos agindo sobre um conjunto de três
elementos, e nada mais.

`FOUND-SEMIGROUP-002` estuda **ações finitas de monoides**, um objeto
matemático padrão. Se um gate futuro quiser construir uma ponte entre este
formalismo e qualquer alegação sobre o mundo, essa ponte precisará de gate
próprio, fonte própria e auditoria própria — exatamente como
`FOUND-SG-GAP-004` já registrou.
