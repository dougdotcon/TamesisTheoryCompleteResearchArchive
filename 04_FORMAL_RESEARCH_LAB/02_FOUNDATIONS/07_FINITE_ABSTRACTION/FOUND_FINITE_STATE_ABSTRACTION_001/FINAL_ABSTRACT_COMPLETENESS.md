---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-FINAL-ABSTRACT-COMPLETENESS
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
category: PUBLIC_SPECIFICATION_CORE
semantic_strength: ABSTRACT_EXISTENCE
---

# Completeness abstrata — final

## Assinatura medida por `#check`

```text
@analyzeAbstractSystem_complete :
  ∀ {C : Type u_3} {A : Type u_4} {stepC : C → C} {stepA : A → A} {n : ℕ}
    (abstraction : CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C),
  ∃ witness, analyzeAbstractSystem abstraction encoding start = Except.ok witness
```

## Verificações

```text
depende de OrbitSeparating           NAO
alega repeticao concreta             NAO
repete o detector                    NAO
escolha classica produzindo witness  NAO
witness permanece existencial em Prop SIM
pre-condicao exigida do consumidor   NENHUMA
```

## DAG confirmado

```text
analyzeEncodedSystem_complete
  → estado abstrato abstraction.abstract start
    → mesmo witness existencial
```

Um termo. A completeness da frente anterior é consumida **sem
adaptação**: o único trabalho é abstrair o estado inicial.

## A leitura proibida

```text
"a analise abstrata e completa, logo todo sistema concreto tem ciclo"
```

Falsa. A completeness garante existência de witness **abstrato**. O
sistema concreto pode não repetir nunca — `BOOL_TO_UNIT` com `C = Bool`
repete, mas nada no teorema depende disso, e `C` pode ser infinito.

```text
STOP-ABS-018 disparada   NAO
```

## Complemento honesto

O witness existe sempre porque `A` é finito, por `CertifiedFiniteEncoding
A n`. A finitude que produz o witness é a de `A`, nunca a de `C`.
