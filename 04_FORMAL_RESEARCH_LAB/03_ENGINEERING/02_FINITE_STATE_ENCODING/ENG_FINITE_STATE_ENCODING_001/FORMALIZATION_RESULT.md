---
document_id: ENC-FORMALIZATION-RESULT
formalized_at_commit: bdc67fb9481743a7463ae4b61faa9bc7dca9e5dd
structures: 1
definitions: 4
theorems: 11
private_theorems: 1
instances: 0
lines: 450
test_lines: 298
lake_build_jobs: 8757
---

# Resultado da formalização

## O que existe agora

```text
sistema deterministico tipado S
    |  codificacao FORNECIDA e certificada
Fin n
    |  Array.ofFn
ValidatedTransitionTable
    |  runtime adapter verificado, sem copia
CycleWitness
    |  interpretacao semantica
stepS^[b + p] start = stepS^[b] start,  em S
```

## Números

```text
estruturas          1
definicoes          4
teoremas           11   (1 privado)
instancias          0
linhas Lean       450   (frente) + 298 (testes)
modulos             5   + agregador
testes              3
lake build       PASS, 8757 jobs, 120 s
```

A frente anterior custou `869` linhas; esta, `450`. A diferença é
reutilização: nada do detector nem da execução bruta foi reescrito.

## Ordem de dependência

```text
Encoding.lean
  └─ TableConstruction.lean
       └─ Commutation.lean
            └─ DynamicAnalysis.lean
```

Cinco arquivos, um import cada, mais o agregador e o `Audit.lean`.

## O que compilou na primeira tentativa

**Todos os quatro módulos.** A revisão havia demonstrado a cadeia inteira
em probe descartável, e a formalização apenas a tornou permanente. O
único ajuste foi trocar `simpa using (tableIndex …).isLt` — que o linter
apontou como `simpa` desnecessário — pela rota explícita
`rw [buildTransitionTable_size]; exact (encode start).isLt`.

## Correção de contagem

`FINAL_PUBLIC_API.md` declarava `public_declarations: 14`, mas listava
**quinze** declarações: cinco executáveis, oito de especificação e dois
corolários. O número correto, medido nos módulos, é:

```text
declaracoes publicas   15
auxiliares internos     1
```

Erro de cabeçalho no documento de revisão, sem qualquer efeito sobre a
API. Registrado em vez de silenciado.

## Testes

```text
Commutation.lean isolado        exit 0
DynamicAnalysis.lean isolado    exit 0
EngFiniteStateEncoding001       exit 0
...Execution                    exit 0
...Axioms                       exit 0
```

Cinco de cinco. Nenhum arquivo obrigatório contém declaração destinada a
falhar — a regra que `ENC-VAL-001` deixou.

## O que **não** foi formalizado

```text
toEquiv;
decode_surjective, decode_injective, encode_surjective;
positive_size_of_state;
exclusoes individuais de erros;
invariancia do witness concreto sob recodificacao;
minimalidade, unicidade;
modelo de custo, benchmark;
extracao, CLI, parser, JSON, rede, integracao;
correcao de um sistema externo especifico.
```
