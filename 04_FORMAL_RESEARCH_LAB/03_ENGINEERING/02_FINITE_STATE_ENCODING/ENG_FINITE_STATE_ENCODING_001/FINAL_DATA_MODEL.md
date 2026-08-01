---
document_id: ENC-FINAL-DATA-MODEL
supersedes: ENC-DATA-MODEL
stage: SPECIFICATION_REVIEW
frozen: true
---

# Modelo de dados final

## A estrutura, congelada

```lean
structure CertifiedFiniteEncoding (S : Type*) (n : Nat) where
  encode : S → Fin n
  decode : Fin n → S
  decode_encode : ∀ s : S, decode (encode s) = s
  encode_decode : ∀ i : Fin n, encode (decode i) = i
```

Inalterada em relação à especificação. Confirmada por compilação.

## Ausências verificadas no probe

```text
[Fintype S]      ausente
[Finite S]       ausente
[DecidableEq S]  ausente
[Nonempty S]     ausente
[Inhabited S]    ausente
```

Nenhuma das dezesseis declarações menciona qualquer typeclass sobre `S`.
`STOP-ENC-015` e `STOP-ENC-016` não dispararam.

A estrutura também não armazena `Array`, `stepS`, estado inicial,
`CycleWitness`, `stateCount` redundante nem resultado de análise. O
tamanho é o parâmetro `n`.

## Os papéis das duas leis — auditados separadamente

```yaml
decode_encode:
  role: PROOF_DEPENDENCY
  required_for:
    - CertifiedFiniteEncoding.encode_injective
    - CertifiedFiniteEncoding.tableIndex_semiconj
    - analyzeEncodedSystem_sound
  measured: usada literalmente na prova da semiconjugacao

encode_decode:
  role: PUBLIC_CONTRACT
  required_for:
    - CertifiedFiniteEncoding.encode_surjective
    - cobertura exata de todo indice de Fin n por um estado de S
    - ausencia de linhas artificiais na tabela
    - equivalencia plena S ≃ Fin n
  proof_dependency_of_core_results: false
  measured_by: seccao WeakEncoding do probe, que compila sem ela
```

## A medição que sustenta a decisão

O probe contém uma estrutura `WeakEncoding` com apenas `decode_encode`, e
nela foram reprovados: `encodedStep`, `buildTable`, `buildTable_size`,
`buildTable_getElem`, `tableIndex`, `tableIndex_val`, `semiconj`,
`run?_corresponds`, `analyzeWeak` e `analyzeWeak_sound`. **Tudo
compilou.**

Conclusão registrada sem rodeio: `encode_decode` não é dependência de
prova. Ela é o contrato.

```text
com as duas leis:  n eh a cardinalidade de S, e a tabela representa
                   exatamente o sistema.

com uma lei so:    n eh apenas um limite superior, e a tabela pode ter
                   linhas que nao correspondem a estado nenhum.
```

A frente promete o primeiro. Trocar para o segundo seria outro contrato,
e o gate é explícito: **outra frente**.

## `Equiv` — decisão final

```yaml
primary_public_representation: CertifiedFiniteEncoding
optional_derived_view: CertifiedFiniteEncoding.toEquiv
toEquiv_formalization_in_v1: DEFERRED_OPTIONAL
```

Razões, todas verificadas: `encode`/`decode` são semanticamente claros;
as leis ficam visíveis na API; não há dependência de `Fintype.equivFin`;
a computação principal usa diretamente os quatro campos. `toEquiv` **não**
será formalizado na v1 — nenhum uso concreto foi demonstrado, e expô-lo
sem uso é inflar a API.
