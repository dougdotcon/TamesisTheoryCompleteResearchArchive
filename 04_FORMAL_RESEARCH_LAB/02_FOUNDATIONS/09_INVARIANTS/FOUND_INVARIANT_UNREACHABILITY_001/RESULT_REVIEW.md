---
document_id: FOUND-INVARIANT-UNREACHABILITY-001-RESULT-REVIEW
work_item_id: FOUND-INVARIANT-UNREACHABILITY-001
review_start_head: 27b1972cab6906f8866a7aa46a640760b3615495
decision: FOUND_INVARIANT_UNREACHABILITY_001_RESULT_REVIEW_APPROVED
---

# Revisão de resultado

## Reexecução independente

Nada foi herdado do gate de formalização. O build e as contagens foram
**rodados de novo aqui**.

```text
lake build             REAL_BUILD_EXIT 0, 8782 jobs, 0 erros reais
contagem derivada      8 publicas (3 defs, 5 teoremas), 2 TEST_ONLY
Fintype                0
DecidableEq            0
instancias             0
tokens proibidos       0 em toda a arvore Lean
frentes encerradas     0 arquivos tocados
pytest                 34 passed
labctl validate        PASS, 0 erros
varredura YAML         0 duplicatas
citacoes DEC           30 registradas, 0 sem registro
```

## Os nove itens

| # | Item | Verdito |
|---|---|---|
| 1 | `Invariant` é definicionalmente `Semiconj ... id` | CONFIRMADO |
| 2 | `Invariant.semiconj` sem pegada alguma | CONFIRMADO |
| 3 | A ferramenta compila e é consumível | CONFIRMADO |
| 4 | `diag_unreachable` prova sobre tipo infinito | CONFIRMADO |
| 5 | O teorema negativo compila | CONFIRMADO |
| 6 | Zero typeclasses no núcleo | CONFIRMADO |
| 7 | `Classical.choice` ausente da frente inteira | CONFIRMADO |
| 8 | Contagem derivada = congelada | CONFIRMADO |
| 9 | Frentes encerradas intocadas | CONFIRMADO |

## Pegada, medida por declaração

```text
Invariant.semiconj                        SEM PEGADA
invariantAbstraction                      SEM PEGADA
constant_invariant_proves_nothing         SEM PEGADA
Invariant.iterate                         propext
unreachable_of_invariant_ne               propext
Invariant.pair                            propext
invariant_orbitSeparating_iff_fixedPoint  propext, Quot.sound
diagStep_invariant                        propext, Quot.sound
diag_unreachable                          propext, Quot.sound
```

`Classical.choice` **não aparece em lugar nenhum**. A frente não
atravessa `analyzeEncodedSystem`: não há `Array`, não há tabela, não há
execução. A previsão da especificação foi conferida contra a medição, e
bateu.

Que `Invariant.semiconj` não tenha pegada alguma não é detalhe: é a
verificação de que a ponte é **definicional**, e não uma prova
disfarçada.

## A força exata do que foi provado

```text
Um invariante que SEPARA dois estados prova que um nao alcanca o outro.
Nenhuma finitude e usada. C pode ser infinito, e na instancia ele e.

Para abstracoes invariantes, OrbitSeparating vale EXATAMENTE nos
pontos fixos.
```

## O que **não** foi provado

```text
que invariante separador seja NECESSARIO para inalcancabilidade
que exista invariante separador quando ha inalcancabilidade
que a ferramenta decida qualquer coisa
que invariantes formem reticulado, algebra ou categoria
qualquer coisa sobre sistemas nao deterministicos
qualquer coisa sobre monovariantes ou terminacao
```

`constant_invariant_proves_nothing` compila **sem pegada alguma** e está
na frente para tornar a assimetria verificável em Lean.

## O quadro que a frente completa

```text
abstracao para COLAPSAR    dez frentes, recorrencia sob OrbitSeparating
abstracao para SEPARAR     esta frente, impossibilidade sob invariante

e os dois usos sao INCOMPATIVEIS fora dos pontos fixos
```

O laboratório passou dez frentes num lado da fronteira. Agora tem os dois
lados, e a medida exata da distância entre eles.

## Claim

Uma única claim, `INVARIANT-UNREACHABILITY-FORMAL-001`,
`evidence_level: F`, novidade `NONE`. Argumentos de invariante são
material clássico; o que a frente faz é dar-lhes lugar no frame formal
que já existia.

```text
ledger antes   24
ledger depois  25
```

## Decisão

```text
FOUND_INVARIANT_UNREACHABILITY_001_RESULT_REVIEW_APPROVED
```

## Ressalva de independência

Os cinco gates da frente foram executados pelo mesmo agente em sessão
única. Nenhum substitui revisão externa. O que sustenta o resultado é o
que foi medido e reexecutado — e, no gate de especificação, também o que
a derivação por script **recusou**.
