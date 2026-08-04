---
document_id: NS-PRESSURE-FIRST-STEP-MEASURED-2026-08-04
measured_at: 2026-08-04
corrects: ATTACK-READINESS-2026-08-04
probe_exit: 0
first_step_kind: FORMAL_NOT_BIBLIOGRAPHIC
verdict_changed: true
---

# NS-PRESSURE-001 — o primeiro passo NAO e bibliografico

## A correcao

`ATTACK_READINESS.md` afirma, para os cinco problemas de baixo da tabela,
que *"o primeiro passo seria bibliografico, nao formal"*. Para
`NS-PRESSURE-001` isso esta **errado**, e a medicao mostra onde.

```text
antes    primeiro passo bibliografico, custo very_high
agora    primeiro passo FORMAL, gargalo identificado, custo high
```

A literatura de Navier-Stokes nao falta. O que falta e **uma peca de
infraestrutura em Lean**, e ela e nomeavel.

## O que o Mathlib TEM (medido, exit 0)

```text
Sobolev H^s     TemperedDistribution.MemSobolev, besselPotential
                MemSobolev.laplacian  (H^s -> H^(s-2))
                MemSobolev.lineDerivOp (H^s -> H^(s-1))
GNS             MeasureTheory.eLpNorm_le_eLpNorm_fderiv
Laplaciano      Laplacian.laplacian, InnerProductSpace.laplacianWithin
multiplicador   TemperedDistribution.fourierMultiplierCLM
divergencia     apenas como TEOREMA de integracao, nao como operador
```

## O que NAO existe

```text
NavierStokes, WeakSolution, LeraySolution, Leray.projection
HeatEquation, divergence (operador), curl, vorticity, pressure
```

E, com **zero ocorrencias em toda a arvore**:

```text
Helmholtz, Leray, Riesz transform, Calderon, Zygmund,
singular integral, Mikhlin, Hormander, maximal function, fluid, Navier
```

## O enunciado e barato, e nao e vacuo

O agente construiu do zero, so com primitivas, `divg` (via `fderiv` e
`EuclideanSpace.single`), `grad` (via `InnerProductSpace.toDual`) e
`IsNSSolution nu u p` para Navier-Stokes incompressivel em R3. Elaboram.

E provou os dois lados, cumprindo `positive_instance_required`:

```text
ns_uniform_flow   escoamento uniforme u = c, p = 0    E solucao
ns_not_radial     campo radial u x = x                NAO e solucao
```

Satisfazivel e refutavel. **O predicado nao e vacuo.**

## Onde o problema morre, medido

A pressao em NS recupera-se de `Laplace p = -div((u . grad) u)`, o que
exige o **projetor de Leray** `P = I - grad (Laplace)^-1 div`, de simbolo
`delta_jk - xi_j xi_k / |xi|^2`.

O unico teorema de limitacao de multiplicador disponivel e
`MemSobolev.fourierMultiplierCLM_of_bounded`, e ele exige
`Function.HasTemperateGrowth g`. Essa definicao comeca com
`ContDiff R infinity f` **global**.

```text
simbolo de Leray   limitado, mas DESCONTINUO na origem
hipotese exigida   suavidade global
resultado          a hipotese falha, e nao ha rota alternativa
```

Sem Calderon-Zygmund, sem transformadas de Riesz, sem
Mikhlin-Hormander, sem funcao maximal — nenhum dos quatro existe.

## O gargalo, que e um lema autocontido

```text
trocar HasTemperateGrowth por mensurabilidade + limitacao essencial
no lema de multiplicador, para o caso L^2
```

Em `L^2` isso e **Plancherel puro** e nao precisa de suavidade. E esse
lema, e nao a bibliografia, o primeiro passo real.

## Custo revisto

```text
high        se o alvo for o projetor de Leray em H^s (base L^2)
very_high   se precisar de estimativa L^p com p != 2
            — ai Calderon-Zygmund inteiro teria de vir antes
```

## O que esta medicao NAO afirma

```text
que NS-PRESSURE-001 esteja proximo
que o laboratorio deva abri-lo
que regularidade de Navier-Stokes tenha ficado alcancavel
```

Ela afirma **uma coisa so**: a classificacao "primeiro passo
bibliografico" estava errada para este item, e o gargalo verdadeiro tem
nome e endereco.
