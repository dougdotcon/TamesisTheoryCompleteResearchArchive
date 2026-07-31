---
document_id: RT-UMBRELLA-COVERAGE-AUDIT
---

# Auditoria de cobertura dos agregadores

## Cadeia verificada

```text
TamesisLab.lean
    -> TamesisLab.Engineering                        (linha 2)
         -> TamesisLab.Engineering.FiniteStateRuntime
              -> RawTable, Validation, Execution,
                 DetectorAdapter, DynamicAnalysis
         -> TamesisLab.Engineering.FiniteStateRuntime.Audit
    -> TamesisLab.Tests.EngFiniteStateRuntime001
    -> ...Execution
    -> ...Axioms
```

`FiniteStateRuntime.lean` importa os **cinco** módulos da frente;
`Engineering.lean` importa o agregador da frente mais o `Audit`;
`TamesisLab.lean` importa `TamesisLab.Engineering` e os três testes
originais.

## Evidência quantitativa

```text
antes da frente   8737 jobs
depois            8748 jobs
diferenca           11 = 6 modulos + agregador da frente
                       + agregador de trilha + 3 testes
```

## Teste de cobertura

Criado `TamesisLab/Tests/EngFiniteStateRuntime001UmbrellaAudit.lean`, que
importa **apenas** `TamesisLab` e referencia as vinte e nove declarações
por nome totalmente qualificado, mais um `#eval` e dois teoremas de
regressão por `decide` — incluindo o caso decisivo
`⟨#[1]⟩` com `start = 100`.

Ele também confirma que as **quatro fundações anteriores** continuam
alcançadas pela mesma raiz.

```text
exit 0, 87 s
```

O tempo reflete a importação da raiz inteira.

## Por que ele não é registrado na raiz

```text
ele importa TamesisLab; registra-lo em TamesisLab.lean criaria ciclo.
```

Mesma limitação estrutural já registrada em
`FOUND-CYCLE-DETECTION-001` — `RT-GAP-018`, que permanece
`OPEN_DEFERRED`. Consequência honesta:

```text
os tres testes originais entram no lake build;
o teste de cobertura NAO entra, e eh executado explicitamente.
```

## Estado final

```text
FiniteStateRuntime.lean importa os cinco modulos   SIM
Engineering.lean importa a frente                  SIM
TamesisLab.lean importa Engineering                SIM
umbrella audit                                     PASS
lake build                                         PASS
```
