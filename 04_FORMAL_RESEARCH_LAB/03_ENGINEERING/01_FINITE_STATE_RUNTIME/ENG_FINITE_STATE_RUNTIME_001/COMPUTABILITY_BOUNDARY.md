---
document_id: RT-COMPUTABILITY-BOUNDARY
---

# Fronteira de computabilidade

## Meta

```text
RawTransitionTable        computavel
Valid                     decidivel
validateTransitionTable   computavel
validateStart             computavel
step                      computavel
run?                      computavel
detectCycle?              computavel
analyzeTransitionTable    computavel
```

Todos verificados na versão descartável do probe, por `#eval`.

## Proibido nos corpos executáveis

```text
marca de nao-computabilidade
escolha classica extraindo dado
igualdade decidivel classica
fallback arbitrario
modulo
clamp
o objeto de orbita quociente da Mathlib
grafos simples
```

## Pegada axiomática — medida no probe

```text
validateT   ->  [propext, Quot.sound]
analyzeT    ->  [propext, Classical.choice, Quot.sound]
```

Achado relevante: **a camada de validação, isolada, não depende de
`Classical.choice`.** A pegada só entra quando o detector é aplicado, por
`Fintype.card`/`Finset.univ` — exatamente a origem já localizada e
documentada em `FOUND-CYCLE-DETECTION-001`.

Regra herdada, e reafirmada aqui:

```text
eh permitido que #print axioms liste propext, Classical.choice e
Quot.sound por infraestrutura APAGADA, desde que:

  as definicoes nao sejam marcadas como nao computaveis;
  #eval funcione;
  nenhuma escolha classica produza DADO.
```

Os três confirmados.

## O que permanece proposicional

```text
RawTransitionTable.Valid   Prop, decidivel
o campo closed             Prop, apagado na execucao
os teoremas de correcao    Prop
CycleWitness.Valid         Prop, herdado do detector
```

O campo `closed` de `ValidatedTransitionTable` merece nota: ele é um
**dado de tipo `Prop`**, o que significa que a estrutura carrega a prova
em tempo de elaboração e **nada** em tempo de execução. É o que permite
`step` ser computável apesar de consumir `t.closed i`.

## `#eval` não é extração

```text
#eval eh evidencia operacional DENTRO do Lean.
NAO eh extracao de produto.
```

`extraction_status` permanece `READY_FOR_FEASIBILITY_AUDIT` e
`extraction_authorized` permanece `false`, herdados da frente anterior.
Nenhum binário, alvo executável, CLI, JSON, arquivo, rede ou banco de
dados pertence a esta especificação.
