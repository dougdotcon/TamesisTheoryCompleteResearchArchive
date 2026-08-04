# Changelog do laboratório formal

## ENG-RUNTIME-SOUNDNESS-002-CLOSURE - 2026-08-04

### Paid

- **A divida esta paga na origem.** `lake build` exit `0`, `8811` jobs,
  `0` `error:`.

```text
copias da reducao do bloco do   4  ->  0
auxiliares privados removidos   3
declaracoes publicas novas      2
assinaturas quebradas           0
mudancas de semantica           0
```

- Verificado por grep: `private theorem analyze_reduce` -> **0**;
  `analyze_reduce_public|_cb|_u` -> **0**.

### Simplified

- Duas provas de dez linhas viraram **uma projecao cada**:

```lean
analyzeTransitionTable_period_pos := (analyzeTransitionTable_rawValid h).2.1
analyzeTransitionTable_bound      := (analyzeTransitionTable_rawValid h).2.2.1
```

### Closed

- `CB-GAP-004` e `UP-GAP-002` **FECHADAS**.
- `ENG-RUNTIME-SOUNDNESS-002` — **decima quinta** frente encerrada.

### Preserved

- `analyzeTransitionTable_sound` **intacta**, `analyzeTransitionTable`
  com semantica inalterada, ramo `internalDetectorFailure` no lugar.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`.
- `DEC-048` registrado no mesmo commit que faz sua edicao.

## BUILDABLE-PIECES - 2026-08-04

### Found

- A quinta medicao paralela fechou o quadro: as sondas nao acharam so
  bloqueios, acharam **4 pecas nomeaveis e autocontidas**, cada uma com
  valor upstream independente do problema que destrava.

```text
B  enumeracao espectral de compactos   RH      moderate
C  Mordell-Weil f.g. sobre Q           BSD     moderate
D  equivalencia racional e Chow        Hodge   PR-scale
A  multiplicador L2 sem suavidade      NS      high
```

### Peca C — o achado da rodada

- `CommGroup.fg_of_descent'` existe no Mathlib e tem **ZERO consumidores
  em toda a arvore**. Junto com `Height.logHeight` e
  `abs_logHeight_addSubMap_sub_two_mul_logHeight_le`, sao tres insumos
  prontos e **desconectados**.
- Falta so a altura ingenua em pontos — **TODO explicito** no proprio
  `Mathlib/NumberTheory/Height/EllipticCurve.lean`. Fechar a cadeia da
  **Mordell-Weil finitamente gerado**, sem o qual `rank` e indefinivel.

### Corrected

- **`EllipticCurve` foi REMOVIDA do Mathlib**, refatorada em
  `WeierstrassCurve` + `IsElliptic`. Novo desde julho: `localEulerFactor`,
  `LFunction`, `LSeries`.
- Mas `LFunction` e serie de Dirichlet **formal**: sem convergencia, sem
  continuacao, sem equacao funcional. `ord_{s=1} L(E,s)` **nao e
  expressavel**, e as **5** quantidades da formula BSD sao todas
  indefiniveis.

### Hodge

- `AlgebraicCycle` existe ha semanas; falta **equivalencia racional**,
  logo falta grupo de Chow. Definir a equivalencia e escala-PR.
- Os **dois** lados da bicondicional carecem de objetos: sem de Rham
  algebrico, sem Betti, sem comparacao, sem (p,q), sem variedade
  complexa, sem `QuasiCoherent`, sem cotangente relativo. `H^q(X, Ω^p)`
  e **informulavel**.
- Homonimo registrado: `RingTheory/Kaehler` e **diferenciais**, nao
  metrica.

### Not claimed

- Peca C da **Mordell-Weil**, nao BSD. Peca D da **Chow**, nao Hodge.
  Nenhum dos 6 ficou alcancavel, e nenhum gate foi aberto.

## OPEN-PROBLEMS-MEASURED - 2026-08-04

### Measured in parallel

- **Cinco medicoes concorrentes**, todas por elaboracao, todas `exit 0`,
  todas somente-leitura com `git_dirty=0` conferido individualmente.
  Primeira vez que o laboratorio mede varias frentes ao mesmo tempo.

### Corrected

- `ATTACK_READINESS.md` classificava os cinco problemas de baixo como
  tendo **primeiro passo bibliografico**. Medido, isso esta errado em
  **tres dos cinco**.

```text
NS-PRESSURE-001    FORMAL   projetor de Leray            high
RH-NOGO-001        FORMAL   enumeracao espectral         very_high
TOE-INTERFACE-001  falta o OBJETO, nao a ferramenta      moderate
YM-LIMIT-001       bibliografico, confirmado             very_high
PVSNP-PHYS-001     formal, mas escala de pesquisa        very_high
```

### `TOE-INTERFACE-001` — o achado que separa

- **O bloqueio nao e do toolchain.** `CategoryTheory` elabora **15 de
  15**: `Category`, `Functor`, `Adjunction`, `Limits`, `Monad`, `Sheaf`,
  `MonoidalCategory`, `Abelian`. O alvo da fila e especificacao
  categorial, nao fisica, e a base esta **completa**.
- Falta o **objeto**: nao existe definicao candidata de "regime" nem de
  "interface" em lugar nenhum. Custo rebaixado de `very_high` para
  **`moderate`** no passo formal.
- E `TamesisLab/TOE.lean` tem **8 linhas**, com
  `theorem toe_smoke : True := by trivial` — **caso-limite do defeito de
  vacuidade**. `YangMills.lean` e identico. Os dois diretorios so tem
  `.gitkeep`.

### `RH-NOGO-001` — a lacuna era maior que o registrado

- `GLOBAL-WEYL-BRIDGE-SCALAR` supunha faltar so calculo
  pseudodiferencial. Falta **tudo**: classes de Hormander, parametrix,
  elipticidade, Schatten, traco, Rellich-Kondrachov, medida riemanniana,
  Laplace-Beltrami. Todo "Weyl" no Mathlib e **grupo** de Weyl.
- Mas ha primeiro passo formal com valor proprio: estender
  `IsSymmetric.eigenvalues` de dimensao finita para **compactos
  autoadjuntos em Hilbert separavel**, produzindo `N(λ)`. Apoia-se em
  dois lemas que **ja existem**, e e contribuicao upstream
  **independente de RH**.

### `YM-LIMIT-001` — tres abismos

- Falta `PrincipalBundle`, `Connection`, `Curvature`: a acao de
  Yang-Mills **classica** nao e enunciavel. Falta Bochner-Minlos: nem o
  campo **livre** e construivel. Falta Wightman/OS: o **enunciado** do
  gap nao existe.
- Ter `LieGroup` + `VectorBundle` + `SchwartzMap` cria **ilusao de
  proximidade** — vocabulario partilhado, maquinaria nenhuma.

### Not claimed

- **Nenhum dos 6 ficou alcancavel, e nenhum foi aberto.** Primeiro passo
  formal nao significa primeiro passo barato. `authorized_action` nao
  muda.

## NS-PRESSURE-FIRST-STEP-MEASURED - 2026-08-04

### Corrected

- `ATTACK_READINESS.md` afirmava que o primeiro passo dos cinco problemas
  de baixo seria **bibliografico**. Medido por elaboracao, `exit 0`, isso
  esta **errado para `NS-PRESSURE-001`**: o primeiro passo e **formal**,
  e o gargalo tem nome.
- Custo revisto de `very_high` para **`high`**. A tabela original **nao
  foi reescrita** — a correcao fica registrada ao lado dela.

### Measured

- Mathlib **tem** `H^s` via distribuicoes temperadas
  (`TemperedDistribution.MemSobolev`, `besselPotential`), Gagliardo-
  Nirenberg-Sobolev (`eLpNorm_le_eLpNorm_fderiv`) e Laplaciano.
- Mathlib **nao tem**, com zero ocorrencias em toda a arvore: `Leray`,
  `Helmholtz`, `Riesz transform`, `Calderon`, `Zygmund`, `Mikhlin`,
  `Hormander`, `maximal function`, `Navier`, `fluid`.

### The bottleneck, named

- A pressao exige o **projetor de Leray**, simbolo
  `δ_jk - ξ_jξ_k/|ξ|²` — limitado mas **descontinuo na origem**.
- O unico lema de multiplicador disponivel,
  `MemSobolev.fourierMultiplierCLM_of_bounded`, exige
  `HasTemperateGrowth`, que comeca com `ContDiff ℝ ∞` **global**. A
  hipotese falha, e nao ha rota alternativa.
- **Primeiro passo real**: trocar `HasTemperateGrowth` por
  mensurabilidade mais limitacao essencial, caso `L²`, onde e
  **Plancherel puro**. Lema autocontido.

### Non-vacuous

- O agente construiu `IsNSSolution` do zero com primitivas e provou os
  **dois** lados: escoamento uniforme **e** solucao, campo radial
  **nao** e. Satisfazivel e refutavel — cumpre
  `positive_instance_required`.

### Not claimed

- `NS-PRESSURE-001` **nao** ficou proximo, e **nao** foi aberto.
  Regularidade de Navier-Stokes segue fora de alcance. A medicao corrige
  **uma classificacao**, nada mais.

## COST-MODEL-PRICE-MEASURED - 2026-08-04

### Measured

- `DEC-046` chamou o custo de instanciar `TM2ComputableInPolyTime` de
  "caro". Medicao por elaboracao, `exit 0`, trocou o adjetivo por
  numeros — e o numero e pior.
- `FinTM2` exige **14 campos**. O unico exemplo do Mathlib custa
  **20 linhas** para uma maquina que **nao computa nada**: `m _ := halt`,
  para no passo 1, e `evals_in_steps` fecha com `rfl`. O piso medido e
  **vacuo**.
- `TM2OutputsInTime` e **`Type`, nao `Prop`**: o traco de execucao e
  **dado a construir**, nao existencia a afirmar.

### Found missing

- **Nenhum segundo exemplo** em todo o Mathlib: `grep -rl FinTM2` retorna
  1 arquivo.
- **Nenhuma composicao**: `TM2ComputableInPolyTime.comp` e
  `proof_wanted`. A construcao nao e modular.
- **Nenhuma ponte utilizavel**: `ToPartrec.lean` (1290 linhas) vai de
  `Partrec` a TM2 mas **nao produz `FinTM2`**, e `Fintype
  PartrecToTM2.Λ'` e **FALSE** — medido, nao suposto. O Mathlib contorna
  com `TM2.Supports`, condicao estritamente mais fraca.
- **Nenhum limite polinomial**: o cabecalho de `ToPartrec.lean` diz
  textualmente *"We don't prove it here"*. O limite e **nao-teorema
  declarado**.
- **Nenhuma codificacao reutilizavel**: `Encoding.lean` cobre `Nat`,
  `Bool`, `List` e `Prod`. Nada para `Array`, `Except` ou struct.

### Verdict

- Instanciar o modelo de custo para `analyzeTransitionTable` e frente de
  **escala de pesquisa, 4 digitos de linhas, com risco de nao fechar** —
  e exigiria fazer primeiro algo que **o Mathlib nunca fez para funcao
  nenhuma**: limite de passos polinomial sobre uma TM2 concreta.
- O laboratorio nao estaria aplicando teoria existente. Estaria
  criando-a.

### Unchanged

- `PVSNP-PHYS-001` continua `SCOPED`. Nenhum gate foi aberto por esta
  medicao, e `authorized_action` nao muda.

## ENG-RUNTIME-SOUNDNESS-002-SPECIFICATION - 2026-08-04

### Specified

- `2` declaracoes publicas congeladas na frente do runtime, probe
  `exit 0`, arvore intocada. `analyzeTransitionTable_reduce` e a reducao
  ja existente tornada **publica**; `analyzeTransitionTable_rawValid` e
  nova e devolve o **contrato inteiro**.

### Removes

- `3` auxiliares privados, tres copias da mesma reducao do bloco `do`:
  `Monovariants/WitnessBounds.lean`, `ComputabilityBridge/WitnessBound.lean`
  e `UniformPrimrec/Analysis.lean`. Os teoremas passam a **projetar do
  contrato**.

### Found

- A clausula `w.baseIndex < raw.next.size` **nunca fora exposta a
  consumidor nenhum**. Sai de graca com as outras, e mostra que a divida
  era maior que as duas parcelas ja cobradas.

### Preserved

- `analyzeTransitionTable_sound` fica **intacta**. Alargar nao e
  substituir. `0` assinaturas publicas quebradas, `0` mudancas de
  semantica.

### Locked

- `authorized_action: ENG_RUNTIME_SOUNDNESS_002_SPECIFICATION_REVIEW_AUTHORIZED`.
- `DEC-047` registrado no mesmo commit que faz sua edicao.

## PORTFOLIO-REVIEW-COST-MODEL - 2026-08-04

### Measured

- **O Mathlib TEM modelo de custo.** Probe `exit 0`:
  `Turing.TM2ComputableInTime` e `Turing.TM2ComputableInPolyTime`
  elaboram, junto com `FinTM2` e `TM2OutputsInTime`.
- Era um quase-Bochner: **nome nao procurado**, nao teoria ausente. A
  proibicao *nao declarar teoria ausente sem tentar elaborar* pegou o
  caso a tempo.

### And priced

- `TM2ComputableInPolyTime` e `Type 1` — **estrutura de dados que carrega
  uma maquina**, nao proposicao. Usa-la significa **construir um
  `FinTM2` para `analyzeTransitionTable`**.
- O unico exemplo trabalhado do Mathlib e `idComputableInPolyTime`: a
  **identidade**, e `noncomputable`.
- E mesmo instanciado, o produto seria uma **definicao de classe**, nao
  um ataque. Acumular pre-requisitos nao aproxima de um resultado.

### Selected

- `ENG-RUNTIME-SOUNDNESS-002`. Nao a mais ambiciosa — a unica **barata e
  devida**.
- `analyzeTransitionTable_sound` perde o contrato `Valid`, e a reducao do
  bloco `do` ja foi reproduzida **quatro vezes**, todas privadas, todas
  declaradas como divida: runtime (origem), monovariantes, ponte, e
  uniforme. Fecha `CB-GAP-004` e `UP-GAP-002`.
- Toca frente encerrada, e por isso **esta revisao autoriza o gate**, e
  nada alem da soundness.

### Unchanged

- Os `6` problemas em aberto seguem com o mesmo status. Nenhum ficou mais
  perto.

### Locked

- `authorized_action: ENG_RUNTIME_SOUNDNESS_002_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `DEC-046` registrado no mesmo commit que faz sua edicao.

## FOUND-UNIFORM-PRIMREC-001-RESULT-REVIEW - 2026-08-04

### Verified

- Build reexecutado: `exit 0`, `8811` jobs, `0` `error:`, `0` `sorry`.
  `36` declaracoes da arvore batendo com a especificacao congelada.
  `0` defeitos novos.

### Closed

- **`CB-GAP-001` FECHADA.** `Primrec₂ analyzeTransitionTable` esta na
  arvore. Era a unica lacuna da ponte com conteudo algoritmico.
- `FOUND-UNIFORM-PRIMREC-001` — **decima quarta** frente encerrada.

### Promoted

- `UNIFORM-ANALYSIS-PRIMREC-FORMAL-001`, nivel `F`. Ledger de `27` para
  `28`. **Dois** qualificadores obrigatorios, porque a claim erra nos
  dois sentidos: *primitivo recursivo NAO significa eficiente* e *sobre
  dominio infinito, e por isso NAO vacuo*.

### The distinction that matters

```text
ponte      Primrec nao mede nada    porque e VACUO sobre dominio finito
uniforme   Primrec nao mede custo   porque a CLASSE e enorme
```

Sao **dois limites diferentes**, e os dois valem. Fechar o nivel uniforme
**nao** aproximou o laboratorio de eficiencia.

### Still missing

- Para `PVSNP-PHYS-001` falta um **modelo de custo** — `UP-GAP-001`. E
  escolher um modelo e **decisao de portfolio, nao descoberta**.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`.
- `DEC-045` registrado no mesmo commit que faz sua edicao.

## FOUND-UNIFORM-PRIMREC-001-FORMALIZATION - 2026-08-04

### Formalized

- `6` modulos mais agregador e `2` arquivos de teste, `9` arquivos novos,
  `2` agregadores modificados. **`lake build` exit `0`, `8811` jobs,
  `0` `error:`, `0` `sorry`, `0` tokens proibidos.**
- `36` declaracoes derivadas **da arvore instalada** batem com a
  especificacao congelada: `31` publicas (`4` def, `27` teoremas),
  `1` privado, `1` TEST_ONLY, `3` testes.

### In the tree

- **`Primrec₂ analyzeTransitionTable`.** `CB-GAP-001` deixa de ser lacuna
  e passa a ser teorema compilado.
- `uniformPrimrecStatement_holds` fecha, por nome, o `def : Prop` que
  `FOUND-COMPUTABILITY-BRIDGE-001` registrou sem prova.

### Corrected

- Um **docstring** de `Analysis.lean` continha linha comecando por
  `theorem`, e o contador leu a propria documentacao como declaracao:
  `32` publicas em vez de `31`. Reescrito. Mesmo defeito ja registrado em
  `FOUND-CYCLE-DETECTION-001` — texto de declaracao dentro do arquivo
  Lean faz a auditoria encontrar a si mesma. Nenhuma assinatura mudou.

### Not claimed

- **`Primrec` continua nao significando eficiente.** A classe contem
  torres de exponenciais, e `0` cotas foram enunciadas.
- `0` modelos de custo, `0` classes de complexidade. **Nenhum problema de
  milenio atacado.**

### Locked

- `authorized_action: FOUND_UNIFORM_PRIMREC_001_RESULT_REVIEW_AUTHORIZED`.
- `DEC-044` registrado no mesmo commit que faz sua edicao.

## FOUND-UNIFORM-PRIMREC-001-SPECIFICATION-REVIEW - 2026-08-04

### Reviewed

- Probe reexecutado neste gate: `exit 0`, `0` linhas `error:`,
  `git_dirty=0`.

### Corrected

- **Universo preso sem motivo.** `primrec_run?_gen` e
  `flatMap_eq_foldr` estavam em `Type`; ambos sobem para `Type*` e o
  probe recompila. Nao era erro de prova — era generalidade jogada fora
  por descuido de assinatura. Hipoteses estritamente mais fracas, mesma
  conclusao, `31` publicas inalteradas.

### Confirmed

- O limite esta escrito nos tres documentos: **`Primrec` NAO significa
  eficiente**, a classe contem torres de exponenciais. A frente anterior
  precisou dizer que a classificacao nao mede nada por ser vacua; esta
  precisa dizer que, mesmo deixando de ser vacua, continua sem medir
  custo. Sao dois limites distintos, e os dois valem.

### Locked

- `authorized_action: FOUND_UNIFORM_PRIMREC_001_FORMALIZATION_AUTHORIZED`.
- `DEC-043` registrado no mesmo commit que faz sua edicao.

## FOUND-UNIFORM-PRIMREC-001-SPECIFICATION - 2026-08-04

### Specified

- `31` declaracoes publicas congeladas (`4` definicoes, `27` teoremas),
  `1` auxiliar privado, `1` TEST_ONLY, `3` testes, `36` no total,
  `6` modulos mais agregador. Probe `exit 0`, `0` linhas `error:`,
  arvore intocada.

### Proved

- **`Primrec₂ analyzeTransitionTable`.** O dominio
  `RawTransitionTable × Nat` e **infinito**, `Primrec.dom_finite` nao se
  aplica, e a prova **consulta o algoritmo**. Primeiro resultado de
  computabilidade do laboratorio com essa propriedade.
- `uniformPrimrecStatement_holds` fecha por nome o `def : Prop` que
  `FOUND-COMPUTABILITY-BRIDGE-001` deixou registrado sem prova.

### Discovered

- O obstaculo nunca foi computabilidade — era **tipo dependente**. A
  chave: `run?` **ja e nao dependente**, e a sua recursao com `Option`
  le-se como iterada, `run? k s = (fun o => o.bind step?)^[k] (some s)`.
  Dai `Primrec.nat_iterate` faz o trabalho.
- O tipo dependente restante vive em `detectCycle?` e sai por
  **casamento**, `valid_iff_rawValid`, apoiado na ponte
  `run?_eq_iterate_step` que a frente do runtime ja tinha. Nada e
  reimplementado.

### Declared

- `PrimrecPred` carrega instancia propria de `DecidablePred`. Construir
  `Primrec fun a => decide (p a)` por fora e entrega-lo onde se espera
  `PrimrecPred p` **falha**, e nenhuma tatica desfaz. Os predicados foram
  escritos com `if ... then true else false` e `Primrec.ite`.
  Registrado em `STOP-UP-005`.
- `analyze_reduce_u` e a **quarta** reproducao da reducao do bloco `do`.
  `UP-GAP-002`.

### Corrected

- `validBool_eq_decide` ficou **morta** quando a condicao passou a ser
  `validBool raw = true`. Removida antes do congelamento: `32` publicas
  viraram `31`.

### Not claimed

- **`Primrec` NAO significa eficiente** — a classe contem torres de
  exponenciais. `STOP-UP-002` existe so para isso.
- `0` modelos de custo, `0` classes de complexidade, `0` afirmacoes sobre
  P vs NP. **Nenhum problema de milenio atacado.**

### Locked

- `authorized_action: FOUND_UNIFORM_PRIMREC_001_SPECIFICATION_REVIEW_AUTHORIZED`.
- `DEC-042` registrado no mesmo commit que faz sua edicao.

## PORTFOLIO-REVIEW-UNIFORM - 2026-08-04

### Counted

- `22` itens na fila: `15` VERIFIED, `1` FROZEN (`RH-NOGO-001`), `6`
  SCOPED. As **16 linhas proprias** do laboratorio estao fechadas. Os `6`
  SCOPED nao sao linhas do laboratorio — sao os problemas que ele
  gostaria de atacar.

### Selected

- `FOUND-UNIFORM-PRIMREC-001`. Das `10` lacunas abertas pela ponte, e a
  **unica** cuja resolucao produz informacao algoritmica.

### Measured

- Viabilidade por **elaboracao**, probe descartavel `exit 0`, arvore
  intocada. Compilaram: `primrec_stepList`, `primrec_runList` e
  `primrec_validList`. O segundo e o coracao — **iterar a tabela
  codificada e primitivo recursivo**, via `Primrec.nat_iterate`.
- O obstaculo real e **tipo dependente**, nao computabilidade:
  `analyzeTransitionTable` atravessa `Fin t.next.size`. A rota medida e
  reformular sobre `List Nat` e casar depois — e o casamento e o volume
  da frente.

### Corrected

- `LAB_STATE.md` carregava `specification_status: READY_FOR_REVIEW`
  enquanto o `STATUS.yaml` da frente dizia `APPROVED` — divergencia entre
  as duas fontes que **sobreviveu a dois gates**, o de formalizacao e o
  de resultado. `labctl validate` nao a pega: ele confere `work_status`
  contra a fila, nao `specification_status` contra a frente. Corrigida na
  transicao de frente, e o furo de validacao fica registrado como
  observacao.

### Measured again, harder

- Segundo probe, `exit 0`, arvore intocada, direto sobre a funcao do
  laboratorio em vez de uma reformulacao:
  **`Primrec (fun p => p.1.1.run? p.1.2 p.2)` compila.**
- `RawTransitionTable.run?` e primitiva recursiva sobre um dominio
  **infinito**. A prova passa por `Primrec.nat_iterate` e **depende do
  que a funcao faz** — e o primeiro resultado de computabilidade do
  laboratorio que consulta o algoritmo.
- O que o tornou barato: `run?` **ja e nao dependente**, e a recursao le-se
  como iterada em `Option Nat`, `run? k s = (fun o => o.bind step?)^[k]
  (some s)`. O obstaculo de tipo dependente vive em `detectCycle?`, nao
  na execucao.

### Not claimed

- Nenhum dos `6` problemas em aberto ficou mais perto. Para
  `PVSNP-PHYS-001` faltam, em ordem: o nivel uniforme, um modelo de
  custo, e reavaliacao — e **o modelo de custo e escolha, nao
  descoberta**.
- Os outros cinco seguem com primeiro passo bibliografico e custo
  `very_high` declarado desde 2026-07-31.

### Locked

- `authorized_action: FOUND_UNIFORM_PRIMREC_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `DEC-041` registrado no mesmo commit que faz sua edicao.

## FOUND-COMPUTABILITY-BRIDGE-001-RESULT-REVIEW - 2026-08-04

### Verified

- Build reexecutado: `exit 0`, `8802` jobs, `0` `error:`, `0` `sorry`.
- Confronto **nome a nome** entre arvore instalada e especificacao
  congelada: `28` assinaturas presentes, `0` ausentes, `0` duplicadas,
  `0` divergentes. A 29a declaracao e o auxiliar privado.
- Pegada `9` livres de axioma e `19` com pegada infraestrutural,
  identica a prevista.

### Corrected

- `RES-REV-CB-001`: a assinatura do auxiliar privado estava so em prosa,
  e o comparador automatico a leu como "instalada a mais". Defeito **do
  comparador**, nao do resultado. A assinatura foi posta em bloco.

### Promoted

- `COMPUTABILITY-CLASSIFICATION-VACUITY-FORMAL-001`, nivel `F`. Ledger
  passa de `26` para `27`. Tres qualificadores sao **obrigatorios** em
  toda formulacao: *por finitude do dominio*, *sem conteudo algoritmico*
  e *cota do certificado, nao de recursos*. Sem eles a afirmacao induz a
  erro.

### Closed

- `FOUND-COMPUTABILITY-BRIDGE-001` — **decima terceira** frente
  encerrada. `19` declaracoes publicas, `29` no total, `10` lacunas
  abertas, `13` condicoes de parada, `0` disparadas, `6` defeitos achados
  pelas revisoes.

### Still open

- `CB-GAP-001` e a unica lacuna desta frente com conteudo algoritmico: o
  nivel **uniforme**, sobre `RawTransitionTable × Nat`, onde o dominio e
  infinito e `dom_finite` nao se aplica. O enunciado elabora; a prova
  **nao foi tentada**.
- `CB-GAP-002` — sem modelo de custo nao ha complexidade. Fecha-la e
  escolher um modelo, e escolher e decisao de portfolio.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`.
- `DEC-040` registrado no mesmo commit que faz sua edicao.

## FOUND-COMPUTABILITY-BRIDGE-001-FORMALIZATION - 2026-08-04

### Formalized

- `5` modulos mais agregador e `2` arquivos de teste, `8` arquivos novos,
  `2` agregadores modificados. **`lake build` exit `0`, `8802` jobs,
  `0` linhas `error:`, `0` `sorry`, `0` tokens proibidos.**
- `29` declaracoes derivadas **da arvore instalada** batem termo a termo
  com a especificacao congelada: `19` publicas (`7` def, `4` instance,
  `8` teoremas), `1` auxiliar privado, `2` TEST_ONLY, `7` testes.

### Measured

- Pegada axiomatica: `9` declaracoes livres de axioma, `19` com
  `propext, Classical.choice, Quot.sound`. Identica a do probe.
- O unico `warning:` do build e **anterior a esta frente**, em
  `RHNogo/AsymptoticCore/Incompatibility.lean:49`. Esta frente produz
  `0`.

### Corrected

- A palavra `sorry` aparecia numa **docstring** de `Classification.lean`,
  e a varredura de tokens proibidos encontrou a propria documentacao.
  Movida para `STOP_CONDITIONS.md`, seguindo o precedente ja registrado
  em `FOUND-CYCLE-DETECTION-001`. Correcao de documentacao: nenhuma
  assinatura mudou.

### Established

- Primeira vez que o laboratorio importa `Mathlib.Computability`. A ponte
  esta na arvore: `Mathlib.Computability.Primrec.List` e
  `Mathlib.Computability.Halting`.
- E o enunciado negativo sobreviveu a formalizacao:
  `primrec_analyzeEncodedSystem` tem corpo de **uma linha**,
  `primrec_of_encoding e _`, e este tem corpo `Primrec.dom_finite f`.

### Not done

- `0` claims promovidas, `26` no ledger — a promocao e do gate de
  revisao de resultado.
- `0` classes de complexidade, `0` afirmacoes de custo. O nivel uniforme
  segue **enunciado e nao provado**.
- **Nenhum problema de milenio atacado.**

### Locked

- `authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_RESULT_REVIEW_AUTHORIZED`.
- `DEC-039` registrado no mesmo commit que faz sua edicao.

## FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION-REVIEW - 2026-08-04

### Reviewed

- Probe reexecutado neste gate: `exit 0`, `0` linhas `error:`, `0`
  `warning:`, `git_dirty=0`, `29` declaracoes derivadas por script,
  pegada medida `29/29`.
- `5` defeitos encontrados, `5` corrigidos, `0` assinaturas alteradas.

### Corrected

- **Afirmacao de primazia FALSA.** A especificacao dizia ser "a primeira
  frente com `instance_declarations != 0`". Derivado por script: a
  biblioteca ja tinha **`22`** instancias em **`6`** arquivos. Terceiro
  defeito de contagem agregada em tres frentes consecutivas, e o primeiro
  que nao e aritmetico — era uma contagem disfarcada de adjetivo.
- `typeclasses_required_of_consumer: 0` era impreciso: o caminho
  principal exige `0`, mas `primrec_of_encoding` exige `[Primcodable σ]`
  do chamador. Separado em dois campos.
- **Teste que nao testava.** `boolEncoding_bound_concrete` enunciava
  `0 + 2 ≤ 2`, decidivel por avaliacao, e passaria com o teorema da cota
  removido do arquivo. Substituido por `boolEncoding_bound_applies`,
  quantificado sobre `w`.

- **Chave YAML duplicada**, pega por `labctl validate` dentro do proprio
  gate: `specification_review` aparecia como campo de status e como bloco
  em `STATUS.yaml`. Renomeado para `specification_review_record`. A regra
  `yaml_duplicate_keys` cobrou, e o defeito morreu antes do commit.

### Declared open

- **A `Primcodable` induzida NAO e canonica.** `Primcodable Bool` ja
  existe no Mathlib e e diferente de `encodingPrimcodable boolEncoding`.
  Omissao da especificacao, corrigida com `CB-GAP-010`, `STOP-CB-013` e
  um teste novo: `boolEncoding_primrec_canonical` mostra que sob a
  instancia canonica a conclusao e a mesma, pela mesma linha — **porque
  quem faz o trabalho e a finitude, nao a codificacao**.
- `10` lacunas, `13` condicoes de parada.

### Frozen

- As `19` assinaturas publicas **nao mudaram**. Os quatro defeitos
  atingiram documentacao, um teste e uma lacuna omitida.

### Locked

- `authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_FORMALIZATION_AUTHORIZED`.
- `DEC-038` registrado no mesmo commit que faz sua edicao.

## FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION - 2026-08-04

### Specified

- Cinco documentos, `19` declaracoes publicas congeladas (`7` definicoes,
  `4` instancias, `8` teoremas), `1` auxiliar privado, `2` TEST_ONLY,
  `6` testes, `28` declaracoes ao todo, `5` modulos Lean planejados mais
  `1` agregador. Todas compilaram em probe, `exit 0`, `0` avisos.

### Frozen

- A ponte e uma linha: `Primcodable.ofEquiv (Fin n) (encodingEquiv e)`.
  `CertifiedFiniteEncoding` tem exatamente os quatro campos de uma
  equivalencia, e **e** um `S ≃ Fin n`.
- **O resultado central e NEGATIVO.** `primrec_of_encoding` prova que
  toda funcao que sai de um tipo com codificacao certificada e primitiva
  recursiva, e seu corpo — `Primrec.dom_finite` — nunca consulta a
  funcao. A classificacao `Primrec`/`Computable` e **constante** sobre o
  dominio finito do laboratorio.
- Logo: "o detector e `Primrec`" e verdadeiro, e **nao** porque a busca e
  limitada. A classificacao nao distingue o detector de uma tabela de
  consulta, e nao serve de degrau para classe de complexidade nenhuma.

### Answered

- As cinco perguntas de `ATTACK_READINESS.md`: `SIM` por construcao para
  `Primcodable`; `SIM` por **finitude** para `Computable`, `Primrec` e
  `ComputablePred`; `NAO` para cota de recursos — `baseIndex + period ≤ n`
  limita o **certificado**, nao o custo; `NAO` para custo sem modelo de
  maquina neste nivel.

### Declared

- `analyze_reduce_cb` e a **terceira** ocorrencia da mesma reducao do
  bloco `do` — original privada no runtime, segunda em
  `Monovariants/WitnessBounds.lean`. Declarada, nao escondida. A correcao
  propria alarga `analyzeTransitionTable_sound` e exige gate sobre frente
  encerrada: `CB-GAP-004`.
- `4` declaracoes `instance`. Primeira frente com
  `instance_declarations ≠ 0`, e a contagem esta publicada.

### Declared open

- `9` lacunas. `CB-GAP-001` e a unica com conteudo algoritmico: no nivel
  uniforme, sobre `RawTransitionTable × Nat`, o dominio e infinito e
  `dom_finite` nao se aplica. `UniformPrimrecStatement : Prop` existe
  para provar que o enunciado **elabora**; a prova nao foi tentada.
- Escolhido `def : Prop` em vez de `sorry` ou axioma local — o enunciado
  fica verificadamente escrevivel sem que nada seja afirmado.

### Corrected

- A varredura de pegada axiomatica cobria `20` de `28` declaracoes e
  seria publicada como integral. Refeita para `28`, cobertura `FULL`, e
  a regra `axiom_scan_scope` foi acrescentada a governanca.
- A prosa de `Estado atual` em `LAB_STATE.md` voltou a dizer "Nenhuma
  frente ativa" enquanto tres frentes eram abertas e duas encerradas —
  **reincidencia** do defeito que o proprio bloco documenta. Corrigida, e
  a reincidencia esta registrada em vez de apagada.

### Observed

- `AGENTS.md` passo 7 exige relatorio em `09_SESSIONS/`. O ultimo
  existente era `2026-08-03_2210`: oito gates passaram sem um. Registrado
  como observacao; **nada e reescrito retroativamente**.

### Not done

- `0` arquivos Lean permanentes, `0` `lake build`, `0` claims, `26` no
  ledger, `0` frentes encerradas tocadas, `0` classes de complexidade.
- **Nenhum problema de milenio atacado.**

### Locked

- `authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_REVIEW_AUTHORIZED`.
- `DEC-037` registrado no mesmo commit que faz sua edicao.

## ATTACK-READINESS - 2026-08-04

### Measured, not read

- A prontidao foi medida por **elaboracao**, nao por leitura de
  documentos: um probe que tenta `#check` nos objetos de que cada
  problema precisa.

```text
riemannZeta, riemannZeta_one_sub, completedRiemannZeta   ELABORAM
InnerProductSpace, MeasureTheory.Measure, fderiv         ELABORAM
Turing.TM2.Stmt, Nat.Partrec, Nat.Partrec.Code           ELABORAM
ComputablePred                                            ELABORA
```

- Correcao de metodo registrada: `MeasureTheory.Integral.Bochner` **nao
  tem `.olean`** porque o modulo foi dividido em versoes recentes. Isso e
  **nome obsoleto, nao lacuna de teoria** — e so se descobre elaborando.

### Found

- **As duas metades nunca se tocaram.** O laboratorio prova coisas sobre
  sistemas finitos **executaveis e certificados**; o Mathlib tem
  `ComputablePred` e `Nat.Partrec`; e **nenhum arquivo sob `TamesisLab/`
  menciona `Computable`, `Partrec` ou `Turing`**.

### Verdict, unflattering

- **O laboratorio NAO esta pronto para atacar nenhum dos seis.** Cinco
  exigem analise, EDP, geometria algebrica ou aritmetica de curvas, e a
  arvore propria tem **zero** disso: o primeiro passo neles e
  bibliografico, com custo `very_high` declarado desde 2026-07-31.
- `riemannZeta` elaborar **nao** e prontidao para RH: a lacuna congelada
  e `GLOBAL-WEYL-BRIDGE-SCALAR`, que exige calculo pseudodiferencial.
  **Ter o objeto nao e ter a teoria.**

### The five checkable questions

1. `analyzeEncodedSystem` e `ComputablePred`-compativel?
2. `CertifiedFiniteEncoding S n` induz `Primcodable S`?
3. O detector, sendo busca limitada, e `Primrec` e nao so `Computable`?
4. A cota `baseIndex + period <= n` da limite de RECURSOS?
5. Existe nocao de custo formalizavel sem comprometer-se com um modelo?

Nenhuma e programa de pesquisa. Todas tem resposta verificavel em Lean, e
**nenhuma foi respondida**.

### Selected

- **`FOUND-COMPUTABILITY-BRIDGE-001`**, o unico caminho em que as doze
  frentes encerradas transferem para um problema em aberto. **Nao e
  ataque**: e pre-requisito, e o caminho mais curto custa no minimo esta
  ponte mais uma frente de recursos, e entao **reavaliacao**.

### Locked

- `authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `DEC-036` registrado no mesmo commit que faz suas edicoes.

## LAB-CORR-MONOVARIANT-VACUITY-001 - 2026-08-04

### Recorded as a theorem, not as errata

- **`Monovariant measure stepC` implica `IsEmpty C`**, e a prova **nao
  depende de axioma nenhum**. Vive em
  `Foundations/Descent/Vacuity.lean`, que **consome** a definicao
  publicada sem modificar nenhum arquivo da frente encerrada.

### Corrected

- **`DescendsOn`**: a medida decresce **enquanto** `P` vale — que e o que
  o argumento classico sempre exigiu.
- **`DescendsOn.exits`**: a partir de qualquer estado, o sistema sai da
  regiao `P` em numero finito de passos. A conclusao certa e
  **terminacao**, nao ausencia de recorrencia.
- **A instancia positiva que faltava**: `strictDown`, o mesmo que a
  frente encerrada registrou como *falha*, **funciona** na forma
  corrigida. Era sintoma, nao limite.

### Claim

- `MONOVARIANT-REFLECTION-LIMIT-FORMAL-001` **nao foi removida**. O
  wording anterior fica preservado e um bloco `correction` declara
  `applicability: VACUOUS_ON_INHABITED_TYPES` e
  `superseded_by: DescendsOn`. Apagar a claim apagaria a evidencia do
  defeito.

### New permanent rule

- `positive_instance_required`: **toda frente que introduz uma hipotese
  deve exibir instancia positiva em tipo habitado, ou declarar que a
  hipotese e vacua.**
- Contagem derivada, pegada medida e tokens varridos verificam **forma**.
  Satisfazibilidade e **conteudo**, e cinco gates passaram sem verifica-la.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `lake build` exit `0`,
  `8794` jobs. `0` arquivos Lean de frente encerrada modificados,
  `0` entradas historicas reescritas.

## PORTFOLIO-REVIEW-VACUITY-CORRECTION - 2026-08-04

### Found, and it is critical

- **A definicao `Monovariant`, encerrada em `a8929d7`, e VACUA.**

```text
Monovariant measure stepC  ->  IsEmpty C
```

  Provado **sem depender de axioma nenhum**. Se `C` e habitado, a imagem
  de `measure` em `Nat` tem minimo, e a hipotese exige um valor menor que
  ele dentro da propria imagem.

- Todos os teoremas daquela frente sao **verdadeiros**; nenhum e
  **aplicavel** a tipo habitado. A claim
  `MONOVARIANT-REFLECTION-LIMIT-FORMAL-001` foi promovida sobre hipotese
  que nada satisfaz.

### Why five gates missed it

```text
contagem derivada     conferida
pegada axiomatica     medida
tokens proibidos      varridos
typeclasses           contadas
SATISFAZIBILIDADE     NAO VERIFICADA
```

- A instancia `strictDown` **falhou** em ser monovariante, e isso foi
  registrado como "limite honesto da ferramenta" quando era o **sintoma**.
  Nenhuma instancia positiva foi exigida em gate nenhum.

### Selected

- **`LAB-CORR-MONOVARIANT-VACUITY-001`**. A alternativa que estava
  selecionada — combinar invariante com monovariante — foi **abandonada**:
  combinar uma peca vacua com outra produziria duas pecas vacuas.

### New permanent rule

- **Toda frente que introduz uma hipotese deve exibir uma instancia
  positiva que a satisfaca, num tipo habitado, ou declarar explicitamente
  que a hipotese e vacua.**

### Locked

- `authorized_action: LAB_CORR_MONOVARIANT_VACUITY_CORRECTION_AUTHORIZED`.
- `DEC-035` registrado no mesmo commit que faz sua edicao.

## FOUND-MONOVARIANT-DESCENT-001-RESULT-REVIEW - 2026-08-04

### Approved

- `FOUND_MONOVARIANT_DESCENT_001_RESULT_REVIEW_APPROVED`, com build e
  contagens **reexecutados** neste gate.

### Promoted

- **`MONOVARIANT-REFLECTION-LIMIT-FORMAL-001`**, `evidence_level: F`,
  novidade `NONE`. Ledger de `25` para `26`.
- `scope_qualifier_required` com **tres** qualificadores: "medida em
  `Nat`", "suficiente, nunca necessaria" e **"decrescimo ESTRITO"**. Sem
  os tres a afirmacao e falsa.

### Closed

- O **par classico esta completo**:

```text
invariante     quantidade conservada   -> impossibilidade
monovariante   quantidade decrescente  -> ausencia de recorrencia
```

- E os dois medem o mesmo limite de angulos opostos: com invariante a
  reflexao vale nos pontos fixos, com monovariante **nao vale em lugar
  nenhum**.

### Recovered, and it stays

- `0 < period` esta de volta na superficie publica, recuperada **sem
  tocar em frente encerrada**.

### Recorded

- **Dois defeitos nesta frente**, ambos registrados sem atenuacao: a
  contagem agregada errada, pega pela propria revisao, **segundo do mesmo
  tipo em duas frentes consecutivas**; e `lt_irrefl` nao resolvendo com o
  import minimo, corrigido em tatica sem mudar assinatura.

### Not done

- **Nenhum problema de milenio atacado.** `RH-NOGO-001` permanece
  `NOT_AUTHORIZED` / `NO_EXECUTION`.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `0` frentes encerradas
  modificadas.

## FOUND-MONOVARIANT-DESCENT-001-FORMALIZATION - 2026-08-04

### Formalized

- Quatro modulos permanentes, dois agregadores tocados so em imports,
  dois arquivos de teste. `lake build` **exit 0**, `8789` jobs, `0`
  linhas de erro reais.
- `7` publicas (`1` definicao, `6` teoremas), `1` auxiliar privado, `2`
  TEST_ONLY — **derivadas por script ANTES de escrever qualquer total**,
  que e a proibicao criada dois gates atras e violada um gate atras.
- `0` `Fintype`, `0` `DecidableEq`, `0` instancias, `0` tokens proibidos.

### Recovered

- **`0 < period` esta de volta na superficie publica.**
  `analyzeTransitionTable_period_pos` e
  `analyzeAbstractSystem_period_pos` recuperam a clausula que se perdia
  entre `detectCycle?_sound` e `analyzeTransitionTable_sound`, sem tocar
  em **nenhum** arquivo de frente encerrada.

### Corrected

- `lt_irrefl` nao resolve com o import minimo de `Definitions.lean`, onde
  so entra `Mathlib.Logic.Function.Iterate`. Trocado por
  `Nat.lt_irrefl`, do core. **Correcao de tatica: nenhuma assinatura
  congelada mudou.**

### Footprint

```text
Monovariant.iterate_lt            propext, Quot.sound
Monovariant.no_periodic_point     propext, Quot.sound
Monovariant.not_reachable_self    propext, Quot.sound
analyzeAbstractSystem_period_pos  propext, Classical.choice, Quot.sound
monovariant_not_orbitSeparating   propext, Classical.choice, Quot.sound
strictDown_not_monovariant        propext
```

`Classical.choice` entra **apenas** no que atravessa
`analyzeEncodedSystem`. A parte de descida pura nao o carrega.

### Locked

- `authorized_action: FOUND_MONOVARIANT_DESCENT_001_RESULT_REVIEW_AUTHORIZED`.
  `0` claims, `25` no ledger, `0` frentes encerradas tocadas.

## FOUND-MONOVARIANT-DESCENT-001-SPECIFICATION-REVIEW - 2026-08-04

### Approved

- `FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_REVIEW_APPROVED`. Sete
  itens: **seis confirmados, um corrigido**.

### Caught, and it is the second in a row

```text
derivado por script   12
declarado             13
soma das partes       12
```

- A decomposicao estava **correta**. O total e que estava errado, e o
  campo `extra_negation_registrations: 1` era **espurio**, inventado para
  a conta fechar.
- **Segundo defeito de contagem agregada em duas frentes consecutivas.**
  A proibicao gravada no gate anterior foi violada por mim no gate
  seguinte ao que a criou. Registrado como tal, sem atenuacao.

### Confirmed

- `0 < period` **e** recuperavel da API publica, e a recuperacao **nao
  toca frente encerrada**.
- `strictDown_not_monovariant` compila: `Nat` e bem fundado e ainda assim
  `k - 1` **nao** e monovariante, porque falha em zero.

### Locked

- `authorized_action: FOUND_MONOVARIANT_DESCENT_001_FORMALIZATION_AUTHORIZED`.
  `0` Lean permanentes, `0` claims, `25` no ledger.

## FOUND-MONOVARIANT-DESCENT-001-SPECIFICATION - 2026-08-04

### Specified

- Cinco documentos, `7` declaracoes publicas congeladas (`1` definicao,
  `6` teoremas), `1` auxiliar privado, `2` TEST_ONLY, `2` testes,
  `4` modulos Lean planejados. Todas ja compilaram em probe, `exit 0`.

### Frozen

- A medida vive em **`Nat`, e so em `Nat`**. Boa fundacao vem de graca,
  `0` typeclasses sao exigidas. Ordens gerais, `WellFoundedRelation` e
  ordinais ficam **NAO AUTORIZADOS**.
- `monovariant_not_orbitSeparating` e a declaracao central, e **nao tem
  hipotese que o consumidor precise inventar**.

### Declared

- O auxiliar `reduce'` e **privado** e reproduz, com API exclusivamente
  publica, uma reducao que a frente encerrada mantem privada. A linha
  esta escrita: **reproduzir uma reducao curta a partir de API publica e
  permitido; reimplementar o detector nao e.** A duplicacao esta
  declarada, nao escondida.

### Declared open

- `8` lacunas. `MON-GAP-001`, a necessidade, e a honesta: para `C`
  finito a reciproca e trivial, para `C` infinito **nao e obvia**, e a
  frente nao trata.
- `MON-GAP-007` fica aberta **de proposito**: descida estrita sobre `Nat`
  implica cota no numero de passos, mas enuncia-la seria afirmacao
  quantitativa, e afirmacao de custo sem modelo esta proibida.

### Not done

- `0` arquivos Lean permanentes, `0` `lake build`, `0` claims, `25` no
  ledger, `0` frentes encerradas tocadas.
- **Nenhum problema de milenio atacado.**

### Locked

- `authorized_action: FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_REVIEW_AUTHORIZED`.
- `DEC-032` registrado no mesmo commit que faz sua edicao.

## PORTFOLIO-REVIEW-MONOVARIANT - 2026-08-04

### Selected

- **`FOUND-MONOVARIANT-DESCENT-001`**, a segunda metade do par classico.
  Quatro alternativas comparadas, criterio de **transferencia**.

### Probed

- `10` declaracoes, `exit 0`, arvore intocada.
- **O negativo e mais forte que o da frente anterior**:

```text
invariante     OrbitSeparating vale EXATAMENTE nos pontos fixos
monovariante   OrbitSeparating NAO VALE EM LUGAR NENHUM
```

  Um monovariante exclui recorrencia concreta em qualquer numero positivo
  de passos, enquanto a analise abstrata **sempre** devolve ciclo com
  periodo positivo. Logo **todo ciclo abstrato de sistema monovariante e
  espurio**.

### Recovered

- `detectCycle?_sound` prova `0 < period`, mas
  `analyzeTransitionTable_sound` devolve tres clausulas e **a
  positividade se perde**. O probe recupera, re-derivando a reducao em
  namespace novo com API so publica, **sem tocar em frente encerrada**.
- E o que torna o negativo **livre de hipotese inventada**.

### Registered

- Duas negacoes impedem a leitura da ferramenta como universal.
  `strictDown_not_monovariant` e a que importa: `Nat` e bem fundado e
  ainda assim `k - 1` **nao** e monovariante, porque falha em zero. **Boa
  fundacao do contradominio nao substitui decrescimo estrito.**

### Not done

- **Nenhum problema de milenio atacado.** `0` arquivos Lean permanentes,
  `0` claims, `25` no ledger.

### Locked

- `authorized_action: FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `DEC-031` registrado no mesmo commit que faz suas tres edicoes.

## FOUND-INVARIANT-UNREACHABILITY-001-RESULT-REVIEW - 2026-08-04

### Approved

- `FOUND_INVARIANT_UNREACHABILITY_001_RESULT_REVIEW_APPROVED`. Nove itens
  CONFIRMADOS, com build e contagens **reexecutados** neste gate.

### Promoted

- **`INVARIANT-UNREACHABILITY-FORMAL-001`**, `evidence_level: F`,
  novidade `NONE`. Ledger de `24` para `25`.
- A entrada carrega `scope_qualifier_required` com dois qualificadores:
  **"suficiente, nunca necessaria"** e **"sistemas deterministicos
  totais"**. Sem os dois a afirmacao e falsa ou vazia.

### Footprint

- **`Classical.choice` ausente das dez declaracoes.** Tres delas —
  `Invariant.semiconj`, `invariantAbstraction` e
  `constant_invariant_proves_nothing` — **nao dependem de axioma nenhum**.
- Que `Invariant.semiconj` nao tenha pegada e a verificacao de que a
  ponte com `Function.Semiconj` e **definicional**, nao uma prova
  disfarcada.

### Closed

- Frente **ENCERRADA**. Invariantes relacionais, monovariantes,
  terminacao, invariante completo e sistemas nao deterministicos seguem
  **NAO AUTORIZADOS**.
- `INV-GAP-001` fica **aberta**: a reciproca ingenua e vacuamente
  verdadeira pelo invariante mais fino, e a pergunta com conteudo —
  existe invariante separador *calculavel* — nao foi atacada.

### Not done

- **Nenhum problema de milenio foi atacado**, por decisao explicita: a
  estrategia e acumular ferramentas antes de abrir tabuleiro.
  `RH-NOGO-001` permanece `NOT_AUTHORIZED` / `NO_EXECUTION`.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `0` frentes encerradas
  modificadas.

## FOUND-INVARIANT-UNREACHABILITY-001-FORMALIZATION - 2026-08-04

### Formalized

- Quatro modulos Lean permanentes, dois agregadores tocados so em
  imports, dois arquivos de teste. `lake build` **exit 0**, `8782` jobs,
  `0` linhas de erro reais.
- `8` declaracoes publicas e `2` TEST_ONLY, **derivadas por script** e
  batendo com o congelado. `0` `Fintype`, `0` `DecidableEq`, `0`
  instancias, `0` tokens proibidos.

### Footprint

- **`Classical.choice` nao aparece em nenhuma declaracao da frente**, como
  a especificacao previu: nada aqui atravessa `analyzeEncodedSystem`, nao
  ha `Array`, tabela nem execucao.

```text
Invariant.semiconj                        sem pegada
Invariant.iterate                         propext
unreachable_of_invariant_ne               propext
Invariant.pair                            propext
invariantAbstraction                      sem pegada
invariant_orbitSeparating_iff_fixedPoint  propext, Quot.sound
diagStep_invariant                        propext, Quot.sound
diag_unreachable                          propext, Quot.sound
```

### Result

- **A ferramenta morde.** `diag_unreachable` prova que `(1, 0)` nao e
  alcancavel a partir de `(0, 0)` sob `diagStep`, sobre `Int x Int`,
  **infinito**, sem enumeracao e sem finitude.
- **O limite esta escrito em Lean.**
  `invariant_orbitSeparating_iff_fixedPoint` mostra que, para abstracoes
  invariantes, a condicao de reflexao vale **exatamente nos pontos
  fixos**. Invariantes certificam impossibilidade e nunca recorrencia.

### Locked

- `authorized_action: FOUND_INVARIANT_UNREACHABILITY_001_RESULT_REVIEW_AUTHORIZED`.
  `0` claims promovidas, `24` no ledger, `0` frentes encerradas tocadas.

## FOUND-INVARIANT-UNREACHABILITY-001-SPECIFICATION-REVIEW - 2026-08-04

### Approved

- `FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_REVIEW_APPROVED`.
  Oito itens: **sete confirmados, um corrigido**.

### Re-executed

- O probe foi **rodado de novo neste gate**, nada herdado: `exit 0`,
  `0` erros, arvore intocada, `0` ocorrencias de `Fintype`, `0` de
  `DecidableEq`, `0` instancias.
- Pegada medida agora, e bate com a esperada. `Classical.choice` **nao**
  aparece.

### Caught

- **A contagem derivada por script deu `12`; a especificacao declarava
  `10`.** A classificacao estava correta — `8` publicas, `2` TEST_ONLY,
  `2` testes — mas o campo `probe.declarations_compiled` **omitiu os dois
  testes**.
- E exatamente a contagem agregada escrita a mao que o `LAB_STATE.md`
  proibe. A regra existia; nao foi aplicada ao proprio campo.
- Corrigido **contra a derivacao**, com a decomposicao explicita. A
  classificacao **nao** foi alterada para caber no numero.
- Documentos historicos **nao foram reescritos**. Quem ler `10` neles
  resolve por `SPECIFICATION_REVIEW.md`. Mesmo principio da colisao de
  `DEC-014`.

### Confirmed

- `Invariant.semiconj` e literalmente o termo `h`, verificado por
  **extracao do corpo do teorema**, nao por leitura. `Invariant` e
  `Function.Semiconj abstract stepC id` sao a mesma proposicao.
- O teorema negativo exige **uma** hipotese e um ponto inicial. Nada
  mais entra: nem finitude, nem decidibilidade, nem hipotese sobre a
  orbita.

### Locked

- `authorized_action: FOUND_INVARIANT_UNREACHABILITY_001_FORMALIZATION_AUTHORIZED`.
  `0` arquivos Lean permanentes, `0` claims, `24` no ledger, `0` frentes
  encerradas tocadas.
- Nova proibicao: **nao escrever contagem agregada sem deriva-la por
  script no mesmo gate**.

## FOUND-INVARIANT-UNREACHABILITY-001-SPECIFICATION - 2026-08-04

### Specified

- Cinco documentos, `8` declaracoes publicas congeladas, `2` TEST_ONLY
  residentes na biblioteca, `4` modulos Lean planejados.
- **Todas as assinaturas ja compilaram em probe**, `exit 0`. Congela-las
  nao e aposta.

### Frozen

- `Invariant` e definicionalmente `Function.Semiconj abstract stepC id`.
  `Invariant.semiconj` e o proprio termo `h` — sem `Iff`, sem transporte,
  sem conversao. A ponte esta **exposta** porque e o conteudo da frente.
- `invariant_orbitSeparating_iff_fixedPoint` e a declaracao central: para
  abstracoes invariantes, a condicao de reflexao vale **exatamente nos
  pontos fixos**.

### Bounded

- `0` typeclasses no nucleo. `Fintype` e `DecidableEq` **nao** aparecem
  em declaracao nenhuma. A instancia usa `Int x Int`, **infinito nas duas
  coordenadas**, escolha deliberada para que ninguem leia a ferramenta
  como dependente de finitude.
- `Classical.choice` nao e esperado: a frente nao atravessa
  `analyzeEncodedSystem`, nao ha `Array`, tabela nem execucao.

### Declared open

- `10` lacunas abertas. `INV-GAP-001`, a completude, e a honesta: a
  reciproca e **vacuamente verdadeira** pelo invariante mais fino, e
  portanto nao diz nada. A pergunta com conteudo — existe invariante
  separador *calculavel* ou de forma restrita — fica **aberta**.
- `INV-GAP-009`, a bibliografia de argumentos de invariante em
  combinatoria, fica **deliberadamente aberta**.

### Not done

- `0` arquivos Lean permanentes, `0` `lake build`, `0` claims promovidas,
  `24` no ledger, `0` frentes encerradas tocadas.
- **Nenhum problema de milenio atacado.**

### Locked

- `authorized_action: FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_REVIEW_AUTHORIZED`.
- `DEC-028` registrado no mesmo commit que faz sua edicao.

## PORTFOLIO-REVIEW-INVARIANT-TOOLKIT - 2026-08-04

### Criterion

- A escolha passou a ser por **transferencia**, nao por impacto local:
  qual peca se encaixa em tabuleiros ainda nao abertos. Uma frente que so
  serve a cadeia que a gerou nao vale a jogada.

### Found

- **Dez frentes encerradas usam abstracao para COLAPSAR. Zero usam para
  SEPARAR** — embora separar seja o mecanismo de toda prova de
  impossibilidade combinatoria: paridade, coloracao, monovariante.
- A peca e quase gratuita: **um invariante E uma semiconjugacao com
  `stepA = id`**, por igualdade definicional. `Invariant.semiconj` e o
  proprio termo, sem conversao.

### Selected

- **`FOUND-INVARIANT-UNREACHABILITY-001`**. Cinco alternativas
  comparadas. A finitude da orbita concreta perdeu por pouco: teorema
  mais forte, mas transfere so para dentro da propria cadeia.

### Probed

- `10` declaracoes compiladas, `exit 0`, arvore versionada intocada.
- `unreachable_of_invariant_ne`, a ferramenta, com pegada `[propext]`.
- `diag_unreachable` prova impossibilidade sobre `Int x Int`, **infinito**,
  sem usar finitude em lugar nenhum.
- **O negativo afiado ja compilou**:
  `invariant_orbitSeparating_iff_fixedPoint`. Para abstracoes
  invariantes, a condicao de reflexao vale **exatamente nos pontos
  fixos**. Invariantes certificam impossibilidade e **nunca**
  recorrencia; os dois usos da mesma maquina sao incompativeis.

### Not done

- **Nenhum problema de milenio foi atacado.** A frente constroi uma peca.
  `RH-NOGO-001` permanece `NOT_AUTHORIZED` / `NO_EXECUTION`.
- `0` arquivos Lean permanentes, `0` claims promovidas, `24` no ledger.

### Locked

- `authorized_action: FOUND_INVARIANT_UNREACHABILITY_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `DEC-026` e `DEC-027` registrados **no mesmo commit** que faz suas
  edicoes. `DEC-027` carrega a pre-condicao **dupla**, seguindo o
  padrao de `DEC-021` — que so existe como entrada registrada porque
  o gate anterior a reconstruiu.

## LAB-GOV-DECISION-LEDGER-001 - 2026-08-04

### Found

- O `DECISION_LEDGER.yaml` terminava em `DEC-014`. Oito identificadores
  eram citados como autoridade **sem entrada nenhuma**: `DEC-015`,
  `DEC-016`, `DEC-017`, `DEC-018`, `DEC-020`, `DEC-021`, `DEC-022` e
  `DEC-023`.
- **`DEC-014` designava duas decisoes diferentes.** No ledger, o
  endurecimento PENDENTE de `FROZEN_PARTIAL_RESULT`, com `authority: null`
  e `affected_paths: []`. No changelog, uma edicao de sequencia de gates
  no `labctl.py`.
- `DEC-019` nunca foi citado em lugar nenhum: buraco na numeracao.
- Todas as oito autorizavam **edicoes literais em `10_TOOLS/labctl.py`**,
  o validador de todo gate. `DEC-021` e a de maior alcance: a
  pre-condicao dupla `VERIFIED` **e** `result_review APPROVED` foi depois
  replicada para **quatro** frentes, governando-as sem que sua
  autorizacao estivesse registrada.

### Reconstructed

- Oito decisoes registradas, cada uma com `original_registration: MISSING`,
  `reconstructed_from` apontando a fonte sobrevivente e
  `reconstruction_confidence`. Nada foi inventado alem do que a fonte diz.
- `DEC-019` registrado como `NEVER_ISSUED` com `reuse_policy: FORBIDDEN`.
  Registrar o buraco e preferivel a reutilizar o numero, que produziria
  ambiguidade indistinguivel da colisao de `DEC-014`.
- A colisao foi resolvida atribuindo `DEC-025` a decisao de sequencia de
  gates, com `cited_in_changelog_as: DEC-014`. **O texto historico do
  changelog nao foi tocado** — reescreve-lo apagaria a evidencia do
  proprio defeito.

### Caught

- **A verificacao nova encontrou, na primeira execucao, uma oitava
  decisao que a inspecao manual perdeu.** `DEC-023` estava citado num
  `.json`, fora do alcance do grep manual que cobriu changelog e YAML.
- A fonte de `DEC-023` e **estruturada**, um bloco
  `governance_deviations`. O laboratorio ja tinha o mecanismo de registro
  por gate; faltava a consolidacao. A informacao estava desconsolidada,
  nao perdida.

### Added

- `scan_decision_citations` no `labctl`: toda citacao `DEC-NNN` sob o
  laboratorio precisa de exatamente uma entrada no ledger, e
  `DECISION_LEDGER has duplicate decision_id` passa a ser erro.
- **Teste negativo executado**: um arquivo temporario citando um
  identificador `DEC-NNN` inexistente foi criado, a verificacao o
  **recusou**, e o arquivo foi removido. Uma verificacao que nunca falhou
  nao foi demonstrada.
- **A verificacao entao recusou esta propria entrada de changelog**, que
  na primeira redacao continha o identificador falso escrito por extenso.
  O instrumento morde quem o escreveu, que e a unica evidencia que vale.
- Limite declarado: a verificacao detecta citacao **sem** entrada. Ela
  **nao** detecta citacao com entrada **errada** — a colisao de `DEC-014`
  foi resolvida por campo explicito, nao por varredura.

### Fixed

- O corpo em prosa do `LAB_STATE.md` estava **desatualizado por seis
  gates**, apresentando `FOUND-FUNCTIONAL-GRAPH-001` como estado corrente
  enquanto o front matter ja registrava dez frentes encerradas. Como
  `resume_read_order` manda ler esse arquivo primeiro, a prosa obsoleta
  enganava exatamente na retomada.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `0` claims promovidas,
  `24` no ledger, `0` frentes encerradas tocadas, `0` arquivos Lean.

## PORTFOLIO-REVIEW-AFTER-BISIMULATION - 2026-08-04

### Selected

- **`LAB-GOV-DECISION-LEDGER-001`**. Sete alternativas comparadas.

### Found

- O `DECISION_LEDGER.yaml` termina em `DEC-014`. O `CHANGELOG.md` invoca
  `DEC-015`, `DEC-016`, `DEC-017`, `DEC-018`, `DEC-020`, `DEC-021` e
  `DEC-022` como autoridade. **Nenhuma das sete existe no ledger.**
- `DEC-014` designa **duas decisoes diferentes**: no ledger, o
  endurecimento PENDENTE de `FROZEN_PARTIAL_RESULT` com `authority: null`;
  no changelog, uma edicao de sequencia de gates no `labctl.py`.
- `DEC-019` nunca e citado: buraco na numeracao.
- Todas autorizam edicoes literais em `10_TOOLS/labctl.py`, **o validador
  de todo gate**.

### Rejected

- O candidato **certificado de reflexao decidivel** foi formalizado em
  probe, **compilou**, e foi **rejeitado mesmo assim**: a hipotese da
  janela implica a da equacao unica, o excedente nao tem nenhum
  consumidor, e "decidivel" e pago com `DecidableEq C`, exatamente a
  hipotese que a frente anterior mede como nao exigida.
- A proposta era minha. Caiu em verificacao adversarial **antes** de
  virar frente.

### Probed

- `15` declaracoes compiladas em probe descartavel, `exit 0`, arvore
  versionada intocada. Duas objecoes dos refutadores foram **derrubadas
  pelo probe**: `0 < period` e `baseIndex + period <= n` **sao**
  recuperaveis da API publica, re-derivando a reducao em namespace novo.

### Locked

- `authorized_action: LAB_GOV_DECISION_LEDGER_CORRECTION_AUTHORIZED`.
  `0` claims promovidas, `24` no ledger, `0` frentes encerradas tocadas.
- `DEC-024` registrado **no mesmo commit** que faz sua edicao.

## FOUND-BISIMULATION-BOUNDARY-001-RESULT-REVIEW - 2026-08-03

### Approved

- `FOUND_BISIMULATION_BOUNDARY_001_RESULT_REVIEW_APPROVED`. Doze itens
  CONFIRMADOS, com build, modulos isolados e contagens **reexecutados**
  neste gate.

### Promoted

- **`DETERMINISTIC-BISIMULATION-COLLAPSE-FORMAL-001`**,
  `evidence_level: F`, novidade `NONE`. Ledger de `23` para `24`.
- A entrada carrega um campo `scope_qualifier_required`: toda formulacao
  precisa dizer "para sistemas deterministicos totais" e "bissimulacao
  funcional". Sem isso a afirmacao e falsa.

### Caught

- **O scanner ampliado pegou dois duplicados YAML introduzidos neste
  proprio ciclo**, antes do commit: um patch orfaou duas linhas do bloco
  `probe:` do `STATUS.yaml`, que cairam dentro de `formalization:`, e um
  `formalization_status` obsoleto sobreviveu na fila.
- `LAB-GOV-FRONTMATTER-SCAN-001` pagou por si mesmo dois gates depois de
  ter sido feito.

### Closed

- Frente **ENCERRADA**. `work_status: VERIFIED`,
  `result_review: APPROVED`. Bissimulacao relacional, sistemas nao
  deterministicos, acoes rotuladas, coinducao, quocientes e extracao
  seguem **NAO AUTORIZADOS**.
- `BIS-GAP-010`, a bibliografia de semantica de concorrencia, fica
  **deliberadamente aberta**: o resultado toca uma nocao com literatura
  propria, e fecha-la por delimitacao seria mais fragil do que foi na
  frente anterior.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `0` frentes encerradas
  modificadas, `0` duplicatas YAML em `413` arquivos.

## FOUND-BISIMULATION-BOUNDARY-001-FORMALIZATION - 2026-08-03

### Formalized

- Oito arquivos Lean permanentes. `lake build` **exit 0**, `8775` jobs,
  `0` linhas de erro reais.
- `8` declaracoes publicas — `3` definicoes e `5` teoremas — contagem
  **derivada por script**, batendo com o congelado.
- **Pegada axiomatica NENHUMA, em dez de dez declaracoes.** Nada aqui
  atravessa `analyzeEncodedSystem`: nao ha `Array`, nao ha tabela, nao ha
  execucao, entao `propext`, `Classical.choice` e `Quot.sound` nao entram
  em lugar nenhum.

### Corrected

- A primeira organizacao deixava `boolToUnit_bisimulation` e
  `forgetBool_surjective` no modulo das negacoes publicas, e o script
  derivava **10** declaracoes contra as **8** congeladas. As duas nao
  podiam ir para os testes — as negacoes publicas as consomem — entao
  foram separadas em `CounterexampleInstance.lean`, como a frente
  anterior fez com `Counterexample.lean`.
- A divergencia foi resolvida **movendo o codigo para refletir a
  classificacao**, nao ajustando a contagem para caber.

### Recorded

- **Um falso negativo, registrado e explicado.** Logo apos criar o modulo
  novo, dois arquivos reportaram `exit=1 errors=1` na elaboracao isolada
  enquanto o `lake build` passava. Causa: `lake env lean` nao constroi
  dependencias, e o `.olean` do modulo recem-criado ainda nao existia.
  Reexecutados apos o build: `exit=0 errors=0` nos oito.
- Um `exit=1` ao lado de um build verde e exatamente o padrao que nao
  pode ser silenciado. Aqui a contradicao tinha explicacao verificavel, e
  foi verificada.

### Locked

- `authorized_action: FOUND_BISIMULATION_BOUNDARY_001_RESULT_REVIEW_AUTHORIZED`.
  `0` claims promovidas, `23` no ledger, `0` frentes encerradas tocadas.

## FOUND-BISIMULATION-BOUNDARY-001-SPECIFICATION-REVIEW - 2026-08-03

### Approved

- `FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_REVIEW_APPROVED`. Dez
  itens conferidos, nenhuma correcao material necessaria.

### Verified

- **`STOP-BIS-002` testada diretamente.** A existencial do zag continua
  no lugar:

```lean
example : Reflects abstract stepC stepA
    ↔ ∀ c, ∃ c', stepC c = c' ∧ abstract c' = stepA (abstract c) := Iff.rfl
```

  E o contraste fecha o argumento: `simulates_iff_semiconj` **e**
  `Iff.rfl`, e `reflects_iff_simulates` **nao e** — precisou de prova nas
  duas direcoes. Se `Reflects` tivesse sido trivializado, os dois seriam
  `Iff.rfl`.

### Measured

- **Sete de sete declaracoes sem pegada axiomatica.** Ao contrario da
  frente anterior, nada aqui atravessa `analyzeEncodedSystem`, de modo
  que `propext`, `Classical.choice` e `Quot.sound` nao entram.
- Probe de revisao: `error_lines=0`, `REAL_EXIT_CODE=0`, capturado por
  arquivo de script.

### Recorded

- Especificacao e revisao sao do mesmo agente, em sessoes consecutivas.
  A revisao vale pelo que mediu.

### Locked

- `authorized_action: FOUND_BISIMULATION_BOUNDARY_001_FORMALIZATION_AUTHORIZED`.
  `0` arquivos Lean permanentes, `0` claims promovidas, `23` no ledger.

## FOUND-BISIMULATION-BOUNDARY-001-SPECIFICATION - 2026-08-03

### Specified

- Especificacao congelada em
  `02_FOUNDATIONS/08_BISIMULATION/FOUND_BISIMULATION_BOUNDARY_001/`.
- Tres definicoes — `Simulates`, `Reflects`, `Bisimulation` — e cinco
  teoremas. `8` declaracoes publicas, `0` typeclasses, pegada axiomatica
  **NENHUMA** em toda a frente.

### Decided

- **`Reflects` conserva o `∃ c'`**, mesmo sabendo que a testemunha esta
  determinada. Escreve-lo ja resolvido tornaria o colapso uma tautologia
  disfarcada de teorema — `STOP-BIS-002`. O contraste e verificavel:
  `simulates_iff_semiconj` **e** `Iff.rfl`, e `reflects_iff_simulates`
  **nao e** — precisou de prova nas duas direcoes.
- Nenhuma estrutura de dado nova. A frente e inteiramente proposicional,
  e por isso **nao ha testes executaveis**: inventar um `#eval` seria
  teatro.

### Bounded

- `SCOPE_BOUNDARY.md` e o documento mais importante da frente. O colapso
  vem da **ausencia de escolha** no zag: `stepC` e funcao total, entao a
  testemunha e imposta. Qualquer relaxamento que devolva escolha —
  nao determinismo, relacoes gerais, bissimulacao relacional, acoes
  rotuladas, funcoes parciais — destroi o argumento.
- Wording proibida registrada: escrever "bissimulacao e semiconjugacao"
  **sem qualificador** e falso, e falso exatamente na teoria de
  concorrencia onde a palavra nasceu.

### Locked

- `authorized_action: FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_REVIEW_AUTHORIZED`.
  `0` arquivos Lean permanentes, `0` claims promovidas, `23` no ledger,
  `0` duplicatas YAML.

## PORTFOLIO-REVIEW-AFTER-FRONTMATTER-SCAN - 2026-08-03

### Selected

- **`FOUND-BISIMULATION-BOUNDARY-001`**, bissimulacao deterministica e o
  limite da reflexao de ciclos. Cinco alternativas comparadas. Ataca
  `ABS-GAP-015`, deixado aberto pela frente anterior.

### Proved in probe

- **Zig e zag COLAPSAM em sistemas deterministicos totais:**

```lean
theorem bisimulation_iff_semiconj (abstract) (stepC) (stepA) :
    Bisimulation abstract stepC stepA
      ↔ Function.Semiconj abstract stepC stepA
```

  Sem depender de nenhum axioma. O zag e gratuito: a testemunha do passo
  concreto e `stepC c`, e a obrigacao que sobra e exatamente o zig.
- **`BOOL_TO_UNIT` ja e uma bissimulacao**, e `forgetBool` e
  **sobrejetiva**. Portanto `bisimulation_does_not_reflect_cycles` e
  `surjective_bisimulation_does_not_reflect_cycles`, ambos teoremas que
  compilam, ambos sem pegada.

### Clarified

- A proibicao ja existente — "nao assumir bissimulacao onde so ha
  semiconjugacao" — deixava implicito que **obter** bissimulacao
  resolveria o problema. No recorte deterministico total nao ha nada a
  obter, e o ciclo continua espurio. O que separa e injetividade sobre a
  orbita.

### Bounded

- O colapso vale para bissimulacao **funcional** entre sistemas
  **deterministicos totais**. Sistemas nao deterministicos, relacoes de
  transicao gerais, bissimulacao relacional, acoes rotuladas e coinducao
  seguem **NAO AUTORIZADOS**, e generalizar o colapso e a stop condition
  principal da frente.

### Locked

- `authorized_action: FOUND_BISIMULATION_BOUNDARY_001_SPECIFICATION_PREPARATION_AUTHORIZED`,
  literal, sem wildcard. `17` itens na fila, `0` claims promovidas, `23`
  no ledger, `0` arquivos Lean tocados.

## LAB-GOV-FRONTMATTER-SCAN-001 - 2026-08-03

### Fixed

- A varredura de chaves YAML duplicadas passou a cobrir o **front matter
  dos documentos Markdown**. Cobertura de `57` para **`390`** arquivos:
  `57` YAML mais `333` front matter.
- `LAB_STATE.md` — onde vivem `authorized_action`, `work_status` e
  `canonical_commit` — **entrou na varredura pela primeira vez**.
- `read_front_matter` deixou de aceitar **"ultimo valor vence"**. Antes,
  `status: READY` seguido de `status: VERIFIED` resolvia silenciosamente
  para `VERIFIED`; num campo como `authorized_action` isso seria uma
  autorizacao escolhida pelo parser. Agora falha com
  `DUPLICATE_YAML_KEY`.

### Found

- Duplicatas em front matter: **`0`**. O corpus estava limpo.
- Front matter malformado: **`1`**, e era o `LAB_STATE.md`. O
  delimitador de fechamento dividia a linha com o primeiro titulo —
  `---# Estado atual` — e passava apenas porque a expressao regular era
  tolerante. Corrigido.

### Preserved

- **A logica de deteccao nao foi tocada.** O defeito era de escopo, nao
  de algoritmo: `detect_duplicate_yaml_keys` ja funcionava sobre front
  matter, e a nova funcao reutiliza o mesmo `_walk_yaml_node`.

### Tested

- `13` testes novos, `FM-TEST-001` a `FM-TEST-013`. Suite de `21` para
  **`34`**, todos passando.
- `FM-TEST-012` impede a regressao especifica: voltar a declarar a
  varredura integral sem `LAB_STATE.md` dentro dela.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. `0` claims promovidas,
  `23` no ledger. `0` arquivos Lean tocados, `0` frentes encerradas
  tocadas.

## PORTFOLIO-REVIEW-AFTER-FINITE-STATE-ABSTRACTION - 2026-08-03

### Found

- **O scanner de chaves YAML duplicadas nunca varreu front matter.**
  Medido por probe: `483` arquivos Markdown no laboratorio, `332` com
  front matter YAML, `57` arquivos enumerados pelo scanner, **`0`**
  deles Markdown. `LAB_STATE.md` — o arquivo mais critico da
  governanca — **nao esta** no scan de duplicatas.
- Ainda assim, todo relatorio de gate afirma
  `yaml_duplicate_key_scan: PASS`. A afirmacao e verdadeira sobre `57`
  arquivos e foi lida como se fosse sobre todos.
- `read_front_matter` usa `yaml.safe_load` e aplica **"ultimo valor
  vence"** — exatamente a semantica que a regra de governanca do
  laboratorio proibe por escrito. Verificado: `status: READY` seguido de
  `status: VERIFIED` resolve silenciosamente para `VERIFIED`.
- O defeito e de **escopo, nao de algoritmo**:
  `detect_duplicate_yaml_keys` aplicado a um `.md` com chave duplicada
  encontra o problema. Apenas `yaml_files_under` filtra por extensao.

### Selected

- **`LAB-GOV-FRONTMATTER-SCAN-001`**, cobertura integral do scanner.
  Seis alternativas comparadas.

### Rejected

- `B` e `D` — bissimulacao e quocientes sao a continuacao cientifica
  natural, e merecem ser abertas com a cadeia de evidencia confiavel,
  nao antes disso.
- `C` — `ENC-GAP-020` segue com o acoplamento que o reprovou na revisao
  anterior; nada mudou.
- `E` — extracao, CLI e parser distribuem garantia sem contrato
  semantico.
- `F` — abrir frente matematica nova enquanto o instrumento de validacao
  tem cobertura menor do que declara seria acumular resultados sobre uma
  medicao ja sabidamente incompleta.

### Locked

- `authorized_action: LAB_GOV_FRONTMATTER_SCAN_CORRECTION_AUTHORIZED`,
  literal, sem wildcard. `0` claims promovidas, `23` no ledger. Nenhuma
  frente encerrada tocada, nenhum arquivo Lean tocado.

## FOUND-FINITE-STATE-ABSTRACTION-001-RESULT-REVIEW - 2026-08-03

### Approved

- `FOUND_FINITE_STATE_ABSTRACTION_001_RESULT_REVIEW_APPROVED`. Os
  **quatorze** itens de conferencia CONFIRMADOS, com build, auditoria
  umbrella e contagens **reexecutados** neste gate — nada foi herdado do
  anterior.

### Promoted

- Uma unica claim: **`CERTIFIED-FINITE-STATE-ABSTRACTION-FORMAL-001`**,
  `evidence_level: F`, `mathematical_novelty: NONE`,
  `algorithmic_novelty: NONE`. Ledger de `22` para `23`.
- A claim carrega a propria contraevidencia: `BOOL_TO_UNIT` e a
  abstracao por paridade estao registrados em `counterevidence`, porque
  medem o limite exato do que foi provado.

### Closed

- Frente **ENCERRADA**. `work_status: VERIFIED`,
  `result_review: APPROVED`, `extension_status: NOT_AUTHORIZED`.
- Bissimulacao, quocientes, extracao, integracao externa, CLI e parser
  permanecem **NAO AUTORIZADOS**. `ABS-GAP-017` — a correcao de uma
  abstracao externa real — fica **permanentemente aberto**.

### Recorded

- Os quatro gates foram executados pelo mesmo agente em sessoes
  consecutivas. Nenhum substitui revisao externa; o que sustenta o
  resultado e o que foi medido e reexecutado.

### Locked

- `authorized_action: PORTFOLIO_REVIEW_REQUIRED`. A trava nao e
  autorizacao: nenhuma frente nova esta escolhida. `0` arquivos de
  frentes encerradas modificados, `0` duplicatas YAML em `57` arquivos.

## FOUND-FINITE-STATE-ABSTRACTION-001-FORMALIZATION - 2026-08-03

### Formalized

- Onze arquivos Lean permanentes. `lake build` **exit 0**, `8767` jobs,
  `0` linhas de erro reais.
- Sete declaracoes publicas, contagem **derivada por script** a partir do
  codigo: `1` estrutura, `2` definicoes, `4` teoremas. Coincide com o
  `PUBLIC_TOTAL` congelado; nenhuma correcao de contagem foi necessaria.
- `OrbitSeparating` e as **dez** declaracoes do contraexemplo:
  `does not depend on any axioms`. A camada nova da frente e onze
  declaracoes com pegada zero.

### Fixed

- `FoundFiniteStateAbstraction001UmbrellaAudit.lean` falhou na primeira
  elaboracao: `failed to synthesize Decidable (Function.Semiconj …)`.
  `Function.Semiconj` e um `def`, e a resolucao de instancias nao o
  desdobra — mesma armadilha ja registrada para `CycleWitness.Valid`.
  Corrigido com `intro i; revert i; decide`. A falha foi registrada,
  nao mascarada.

### Corrected

- **Defeito de metodo, nao de resultado**: codigos de saida capturados
  com `echo $?` atravessavam uma fronteira de shell e refletiam o
  hospedeiro, nao o `lean`. Detectado por dois sintomas: um "exit 0" com
  `lake` ausente do PATH, e um "exit 0" com `error: failed to synthesize`
  na saida.
- Toda captura passou a viver em **arquivo de script**. Os dois probes
  dos gates anteriores foram **reexecutados**: `errors=0`,
  `REAL_EXIT_CODE=0` nos dois. Nenhuma afirmacao anterior era falsa.
  Registrado em `VERIFICATION_METHOD_CORRECTION.md`.

### Demonstrated

- A auditoria umbrella instancia uma abstracao **genuinamente
  muitos-para-um**: `Fin 4 → Fin 2` pela paridade, sobre rotacao. A
  analise devolve `.ok ⟨0,2⟩`, a recorrencia **observacional vale** e a
  **concreta falha** — `rotate4` so volta em quatro passos. O fenomeno
  central da frente, sem depender da degenerescencia de `BOOL_TO_UNIT`.

### Closed

- `15` de `20` gaps. Permanecem abertos `ABS-GAP-015`, `016`, `018` e
  `020` por escopo, e **`ABS-GAP-017` permanentemente**: nenhuma frente
  formal decide se um sistema externo real foi corretamente modelado.

### Locked

- `authorized_action: FOUND_FINITE_STATE_ABSTRACTION_001_RESULT_REVIEW_AUTHORIZED`.
  `0` claims promovidas — a promocao pertence ao gate de revisao de
  resultado. `22` no ledger. `0` duplicatas YAML. `0` arquivos de
  frentes encerradas modificados.

## FOUND-FINITE-STATE-ABSTRACTION-001-SPECIFICATION-REVIEW - 2026-08-03

### Approved

- `FOUND_FINITE_STATE_ABSTRACTION_001_SPECIFICATION_REVIEW_APPROVED`.
  Os **quinze** criterios de aprovacao verificados um a um; nenhuma
  correcao material foi necessaria.

### Measured, not quoted

- `#check` confirmou que `analyzeAbstractSystem_observational_sound`
  conclui em `abstraction.abstract (…) = abstraction.abstract (…)` —
  **ambos os lados sob `abstract`**, igualdade em `A`.
- `#check` confirmou `OrbitSeparating` como hipotese **explicita e
  primeira** de `analyzeAbstractSystem_reflected_sound`, que e a unica
  declaracao publica a concluir em `C`.
- `CertifiedFiniteAbstraction : (C : Type u) → (A : Type v) → (C → C) →
  (A → A) → Type (max u v)`. Zero typeclasses no tipo.

### Proved

- `naive_cycle_reflection_is_false`, novo no probe de revisao:
  **sem depender de axioma nenhum**.
- `boolToUnit_not_orbitSeparating` reescrito como termo puro,
  eliminando o `Quot.sound` que a versao com `simp` carregava.

### Probed

- `/tmp/FiniteStateAbstractionReviewProbe.lean`, **exit 0**, removido.
  `0` declaracoes destinadas a falhar, `0` usos de `native_decide`.

### Recorded

- A especificacao e sua revisao ocorreram em sessoes consecutivas do
  mesmo agente. A revisao vale pelo que **mediu**, nao por independencia
  de autoria. Registrado em `SPECIFICATION_REVIEW.md`.

### Locked

- `authorized_action: FOUND_FINITE_STATE_ABSTRACTION_001_FORMALIZATION_AUTHORIZED`,
  literal, sem wildcard. Bissimulacao, quocientes, extracao, integracao,
  CLI e parser seguem **nao autorizados**. `0` arquivos Lean
  permanentes, `0` claims promovidas, `22` no ledger, `0` duplicatas
  YAML em `57` arquivos.

## FOUND-FINITE-STATE-ABSTRACTION-001-SPECIFICATION - 2026-08-03

### Renamed

- O item ativo passou a ser **`FOUND-FINITE-STATE-ABSTRACTION-001`**. O
  nome candidato anterior, `FOUND-FINITE-ABSTRACTION-001`, sobrevive
  apenas em artefatos historicos imutaveis. `aliases_active: 0`,
  `duplicate_work_items: 0`. A saida (b) da secao 10 de
  `PROGRAM_STATE_AND_ROADMAP.md` foi a executada.

### Specified

- Especificacao congelada em
  `02_FOUNDATIONS/07_FINITE_ABSTRACTION/FOUND_FINITE_STATE_ABSTRACTION_001/`.
- `CertifiedFiniteAbstraction`: **dois campos**, `abstract` e `commutes`.
  Nao armazena encoding, estado inicial, witness, tabela nem condicao de
  reflexao — a codificacao permanece argumento separado.
- Orientacao da semiconjugacao auditada contra a assinatura real e
  confirmada por `Iff.rfl`:
  `abstract (stepC c) = stepA (abstract c)`.
- **A soundness observacional termina em `A`**, depois de aplicar
  `abstract`. Concluir em `C` sem hipotese adicional passou a ser
  `STOP-ABS-004`.
- A reflexao concreta exige `OrbitSeparating` **visivel na assinatura**.
- `analyzeAbstractSystem_complete` garante existencia de witness
  abstrato, e **nao** recorrencia concreta — `STOP-ABS-018`, nova.

### Probed

- `/tmp/FiniteStateAbstractionProbe.lean`, **exit 0**, removido depois.
  Nenhuma declaracao destinada a falhar; o resultado negativo e o
  teorema `boolToUnit_not_orbitSeparating`, que compila **sem depender
  de axioma nenhum**.
- `OrbitSeparating`, `orbitSeparating_iff_injOn` e
  `orbitSeparating_of_injective`: nenhum axioma. A pegada
  `propext, Classical.choice, Quot.sound` entra somente onde
  `analyzeEncodedSystem` entra.
- Nenhuma typeclass sobre `C` ou `A` na cadeia central, confirmado por
  compilacao com `C A : Type*`.

### Decided

- `Set.InjOn` sobre a orbita: equivalencia **compilada sem axiomas** e
  ainda assim classificada `DEFERRED_OPTIONAL`. Compilar nao e motivo
  para publicar; nenhum resultado central a consome.

### Locked

- `authorized_action: FOUND_FINITE_STATE_ABSTRACTION_001_SPECIFICATION_REVIEW_AUTHORIZED`,
  entrada literal, sem wildcard. Formalizacao, bissimulacao, quocientes,
  extracao, CLI e integracao seguem **nao autorizadas**. `0` arquivos
  Lean permanentes criados, `0` claims promovidas, `22` no ledger, `0`
  duplicatas YAML.

## PORTFOLIO-REVIEW-AFTER-CERTIFIED-ENCODING - 2026-08-01

### Selected

- **`FOUND-FINITE-ABSTRACTION-001`**, abstracao finita certificada,
  simulacao e fronteiras de reflexao de ciclos. Sete alternativas
  comparadas; as **doze** condicoes da regra de decisao verificadas,
  **oito delas por compilacao**.

### Proved in probe

- **A reflexao ingenua eh FALSA, e agora isso eh teorema**:

```lean
theorem naive_cycle_reflection_is_false :
    ¬ (∀ C A stepC stepA abstract, Function.Semiconj abstract stepC stepA →
        ∀ start, abstract (stepC start) = abstract start → stepC start = start)
```

  Compilado **sem depender de axioma nenhum**, pelo contraexemplo
  `Bool → Unit` com `stepC = not`: o sistema abstrato repete em um passo,
  o concreto nao.
- A **soundness observacional** vale com apenas semiconjugacao: a analise
  do sistema abstrato conclui `abstract (stepC^[b+p] start) =
  abstract (stepC^[b] start)` — igualdade entre **observacoes**, nao
  entre estados.
- `OrbitSeparating` recupera a igualdade concreta, e eh **nao
  tautologica**: `boolToUnit_not_orbitSeparating` prova que ela falha
  exatamente no contraexemplo. Sem axiomas.
- `orbitSeparating_iff_injOn` — equivalente a `Set.InjOn` sobre a orbita.
  Sem axiomas.

### Measured

- Nenhuma peca exige `C` finito nem `DecidableEq C`: os probes usam
  `C : Type*` sem typeclass.
- Auditoria da alternativa `F`: `429` arquivos Markdown, `277` com front
  matter YAML, **`0`** com chave duplicada; o bloco de `LAB_STATE.md`
  tambem limpo. A lacuna eh real — o scanner seleciona por extensao — mas
  **nao esta sendo explorada**, e por isso nao tem prioridade.

### Rejected

- `B` fecharia `ENC-GAP-020`, mas a igualdade do witness concreto depende
  da ordem de enumeracao do detector: risco de acoplamento **o mais alto
  das sete**.
- `C` e `D` distribuem garantia sem contrato semantico para o caso geral;
  `D` ainda depende de `C`.
- `E` eh conforto operacional. `G` nao tem produto em trinta dias.

### Locked

- `authorized_action: FOUND_FINITE_ABSTRACTION_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
  Uma entrada literal, sem wildcard. Formalizacao, bissimulacao,
  quocientes, extracao, CLI e integracao seguem **nao autorizadas**;
  todos os `extension_status: NOT_AUTHORIZED` preservados. `22` claims,
  `0` duplicatas YAML.


## LAB-GOV-YAML-DUPLICATE-KEYS-001 - 2026-08-01

### Found

- A varredura **integral** dos `55` arquivos YAML do laboratorio achou
  **8 duplicatas em 3 arquivos**, e nao as tres da fila que o relatorio
  anterior mencionava. Duas divergencias novas apareceram porque a busca
  anterior olhou apenas `RESEARCH_QUEUE.yaml`:

```text
FOUND_CYCLE_DETECTION_001/STATUS.yaml  extraction_status
    NOT_AUTHORIZED  contra  READY_FOR_FEASIBILITY_AUDIT
ENG_FINITE_STATE_ENCODING_001/STATUS.yaml  documents
    39  contra  65
```

- A primeira eh a mais seria: uma frente **encerrada** vinha sendo lida
  com uma trava **mais fraca** do que a governanca de fato mantem.

### Resolved

- `tests_planned` do runtime adapter: `9` contra `8`, com o parser usando
  `8`. Fonte de verdade: `TEST_PLAN.md`, que congela `RT-TEST-001..009`, e
  o `STATUS.yaml` da frente — ambos `9`. O `8` era a contagem de
  **selecao**, anterior ao congelamento. Valor final **`9`**, e a mudanca
  eh classificada como
  `NON_MATHEMATICAL_GOVERNANCE_SEMANTIC_CORRECTION`, nao como cosmetica.
- `extraction_status` do detector de ciclos: valor final `NOT_AUTHORIZED`,
  por `CLOSURE_RECORD.md` e `LAB_STATE`. O valor de estagio permanece
  registrado em `COMPUTABILITY_REVIEW.md`.
- `documents` da codificacao certificada: `65`, a contagem real do
  diretorio.
- Cinco duplicatas identicas normalizadas, mantida a primeira ocorrencia.

### Enforced

- `labctl validate` passou a **rejeitar** qualquer chave duplicada, com o
  codigo `DUPLICATE_YAML_KEY`, antes de qualquer carregamento normal. A
  deteccao percorre a **arvore sintatica** por `yaml.compose_all` — o
  objeto ja carregado nao serve, porque nele a duplicata desapareceu.
- Escopo: **todo** `.yaml` e `.yml` versionado sob o laboratorio, e nao
  apenas os arquivos que o `labctl` carrega.
- Duplicata identica tambem eh `FAIL`. Nao existe modo de aviso.

### Tested

- `pytest`: **21** testes, contra `9` antes. Doze novos cobrem mapa raiz,
  mapa aninhado, mapa dentro de sequencia, multiplos documentos, linhas
  reportadas, chaves iguais em mapas distintos, valores repetidos em
  lista, diretorios excluidos e a varredura integral do repositorio.

### Ruled

- `00_GOVERNANCE/YAML_DUPLICATE_KEY_POLICY.md`: uma chave por mapa;
  duplicatas identicas proibidas; "ultimo valor vence" nao eh semantica de
  governanca; e **auditoria declarada integral deve percorrer o conjunto
  completo** — uma auditoria parcial nao pode ser descrita como completa.

### Preserved

- `22` claims, `15` work items, zero arquivos Lean criados ou modificados,
  zero teoremas tocados, `lake build` nao executado. Nenhum estado
  cientifico alterado: as unicas mudancas de valor efetivo estao nos tres
  campos divergentes, todos de governanca.


## ENG-FINITE-STATE-ENCODING-001-RESULT-REVIEW - 2026-08-01

### Closed

- **A primeira cadeia do laboratorio que comeca em um objeto Lean TIPADO e
  termina em um certificado interpretado nesse mesmo objeto.** `15`
  declaracoes publicas — **derivadas do codigo, nao lidas do cabecalho** —,
  `1` auxiliar privado, `2` pontos de transporte, `20` lacunas com `15`
  resolvidas, `22` claims.

### Verified

- `tableIndex_val` eh `rfl`: o transporte **nao altera** o indice natural.
- A semiconjugacao usa `decode_encode`; `encode_decode` **nao aparece** em
  `Commutation.lean`.
- A soundness termina em igualdade **em `S`**; a completeness nao exige
  **nenhuma** pre-condicao.
- `run?` e `step?` nao foram copiados; `validateTransitionTable` aparece
  `1` vez em docstring e `0` vezes em codigo.
- Novo `EngFiniteStateEncoding001UmbrellaAudit.lean` alcanca as quinze
  declaracoes pela raiz. Exit `0`, `80` s. Nao registrado em
  `TamesisLab.lean` — importa a raiz, e registra-lo criaria ciclo.

### Found

- **`META-ENC-003`**: a varredura de chaves duplicadas foi refeita sobre a
  **fila inteira**, e nao sobre duas chaves nomeadas. Achou tres itens com
  duplicatas, e um deles **divergente**:
  `ENG-FINITE-STATE-RUNTIME-001.tests_planned = ['9', '8']`. Frente
  encerrada: **nada foi alterado**, e o caso aguarda gate corretivo.
- Uma verificacao parcial apresentada como completa eh o mesmo defeito de
  `ENC-VAL-001` — evidencia mais fraca que a afirmacao que sustenta.

### Ruled

- Nova regra: **contagens agregadas nao sao fonte primaria**, devem ser
  derivadas ou conferidas automaticamente, e a conferencia precisa
  percorrer **todas** as entradas. Terceira divergencia deste tipo.

### Locked

- `result_review: APPROVED`; extensao, recodificacao, extracao, CLI,
  parser e integracao em `NOT_AUTHORIZED`;
  `external_abstraction_correctness: DEFERRED`;
  `authorized_action: PORTFOLIO_REVIEW_REQUIRED` — **trava**, nao
  autorizacao. Nenhuma entrada nova no allowlist.


## ENG-FINITE-STATE-ENCODING-001-FORMALIZATION - 2026-08-01

### Built

- **A cadeia que comeca em um objeto Lean TIPADO e termina em um
  certificado interpretado NESSE objeto.** `1` estrutura, `4` definicoes,
  `11` teoremas (1 privado), `450` linhas — contra `869` da frente
  anterior. A diferenca eh reutilizacao: nada do detector nem da execucao
  bruta foi reescrito.
- **A soundness termina em `S`**:
  `stepS^[b + p] start = stepS^[b] start`. Quatro linhas de prova, cuja
  ultima seta eh `encode_injective`.
- **A completeness nao exige pre-condicao nenhuma** do consumidor: a
  validade da tabela e o dominio do indice vem da construcao.

### Key move

- `table_iterate_commutes` eh **um termo de uma linha**, por
  `Function.Semiconj.iterate_right`. O resultado analogo da frente
  anterior custou inducao manual com dois `show` obrigatorios.
- **Dois** pontos de transporte, e apenas dois: `tableIndex`, publico, e
  `buildTransitionTable_getElem`, `private`. Este ultimo vive em
  `Commutation.lean` e nao em `TableConstruction.lean` por uma razao
  concreta: `private` eh escopo de modulo, e seu unico consumidor eh a
  semiconjugacao.

### Measured

- `encode_injective` e `encodedStep` **nao dependem de axioma nenhum**. A
  pegada entra em `buildTransitionTable`, pelo campo `closed`.
- `sorryAx` `0`, axiomas locais `0`, tokens proibidos `0`, correcoes
  silenciosas `0`, `Eq.ndrec` `0`, `HEq` `0`.
- `lake build` **PASS, 8757 jobs**, `120` s. Baseline `8748`; a diferenca
  de `9` eh exatamente 5 modulos + agregador + 3 testes.
- `ENC-TEST-006`: sob a codificacao `i ↦ 3 - i` a tabela vira
  `#[1,0,1,2]` em vez de `#[1,2,3,2]`, e a **mesma** conclusao semantica
  eh derivada no tipo original.

### Corrected

- `FINAL_PUBLIC_API.md` declarava `14` declaracoes publicas mas listava
  quinze. O numero medido nos modulos eh **`15`**. Erro de cabecalho do
  gate de revisao, registrado em vez de silenciado.

### Bounded

- Novidade `NONE`. **Nao** foi provada invariancia do witness concreto sob
  recodificacao — `ENC-GAP-020`, `STOP-ENC-019` —, e a coincidencia
  observada nos testes eh observacao, nao teorema.

### Locked

- `formalization_status: VERIFIED`;
  `authorized_action: ENG_FINITE_STATE_ENCODING_001_RESULT_REVIEW_AUTHORIZED`.
  Uma entrada literal, sem wildcard. Extracao, CLI, parser, integracao e
  `002` seguem **nao autorizadas**. Ledger: `22` claims.


## ENG-FINITE-STATE-ENCODING-001-CORRECTIVE-VALIDATION - 2026-08-01

### Corrected

- **`ENC-VAL-001`**, `NON_MATHEMATICAL_VALIDATION_FAILURE`. O probe de
  axiomas do gate anterior terminou com `exit 1` e mesmo assim foi
  reportado como `PASS`. As falhas eram experimentos negativos
  intencionais sobre a rota definicional descartada — medicao valida, no
  arquivo errado.
- Os dois probes obrigatorios foram reescritos e reexecutados:

```text
FiniteStateEncodingReviewProbe.lean   exit 0, 30 s, 0 erros
FiniteStateEncodingAxiomProbe.lean    exit 0,  3 s, 0 erros
```

### Unchanged

- **Zero alteracao material.** A estrutura, as duas leis, a construcao
  unica, os dois pontos de transporte, `tableIndex_val` por `rfl`,
  `tableIndex_semiconj` como principal, a soundness terminando em `S`, a
  completeness sem pre-condicoes — tudo permanece exatamente como a
  revisao congelou. `20` lacunas e `21` claims intactas.
- Pegada axiomatica reconfirmada, identica: `encode_injective` e
  `encodedStep` **sem axioma nenhum**; primeira aparicao de
  `Classical.choice` em `buildTransitionTable`.

### Ruled

- Nova regra de governanca: **experimentos negativos nao compartilham
  arquivo com probes obrigatorios**. Validacao obrigatoria termina com
  codigo de saida zero. Um processo Lean com `exit 1` nunca eh evidencia
  de `PASS`.

### Restored

- A autorizacao `ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED`
  esteve **suspensa** entre `751cef8` e este commit — presente no
  allowlist, nao executavel. Volta a ser utilizavel apos os dois `exit 0`.
  **Nenhuma entrada nova** foi adicionada ao allowlist.


## ENG-FINITE-STATE-ENCODING-001-SPECIFICATION-REVIEW - 2026-08-01

### Decided

- **`encode_decode` fica** — e a auditoria mostrou por que **nao** era o
  motivo suposto. O probe contem uma seccao `WeakEncoding` com apenas
  `decode_encode`, e nela a cadeia inteira, ate a soundness tipada,
  **compila**. Logo `encode_decode` nao eh dependencia de prova de nenhum
  resultado CORE: ela eh o **contrato publico** de que todo indice de
  `Fin n` eh um estado real e a tabela representa exatamente o sistema.
- **`encodedStep` eh `PUBLIC_EXECUTABLE_CORE`**, com justificativa nova: a
  revisao tornou `buildTransitionTable_getElem` interno, e sem ele
  `encodedStep` passa a ser o unico nome publico capaz de descrever o
  conteudo da tabela.
- **`ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT`.**

### Measured

- `encode_injective`, `encode_surjective` e `encodedStep` **nao dependem
  de axioma nenhum**. A primeira declaracao a carregar
  `[propext, Classical.choice, Quot.sound]` eh `buildTransitionTable`,
  pelo campo `closed` via `Array.getElem_ofFn`. Isto **corrige** a
  afirmacao de pegada uniforme feita na especificacao.
- Rota leve tentada e **medida como inviavel**:
  `(Array.ofFn f).size = n := rfl` falha com *"Not a definitional
  equality"* para `n` generico, e passa apenas com tamanho literal.
- Argumento decisivo: `analyzeTransitionTable` **ja carrega os tres
  axiomas**. Uma prova de `closed` mais leve nao mudaria nada a jusante.

### Corrected

- `tableIndex_semiconj` passa a **teorema semantico principal**, provado
  diretamente; `table_step_commutes` passa a `PUBLIC_COROLLARY`, um
  `.symm` de uma linha. A especificacao previa o inverso.
- `buildTransitionTable_getElem` passa a `INTERNAL_HELPER`.
- `tableIndex_val` recebe `@[simp]`.
- Declaracoes movidas para o namespace `CertifiedFiniteEncoding`.
- Declaracoes publicas: `16 -> 14`.

### Bounded

- Novo `ENC-GAP-020` e `STOP-ENC-019`: **nao** se afirma invariancia do
  witness concreto sob recodificacao. Medido: `#[1,2,3,2]` contra
  `#[1,0,1,2]`; os witnesses coincidiram em `⟨2,2⟩` — **coincidencia
  observada, nao teorema**.

### Locked

- `specification_status: APPROVED`;
  `authorized_action: ENG_FINITE_STATE_ENCODING_001_FORMALIZATION_AUTHORIZED`.
  Uma entrada literal, sem wildcard. `0` arquivos Lean permanentes, `0`
  provas permanentes, `lake build` **nao** executado, `21` claims intactas.


## ENG-FINITE-STATE-ENCODING-001-SPECIFICATION - 2026-08-01

### Specified

- **A ponte que faltava**: de um sistema Lean tipado ate um certificado
  interpretado NESSE sistema. `16` declaracoes publicas planejadas, `13`
  resultados CORE, `29` documentos, `19` lacunas, `18` stop conditions.
- O consumidor fornece `CertifiedFiniteEncoding S n`, `stepS : S -> S` e
  `start : S`. **Zero typeclasses** — sem `Fintype`, sem `DecidableEq`,
  sem `Nonempty`, sem `Inhabited`.

### Proved in probe

- **Os treze resultados CORE compilaram**, nao apenas foram planejados.
  Dois probes descartaveis, ambos exit `0`, ambos removidos.
- A soundness termina em **igualdade sobre `S`**:
  `stepS^[b+p] start = stepS^[b] start`. Tres linhas de prova.
- A completeness **nao exige pre-condicao nenhuma** do consumidor: a
  validade e o dominio sao consequencias da construcao.
- `table_iterate_commutes` eh **um termo de uma linha** via
  `Function.Semiconj.iterate_right` — contra a inducao com dois `show` que
  o resultado analogo custou na frente anterior.

### Frozen

- **Dois** pontos de transporte `Fin n` ↔ `Fin table.next.size`, e apenas
  dois: `tableIndex` e `buildTransitionTable_getElem`.
- `tableIndex_val` — o teorema **anti-correcao** desta frente — eh `rfl`:
  o cast nao modifica o indice natural.
- Orientacao unica do tamanho: `size = n`.
- `decode_encode` eh a lei da comutacao; `encode_decode` nao se aplica ali.

### Measured

- Achado tecnico central: `Array.size_ofFn` e `Array.getElem_ofFn` sao
  aceitos **em modo termo** por defeq, e **rejeitados** por `rw`/`simp`,
  que trabalham em transparencia reduzida. Quatro rotas testadas; a que
  passou foi o termo puro.
- `ENC-TEST-006`: com a codificacao permutada `i ↦ 3 - i`, a tabela muda
  de `#[1,2,3,2]` para `#[1,0,1,2]` e o witness **permanece** `⟨2,2⟩`.

### Bounded

- `relationship_to_RT_GAP_017: ADDRESSED_FOR_CERTIFIED_TYPED_SYSTEMS_ONLY`.
  `RT-GAP-017` **nao** foi alterado retroativamente e o caso externo geral
  segue `OPEN`.
- Precisao de linguagem congelada: um erro de codificacao **nao** torna
  falso o certificado sobre a tabela; ele apenas impede que o certificado
  sustente uma conclusao sobre o sistema pretendido.

### Locked

- `authorized_action: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_AUTHORIZED`.
  Uma entrada literal, sem wildcard. `0` arquivos Lean permanentes, `0`
  provas permanentes, `lake build` **nao** executado, `21` claims
  intactas.


## PORTFOLIO-REVIEW-AFTER-RUNTIME-ADAPTER - 2026-08-01

### Selected

- **`ENG-FINITE-STATE-ENCODING-001`**, codificacao certificada de estados
  e construcao da tabela. Seis alternativas comparadas; as dez condicoes
  da regra de decisao verificadas uma a uma, **dez de dez**.

### Diagnosed

- A proxima limitacao **nao** eh desempenho, CLI nem JSON. Eh `RT-GAP-017`:
  a tabela eh analisada corretamente, mas nada prova que ela representa o
  sistema que a originou. Extrair e empacotar amplificaria esse buraco em
  vez de fecha-lo.

### Measured

- `Array.ofFn` eh **computavel**, sai com `[propext]` e produz dado sob
  `#eval`. `Array.size_ofFn` e `Array.getElem_ofFn` existem no core.
- **`Function.Semiconj.iterate_right`** existe com axiomas `[propext]` e a
  forma exata `Semiconj f ga gb -> forall n, Semiconj f ga^[n] gb^[n]`. A
  comutacao de iteradas vira corolario de uma linha.
- **`Fintype.equivFin` eh `noncomputable`.** A codificacao tera de ser
  **recebida**, nunca derivada — vira `STOP-ENC-006`.

### Bounded

- Uma codificacao certificada prova correspondencia entre um sistema
  **tipado** e sua tabela. Ela **nao** prova que um sistema fisico,
  servico, workflow ou programa real foi modelado corretamente.
  `RT-GAP-017` sera fechado **apenas** no recorte tipado.

### Locked

- `authorized_action: ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
  Uma unica entrada literal no allowlist, sem wildcard. Formalizacao,
  extracao, CLI e integracao seguem **NAO autorizadas**; todos os
  `extension_status: NOT_AUTHORIZED` preservados.


## ENG-FINITE-STATE-RUNTIME-001-RESULT-REVIEW - 2026-08-01

### Closed

- **A primeira cadeia completa do laboratorio que comeca em um dado de
  runtime potencialmente invalido e termina em um certificado formal de
  repeticao sobre esse mesmo dado** foi revisada e encerrada. `12`
  documentos de fechamento; `53` documentos na frente; **zero** modulos
  matematicos tocados e **zero** teoremas novos.

### Fixed

- `GAP_REGISTER.yaml`: `resolved_formally` `10 -> 11` e `open_deferred`
  `8 -> 7`. Estritamente documental — nenhum status individual, nenhuma
  claim, nenhuma forca de resultado. O cabecalho passou a ser
  **verificado por script** contra as entradas.

### Audited

- `destinos invalidos sao REJEITADOS, nunca corrigidos`: busca por `%`,
  `mod`, `clamp`, `min`, `max`, `getD` e `fallback` deu **zero no
  codigo**. Os dois teoremas que tornam isso impossivel de esconder sao
  `validateTransitionTable_sound` e o **anti-clamp**
  `validateStart_sound`.
- A ponte `run?_eq_iterate_step` foi auditada linha por linha:
  quantificador **no enunciado**, `Function.iterate_succ_apply`, nenhuma
  orientacao inversa, coercoes explicitas, `[propext, Quot.sound]`.
- `analyzeTransitionTable_sound`: zero `cast`, zero `Eq.ndrec`, zero
  transporte dependente, zero hipoteses extras do consumidor.
- Precedencia medida: `analyzeTransitionTable ⟨#[1]⟩ 100` devolve
  `transitionDestinationOutOfBounds` — o erro de **tabela** vence.

### Covered

- Novo `EngFiniteStateRuntime001UmbrellaAudit.lean` importa **apenas**
  `TamesisLab` e referencia as `29` declaracoes por nome totalmente
  qualificado. Exit `0`, `87` s. Nao registrado na raiz: importa-a, e
  registra-lo criaria ciclo (`RT-GAP-018`).

### Deviated

- `DOC-RT-001`, `NAME_COLLISION_AVOIDED`: `COMPUTABILITY_REVIEW.md` ja
  existia desde `6c3b837`. O conteudo de resultado foi para
  `FINAL_COMPUTABILITY_REVIEW.md`, no padrao `FINAL_*` da propria frente,
  e o original foi restaurado. **Zero documentos preexistentes apagados.**

### Locked

- `result_review: APPROVED`; extracao, CLI, formato externo, integracao
  e diagnostico detalhado em `NOT_AUTHORIZED`;
  `external_abstraction_correctness: DEFERRED`;
  `authorized_action: PORTFOLIO_REVIEW_REQUIRED` — **trava**, nao
  autorizacao. Nenhuma entrada nova no allowlist.


## ENG-FINITE-STATE-RUNTIME-001-FORMALIZATION - 2026-08-01

### Built

- **A primeira API do laboratorio que aceita diretamente uma estrutura de
  dados dinamica** e preserva uma cadeia formal completa ate o
  certificado. `2` estruturas, `1` indutivo, `9` definicoes, `1`
  instancia, `18` teoremas, `869` linhas.
- **As duas obrigacoes sem evidencia — `analyzeTransitionTable_sound` e
  `_complete` — compilaram na PRIMEIRA tentativa**, junto com os outros
  cinco modulos. A revisao ja havia demonstrado as demais em ambiente
  descartavel e registrado os padroes que funcionam.

### Key move

- O auxiliar privado `analyze_reduce` isola de uma vez as duas reducoes
  que a notacao `do` esconde. Soundness ficou com **sete** linhas;
  completeness, com **quatro**.
- **Nenhum transporte dependente.** A tabela concreta `⟨raw.next, hRaw⟩`
  tem `next` sintaticamente igual a `raw.next`, e seu `toRaw` eh
  definicionalmente `raw` por eta. Zero `cast`, zero `Eq.ndrec`.

### Layered

```text
camada 0   Raw, Valid, step?, run?     nenhuma typeclass
camada 1   validacoes                  nenhuma typeclass
camada 2   step e pontes               nenhuma typeclass
camada 3   detectCycle?                Fintype/DecidableEq INFERIDAS
camada 4   analyzeTransitionTable      nenhuma do chamador
```

O consumidor fornece `Array Nat` e `Nat`. **Nada mais.**

### Axioms

- **`step?` e `run?` nao dependem de axioma nenhum.** Toda a camada de
  validacao e `run?_eq_iterate_step` ficam em `[propext, Quot.sound]` —
  **sem `Classical.choice`**. A pegada entra exatamente onde o detector
  entra, por `Fintype.card`. `sorryAx`: **0**.

### Enforced

- **Destinos invalidos sao REJEITADOS, nunca corrigidos.**
  `validateTransitionTable_sound` forca a tabela devolvida a ser a mesma;
  `validateStart_sound` — o teorema **anti-clamp** — forca o indice a ter
  o valor pedido. Correcoes silenciosas no codigo: **0**.
- **Precedencia dos erros provada e medida**:
  `analyzeTransitionTable ⟨#[1]⟩ 100 -> transitionDestinationOutOfBounds`
  — tabela invalida **e** inicio invalido, e o erro de tabela vence.
- `internalDetectorFailure` permanece na funcao executavel, com sua
  impossibilidade provada. **O detector anterior NAO foi totalizado.**

### Reused, not reproved

- `detectCycleWitness?`, `_sound` e `_complete` — os dois teoremas sao
  **termos de uma linha**. `cycleCandidates`, pigeonhole e colisao
  limitada: **0** mencoes. Quinta frente a consumir a casa dos pombos
  atraves do teorema original.

### Validated

- Tres testes `exit 0` com **zero** erros; `DynamicAnalysis.lean` isolado
  `exit 0`; **`lake build` PASS, 8748 jobs** (era 8737 — os seis modulos,
  o `Audit`, os dois agregadores e os tres testes). A raiz alcanca
  `TamesisLab.Engineering`.
- Dez casos executaveis, **22** teoremas de regressao, sem
  `native_decide`. Os quatro que produzem certificado reproduzem, em
  forma de tabela, os modelos `Fin 1`, `Bool`, `Fin 3` e `Fin 4` ja
  verificados no detector.

### Not done

- **0** CLI, parser, JSON, CSV, rede, extracao, integracao, diagnostico
  detalhado, Floyd, Brent ou tabela visitada. **0** legado, **0**
  arquivos matematicos das quatro frentes anteriores.

### Claimed

- Uma claim, a vigesima primeira:
  `FINITE-STATE-RUNTIME-ADAPTER-FORMAL-001`, `VERIFIED`,
  `evidence_level F`, novidade matematica e algoritmica **NONE**.

### Result

- `ENG_FINITE_STATE_RUNTIME_001_FORMALIZATION_VERIFIED`. Onze lacunas
  resolvidas formalmente, oito diferidas, uma bibliografica.

## ENG-FINITE-STATE-RUNTIME-001-SPECIFICATION-REVIEW - 2026-08-01

### Demonstrated

- **O teorema central FECHA.** O probe descartavel compilou com **zero
  erros**, incluindo `run?_eq_iterate_step`, `step?_eq_some_step`,
  `detectCycle?_raw_repeat` e os dois teoremas de precedencia de erro.
  Era essa a condicao de aprovacao do gate.
- `run?_eq_iterate_step` depende de **`[propext, Quot.sound]`** — sem
  `Classical.choice`.

### Frozen

Tres detalhes da prova central:

1. **a generalizacao vem do ENUNCIADO**, com `∀ start` depois de `k`;
   `generalizing` NAO eh usado;
2. **dois `show` sao obrigatorios** — o primeiro expoe o `bind` escondido
   pela notacao `do`, o segundo forca a reducao de
   `Option.bind (some a) f`;
3. a variante correta eh **`Function.iterate_succ_apply`**, nao a linha.

Precedencia dos erros congelada e **medida**:
`analyzeT #[1] com start 100 -> transitionDestinationOutOfBounds` — tabela
invalida **e** inicio invalido, e o erro de **tabela** vence.

Coercoes `Fin`/`Nat` explicitas em todos os enunciados publicos.

### Found

- **As provas de precedencia exigem `show`.** Tres abordagens falham e
  ficam registradas: `simp [..., Except.bind]`, `split`, e
  `simp only [...]; simp [hStart]`. Motivo: apos `dif_pos`, a condicao usa
  `validated` ainda ligado pelo `do`, e o campo projetado eh *defeq* mas
  nao sintaticamente igual a `raw.next.size`.
- **Correcao a auditoria anterior**: `Array.getElem?` nao existe como
  constante (confirmado), mas `getElem?_pos` e
  `Array.getElem?_eq_getElem` **existem** como lemas; `getElem?_pos` foi
  o usado.
- **As duas camadas de validacao e o teorema central nao dependem de
  `Classical.choice`** — a pegada so entra onde o detector entra.

### Remaining risk

- `analyzeTransitionTable_sound` e `_complete` foram **planejadas**, nao
  demonstradas no probe. Sao as duas unicas obrigacoes centrais sem
  evidencia executavel. Mitigacao registrada: trabalhar com a tabela
  concreta para evitar transporte dependente.

### Not done

- **0** arquivos Lean no repositorio, **0** provas, **0** implementacao
  permanente, **0** `lake build`, **0** claims (ledger em **20**), **0**
  legado, **0** matematicos das tres fundacoes. Probe **removido**.
  Nenhum diretorio renomeado — a duplicacao de prefixo `03_` fica
  `ACKNOWLEDGED_COSMETIC`.

### Result

- `ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_REVIEW_APPROVED`.
  Vinte e cinco declaracoes publicas congeladas; 22 lacunas, nenhuma
  fechada por expectativa.

## ENG-FINITE-STATE-RUNTIME-001-SPECIFICATION - 2026-08-01

### Frozen

```text
entrada bruta        Array Nat
tabela vazia         estruturalmente valida
destino invalido     erro, NUNCA modulo/clamp/fallback
resultado dinamico   Except RuntimeCycleError CycleWitness
```

- `RawTransitionTable` com **um** campo; `size`, `stateCount`, `proof`,
  `start` e `fallback` rejeitados.
- `Valid` na formulacao por `Fin`, decidivel, com as outras duas
  auditadas e **nao** adotadas — sem tres predicados concorrentes.
- `ValidatedTransitionTable` como **estrutura nomeada**, nao `Subtype`.
- `RuntimeCycleError` com tres construtores; erro de **tabela** e erro de
  **consulta** NAO colapsados.

### Probed

- Versao **descartavel** do pipeline inteiro escrita, executada e
  removida. **Treze casos avaliados, todos com o resultado previsto.**
- Os quatro que produzem certificado reproduzem **exatamente** os modelos
  `Fin 1`, `Bool`, `Fin 3` e `Fin 4` ja verificados no detector — um
  **oraculo independente**.
- `step_val` fecha por `rfl`; a instancia decidivel foi sintetizada;
  `run?` devolveu `none` no acesso fora do array, sem fallback.

### Decided

Quatro pontos que o gate deixou em aberto:

1. **`stateCount` NAO sera criado** — duplicaria `next.size`.
2. **`toRaw` sera publico** — eh a unica forma de enunciar os dois
   teoremas centrais, que falam da tabela original.
3. **`step?_eq_some_step` eh `CORE`** — a inducao depende dele.
4. **A variante de iteracao eh `Function.iterate_succ_apply`**, nao a
   linha: `run?` aplica um passo e recorre, logo a contagem externa
   consome o passo **interno**. Auditado, nao presumido.

### Audited

- **20 APIs confirmadas**, 3 `NOT_FOUND` (`Array.get`, `Array.getElem?`,
  `Array.size_toArray` — ausencias de NOME; a notacao `xs[i]` e `xs[i]?`
  funciona), 4 `NOT_NEEDED`.
- **`#print axioms validateT` -> `[propext, Quot.sound]`**: a camada de
  validacao, isolada, **nao** depende de `Classical.choice`.

### Binding

- **Nao corrigir destinos invalidos.** `validateStart_sound` — preservacao
  exata do `start` — eh o teorema **anti-clamp**.
- O consumidor fornece `Array Nat` e `Nat`. **Zero** typeclasses.
- `Option` preservado internamente; o `none` vira
  `internalDetectorFailure`, ramo defensivo que a correcao prova
  impossivel. **Nao totaliza** o detector anterior.
- Converter um sistema real em tabela finita eh uma **abstracao** cuja
  correcao esta frente **nao** fornece (`RT-GAP-017`).

### Risk

- `run?_eq_iterate_step` eh o **unico** teorema da frente cuja prova nao
  eh mecanica. A revisao deve olha-lo primeiro.

### Not done

- **0** arquivos Lean, **0** provas, **0** adaptador, **0** executavel,
  **0** `lake build`, **0** claims (ledger em **20**), **0** legado, **0**
  arquivos matematicos das tres fundacoes encerradas. Probe **removido**.

### Result

- `ENG_FINITE_STATE_RUNTIME_001_SPECIFICATION_READY`. Vinte e cinco
  documentos, vinte e duas lacunas, nove testes, doze teoremas `CORE`.

## PORTFOLIO-REVIEW-FINITE-STATE-RUNTIME - 2026-08-01

### Selected

- **`ENG-FINITE-STATE-RUNTIME-001`** — *Certified Runtime Adapter for
  Finite Deterministic Systems*, criado como `SCOPED` na nova track
  `engineering_foundation`.
- **A lacuna**: o laboratorio tem um programa verificado que **nao
  consegue receber uma entrada**. O detector opera sobre `X : Type*` com
  `[Fintype X]` e `[DecidableEq X]` definidos em **compilacao**; os cinco
  modelos de teste estao escritos no fonte.

### Compared

- **Seis alternativas.** `A` totalizacao
  `DEFERRED_LOW_INCREMENTAL_VALUE` — em camada dinamica, `Option` eh o
  **menor** dos problemas; o erro real a reportar eh "tabela invalida".
  `B` Floyd e `C` Brent `DEFERRED_PREMATURE_OPTIMIZATION`. `D` extracao
  isolada `INSUFFICIENT_RUNTIME_VALUE` — o binario responderia apenas
  sobre os cinco modelos ja escritos. `E` infraestrutura de testes
  `P2_LAB_INFRASTRUCTURE`, registrada em `RT-GAP-018`, sem bloqueio real.
  `F` adaptador **`SELECTED`**: unica das seis que muda o que o
  laboratorio **consegue fazer**.
- **Duplicata: NAO encontrada.** Zero itens `ENG-`; zero ocorrencias de
  `RawTransitionTable`, `TransitionTable` ou `RUNTIME-001`; zero `Array`
  no nucleo. As mencoes a "adaptador" sao o adaptador de componente
  (`CD-GAP-012`) ou a classificacao `REQUIRES_ADAPTER` — que **descreve**
  a lacuna a fechar.

### Scoped, not frozen

- `RawTransitionTable` com **um** campo `next : Array Nat` — sem `size`,
  derivavel, mesma disciplina que rejeitou `entryPoint`.
- Validacao por `Except` com erros tipados e **tres** validacoes
  separadas: tabela, consulta, execucao. Nunca um unico `Bool`.
- `iterate_step_corresponds` sera o **principal resultado formal**: sem
  ela o certificado fala de um objeto que ninguem relaciona com a entrada.
- **21 lacunas** abertas, **8** testes planejados, **7** resultados
  candidatos. Nada congelado.

### Binding prohibition

- **Nao corrigir destinos invalidos por modulo, clamp ou fallback.** Um
  `% n` silencioso transformaria uma tabela errada em um **sistema
  diferente**, e o certificado seria correto sobre um sistema que o
  usuario nunca descreveu.
- **Converter um sistema real em tabela finita eh uma ABSTRACAO**, cuja
  correcao o adaptador **nao** fornece (`RT-GAP-017`).

### Governance

- Tres edicoes minimas e literais em `labctl.py`, sem wildcard:
  `DEC-020` (gate sequence), `DEC-021` (**pre-condicao dupla** —
  `VERIFIED` **e** `result_review APPROVED`, a primeira do laboratorio a
  exigir duas propriedades) e `DEC-022` (allowlist).
- Regras de governanca gravadas no `LAB_STATE.md`:
  `GATE_POST_COMMIT_VALIDATION_FAILED` e a proibicao de assumir sucesso a
  partir de saida truncada.
- `canonical_commit`: `d9d672c` -> `a4907b7`.

### Not done

- **0** arquivos Lean, **0** provas, **0** adaptador, **0** executavel,
  **0** `lake build`, **0** claims (ledger em **20**), **0** legado, **0**
  arquivos matematicos das tres fundacoes encerradas e de `RH-NOGO-001`.
  Pasta de especificacao **nao** criada.

### Result

- `PORTFOLIO_REVIEW_APPROVED_FINITE_STATE_RUNTIME_SELECTED`.

## FOUND-CYCLE-DETECTION-001-RESULT-REVIEW - 2026-08-01

### Reviewed

- **`CDR-001` a `CDR-011`: todos CONFIRMADOS**, conferidos contra o fonte.
  `Valid` coincide termo a termo com a conclusao de
  `exists_bounded_iterate_collision`; a soundness NAO depende de
  `mem_cycleCandidates_iff`; as tres pontes tem uma linha cada e nao
  exigem `DecidableEq`.
- Semantica **medida**: a busca por `baseIndex` associado a "minimo" ou
  "menor" retornou **zero**; `minimalPeriod` aparece em tres linhas, todas
  documentais e todas **negando** a identificacao.
- `List.find?` devolve o **primeiro** aceito segundo a ordem concreta —
  isso **nao** eh o menor certificado segundo ordem matematica provada.
  **Zero** teoremas de minimalidade.

### Audited

- **API publica: 13 declaracoes** classificadas — 3
  `PUBLIC_EXECUTABLE_CORE`, 4 `PUBLIC_SPECIFICATION_CORE`, 5
  `PUBLIC_COROLLARY`, 1 `INSTANCE_SUPPORT`. Zero `INTERNAL_HELPER`.
- **Instancias: 1 declarada, 3 derivadas, 0 conflitos.** Nenhuma instancia
  global de `DecidableEq X` — o detector a **recebe**, nao a fabrica.
- **Cobertura dos agregadores verificada sobre o conteudo COMMITTADO**,
  com `git show HEAD:`. Evidencia quantitativa: **8727 -> 8737 jobs**.

### Found and fixed

- **Import circular.** Registrar os dois testes de auditoria dentro de
  `TamesisLab.lean` cria ciclo, pois eles importam a raiz. O `lake build`
  falhou; o registro foi removido. Consequencia registrada: os tres testes
  originais entram no build; os dois de auditoria **nao** entram e sao
  executados explicitamente.

### Governance

- **`GOV-CD-001: ACKNOWLEDGED_NON_MATERIAL`.** Sete fatos verificados por
  comando: o commit `61630fb` **nao** foi publicado (0 branches remotos
  contendo o HEAD), **0** branches, tags e refs o contem, o HEAD final
  contem os dois agregadores, o build cobre a frente, a arvore ficou
  limpa, os artefatos registraram o desvio e o estado matematico eh
  consistente. O `diff` do amend: cinco linhas de `import` e documentacao
  — **nenhum modulo matematico**.
- O desvio **foi** um desvio; a classificacao diz que o dano eh nulo, nao
  que a regra foi cumprida.
- **Regra normativa futura**: quando uma auditoria obrigatoria falhar
  depois do commit e amend e commit corretivo estiverem ambos proibidos,
  parar com `GATE_POST_COMMIT_VALIDATION_FAILED`. O historico atual
  **nao** foi alterado para satisfaze-la.
- **Causa raiz**: assumir sucesso a partir de saida truncada. Duas medidas
  preventivas saem daqui.

### Closed

- **19 lacunas: 10 resolvidas, 9 abertas**, nenhuma fechada por
  expectativa. Matriz de reutilizacao: 2 `DIRECT_REUSE`, 6
  `REQUIRES_ADAPTER`, 2 `CONCEPTUAL_ONLY`, separando uso no Lean, apos
  extracao e em sistemas reais.
- `result_review: APPROVED`; `totalization`, `extraction`, `optimization`
  e `minimality` todos **nao autorizados**; trava final
  `PORTFOLIO_REVIEW_REQUIRED`.

### Not done

- **0** teoremas novos, **0** modulos matematicos alterados, **0**
  alteracoes no detector, **0** claims novas (ledger em **20**), **0**
  legado, **0** de `RH-NOGO-001`, **0** matematicos das duas fundacoes
  anteriores. **Nenhum `commit --amend`.**

### Result

- `FOUND_CYCLE_DETECTION_001_RESULT_REVIEW_APPROVED`. A primeira fundacao
  algoritmica executavel do laboratorio fica encerrada.

## FOUND-CYCLE-DETECTION-001-FORMALIZATION - 2026-08-01

### Built

- **O primeiro programa executavel verificado do laboratorio.**
  `1` estrutura, `3` definicoes, `1` instancia, `8` teoremas, `609`
  linhas, em `TamesisLab/Foundations/CycleDetection/`.
- `detectCycleWitness?` devolve `Option CycleWitness` por busca limitada
  sobre `cycleCandidates (Fintype.card X)`, com `soundness` e
  `completeness` provadas.

### Layered

```text
camada 0   cycleCandidates, mem_cycleCandidates_iff   sem Fintype, sem DecidableEq
camada 1   CycleWitness.Valid                         Fintype, SEM DecidableEq
camada 2   detectCycleWitness?, _sound, _complete     Fintype e DecidableEq
camada 3   isPeriodicPt, mem_periodicPts, propagates  SEM DecidableEq
```

`DecidableEq X` entra em **uma unica definicao** e nao vaza para resultado
proposicional algum.

### Reused, not reproved

- Os tres teoremas de `Periodicity.lean` tem **uma linha de prova cada**:
  `periodic_tail_of_collision`, `Function.mk_mem_periodicPts` e
  `collision_propagates`.
- A completude eh **transporte** de `exists_bounded_iterate_collision`,
  cuja conclusao coincide termo a termo com `Valid`.
- **Casa dos pombos NAO repetida**: contagem `grep` zero em toda a frente.
  `Function.iterate_add_apply` nao aparece.

### Two frictions

- `List.find?_some` falhou por unificacao de ordem superior — Lean
  escolhia `@decide (Valid f x w)` como funcao **constante**. Resolvido
  passando o predicado explicitamente.
- As auditorias de tokens e imports encontravam as **proprias mencoes
  documentais** nas docstrings. Movidas para `COMPUTABILITY_RESULT.md`,
  fora do Lean. As quatro auditorias passaram a **zero**.

### Executed

- Cinco modelos avaliados por `#eval` **e** provados por `decide`, sem
  `native_decide`: `Fin 1` id, `Bool` id, `Bool` not, `Fin 3` cauda,
  `Fin 4` cauda e ciclo de dois. **Catorze** teoremas de regressao.
- Dois exemplos fecham o ciclo entre execucao e prova: soundness aplicada
  a um resultado obtido por `decide`, e `mem_periodicPts` sobre ele.

### Axioms

- `cycleCandidates` **nao depende de axioma algum** — eh o unico objeto
  que nao menciona `Fintype`, confirmando a origem da pegada em
  `Fintype.card` e `Finset.univ`. Os demais listam `propext`,
  `Classical.choice` e `Quot.sound`. `sorryAx`: **0**.
- Registro vinculante: **pegada axiomatica nao eh nao-computabilidade**.

### Omitted on purpose

- `detected_cycle_is_component_cycle` **nao** formalizado — adaptador
  mecanico; dispensa o import de `FunctionalGraphs` (`CD-GAP-012`).
- Funcao total **nao** formalizada; API garantida permanece
  `Option CycleWitness`, sem valor padrao falso (`CD-GAP-017`).
- Floyd, Brent, tabela visitada, minimalidade, complexidade, extracao e
  integracao: **nada implementado**.

### Validated

- Tres testes isolados `exit 0`; `lake build` **PASS, 8737 jobs** —
  contra 8727 antes de registrar a frente em
  `TamesisLab/Foundations.lean` e `TamesisLab.lean`;
  `pytest` PASS; `labctl validate` PASS. Nenhum teste removido, nenhum
  modulo anterior alterado.

### Claimed

- Uma claim, a vigesima: `EXECUTABLE-CYCLE-WITNESS-FORMAL-001`,
  `VERIFIED`, `evidence_level F`, novidade matematica e algoritmica
  **NONE**.

### Result

- `FOUND_CYCLE_DETECTION_001_FORMALIZATION_VERIFIED`. Dez lacunas
  resolvidas, sete diferidas, uma bibliografica, uma pronta para auditoria
  de viabilidade.

## FOUND-CYCLE-DETECTION-001-SPECIFICATION-REVIEW - 2026-07-31

### Renamed

- **`prefixIndex` -> `baseIndex`**, 40 ocorrencias em 8 documentos.
  `baseIndex` eh o **indice-base da igualdade**
  `f^[baseIndex + period] x = f^[baseIndex] x`, e nao o menor indice de
  entrada. Nomes proibidos: `prefixIndex`, `entryIndex`, `tailLength`,
  `cycleEntry`.
- **Registros historicos NAO foram reescritos.** O JSON do gate anterior,
  sua sessao e o changelog preservam `prefixIndex`; a decisao esta
  marcada como **superada** em `DATA_MODEL.md` e na tabela de
  renomeacoes. A governanca viva foi atualizada.

### Measured

- Probe descartavel em `/tmp`, 28 s, **zero erros**, removido ao final.
- **Os cinco casos obrigatorios bateram**: `Fin 1` id -> `<0,1>`;
  `Bool` id -> `<0,1>`; `Bool` not -> `<0,2>`; `Fin 3` cauda -> `<2,1>`;
  `Fin 4` cauda e ciclo de dois -> `<2,2>`. Nenhuma funcao e nenhuma
  ordem foi alterada para satisfazer expectativa.
- Enumeracao: `cycleCandidates 0 = []` e `1 = [<0,1>]` por `rfl`;
  comprimentos 6, 10 e 15 para n = 3, 4 e 5; fronteira de soma medida por
  filtro.

### Findings

- **A instancia `Decidable` precisa ser DECLARADA.** `Valid` eh um `def`
  e a resolucao de instancias nao o desdobra; sem
  `CycleWitness.decidableValid` o `decide` nao elabora. Ausente da
  especificacao inicial; acrescentada as assinaturas congeladas.
- **Pegada axiomatica NAO eh noncomputabilidade.**
  `detectCycleWitness?` carrega `[propext, Classical.choice, Quot.sound]`
  — origem localizada em `Fintype.card` e `Finset.univ`. `cycleCandidates`,
  `List.range`, `find?` e `Nat.iterate` nao dependem de axioma algum.
  Criterio reformulado: nao `noncomputable`, `#eval` funciona, nenhum
  `Classical.choose` produzindo dado. Os tres confirmados.
- **`ValidAt` nao resolveria** a pegada: o detector calcula
  `Fintype.card X` de qualquer modo. Permanece `DEFERRED`.
- `propagates` **alinhada** a ordem de argumentos de
  `collision_propagates`: hipotese primeiro, `k` depois.
- Rota unica de completude: `List.find?_isSome` + `Option.isSome_iff_exists`.

### Frozen

- `CycleWitness` com dois naturais; `Valid`; `cycleCandidates`;
  `mem_cycleCandidates_iff`; `detectCycleWitness?`; soundness;
  completeness; as tres pontes proposicionais. Doze assinaturas publicas
  mais uma instancia.
- `total_wrapper: DEFERRED`, `OPTIONAL_CORE_PENDING_EXECUTION_TEST`. Seis
  dos sete criterios confirmados; o setimo exigiria provar a completude no
  probe. API v1 permanece `Option`. `getD` com certificado falso
  **proibido**.

### Not done

- **0** arquivos Lean no repositorio, **0** provas, **0** implementacao
  permanente, **0** `lake build`, **0** claims (ledger em **19**), **0**
  legado, **0** de `RH-NOGO-001`, **0** matematicos das duas fundacoes
  encerradas. Probe **removido**.

### Changed

- `canonical_commit`: `ab79032` -> `03e1ec3`.
- `specification_status` -> `APPROVED`.
- `authorized_action` -> `FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED`
  (`DEC-018`, uma entrada literal, sem wildcard).

### Result

- `FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED`. Dezenove
  lacunas reclassificadas: 6 resolvidas, 5 prontas para formalizacao, 1
  para auditoria de viabilidade, 6 diferidas, 1 bibliografica.

## FOUND-CYCLE-DETECTION-001-SPECIFICATION - 2026-07-31

### Frozen

- **`BOUNDED_CERTIFICATE_SEARCH`** como algoritmo primario. **Nao eh
  Floyd.** O argumento decisivo: o contrato do certificado coincide
  TERMO A TERMO com a conclusao de `exists_bounded_iterate_collision`,
  ja `VERIFIED`. A completude deixa de ser prova nova e passa a ser
  transporte.
- **`CycleWitness`** com **dois** naturais, `prefixIndex` e `period`.
  `entryPoint` **rejeitado** — derivavel por `f^[prefixIndex] x0`. A
  estrutura NAO eh parametrizada por `X`.
- Semantica vinculante: `prefixIndex` eh **indice-base de colisao
  certificada**, NAO o menor indice de entrada — o nome `entryIndex` fica
  proibido. `period` eh **periodo positivo testemunhado**, NAO
  `minimalPeriod`.

### Audited

- **31 APIs confirmadas** com assinatura impressa pelo proprio Lean, via
  sonda temporaria em `/tmp` (removida ao final). **Dois nomes do gate
  divergiam do checkout**: `List.find?_eq_some` ->
  `List.find?_eq_some_iff_append`; `Function.iterate` -> `Nat.iterate`.
  `List.get?` e `List.getElem?` **nao existem** como constantes.
- Fronteira `mu + lam = n` verificada **por avaliacao**: `n = 3` produz
  `(0,3), (1,2), (2,1)`; `n = 1` produz `[(0,1)]`.
- Predicado executavel: **Opcao A**, `decide`. A instancia `Decidable` da
  conjuncao completa foi obtida por `inferInstance` para `X = Bool`.
  `Bool` e `Prop` **nao** ficam congelados simultaneamente.

### Deviations

- **`mem_cycleCandidates_iff` NAO eh dependencia da soundness** — as tres
  cotas vivem dentro de `Valid`. Fortificacao, nao lacuna: a soundness
  sobrevive a uma troca de algoritmo. O DAG do gate foi corrigido nesse
  ramo.
- **Totalizacao `DEFERRED`.** Quatro das cinco condicoes tem argumento
  favoravel; a quinta — `#eval` funcionar — so eh verificavel
  implementando. API v1 permanece baseada em `Option`.

### Boundary

- `DecidableEq X` eh sobre **estados**; `periodicOrbit` vive em
  `Cycle X`. Nenhuma decidibilidade sobre `Cycle X` eh assumida.
  `DecidableEq` fica SOMENTE na camada do detector — as tres pontes
  proposicionais nao a recebem.
- Terminacao **estrutural**: lista finita + `List.find?`. Sem `fuel`, sem
  recursao bem fundada, sem `Classical.choice`, sem `Classical.choose`.
- Casa dos pombos consumida **uma unica vez**, em `FOUND-SEMIGROUP-002`;
  `Fintype.exists_ne_map_eq_of_card_lt` NAO aparecera nesta frente.
- `complexity_status: NOT_FORMALIZED`; minimalidade de `mu` e de `lam`
  **nao autorizadas**; `mathematical_novelty` e `algorithmic_novelty`
  ambas `NONE`.

### Not done

- **0** arquivos Lean permanentes, **0** provas, **0** algoritmos
  implementados, **0** `lake build`, **0** claims (ledger em **19**),
  **0** arquivos de legado, **0** de `RH-NOGO-001`, **0** matematicos de
  `FOUND-SEMIGROUP-002` e de `FOUND-FUNCTIONAL-GRAPH-001`. Sonda
  temporaria **removida**.

### Changed

- `canonical_commit`: `49924c3` -> `ab79032`, no preflight.
- `work_status` -> `READY`; `specification_status: READY_FOR_REVIEW`.
- `authorized_action` ->
  `FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_AUTHORIZED`
  (`DEC-017`, uma entrada literal no allowlist, sem wildcard).

### Result

- `FOUND_CYCLE_DETECTION_001_SPECIFICATION_READY`. Vinte e um documentos,
  dezenove lacunas, sete casos de teste, dez teoremas `CORE` e tres
  `OPTIONAL_CORE`.

## PORTFOLIO-REVIEW-CYCLE-DETECTION - 2026-07-31

### Selected

- **`FOUND-CYCLE-DETECTION-001`** — *Executable Cycle Detection for
  Finite Deterministic Systems*, criado como `SCOPED`. Ataca a lacuna
  registrada no fechamento anterior: `periodicOrbit` eh **noncomputavel**,
  e o resultado proposicional nao entrega algoritmo, `mu`, `lambda`,
  ponto de entrada, lista do ciclo nem certificado computavel.
- **Duplicata: NAO encontrada.** Zero ocorrencias de `CYCLE-DETECTION` ou
  `detectCycle`. Floyd e Brent aparecem em tres documentos, e nos tres
  como material declarado **fora de escopo**.

### Audited

- **Seis** itens nao executados reavaliados com os nove campos exigidos.
  Todos rejeitados. `TOE-INTERFACE-001` por motivo estrutural: depende de
  `RH-NOGO-001`, congelada — dependencia **bloqueante**.
- Nenhuma pesquisa matematica das frentes rejeitadas foi iniciada.

### Planned, not built

- Estrutura candidata `CycleDetectionResult` com seis invariantes,
  **nao congelada**.
- Algoritmos comparados: `PRIMARY: FLOYD_WITH_FUEL`,
  `REFERENCE_BASELINE: VISITED_TABLE`, `DEFERRED: BRENT`. **Nenhum
  implementado.**
- Risco principal: **terminacao**. Quatro camadas que a especificacao deve
  manter separadas — terminacao, correcao, complexidade e equivalencia
  com a API proposicional.
- Seis casos de teste (`CD-CE-001..006`) com valores **candidatos**;
  dezesseis lacunas (`CD-GAP-001..016`), **nenhuma fechada**.

### Boundary

- `DecidableEq X` eh sobre **estados**; `periodicOrbit` vive em
  `Cycle X`, e nenhuma decidibilidade sobre `Cycle X` eh assumida,
  requerida ou construida. A ponte eh **proposicional**.
- Minimalidade de `mu` e de `lambda`, complexidade assintotica formal,
  bacia completa e enumeracao global: **nao autorizadas**.
- `mathematical_novelty: NONE`. Deteccao de ciclos em sistemas
  deterministicos finitos eh material classico.

### Governance

- Tres edicoes minimas e literais em `10_TOOLS/labctl.py`, **sem
  wildcard**: `DEC-014` (gate sequence), `DEC-015` (dependencia de
  `FOUND-FUNCTIONAL-GRAPH-001` VERIFIED) e `DEC-016` (entrada de
  allowlist). `PORTFOLIO_REVIEW_AUTHORIZED` ja existia.
- `canonical_commit`: `3f6d7e7` -> `49924c3`, no preflight.
- `authorized_action` ->
  `FOUND_CYCLE_DETECTION_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
  Formalizacao, extracao e integracao permanecem **nao autorizadas**.

### Not done

- **0** arquivos Lean, **0** provas, **0** algoritmos, **0** `lake build`,
  **0** claims promovidas (ledger em **19**), **0** arquivos de legado,
  **0** de `RH-NOGO-001`, **0** matematicos de `FOUND-SEMIGROUP-002` e de
  `FOUND-FUNCTIONAL-GRAPH-001`. Pasta de especificacao **nao** criada.

### Result

- `PORTFOLIO_REVIEW_APPROVED_CYCLE_DETECTION_SELECTED`.

## FOUND-FUNCTIONAL-GRAPH-001-RESULT-REVIEW - 2026-07-31

### Reviewed

- `FGR-001` a `FGR-008`: **todos CONFIRMADOS**. Transitividade revisada
  linha a linha, com o mapa `mx/ny/my/nz` e as testemunhas `(d + mx, nz)`
  e `(mx, d + nz)`.
- **Caso infinito**: `EventuallyMeets` continua relacao de equivalencia
  para tipos infinitos; a existencia de ponto periodico eh FALSA em geral
  (`X = N`, `f n = n + 1`). Nenhum teorema Lean criado para isso.
  `[Fintype X]` aparece SOMENTE em `ComponentCycle.lean`.
- **Caso vazio**: os teoremas recebem `x : X`; com `X` vazio nao existe tal
  termo. Zero hipoteses de `Nonempty`, `Inhabited`, `Finite` ou
  `DecidableEq`.

### Binding caveat

- **A reciproca EXIGE ambos os pontos periodicos.** Dois pontos NAO
  periodicos tem, ambos, `periodicOrbit = Cycle.nil`; as orbitas vazias
  sao iguais SEM que as trajetorias se encontrem. As hipoteses `hp` e `hq`
  permanecem visiveis na assinatura, e o teste de auditoria verifica
  concretamente `periodicOrbit CE002.f a = Cycle.nil`.
- **Nao formalizado**: nenhum dos seis contraexemplos exibe dois pontos
  nao periodicos que NAO se encontram — em `CE-002` e `CE-004` os
  transitorios SE ENCONTRAM. Construi-lo exigiria um setimo modelo, isto
  eh, matematica nova, proibida neste gate. Registrado como observacao
  estrutural, NAO como fato formalizado.

### API and instance audit

- **16 declaracoes publicas**, exatamente a lista minima. Um unico
  auxiliar, `minimalPeriod_eq_two`, confirmado `private`.
- **5 instancias, ZERO no nucleo matematico.** Todas `Fintype` de
  contraexemplo, em cinco namespaces; `CE005` nao declara instancia.
- **0 conflitos**, zero `Setoid`, zero import de `SimpleGraph`, zero
  `Quotient`. Umbrella nao ambiguo.
- Wrappers relacionais usam `Std.Refl` e `Std.Symm`, os nomes **nao
  depreciados**; `IsTrans` tambem nao esta depreciado. Nenhum exigiu API
  depreciada.
- Novo teste `Tests/FoundFunctionalGraph001InstanceAudit.lean` (exit 0),
  que **nao altera modulo matematico algum** e verifica que, com todas as
  instancias em escopo, a API continua se aplicando a `Bool`.

### Limits

- **`periodicOrbit` eh noncomputavel**: o resultado NAO fornece algoritmo
  executavel de enumeracao de componentes, calculo de `mu` ou deteccao de
  ciclo. Registrado em `REUSE_MATRIX.md`, que separa uso proposicional de
  uso computacional.
- Matriz de reutilizacao: **1** `DIRECT_REUSE`, **7** `REQUIRES_ADAPTER`,
  **2** `CONCEPTUAL_ONLY`. Nenhuma integracao criada.

### Gaps

- **Onze resolvidos, quatro abertos** (`006`, `007`, `012` diferidos;
  `014` bibliografico). Nenhum fechado sem evidencia.

### Not done

- **0** teoremas novos, **0** modulos matematicos alterados, **0** claims
  novas (ledger em **19**), **0** arquivos de legado, **0** de
  `RH-NOGO-001`, **0** de `FOUND-SEMIGROUP-002`.

### Changed

- `canonical_commit`: `f8ccc02` -> `3f6d7e7`, no preflight.
- `result_review: APPROVED`; `extension_status: NOT_AUTHORIZED`.
- `authorized_action` -> `PORTFOLIO_REVIEW_REQUIRED`, que eh **trava de
  governanca**, nao acao autorizada. `NO_ACTION_AUTHORIZED` NAO foi usado.
  Nenhuma entrada nova no allowlist.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_RESULT_REVIEW_APPROVED`. A frente fica
  encerrada. **O laboratorio nao tem frente ativa.**

## FOUND-FUNCTIONAL-GRAPH-001-FORMALIZATION - 2026-07-31

### Added

- Nucleo Lean em
  `05_FORMAL/lean/TamesisLab/Foundations/FunctionalGraphs/`:
  `Relations`, `PeriodicOrbits`, `ComponentCycle`, `Counterexamples`,
  `Audit`, agregador e dois testes isolados.
  **8 definicoes, 44 teoremas, 5 indutivos, 5 instancias, 0 estruturas.**
- Teorema principal `exists_component_cycle_with_entry_bound`: toda
  trajetoria alcanca um ponto periodico antes de `card X` passos, e todos
  os pontos periodicos do mesmo componente determinam a **mesma orbita
  periodica**. Prova por composicao de cinco passos.
- Corolario opcional `eventuallyMeets_of_periodicOrbit_eq`: **formalizado**,
  nao adiado.
- Seis contraexemplos `FFG-CE-001..006`, todos em Lean.
- `THEOREM_MAP.md`, `PROOF_AUDIT.md`, `COUNTEREXAMPLE_AUDIT.md`,
  `RESULT_BOUNDARY.md`.
- Claim `FUNCTIONAL-GRAPH-COMPONENT-FORMAL-001` (`F`, VERIFIED,
  `mathematical_novelty: NONE`). Ledger: **19 claims**.

### Verified

- `lake build` PASS com **8.726 jobs** em 96 s; dois testes isolados exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms`: `iterReachable_trans` **nao depende de axioma algum**;
  `eventuallyMeets_trans` usa apenas `propext` e `Quot.sound`; os demais
  ficam em `propext, Classical.choice, Quot.sound`. Sem `sorryAx`.
- **Arquitetura por hipoteses confirmada pelas assinaturas**:
  `eventuallyMeets_trans` e `periodicOrbit_eq_of_eventuallyMeets` **nao**
  exigem `Fintype X`; `DecidableEq X` **ausente de todos** os teoremas.
- **Zero instancias no nucleo matematico**; as 5 sao `Fintype` dos
  contraexemplos. Zero `Setoid`, zero import de `SimpleGraph`, zero
  `Quotient`.
- Pigeonhole **nao reaplicado** — consumido em `FOUND-SEMIGROUP-002`.
- `decide` **nao** usado sobre igualdade de `periodicOrbit`
  (noncomputavel); `CE003.orbit_eq` sai de
  `periodicOrbit_apply_iterate_eq`. Zero `native_decide`.
- Auditoria de whitespace executada **antes** do `git add`; **um unico
  commit**, sem commit corretivo posterior.

### Corrected

- `le_total` desconhecido sob imports minimos -> `Nat.le_total` (core).
- `Symmetric` **depreciado** -> `Std.Symm`, cujo construtor tem os dois
  elementos **explicitos** (`⟨fun _ _ h => …⟩`).
- `rw` nao fechava por `rfl` em cinco lemas de iteracao: o `rfl` automatico
  usa transparencia reduzivel e nao desdobra funcoes por casamento de
  padrao. `rfl` explicito acrescentado.
- `Mathlib.Tactic.Omega` **nao existe** nesta revisao; o import sugerido
  pelo gate foi omitido. `omega` eh do core.

### Not deferred

- **`FFG-CE-006` na versao FORTE.** O gate permitia adiar a igualdade dos
  periodos minimos; nao foi necessario. `minimalPeriod f a0 =
  minimalPeriod f b0 = 2` provado via `IsPeriodicPt.minimalPeriod_dvd`,
  `minimalPeriod_pos_of_mem_periodicPts`, `Nat.le_of_dvd`,
  `minimalPeriod_eq_one_iff_isFixedPt` e `omega`.

### Blocked

- **A unicidade eh da ORBITA**, nao do ponto (`FFG-CE-005` refuta), nao do
  representante, nao de `mu`, nao do periodo, nao de um ciclo global
  (`FFG-CE-001` refuta).
- Diferidos: ponte `SimpleGraph` (`FFG-GAP-012`), arvores (`FFG-GAP-007`),
  distancia minima (`FFG-GAP-006`), tempo minimo, representante canonico,
  quociente, classificacao completa.
- `FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`.
- `mathematical_novelty: NONE`.
- `RH-NOGO-001` e os arquivos matematicos de `FOUND-SEMIGROUP-002`:
  **0 tocados**.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_VERIFIED`.

## FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION-REVIEW - 2026-07-31

### Corrected

- **`MutuallyReachable`**: retirada a formulacao imprecisa "identifica o
  ciclo, nao o componente". Adotada a formulacao por classes: em pontos
  periodicos expressa pertencimento a mesma trajetoria ciclica; no dominio
  total, a classe de `p` periodico tem `minimalPeriod f p` elementos e cada
  ponto transitorio forma classe unitaria. Argumento de isolamento escrito.
  **Refinamento acrescentado pela revisao**: "classe unitaria" NAO distingue
  transitorio de ponto fixo — um ponto fixo tambem tem classe unitaria.
- **`IsRecurrent` RETIRADO.** "Recorrencia" tem significados mais amplos em
  dinamica. Estrategia A com a clausula condicional resolvida
  negativamente: os teoremas publicos usam `x ∈ Function.periodicPts f`
  diretamente; `IsCyclePoint`/`IsTransientPoint` NAO criados, porque a
  lista CORE nao os usa. Nessa resolucao A coincide com B.
- **Testemunhas da transitividade corrigidas.** A auditoria confirmou
  `iterate_add_apply (f) (m n) (x) : f^[m + n] x = f^[m] (f^[n] x)` — a
  contagem EXTERNA vem a esquerda. Formas naturais: `d + mx` e `d + nz`,
  nao `mx + d` e `nz + d`. Novo gap `FFG-GAP-015`.
- **`FFG-MAIN-001` e `FFG-MAIN-002` COLAPSADOS** em
  `exists_component_cycle_with_entry_bound`: o `p` existencial era sempre
  `f^[mu] x`, logo redundante. `FFG-REC-001` tambem removido.

### Added

- `SPECIFICATION_REVIEW.md`, `FINAL_DEFINITIONS.md`, `FINAL_SIGNATURES.md`,
  `API_NAMING_DECISION.md`, `REVIEW_DECISION.md` — **congelados**.
- Nucleo: 3 definicoes e **9 teoremas**; 2 corolarios opcionais.

### Verified

- Probe descartavel em `/tmp`, somente `import` e `#check`, exit **0**,
  **removido**. Zero `theorem`/`example`/`axiom`/`sorry`/`admit`.
  **0 arquivos `.lean` no repositorio; nenhum `lake build`.**
- `periodicPts` exige periodo positivo; `IsPeriodicPt f 0 x` eh sempre
  verdadeiro e nao serve sozinha.
- `periodicOrbit : Cycle X`, sem `DecidableEq`, **noncomputavel** — nao
  impede provas proposicionais, impede `decide` sobre igualdade de orbitas.
- Hipoteses: nenhuma finitude nas relacoes e na igualdade de orbitas;
  `[Fintype X]` so na existencia e no principal; `DecidableEq X` ausente.
- pytest 9 passed; `labctl validate` PASS.

### Blocked

- `componentSet` `DEFERRED_API_ALIAS` — sem uso na API publica.
- `Setoid`, `SimpleGraph`, arvores, distancia minima, representante
  canonico, classificacao completa: **DEFERRED**. A ponte com `SimpleGraph`
  fica como **conjectura futura**, nao como claim.
- `FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`.
- `mathematical_novelty: NONE`; ledger em **18** claims.
- `RH-NOGO-001` e os arquivos matematicos de `FOUND-SEMIGROUP-002`:
  **0 tocados**.

### Changed

- `canonical_commit`: `df6adb9` -> `90fb4e2`, no preflight.
- `specification_status`: `READY_FOR_REVIEW` -> `APPROVED`.
- `authorized_action` -> `FOUND_FUNCTIONAL_GRAPH_001_FORMALIZATION_AUTHORIZED`.
- `DEFINITIONS.md` e `THEOREM_CANDIDATES.md` marcados **historicos**, com as
  decisoes superadas preservadas e a correcao anexada.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_REVIEW_APPROVED`.

## FOUND-FUNCTIONAL-GRAPH-001-SPECIFICATION - 2026-07-31

### Decided

- **Componente funcional := classe de `EventuallyMeets`**
  (`∃ m n, f^[m] x = f^[n] y`). **NAO** `MutuallyReachable`.
  Contraexemplo decisivo `FFG-CE-004`: em `a→c, b→c, c→c`, os estados `a` e
  `b` estao no mesmo componente e nenhum alcanca o outro;
  `MutuallyReachable` separaria em tres classes o que eh uma estrutura so.
- **Um unico nome**: `EventuallyMeets`. `SameFunctionalComponent` rejeitado
  como segundo nome, **inclusive na forma `abbrev`**.
- **Unicidade = igualdade de `Function.periodicOrbit`**, nao existencia de
  um unico ponto periodico (`FFG-CE-005` refuta) nem representante
  canonico. O objeto unico eh a ORBITA.
- **Orientacao fixada**: o primeiro argumento de `EventuallyMeets` vai para
  o lado esquerdo da igualdade de orbitas. Consistente em `FFG-CYCLE-001` e
  `FFG-MAIN-001`.
- Alvo `CORE_UNIQUE_CYCLE_WITH_ENTRY_BOUND`, com `mu < Fintype.card X`.

### Added

- Especificacao em
  `02_FOUNDATIONS/04_FUNCTIONAL_GRAPHS/FOUND_FUNCTIONAL_GRAPH_001/`,
  **16 artefatos**. Quinze teoremas candidatos, seis contraexemplos,
  catorze gaps, catorze stop conditions.
- `COMPONENT_NOTIONS.md` e `NOVELTY_BOUNDARY.md` sao **vinculantes**.

### Verified (auditoria da Mathlib, por leitura da fonte)

- `periodicPts f = { x | ∃ n > 0, IsPeriodicPt f n x }` — periodo positivo
  **por definicao**, o que resolve a armadilha de `n = 0`.
- `periodicOrbit : Cycle α` **SEM `DecidableEq`** — bloco de variaveis em
  `Dynamics/PeriodicPts/Defs.lean:57`.
- **`periodicOrbit` eh NONCOMPUTAVEL** (`noncomputable section`, 240-490):
  `decide` indisponivel para igualdade de orbitas. Afeta os contraexemplos,
  nao o nucleo. `FFG-GAP-011`.
- `periodicOrbit_apply_iterate_eq` da `FFG-CYCLE-001` em **tres passos**,
  sem aritmetica modular.
- `mk_mem_periodicPts` eh o adaptador exato de `exists_eventual_period`.
- **Zero `NOT_FOUND`**: toda a maquinaria de ciclos ja existe. O conteudo
  matematico proprio desta frente eh menor que o da anterior; o valor eh de
  API e integracao.

### Corrected

- **Previsao refutada**: `FFG-GAP-008` previa que `DecidableEq X`
  provavelmente seria necessaria aqui. A leitura da fonte mostrou que
  **nao eh** — o nucleo exige apenas `[Fintype X]`. Registrado como
  refutacao explicita.
- **Assinatura rejeitada**: a forma `∃ μ p : ℕ × X` de
  `exists_recurrent_reachable` foi descartada por ser par artificial;
  adotada a forma limpa recomendada pelo proprio gate.

### Blocked

- **Formalizacao NAO autorizada.** A proxima etapa eh a REVISAO da
  especificacao, para que uma definicao inadequada de componente nao seja
  congelada em Lean.
- Diferidos: ponte `SimpleGraph` (`FFG-GAP-012`), arvores de entrada,
  distancia minima, unicidade de `mu`, contagem de componentes.
- `mathematical_novelty: NONE`. Decomposicao "forma rho" eh material padrao.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.
- `FOUND-SEMIGROUP-002.extension_status` permanece `NOT_AUTHORIZED`.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** experimentos
  Python, **0** claims promovidas (ledger em 18), **0** arquivos de legado.

### Result

- `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_READY`.

## PORTFOLIO-REVIEW - 2026-07-31

### Lock transition

- **`NO_ACTION_AUTHORIZED` -> `PORTFOLIO_REVIEW_REQUIRED`**, atomicamente,
  nos cinco pontos de governanca viva: allowlist do `labctl.py`,
  `LAB_STATE`, `RESEARCH_QUEUE`, `STATUS.yaml` e `CLOSURE_RECORD.md` de
  `FOUND-SEMIGROUP-002`. Motivo: o sufixo `_AUTHORIZED` convidava a ler a
  trava como autorizacao.
- **Registros historicos NAO foram reescritos** —
  `found-semigroup-002-result-review.json`, `09_SESSIONS/` e este
  changelog documentam o que aquele gate decidiu, com o nome que a trava
  tinha entao. Uma busca futura ainda encontrara o nome antigo neles, e
  isso eh correto.
- A trava foi **satisfeita** neste mesmo gate, pela emissao explicita de
  uma revisao de portfolio.

### Decided

- **`FOUND-FUNCTIONAL-GRAPH-001` selecionado** (Finite Functional Graph
  Decomposition), track `foundations`, status `SCOPED`. Busca por
  duplicata: **0 ocorrencias**.
- Os seis itens `SCOPED` remanescentes foram reavaliados; **nenhum**
  satisfaz simultaneamente infraestrutura Mathlib pronta, acesso alto a
  contraexemplos e PoC em 30 dias. `TOE-INTERFACE-001` esta **bloqueado**:
  depende formalmente de `RH-NOGO-001`, congelado.
- **Resultado forte NAO autorizado**: a unicidade do ciclo por componente
  depende de qual nocao de componente for adotada (`FFG-GAP-002`,
  `FFG-GAP-004`). `strong_result_status:
  NOT_AUTHORIZED_BEFORE_SPECIFICATION`.

### Added

- `01_PORTFOLIO/PORTFOLIO_REVIEW_2026_07_31.md` e
  `01_PORTFOLIO/NEXT_WORK_ITEM_DECISION.md`.
- Entrada `FOUND-FUNCTIONAL-GRAPH-001` em `RESEARCH_QUEUE.yaml` e cadeia
  de fundacoes finitas em `GLOBAL_DEPENDENCY_GRAPH.md`.
- Dez gaps iniciais `FFG-GAP-001..010` e cinco contraexemplos planejados
  `FFG-CE-001..005`.

### Changed

- `canonical_commit`: `b4ce2551` -> `3f72ad0`, no preflight.
- `active_work_item`: `FOUND-SEMIGROUP-002` -> `FOUND-FUNCTIONAL-GRAPH-001`.
- `authorized_action` -> `FOUND_FUNCTIONAL_GRAPH_001_SPECIFICATION_PREPARATION_AUTHORIZED`.
- `labctl`: sequencia de gates admite o novo item, com pre-condicao
  `FOUND-SEMIGROUP-002 VERIFIED`.

### Blocked

- **`FOUND-FUNCTIONAL-GRAPH-001` NAO eh extensao de `FOUND-SEMIGROUP-002`**,
  cujo `extension_status` permanece `NOT_AUTHORIZED`. A relacao eh de
  reutilizacao de API verificada.
- `mathematical_novelty: NONE`. Decomposicao "rho shape" de iteracao
  finita eh material padrao.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** claims
  promovidas, **0** arquivos de legado, **0** arquivos matematicos de
  `FOUND-SEMIGROUP-002`, **0** pastas de especificacao da nova frente.

### Result

- `PORTFOLIO_REVIEW_APPROVED_FUNCTIONAL_GRAPH_SELECTED`.

## FOUND-SEMIGROUP-002-RESULT-REVIEW - 2026-07-31

### Reviewed

- `FRR-001` a `FRR-007`: **todos CONFIRMADOS**. Verificado por inspecao
  que a reciproca de `IsInvariant.under` NAO eh afirmada, e que a palavra
  "periodo" nunca significa periodo minimo.
- **Caso `card X = 0`**: o teorema recebe `x : X`, logo no ponto de
  aplicacao `X` eh habitado. Sem contradicao escondida. Zero instancias de
  `Nonempty`/`Inhabited`.
- **Casa dos pombos**: 1 uso real (3 ocorrencias textuais: uso, docstring,
  `#check`). Nao reprovada no teorema principal, no corolario de acao nem
  na propagacao.
- **`minimalPeriod`**: 4 mencoes, **todas em comentario**; 0 usos.
  `MulAction.period`: 0 ocorrencias.

### API and instance audit

- **API publica: 17 declaracoes**, exatamente a lista minima esperada.
  Um unico auxiliar, `eventual_period_of_lt`, e ele eh `private`.
- **11 instancias, ZERO no nucleo matematico.** Todas em
  `Counterexamples`, sob cinco namespaces: `CE001` 4, `CE002` 4,
  `CE003` 1, `CE004` 2, `CE005` 0.
- **0 conflitos.** `CE004` reutiliza `CE001.Tr` sobre outro espaco de
  estados; os pares sao distintos e ambos `•` resolvem corretamente.
- **Nenhuma instancia de `Preorder`** (1 ocorrencia da palavra, num
  comentario que declara a exclusao).
- Novo teste `Tests/FoundSemigroup002InstanceAudit.lean` (exit 0), que
  **nao altera modulo matematico algum**: onze `#synth`, desambiguacao do
  `•`, e a verificacao decisiva de que `exists_eventual_period` continua
  se aplicando a `Bool` com todas as instancias em escopo.

### Gaps

- Nove resolvidos, tres abertos. **`FSG2-GAP-007` NAO fechado** (negativa
  sobre o periodo continua sem contraexemplo); **`FSG2-GAP-009` NAO
  fechado** (sem auditoria bibliografica).

### Reuse

- Um unico `DIRECT_REUSE`: testes de alcancabilidade — a parte da API que
  **nao exige finitude**. Seis `REQUIRES_ADAPTER`, tres `CONCEPTUAL_ONLY`.
  Nenhuma integracao criada.

### Not done

- **0** teoremas novos, **0** modulos matematicos alterados, **0** claims
  novas, **0** claims fisicas ou de novidade, **0** arquivos de legado,
  **0** arquivos de `RH-NOGO-001` tocados.

### Changed

- `canonical_commit`: `2b86a880` -> `b4ce2551`, no preflight.
- `result_review: APPROVED`; `extension_status: NOT_AUTHORIZED`.
- `authorized_action` -> `NO_ACTION_AUTHORIZED`, que eh **trava, nao
  autorizacao de execucao**.

### Result

- `FOUND_SEMIGROUP_002_RESULT_REVIEW_APPROVED`. A frente fica **encerrada
  como fundacao formal reutilizavel**, sem autorizacao ativa. O
  laboratorio nao tem frente ativa: a escolha do proximo trabalho exige um
  gate separado de revisao de portfolio.

## FOUND-SEMIGROUP-002-FORMALIZATION - 2026-07-31

### Corrected

- **5.1 Invariancia sob um elemento.** Retirada a afirmacao de que
  `IsInvariantUnder a` seria *universalmente* mais fraca que
  `IsInvariant`. O que vale e foi formalizado eh apenas a implicacao
  `IsInvariant I -> IsInvariantUnder a I` (`IsInvariant.under`). A estrita
  fraqueza PODE ocorrer, mas nao uniformemente: se `a` gera `M`, as duas
  nocoes coincidem.
- **5.2 Contraexemplo de alcancabilidade.** `CE-001` reconstruido como
  **acao genuina de monoide** (`{idT, collapse}` sobre `{zero, one}`), com
  as leis verificadas antes da instanciacao. O grafo de uma funcao isolada
  refutaria apenas a alcancabilidade por aquele gerador, nao a simetria de
  `Reachable`, que eh definida pela acao COMPLETA.

### Added

- Nucleo Lean em `05_FORMAL/lean/TamesisLab/Foundations/FiniteDynamics/`:
  `Reachability`, `Invariants`, `EventualPeriodicity`, `MonoidIteration`,
  `Counterexamples`, `Audit`, agregador e dois testes isolados.
  **41 teoremas, 10 defs, 6 indutivos, 11 instancias.**
- Teorema principal `exists_eventual_period`: toda trajetoria de
  `f : X -> X` com `X` finito eh eventualmente periodica, com
  `mu < card X`, `0 < lam`, `mu + lam <= card X`, ponto periodico na cauda
  e propagacao a todos os indices posteriores.
- Corolarios de acao `monoid_element_eventually_periodic` e
  `..._propagates`, **derivados** via `smul_iterate_apply`.
- Cinco contraexemplos formais (`CE-001..CE-005`), todos em Lean, **sem
  Python** e **sem `native_decide`**.
- `THEOREM_MAP.md`, `PROOF_AUDIT.md`, `COUNTEREXAMPLE_AUDIT.md`,
  `RESULT_BOUNDARY.md`, `C3_BOUNDARY.md`.
- Claim `FINITE-DYNAMICS-FORMAL-001` (`F`, VERIFIED,
  `mathematical_novelty: NONE`).

### Verified

- `lake build` PASS com **8.717 jobs** em 117 s; dois testes isolados
  exit 0. Build final **sem avisos**.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms` nos 8 objetos: **quatro nao dependem de axioma algum**;
  os demais usam apenas `propext`, `Classical.choice`, `Quot.sound`.
- Casa dos pombos usada **uma unica vez**; `minimalPeriod` **nunca** usado;
  **nenhuma** instancia global de `Preorder`.
- Hipoteses ociosas confirmadas e removidas: `exists_eventual_period` exige
  **somente** `[Fintype X]`; o corolario de acao nao exige `Fintype M`,
  `DecidableEq X` nem `Group M`. `FSG2-GAP-004c` fechado.
- pytest 9 passed; `labctl validate` PASS com `canonical_commit_check` PASS.

### Changed

- `canonical_commit`: `39e3d95` -> `2b86a880`, no preflight.
- `FOUND-SEMIGROUP-002`: `READY` -> `VERIFIED`.
- `authorized_action` -> `FOUND_SEMIGROUP_002_RESULT_REVIEW_AUTHORIZED`
  (entrada literal unica).

### Blocked

- **Novidade matematica: NONE.** Periodicidade eventual em conjunto finito
  eh o principio da casa dos pombos.
- NAO provados: unicidade da cauda, minimalidade do periodo, decomposicao
  canonica, classificacao de acoes finitas, sistemas infinitos, qualquer
  resultado fisico, TRI, TDTR.
- `C3_BOUNDARY.md` (vinculante): "propriedades de C3 falham em geral"
  significa que para CADA UMA existe contraexemplo, **nao** que todas
  falhem simultaneamente em toda acao. Nenhum teorema de
  `FOUND-SEMIGROUP-001` foi alterado.
- `FSG2-GAP-007`: a negativa "o periodo depende do estado inicial"
  continua sem contraexemplo e **nao eh afirmada**.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT`; **0** arquivos tocados.

### Result

- `FOUND_SEMIGROUP_002_FORMALIZATION_VERIFIED`.

## FOUND-SEMIGROUP-002-SPECIFICATION - 2026-07-31

### Preflight

- `canonical_commit` atualizado de `c186ab59` para `39e3d95` **antes** de
  qualquer trabalho de especificacao; politica textual substituida por
  "ultimo commit canonico integralmente encerrado antes da sessao atual;
  deve existir e ser ancestral do HEAD".
- Commits `1576cf1` e `39e3d95` fazem parte obrigatoria do estado de
  retomada.

### Added

- Validacao nao destrutiva de `canonical_commit` em `labctl.py`
  (`check_canonical_commit`, funcao pura com `runner` injetavel):
  `cat-file` ausente -> `CANONICAL_COMMIT_UNAVAILABLE` com recomendacao de
  completar o historico; `is-ancestor` exit 0 -> PASS (igualdade aceita);
  exit 1 -> `CANONICAL_COMMIT_NOT_ANCESTOR`; outro exit ->
  `CANONICAL_COMMIT_GIT_ERROR`. Severidade **erro**, nunca warning.
- `tests/test_canonical_commit.py`: 7 testes cobrindo os cinco casos
  pedidos, **sem criar branch nem reescrever historico**. O teste de
  igualdade afirma que nao ha `rev-parse` extra, travando a ancestralidade
  nao estrita.
- Especificacao `FOUND-SEMIGROUP-002` em
  `02_FOUNDATIONS/03_SEMIGROUPS/FOUND_SEMIGROUP_002/` (13 artefatos).
  Onze teoremas candidatos, cinco contraexemplos, doze gaps.

### Decided

- Meta principal: **`C. CORE_BOUNDS_AND_PROPAGATION`**. Os tres limitantes
  foram verificados como simultaneamente alcancaveis ANTES da escolha.
  **`DECOMPOSITION` excluida** apos analise de custo (`FSG2-GAP-004b`).
- Tres camadas separadas: acao completa / gerador / funcao finita.
  Periodicidade eventual pertence a Camada C e **nao** menciona monoide.
- Sem instancia global `Preorder` para alcancabilidade (`FSG2-GAP-006`).

### Verified

- `smul_iterate_apply` **existe** na Mathlib fixada: `FSG2-GAP-003`
  resolvido pela API, nao por prova.
- `mem_orbit_iff` eh `Iff.rfl`: a ponte alcancabilidade/orbita custa zero.
- Periodicidade eventual **ausente** do Mathlib (zero ocorrencias de
  `preperiodic`/`eventuallyPeriodic`): o enunciado sera local.
- **Armadilha registrada**: `minimalPeriod` e `MulAction.period` devolvem 0
  fora de `periodicPts`; `CE-003` a torna detectavel (`FSG2-GAP-002b`).
- pytest **9 passed**; `labctl validate` PASS com `canonical_commit_check`
  PASS.

### Not done

- **0** arquivos Lean, **0** provas, **0** `lake build`, **0** experimentos
  Python, **0** claims cientificas promovidas, **0** arquivos de legado
  modificados, **0** arquivos de `RH-NOGO-001` tocados.

### Blocked

- Novidade matematica: **NONE**. Periodicidade eventual em conjunto finito
  eh o principio da casa dos pombos. `NOVELTY_BOUNDARY.md` eh vinculante.
- Bibliografia primaria `NOT_AUDITED` (`FSG2-GAP-009`): nenhuma afirmacao
  de prioridade historica eh permitida.
- `RH-NOGO-001` permanece `FROZEN_PARTIAL_RESULT` / `NOT_AUTHORIZED` /
  `NO_EXECUTION`.

### Result

- `FOUND_SEMIGROUP_002_SPECIFICATION_READY`.
  `authorized_action` -> `FOUND_SEMIGROUP_002_FORMALIZATION_AUTHORIZED`.

## APPROVAL RECORD - 2026-07-31

### Approved

- **`DEC-012` aprovado apos revisao.** As quatro alteracoes em
  `labctl.py` sao minimas, literais e deflacionarias, e preservam
  `RH-NOGO-001` como `NOT_AUTHORIZED` / `NO_EXECUTION`. Nao houve
  relaxamento material do guardrail.
- **`DEC-013` aprovado apos revisao.** `FOUND-SEMIGROUP-002` eh aceito
  como novo work item `SCOPED`, porque os itens remanescentes da fila
  canonica eram incompativeis com os criterios de custo e dependencia da
  revisao. A criacao **nao** eh uma descoberta cientifica: o item deve
  investigar propriedades padrao de acoes finitas de monoides - orbitas,
  alcancabilidade, invariantes, periodicidade eventual e contraexemplos.
- Escopo da aprovacao: **apenas preparacao da especificacao**.

### Added

- `DEC-014`: endurecimento futuro de governanca para
  `FROZEN_PARTIAL_RESULT`, registrado como `PENDING_NOT_IMPLEMENTED`.
  Todo item nesse estado deveria exigir `freeze_record`,
  `result_boundary`, `reactivation_criteria` e `concrete_layer_status`.
  **Nao implementado em `labctl.py`** neste gate.
- `RESEARCH_QUEUE.yaml`: `concrete_layer_status: DEFERRED` em
  `RH-NOGO-001`, que passa a conter os quatro campos propostos - o
  endurecimento futuro sera um no-op para o estado atual.

### Unchanged

- Commit `1576cf1` **nao foi reescrito**.
- `active_work_item: FOUND-SEMIGROUP-002`, `work_status: SCOPED`,
  `authorized_action: FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED`.
- Nenhum teorema Lean, nenhuma claim promovida, nenhuma especificacao
  iniciada.

## RH-NOGO-RESEARCH-REVIEW - 2026-07-31

### Decided

- **`RH-NOGO-001` CONGELADO** como resultado parcial formal
  (`A_FREEZE_AS_PARTIAL_FORMAL_RESULT`, `DEC-012`). Congelado, **nao
  descartado**: a camada abstrata eh verificada e reutilizavel.
- Opcoes B (continuar), C (colaboracao externa) e D (rejeitar) descartadas
  com motivo registrado.
- `FOUND-SEMIGROUP-002` selecionado como proximo work item (`DEC-013`),
  **apenas para especificacao**. Nenhum dos seis itens remanescentes da
  fila satisfazia os criterios do gate.

### Added

- `RH_NOGO_FINAL_RESEARCH_REVIEW.md`, `RH_NOGO_FREEZE_RECORD.md`,
  `RH_NOGO_REACTIVATION_CRITERIA.md`, `RH_NOGO_RESULT_BOUNDARY.md`.
- `RESEARCH_QUEUE.yaml`: item `FOUND-SEMIGROUP-002` (algebra finita e
  dinamica discreta; `Fintype`/`Decidable`/`decide` ja disponiveis).

### Changed

- `RH-NOGO-001`: `SCOPED` -> `FROZEN_PARTIAL_RESULT` na fila e em
  `STATUS.yaml`. `authorization_state` e `execution_state` **inalterados**.
- `active_work_item`: `RH-NOGO-001` -> `FOUND-SEMIGROUP-002`.
- `authorized_action`: `RH_NOGO_RESEARCH_REVIEW_AUTHORIZED` ->
  `FOUND_SEMIGROUP_002_SPECIFICATION_PREPARATION_AUTHORIZED`.
- **`labctl.py`, quatro alteracoes minimas e literais** (registradas em
  `DEC-012`): `ALLOWED_WORK_STATUS += FROZEN_PARTIAL_RESULT`; checagem de
  `RH-NOGO-001` aceita `{SCOPED, FROZEN_PARTIAL_RESULT}` (deflacionaria,
  segue bloqueando `READY`/`IN_PROGRESS`/`VERIFIED`); sequencia de gates
  admite `FOUND-SEMIGROUP-002`; allowlist +1 entrada literal.
  As travas `NOT_AUTHORIZED` / `NO_EXECUTION` **nao foram tocadas**.

### Verified

- Teoremas Lean novos: **0**. Claims promovidas: **0**. No-go executado:
  **nao**. Legado modificado: **0**.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- `GLOBAL-WEYL-BRIDGE-SCALAR`: 9 obrigacoes, **0 provadas**.
- Riemann-von Mangoldt: **nao formalizada**.
- Reativacao so por `REACT-001..005`. Mais capacidade computacional ou um
  modelo de IA mais forte **nao** sao criterio.

### Result

- `RH_NOGO_FROZEN_AS_PARTIAL_FORMAL_RESULT`.
  `spectral_nogo: NOT_ESTABLISHED`; `hilbert_polya: NOT_EXCLUDED`;
  `riemann_hypothesis: NO_RESULT`.

## ABSTRACT-COUNTING-NOGO - 2026-07-31

### Added

- `ABSTRACT-NOGO-001` formalizado em
  `05_FORMAL/lean/TamesisLab/RHNogo/Composition/`: `AbstractNogo.lean`,
  `Corollaries.lean`, `Audit.lean`, agregador `Composition.lean` e teste
  `Tests/RHNogoAbstractComposition.lean`. **5 teoremas**, 1 estrutura,
  1 definicao.
- Teorema principal `abstract_power_tlog_incompatibility`: uma lei de
  potencia positiva para `NTarget`, uma lei positiva `T log T` para
  `NBase` e `NTarget - NBase = o(T log T)` sao simultaneamente
  insatisfaziveis. Prova em DUAS LINHAS: composicao de
  `COUNTING-LAW-BRIDGE` com `ASYM-NOGO-001`.
- Estrutura `AbstractCountingNogoData` (nao eh `class`) e o teorema
  `.false` de inabitabilidade.
- Corolarios `ABSTRACT-NOGO-E0-001` (igualdade eventual) e
  `ABSTRACT-NOGO-E1-001` (diferenca limitada), reutilizando conversoes ja
  verificadas.
- `ABSTRACT_COMPOSITION_THEOREM_MAP.md` e
  `ABSTRACT_COMPOSITION_PROOF_AUDIT.md`.
- Claim `ABSTRACT-COUNTING-NOGO-FORMAL-001` (`F`, `formal_asymptotics`,
  VERIFIED).

### Verified

- `lake build` PASS com **8.708 jobs** em 129 s; teste isolado exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0` na arvore inteira.
- `#print axioms` nos 7 objetos: apenas `propext`, `Classical.choice`,
  `Quot.sound`.
- Imports da pasta `Composition/`: **apenas** `AsymptoticCore` e `Bridge`.
  **`Geometry/` NAO importado.**
- Vocabulario proibido na pasta: 7 ocorrencias, **todas em comentarios que
  declaram a exclusao**; nenhuma em identificador, tipo ou termo de prova.
- Direcao da diferenca confirmada por `Iff.rfl`: `SubdominantTLog X Y` eh
  literalmente `X - Y = o(T log T)`. Opcao C (documentar a convencao
  existente); nenhum lema de sinal foi necessario.
- pytest 2 passed; `labctl validate` PASS.
- Nenhuma falha de compilacao: os cinco arquivos passaram de primeira.

### Changed

- `authorized_action`: `RH_NOGO_ABSTRACT_COMPOSITION_FORMALIZATION_AUTHORIZED`
  -> `RH_NOGO_RESEARCH_REVIEW_AUTHORIZED` (entrada literal unica).
- `STATUS.yaml`: `abstract_layer: COMPLETE`.

### Blocked

- **Nenhuma instancia de `PowerCountingLaw` vinda de operador** — exigiria
  `GWB-001..009`, zero provadas.
- **Nenhuma instancia de `TLogCountingLaw` vinda da zeta** — exigiria
  Riemann-von Mangoldt (`SB-GAP-010B`).
- `E3` nao formalizado (`SB-GAP-011`).
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_ABSTRACT_COMPOSITION_VERIFIED`. A camada analitica abstrata
  esta COMPLETA. O resultado **nao eh novidade matematica**.

## RH-NOGO-GEOMETRIC-GAP-RESOLUTION - 2026-07-31

### Added

- `W_ELLIPTIC_SCALAR_V3.md`: classe dividida em
  **W-ELLIPTIC-SCALAR-SOURCE** (6 condicoes literais de Coriasco-Doll p.1)
  e **W-ELLIPTIC-SCALAR-BRIDGE** (mais 6 acrescimos deste laboratorio,
  cada um marcado `EXPLICIT_BRIDGE_ASSUMPTION`). Metade da classe eh
  deste laboratorio, e isso agora esta numa tabela.
- Condicoes novas e explicitas: `M` nao vazia (B3), `d >= 1` (B4) e
  simbolo principal real, positivo fora da secao nula e homogeneo de
  grau `m > 0` (B5). B5 estava sendo usada TACITAMENTE.
- `WEYL_COEFFICIENT_POSITIVITY.md`: argumento em seis passos para
  `C_P > 0`, com o estado de cada passo.
- `GLOBAL_WEYL_DATA_BRIDGE.md`: instanciacao de `PowerCountingLaw`
  campo a campo, com fornecedor e evidencia.
- `DISCRETENESS_CLASSIFICATION.md`, `GEOMETRIC_LEAN_SCOPE.md`,
  `GEOMETRIC_GAP_RESOLUTION_AUDIT.md`.
- Nucleo Lean em `05_FORMAL/lean/TamesisLab/RHNogo/Geometry/`:
  5 teoremas, 1 estrutura, 1 construtor. Teoria da medida elementar.
- Claim `WEYL-COEFFICIENT-INTERFACE-001` (`F`,
  `spectral_interface_governance`).

### Changed

- **`GWB-008` dividida em tres**: `008A` (positividade da medida no
  espaco de fases, `DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE`),
  `008B` (`C_P > 0`, `ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE`) e
  `008C` (`C_P < infinito`, `DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE`).
- **Discretude classificada sem inflacao**: `GWB-001` eh
  `EXPLICIT_CLASS_ASSUMPTION`; `GWB-002` eh `SOURCE_CITED_RESULT`.
- `GAP-RH-014` -> `RESOLVED_DOCUMENTALLY_FOR_SCALAR_BRIDGE_CLASS_ONLY`.
  NAO eh `CLOSED`: o argumento foi ESCRITO, nao provado.
- `GAP-RH-012` -> `EXPLICIT_CLASS_ASSUMPTION_CLASSIFIED`.
- `GAP-RH-009` -> `OPEN_SYSTEMS_DEFERRED`. **NAO fechado.**
- `authorized_action`: `RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED`
  -> `RH_NOGO_ABSTRACT_COMPOSITION_FORMALIZATION_AUTHORIZED`
  (entrada literal unica, sem wildcard).

### Verified

- `lake build` PASS com **8.703 jobs**; teste isolado exit 0.
- Tokens proibidos: `sorry=0 admit=0 axiom=0 unsafe=0`.
- `#print axioms` nos 7 objetos: apenas `propext`, `Classical.choice`,
  `Quot.sound`.
- Auditoria de escopo em `Geometry/`: nenhuma definicao de variedade,
  fibrado cotangente, operador pseudodiferencial, simbolo principal,
  medida de Liouville ou coeficiente de Weyl concreto. As unicas
  ocorrencias desse vocabulario sao os avisos que declaram a exclusao.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- **As onze obrigacoes `GWB-001..009` continuam NAO PROVADAS.**
- `GAP-RH-015` (finitude de `C_P`) aberto; `SB-GAP-012` (seis acrescimos
  de ponte sem fonte) aberto; `SB-GAP-001` dividido em `001A/001B/001C`.
- `ASYM-NOGO-001` NAO aplicado. Nenhum operador construido ou excluido.
  Hilbert-Polya NAO excluido. Nada afirmado sobre a Hipotese de Riemann.

### Result

- `RH_NOGO_SCALAR_GEOMETRIC_INTERFACE_READY`. A entrada geometrica foi
  resolvida em nivel de INTERFACE e de REGISTRO, nao de prova.

## COUNTING-LAW-BRIDGE — 2026-07-31

### Added

- Ponte de contagem formalizada em
  `05_FORMAL/lean/TamesisLab/RHNogo/Bridge/`: `Definitions.lean`,
  `TLogScale.lean`, `LittleOTransfer.lean`, `CountingLawBridge.lean`,
  `StrongAsymptoticCorollary.lean`, `Audit.lean`, agregador `Bridge.lean`
  e teste `Tests/RHNogoCountingBridge.lean`. **15 teoremas**, 9 definicoes.
- Teorema principal `counting_law_bridge`: se `N_base/(T log T) -> c` e
  `N_target - N_base = o(T log T)`, entao `N_target/(T log T) -> c`.
- Versao estrutural `TLogCountingLaw.transfer`, com preservacao da
  constante provada por `rfl`.
- `STRONG-TLOG-COROLLARY` (`tendsto_tLog_of_eq_main_add_littleO`):
  "formula forte implica limite", **sem mencionar zeta**.
- Hierarquia `E0 => E1 => E2` formalizada.
- `COUNTING_BRIDGE_THEOREM_MAP.md` e `COUNTING_BRIDGE_PROOF_AUDIT.md`.
- Claim `COUNTING-BRIDGE-FORMAL-001` (`F`, `formal_asymptotics`, VERIFIED).

### Corrected

- **`SB-GAP-010` dividido e parcialmente fechado.** A afirmacao anterior de
  que formalizar `RVM-LIMIT` exigiria definir a funcao zeta estava ERRADA
  para a parte generica. `SB-GAP-010A` (corolario generico)
  `CLOSED_BY_FORMALIZATION`; `SB-GAP-010B` (Riemann-von Mangoldt concreto)
  `OUT_OF_CURRENT_SCOPE`; `SB-GAP-010` `SUPERSEDED`.
- **Hipotese ociosa removida:** `0 < c` nao eh necessaria em
  `counting_law_bridge` e foi retirada do teorema tecnico; a positividade
  permanece apenas na interface `TLogCountingLaw`.
- `Bridge/SignatureProbe.lean` reduzido a registro historico: as definicoes
  foram promovidas para `Bridge/Definitions.lean`.

### Verified

- `lake build` PASS com **8.699 jobs**; teste isolado exit 0; tokens
  proibidos zero.
- `#print axioms` nos 13 objetos rastreaveis: apenas `propext`,
  `Classical.choice`, `Quot.sound`.
- Auditoria de escopo: imports da pasta `Bridge/` sao apenas `Log.Basic`,
  `Pow.Real` e `Asymptotics.Lemmas`; busca por `zeta`, `Riemann`, `Weyl`,
  `Complex`, `spectral`, `operator`, `Polya`: **nenhuma ocorrencia**.
- pytest 2 passed; `labctl validate` PASS.
- `ASYM-NOGO-001` **nao** aplicado.

### Changed

- `authorized_action`: `RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED`
  -> `RH_NOGO_GEOMETRIC_GAP_RESOLUTION_AUTHORIZED` (entrada literal unica).

### Blocked

- `GWB-008` (`C_P > 0`): obrigacao GEOMETRICA; nao bloqueou este gate.
- `GAP-RH-012` (discretude), `GAP-RH-009` (fibrados, NAO fechado),
  `SB-GAP-010B`, `SB-GAP-011` (nivel E3 nao formalizado).
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_COUNTING_BRIDGE_VERIFIED`. Componentes analiticos abstratos
  verificados: `COUNTING-LAW-BRIDGE` -> `ASYM-NOGO-001`.

## RH-NOGO-001 — especificacao da ponte de contagem — 2026-07-31

### Added

- Especificacao completa da ponte em `03_MILLENNIUM/01_RIEMANN/`:
  `SOURCE_BRIDGE_SPECIFICATION.md` (indice), `W_ELLIPTIC_SCALAR_V2.md`,
  `W_ELLIPTIC_SYSTEM_DEFERRED.md`, `GLOBAL_WEYL_BRIDGE_OBLIGATIONS.md`
  (GWB-001..009), `RVM_LIMIT_BRIDGE.md`, `COUNTING_LAW_RELATIONS.md`
  (E0-E3), `COUNTING_LAW_BRIDGE_SPEC.md`, `NARROW_NOGO_STATEMENT.md`,
  `SPECTRAL_MATCH_CONVENTIONS.md` (SMC-001..007),
  `SOURCE_BRIDGE_DEPENDENCY_DAG.yaml`, `SOURCE_BRIDGE_GAP_REGISTER.yaml`
  (SB-GAP-001..010), `SOURCE_BRIDGE_LEAN_FEASIBILITY.md`.
- `05_FORMAL/lean/TamesisLab/RHNogo/Bridge/SignatureProbe.lean`: oito
  assinaturas elaboradas (`PowerCountingLaw`, `TLogCountingLaw`,
  `SubdominantDifference`, `EventualEquality`, `BoundedDifference`,
  `RatioEquivalence`, `CountingLawBridgeStatement`,
  `NarrowSpectralNogoStatement`), `set_option autoImplicit false`,
  **nenhuma prova**.

### Changed

- **Alvo migrado de igualdade espectral exata para `N_P(T) - N_zeta(T) =
  o(T log T)` (nivel E2)**, que cobre E0, E1, E2 e E3 com um unico lema.
- `W-ELLIPTIC-SCALAR` v2: bordo e sistemas/fibrados **excluidos**
  deliberadamente. `GAP-RH-009` NAO foi fechado - foi contornado por
  estreitamento (`SB-GAP-006`).
- Regra de quantificacao fixada: "para todo operador REALIZADO P que
  satisfaca INDIVIDUALMENTE as hipoteses". A forma "para todas as
  realizacoes de uma expressao formal" esta proibida.
- `authorized_action`: `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` ->
  `RH_NOGO_COUNTING_BRIDGE_FORMALIZATION_AUTHORIZED` (entrada literal
  unica).

### Verified

- `lake build` PASS com 8.692 jobs; probe isolado exit 0; tokens proibidos
  zero; `ASYM-NOGO-001` **nao** aplicado.
- pytest 2 passed; `labctl validate` PASS.

### Blocked

- `SB-GAP-001` / `GAP-RH-014`: **`C_P > 0` nao eh afirmado por nenhuma
  fonte obtida** - bloqueante para `POWER-LAW-FOR-NP`.
- `SB-GAP-002` / `GAP-RH-012`: discretude eh hipotese incorporada.
- `SB-GAP-003`: convencoes de fronteira (`<` vs `<=`) nao reconciliadas.
- `SB-GAP-010`: `RVM-LIMIT` fora de alcance de formalizacao.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

### Result

- `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_READY`.

## RH-NOGO-001 — fonte global e reformulação da classe — 2026-07-31

### Added

- Separação arquitetural em duas classes: `W_POWER_CLASS.md` (assintótica
  abstrata; nenhuma EDP) e `W_ELLIPTIC_CLASS.md` (v2: pseudodiferencial
  clássico, positivo, auto-adjunto, ordem `m > 0`, variedade compacta).
- `HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md`: as sete etapas A–G com estado e
  fonte de cada uma, mais os cinco pontos que o gate proibiu chamar de
  triviais.
- `GLOBAL_WEYL_THEOREM_CANDIDATES.md`, `GLOBAL_WEYL_CONSTANT.md`,
  `CLASS_W_V2_DECISION.md`, `SELF_ADJOINT_REALIZATION_DECISION.md`,
  `ORDER_PARITY_AUDIT.md`, `ADDITIONAL_SOURCE_AUDIT.md`.
- Fontes obtidas por acesso público (arXiv), com `sha256`: Ivrii 2016
  (*100 years of Weyl's law*, 90 pp.) e Coriasco–Doll 2020 (*Weyl Law on
  Asymptotically Euclidean Manifolds*, 26 pp.).

### Verified

- **A lei de Weyl global existe com hipóteses precisas.** Coriasco–Doll
  p. 1: *"positive elliptic self-adjoint classical pseudodifferential
  operator of order `m > 0` on a compact manifold"*,
  `N(λ) = #{j : λ_j < λ}`, `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`.
- Ivrii (3.1.3) dá a constante correta para **sistemas**:
  `κ₀ = (2π)^{−d}∬ n(x,ξ)dxdξ`, `n` = nº de autovalores do símbolo
  principal em `(0,1)` — não um volume escalar.
- Ivrii (3.1.11) escreve a identidade local→global
  `N⁻(λ) = ∫ e(x,x,λ)dx`, que era a etapa ausente.
- Ivrii 3.1.1(iv): a assintótica de **um termo** vale sem hipótese de não
  degenerescência — suficiente para `W-POWER`.

### Corrected

- **Atribuição bibliográfica (GAP-RH-013).** Coriasco–Doll atribuem a lei
  global a "Hörmander [15]" = Acta Math. 121 (1968), 193–218, artigo que
  enuncia apenas a lei **local**. Regra adotada: citar Hörmander pelo
  resultado local; a lei global por Coriasco–Doll/Ivrii ou pela ponte
  explícita. Hörmander 1968 **não** foi reclassificado.
- `GAP-RH-010` (auto-adjunção) e `GAP-RH-011` (paridade da ordem)
  fechados **por reformulação**, não por prova. `OPERATOR_CLASS.md` (v1)
  não foi editado: permanece como registro do que a auditoria refutou.

### Changed

- Decisões: classe `REFORMULATE_AS_CLASSICAL_PSEUDODIFFERENTIAL`; ordem
  `PSEUDODIFFERENTIAL_POSITIVE_ORDER`; auto-adjunção
  `positive_self_adjoint_operator` (uma realização).
- `authorized_action`: `RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED` →
  `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` (entrada literal única).

### Blocked

- `RETRIEVAL_FAILED`: Safarov–Vassiliev, Shubin e a monografia de Ivrii —
  comerciais; nenhuma tentativa de burlar acesso. As **provas** da lei
  global permanecem em textos não lidos.
- Abertos: `GAP-RH-009` (fibrados/sistemas na etapa D — `UNRESOLVED`),
  `GAP-RH-012` (discretude, `PARTIALLY_SUPPORTED`), `GAP-RH-014`
  (positividade de `C_P`), bordo `AMBIGUOUS`.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
  `ASYM-NOGO-001` **não** aplicado; nenhum teorema Lean criado; nenhuma
  claim promovida.

### Result

- `RH_NOGO_LOCAL_TO_GLOBAL_BRIDGE_SUFFICIENT`.

## RH-NOGO-001 — auditoria de fontes primárias — 2026-07-31

### Added

- Acervo de fontes em `08_REVIEWS/SOURCES/RH_NOGO/`: quatro PDFs originais
  não modificados, com proveniência, tamanho e `sha256` em
  `SOURCE_MANIFEST.yaml`; extrações de texto marcadas como derivadas.
  Nenhuma OCR usada.
- Auditorias por documento: `VON_MANGOLDT_1905_AUDIT.md` (12 perguntas
  respondidas com citação de página), `HORMANDER_1968_AUDIT.md` (17
  perguntas), `RIEMANN_1859_AUDIT.md`, `BOMBIERI_CLAY_AUDIT.md`.
- `CLASS_W_SOURCE_MAPPING.md`: matriz W1–W8 contra fonte primária.
- `SOURCE_BRIDGE_REQUIREMENTS.md`: mapa lógico A–H, sem prova.
- `UNRESOLVED_SOURCE_QUESTIONS.md`: dez questões abertas.

### Verified

- **Pilar A sustentado.** von Mangoldt 1905 p. 19 prova, para `T > 28,558`,
  `N = (T/2π)l(T/2π) − T/2π + 7/8 + η(0,43200 lT + 1,91662 llT + 12,20373)`,
  `−1 < η < 1`. Contagem por parte real de `ξ(t)`, **com multiplicidade**
  ("jede so oft gezählt, als ihre Ordnungszahl angibt", p. 2), `T` escolhido
  fora de zeros, método do princípio do argumento — **incondicional**.
- Riemann 1859 (tradução Wilkins, lida integralmente) apenas esboça e
  declara faltar prova estrita; Bombieri/Clay confirma
  ("states, sketching a proof").

### Blocked

- **Pilar B parcialmente sustentado.** Hörmander 1968 prova a lei de Weyl
  **local** da função espectral (eq. 5.3, p. 215) mas **não enuncia** a
  contagem global `N_P(Λ) ~ C_P Λ^(d/m)`. Busca no texto integral por
  "number of eigenvalues" / "counting function" / `N(λ)`: nenhuma
  ocorrência.
- Classe W: apenas W4 e W6 `SUPPORTED_DIRECTLY`; W7 e W8 `NOT_SUPPORTED`;
  W5 `AMBIGUOUS` (Friedrichs vs. essencial auto-adjunção); W2 cobre apenas
  sistemas com autovalores distintos do símbolo principal.
- A cadeia da ponte quebra na etapa E de `SOURCE_BRIDGE_REQUIREMENTS.md`.

### Changed

- `authorized_action`: `RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED` →
  `RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL_AUTHORIZED` (entrada literal única
  no allowlist). `RH_NOGO_SOURCE_BRIDGE_SPECIFICATION_AUTHORIZED` **não**
  foi concedida, por decisão B.
- `GAP-RH-002` → `AUDITED_INSUFFICIENT`; abertos `GAP-RH-009` a
  `GAP-RH-012`.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- Nenhum teorema Lean escrito, nenhuma claim criada ou promovida.

### Result

- `RH_NOGO_PRIMARY_SOURCES_PARTIALLY_SUFFICIENT`.

## ASYM-NOGO-001 — 2026-07-31

### Added

- Núcleo assintótico formalizado em
  `TamesisLab/RHNogo/AsymptoticCore/{Definitions,Normalization,PowerLog,Incompatibility,Audit}.lean`,
  agregador e teste `Tests/RHNogoAsymptotic001.lean`: 4 definições e 12
  teoremas rastreáveis (ASYM-NOGO-ALG/PL/AUX/CONTRA/PROBE).
- Teorema principal `asym_nogo_001`: nenhuma função real admite
  simultaneamente `N(T)/(T log T) → c > 0` e `N(T)/T^α → C > 0` com `α > 0`.
- `ASYM_NOGO_001_THEOREM_MAP.md` e `ASYM_NOGO_001_PROOF_AUDIT.md`
  (auditoria adversarial + `#print axioms`).
- `EPISTEMIC_CORRECTIONS.md` com os dois eixos separados
  (`source_retrieval_status` / `mathematical_claim_status`).
- Claim `ASYM-NOGO-FORMAL-001` (`F`, `formal_asymptotics`, VERIFIED).

### Corrected

- Afirmação de exaustividade sobre a literatura substituída por
  "amostra bibliográfica catalogada nesta sessão" em `DEFINITIONS.md` e
  `EXCLUSIONS.md`.
- `sources_audited` → `bibliographic_records_classified` em
  `rh-nogo-001-specification-result.json`; nenhuma obra está
  `CONTENT_AUDITED`. O relatório de sessão anterior não foi reescrito.
- `SignatureProbe.lean`: nota registrando que o enunciado, antes sem corpo
  probatório, passou a ser provado.

### Changed

- `authorized_action`: `RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED`
  → `RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED`; entrada literal acrescentada
  ao allowlist do `labctl`, sem wildcard.
- `GAP-RH-004` fechado (`CLOSED_BY_FORMALIZATION`).

### Verified

- `lake build` PASS (8.691 jobs); teste isolado PASS; tokens proibidos zero.
- `#print axioms`: apenas `propext`, `Classical.choice`, `Quot.sound`.
- pytest 2 passed; `labctl validate` PASS.
- `ASYM_NOGO_001_VERIFIED`.

### Blocked

- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`; a ponte
  para Riemann–von Mangoldt e para a lei de Weyl depende de leitura
  primária (GAP-RH-002, GAP-RH-003).
- Nenhuma claim sobre a Hipótese de Riemann foi promovida.

## RH-NOGO-001 (especificação) — 2026-07-31

### Added

- Especificação completa da frente em `03_MILLENNIUM/01_RIEMANN/`:
  `OPERATOR_CLASS.md` (Classe W, W1–W8), `TARGET_RESULT.md` (enunciado
  candidato em três níveis), `DEFINITIONS.md` (as 14 questões obrigatórias
  respondidas), `ASSUMPTIONS.md`, `ASYMPTOTIC_CORE.md` (sublema
  `ASYM-NOGO-001` com análise de casos e estratégia), `EXCLUSIONS.md`,
  `ESCAPE_ROUTES.md` (14 rotas não cobertas), `BIBLIOGRAPHY_AUDIT.md`
  (8 fontes classificadas), `CLAIM_MATRIX.md`
  (ESTABLISHED/CONDITIONAL/PROPOSED/OUT_OF_SCOPE), `LEAN_FEASIBILITY.md`,
  `STOP_CONDITIONS.md`, `GAP_REGISTER.yaml` (GAP-RH-001..008),
  `DEPENDENCY_DAG.yaml`, `LEAN_MAP.md`, `PROOF_SKETCH.md` (sem execução).
- `05_FORMAL/lean/TamesisLab/RHNogo/SignatureProbe.lean`: `Prop` do núcleo
  abstrato **sem corpo probatório** + `#check` das ferramentas Mathlib
  previstas. Compila (`lake build` 8.684 jobs).

### Changed

- `authorized_action`: `RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED` →
  `RH_NOGO_ASYMPTOTIC_LEMMA_FORMALIZATION_AUTHORIZED` (entrada literal
  acrescentada ao allowlist do `labctl`; sem wildcard).
  `RH_NOGO_PROOF_EXECUTION` **não** foi autorizado.
- `RH-NOGO-001` permanece `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`;
  acrescentado `specification_status: SPECIFICATION_READY` na fila.

### Verified

- Fontes: Riemann 1859, von Mangoldt 1905, Bombieri/Clay, Hörmander 1968,
  Berry–Keating 1999, Connes 1999, Bender–Brody–Müller 2017 e o preprint
  Hedenmalm 2026 (existência confirmada em listagem arXiv nesta sessão;
  classificado como preprint não revisado, em
  `CLAIMS_REQUIRING_INDEPENDENT_AUDIT`).
- Ferramentas assintóticas presentes na Mathlib fixada
  (`isLittleO_log_rpow_atTop`, `tendsto_log_atTop`, `rpow`, `IsLittleO`).
- `RH_NOGO_001_SPECIFICATION_READY`.

### Blocked

- Prova do no-go completo: bloqueada por GAP-RH-002 (transcrição da versão
  exata da lei de Weyl de Hörmander 1968) e sem autorização.
- Nenhuma claim científica foi criada ou promovida neste gate.

## FOUND-SEMIGROUP-001 — 2026-07-31

### Added

- Frente de semigrupos formalizada:
  `TamesisLab/Foundations/Semigroups/{Basic,Regime3,Theorems,Action,Audit}.lean`,
  agregador `Semigroups.lean` e teste `Tests/FoundSemigroup001.lean`.
- Modelo C3: `Regime3` (3 regimes), `Shift3` (3 transições),
  `Shift3.apply`, `Shift3.comp`; 12 teoremas FOUND-SG-002..013
  (associatividade, identidades, lei da ação, ciclo, cardinalidades,
  distinção, fidelidade, transitividade); FOUND-SG-001 (fechamento)
  registrado como garantido por construção.
- Instâncias `Monoid Shift3` e `MulAction Shift3 Regime3` criadas após as
  leis; camada abstrata reutiliza `SemigroupAction`/`MulAction` da Mathlib
  — nenhuma duplicata local (stop condition respeitada).
- Documentação da frente `02_FOUNDATIONS/03_SEMIGROUPS/`:
  TARGET_RESULT, DEFINITIONS (convenção de composição explícita),
  ASSUMPTIONS, KNOWN_RESULTS_MATRIX (separação álgebra padrão / modelo C3 /
  vocabulário Tamesis não justificado), DEPENDENCY_DAG, GAP_REGISTER,
  LEAN_MAP, THEOREM_MAP.
- Auditoria computacional
  `06_COMPUTATION/python/experiments/found_semigroup_001_audit.py`
  (`COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY`): 7 verificações exaustivas PASS
  e 4 fixtures negativas com falha esperada observada (não associatividade,
  ação incompatível, não transitividade, não fidelidade).
- Claim `FOUND-SG-FORMAL-001` (`F`, `formal_foundations`, VERIFIED); nenhuma
  claim científica promovida.

### Changed

- `FOUND-SEMIGROUP-001`: `READY` → `VERIFIED`.
- `active_work_item`: `FOUND-SEMIGROUP-001` → `RH-NOGO-001` (`SCOPED`), com
  autorização exclusiva de preparação
  (`RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`); a execução da prova
  permanece `NOT_AUTHORIZED / NO_EXECUTION`.
- `labctl`: entradas literais `RH_NOGO_SPECIFICATION_PREPARATION_AUTHORIZED`
  no allowlist e `RH-NOGO-001` como item ativo condicionado a
  `FOUND-SEMIGROUP-001` `VERIFIED`; sem wildcard.
- Instâncias `Fintype` de `Regime3`/`Shift3` escritas manualmente: o derive
  handler da revisão fixada falha sob imports mínimos (registrado em
  `LEAN_MAP.md`).

### Verified

- `lake build` PASS, 8.683 jobs; teste isolado PASS; tokens proibidos zero.
- Auditoria Python PASS; pytest 2 passed; `labctl validate` PASS.
- `FOUND_SEMIGROUP_001_VERIFIED`.

### Blocked

- `RH-NOGO-001`: somente preparação autorizada; prova não autorizada.

## LAB-BENCH-001 — 2026-07-31

### Added

- Módulos Lean do benchmark: `TamesisLab/Benchmark/{Core,Structures,Relations,MathlibInterop}.lean`,
  agregador `TamesisLab/Benchmark.lean` e teste
  `TamesisLab/Tests/BenchmarkSmoke.lean` — 11 definições e 15 teoremas
  elementares conhecidos, todos referenciados no teste.
- Matriz de rastreabilidade `05_FORMAL/specifications/LAB-BENCH-001_THEOREM_MAP.md`
  ligando cada requisito BENCH-* a arquivo, assinatura e método de prova.
- Claim de infraestrutura `BENCH-INFRA-001` (`evidence_level: F`,
  `domain: formal_infrastructure`); nenhuma claim científica criada ou
  promovida.
- Skills locais de agente copiadas de `AJUSTE_FINO/` para `.claude/skills`
  (24 operacionais, 1 incompleta), fora do controle de versão via
  `.git/info/exclude`.

### Changed

- `LAB-BENCH-001`: `READY` → `VERIFIED`; todas as seis fases `PASS`.
- `active_work_item`: `LAB-BENCH-001` → `FOUND-SEMIGROUP-001` (`READY`);
  autorização passou a `FOUNDATIONS_EXECUTION_AUTHORIZED`.
- `labctl` atualizado para o novo estágio do gate: entrada literal
  `FOUNDATIONS_EXECUTION_AUTHORIZED` no allowlist; `FOUND-SEMIGROUP-001`
  aceito como item ativo somente com `LAB-BENCH-001` `VERIFIED`; `VERIFIED`
  do benchmark exige fases de execução e verificação `PASS`; fases de
  execução/verificação aceitam `NOT_STARTED` ou `PASS`, com verificação
  condicionada à execução.

### Verified

- `lake build` PASS com 8.676 jobs; `BenchmarkSmoke` PASS individual.
- Tokens proibidos: zero nos fontes do laboratório.
- pytest: 2 passed; `labctl validate`: PASS sem erros.
- `LAB_BENCH_001_VERIFIED`.

### Blocked

- `FOUND-SEMIGROUP-001`: `READY`, não executado nesta sessão.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.

## LAB-WSL-MIGRATION — 2026-07-31

### Changed

- O runtime canônico do laboratório passou de Windows nativo para Ubuntu 24.04
  no WSL2. Diretório canônico:
  `/home/linuxdev/projects/TamesisTheoryCompleteResearchArchive`.
- O par Lean/Mathlib canônico passou de `v4.32.2` para `v4.33.0-rc1`. Mathlib
  fixada em `79d0395a1825a6264ad5d269e35e60537518955e`. Nenhuma formalização
  científica dependia do par anterior.
- `05_FORMAL/lean/lean-toolchain` e `05_FORMAL/lean/lakefile.toml` foram
  alinhados ao par validado; `lake update mathlib` regenerou o manifesto.
- `LAB-BENCH-001` passou de `BLOCKED` para `READY`; a autorização passou a
  `LAB_BENCHMARK_EXECUTION_AUTHORIZED`.

### Corrected

- `labctl.lean_check` usava `USERPROFILE`, variável exclusiva do Windows, e não
  localizava o diretório de toolchains sob Linux. Passou a resolver
  `ELAN_HOME`, depois `USERPROFILE`, depois `HOME`.
- `labctl validate` não podia retornar `PASS` em nenhuma circunstância, porque
  exigia `lean_check()["status"] == "PASS"` e essa função só retornava
  `BLOCKED` ou `NOT_RUN`. O registro histórico `lab0-result.json` mostra
  `LAB0_LEAN_ENVIRONMENT_FAILED` com `errors: []`. `lean_check` passa a
  retornar `PASS` quando há toolchain estável não-`.tmp` resolvido no PATH,
  sem jamais invocar build.
- `LAB_STATE.canonical_commit` continha um SHA abreviado de 7 caracteres,
  violando o padrão de 40 exigido por `lab-state.schema.json`.
- O allowlist de `authorized_action` em `labctl` recebeu a entrada literal
  `LAB_BENCHMARK_EXECUTION_AUTHORIZED`, sem wildcard nem relaxamento genérico.

### Verified

- `LEAN_ENVIRONMENT_DISCOVERY: PASS`.
- `LEAN_TOOLCHAIN_AVAILABILITY: PASS` com toolchain definitivo.
- `LEAN_SMOKE_BUILD: PASS`: os três smokes de Mathlib compilaram.
- `LAB_BENCHMARK_PREPARATION: PASS`.
- `lake build` concluiu 8.670 jobs.
- Tokens proibidos nos fontes do laboratório: zero.

### Blocked

- `LAB_BENCHMARK_EXECUTION` e `LAB_BENCHMARK_VERIFICATION`: `NOT_STARTED`.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- A rota nativa Windows fica `FROZEN / HISTORICAL / NOT_OPERATIONAL` na tag
  `lab-native-windows-paused`.

## Unreleased

### Added

- Camada isolada `04_FORMAL_RESEARCH_LAB`.
- Estado canônico de retomada, governança, fila e mapas.
- Esqueletos formais Lean/Python sem alegações novas.
- Ferramenta de continuidade `labctl`.
- Especificação e estado de fases de `LAB-BENCH-001`.
- Benchmark documental de rastreabilidade de Poincaré.

### Changed

- O diagnóstico Lean separa smoke build de disponibilidade reprodutível.
- O benchmark de Poincaré está limitado a documentação histórica.

### Corrected

- `LAB-BENCH-001` deixou de ser classificado como `VERIFIED`: somente o smoke
  build passou.
- O `active_work_item` voltou de `RH-NOGO-001` para `LAB-BENCH-001`.
- A autorização foi reconciliada para
  `LAB_BENCHMARK_FORMALIZATION_PREPARATION_AUTHORIZED`.
- Um diretório `.tmp` deixou de ser tratado como toolchain canônico.
- A autoridade de documentos históricos permanece subordinada à precedência
  documental e às auditorias canônicas.

### Retracted

- Foi retirada a inferência operacional de que o smoke build concluiu
  `LAB-BENCH-001`.
- Nenhuma retratação matemática nova foi criada.

### Verified

- `LEAN_ENVIRONMENT_DISCOVERY: PASS`.
- `LEAN_SMOKE_BUILD: PASS` com 12 jobs usando Lean 4.32.2.
- O LAB-0 técnico e seus validadores permanecem `PASS`.

### Blocked

- `LEAN_TOOLCHAIN_AVAILABILITY: PARTIAL`: o toolchain definitivo não existe.
- `LAB_BENCHMARK_PREPARATION: PARTIAL`: revisão Mathlib ainda não fixada.
- `LAB_BENCHMARK_EXECUTION` e `LAB_BENCHMARK_VERIFICATION`: `NOT_STARTED`.
- `RH-NOGO-001`: `SCOPED / NOT_AUTHORIZED / NO_EXECUTION`.
- LAB-0.6 interrompido por `LAB06_RECONCILIATION_DIFF_UNRESOLVED`: o HEAD
  inicial não contém o laboratório e o resultado histórico do LAB-0 não pode
  ser recuperado por Git.
- Um processo externo criou `363be8a`; ele contém a camada formal e o artefato
  LAB-0.5, mas não é um commit exclusivo desta sessão.
- LAB-0.6 interrompido por `LAB_LEAN_TOOLCHAIN_INSTALLATION_FAILED` após o
  comando oficial do Elan expirar em 184 segundos.
- A instalação foi posteriormente concluída pelo Elan; o toolchain agora é
  definitivo e Mathlib está fixada no commit v4.32.2.
- O smoke import Mathlib excedeu 600 segundos em compilação local e o gate
  terminou como `LAB_MATHLIB_SMOKE_BUILD_FAILED`.
- LAB-0.7 confirmou checkout Mathlib compatível com o manifesto, mas o comando
  oficial `cache get` falhou com recurso ausente; o smoke direto acusou
  `MISSING_OLEAN` e o alvo isolado excedeu 600 segundos.
- LAB-0.7 terminou como `LAB07_CACHE_UNAVAILABLE_FOR_REVISION`; nenhum benchmark
  ou problema Clay foi executado.
- LAB-0.8 confirmou que `v4.32.2` é tag Mathlib oficial e compatível com o
  toolchain declarado, mas o cache falha com exceção Windows de processo antes
  de informar URL/HTTP. O probe isolado de `v4.32.1` reproduziu a falha.
- LAB-0.8 terminou como `LAB08_NO_REPRODUCIBLE_PAIR_FOUND`; nenhuma migração
  canônica foi executada.
- LAB-0.9 identificou que o erro Windows 2 vinha da chamada interna a
  `uname.exe`, ausente no PATH enquanto o cache avaliava curl 7.55.1.
- A precedência temporária de `Git/usr/bin` removeu o erro de criação de
  processo, mas os downloads curl permaneceram presos por 600 segundos; o gate
  terminou como `LAB09_CAUSE_STILL_UNRESOLVED`.
- LAB-0.10 separou o cURL Windows 7.55.1 do cURL Git 8.21.0 e confirmou que
  `Git/usr/bin` sozinho não altera a seleção do cURL.
- A precedência interna do cache passou a usar o cURL Git verificado; 398
  `.ltar` foram transferidos e a contagem `.olean` subiu para 1.173, mas 2.583
  objetos permaneceram `.part`/404 e a transferência não concluiu.
- LAB-0.10 terminou como `LAB010_CACHE_TRANSFER_STALLED`.
