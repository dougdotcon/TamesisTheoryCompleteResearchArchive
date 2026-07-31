# Grafo global de dependências

```text
LAB-ARCH-001
    └── LAB-BENCH-001
            ├── FOUND-SEMIGROUP-001
            │       └── TOE-INTERFACE-001
            ├── RH-NOGO-001
            ├── NS-PRESSURE-001
            ├── PVSNP-PHYS-001
            ├── YM-LIMIT-001
            ├── HODGE-CDK-001
            └── BSD-HYP-MATRIX-001
```

As setas são dependências de infraestrutura/formalização, não implicações
matemáticas entre os Problemas do Milênio.

## Fundações finitas — cadeia verificada

```text
LAB-BENCH-001            VERIFIED
        |
FOUND-SEMIGROUP-001      VERIFIED    modelo C3 (monoide finito agindo)
        |
FOUND-SEMIGROUP-002      VERIFIED    alcancabilidade, invariantes,
        |                            periodicidade eventual
        v
FOUND-FUNCTIONAL-GRAPH-001   SCOPED      estrutura GLOBAL do grafo de f
```

`FOUND-FUNCTIONAL-GRAPH-001` depende de `FOUND-SEMIGROUP-002` por
**reutilização de API verificada**, não por extensão de escopo: o
`extension_status` de `FOUND-SEMIGROUP-002` permanece `NOT_AUTHORIZED`.

## Frente congelada

```text
RH-NOGO-001   FROZEN_PARTIAL_RESULT   camada abstrata completa,
                                      camada concreta deferida
        |
        x   TOE-INTERFACE-001 depende dela — dependencia BLOQUEANTE
```

