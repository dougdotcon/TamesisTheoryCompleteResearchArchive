---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-SPECIFICATION-DECISION
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
specification_status: READY_FOR_REVIEW
formalization_status: NOT_STARTED
---

# Decisões congeladas da especificação

Nada neste documento é prova. Todas as assinaturas abaixo foram
compiladas em probe descartável antes de serem congeladas — ver
[`PROBE_RESULT.md`](PROBE_RESULT.md).

## D-01 — Representação da abstração

```lean
structure CertifiedFiniteAbstraction
    (C A : Type*)
    (stepC : C → C)
    (stepA : A → A) where
  abstract : C → A
  commutes :
    Function.Semiconj abstract stepC stepA
```

Dois campos: um dado e uma lei. A estrutura **não** armazena
`CertifiedFiniteEncoding`, estado inicial, `CycleWitness`, resultado da
análise, `Array`, tabela, prova de `OrbitSeparating` nem concretização
`A → C`.

## D-02 — Abstração e codificação permanecem separadas

```text
abstracao possivelmente muitos-para-um   C → A
codificacao exata                        A ≃ Fin n
```

A codificação entra como argumento independente,
`encoding : CertifiedFiniteEncoding A n`. Fundi-las apagaria justamente
a distinção que a frente existe para provar.

## D-03 — Orientação da semiconjugação

```text
abstract (stepC c) = stepA (abstract c)
```

Congelada contra a assinatura real de `Function.Semiconj`, auditada em
[`SEMICONJUGATION_ORIENTATION.md`](SEMICONJUGATION_ORIENTATION.md).

## D-04 — Correspondência de iteradas por API oficial

Rota única: `abstraction.commutes.iterate_right`. Indução manual é
proibida enquanto a API oficial resolver o objetivo.

## D-05 — A soundness central termina em `A`

`analyzeAbstractSystem_observational_sound` conclui uma igualdade entre
`abstract` de dois estados concretos. Concluir igualdade em `C` sem
hipótese adicional dispararia `STOP-ABS-004`.

## D-06 — `OrbitSeparating` como contrato público primário

```lean
def OrbitSeparating
    (abstract : C → A)
    (stepC : C → C)
    (start : C) : Prop :=
  ∀ i j : Nat,
    abstract ((stepC^[i]) start) =
      abstract ((stepC^[j]) start) →
    (stepC^[i]) start =
      (stepC^[j]) start
```

## D-07 — `Set.InjOn` fica diferido

A equivalência com
`Set.InjOn abstract (Set.range fun k => (stepC^[k]) start)` foi
**provada em probe, sem axiomas**, e mesmo assim **não** entra na v1:
nenhum resultado central a consome. Classificação `DEFERRED_OPTIONAL`.
Ver [`ORBIT_SEPARATION.md`](ORBIT_SEPARATION.md).

## D-08 — A reflexão exige hipótese visível na assinatura

`analyzeAbstractSystem_reflected_sound` recebe `hSeparating` como
argumento explícito. Escondê-la dentro da estrutura dispararia
`STOP-ABS-005`.

## D-09 — Completeness é abstrata

`analyzeAbstractSystem_complete` afirma existência de witness. Ela não
afirma recorrência concreta e não depende de `OrbitSeparating`.
Descrevê-la como completeness concreta dispararia `STOP-ABS-018`.

## D-10 — Hipóteses negativas sobre os tipos

```text
Fintype C        NAO exigido
Finite C         NAO exigido
DecidableEq C    NAO exigido
Nonempty C       NAO exigido
Inhabited C      NAO exigido
Fintype A        NAO exigido
DecidableEq A    NAO exigido
```

A finitude executável de `A` vem **exclusivamente** de
`CertifiedFiniteEncoding A n`.

## D-11 — Reutilização integral da cadeia anterior

```text
CertifiedFiniteEncoding
analyzeEncodedSystem
analyzeEncodedSystem_sound
analyzeEncodedSystem_complete
CycleWitness
RuntimeCycleError
```

Nenhum detector é copiado, nenhum runtime adapter é copiado, nenhuma
segunda semântica de execução é criada, nenhum construtor de erro é
criado ou removido.

## D-12 — Identificador canônico

`FOUND-FINITE-STATE-ABSTRACTION-001`, forma de autorização
`FOUND_FINITE_STATE_ABSTRACTION_001_...`. Ver
[`IDENTIFIER_CANONICALIZATION_RECORD.md`](IDENTIFIER_CANONICALIZATION_RECORD.md).

## O que permanece fora

```text
bissimulacao
quocientes
relacao de simulacao geral
concretizacao γ : A → C
sistemas nao deterministicos
extracao
CLI, parser, JSON, rede
integracao externa
minimalidade ou unicidade do witness
invariancia do witness sob recodificacao
```
