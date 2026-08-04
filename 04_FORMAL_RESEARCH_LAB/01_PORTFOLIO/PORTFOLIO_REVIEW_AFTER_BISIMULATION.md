---
document_id: PORTFOLIO-REVIEW-AFTER-BISIMULATION
reviewed_at: 2026-08-04
selected_work_item: LAB-GOV-DECISION-LEDGER-001
alternatives_compared: 7
probes_compiled_in_this_gate: 15
probe_exit: 0
---

# Revisão de portfólio — depois da fronteira de bissimulação

## Estado de entrada

```text
FOUND-BISIMULATION-BOUNDARY-001   VERIFIED / APPROVED   ENCERRADA
frentes encerradas                10
claims no ledger                  24
lake build                        exit 0, 8775 jobs
authorized_action                 PORTFOLIO_REVIEW_REQUIRED
```

## As sete alternativas

| | Candidato | Veredito |
|---|---|---|
| A | Certificado de reflexão decidível / executável | **REJEITADO** |
| B | Finitude da órbita concreta, `ABS-GAP-021` | selecionado **depois** |
| C | Quocientes pelo núcleo da abstração, `ABS-GAP-016` | adiado |
| D | Invariância do witness sob recodificação, `ENC-GAP-020` | rejeitado |
| E | Bibliografia de semântica de concorrência, `BIS-GAP-010` | adiado |
| F | Extração, CLI, parser, formato externo | rejeitado |
| G | **Integridade do registro de decisões** | **SELECIONADO** |

## Por que A foi rejeitado

A hipótese natural — "uma verificação numa janela finita descarrega
`OrbitSeparating`" — foi formalizada em probe e **compila**. Foi
rejeitada mesmo assim, por três razões que a compilação não responde.

```text
1. A hipotese da janela IMPLICA a hipotese da equacao unica.
   WindowSeparating(b+p) instanciada em (b+p, b) ja da a conclusao.
   Custo: (b+p+1)^2 implicacoes para comprar o que 1 implicacao compra.

2. O excedente — o certificado OrbitSeparating reutilizavel — nao tem
   NENHUM consumidor. OrbitSeparating e hipotese de exatamente uma
   declaracao nao-teste em todo o laboratorio, consumida em exatamente
   um par de indices.

3. "Decidivel" e pago com DecidableEq C e stepC computavel — exatamente
   as hipoteses que a frente anterior mede como NAO exigidas.
```

O regime computacional é **estritamente dominado**: com `DecidableEq C`
e `stepC` computável em mãos, perguntar diretamente "existe `i < j ≤ b+p`
com `s_i = s_j`" custa o mesmo, é completo exatamente quando o caminho
caro é, e não consome `abstract`, `stepA`, `Semiconj`, codificação nem
execução da análise.

**Registro honesto:** a proposta era minha. Foi derrubada por verificação
adversarial antes de virar frente, não depois de virar commit.

## O que sobreviveu de A, e virou B

Uma única declaração de A não é reescrita de nada já publicado:

```text
o conjunto alcancavel de um sistema concreto SEM NENHUMA estrutura de
finitude e limitado pelo numero de estados ABSTRATOS
```

Isso vira `FOUND-ORBIT-FINITENESS-001`, **a próxima frente**, depois de G.

## Duas objeções dos refutadores que o probe derrubou

Os refutadores afirmaram que `0 < period` e a cota `b + p ≤ n` são
**irrecuperáveis** da API pública, porque `analyze_reduce` é `private` e
alargar `analyzeTransitionTable_sound` tocaria frente encerrada.

O probe deste gate provou os dois, re-derivando a redução em namespace
novo, com API exclusivamente pública, sem tocar em nada encerrado:

```text
analyzeTransitionTable_bounds    0 < period  AND  b + p <= next.size
analyzeAbstractSystem_bounds     0 < period  AND  b + p <= n
probe exit                       0
arvore versionada suja           0
```

A condição de parada que eles anteciparam **não dispara**.

## Por que G vem primeiro

O `DECISION_LEDGER.yaml` termina em `DEC-014`. O `CHANGELOG.md` invoca
`DEC-015`, `DEC-016`, `DEC-017`, `DEC-018`, `DEC-020`, `DEC-021` e
`DEC-022` como autoridade de edições. Nenhuma dessas sete existe no
ledger.

Além disso `DEC-014` designa **duas decisões diferentes**: no ledger, o
endurecimento PENDENTE de `FROZEN_PARTIAL_RESULT` com `authority: null`;
no changelog, uma edição de sequência de gates no `labctl.py`. E
`DEC-019` nunca é citado — buraco na numeração.

```text
sete identificadores citados como autoridade, sem registro
uma colisao de identificador entre duas decisoes distintas
um buraco na numeracao
todos autorizam edicoes literais em 10_TOOLS/labctl.py
```

`labctl.py` é **o validador de todo gate**. Toda vez que um gate declarou
`labctl validate PASS`, o fez sob uma ferramenta modificada por edições
cuja autorização existe apenas na narrativa do changelog.

Este é o mesmo padrão de `LAB-GOV-FRONTMATTER-SCAN-001`: uma afirmação de
integridade que a instrumentação não sustentava. Aquele gate se pagou
dois gates depois, pegando duplicatas que eu mesmo introduzi. O
precedente é explícito — **corrigir o instrumento antes de usá-lo**.

## Por que não C, D, E, F

- **C** — o núcleo de uma semiconjugação é automaticamente uma
  congruência, então `stepC` desce e a abstração induzida é injetiva
  **por construção**: a igualdade "concreta" obtida no quociente é
  exatamente a igualdade abstrata, ou seja, a soundness observacional
  reescrita. Entra direto na armadilha de tautologia. Adiado, não
  rejeitado.
- **D** — `ENC-GAP-020` mantém o acoplamento à ordem de enumeração do
  detector que já o reprovou duas vezes.
- **E** — permanece **deliberadamente aberta**.
- **F** — distribuiria garantia sem contrato semântico.

## Escopo negativo desta seleção

```text
minimalidade de baseIndex ou period    NAO AUTORIZADA
Function.minimalPeriod                 NAO AUTORIZADO
quocientes                             NAO AUTORIZADOS
extracao, CLI, parser                  NAO AUTORIZADOS
reescrita de historia                  PROIBIDA
alteracao de frente encerrada          PROIBIDA
alteracao de entrada historica do CHANGELOG  PROIBIDA
```

A colisão de `DEC-014` será resolvida **sem reescrever o registro
histórico**: o texto do changelog permanece intacto e o ledger passa a
carregar o mapeamento explícito da citação.

## Próxima ação

```text
LAB_GOV_DECISION_LEDGER_CORRECTION_AUTHORIZED
```
