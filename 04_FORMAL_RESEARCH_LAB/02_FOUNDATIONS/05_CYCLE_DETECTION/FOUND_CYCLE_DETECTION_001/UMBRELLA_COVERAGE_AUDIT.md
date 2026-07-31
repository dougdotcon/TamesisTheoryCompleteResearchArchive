---
document_id: FCD-UMBRELLA-COVERAGE-AUDIT
motivated_by: defeito real do gate de formalizacao
---

# Auditoria de cobertura dos agregadores

Este documento existe por causa de um defeito real: na primeira passagem
da formalização os agregadores **não** foram atualizados, e o alvo padrão
do `lake build` passava **sem cobrir a frente**.

## Cadeia de cobertura, verificada no commit revisado

```text
TamesisLab.lean
    -> TamesisLab.Foundations                        (linha 1)
         -> TamesisLab.Foundations.CycleDetection     (Foundations.lean, linha 5)
              -> Witness, Candidates, Detector,
                 Correctness, Periodicity
         -> TamesisLab.Foundations.CycleDetection.Audit  (linha 6)
    -> TamesisLab.Tests.FoundCycleDetection001        (linhas 24-26)
    -> TamesisLab.Tests.FoundCycleDetection001Execution
    -> TamesisLab.Tests.FoundCycleDetection001Axioms
```

Confirmado por `git show HEAD:` sobre os dois agregadores — isto é, no
conteúdo **committado**, não apenas na árvore de trabalho.

## Evidência quantitativa

```text
antes de registrar a frente   8727 jobs
depois                        8737 jobs
diferenca                       10 = 6 modulos + 1 agregador + 3 testes
```

O contador é a evidência direta de que o alvo padrão passou a alcançar a
frente.

## Teste de cobertura

Criado `TamesisLab/Tests/FoundCycleDetection001UmbrellaAudit.lean`, que
importa **apenas** `TamesisLab` e referencia as treze declarações por nome
totalmente qualificado, mais um `#eval` e dois teoremas de regressão por
`decide`. **Exit 0**, 6 s.

O teste falha se a frente deixar de ser alcançada pelo agregador raiz —
que é exatamente o defeito que passou despercebido.

## O import circular

Registrar os dois testes de auditoria **dentro** de `TamesisLab.lean`
produz um ciclo: a raiz importaria testes que importam a raiz. O
`lake build` falhou com

```text
- TamesisLab.Tests.FoundCycleDetection001InstanceAudit
- TamesisLab.Tests.FoundCycleDetection001UmbrellaAudit
error: build failed
```

O registro foi removido. Os dois testes ficam **fora** do agregador raiz
por construção — é a única forma de eles poderem importá-la — e são
executados por `lake env lean`. `TamesisLab.lean` permanece idêntico ao
commit revisado.

Consequência a registrar honestamente:

```text
os tres testes ORIGINAIS entram no lake build;
os dois testes de AUDITORIA nao entram, e precisam ser executados
explicitamente.
```

Isso é uma limitação estrutural do padrão "teste que importa a raiz", não
um descuido.

## Estado final

```text
Foundations.lean importa CycleDetection            SIM
Foundations.lean importa CycleDetection.Audit      SIM
TamesisLab.lean alcanca a frente pelo agregador    SIM
umbrella audit                                     PASS
lake build                                         PASS, 8737 jobs
```
