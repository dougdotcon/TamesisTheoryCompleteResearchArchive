---
document_id: FSG2-C3-BOUNDARY
status: BINDING
relates_to: FOUND-SEMIGROUP-001
---

# Fronteira do modelo C3

## O que C3 tem de especial

O modelo verificado em `FOUND-SEMIGROUP-001` — monoide cíclico de três
transições agindo sobre três regimes — possui quatro propriedades:

```text
acao fiel                         FOUND-SG-012 (apply_faithful)
acao transitiva                   FOUND-SG-013 (apply_transitive)
alcancabilidade simetrica         consequencia de C3 ser um grupo
periodicidade desde o instante 0  forward^3 = identidade (FOUND-SG-006)
```

## Essas propriedades **não** são gerais

Nenhuma delas é consequência de uma ação finita de monoide. Cada uma tem
contraexemplo verificado em `FOUND-SEMIGROUP-002`:

| Propriedade de C3 | Refutada em geral por |
|---|---|
| ação fiel | `CE-004` |
| ação transitiva | `CE-002` |
| alcançabilidade simétrica | `CE-001` |
| periodicidade desde `n = 0` | `CE-003` |

## Leitura correta — vinculante

```text
CORRETO:
Para cada uma das quatro propriedades existe uma acao finita de monoide na
qual ela FALHA. Logo nenhuma delas pode ser promovida a teorema universal.

ERRADO:
As quatro propriedades falham simultaneamente em toda acao finita.
```

A leitura errada seria falsa: em `C3` as quatro valem ao mesmo tempo, e é
justamente por isso que `C3` **não serve** como caso de teste da parte
interessante do alvo — ele é bom demais.

## Consequência prática

O modelo `C3` continua válido e verificado. **Nenhum teorema de
`FOUND-SEMIGROUP-001` foi alterado neste gate.** O que muda é o que se pode
concluir dele: nada além do próprio modelo.

Qualquer texto futuro que use `C3` como evidência de comportamento geral
está errado, e os contraexemplos existem para tornar esse erro detectável.

## Onde a fronteira já existia

`FOUND-SG-GAP-004` (frente anterior) já registrava que nenhuma ponte formal
entre o modelo e o vocabulário TRI/TDTR havia sido construída, e que
qualquer uso científico exigiria gate próprio. Este documento estende a
mesma disciplina às propriedades **matemáticas** do modelo.
