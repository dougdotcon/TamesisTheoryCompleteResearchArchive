---
document_id: NEXT-WORK-ITEM-FINITE-STATE-RUNTIME
work_item_id: ENG-FINITE-STATE-RUNTIME-001
status: SCOPED
decided_at: 2026-08-01
authorized_action: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
---

# ENG-FINITE-STATE-RUNTIME-001 — decisão e escopo preliminar

> **Escopo apenas.** Nada é congelado aqui. Nenhum arquivo Lean, nenhuma
> prova, nenhum adaptador, nenhum executável.

## Identificação

```yaml
work_item_id: ENG-FINITE-STATE-RUNTIME-001
title: "Certified Runtime Adapter for Finite Deterministic Systems"
track: ENGINEERING_FOUNDATION
work_status: SCOPED
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

## A limitação atacada

`FOUND-CYCLE-DETECTION-001` opera sobre:

```text
X : Type*
[Fintype X]
[DecidableEq X]
f : X -> X
x : X
```

Interface ideal para matemática e para programas escritos **dentro** do
Lean. Ela **não** recebe:

```text
arrays carregados em runtime;
tabelas de transicao;
JSON;
CSV;
estados numerados externos;
configuracoes de workflows;
logs ou modelos vindos de outros sistemas.
```

A frente ataca a lacuna entre

```text
funcao total tipada dentro do Lean
```

e

```text
dados dinamicos potencialmente invalidos.
```

## Representação bruta candidata

```lean
structure RawTransitionTable where
  next : Array Nat
```

**Sem** campo `size`, porque `size = next.size` é derivável — a mesma
disciplina que rejeitou `entryPoint` em `CycleWitness`. **Sem** prova
embutida: a tabela bruta *pode* conter destinos inválidos, e é isso que a
torna a representação certa para a entrada.

Alternativas a comparar na especificação: `Array Nat`, `List Nat`,
`Array UInt64`, `ByteArray`.

Recomendação preliminar: **`Array Nat`** — estrutura executável, índices
naturais, acesso direto, integração razoável com `Fin`, facilidade para
`#eval`, e nenhum parser externo no núcleo inicial.

## Validade da tabela

```lean
def RawTransitionTable.Valid (t : RawTransitionTable) : Prop :=
  ∀ i : Nat, i < t.next.size → t.next[i] < t.next.size
```

A assinatura final deverá usar a API segura de acesso do checkout; pode
ser necessário formular por `∀ i : Fin t.next.size, t.next[i] < t.next.size`.
A especificação deve **comparar as duas** — a versão com `Fin` costuma ser
mais fácil de consumir, a versão com `Nat` mais fácil de produzir a partir
de um laço de validação.

O que a validade significa:

```text
todo estado registrado possui exatamente um sucessor;
todo sucessor permanece dentro do mesmo espaco finito.
```

O que ela **não** significa:

```text
todos os estados sao alcancaveis;
ha um unico componente;
ha um unico ciclo global;
a tabela eh nao vazia;
o estado inicial eh valido.
```

## Sistema validado candidato

Duas rotas a comparar:

```lean
structure ValidatedTransitionTable where
  next : Array Nat
  closed : ∀ i : Fin next.size, next[i] < next.size
```

ou dado executável puro com certificado separado:

```lean
structure FiniteTransitionSystem where
  stateCount : Nat
  stepIndex : Nat → Nat
```

Recomendação: **manter dado executável e provas separados sempre que
possível**, evitar redundância entre `stateCount` e `Array.size`, e não
armazenar funções arbitrárias quando uma tabela concreta basta. A segunda
rota reintroduz exatamente a redundância que a primeira evita.

A especificação decidirá se o resultado da validação é um
`Subtype RawTransitionTable.Valid` ou uma estrutura nomeada.

## Validação executável

```lean
def validateTransitionTable (t : RawTransitionTable) :
    Except TransitionValidationError ValidatedTransitionTable

inductive TransitionValidationError
  | emptyTable
  | destinationOutOfBounds (source destination stateCount : Nat)
```

**Não congelar ainda**: formato textual, JSON, mensagens humanas, códigos
de saída, localização do arquivo.

### Tabela vazia

Recomendação preliminar: **permitir representar tabela vazia** e rejeitar
qualquer tentativa de execução sem estado inicial. Isso preserva a
separação entre **validade estrutural** e **validade da consulta** — uma
tabela vazia é estruturalmente coerente (nenhum destino viola nada); o que
não existe é estado inicial. `RT-GAP-005`.

## Estado inicial dinâmico

```text
start : Nat        precisa de   start < table.next.size
```

```lean
| initialStateOutOfBounds (start stateCount : Nat)
```

A especificação deve manter **três** validações separadas:

```text
validacao da tabela;
validacao da consulta;
execucao do detector.
```

Não combinar tudo em um único `Bool` — a informação de *qual* validação
falhou é o produto principal para o consumidor.

## Função de transição tipada

```lean
def ValidatedTransitionTable.step (t : ValidatedTransitionTable) :
    Fin t.next.size → Fin t.next.size
```

derivada do array e da prova de fechamento.

**Proibições vinculantes:**

```text
Classical.choose;
fallback para zero;
mod para forcar o destino aos limites;
clamp;
valor padrao silencioso.
```

Destinos inválidos são **rejeitados pela validação**, não "corrigidos".
Um `% n` silencioso transformaria uma tabela errada em um sistema
diferente — e o certificado devolvido seria correto sobre um sistema que
o usuário nunca descreveu. É o modo de falha mais perigoso desta frente.

## Ponte semântica — o principal resultado formal

```lean
theorem step_val (t : ValidatedTransitionTable) (i : Fin t.next.size) :
    (t.step i : Nat) = t.next[i]

theorem iterate_step_corresponds
```

A segunda diz que **iterar a função tipada sobre `Fin` corresponde a
seguir repetidamente os índices da tabela**. Sem ela, o certificado fala
de um objeto Lean que ninguém consegue relacionar com o dado de entrada.

A teoria de ciclos **não** é reimplementada.

## Aplicação do detector

```lean
def detectTableCycle? (t : ValidatedTransitionTable)
    (start : Fin t.next.size) : Option CycleWitness :=
  detectCycleWitness? t.step start
```

Como o detector já é completo, a função devolve `some` para toda chamada
bem tipada. A API pode continuar com `Option`. **Não totalizar** nesta
frente sem autorização específica.

## API dinâmica candidata

```text
RawTransitionTable
        |
validateTransitionTable
        |
ValidatedTransitionTable
        |
validate start
        |
Fin table.size
        |
detectTableCycle?
        |
CycleWitness
```

```lean
def analyzeTransitionTable (next : Array Nat) (start : Nat) :
    Except RuntimeCycleError CycleWitness
```

A especificação decidirá se esta função pertence ao primeiro núcleo. Ela
precisa distinguir **tabela inválida**, **estado inicial inválido** e
**falha interna impossível do detector** — e **não** esconder o ramo
impossível com certificado falso.

## O ramo impossível

`detectCycleWitness?_complete` prova que o detector nunca devolve `none`
em chamada bem tipada. Um caso `internalDetectorFailure` só é admissível
se for **defesa operacional**, **documentado como proposicionalmente
impossível** e **não usado para mascarar erro de validação**.

Três rotas a comparar, **sem decidir agora**: devolver `Option` dentro de
`Except`; usar a prova para eliminar o `none`; manter erro defensivo.
`RT-GAP-011`, `RT-GAP-012`.

## Resultados principais candidatos

```text
RT-001  validacao correta      sucesso -> RawTransitionTable.Valid
RT-002  validacao completa     Valid -> sem erro estrutural
RT-003  transicao preservada   step corresponde a tabela original
RT-004  iteracao preservada    iteradas correspondem a execucao da tabela
RT-005  witness no dominio     detectTableCycle? devolve witness valido
RT-006  witness na tabela      a igualdade certificada corresponde a
                               repeticao dos mesmos indices
RT-007  execucao segura        tabela valida + start no limite ->
                               certificado correto
```

**Não autorizados ainda**: parsing JSON, arquivo de configuração,
servidor HTTP, integração com parser real, integração com pipeline real,
otimização Floyd, benchmark.

## Extração e execução nativa

Auditoria futura de `#eval`, `lake env lean`, alvo executável do Lake,
compilação nativa e argumentos CLI simples. Mas o **primeiro núcleo**
permanece separado de parsing de arquivo, biblioteca JSON, interface web,
banco de dados e rede.

```text
A execucao nativa deve ser CONSEQUENCIA do adaptador, nao seu
substituto.
```

## Casos de teste preliminares

```text
RT-TEST-001  []                          decisao sobre tabela vazia
RT-TEST-002  [1]                         destino fora dos limites
RT-TEST-003  [0], start = 1              estado inicial fora dos limites
RT-TEST-004  [0], start = 0              esperado <0,1>
RT-TEST-005  [1,0], start = 0            esperado <0,2>
RT-TEST-006  [1,2,2], start = 0          esperado <2,1>
RT-TEST-007  [1,2,3,2], start = 0        esperado <2,2>
RT-TEST-008  varios starts na mesma tabela
```

Os quatro últimos valores reproduzem, **em forma de tabela**, exatamente
os modelos `Fin 1`, `Bool`, `Fin 3` e `Fin 4` já verificados no detector —
o que torna a frente comparável contra um oráculo já existente.

`RT-TEST-008` **não** deve ser interpretado como enumeração global dos
componentes.

## Aplicações

| Aplicação | Classificação |
|---|---|
| autômatos | `DIRECT_WITH_TABLE` |
| configurações finitas | `DIRECT_WITH_TABLE` |
| máquinas de estado | `DIRECT_WITH_TABLE` |
| workflows | `REQUIRES_STATE_ENCODING` |
| auditoria de transições | `REQUIRES_STATE_ENCODING` |
| retries | `REQUIRES_STATE_ENCODING` |
| pipelines | `REQUIRES_ABSTRACTION_PROOF` |
| parsers | `REQUIRES_ABSTRACTION_PROOF` |
| agentes determinísticos | `REQUIRES_ABSTRACTION_PROOF` |
| jogos | `CONCEPTUAL_ONLY` |

Registro explícito e vinculante:

```text
converter um sistema real para uma tabela finita eh uma ABSTRACAO;
a correcao dessa abstracao NAO eh automaticamente fornecida pelo
detector nem pelo adaptador.
```

O adaptador garante que *a tabela dada* é analisada corretamente. Que *a
tabela represente o sistema real* é responsabilidade de quem a produziu.
`RT-GAP-017`.

## Gaps iniciais

```yaml
RT-GAP-001: {title: representacao bruta da tabela, status: OPEN}
RT-GAP-002: {title: predicado de fechamento dos destinos, status: OPEN}
RT-GAP-003: {title: validacao executavel da tabela, status: OPEN}
RT-GAP-004: {title: representacao da tabela validada, status: OPEN}
RT-GAP-005: {title: tratamento da tabela vazia, status: OPEN}
RT-GAP-006: {title: validacao do estado inicial, status: OPEN}
RT-GAP-007: {title: construcao de Fin n -> Fin n, status: OPEN}
RT-GAP-008: {title: correspondencia entre step e lookup, status: OPEN}
RT-GAP-009: {title: correspondencia entre iteracoes e execucao da tabela, status: OPEN}
RT-GAP-010: {title: aplicacao de detectCycleWitness?, status: OPEN}
RT-GAP-011: {title: eliminacao ou preservacao do Option, status: OPEN}
RT-GAP-012: {title: modelo de erros dinamicos, status: OPEN}
RT-GAP-013: {title: execucao nativa via Lake, status: OPEN}
RT-GAP-014: {title: interface CLI minima, status: OPEN}
RT-GAP-015: {title: parsing de formato externo, status: OPEN}
RT-GAP-016: {title: extracao de certificado para tipos externos, status: OPEN}
RT-GAP-017: {title: abstracao de sistemas reais em estados finitos, status: OPEN}
RT-GAP-018: {title: arquitetura de testes que importam a raiz, status: OPEN}
RT-GAP-019: {title: complexidade e escalabilidade, status: OPEN}
RT-GAP-020: {title: fronteira de novidade, status: OPEN}
RT-GAP-021: {title: bibliografia de verificacao de maquinas de estado, status: OPEN}
```

Vinte e uma, nenhuma fechada.

## Stop conditions

```text
destinos invalidos corrigidos por modulo;
fallback silencioso;
estado inicial invalido convertido por modulo;
tabela validada podendo apontar para fora do dominio;
Classical.choose produzindo dados;
execucao dependendo de periodicOrbit;
o adaptador repetindo o detector;
o pigeonhole repetido;
parsing JSON misturado ao nucleo formal;
servidor ou rede na primeira versao;
Floyd como dependencia;
totalizacao do detector tornada obrigatoria;
abstracao de sistema real declarada automaticamente correta;
complexidade afirmada sem modelo;
novidade matematica ou algoritmica reivindicada;
TRI, TDTR, TOE, fisica ou Clay conectados.
```

## Limites científicos

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

```text
Representar uma maquina de estados finita por uma tabela de
transicoes e validar seus indices eh engenharia formal padrao.

O valor deste work item estara na ligacao verificavel entre dados
dinamicos, uma funcao total sobre Fin n e o detector de ciclos ja
formalizado.

A frente nao propoe um novo algoritmo nem uma nova teoria.
```

Proibido afirmar: novo modelo de computação, novo algoritmo, nova teoria
de autômatos, descoberta, resultado físico.

## Dependências

```text
FOUND-SEMIGROUP-002
        |
FOUND-FUNCTIONAL-GRAPH-001
        |
FOUND-CYCLE-DETECTION-001
        |
ENG-FINITE-STATE-RUNTIME-001
```

```yaml
FOUND-CYCLE-DETECTION-001:
  dependency_type:
    - FORMAL_API
    - EXECUTABLE_CORE
    - CORRECTNESS_THEOREMS
```

**Não** é extensão autorizada da frente encerrada: o
`extension_status` de `FOUND-CYCLE-DETECTION-001` permanece
`NOT_AUTHORIZED`, e a nova frente apenas **consome** sua API pública.

## Próximo passo autorizado

```yaml
authorized_action: ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_PREPARATION_AUTHORIZED
```

Preparar a especificação. **Nenhuma formalização. Nenhum arquivo Lean.
Nenhum executável. Nenhum CLI. Nenhum JSON. Nenhuma integração.**
