---
document_id: FFG-REUSE-MATRIX
status: ASSESSMENT_ONLY
integrations_created: 0
---

# FOUND-FUNCTIONAL-GRAPH-001 — Matriz de reutilização

Avaliação apenas. **Nenhuma integração criada.**

## A distinção que organiza tudo

```text
USO PROPOSICIONAL     provar propriedades sobre um sistema modelado
USO COMPUTACIONAL     obter um algoritmo executavel
```

Esta frente serve o primeiro. Para o segundo há um obstáculo estrutural:

```text
Function.periodicOrbit eh NONCOMPUTAVEL.

O resultado formal NAO fornece diretamente um algoritmo executavel de
enumeracao de componentes, de deteccao de ciclo ou de calculo de mu.
```

```yaml
- domain: maquinas de estado
  classification: REQUIRES_ADAPTER
  propositional_use: "alcance e invariancia entre estados de controle"
  computational_use: "NAO — periodicOrbit noncomputavel"
  adapter: "modelar o espaco de controle como Fintype; transicao por letra fixa"

- domain: pipelines
  classification: REQUIRES_ADAPTER
  propositional_use: "provar que um estagio eh alcancavel ou inalcancavel"
  computational_use: NAO
  adapter: "recortar o esqueleto de controle finito"

- domain: parsers
  classification: REQUIRES_ADAPTER
  propositional_use: "estados de controle do automato subjacente"
  computational_use: NAO
  adapter: "excluir pilha e lookahead, que quebram Fintype"

- domain: deteccao de loops
  classification: REQUIRES_ADAPTER
  propositional_use: "CORRECAO de um detector: mu < card X garante terminacao"
  computational_use: "NAO — o algoritmo (Floyd, Brent) teria de ser escrito a parte"
  note: >
    Esta frente prova que o ciclo EXISTE e onde ele comeca a existir;
    nao prova nada sobre como encontra-lo.

- domain: automatos deterministicos
  classification: REQUIRES_ADAPTER
  propositional_use: "iteracao de delta por uma letra fixa"
  computational_use: NAO
  note: "Mathlib ja tem DFA; uma ponte seria trabalho proprio"

- domain: workflows
  classification: REQUIRES_ADAPTER
  propositional_use: "alcancabilidade entre etapas"
  computational_use: NAO

- domain: jogos finitos
  classification: CONCEPTUAL_ONLY
  reason: "envolve escolha entre jogadores; a dinamica nao eh iteracao de UMA funcao"

- domain: agentes discretos
  classification: CONCEPTUAL_ONLY
  reason: "nao determinismo ou probabilidade, ambos fora do escopo"

- domain: testes de alcancabilidade
  classification: DIRECT_REUSE
  propositional_use: "IterReachable, EventuallyMeets e suas propriedades"
  computational_use: "parcial — as relacoes sao Prop, nao decidiveis por construcao"
  note: >
    Unico DIRECT_REUSE, e justamente o mais abstrato: essa parte da API
    NAO exige finitude.

- domain: auditoria de transicoes
  classification: REQUIRES_ADAPTER
  propositional_use: "provar que um estado nunca eh atingido"
  computational_use: NAO
```

## Resumo

| Classificação | Domínios |
|---|---|
| `DIRECT_REUSE` | 1 — testes de alcançabilidade |
| `REQUIRES_ADAPTER` | 7 |
| `CONCEPTUAL_ONLY` | 2 |
| `OUT_OF_SCOPE` | 0 |

## Limite computacional — vinculante

```text
periodicOrbit eh noncomputavel.

A claim NAO apresenta periodicOrbit como algoritmo executavel.

Nenhum resultado desta frente fornece enumeracao de componentes,
calculo de mu, ou deteccao de ciclo executavel.
```

## Aviso

```text
A reutilizacao em software NAO transforma o resultado matematico padrao
em descoberta cientifica.
```
