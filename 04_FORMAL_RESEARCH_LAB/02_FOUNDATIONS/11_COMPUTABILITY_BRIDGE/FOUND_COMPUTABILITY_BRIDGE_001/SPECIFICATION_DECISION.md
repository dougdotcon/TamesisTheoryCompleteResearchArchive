---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION-DECISION
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
signatures_frozen: true
public_declarations: 19
public_definitions: 7
public_instances: 4
public_theorems: 8
private_helpers: 1
test_only_declarations: 2
tests: 7
declarations_total: 29
count_source: DERIVED_BY_SCRIPT
count_corrected_in_gate: FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION-REVIEW
typeclasses_required_on_main_path: 0
typeclasses_required_by_generic_lemma: 1
instance_declarations: 4
instance_declarations_preexisting_in_lab: 22
probe_exit: 0
probe_error_lines: 0
probe_warning_lines: 0
versioned_tree_touched: false
---

# Decisão de especificação — assinaturas congeladas

Todas compilaram em probe descartável, `exit 0`, zero `error:`, zero
`warning:`, árvore versionada intocada (`git_dirty=0`).

## Módulos

```text
Foundations/ComputabilityBridge.lean                agregador
Foundations/ComputabilityBridge/Encoding.lean       a ponte Primcodable
Foundations/ComputabilityBridge/ResultCodes.lean    codificar o resultado
Foundations/ComputabilityBridge/Classification.lean Primrec, Computable, o limite
Foundations/ComputabilityBridge/WitnessBound.lean   a cota do certificado
Foundations/ComputabilityBridge/Instance.lean       TEST_ONLY, instancia positiva
```

Cinco módulos de conteúdo mais um agregador.

## Encoding.lean — 2 definições, 2 teoremas

```lean
def encodingEquiv (e : CertifiedFiniteEncoding S n) : S ≃ Fin n

@[instance_reducible]
def encodingPrimcodable (e : CertifiedFiniteEncoding S n) : Primcodable S

theorem finite_of_encoding (e : CertifiedFiniteEncoding S n) : Finite S

theorem isEmpty_of_encoding_zero (e : CertifiedFiniteEncoding S 0) : IsEmpty S
```

`encodingPrimcodable` **não** é `instance`: ela toma um argumento
explícito, e registrá-la globalmente colocaria a resolução de instâncias
a procurar codificações. `@[instance_reducible]` existe porque sem ele o
Lean emite aviso de redutibilidade em definição de tipo classe — e a
frente termina com **zero avisos**.

`isEmpty_of_encoding_zero` é a armadilha de vacuidade, escrita antes de
alguém cair nela.

## ResultCodes.lean — 4 definições, 4 instâncias

O tipo de resultado do laboratório precisa ser codificável, ou o
enunciado central sequer é escrevível.

```lean
def cycleWitnessEquiv : CycleWitness ≃ (Nat × Nat)
instance instPrimcodableCycleWitness : Primcodable CycleWitness

def runtimeCycleErrorEquiv : RuntimeCycleError ≃ (Bool ⊕ (Nat × Nat))
instance instPrimcodableRuntimeCycleError : Primcodable RuntimeCycleError

def exceptEquiv (ε α : Type*) : Except ε α ≃ (ε ⊕ α)
instance instPrimcodableExcept [Primcodable ε] [Primcodable α] :
    Primcodable (Except ε α)

def rawTableEquiv : RawTransitionTable ≃ List Nat
instance instPrimcodableRawTransitionTable : Primcodable RawTransitionTable
```

`Bool ⊕ (Nat × Nat)` codifica os **três** construtores de
`RuntimeCycleError` sem perda: os dois sem argumento viram `false` e
`true`, e `initialStateOutOfBounds` guarda seus dois naturais. Nenhum
construtor é descartado, e o Mathlib não tem `Primcodable Unit` que
tornasse a soma tripla mais natural.

Quatro `instance` são declaradas. A biblioteca já tem **22**, em seis
arquivos — `CycleWitness.decidableValid`, `Fintype Regime3`,
`Monoid Shift3`, `MulAction Shift3 Regime3` e as dos contraexemplos.
Ambas as contagens são derivadas por script.

**A instância induzida não é canônica.** `Primcodable Bool` já existe no
Mathlib e é *diferente* de `encodingPrimcodable boolEncoding`. Enunciados
sob uma não são, sintaticamente, enunciados sob a outra. Ver
`CB-GAP-010`, `STOP-CB-013` e o teste `boolEncoding_primrec_canonical`,
que mostra que aqui a diferença não morde — porque quem faz o trabalho é
a finitude, não a codificação.

## Classification.lean — 1 definição, 4 teoremas

```lean
theorem primrec_of_encoding (e : CertifiedFiniteEncoding S n) {σ : Type*}
    [Primcodable σ] (f : S → σ) : Primrec f

theorem primrec_analyzeEncodedSystem (e : CertifiedFiniteEncoding S n)
    (stepS : S → S) : Primrec (analyzeEncodedSystem e stepS)

theorem computable_analyzeEncodedSystem (e : CertifiedFiniteEncoding S n)
    (stepS : S → S) : Computable (analyzeEncodedSystem e stepS)

theorem computablePred_of_encoding (e : CertifiedFiniteEncoding S n)
    (p : S → Prop) : ComputablePred p

def UniformPrimrecStatement : Prop := Primrec₂ analyzeTransitionTable
```

**`primrec_of_encoding` é a declaração central, e é negativa.** Seu corpo
é `Primrec.dom_finite f`: a finitude do domínio decide sozinha, e a
definição de `f` nunca é consultada. As duas seguintes são corolários de
uma linha, e é exatamente isso que elas demonstram — que a classificação
não contém informação sobre o algoritmo.

`UniformPrimrecStatement` é uma `def : Prop`, **não** um teorema. Ela
existe para provar que o enunciado uniforme **elabora**, localizando a
lacuna com precisão em vez de descrevê-la em prosa. Nenhum `sorry`,
nenhum axioma local: o que não está provado não está afirmado.

## WitnessBound.lean — 2 teoremas, 1 auxiliar privado

```lean
theorem analyzeTransitionTable_bound {raw : RawTransitionTable} {start : Nat}
    {w : CycleWitness} (h : analyzeTransitionTable raw start = .ok w) :
    w.baseIndex + w.period ≤ raw.next.size

theorem analyzeEncodedSystem_bound {e : CertifiedFiniteEncoding S n}
    {stepS : S → S} {start : S} {w : CycleWitness}
    (h : analyzeEncodedSystem e stepS start = .ok w) :
    w.baseIndex + w.period ≤ n
```

A cota é sobre o **certificado**: o testemunho cabe em `n`. Ela **não**
diz que a computação custa `n` passos, e afirmar isso está proibido —
não há modelo de custo.

```lean
private theorem analyze_reduce_cb {raw : RawTransitionTable} (hRaw : raw.Valid)
    {start : Nat} (hStart : start < raw.next.size) :
    analyzeTransitionTable raw start =
      (match ValidatedTransitionTable.detectCycle?
          (⟨raw.next, hRaw⟩ : ValidatedTransitionTable) ⟨start, hStart⟩ with
        | some witness => .ok witness
        | none => .error .internalDetectorFailure)
```

O auxiliar privado `analyze_reduce_cb` reproduz, com API exclusivamente
pública, a redução do bloco `do` que a frente do runtime mantém privada.
A assinatura está em bloco, e não só em prosa, porque o comparador
automático da revisão de resultado só enxerga blocos —
`RES-REV-CB-001`.
**É a terceira cópia** dessa redução no laboratório: a original é privada
em `FiniteStateRuntime/DynamicAnalysis.lean`, a segunda é privada em
`Monovariants/WitnessBounds.lean`. A duplicação está declarada, não
escondida, e a correção própria — alargar
`analyzeTransitionTable_sound` para devolver o contrato `Valid` inteiro —
exige gate sobre frente encerrada e **não está autorizada**. Ver
`CB-GAP-004`.

## Instance.lean — 2 TEST_ONLY, 7 testes

```lean
def boolEncoding : CertifiedFiniteEncoding Bool 2
def emptyEncoding : CertifiedFiniteEncoding Empty 0

theorem boolEncoding_nonempty : Nonempty Bool
theorem boolEncoding_analysis_concrete :
    analyzeEncodedSystem boolEncoding not true = .ok ⟨0, 2⟩
theorem boolEncoding_bound_applies :
    ∀ w : CycleWitness, analyzeEncodedSystem boolEncoding not true = .ok w →
      w.baseIndex + w.period ≤ 2
theorem boolEncoding_primrec : Primrec (analyzeEncodedSystem boolEncoding not)
theorem boolEncoding_primrec_canonical :
    Primrec (analyzeEncodedSystem boolEncoding not)
theorem boolEncoding_computable : Computable (analyzeEncodedSystem boolEncoding not)
theorem emptyEncoding_isEmpty : IsEmpty Empty
```

`boolEncoding_bound_applies` é **quantificada sobre `w`** de propósito. A
primeira versão enunciava `0 + 2 ≤ 2`, decidível por avaliação, e teria
passado com o teorema da cota removido do arquivo. Corrigido na revisão.

`boolEncoding_primrec` e `boolEncoding_primrec_canonical` diferem
**apenas** na instância `Primcodable Bool` usada — a da frente e a do
Mathlib. As duas provas têm uma linha, e é o mesmo ponto negativo visto
de outro ângulo.

**A instância positiva exigida pela governança.** `Bool` é habitado,
`n = 2 > 0`, e `boolEncoding_analysis_concrete` é decidida por avaliação
— não é uma hipótese assumida satisfazível, é o valor calculado.
`emptyEncoding_isEmpty` fica ao lado dela para que o contraste entre o
caso vácuo e o caso positivo esteja escrito no mesmo arquivo.

## Contagem congelada

```text
publicas             19   (7 definicoes, 4 instancias, 8 teoremas)
auxiliar privado      1
TEST_ONLY residentes  2   (definicoes)
testes                7   (teoremas)
total                29
```

Derivada por script sobre o arquivo do probe, com verificação de
partição (`PARTITION_OK`): a soma das partes é conferida contra o total
de declarações casadas, e não contra a memória de quem escreve.

## Pegada esperada

```text
SEM AXIOMA (9)
  encodingEquiv            cycleWitnessEquiv       exceptEquiv
  isEmpty_of_encoding_zero runtimeCycleErrorEquiv  boolEncoding
  emptyEncoding            boolEncoding_nonempty   emptyEncoding_isEmpty

propext, Classical.choice, Quot.sound (20)
  todas as demais
```

Medida por `#print axioms` sobre as **29** declarações — cobertura
`FULL`, não amostra. A primeira medição cobriu 20 de 28 e teria sido
publicada como se fosse integral; foi refeita antes do commit.

`Classical.choice` entra pela infraestrutura do Mathlib e por
`analyzeEncodedSystem`; sua remoção é explicitamente proibida.

Vale notar o que a lista mostra: **as quatro equivalências e as duas
codificações são livres de axioma**. O que traz pegada é sempre a
travessia para `Primcodable`/`Primrec`, nunca a ponte estrutural.

## Recorte

```text
nivel tipado, dominio finito       ESTA FRENTE
nivel uniforme, dominio infinito   ENUNCIADO, NAO PROVADO
classes de complexidade            NAO AUTORIZADAS
custo, complexidade assintotica    NAO AUTORIZADOS
maquinas de Turing, Nat.Partrec    NAO USADOS
P vs NP                            NAO TOCADO
typeclasses exigidas do consumidor 0
```

## O que NÃO é afirmado

```text
que a ponte certifique o algoritmo
que Primrec distinga o detector de uma tabela de consulta
que baseIndex + period <= n seja cota de recursos
que exista custo formalizavel sem modelo de maquina
que o laboratorio esteja pronto para PVSNP-PHYS-001
```
