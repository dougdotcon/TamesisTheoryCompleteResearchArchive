---
document_id: PROGRAM-STATE-AND-ROADMAP
generated_at_commit: ffedf33b26b146354c2a5b09592431fcebfb92fd
canonical_commit: 17c070fceba6f3c1600205ca9293228da73614a1
scope: consolidado do laboratorio formal
superseded_sections: "10 — resolvida pela secao 11"
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# Programa Tamesis — estado, cronologia e roadmap

Documento consolidado. Escrito a pedido, fora de gate, sem alterar
governança: nenhum status, autorização, claim ou lacuna foi tocado para
produzi-lo.

---

## 1. Checkpoint — onde estamos agora

```text
HEAD                    17c070fceba6f3c1600205ca9293228da73614a1
canonical_commit        17c070fceba6f3c1600205ca9293228da73614a1
active_work_item        FOUND-FINITE-STATE-ABSTRACTION-001
work_status             READY
specification_status    READY_FOR_REVIEW
authorized_action       FOUND_FINITE_STATE_ABSTRACTION_001_SPECIFICATION_REVIEW_AUTHORIZED
current_blocker         null
portfolio_review_status CONSUMED
yaml_duplicate_key_status VERIFIED_CLEAN
```

```text
claims no ledger        22
work items na fila      16
duplicatas YAML         0, em 55 arquivos
testes Python           21
lake build              PASS, 8757 jobs
arvore de trabalho      limpa
processos ativos        nenhum
```

**A frente ativa está READY e especificada.** O bloqueio descrito na
seção 10 foi resolvido pela **saída (b)**, registrada na seção 11: o
item foi renomeado para `FOUND-FINITE-STATE-ABSTRACTION-001` e a
especificação foi congelada.

### As cinco frentes encerradas

| Frente | Claim | Linhas Lean | Docs | Lacunas |
|---|---|---|---|---|
| `FOUND-SEMIGROUP-002` | `FINITE-DYNAMICS-FORMAL-001` | — | — | — |
| `FOUND-FUNCTIONAL-GRAPH-001` | `FUNCTIONAL-GRAPH-COMPONENT-FORMAL-001` | — | — | — |
| `FOUND-CYCLE-DETECTION-001` | `EXECUTABLE-CYCLE-WITNESS-FORMAL-001` | 334 | 42 | 19 |
| `ENG-FINITE-STATE-RUNTIME-001` | `FINITE-STATE-RUNTIME-ADAPTER-FORMAL-001` | 559 | 53 | 22 |
| `ENG-FINITE-STATE-ENCODING-001` | `CERTIFIED-FINITE-STATE-ENCODING-FORMAL-001` | 417 | 65 | 20 |

Todas com `work_status: VERIFIED`, `result_review: APPROVED` e
`extension_status: NOT_AUTHORIZED`. `RH-NOGO-001` permanece
`FROZEN_PARTIAL_RESULT`, `NOT_AUTHORIZED`, `NO_EXECUTION`.

---

## 2. O que está provado — a cadeia formal

Esta é a espinha do trabalho. Cada seta é teorema em Lean 4, verificado
pelo kernel, sem `sorry` e sem axioma local.

```text
X finito, f : X → X
    │  casa dos pombos limitada
    ▼
CycleWitness  ⟨baseIndex, period⟩,  com  f^[b+p] x = f^[b] x
    │  busca certificada por candidatos
    ▼
detectCycleWitness?          soundness + completeness
    │
    │  ═══ ENG-FINITE-STATE-RUNTIME-001 ═══
    ▼
Array Nat, possivelmente invalido
    │  validacao estrutural — destinos invalidos REJEITADOS, nunca corrigidos
    ▼
ValidatedTransitionTable
    │  Fin n → Fin n, total por construcao
    ▼
analyzeTransitionTable       soundness sobre o Array ORIGINAL
    │
    │  ═══ ENG-FINITE-STATE-ENCODING-001 ═══
    ▼
S tipado, stepS : S → S, com codificacao FORNECIDA S ≃ Fin n
    │  Array.ofFn — tabela construida e provada correspondente
    ▼
analyzeEncodedSystem
    │
    ▼
stepS^[b + p] start = stepS^[b] start        ← igualdade NO TIPO S
```

### As três garantias que definem o conjunto

```text
1. destinos invalidos sao REJEITADOS, nunca corrigidos;
2. o transporte de indice NAO altera o valor natural;
3. a soundness termina em igualdade no tipo do consumidor.
```

A primeira é sustentada por `validateTransitionTable_sound` e pelo
teorema anti-clamp `validateStart_sound`. A segunda, por `tableIndex_val`,
que é `rfl`. A terceira, por `encode_injective`, a última seta do DAG.

### O que o consumidor precisa fornecer

```text
Array Nat + Nat                              (runtime adapter)
CertifiedFiniteEncoding S n + stepS + start  (codificacao certificada)
```

**Zero typeclasses** em ambos os casos. Nem `Fintype`, nem `DecidableEq`,
nem habitação. Isso foi verificado por exemplos genéricos que falhariam
por instância ausente.

---

## 3. Cronologia estruturada

Dez commits nesta sequência, do adaptador de runtime até a seleção da
próxima fundação.

### Ciclo I — adaptador de runtime

| # | Commit | Gate | Resultado |
|---|---|---|---|
| 1 | `746102f` | formalização | 18 teoremas, 869 linhas; `analyzeTransitionTable_sound` e `_complete` compilaram na **primeira tentativa** |
| 2 | `861dc6b` | revisão de resultado | encerrada; cabeçalho de lacunas corrigido `10→11` e `8→7` |

**Descoberta central:** `ValidatedTransitionTable.run?_eq_iterate_step`
exigiu indução com o quantificador **no enunciado** (não `generalizing`),
dois `show` obrigatórios para expor o `bind` que a notação `do` esconde, e
`Function.iterate_succ_apply` — **não** a variante com apóstrofo.

### Ciclo II — codificação certificada

| # | Commit | Gate | Resultado |
|---|---|---|---|
| 3 | `4c15d4a` | portfólio | selecionada a codificação certificada, entre 6 alternativas |
| 4 | `2066edc` | especificação | 29 documentos; 13 resultados CORE **provados em probe** |
| 5 | `751cef8` | revisão | 5 correções de classificação; 10 documentos |
| 6 | `bdc67fb` | **correção de validação** | `ENC-VAL-001` |
| 7 | `2a05887` | formalização | 11 teoremas, 417 linhas; `lake build` 8757 jobs |
| 8 | `e9e2ce7` | revisão de resultado | encerrada; 12 documentos de fechamento |

**Descoberta central do ciclo:** `Array.size_ofFn` e `Array.getElem_ofFn`
são aceitos **em modo termo** por defeq e **rejeitados** por `rw`/`simp`,
que trabalham em transparência reduzida. Quatro rotas foram testadas; a
que passou foi o termo puro. E `Fintype.equivFin` é `noncomputable` — por
isso a codificação é **dado fornecido**, nunca derivada.

### Ciclo III — governança

| # | Commit | Gate | Resultado |
|---|---|---|---|
| 9 | `e0db1dc` | correção transversal | 8 duplicatas YAML corrigidas; validador permanente |
| 10 | `ffedf33` | portfólio | selecionada a abstração finita, entre 7 alternativas |

---

## 4. Descobertas técnicas — Lean e Mathlib

Registradas porque custaram tempo e porque a próxima frente vai reusá-las.

### APIs que resolveram problemas inteiros

```text
Function.Semiconj.iterate_right
    Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
    axiomas [propext]
```

Transformou a comutação de iteradas — que na frente do runtime custou
indução manual com dois `show` — em **um termo de uma linha**. Já foi
usada em duas frentes e será a espinha da terceira.

```text
Array.ofFn          computavel, [propext]
Array.size_ofFn     [propext]
Array.getElem_ofFn  [propext, Classical.choice, Quot.sound]
Fin.cast            SEM axiomas, preserva val definicionalmente
```

### Armadilhas confirmadas por medição

| Armadilha | Comportamento medido |
|---|---|
| `(Array.ofFn f).size = n := rfl` | **falha** para `n` genérico; passa só com tamanho literal |
| `rw [Array.getElem_ofFn]` sobre índice `Fin` | **não casa**; exige `show` convertendo para índice `Nat` |
| `do` sobre `Except` | **não** reduz por `simp`, `split` ou `simp only`; exige `unfold` + `rw [show … from dif_*]` + `show … .bind _ = _` + `rfl` |
| `List.find?_some` | unificação de ordem superior escolhe função constante; exige `(p := fun v => …)` explícito |
| `private` em Lean 4 | escopo de **módulo** — um auxiliar privado precisa morar no arquivo do seu consumidor |
| teste que importa `TamesisLab` | **não** pode ser registrado em `TamesisLab.lean`: ciclo de imports |
| `Fintype.equivFin` | `noncomputable`; `truncEquivFin` devolve `Trunc`, que não produz dado |

### Regra axiomática consolidada — sexta reafirmação

```text
a presenca infraestrutural de propext, Classical.choice e Quot.sound
NAO bloqueia se:
  nenhuma definicao for noncomputable;
  a avaliacao funcionar;
  nenhuma escolha classica produzir dado.
```

Medição mais fina obtida no último ciclo: `encode_injective` e
`encodedStep` **não dependem de axioma nenhum**; a pegada entra na
primeira declaração que consome a API de arrays — `buildTransitionTable`,
pelo campo `closed`.

---

## 5. Descobertas de governança

### `ENC-VAL-001` — exit 1 relatado como PASS

Um probe obrigatório terminou com `exit 1` porque continha experimentos
negativos intencionais, e foi reportado como `PASS`.

```text
Regra: experimentos negativos nao compartilham arquivo com probes
obrigatorios. Validacao obrigatoria termina com exit 0. Um processo com
exit 1 nunca eh evidencia de PASS.
```

Resultados negativos passam a ser formulados como **teoremas de negação
que compilam** — foi assim que o contraexemplo `BOOL_TO_UNIT` foi
formalizado depois.

### `META-ENC-003` — chaves YAML duplicadas

```text
yaml.safe_load("a: 1\na: 2\n")  ->  {"a": 2}
```

Sem erro, sem aviso. A varredura integral achou **8 ocorrências em 3
arquivos** — não as 3 que uma busca parcial havia encontrado. Duas
divergências novas apareceram **fora** da fila, e uma delas era séria:
o `STATUS.yaml` de uma frente encerrada era lido com
`extraction_status: READY_FOR_FEASIBILITY_AUDIT` quando o
`CLOSURE_RECORD` e o `LAB_STATE` dizem `NOT_AUTHORIZED` — **uma trava
mais fraca do que a governança de fato mantinha**.

```text
Regra: uma chave por mapa; duplicatas identicas tambem proibidas;
"ultimo valor vence" nao eh semantica de governanca; labctl rejeita
com DUPLICATE_YAML_KEY.
```

### Contagens escritas à mão — três divergências

```text
GAP_REGISTER do runtime      resolved_formally 10 declarado / 11 real
FINAL_PUBLIC_API             14 declarado / 15 real
tests_planned do runtime      9 e 8 no mesmo mapa
```

```text
Regra: contagem agregada nao eh fonte primaria. Deve ser derivada ou
conferida automaticamente contra as entradas, percorrendo TODAS elas.
```

### A lição que atravessa as três

Nos três casos o defeito não foi cálculo: foi **evidência mais fraca do
que a afirmação que ela sustentava**. Uma verificação parcial apresentada
como completa é o mesmo erro que um `exit 1` apresentado como `PASS`.

---

## 6. Lacunas abertas, consolidadas

### Científicas

```text
GAP-A  correcao da abstracao externa            RT-GAP-017, ENC-GAP-019
GAP-B  abstracoes muitos-para-um                a proxima frente
GAP-C  ciclos abstratos espurios                a proxima frente
```

### De engenharia

```text
GAP-D  invariancia do witness sob recodificacao  ENC-GAP-020
GAP-E  extracao nativa                           RT-GAP-013
GAP-F  CLI e parser                              RT-GAP-014, RT-GAP-015
GAP-G  diagnostico detalhado                     RT-GAP-022
       modelo de custo                           RT-GAP-019, ENC-GAP-020
       testes que importam a raiz                RT-GAP-018
```

### De governança

```text
GAP-H  YAML em front matter Markdown nao coberto pelo scanner
```

Auditado: 429 arquivos Markdown, 277 com front matter, **0** com
duplicata. A lacuna é real — o scanner seleciona por extensão — mas não
está sendo explorada.

### Bibliográficas

```text
nenhuma fonte primaria consultada em nenhuma das tres frentes formais
```

---

## 7. O que a próxima frente vai provar

`FOUND-FINITE-STATE-ABSTRACTION-001` já teve suas peças centrais **compiladas
em probe descartável** durante o gate de portfólio. O que falta é
especificá-las, revisá-las e formalizá-las em módulos permanentes.

### A pergunta

A cadeia atual resolve o caso **exato**: `S ≃ Fin n`, nada se perde.
Falta o caso em que **se perde** — abstração muitos-para-um.

### A resposta, em três peças já verificadas

```lean
-- 1. preserva, sempre
abstract (stepC^[b+p] start) = abstract (stepC^[b] start)

-- 2. a reflexao ingenua eh FALSA
theorem naive_cycle_reflection_is_false : ¬ (∀ …)     -- sem axiomas

-- 3. recupera, sob hipotese explicita
OrbitSeparating abstract stepC start →
  stepC^[b+p] start = stepC^[b] start
```

O contraexemplo é `Bool → Unit` com `stepC = not`: o sistema abstrato
repete em um passo, o concreto não.

```lean
def OrbitSeparating (abstract : C → A) (stepC : C → C) (start : C) : Prop :=
  ∀ i j : Nat,
    abstract (stepC^[i] start) = abstract (stepC^[j] start) →
      stepC^[i] start = stepC^[j] start
```

Verificado: **não tautológica** (falha no contraexemplo, provado sem
axiomas), **satisfazível** (toda abstração injetiva a cumpre),
**equivalente** a `Set.InjOn` sobre a órbita, e **não exige** `C` finito
nem `DecidableEq C`.

### As duas frases que a frente deve deixar

```text
A analise abstrata sempre pode produzir um witness observacional.

Esse witness somente se torna uma repeticao concreta quando a abstracao
separa os estados relevantes da orbita.
```

---

## 8. Roadmap

### Imediato — desbloquear e especificar

```text
0.  resolver o identificador  (secao 11)    CONCLUIDO
1.  FOUND-FINITE-STATE-ABSTRACTION-001-SPECIFICATION   CONCLUIDO
2.  ...-SPECIFICATION-REVIEW
3.  ...-FORMALIZATION
4.  ...-RESULT-REVIEW
```

Estimativa: quatro gates, o padrão já rodado duas vezes. As peças
matemáticas já compilaram; o custo é de especificação e auditoria, não de
descoberta.

### Médio prazo — as escolhas que vêm depois

Em ordem de prioridade defensável hoje, sujeita a revisão de portfólio:

```text
A. invariancia do witness sob recodificacao   fecha GAP-D
   risco: acoplamento com a ordem de enumeracao do detector

B. extracao nativa                            fecha GAP-E
   so faz sentido DEPOIS de um contrato semantico para o caso geral

C. diagnostico detalhado                      fecha GAP-G
   barato, seguro, incremento cientifico proximo de zero

D. front matter YAML                          fecha GAP-H
   barato; sem risco imediato medido
```

**A ordem não é acidental.** `B` e `C` produzem coisas visíveis; `A` e a
abstração produzem coisas verdadeiras. O laboratório tem escolhido
verdade antes de visibilidade em cinco portfólios seguidos, e a razão é
sempre a mesma: distribuir uma garantia que ainda não existe amplifica o
buraco em vez de fechá-lo.

### Longo prazo — onde queremos chegar

O destino declarado não é uma CLI nem um binário. É este enunciado:

```text
Dado um sistema real,
uma abstracao finita dele,
e prova de que a abstracao comuta e separa a orbita,

o laboratorio produz um certificado formal sobre o SISTEMA,
nao sobre a tabela.
```

Hoje temos as três primeiras setas. O que falta, e provavelmente sempre
faltará como obrigação **do modelador**, é a primeira ponte: que a
abstração represente o sistema real. Nenhuma frente formal responde isso
por quem modela.

Depois da abstração finita, as continuações plausíveis — **nenhuma
autorizada** — são:

```text
bissimulacao          quando a abstracao preserva nos dois sentidos
quocientes            abstracao canonica por relacao de equivalencia
concretizacao γ       conexao de Galois entre concreto e abstrato
transicoes nao deterministas    stepC : C → Set C
```

E as frentes matemáticas independentes — Navier–Stokes, P vs NP,
Yang–Mills, Hodge, BSD, Riemann, TOE — permanecem `SCOPED` na fila, sem
autorização, com risco epistemológico registrado como `EXTREME` e sem
produto verificável em trinta dias.

---

## 9. O que não afirmamos

Registro permanente, porque é a parte mais fácil de erodir.

```text
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE / FORMAL_SEMANTIC_FOUNDATION
```

```text
Nao ha algoritmo novo. Casa dos pombos, busca limitada por candidatos,
codificacao de tipo finito como Fin n e semiconjugacao sao material
classico.

Nao ha novidade matematica. Nada aqui avanca a fronteira; o que avanca
eh a VERIFICACAO de coisas conhecidas dentro de uma cadeia auditavel.

Nao ha progresso sobre a Hipotese de Riemann. Hilbert-Polya nao eh
excluida, e RH-NOGO-001 permanece congelada por decisao propria.

Nao ha evidencia fisica, modelo universal de sistemas, nem correcao
automatica de workflows, agentes ou programas externos.

Reutilizacao em software nao transforma resultado padrao em descoberta
cientifica. Isto foi escrito sete vezes, uma por frente.
```

---

## 10. O bloqueio atual, e as duas saídas

Dois gates consecutivos pararam no preflight. Nenhum deles falhou por
erro de execução.

### Os fatos, medidos

```text
HEAD                          ffedf33  "lab: select certified finite abstraction foundation"
commit de especificacao       NAO existe  (git log --grep = 0)
pasta 02_FOUNDATIONS/04_FINITE_ABSTRACTION   AUSENTE

id exigido pelos dois gates   FOUND-FINITE-STATE-ABSTRACTION-001
id registrado no repositorio  FOUND-FINITE-ABSTRACTION-001

ocorrencias do id com "STATE" em todo o laboratorio:  0
aliases_active                0
duplicate_work_items          0
```

> **Superada pela seção 11.** O parágrafo abaixo registra a leitura
> feita naquele momento; a decisão executada foi a **saída (b)**.

O identificador canônico é **inequívoco**: `FOUND-FINITE-ABSTRACTION-001`.
A forma com `STATE` **não existe no repositório** — ela aparece apenas no
texto dos dois últimos prompts de gate. Não há conflito de identificadores
a corrigir; há um desencontro entre o nome que o gate de portfólio ditou
(§20, `FOUND-FINITE-ABSTRACTION-001`) e o nome que os gates seguintes
pediram.

### Consequência em cadeia

```text
gate de PREPARACAO   parou no §0   item exigido inexistente
gate de REVISAO      parou no §1   especificacao inexistente, porque o
                                   gate anterior nao pode rodar
```

### Saída (a) — reemitir com o nome registrado

Trocar, no texto do gate, `FOUND-FINITE-STATE-ABSTRACTION-001` por
`FOUND-FINITE-ABSTRACTION-001` e `FOUND_FINITE_STATE_ABSTRACTION_001_*`
por `FOUND_FINITE_ABSTRACTION_001_*`.

```text
custo            zero commits de governanca
risco            nenhum
conteudo do gate integralmente aproveitavel
```

### Saída (b) — renomear o item

Gate corretivo que altere a fila, o allowlist, o conjunto de
`active_work_item` e a pré-condição em `labctl.py`, e só então reemitir a
especificação.

```text
custo            um commit adicional de governanca
ganho            o nome casa com ENG-FINITE-STATE-RUNTIME-001 e
                 ENG-FINITE-STATE-ENCODING-001
```

**Recomendação:** (b), se o padrão `FINITE-STATE` for para ficar — o
laboratório já tem duas frentes com ele, e nomes consistentes valem um
commit. (a), se a prioridade for retomar a matemática imediatamente.

A decisão é sua. Nenhuma das duas foi tomada por conta própria.

---

## 11. Números finais

```text
commits nesta sequencia          10
claims                           22   (6 VERIFIED nas frentes formais)
work items                       16
frentes encerradas                5
linhas Lean nas tres frentes    1310
arquivos de teste Lean            13
documentos nas tres frentes      160
lacunas registradas               61
testes Python                     21
lake build                     8757 jobs, PASS
duplicatas YAML                    0
arquivos Lean com sorry            0
axiomas locais                     0
```

---

## 11. Resolução do identificador — saída (b), executada

A seção 10 apresentou duas saídas. A executada foi a **(b)**: renomear o
item.

```text
identificador canonico   FOUND-FINITE-STATE-ABSTRACTION-001
nome candidato anterior  FOUND-FINITE-ABSTRACTION-001
aliases operacionais ativos   0
work items duplicados         0
```

### Por que (b), e não (a)

O nome com `STATE` casa com `ENG-FINITE-STATE-RUNTIME-001` e
`ENG-FINITE-STATE-ENCODING-001`, e nomeia o objeto real da frente: a
abstração de **estados finitos**, que consome `CertifiedFiniteEncoding`.
A saída (a) teria congelado uma inconsistência de nomenclatura na trilha
inteira para poupar um commit.

### Superfície migrada

```text
LAB_STATE.md                      active_work_item, authorized_action
01_PORTFOLIO/RESEARCH_QUEUE.yaml  work_item_id, authorized_next_gate
10_TOOLS/labctl.py                gate de sequencia, pre-condicao, allowlist
01_PORTFOLIO/FINITE_ABSTRACTION_CANDIDATE.md   work_item_id
PROGRAM_STATE_AND_ROADMAP.md      secoes 1, 7 e 10
```

Artefatos imutáveis de gates encerrados — `*-result.json`, relatórios de
sessão, revisões de portfólio — **preservam** o nome anterior. Eles são
registro histórico, não item ativo.

### Além do rename

O mesmo gate reconstruiu a especificação que faltava, em
`02_FOUNDATIONS/07_FINITE_ABSTRACTION/FOUND_FINITE_STATE_ABSTRACTION_001/`.
A numeração `07` foi escolhida porque `04`, `05` e `06` já estão em uso
em `02_FOUNDATIONS`.

```text
probe descartavel        exit 0
declaracoes publicas     7
gaps                     20, nenhum fechado
stop conditions          18, nenhuma disparada
claims promovidas        0
arquivos Lean criados    0
```
