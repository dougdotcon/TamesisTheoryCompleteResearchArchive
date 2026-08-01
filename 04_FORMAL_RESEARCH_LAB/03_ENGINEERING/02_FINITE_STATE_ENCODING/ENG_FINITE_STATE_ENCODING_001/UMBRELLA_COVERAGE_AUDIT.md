---
document_id: ENC-UMBRELLA-COVERAGE-AUDIT
---

# Auditoria de cobertura pelos agregadores

## Cadeia verificada

```text
TamesisLab.lean
    -> TamesisLab.Engineering                       (linha 2)
         -> TamesisLab.Engineering.FiniteStateRuntime
         -> TamesisLab.Engineering.FiniteStateRuntime.Audit
         -> TamesisLab.Engineering.FiniteStateEncoding      (linha 3)
              -> Encoding, TableConstruction,
                 Commutation, DynamicAnalysis
         -> TamesisLab.Engineering.FiniteStateEncoding.Audit (linha 4)
    -> TamesisLab.Tests.EngFiniteStateEncoding001
    -> ...Execution
    -> ...Axioms
```

`FiniteStateEncoding.lean` importa os **quatro** módulos funcionais.
`Engineering.lean` importa a frente e seu `Audit`. `TamesisLab.lean`
importa `TamesisLab.Engineering` e registra os **três** testes originais.

## Novo teste de cobertura

`TamesisLab/Tests/EngFiniteStateEncoding001UmbrellaAudit.lean` importa
**apenas** `TamesisLab` e alcança as **quinze** declarações públicas por
nome totalmente qualificado, mais três declarações das frentes
anteriores, mais um exemplo executável e a conclusão semântica no tipo
original.

```text
exit 0, 80 s
```

O tempo reflete a importação da raiz inteira.

## Por que ele não é registrado na raiz

```text
ele importa TamesisLab; registra-lo em TamesisLab.lean criaria ciclo.
```

Mesma limitação estrutural de `CD-GAP-018` e `RT-GAP-018`. Consequência
honesta, e verificada:

```text
grep 'EngFiniteStateEncoding001UmbrellaAudit' TamesisLab.lean  ->  0
os tres testes originais entram no lake build
o umbrella audit NAO entra, e eh executado explicitamente
```

## Build

```text
lake build   PASS, 8757 jobs
delta contra a formalizacao   0
```

O umbrella audit não altera a contagem porque não está no alvo padrão —
que é exatamente o comportamento esperado.
