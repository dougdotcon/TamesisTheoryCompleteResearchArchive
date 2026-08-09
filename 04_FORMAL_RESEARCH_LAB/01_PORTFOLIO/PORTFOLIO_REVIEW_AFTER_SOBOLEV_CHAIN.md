---
document_id: PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09
reviewed_at: 2026-08-09
selected_work_items:
  - NS-PRESSURE-001
  - PVSNP-PHYS-001
  - YM-LIMIT-001
  - HODGE-CDK-001
  - BSD-HYP-MATRIX-001
excluded_work_item: TOE-INTERFACE-001
methodology_change: PARALLEL_EXECUTION_AUTHORIZED
requested_by: principal, sessão 2026-08-09
---

# Revisão de portfólio — depois da cadeia de Sobolev, abrindo paralelismo

## O que fechou desde a última revisão registrada

Cinco frentes de fundações (analise funcional/EDP) fecharam em sequência sem
gate de portfólio dedicado entre elas — o próprio defeito que
`LAB-CORR-VALIDATION-BLINDNESS-001` corrigiu na contabilidade, não na
matemática:

```text
FOUND-SPECTRAL-COUNTING-001       VERIFIED/APPROVED   N(lambda) nao-vazio, nao-acumulacao provada
FOUND-FOURIER-MULTIPLIER-L2-001   VERIFIED/APPROVED   multiplicador L2 corrigido (HasTemperateGrowth)
FOUND-ELLIPTIC-HEIGHT-001         VERIFIED/APPROVED   obrigacao D descarregada, TODO do Mathlib fechado
FOUND-LERAY-PROJECTOR-001         VERIFIED/APPROVED   projetor ortogonal, norma 1, DEC-056
FOUND-SOBOLEV-SPACE-001           VERIFIED/APPROVED   H^s como tipo, Banach
```

Todas com `mathematical_novelty: NONE`, `algorithmic_novelty: NONE`,
`research_role: FORMAL_FOUNDATION`. Nenhuma resolve nem aproxima a
resolução de Navier-Stokes; formam um kit de análise funcional (Sobolev,
Leray, Fourier, contagem espectral) que existia como pré-requisito
disperso e agora existe como código Lean verificado.

`LAB_STATE.md` também tinha uma lacuna própria: seu bloco estruturado
`closed_work_items` não continha `ENG-RUNTIME-SOUNDNESS-002` nem as cinco
frentes acima — só a tabela em prosa as registrava. Corrigido neste gate,
junto com este documento.

## A mudança pedida: paralelismo

O laboratório operou em série, uma frente por vez, desde `LAB-ARCH-001`.
Isso não era um limite estrutural — era a forma mais fácil de manter a
contabilidade de governança correta com um único agente por sessão. A
sessão atual foi explicitamente instruída a trabalhar **em várias
frentes ao mesmo tempo, com paralelismo e concorrência**, e a nunca
ficar ociosa entre ciclos.

Isso é autorizado aqui, sob três condições que preservam exatamente a
disciplina que o gate corretivo anterior existiu para restaurar:

```text
1. cada frente escreve SOMENTE dentro do seu proprio subdiretorio
   03_MILLENNIUM/0X_.../ (COMPUTATION, COUNTEREXAMPLES, FORMAL,
   RESULTS, REVIEWS, e os arquivos de topo ja escafoldados)
2. os arquivos de governanca compartilhados (LAB_STATE.md,
   RESEARCH_QUEUE.yaml, CHANGELOG.md, DECISION_LEDGER.yaml,
   CLAIM_LEDGER.yaml) sao escritos SOMENTE pela sessao orquestradora,
   em serie, depois que cada frente reporta — nunca concorrentemente
   por agentes de frente
3. labctl validate roda de novo, e o campo status e LIDO, depois de
   cada integracao — a regra validate_status_must_be_read se aplica
   igualmente sob concorrencia
```

Paralelismo é uma propriedade da execução, não uma isenção da
contabilidade. As regras de `governance_rules` em `LAB_STATE.md`
continuam valendo por frente.

## Por que estas cinco, e não outras

As seis frentes `SCOPED` nunca executadas do track `millennium` são:

```text
NS-PRESSURE-001      dep: LAB-BENCH-001 (VERIFIED)        execution_authorized: false → true
PVSNP-PHYS-001       dep: LAB-BENCH-001 (VERIFIED)        execution_authorized: false → true
YM-LIMIT-001         dep: LAB-BENCH-001 (VERIFIED)        execution_authorized: false → true
HODGE-CDK-001        dep: LAB-BENCH-001 (VERIFIED)        execution_authorized: false → true
BSD-HYP-MATRIX-001   dep: LAB-BENCH-001 (VERIFIED)        execution_authorized: false → true
TOE-INTERFACE-001    dep: FOUND-SEMIGROUP-001 (VERIFIED),
                          RH-NOGO-001 (FROZEN_PARTIAL_RESULT, não é VERIFIED),
                          NS-PRESSURE-001 (SCOPED, ainda não executado)
```

`TOE-INTERFACE-001` **fica de fora desta onda**: duas de suas três
dependências não estão satisfeitas. Abri-la agora violaria a própria
`RESEARCH_QUEUE.yaml` — não é um limite novo, é o registro existente.

As cinco restantes já tinham `authorized_next_gate` nomeado
individualmente na fila desde que foram escopadas, cada uma com
`dependencies: [LAB-BENCH-001]` apenas, e cada uma já possui um
diretório próprio, isolado, pré-escafoldado sob `03_MILLENNIUM/`. Isto
não é um plano novo — é a primeira vez que o laboratório executa um
plano de paralelismo que já estava desenhado na estrutura de diretórios
desde `LAB-ARCH-001`.

## O que esta onda é, e o que não é

Cada frente é uma **auditoria**, não uma tentativa de resolver o
problema de milênio correspondente:

```text
NS-PRESSURE-001     testar UMA hipotese sobre Hessiana de pressao — contraexemplo, correcao ou teorema condicional
PVSNP-PHYS-001      DEFINIR P_phys/NP_phys sem afirmar P != NP
YM-LIMIT-001        teorema de insuficiencia OU contraexemplo abstrato sobre sobrevivencia do gap em limites
HODGE-CDK-001       formalizar exatamente o que Cattani-Deligne-Kaplan prova e o que nao prova
BSD-HYP-MATRIX-001  particionar a literatura de BSD por hipotese/curva/posto/primo, sem unir teoremas indevidamente
```

Nenhuma frente pode declarar um Problema do Milênio resolvido — proibição
já existente em `AGENTS.md`, reafirmada aqui porque cinco frentes
simultâneas multiplicam a superfície onde isso poderia escapar sem
revisão.

## Postura epistêmica exigida desta onda

Cada uma destas cinco frentes tenta reconstruir, a partir de literatura
que só pode ler em parte, um resultado que não tem acesso direto — a
mesma posição de quem tenta desenhar uma árvore só a partir de descrição,
sem nunca ter visto uma. O produto certo não é uma reconstrução que
finge completude; é uma que **separa, de forma legível, o que foi
verificado do que foi aproximado**:

```text
verificado    citação recuperável (WebSearch) + lake build exit 0 quando ha Lean + prova em Lean/Python
aproximado    lido do ANALISE_CRITICA_*.md legado ou de memória de treino, sem fonte primária conferida nesta sessao
```

Cada `RESULTS/` ou `REVIEWS/` desta onda deve ter as duas seções
separadas. `AGENTS.md` já proíbe inventar referências; a seção
"aproximado" é onde uma afirmação não verificável vai para ficar visível
em vez de desaparecer disfarçada de resultado.

## O que isto NÃO afirma

```text
que qualquer Problema do Milenio ficou alcancavel
que exista novidade matematica ou algoritmica nas cinco frentes
que a execucao paralela substitua a leitura do campo status do validador
que a auditoria de literatura equivale a resultado formal (F != T)
```

## Trava consumida

`authorized_action` sai de `PORTFOLIO_REVIEW_REQUIRED` para
`PARALLEL_AUDIT_WAVE_IN_PROGRESS`. As cinco frentes citadas têm
`execution_authorized` promovido para `true` em seus respectivos
`STATUS.yaml`, citando este documento como autoridade.
