---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-SPECIFICATION-REVIEW
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
review_start_head: b83598392af465b5a8409ec809f8765196bfa63e
decision: FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_REVIEW_APPROVED
defects_found: 1
defects_corrected: 1
---

# Revisão de especificação

## Reexecução, nada herdado

O probe foi **rodado de novo neste gate**. Nenhum número abaixo vem do
gate anterior.

```text
REAL_PROBE3_EXIT       0
error_lines            0
git_dirty              0
Fintype no probe       0 ocorrencias
DecidableEq no probe   0 ocorrencias
instance declarations  0
arquivos Lean mudados  0
frentes encerradas     0 arquivos tocados
```

## Pegada medida agora

```text
Invariant.iterate                        propext
unreachable_of_invariant_ne              propext
invariant_orbitSeparating_iff_fixedPoint propext, Quot.sound
diag_unreachable                         propext, Quot.sound
```

Bate com o esperado na especificação. `Classical.choice` **não** aparece,
como previsto: a frente não atravessa `analyzeEncodedSystem`.

## O defeito que a revisão encontrou

A contagem derivada por script deu **12**; a especificação declarava
**10**.

```text
defs      4   Invariant, Reachable, invariantAbstraction, diagStep
theorems  8   semiconj, iterate, unreachable_of_invariant_ne, pair,
              orbitSeparating_iff_fixedPoint, diagStep_invariant,
              diag_unreachable, constant_invariant_proves_nothing
total    12
```

Classificação correta:

```text
publicas                    8   (3 defs + 5 teoremas)
TEST_ONLY residentes        2   diagStep, diagStep_invariant
testes                      2   diag_unreachable,
                                constant_invariant_proves_nothing
                           --
                           12
```

**As oito assinaturas congeladas conferem.** O erro estava apenas no
campo `probe.declarations_compiled`, que omitiu os dois testes.

É precisamente a contagem agregada escrita à mão que
`LAB_STATE.md` proíbe: *"Não derivar contagens agregadas à mão: verificar
cabeçalho contra as entradas por script"*. A regra existia, e eu não a
apliquei ao próprio campo.

### Como foi corrigido

O campo foi corrigido contra a derivação, com a decomposição explícita.
**A classificação não foi alterada para caber no número** — ela já estava
certa; o número é que estava errado.

Documentos históricos — a entrada de changelog e
`PORTFOLIO_REVIEW_INVARIANT_TOOLKIT.md` — **não foram reescritos**. Quem
ler `10` neles deve resolver por este documento. Mesmo princípio aplicado
à colisão de `DEC-014`: reescrever a evidência apagaria o defeito.

## Os oito itens da revisão

| # | Item | Veredito |
|---|---|---|
| 1 | `Invariant` é definicionalmente `Semiconj ... id` | **CONFIRMADO** |
| 2 | `Invariant.semiconj` é o termo `h`, não uma prova | **CONFIRMADO** |
| 3 | Zero typeclasses em qualquer assinatura | CONFIRMADO |
| 4 | Zero `Fintype`, zero `DecidableEq` | CONFIRMADO |
| 5 | O teorema negativo exige só `Invariant` e `start` | CONFIRMADO |
| 6 | A instância usa tipo infinito | CONFIRMADO |
| 7 | Contagem derivada = declarada | **CORRIGIDO** |
| 8 | Frentes encerradas intocadas | CONFIRMADO |

## O item 2, que é o conteúdo da frente

```text
semiconj_body   = h
IS_DEFINITIONAL = True
```

Verificado por extração do corpo do teorema, não por leitura. `Invariant`
e `Function.Semiconj abstract stepC id` são a mesma proposição, e a
ponte não custa nada.

## O item 5, que impede a degeneração

O teorema negativo poderia ter degenerado se exigisse finitude,
decidibilidade ou hipótese sobre a órbita. Sua assinatura tem exatamente
uma hipótese e um ponto inicial. Nada mais entra.

## A assimetria, reconferida

```text
suficiencia   PROVADA        unreachable_of_invariant_ne
necessidade   NAO AFIRMADA   INV-GAP-001, aberta
```

`constant_invariant_proves_nothing` compila e está na frente exatamente
para tornar a assimetria verificável em Lean, não só declarada em prosa.

## Decisão

```text
FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_REVIEW_APPROVED
```

## Ressalva de independência

Este gate foi executado pelo mesmo agente que escreveu a especificação.
Não substitui revisão externa. O que sustenta a aprovação é o que foi
**reexecutado** — e, neste gate, também o que a derivação por script
**recusou**.
