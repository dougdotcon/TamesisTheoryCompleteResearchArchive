---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-SPECIFICATION-REVIEW
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
review_start_head: 4c7c11dbf655edc61d75d1eb99f690dea9750a84
decision: FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_REVIEW_APPROVED
defects_found: 5
defects_corrected: 5
declarations_before: 28
declarations_after: 29
---

# Revisão de especificação

## Reexecução

O probe foi **rodado de novo neste gate**, já com as correções.

```text
REAL_REPROBE_EXIT   0
error_lines         0
warning lines       0
git_dirty           0
declaracoes         29   derivadas por script, PARTITION_OK
pegada medida       29/29
```

## Os quatro defeitos

### 1. Contagem de instâncias — afirmação FALSA

```text
declarado    "primeira frente do laboratorio com instance_declarations != 0"
derivado     22 instancias ja existem na biblioteca, em 6 arquivos
```

`CycleWitness.decidableValid`, `Fintype Regime3`, `Monoid Shift3`,
`MulAction Shift3 Regime3` e as instâncias dos contraexemplos de
`FiniteDynamics` e `FunctionalGraphs` são anteriores a esta frente.

**Terceiro defeito de contagem agregada em três frentes consecutivas** —
e o primeiro que não é aritmético, e sim uma afirmação de primazia
publicada sem ser derivada. A regra `aggregate_counts` fala de contagens;
esta era uma contagem disfarçada de adjetivo.

Correção: a afirmação foi removida e substituída pela contagem derivada.

### 2. `typeclasses_required_of_consumer: 0` — impreciso

O caminho principal não exige nada: `primrec_analyzeEncodedSystem`
recebe as instâncias do próprio `ResultCodes.lean`. Mas
`primrec_of_encoding` é genérico em `σ` e **exige `[Primcodable σ]` do
chamador**.

Corrigido para dois campos, que não podem ser lidos um pelo outro:

```yaml
typeclasses_required_on_main_path: 0
typeclasses_required_by_generic_lemma: 1
```

### 3. `boolEncoding_bound_concrete` — teste que não testava

```lean
(⟨0, 2⟩ : CycleWitness).baseIndex + (⟨0, 2⟩ : CycleWitness).period ≤ 2
```

O enunciado reduz a `0 + 2 ≤ 2` e é decidível por avaliação. Ele passaria
com o teorema da cota **removido**. O termo de prova exercitava
`analyzeEncodedSystem_bound`, mas o enunciado não obrigava a isso.

Substituído por uma forma quantificada, que não é decidível por
avaliação:

```lean
theorem boolEncoding_bound_applies :
    ∀ w : CycleWitness, analyzeEncodedSystem boolEncoding not true = .ok w →
      w.baseIndex + w.period ≤ 2
```

### 4. A instância induzida não é canônica — OMISSÃO

`Primcodable Bool` **já existe no Mathlib**, e
`encodingPrimcodable boolEncoding` é uma instância **diferente**. O
enunciado `boolEncoding_primrec` vale sob a instância da frente, e um
leitor desatento o leria como se fosse sob a canônica.

Nada é falso, mas a especificação não declarava o risco. Corrigido em
três lugares:

- `CB-GAP-010`, nova;
- `STOP-CB-013`, nova;
- e um teste novo que resolve a questão em vez de só avisar:

```lean
theorem boolEncoding_primrec_canonical :
    Primrec (analyzeEncodedSystem boolEncoding not) :=
  Primrec.dom_finite _
```

Sob a instância **canônica** do Mathlib a conclusão é a mesma, e a prova
é a mesma linha. Isso não é um detalhe: é o resultado central visto de
outro ângulo — **a codificação não importa porque quem faz o trabalho é a
finitude**.

### 5. Chave YAML duplicada — pega pelo validador, dentro do gate

`STATUS.yaml` passou a ter `specification_review` **duas vezes**: como
campo de status no topo (`APPROVED`) e como bloco do registro da revisão.
`labctl validate` recusou com `DUPLICATE_YAML_KEY ... classification=
DIVERGENT_DUPLICATE`, apontando linha e primeira definição.

O bloco foi renomeado para `specification_review_record`. A regra
`yaml_duplicate_keys` existe desde `LAB-GOV-YAML-DUPLICATE-KEYS-001` e
**cobrou** — o defeito nasceu e morreu dentro do mesmo gate, antes do
commit.

## Pegada, medida agora

```text
SEM AXIOMA (9)   as 4 equivalencias, isEmpty_of_encoding_zero,
                 as 2 codificacoes TEST_ONLY, boolEncoding_nonempty,
                 emptyEncoding_isEmpty

propext, Classical.choice, Quot.sound (20)   todas as demais
```

Cobertura `29/29`. Bate com o esperado.

## Os dez itens

| # | Item | Veredito |
|---|---|---|
| 1 | `CertifiedFiniteEncoding` é um `S ≃ Fin n` | CONFIRMADO |
| 2 | `Primcodable.ofEquiv` se aplica direto | CONFIRMADO |
| 3 | O resultado central está enunciado como NEGATIVO | CONFIRMADO |
| 4 | `primrec_of_encoding` não consulta `f` | CONFIRMADO |
| 5 | A cota é do certificado, não de recursos | CONFIRMADO |
| 6 | O nível uniforme elabora e não é afirmado | CONFIRMADO |
| 7 | Instância positiva em tipo habitado, `n = 2` | CONFIRMADO |
| 8 | Nenhuma frente encerrada é tocada | CONFIRMADO |
| 9 | Contagem de instâncias | **CORRIGIDO** |
| 10 | Canonicidade da instância induzida | **CORRIGIDO** |
| 11 | Chaves YAML únicas em `STATUS.yaml` | **CORRIGIDO** |

## O item 3, que é o que a revisão tinha de proteger

A tentação desta frente é vender a ponte como conquista. O revisor
procurou, especificamente, qualquer frase que sugerisse que
`Primrec (analyzeEncodedSystem ...)` diga algo sobre a busca limitada.

Não há nenhuma. `README.md`, `SPECIFICATION_DECISION.md` e
`STOP_CONDITIONS.md` afirmam o contrário, nessa ordem, e
`boolEncoding_primrec_canonical` agora demonstra o ponto em Lean.

## Verificação anti-regressão

```text
mencoes a Computable/Partrec/Turing sob TamesisLab    0  (ainda)
ocorrencias da reducao do bloco do                    2  (a terceira e desta frente)
arquivos de frente encerrada modificados              0
sorry, admit, axioma local                            0
```

## Decisão

`FOUND_COMPUTABILITY_BRIDGE_001_SPECIFICATION_REVIEW_APPROVED`.

As 19 assinaturas públicas seguem congeladas — nenhuma foi alterada pelos
quatro defeitos, que atingiram documentação, um teste e uma omissão de
lacuna. Segue para formalização.
