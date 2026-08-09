---
document_id: QCU-SCOPE
work_item_id: QCU-001
status: UNSCOPED
---

# Problema 8 (extensão do laboratório) — Unificação de Mecânica Clássica e Mecânica Quântica

## Nota de honestidade obrigatória, antes de qualquer outra coisa

Este **NÃO** é um dos sete Problemas do Milênio do Clay Mathematics
Institute (P vs NP, Hodge, Riemann, Yang-Mills, Navier-Stokes, BSD,
Poincaré — este último resolvido por Perelman e usado como benchmark em
`00_POINCARE_BENCHMARK/`). Não há prêmio de US$1.000.000, não há
reconhecimento oficial de instituição alguma, e não há um enunciado
único e universalmente aceito do que "unificação de mecânica clássica e
quântica" significa formalmente — ao contrário dos seis problemas Clay
em aberto que este laboratório rastreia, cada um dos quais TEM um
enunciado matemático preciso.

Este item é adicionado aqui **a pedido explícito do usuário**, como uma
extensão numerada informalmente como "problema 8" para o rastreamento
interno deste laboratório -- não como afirmação de que se trata de um
problema de milênio reconhecido.

## Por que isso importa para o escopo

Antes de qualquer trabalho formal em Lean fazer sentido, a própria
ambiguidade do problema precisa ser resolvida em um `target_statement`
específico, demonstrável-ou-refutável -- exatamente como todo outro item
de `RESEARCH_QUEUE.yaml` exige. "Unificar mecânica clássica e quântica"
cobre facetas genuinamente distintas, sem consenso sobre qual (se
alguma) é "a" unificação:

```text
- Princípio de correspondência / limite clássico ħ→0 (teorema de
  Ehrenfest, aproximação WKB)
- Quantização por deformação (teorema de formalidade de Kontsevich --
  variedades de Poisson → produtos-estrela)
- Quantização geométrica (variedades simpléticas → espaços de Hilbert)
- Formalismo de Wigner-Weyl-Moyal (mecânica quântica no espaço de fase)
- Unificação categorial/funtorial (quantização como funtor, ao estilo TQFT)
- O "problema da medida" e interpretações de QM (Copenhagen, muitos-
  mundos, onda-piloto) -- terreno filosoficamente contestado, fora de
  escopo formal a menos que reduzido a um enunciado algebrico preciso
```

Nenhuma dessas facetas foi escolhida ainda. Nenhuma prova, definição, ou
linha de Lean foi escrita para este item.

## Relação com `TOE-INTERFACE-001` (`04_TOE_SYNTHESIS/`)

Unificação quântico-clássica é um CASO ESPECÍFICO da teoria geral de
"regimes, interfaces, invariantes, obstruções e transições" que
`TOE-INTERFACE-001` já mira, sem equação mestre única (ver
`TOE_SCOPE.md`). Registrar isto como item separado é um recorte de
escopo mais estreito, não uma duplicação -- mas as duas frentes devem
permanecer cross-referenciadas, e qualquer decisão futura de fundir os
dois itens precisa de gate próprio.

## Status

`UNSCOPED`. Nenhum `target_statement` escolhido, nenhuma dependência
declarada, nenhum trabalho formal autorizado. Requer uma revisão de
portfólio dedicada -- que exige primeiro escolher UMA faceta concreta
da lista acima -- antes de qualquer `FORMALIZATION` ser autorizada.
