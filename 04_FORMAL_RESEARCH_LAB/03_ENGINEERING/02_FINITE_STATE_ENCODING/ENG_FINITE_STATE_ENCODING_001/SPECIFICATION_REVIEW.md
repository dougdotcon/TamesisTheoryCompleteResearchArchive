---
document_id: ENC-SPECIFICATION-REVIEW
stage: SPECIFICATION_REVIEW
decision: A_SPECIFICATION_REVIEW_APPROVED
reviewed_at_commit: 2066edc165ace0fbf4e183303e30c4ced246aaaa
corrections_applied: 5
stop_conditions_triggered: 0
---

# Revisão da especificação

## As três perguntas que o gate mandou decidir

### 1. `encode_decode` permanece necessário?

**Sim — mas não pelo motivo que a especificação sugeria.**

A auditoria foi feita por construção, não por leitura: o probe contém uma
seção `WeakEncoding` com **apenas** `decode_encode`, e nela a cadeia
inteira foi reprovada — tabela, tamanho, leitura, índice, preservação do
valor, semiconjugação, correspondência de `run?`, análise dinâmica e
**soundness tipada**. Tudo compilou.

```text
encode_decode NAO eh dependencia de prova de nenhum resultado CORE.
```

E ainda assim ela **fica**, porque é a única coisa que sustenta a
promessa pública da frente:

```text
com as duas leis:   encode eh bijetiva; TODO indice de Fin n eh um
                    estado real; a tabela representa exatamente o
                    sistema, e n eh a cardinalidade de S.

com uma lei so:     encode eh apenas injetiva; podem existir indices
                    fora da imagem; a tabela eh um SUPERCONJUNTO com
                    linhas que nao correspondem a estado nenhum.
```

O segundo contrato — imersão de `S` numa tabela maior — é uma frente
diferente, com outro enunciado e outro nome. Enfraquecer a estrutura para
`LeftInverse` silenciosamente seria trocar o contrato sem dizer.

```yaml
decode_encode:
  role: PROOF_DEPENDENCY
  required_for: [encode_injective, semiconj, typed soundness]
encode_decode:
  role: PUBLIC_CONTRACT
  required_for: [encode_surjective, exact coverage, absence of artificial rows]
  proof_dependency_of_core_results: false
```

### 2. `encodedStep` é API pública ou auxiliar interno?

**`PUBLIC_EXECUTABLE_CORE`**, e a razão mudou em relação à
especificação.

A especificação justificava a exposição dizendo que `encodedStep` aparece
no enunciado de `buildTransitionTable_getElem`, que era público. Esta
revisão torna `buildTransitionTable_getElem` **interno**, de modo que
aquele argumento caiu.

O argumento que sobrevive é outro, e é suficiente: com o lema de leitura
interno, `encodedStep` passa a ser **o único nome público capaz de
descrever o conteúdo da tabela**. Sem ele, nada na API pública diz o que
`next[i]` contém. Ele tem significado independente — é a dinâmica
codificada `Fin n → Fin n` —, é uma composição que todo consumidor
reescreveria, e **não depende de axioma nenhum**.

### 3. A pegada axiomática herdada é aceitável?

**`ACCEPT_INFRASTRUCTURAL_AXIOM_FOOTPRINT`.** Três medições sustentam a
decisão; ver `AXIOM_FOOTPRINT_REVIEW.md`.

## Correções aplicadas por esta revisão

| # | Item | Antes | Depois |
|---|---|---|---|
| 1 | `tableIndex_semiconj` | `PUBLIC_SPECIFICATION_CORE` empatado com a comutação | **teorema semântico principal**, provado diretamente |
| 2 | `table_step_commutes` | `PUBLIC_SPECIFICATION_CORE` | **`PUBLIC_COROLLARY`**, agora `(semiconj s).symm` |
| 3 | `buildTransitionTable_getElem` | `PUBLIC_SPECIFICATION_CORE` | **`INTERNAL_HELPER`** |
| 4 | `tableIndex_val` | teorema simples | **`@[simp]`** |
| 5 | nomes | mistos, fora do namespace | **todos sob `CertifiedFiniteEncoding.`**, exceto `buildTransitionTable*` e `analyzeEncodedSystem*` |

A inversão de 1 e 2 tem consequência prática: a semiconjugação passou a
ser **provada diretamente**, e a comutação virou um `.symm` de uma linha —
o inverso do que a especificação previa. O probe confirmou que a prova
direta da semiconjugação é igualmente curta.

## O que foi confirmado sem alteração

```text
a codificacao eh dado fornecido, nunca derivada;
zero typeclasses exigidas do consumidor;
uma unica construcao publica da tabela;
validade por construcao, sem revalidar;
orientacao unica size = n;
exatamente DOIS pontos de transporte;
tableIndex_val por rfl;
decode_encode eh a lei da comutacao;
iteradas por Semiconj.iterate_right, sem inducao;
soundness termina em igualdade sobre S;
completeness sem pre-condicoes;
um unico corolario de erro, quantificado;
caso vazio coerente e nao habitado para analise.
```

## Novo limite registrado

```yaml
encoding_invariance_of_concrete_witness:
  status: OPEN_DEFERRED
  gap: ENC-GAP-020
  stop_condition: STOP-ENC-019
```

Duas codificações corretas do mesmo sistema **não** produzem
necessariamente o mesmo `Array`, o mesmo `baseIndex`, o mesmo `period`
nem o mesmo primeiro witness na ordem de busca. Medido: com a codificação
identidade a tabela é `#[1,2,3,2]`; com `i ↦ 3 - i` é `#[1,0,1,2]`. Os
dois witnesses coincidiram em `⟨2,2⟩` — **coincidência observada, não
teorema**, e o gate proíbe elevá-la a afirmação.

O que **é** preservado por qualquer codificação correta é a validade
**semântica** do witness no sistema tipado, e isso é exatamente
`analyzeEncodedSystem_sound`.

## Evidência

```text
probe principal   exit 0, 33 s, zero erros, zero tokens proibidos
probe de axiomas  exit 1 por desenho: contem as tentativas da rota leve
probes removidos  sim
lake build        NAO executado
```

Dezesseis declarações reprovadas no probe principal, mais a seção
`WeakEncoding` completa e os oito testes concretos.

## Decisão

```text
A. ENG_FINITE_STATE_ENCODING_001_SPECIFICATION_REVIEW_APPROVED
```

Zero stop conditions disparadas. A formalização está autorizada.


---

## Correção de validação — `ENC-VAL-001`

O registro original permanece intacto acima. Acrescenta-se:

O probe de axiomas daquele gate terminou com `exit 1`, porque continha
experimentos negativos intencionais no mesmo arquivo da auditoria
obrigatória. A decisão A era correta no mérito e **não** mudou, mas só
passou a ser integralmente válida após o gate corretivo, no qual os dois
probes terminaram com `exit 0`.

```text
main_probe_exit   0
axiom_probe_exit  0
```

Nenhuma decisão técnica desta revisão foi alterada.
