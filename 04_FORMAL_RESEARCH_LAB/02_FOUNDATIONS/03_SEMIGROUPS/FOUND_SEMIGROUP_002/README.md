# FOUND-SEMIGROUP-002 — Dinâmica discreta de ações finitas de monoides

Especificação. **Nenhuma prova foi executada neste gate.**

## O que esta frente estuda

Três coisas que são frequentemente confundidas e que aqui ficam separadas
por construção:

```text
CAMADA A   acao completa do monoide M sobre X
           alcancabilidade: existe ALGUM m com m . x = y

CAMADA B   dinamica de UM elemento a fixo
           a . x, a^2 . x, a^3 . x, ...

CAMADA C   sistema funcional finito (X, f)
           f(x), f(f(x)), ...   sem monoide algum
```

A periodicidade eventual pertence à **Camada C**: ela depende apenas da
finitude de `X` e da iteração de `f`. Não requer monoide. Formalizá-la na
Camada A seria um erro de nível.

## Alvo principal

Para todo `f : X → X` com `X` finito e todo `x : X`, a sequência `f^[n] x`
é eventualmente periódica, com limitantes em `Fintype.card X`, e a
propriedade se propaga para todos os índices posteriores.

Meta escolhida para a primeira execução: **`C. CORE_BOUNDS_AND_PROPAGATION`**.
A decomposição única em cauda + ciclo fica **fora** desta execução
(`FSG2-GAP-004b`, análise de custo em `THEOREM_CANDIDATES.md`).

## Relação com FOUND-SEMIGROUP-001

`FOUND-SEMIGROUP-002` depende **conceitualmente** da frente anterior:
convenção de composição (`comp a b` aplica `b` primeiro, alinhada a
`mul_smul`), reuso da interface oficial `Monoid`/`MulAction` da Mathlib e o
modelo `C3` como instância de teste.

O modelo `C3` **não** é promovido a teoria universal. Ele é um exemplo com
propriedades atípicas — fiel, transitivo, e todo estado é periódico **sem
cauda** — que por isso mesmo **não serve** como caso de teste para a parte
interessante do alvo. Os contraexemplos de `COUNTEREXAMPLE_PLAN.md` existem
exatamente para cobrir o que `C3` não cobre.

## Artefatos

```text
STATUS.yaml               estado da frente
TARGET_RESULT.md          enunciado-alvo e o que ele nao eh
DEFINITIONS.md            definicoes e separacao das tres camadas
ASSUMPTIONS.md            hipoteses e o que nao eh assumido
THEOREM_CANDIDATES.md     assinaturas candidatas, sem corpos de prova
LEAN_FEASIBILITY.md       auditoria da API Mathlib fixada
COUNTEREXAMPLE_PLAN.md    cinco modelos finitos de refutacao
KNOWN_RESULTS_MATRIX.md   o que ja eh padrao na literatura
DEPENDENCY_DAG.yaml       dependencias por tipo
GAP_REGISTER.yaml         FSG2-GAP-001..008
STOP_CONDITIONS.md        condicoes de parada
NOVELTY_BOUNDARY.md       fronteira de novidade — vinculante
```

## Aviso vinculante

Periodicidade eventual em conjunto finito **não é descoberta matemática**.
É o princípio da casa dos pombos. Ver `NOVELTY_BOUNDARY.md`.
