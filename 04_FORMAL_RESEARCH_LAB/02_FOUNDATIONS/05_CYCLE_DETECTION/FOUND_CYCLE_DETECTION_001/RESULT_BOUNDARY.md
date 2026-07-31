---
document_id: FCD-RESULT-BOUNDARY
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# Fronteira do resultado

```text
Foi formalizado:

- um certificado executável com baseIndex e period;
- o predicado de validade do certificado;
- uma enumeração finita completa de todos os candidatos
  dentro das cotas;
- um detector executável que retorna Option CycleWitness;
- soundness do resultado retornado;
- completeness para toda trajetória em tipo finito;
- conversão do certificado em ponto periódico;
- propagação da colisão para toda a cauda posterior;
- testes executáveis em modelos finitos.

Não foi formalizado:

- função total sem Option;
- minimalidade de baseIndex;
- minimalidade de period;
- Floyd;
- Brent;
- tabela visitada;
- complexidade formal;
- extração de binário;
- integração externa;
- periodicOrbit computável;
- enumeração de componentes;
- SimpleGraph;
- novidade matemática ou algorítmica.
```

## Interpretação exata

O que o laboratório passou a ter é **um programa cuja correção e cuja
completude são teoremas**. Dado qualquer sistema determinístico finito com
igualdade decidível e qualquer estado inicial, o detector devolve um par
`⟨baseIndex, period⟩`, e está provado que esse par satisfaz o contrato e
que ele sempre existe.

O que o laboratório **não** passou a ter é um detector ótimo, um detector
mínimo, ou um produto extraído.

## As duas omissões deliberadas

### Adaptador de componente

`detected_cycle_is_component_cycle` **não** foi formalizado. É um
adaptador mecânico para `FOUND-FUNCTIONAL-GRAPH-001`, não é necessário à
soundness, à completeness nem à execução, e sua omissão mantém o núcleo
algorítmico mínimo — inclusive dispensando o import de `FunctionalGraphs`.

```yaml
CD-GAP-012: OPEN_DEFERRED
```

### Função total

`detectCycleWitness` **não** foi formalizado. A API garantida da v1 é
`Option CycleWitness`. Nenhum valor padrão falso foi introduzido.

```yaml
CD-GAP-017: OPEN_DEFERRED
```

## Semântica que não pode ser esquecida

```text
baseIndex eh o indice-base de uma colisao certificada.
NAO eh o menor indice de entrada no ciclo.

period eh um periodo positivo testemunhado.
PODE ser multiplo do periodo minimo.
NAO eh Function.minimalPeriod.
```

Os testes de regressão frequentemente devolvem os valores mínimos — isso é
consequência da ordem da enumeração, e **não** foi provado.

## Novidade

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

A busca limitada por certificado é a implementação ingênua contra a qual
Floyd e Brent foram propostos como melhorias. Não há nada a reivindicar —
nem detector novo, nem algoritmo novo, nem teoria nova, nem descoberta
matemática, nem resultado físico. O valor é a execução verificada dentro
do Lean e a reutilização de fundações anteriores sem repeti-las.
