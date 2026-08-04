---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-README
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
specification_status: READY_FOR_REVIEW
research_role: FORMAL_PROOF_TOOL
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# FOUND-INVARIANT-UNREACHABILITY-001

## O que a frente é

Uma **ferramenta**, não um resultado. A peça que faltava para o
laboratório usar abstração no sentido oposto ao que usou até aqui.

```text
dez frentes: abstracao para COLAPSAR    achar recorrencia
esta frente: abstracao para SEPARAR     provar impossibilidade
```

## A observação que torna a frente barata

Um invariante **é** uma semiconjugação para o sistema parado:

```text
Invariant abstract stepC   :=  forall c, abstract (stepC c) = abstract c
Semiconj abstract stepC id :=  forall c, abstract (stepC c) = id (abstract c)
```

As duas são iguais por definição. `Invariant.semiconj` é o próprio termo
`h`, sem conversão, sem `Iff`, sem transporte. Toda a maquinaria de
iteradas já provada em `Function.Semiconj.iterate_right` fica disponível
de graça.

## O teorema que a frente entrega

```text
um invariante que SEPARA dois estados prova que um nao alcanca o outro
```

É a forma geral de todo argumento de paridade, coloração ou monovariante
— e o laboratório não tinha nenhuma peça dessas.

## O teorema NEGATIVO que a frente entrega

```text
para abstracoes invariantes, OrbitSeparating vale
EXATAMENTE nos pontos fixos
```

Portanto invariantes **nunca** certificam recorrência. Os dois usos da
mesma máquina são incompatíveis fora dos pontos fixos, e essa
incompatibilidade é um teorema, não uma observação.

## O que a frente NÃO entrega

```text
invariante separador NAO e necessario para inalcancabilidade
invariante constante NAO prova nada
nenhuma finitude e usada, nem obtida
nenhum problema de milenio e atacado
```

`constant_invariant_proves_nothing` existe exatamente para impedir a
leitura ao contrário.

## Documentos

```text
SPECIFICATION_DECISION.md   assinaturas congeladas e recorte
STOP_CONDITIONS.md          o que aborta a frente
GAPS.md                     o que fica aberto, declarado antes
STATUS.yaml                 estado operacional
```
