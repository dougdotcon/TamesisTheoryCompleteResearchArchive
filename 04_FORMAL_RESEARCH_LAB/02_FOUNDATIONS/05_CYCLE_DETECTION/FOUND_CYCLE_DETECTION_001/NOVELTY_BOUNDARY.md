---
document_id: FCD-NOVELTY-BOUNDARY
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# Fronteira de novidade

## Registro literal

```text
A busca finita por certificados de colisao eh uma implementacao
direta de um resultado classico de periodicidade em sistemas
deterministicos finitos.

A contribuicao deste work item nao eh um novo algoritmo.

O valor esta em:

- execucao dentro do Lean;
- correcao formal;
- completude formal;
- reutilizacao de teoremas anteriores;
- producao de certificados;
- base verificavel para otimizacoes futuras.
```

## Classificação

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

## Proibido afirmar

```text
novo detector;
novo algoritmo de ciclos;
nova teoria de dinamica;
descoberta matematica;
descoberta fisica.
```

## O que é, historicamente

A ideia de procurar exaustivamente um par `(μ, λ)` dentro de cotas
conhecidas é anterior a qualquer algoritmo esperto de detecção de ciclos —
é a implementação ingênua contra a qual Floyd e Brent foram propostos como
melhorias. Não há nada a reivindicar aqui, e a atribuição histórica de
Floyd e Brent permanece uma lacuna bibliográfica aberta
(`CD-GAP-016`).

## A distinção que importa

```text
FOUND-FUNCTIONAL-GRAPH-001  provou que o ciclo existe
FOUND-CYCLE-DETECTION-001   entrega um programa que o encontra
```

A segunda **não é matemática nova**. É a mesma matemática, atravessada por
uma fronteira de execução. O valor é de engenharia formal: um programa
cuja correção e cuja completude são teoremas.

## Reutilização em software

Repetido pela terceira vez neste laboratório, porque continua verdadeiro:

```text
A reutilizacao em software NAO transforma o resultado matematico padrao
em descoberta cientifica.
```
