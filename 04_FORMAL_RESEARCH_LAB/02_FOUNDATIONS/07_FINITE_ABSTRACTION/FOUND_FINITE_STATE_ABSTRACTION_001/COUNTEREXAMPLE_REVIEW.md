---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-COUNTEREXAMPLE-REVIEW
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
status: FROZEN
naive_cycle_reflection: FALSE
counterexample_orbit_separating: FALSE
---

# Revisão do contraexemplo

## As quatro obrigações, todas cumpridas

```text
1  a semiconjugacao VALE                       boolToUnit_semiconj
2  a recorrencia abstrata VALE                 rfl, periodo 1
3  a recorrencia concreta NAO vale             decide
4  OrbitSeparating FALHA                       boolToUnit_not_orbitSeparating
```

Todas as quatro, mais a codificação `CertifiedFiniteEncoding Unit 1`,
compilam **sem depender de axioma nenhum**.

## A análise abstrata executa

```lean
example : analyzeAbstractSystem boolToUnitAbstraction unitEncoding false
    = .ok ⟨0, 1⟩ := by decide
```

Witness compatível com repetição abstrata de período `1`, como exigido.

Registro honesto: `⟨0, 1⟩` é **observação de teste**. Nada é afirmado
sobre minimalidade, unicidade ou invariância sob recodificação — a
última é explicitamente `ENC-GAP-020`, de outra frente, e continua
aberta.

## O resultado negativo é um teorema que compila

```lean
theorem boolToUnit_not_orbitSeparating :
    ¬ OrbitSeparating forgetBool concreteStep false :=
  fun hsep => boolToUnit_no_concrete_recurrence (hsep 1 0 rfl)
```

Índices `0` e `1`, como especificado. DAG:

```text
observacoes abstratas iguais       forgetBool _ = forgetBool _, por rfl
→ OrbitSeparating produziria estados concretos iguais
→ concreteStep false = false
→ contradicao com decide
```

Nenhum arquivo deliberadamente inválido foi criado. A regra
`mandatory_probe_exit_code` do laboratório é respeitada: o experimento
negativo é uma **negação provada**, e vive no mesmo arquivo que os
probes obrigatórios sem comprometer o `exit 0`.

## A generalização, também teorema

```lean
theorem naive_cycle_reflection_is_false :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Semiconj abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start)
```

`does not depend on any axioms`.

## Leitura correta

```text
O contraexemplo NAO denuncia defeito da semiconjugacao.

Ele exibe a perda de informacao que uma abstracao existe para
produzir, e mede a forca exata do resultado observacional.
```

```text
STOP-ABS-002 disparada   NAO
```
