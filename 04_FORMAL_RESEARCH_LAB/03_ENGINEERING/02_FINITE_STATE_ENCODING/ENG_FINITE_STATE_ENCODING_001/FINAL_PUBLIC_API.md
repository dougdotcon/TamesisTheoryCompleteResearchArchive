---
document_id: ENC-FINAL-PUBLIC-API
supersedes: ENC-PUBLIC-API-SPECIFICATION
stage: SPECIFICATION_REVIEW
frozen: true
public_declarations: 14
---

# API pública final

Quatorze declarações públicas, um auxiliar interno, seis diferidas.
A especificação previa dezesseis públicas; a revisão moveu duas.

## `PUBLIC_EXECUTABLE_CORE` — cinco

```yaml
- CertifiedFiniteEncoding
- CertifiedFiniteEncoding.encodedStep
- buildTransitionTable
- CertifiedFiniteEncoding.tableIndex
- analyzeEncodedSystem
```

### A decisão sobre `encodedStep`

```yaml
declaration: CertifiedFiniteEncoding.encodedStep
category: PUBLIC_EXECUTABLE_CORE
axioms: nenhum
```

Critérios do gate, respondidos um a um:

```text
significado independente        SIM — eh a dinamica codificada Fin n -> Fin n
aparece em especificacao/teste  SIM — no enunciado do auxiliar e nos testes
util para comparar tabela e
  dinamica codificada           SIM — eh o unico nome publico do conteudo
evita reimplementacao           SIM — a composicao seria reescrita por todos
```

O critério contrário — *"só aparece no corpo de `buildTransitionTable`"* —
**não** se aplica: ele aparece também no enunciado do auxiliar de leitura
e, mais importante, com esse auxiliar agora interno, nenhuma outra
declaração pública seria capaz de dizer o que a tabela contém.

Registrado com honestidade: a justificativa que a **especificação** deu
para expô-lo caiu junto com a publicidade do auxiliar. Esta é uma
justificativa nova, não a mesma repetida.

## `PUBLIC_SPECIFICATION_CORE` — sete

```yaml
- CertifiedFiniteEncoding.encode_injective
- buildTransitionTable_size
- CertifiedFiniteEncoding.tableIndex_val          # @[simp]
- CertifiedFiniteEncoding.tableIndex_semiconj     # teorema semantico PRINCIPAL
- CertifiedFiniteEncoding.table_iterate_commutes
- CertifiedFiniteEncoding.run?_corresponds_to_typed_iterate
- analyzeEncodedSystem_sound
- analyzeEncodedSystem_complete
```

## `PUBLIC_COROLLARY` — dois

```yaml
- CertifiedFiniteEncoding.table_step_commutes   # (semiconj s).symm
- analyzeEncodedSystem_ne_error                 # quantificado sobre err
```

## `INTERNAL_HELPER` — um

```yaml
declaration: buildTransitionTable_getElem
category: INTERNAL_HELPER
visibility: private
role: "primeiro ponto de transporte; encanamento de leitura do Array.ofFn"
adds_mathematical_hypothesis: false
reason_for_demotion: >
  nao ha razao forte de reutilizacao externa; seu enunciado eh puro
  transporte, e a API publica ja diz tudo o que importa por meio da
  semiconjugacao e da correspondencia de run?, ambas livres de indice.
```

Mesma classificação que `analyze_reduce` recebeu na frente anterior, e
pelo mesmo motivo: encapsula uma redução, não uma afirmação.

## `DEFERRED_OPTIONAL` — seis

```text
CertifiedFiniteEncoding.toEquiv
CertifiedFiniteEncoding.encode_surjective
CertifiedFiniteEncoding.decode_surjective
CertifiedFiniteEncoding.decode_injective
exclusoes individuais dos tres construtores de erro
positive_size_of_state
```

`encode_surjective` merece nota: ela é a consequência de uma linha que
**exprime** o contrato de `encode_decode`, e foi provada no probe
(`Function.RightInverse.surjective`, sem axiomas). Fica diferida porque o
contrato já está enunciado na própria lei da estrutura; expor a
consequência é conveniência, não necessidade.

## Namespace

Todas as declarações sobre a codificação ficam sob
`CertifiedFiniteEncoding.`. Fora dele permanecem apenas
`buildTransitionTable`, `buildTransitionTable_size`,
`buildTransitionTable_getElem` e a família `analyzeEncodedSystem*` — que
falam da tabela e da análise, não da codificação.

## Ausências confirmadas

```text
stateCount                                  NAO existe
buildRawTransitionTable                     NAO existe
buildValidatedTransitionTable               NAO existe
transitionArray                             NAO existe
segunda orientacao do tamanho               NAO existe
segundo tableIndex sobre Fin n              NAO existe — encode ja o eh
segunda funcao de execucao                  NAO existe
novo construtor de erro                     NAO existe
CLI, parser, JSON, IO                       NAO existem
```
