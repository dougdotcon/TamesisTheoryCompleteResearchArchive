---
document_id: PR-AFTER-CERTIFIED-ENCODING
gate: PORTFOLIO_REVIEW
reviewed_at_commit: e0db1dceaf8e73239d361ed17453b050716d88bc
decision: A_PORTFOLIO_REVIEW_APPROVED_FINITE_ABSTRACTION_SELECTED
selected_work_item: FOUND-FINITE-ABSTRACTION-001
alternatives_compared: 7
---

# Revisão de portfólio após a codificação certificada

## O que o laboratório tem

```text
S, tipado
    |  codificacao BIJETIVA certificada
Fin n
    |  Array.ofFn
ValidatedTransitionTable
    |  runtime adapter
CycleWitness
    |  soundness
stepS^[b + p] start = stepS^[b] start,  em S
```

Cinco frentes encerradas, `22` claims, `15` work items, `0` chaves YAML
duplicadas.

## A lacuna central

A cadeia resolve o caso **exato**: `S ≃ Fin n`, nada se perde. Falta o
caso em que **se perde**:

```text
Como relacionar um sistema concreto, possivelmente grande ou infinito,
com uma abstracao finita muitos-para-um?
```

## A pergunta certa, e a resposta que o probe já deu

A tentação é perguntar "abstração finita preserva ciclos?". A resposta é
**não**, e agora isso é teorema:

```lean
theorem naive_cycle_reflection_is_false :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Semiconj abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start)
```

Compilado, **sem depender de axioma nenhum**, pelo contraexemplo
`Bool → Unit` com `stepC = not`.

A pergunta certa é a outra: **o que a abstração preserva, e sob qual
hipótese o que ela destrói pode ser recuperado.** As duas metades já
compilaram em probe descartável:

```lean
-- preserva, sempre
abstract (stepC^[b+p] start) = abstract (stepC^[b] start)

-- recupera, SOB hipotese explicita
OrbitSeparating abstract stepC start →
  stepC^[b+p] start = stepC^[b] start
```

## Alternativas comparadas

Sete, na matriz de `NEXT_TARGET_COMPARISON_AFTER_ENCODING.md`:

```text
A  FOUND-FINITE-ABSTRACTION-001        abstracao finita e reflexao
B  ENG-FINITE-STATE-REENCODING-001     invariancia do witness
C  ENG-LEAN-NATIVE-EXTRACTION-001      extracao nativa
D  ENG-FINITE-STATE-CLI-001            CLI e parser
E  ENG-FINITE-STATE-DIAGNOSTICS-001    diagnostico detalhado
F  LAB-GOV-YAML-FRONT-MATTER-001       integridade de front matter
G  nova frente matematica independente
```

## Decisão

```text
A. PORTFOLIO_REVIEW_APPROVED_FINITE_ABSTRACTION_SELECTED
```

As doze condições da regra de decisão foram verificadas, **oito delas por
compilação**. Nenhuma falhou.

## Por que não as outras

- **B** fecha `ENC-GAP-020`, é estreita e de baixo risco — mas depende de
  detalhes internos da enumeração do detector, criando acoplamento com a
  implementação que o laboratório vem evitando há quatro frentes.
- **C** e **D** continuam distribuindo garantia sem contrato semântico
  para o caso geral. `D` ainda depende de `C`, que não tem consumidor.
- **E** é conforto operacional; incremento científico próximo de zero.
- **F** é honesta e barata, e foi **apurada por varredura**, não por
  impressão: `429` arquivos Markdown, `277` com front matter YAML,
  **`0` com chave duplicada**. O bloco de `LAB_STATE.md` — o único
  YAML-em-Markdown de que a governança depende para decidir — também está
  limpo, conferido exatamente na fatia que o `labctl` carrega. Sem risco
  concreto e imediato, a alternativa fica registrada como candidata **sem
  prioridade automática** sobre a lacuna científica.
- **G** não tem produto verificável em trinta dias e deixaria aberta a
  lacuna que o próprio laboratório acabou de isolar.

## A fronteira que o gate congela

```text
Uma semiconjugacao prova que a trajetoria concreta eh OBSERVADA
corretamente no sistema abstrato.

Uma igualdade entre estados abstratos demonstra apenas que os estados
concretos possuem a mesma OBSERVACAO.

Ela nao demonstra, por si so, que os estados concretos sao iguais.

A reflexao de uma repeticao abstrata exige hipotese adicional, como
injetividade da abstracao sobre a orbita alcancada.

Mesmo com essa hipotese formalizada, continua sendo responsabilidade do
adaptador da aplicacao provar que a funcao de abstracao representa
corretamente o sistema externo real.
```

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SEMANTIC_FOUNDATION
```

Simulação, abstração e reflexão de propriedades são material clássico de
métodos formais. O que a frente acrescenta é conectá-las, com prova, à
cadeia finita já verificada — e dizer com precisão onde a ponte quebra.

## O que este gate NÃO fez

```text
nao executou a frente selecionada;
nao criou modulo Lean permanente;
nao criou prova permanente;
nao executou lake build;
nao modificou frente encerrada;
nao iniciou extracao, CLI, parser ou integracao;
nao promoveu claim.
```
