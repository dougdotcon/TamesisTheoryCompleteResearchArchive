---
document_id: ENC-EMPTY-TYPE-POLICY
probe_status: PROBE_PROVED
---

# Política do tipo vazio

## O fato

```text
CertifiedFiniteEncoding S 0 exige encode : S -> Fin 0.
Fin 0 eh vazio, logo S tem de ser vazio.
```

Não é uma restrição imposta: é o que o tipo já diz.

## Nada é adicionado à estrutura

```text
0 < n           NAO adicionado
Nonempty S      NAO adicionado
Inhabited S     NAO adicionado
```

`STOP-ENC-017` dispara se a formalização adicionar `n > 0` à estrutura.

## Comportamento congelado

```yaml
empty_state_type_policy:
  encoding_structure: ALLOWED
  table_construction: ALLOWED
  table_structural_validity: VALID
  analysis_call: UNINHABITED
```

A codificação `Empty → Fin 0` foi construída no probe:

```lean
def emptyEnc : CertifiedFiniteEncoding Empty 0 where
  encode := fun s => s.elim
  decode := fun i => absurd i.isLt (Nat.not_lt_zero _)
  decode_encode := fun s => s.elim
  encode_decode := fun i => absurd i.isLt (Nat.not_lt_zero _)
```

e a tabela avaliou para:

```text
#eval (buildTransitionTable emptyEnc id).next   ->   #[]
```

A tabela vazia é estruturalmente válida — resultado já provado na frente
anterior como `valid_empty`, e aqui obtido por construção.

## Nenhuma chamada bem tipada de análise

```lean
analyzeEncodedSystem e stepS start   exige   start : S
```

Com `S` vazio, não existe `start`. **A ausência de chamada é garantida
pelo sistema de tipos, não por uma verificação em tempo de execução.**

Compare com a frente anterior: lá, a tabela vazia era válida e a consulta
era **rejeitada com erro**, porque o índice vinha como `Nat` e podia ser
qualquer coisa. Aqui a consulta é **impossível de escrever**. As duas
respostas são coerentes, e a diferença vem de onde a informação de
domínio está: em `Nat` sem garantia, ou em `S` com garantia.

## `0 < n` como corolário opcional

```lean
theorem positive_size_of_state (e : CertifiedFiniteEncoding S n) (s : S) : 0 < n
```

Rota: `e.encode s : Fin n`, depois `Fin.isLt`. Classificado
`OPTIONAL_ADAPTER`, **não** dependência central: onde a positividade é
necessária, `(e.encode s).isLt` já a fornece diretamente, e foi assim que
a completeness a usou no probe.
