---
session_id: 2026-08-01-PORTFOLIO-REVIEW-FINITE-STATE-RUNTIME
date: 2026-08-01
gate: PORTFOLIO_REVIEW
authorized_action: PORTFOLIO_REVIEW_AUTHORIZED
agent: claude-opus-5
commit_before: a4907b7cb2b421ccb52fc0262bf276ef2d94f8a9
decision: A_PORTFOLIO_REVIEW_APPROVED_FINITE_STATE_RUNTIME_SELECTED
selected_work_item: ENG-FINITE-STATE-RUNTIME-001
lean_files_created: 0
---

# Sessão — Revisão de portfólio · ponte para sistemas finitos reais

Seleção da próxima frente após o encerramento de
`FOUND-CYCLE-DETECTION-001`. **Nenhum arquivo Lean, nenhuma prova, nenhum
adaptador, nenhum executável, nenhum `lake build`.**

## Preflight

```text
HEAD                  a4907b7cb2b421ccb52fc0262bf276ef2d94f8a9
árvore                limpa
processos Lean/Lake   nenhum
cat-file -e           0
merge-base ancestor   0   (igualdade aceita)
canonical_commit      d9d672c -> a4907b7
```

Todos os códigos de saída foram verificados explicitamente — nenhuma
conclusão foi tirada de saída truncada.

## O estado, com precisão

```text
EXECUTAVEL dentro do Lean       CycleWitness, cycleCandidates,
                                detectCycleWitness?
PROPOSICIONAL                   Valid e os quatro teoremas, periodicPts,
                                EventuallyMeets, periodicOrbit
DEPENDE DE COMPILACAO           o detector inteiro; os cinco modelos de
                                teste sao definidos NO FONTE
FALTA PARA DADOS EXTERNOS       tudo
```

O laboratório tem um programa verificado que **não consegue receber uma
entrada**. É essa a lacuna.

## As seis alternativas

| | Classificação |
|---|---|
| A totalização | `DEFERRED_LOW_INCREMENTAL_VALUE` |
| B Floyd | `DEFERRED_PREMATURE_OPTIMIZATION` |
| C Brent | `DEFERRED_PREMATURE_OPTIMIZATION` |
| D extração isolada | `INSUFFICIENT_RUNTIME_VALUE` |
| E infraestrutura de testes | `P2_LAB_INFRASTRUCTURE` |
| **F adaptador de runtime** | **`SELECTED`** |

O argumento decisivo: **F é a única das seis que muda o que o laboratório
consegue fazer**, e não apenas quão rápido ou quão elegante ele faz.

Sobre a totalização, uma observação que não estava no gate: em uma camada
dinâmica, `Option` é o **menor** dos problemas — o erro real a reportar é
"esta tabela é inválida", e a totalização não endereça isso.

Sobre a infraestrutura de testes: registrada em `RT-GAP-018`, **não**
selecionada, porque nenhum bloqueio real foi encontrado no `lake build`,
que passa com 8737 jobs.

## Alvo selecionado

```yaml
work_item: ENG-FINITE-STATE-RUNTIME-001
title: "Certified Runtime Adapter for Finite Deterministic Systems"
track: ENGINEERING_FOUNDATION
work_status: SCOPED
research_role: FORMAL_SOFTWARE_BRIDGE
```

**Duplicata: não encontrada.** Zero itens com prefixo `ENG-` na fila; zero
ocorrências de `RawTransitionTable`, `TransitionTable` ou `RUNTIME-001`;
zero usos de `Array` no núcleo `Foundations`. As menções a "adaptador" no
laboratório são ou o *adaptador de componente* (`CD-GAP-012`) ou a
classificação `REQUIRES_ADAPTER` das matrizes de reutilização — que
**descrevem exatamente a lacuna** que esta frente vai fechar.

Nenhum dos seis critérios de rejeição ocorreu.

## Desenho preliminar

`RawTransitionTable` com um único campo `next : Array Nat` — **sem**
`size`, porque é derivável, a mesma disciplina que rejeitou `entryPoint`
em `CycleWitness`. A tabela bruta **pode** conter destinos inválidos, e é
isso que a torna a representação certa para a entrada.

Validação executável devolvendo `Except` com erros tipados, **três**
validações separadas — tabela, consulta, execução — e nunca um único
`Bool`.

## A proibição mais importante

```text
NAO corrigir destinos invalidos por modulo, clamp ou fallback.
```

Um `% n` silencioso transformaria uma tabela errada em um **sistema
diferente**, e o certificado devolvido seria correto sobre um sistema que
o usuário nunca descreveu. É o modo de falha mais perigoso desta frente, e
por isso entrou também nas proibições vivas do `LAB_STATE.md`.

## O principal resultado formal futuro

`iterate_step_corresponds`: iterar a função tipada sobre `Fin` corresponde
a seguir repetidamente os índices da tabela. Sem ela, o certificado fala
de um objeto Lean que ninguém consegue relacionar com o dado de entrada.

## A ressalva que a frente não pode apagar

```text
converter um sistema real para uma tabela finita eh uma ABSTRACAO;
a correcao dessa abstracao NAO eh fornecida pelo adaptador.
```

O adaptador garante que **a tabela dada** é analisada corretamente. Que a
tabela **represente** o sistema real é de quem a produziu. `RT-GAP-017`.

## Desvios de governança

Três edições mínimas e literais em `labctl.py`, sem wildcard: `DEC-020`
(gate sequence), `DEC-021` (pré-condição dupla — `VERIFIED` **e**
`result_review APPROVED`, a primeira do laboratório a exigir duas
propriedades) e `DEC-022` (entrada de allowlist).
`PORTFOLIO_REVIEW_AUTHORIZED` já existia.

## Validação

```text
pytest                            PASS
labctl validate                   PASS
canonical_commit_check            PASS
arquivos Lean criados             0
provas criadas                    0
adaptador implementado            NAO
executavel criado                 NAO
lake build                        NAO executado
claims promovidas                 0   (ledger em 20)
legado modificado                 0
frentes encerradas tocadas        0 arquivos matematicos
whitespace                        PASS, antes do git add
commit --amend                    NAO usado
```

## Estado final

```text
active_work_item   ENG-FINITE-STATE-RUNTIME-001
work_status        SCOPED
authorized_action  ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED
```

Formalização, extração, CLI, JSON e integração permanecem **não
autorizadas**. Floyd, Brent e a totalização de
`FOUND-CYCLE-DETECTION-001` também.

## Próxima ação única

Preparar a especificação de um adaptador executável que valide uma tabela
dinâmica de transições, construa uma função total sobre `Fin n` e aplique
o detector certificado de ciclos.
