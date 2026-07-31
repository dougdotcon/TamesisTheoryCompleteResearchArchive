# FOUND-FUNCTIONAL-GRAPH-001 — Plano de contraexemplos

Seis modelos. **Nada foi implementado neste gate.**

## Restrição de método descoberta na auditoria

`Function.periodicOrbit` está em `noncomputable section`
(`Dynamics/PeriodicPts/Defs.lean:240-490`). Consequência prática:

```text
`decide` NAO pode ser usado em enunciados sobre igualdade de orbitas.
```

Toda afirmação da forma `periodicOrbit f a = periodicOrbit f b` terá de ser
provada por `periodicOrbit_apply_iterate_eq`, não por computação finita.
Afirmações sobre `f`, `f^[n]` e pertinência a `periodicPts` continuam
decidíveis. Registrado em `FFG-GAP-011`.

---

```yaml
- id: FFG-CE-001
  claim_refuted: "todo grafo funcional finito possui um unico ciclo global"
  finite_type: "Fin 2 ou indutivo de dois construtores"
  transition_table: "a -> a ; b -> b"
  component_relation: >
    ¬ EventuallyMeets f a b — as trajetorias sao constantes e distintas
  periodic_points: "a e b, ambos"
  periodic_orbits: "periodicOrbit f a ≠ periodicOrbit f b"
  expected_lean_representation: >
    def f : St -> St := id (ou tabela explicita)
    example : ¬ EventuallyMeets f St.a St.b
    A negativa eh decidivel: reduz-se a ∀ m n, f^[m] a ≠ f^[n] b, e ambas
    as iteradas sao constantes.
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION

- id: FFG-CE-002
  claim_refuted: "todo estado eh periodico desde o inicio"
  finite_type: "tres estados"
  transition_table: "a -> b ; b -> c ; c -> c"
  component_relation: "EventuallyMeets f a c, com m = 2, n = 0"
  periodic_points: "somente c"
  periodic_orbits: "periodicOrbit f c; a e b dao Cycle.nil"
  expected_lean_representation: >
    example : a ∉ Function.periodicPts f
    example : IsTransient f a ∧ IsTransient f b ∧ IsRecurrent f c
    example : Function.periodicOrbit f a = Cycle.nil
      via periodicOrbit_eq_nil_iff_not_periodic_pt
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Reaproveita a forma de CE-003 de FOUND-SEMIGROUP-002, agora com o
    vocabulario transitorio/recorrente.

- id: FFG-CE-003
  claim_refuted: "todo ciclo eh um ponto fixo"
  finite_type: "dois estados"
  transition_table: "a -> b ; b -> a"
  component_relation: "EventuallyMeets f a b, com m = 1, n = 0"
  periodic_points: "a e b"
  periodic_orbits: "periodicOrbit f a, de comprimento 2"
  expected_lean_representation: >
    example : ¬ Function.IsFixedPt f St.a
    example : Function.IsPeriodicPt f 2 St.a
    example : St.a ∈ Function.periodicPts f
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION

- id: FFG-CE-004
  claim_refuted: "mesmo componente funcional implica alcancabilidade mutua"
  finite_type: "tres estados"
  transition_table: "a -> c ; b -> c ; c -> c"
  component_relation: >
    EventuallyMeets f a b  — testemunhas m = 1, n = 1, pois f a = c = f b
  periodic_points: "somente c"
  periodic_orbits: "periodicOrbit f c"
  expected_lean_representation: >
    example : EventuallyMeets f St.a St.b := ⟨1, 1, rfl⟩
    example : ¬ IterReachable f St.a St.b
    example : ¬ IterReachable f St.b St.a
    example : ¬ MutuallyReachable f St.a St.b
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    ESTE EH O CONTRAEXEMPLO DECISIVO DA FRENTE. Ele justifica a rejeicao
    de MutuallyReachable como definicao de componente (COMPONENT_NOTIONS.md)
    e eh a razao de a revisao da especificacao vir antes da formalizacao.

- id: FFG-CE-005
  claim_refuted: "cada componente possui exatamente um ponto periodico"
  finite_type: "dois estados"
  transition_table: "a -> b ; b -> a"
  component_relation: "EventuallyMeets f a b"
  periodic_points: "a e b, DISTINTOS"
  periodic_orbits: "periodicOrbit f a = periodicOrbit f b"
  expected_lean_representation: >
    example : St.a ≠ St.b
    example : St.a ∈ periodicPts f ∧ St.b ∈ periodicPts f
    example : Function.periodicOrbit f St.b = Function.periodicOrbit f St.a
      NAO por decide (noncomputavel), e sim por
      periodicOrbit_apply_iterate_eq ha 1, ja que b = f^[1] a.
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
  note: >
    Refuta a leitura errada de "um ciclo por componente" e CONFIRMA a
    leitura correta: o objeto unico eh a orbita, nao o representante.
    Mesmo sistema de CE-003, pergunta diferente.

- id: FFG-CE-006
  claim_refuted: "igualdade de periodo implica mesmo componente"
  finite_type: "quatro estados"
  transition_table: "a -> b ; b -> a ; c -> d ; d -> c"
  component_relation: "¬ EventuallyMeets f a c"
  periodic_points: "os quatro"
  periodic_orbits: >
    periodicOrbit f a ≠ periodicOrbit f c, embora
    minimalPeriod f a = minimalPeriod f c = 2
  expected_lean_representation: >
    example : ¬ EventuallyMeets f St.a St.c
    example : (periodicOrbit f St.a).length = (periodicOrbit f St.c).length
      via periodicOrbit_length
  scientific_value: COUNTEREXAMPLE_TO_OVERGENERALIZATION
```

---

## Cobertura

| Afirmação refutada | Contraexemplo |
|---|---|
| ciclo global único | `FFG-CE-001` |
| todo estado periódico desde o início | `FFG-CE-002` |
| todo ciclo é ponto fixo | `FFG-CE-003` |
| mesmo componente ⟹ alcançabilidade mútua | **`FFG-CE-004`** |
| um ponto periódico por componente | `FFG-CE-005` |
| mesmo período ⟹ mesmo componente | `FFG-CE-006` |

## Independência

Registrar na formalização, como em `FOUND-SEMIGROUP-002`:

```text
NAO foi provado que todas essas falhas ocorrem simultaneamente numa unica
funcao.

NAO foi provado que toda funcao finita exibe essas falhas.
```

Os seis modelos são independentes; `FFG-CE-003` e `FFG-CE-005` usam o mesmo
sistema com perguntas diferentes, e isso está declarado.

## Estratégia de codificação

Herdada de `FOUND-SEMIGROUP-002`, onde funcionou: tipos indutivos próprios
com `Fintype` manual (o derive handler falha sob imports mínimos nesta
revisão), provas por `decide` sobre poucos casos, **sem `native_decide`**.

Exceção obrigatória: igualdade de `periodicOrbit`, que exige
`periodicOrbit_apply_iterate_eq` em vez de `decide`.

Cada modelo em namespace próprio; nenhuma instância global.
