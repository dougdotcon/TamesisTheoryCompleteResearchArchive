---
document_id: PORTFOLIO-REVIEW-UNIFORM-2026-08-04
reviewed_at: 2026-08-04
selected_work_item: FOUND-UNIFORM-PRIMREC-001
queue_total: 22
queue_verified: 15
queue_frozen: 1
queue_scoped_open_problems: 6
feasibility_probe_exit: 0
---

# Revisão de portfólio — depois da ponte

## O estado, contado e não lembrado

```text
22 itens na fila
15 VERIFIED
 1 FROZEN_PARTIAL_RESULT   RH-NOGO-001
 6 SCOPED                  os problemas em aberto, nunca executados
```

As **16 linhas próprias** do laboratório — 15 encerradas e uma congelada
— estão fechadas. Os 6 `SCOPED` não são linhas do laboratório: são os
problemas que ele gostaria de atacar.

## O que a ponte mudou, e o que não mudou

`FOUND-COMPUTABILITY-BRIDGE-001` respondeu as cinco perguntas. Três
respostas foram `SIM, por finitude` — verdadeiras e **vazias de conteúdo
algorítmico**. Duas foram `NÃO`.

```text
mudou      o laboratorio tem endereco na hierarquia do Mathlib
           e sabe exatamente quanto esse endereco vale: nada
nao mudou  continua sem qualquer resultado de computabilidade
           que dependa de um algoritmo seu
```

Nenhum dos 6 problemas ficou mais perto. Dizer o contrário seria o
teatro que `ATTACK_READINESS.md` já proibiu.

## A única candidata com conteúdo

`CB-GAP-001`, o nível uniforme:

```lean
Primrec₂ analyzeTransitionTable
```

Sobre `RawTransitionTable × Nat` o domínio é **infinito**.
`Primrec.dom_finite` não se aplica. A conclusão passa a depender do que a
função faz — pela primeira vez no laboratório.

## Viabilidade, medida por elaboração

Um probe descartável, `exit 0`, árvore intocada. Não é opinião sobre
dificuldade; são teoremas que compilaram:

```lean
theorem primrec_stepList : Primrec₂ stepList                       COMPILA
theorem primrec_runList  : Primrec (fun p => runList ...)          COMPILA
theorem primrec_validList : PrimrecPred (fun q => ValidList ...)   COMPILA
```

O segundo é o coração: **iterar a tabela codificada é primitivo
recursivo**, via `Primrec.nat_iterate`. O terceiro reproduz as quatro
cláusulas de `CycleWitness.Valid` na mesma ordem e no mesmo aninhamento.

## A arquitetura que o probe validou

O obstáculo real nunca foi computabilidade — é **tipo dependente**.
`analyzeTransitionTable` atravessa `Fin t.next.size`, e `Primrec` não
conversa com isso.

```text
1. reformular sobre List Nat, sem tipo dependente     PROBE OK
2. provar Primrec da reformulacao                     PROBE OK (nucleo)
3. provar a busca limitada Primrec                    NAO PROBADO
4. casar a reformulacao com analyzeTransitionTable    NAO PROBADO, e o grosso
```

Os passos 1 e 2 estão medidos. O 3 tem as ferramentas à vista
(`list_range`, `list_findIdx`). O **4 é o volume da frente**, e é prova
de semântica, não de computabilidade.

## O que esta seleção NÃO afirma

```text
que o nivel uniforme ja esteja provado
que fecha-lo defina classe de complexidade
que fecha-lo aproxime P vs NP
que os outros 5 problemas tenham mudado de status
que exista modelo de custo depois dele
```

Fechar `CB-GAP-001` dá ao laboratório **um** resultado de computabilidade
que depende de um algoritmo seu. Isso é pré-requisito de conversa sobre
custo. Não é conversa sobre custo.

## A seleção

```text
FOUND-UNIFORM-PRIMREC-001
```

Critério: é a única lacuna aberta do laboratório cuja resolução produz
informação algorítmica, e sua viabilidade foi **medida**, não estimada.

## O veredito honesto sobre prontidão

```text
NS-PRESSURE-001    EDP e analise de fluidos          NAO
YM-LIMIT-001       QFT construtiva                   NAO
HODGE-CDK-001      geometria algebrica               NAO
BSD-HYP-MATRIX-001 aritmetica de curvas, Iwasawa     NAO
RH-NOGO-001        calculo pseudodiferencial         NAO
PVSNP-PHYS-001     estrutural sobre computabilidade  AINDA NAO
```

Para `PVSNP-PHYS-001` faltam, em ordem: o nível uniforme, um modelo de
custo, e então uma reavaliação. Duas frentes e um gate de decisão — e o
modelo de custo é **escolha**, não descoberta.

Os outros cinco continuam com primeiro passo bibliográfico e custo
`very_high` declarado desde 2026-07-31. Nada nesta rodada mudou isso.
