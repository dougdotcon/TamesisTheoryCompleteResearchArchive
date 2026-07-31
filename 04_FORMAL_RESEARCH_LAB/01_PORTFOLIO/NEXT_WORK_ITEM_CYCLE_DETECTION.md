---
document_id: NEXT-WORK-ITEM-CYCLE-DETECTION
work_item_id: FOUND-CYCLE-DETECTION-001
status: SCOPED
decided_at: 2026-07-31
authorized_action: FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED
mathematical_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
---

# FOUND-CYCLE-DETECTION-001 — decisão e escopo preliminar

> **Escopo apenas.** Nenhum teorema é especificado definitivamente aqui.
> Nenhum algoritmo é implementado. Nenhum arquivo Lean foi criado.
> Nenhuma estrutura é congelada.

## Identificação

```yaml
work_item_id: FOUND-CYCLE-DETECTION-001
title: "Executable Cycle Detection for Finite Deterministic Systems"
track: FOUNDATIONS
work_status: SCOPED
mathematical_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

## A lacuna atacada

`FOUND-FUNCTIONAL-GRAPH-001` provou **proposicionalmente**:

```text
toda trajetoria em tipo finito alcanca uma orbita periodica;
existe mu < card X;
o componente possui uma unica periodicOrbit.
```

E **não** forneceu:

```text
algoritmo executavel;
valor computado de mu;
valor computado de lambda;
ponto de entrada calculado;
lista concreta dos estados do ciclo;
certificado computavel do componente.
```

A distância entre as duas listas é exatamente o escopo desta frente. O
resultado anterior diz *que o ciclo existe*; esta frente deve entregar *um
programa verificado que o encontra e devolve um certificado correto*.

Classificação esperada:

```yaml
expected_mathematical_novelty: NONE
expected_formal_value: HIGH
expected_software_reuse: VERY_HIGH
expected_cost: MODERATE
counterexample_access: HIGH
algorithmic_value: HIGH
```

## Dados centrais

```text
X  : tipo finito
f  : X -> X
x0 : X
```

Hipóteses **esperadas**, não presumidas:

```text
Fintype X       quase certamente necessaria — limita a busca
DecidableEq X   provavelmente necessaria — o algoritmo compara estados
```

Registro explícito: `FOUND-FUNCTIONAL-GRAPH-001` demonstrou que
`DecidableEq X` **não** é necessária para a camada proposicional, e
`LAB_STATE.md` proíbe acrescentá-la sem necessidade verificada. Aqui a
situação muda de natureza — comparar estados **durante a execução** é
diferente de afirmar igualdade em uma proposição — mas isso continua sendo
uma hipótese a **confirmar** na especificação, registrada como
`CD-GAP-004`. A especificação deve confirmar a necessidade real, não
presumi-la.

## Estrutura de resultado candidata

```lean
structure CycleDetectionResult (X : Type*) where
  entryIndex : ℕ
  period : ℕ
  entryPoint : X
```

Invariantes candidatos:

```text
entryIndex < card X
0 < period
entryIndex + period <= card X
entryPoint = f^[entryIndex] x0
f^[entryIndex + period] x0 = entryPoint
para todo k, f^[entryIndex + k + period] x0 = f^[entryIndex + k] x0
```

A especificação deverá decidir se a estrutura armazena somente `μ` e `λ`,
ou também o ponto, ou uma `List`/`Finset` do ciclo, ou certificados de
correção embutidos. **A estrutura definitiva não é congelada neste gate**
(`CD-GAP-002`).

## Algoritmos comparados

### Floyd — tortoise and hare

```text
Fase 1  encontrar uma colisao
Fase 2  encontrar o ponto de entrada
Fase 3  calcular o periodo
```

| Vantagens candidatas | Riscos |
|---|---|
| memória constante | prova de terminação |
| algoritmo clássico, atribuição estável | índices e aritmética |
| bom valor para formalização de invariantes | relação entre colisão e entrada |
| as três fases mapeiam bem em três lemas | recursão estrutural ou `fuel` |

### Brent

| Vantagens candidatas | Riscos |
|---|---|
| menos avaliações de `f` em vários casos | invariantes mais complexos |
| estrutura iterativa diferente | dobramento de blocos |
| também usa memória constante | maior atrito inicial em Lean |

### Enumeração com tabela visitada

| Vantagens | Riscos |
|---|---|
| prova simples | memória `O(card X)` |
| extração direta do primeiro índice repetido | armazenamento de índices |
| adequada a tipos finitos | dependência maior de `Finset`/`List`/`Array` |

### Recomendação inicial

```text
PRIMARY:            FLOYD_WITH_FUEL
REFERENCE_BASELINE: VISITED_TABLE
DEFERRED:           BRENT
```

O baseline por tabela visitada tem papel duplo: é a implementação cuja
correção é mais fácil de provar e serve de **oráculo** contra o qual
comparar Floyd nos casos de teste. **Nenhum dos três é implementado neste
gate.**

## Terminação — o risco principal

```text
Lean precisa reconhecer que o algoritmo termina.
```

Alternativas a avaliar na especificação:

```text
fuel = card X ou multiplo controlado
recursao bem fundada
StateM com contador
execucao sobre Fin (card X + 1)
busca em Finset/List de estados visitados
```

A especificação deve manter **quatro camadas separadas**:

| Camada | Pergunta |
|---|---|
| terminação do programa | o Lean aceita a definição? |
| correção matemática | o valor devolvido satisfaz os invariantes? |
| limites de complexidade | quantas avaliações de `f`? |
| equivalência com a API proposicional | o certificado implica os teoremas já provados? |

Misturar as quatro é o modo típico de falha desta classe de trabalho.

## Ponte obrigatória com os resultados anteriores

```text
resultado computacional
        |
certificado de colisao
        |
exists_bounded_iterate_collision
        |
periodic_tail_of_collision
        |
exists_component_cycle_with_entry_bound
```

A frente **não** deve reprovar:

```text
casa dos pombos;
periodicidade eventual;
unicidade da periodicOrbit.
```

Deve mostrar que o algoritmo produzido **satisfaz** essas propriedades já
verificadas. A casa dos pombos foi consumida uma única vez, em
`FOUND-SEMIGROUP-002`, e continua consumida.

## Resultado funcional candidato

```lean
def detectCycle
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    CycleDetectionResult X
```

Teorema de correção candidato:

```lean
theorem detectCycle_correct
    {X : Type*}
    [Fintype X]
    [DecidableEq X]
    (f : X → X)
    (x : X) :
    let r := detectCycle f x
    r.entryPoint = f^[r.entryIndex] x ∧
    r.entryIndex < Fintype.card X ∧
    0 < r.period ∧
    f^[r.entryIndex + r.period] x = r.entryPoint
```

Teorema de propagação candidato:

```lean
theorem detectCycle_propagates :
  ∀ k,
    f^[r.entryIndex + k + r.period] x =
      f^[r.entryIndex + k] x
```

### Minimalidade — NÃO autorizada

```text
minimalidade de mu               NAO AUTORIZADA
minimalidade de lambda           NAO AUTORIZADA
complexidade assintotica formal  NAO AUTORIZADA
lista completa da bacia          NAO AUTORIZADA
enumeracao de componentes globais NAO AUTORIZADA
```

Floyd, quando corretamente implementado, tende a produzir o `μ` mínimo e o
`λ` mínimo — mas *tender* não é *provar*. A especificação deverá decidir se
vale provar isso já no primeiro ciclo ou se o contrato se limita a
existência com cota. Registrado em `CD-GAP-009` e `CD-GAP-010`.

## Relação com `periodicOrbit`

```text
A saida executavel NAO deve depender de decidir igualdade de
Function.periodicOrbit, pois periodicOrbit eh nao computavel.
```

A ponte é **proposicional**:

```text
o entryPoint calculado pertence a periodicPts;
sua periodicOrbit eh a orbita unica do componente;
o algoritmo opera sobre igualdade decidivel de ESTADOS,
nao sobre igualdade decidivel de Cycle.
```

Esta é a distinção que separa esta frente de um erro de categoria:
`DecidableEq X` é sobre `X`; `periodicOrbit` vive em `Cycle X`, e nenhuma
decidibilidade sobre `Cycle X` é assumida, requerida ou construída.

## Aplicações mapeadas

```text
deteccao de loops em parsers
retries de pipelines
maquinas de estado
workflows
agentes deterministicos
jogos finitos
simuladores discretos
auditoria de estados
deteccao de dead loops
sistemas embarcados finitos
```

**Nenhuma integração é implementada neste gate.** E, como já registrado
duas vezes neste laboratório: reutilização em software não transforma
resultado padrão em descoberta científica.

## Casos de teste preliminares

Valores esperados são **candidatos**; nenhum contrato de minimalidade foi
escolhido ainda.

### CD-CE-001 — ponto fixo imediato

```yaml
expected_entry_index: 0
expected_period: 1
expected_entry_point: a
expected_trace: "a -> a"
property_tested: caso degenerado; entryIndex zero
```

### CD-CE-002 — cauda e ponto fixo

```yaml
expected_entry_index: 2
expected_period: 1
expected_entry_point: c
expected_trace: "a -> b -> c -> c"
property_tested: cauda nao trivial com ciclo trivial
```

### CD-CE-003 — ciclo desde o início

```yaml
expected_entry_index: 0
expected_period: 3
expected_entry_point: a
expected_trace: "a -> b -> c -> a"
property_tested: ciclo nao trivial sem cauda
```

### CD-CE-004 — cauda mais ciclo não trivial

```yaml
expected_entry_index: 2
expected_period: 2
expected_entry_point: c
expected_trace: "a -> b -> c -> d -> c"
property_tested: caso geral; as duas fases nao triviais
```

### CD-CE-005 — dois estados externos entrando no mesmo ciclo

```yaml
expected_entry_index: depende do estado inicial
expected_period: igual para os dois
expected_entry_point: mesmo ponto ou ponto da mesma orbita
expected_trace: "executar separadamente a partir de cada estado inicial"
property_tested: >
  o periodo eh propriedade do componente; o entryIndex NAO eh.
  Liga-se diretamente a exists_component_cycle_with_entry_bound
```

### CD-CE-006 — função em `Bool`

```yaml
expected_entry_index: 0
expected_period: 1 ou 2 conforme a funcao escolhida
expected_entry_point: conforme a funcao escolhida
expected_trace: "caso minimo"
property_tested: API generica em tipo da biblioteca, nao inventado aqui
```

## Gaps iniciais

Nenhum é fechado neste gate.

```yaml
CD-GAP-001:
  title: escolha entre Floyd, tabela visitada e Brent
  status: OPEN

CD-GAP-002:
  title: representação executável do resultado
  status: OPEN

CD-GAP-003:
  title: prova de terminação
  status: OPEN

CD-GAP-004:
  title: necessidade de DecidableEq X
  status: OPEN

CD-GAP-005:
  title: limite de fuel
  status: OPEN

CD-GAP-006:
  title: correção da colisão encontrada
  status: OPEN

CD-GAP-007:
  title: cálculo do ponto de entrada
  status: OPEN

CD-GAP-008:
  title: cálculo do período
  status: OPEN

CD-GAP-009:
  title: minimalidade de μ
  status: OPEN

CD-GAP-010:
  title: minimalidade de λ
  status: OPEN

CD-GAP-011:
  title: ponte com periodicPts
  status: OPEN

CD-GAP-012:
  title: ponte com periodicOrbit não computável
  status: OPEN

CD-GAP-013:
  title: complexidade formal
  status: OPEN

CD-GAP-014:
  title: extração de código executável
  status: OPEN

CD-GAP-015:
  title: fronteira de novidade e uso em software
  status: OPEN

CD-GAP-016:
  title: bibliografia e atribuição histórica dos algoritmos
  status: OPEN
```

## Stop conditions

Rejeitar ou pedir refinamento se:

```text
a frente tentar decidir igualdade de periodicOrbit;
o algoritmo nao possuir argumento claro de terminacao;
a implementacao exigir teoria infinita;
o contrato misturar existencia com minimalidade sem prova;
a nova frente repetir a casa dos pombos;
a estrutura de resultado for excessivamente grande;
a extracao de codigo depender de Classical.choice;
a primeira versao tentar enumerar todos os componentes;
a frente for apresentada como descoberta matematica;
a aplicacao de software for confundida com novidade cientifica;
forem abertas conexoes com TRI, TDTR, fisica ou Clay.
```

## Limites científicos

```yaml
mathematical_novelty: NONE
research_role: FORMAL_ALGORITHM_FOUNDATION
```

Registro literal:

```text
Algoritmos de deteccao de ciclos em sistemas deterministicos
finitos sao resultados classicos.

O valor deste work item estara na formalizacao executavel,
na correcao verificada, na integracao com as fundacoes anteriores
e na possibilidade de extracao para software.
```

Proibido afirmar:

```text
novo algoritmo; nova teoria de grafos; nova lei de dinamica;
descoberta matematica; resultado fisico;
TRI; TDTR; TOE; RH; problema Clay.
```

## Dependências

```text
FOUND-SEMIGROUP-002
        |
periodicidade eventual e colisao limitada
        |
FOUND-FUNCTIONAL-GRAPH-001
        |
componente e orbita periodica unica
        |
FOUND-CYCLE-DETECTION-001
        |
algoritmo executavel e certificado
```

Classificação:

| Dependência | Classe | Conteúdo |
|---|---|---|
| `FOUND-SEMIGROUP-002` → colisão limitada | `MATHEMATICAL` | `exists_bounded_iterate_collision`, `periodic_tail_of_collision`, `exists_eventual_period` |
| `FOUND-FUNCTIONAL-GRAPH-001` → órbita única | `MATHEMATICAL` | `exists_component_cycle_with_entry_bound` |
| API de iteração e periodicidade | `LEAN_API` | `Function.iterate_add_apply`, `Function.periodicPts`, `Function.minimalPeriod` |
| Floyd, Brent, tabela visitada | `ALGORITHMIC` | escolha e invariantes — `CD-GAP-001` |
| terminação, `fuel`, extração | `COMPUTATIONAL` | `Fintype.card`, recursão bem fundada, `Decidable` |
| allowlist e trava de gate | `GOVERNANCE` | `FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED` |
| atribuição de Floyd e Brent | `BIBLIOGRAPHIC` | `CD-GAP-016` |

Reutilização por **API verificada**, não por extensão: os
`extension_status` de `FOUND-SEMIGROUP-002` e
`FOUND-FUNCTIONAL-GRAPH-001` permanecem `NOT_AUTHORIZED`.

## Próximo passo autorizado

```yaml
authorized_action: FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED
```

Preparar a especificação. **Nenhuma formalização autorizada. Nenhum
arquivo Lean. Nenhuma extração de código. Nenhuma integração com sistemas
reais.**
