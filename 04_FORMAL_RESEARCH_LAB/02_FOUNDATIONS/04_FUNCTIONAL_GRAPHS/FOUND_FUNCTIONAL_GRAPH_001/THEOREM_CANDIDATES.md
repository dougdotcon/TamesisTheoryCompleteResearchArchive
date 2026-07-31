# FOUND-FUNCTIONAL-GRAPH-001 — Teoremas candidatos

Assinaturas apenas. **Nenhum corpo de prova neste gate.**

Classificação: `CORE`, `COROLLARY`, `OPTIONAL`, `DEFERRED`.

---

## Alcançabilidade dirigida

### FFG-REACH-001 — reflexividade `CORE`

```lean
theorem iterReachable_refl (f : X → X) (x : X) : IterReachable f x x
```

Testemunha `n = 0`; `f^[0] x = x` é `rfl`.

### FFG-REACH-002 — transitividade `CORE`

```lean
theorem iterReachable_trans {f : X → X} {x y z : X}
    (hxy : IterReachable f x y) (hyz : IterReachable f y z) :
    IterReachable f x z
```

Testemunha `n₂ + n₁`, via `Function.iterate_add_apply f n₂ n₁ x`.
**Nenhuma simetria é enunciada** — `FFG-CE-002` a refuta.

---

## Encontro eventual

### FFG-MEET-001 — reflexividade `CORE`

```lean
theorem eventuallyMeets_refl (f : X → X) (x : X) : EventuallyMeets f x x
```

Testemunhas `m = n = 0`.

### FFG-MEET-002 — simetria `CORE`

```lean
theorem eventuallyMeets_symm {f : X → X} {x y : X}
    (h : EventuallyMeets f x y) : EventuallyMeets f y x
```

Troca das testemunhas e `.symm` na igualdade.

### FFG-MEET-003 — transitividade `CORE`

```lean
theorem eventuallyMeets_trans {f : X → X} {x y z : X}
    (hxy : EventuallyMeets f x y) (hyz : EventuallyMeets f y z) :
    EventuallyMeets f x z
```

Este é o **único** dos três com conteúdo real.

```text
hxy da  m1, n1  com  f^[m1] x = f^[n1] y
hyz da  m2, n2  com  f^[m2] y = f^[n2] z

Alinhar as duas iteradas da trajetoria intermediaria y:
a partir de n1 e m2, avancar ambos ate max(n1, m2).

Caso n1 <= m2:  avancar o lado de x em (m2 - n1)
  f^[(m2 - n1) + m1] x = f^[m2 - n1] (f^[n1] y) = f^[m2] y = f^[n2] z
  testemunhas: ((m2 - n1) + m1, n2)

Caso m2 <= n1:  avancar o lado de z em (n1 - m2)
  f^[m1] x = f^[n1] y = f^[n1 - m2] (f^[m2] y) = f^[(n1 - m2) + n2] z
  testemunhas: (m1, (n1 - m2) + n2)
```

**Os dois casos devem aparecer explicitamente na prova futura**, separados
por `Nat.le_total n1 m2` ou `rcases le_or_lt`. Ferramentas: subtração
truncada de `ℕ` normalizada por `omega`, mais `Function.iterate_add_apply`.

Registrado em `FFG-GAP-002`.

### FFG-MEET-004 — alcançabilidade implica encontro `COROLLARY`

```lean
theorem eventuallyMeets_of_iterReachable {f : X → X} {x y : X}
    (h : IterReachable f x y) : EventuallyMeets f x y
```

Testemunhas `(n, 0)`.

---

## Conjunto componente

### FFG-COMP-001 — pertinência do estado inicial `COROLLARY`

```lean
theorem self_mem_componentSet (f : X → X) (x : X) : x ∈ componentSet f x
```

### FFG-COMP-002 — estabilidade `COROLLARY`

```lean
theorem componentSet_eq_of_eventuallyMeets {f : X → X} {x y : X}
    (h : EventuallyMeets f x y) : componentSet f x = componentSet f y
```

Forma mais forte e mais útil que "estável por `EventuallyMeets`": as
classes coincidem. Decorre de `FFG-MEET-002` e `FFG-MEET-003` por
`Set.ext`.

**Nenhuma instância de `Setoid` é criada.**

---

## Recorrência

### FFG-REC-000 — auditoria dos aliases `COROLLARY`

```lean
theorem isRecurrent_iff (f : X → X) (x : X) :
    IsRecurrent f x ↔ x ∈ Function.periodicPts f
```

Esperado `Iff.rfl`. Se deixar de ser, o alias virou segunda noção e deve
ser removido.

### FFG-REC-001 — existência de periódico alcançável `CORE`

```lean
theorem exists_recurrent_reachable {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ p : X, IterReachable f x p ∧ p ∈ Function.periodicPts f
```

### FFG-REC-002 — versão com limite de entrada `CORE`

```lean
theorem exists_recurrent_reachable_with_bound {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ mu : ℕ, mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f
```

#### Assinatura rejeitada

A forma sugerida pelo gate com `∃ μ p : ℕ × X` foi **descartada**: o par
`(μ, p)` é artificial, obriga a escrever `p.2` na conclusão e não acrescenta
informação — `p` é determinado por `f^[μ] x`. A forma acima é a limpa, e é
a própria alternativa que o gate recomendou.

#### Derivação

```text
exists_eventual_period f x  da  mu, lam  com
  mu < card X, 0 < lam, mu + lam <= card X,
  IsPeriodicPt f lam (f^[mu] x)

Function.mk_mem_periodicPts (hn := hlam) (hx := hper)
  : f^[mu] x ∈ periodicPts f
```

**A casa dos pombos não é reaplicada.** `exists_eventual_period` já a
consumiu, uma única vez, em `FOUND-SEMIGROUP-002`.

`FFG-REC-001` é corolário de `FFG-REC-002` com `p := f^[mu] x` e
`IterReachable` testemunhado por `mu`.

#### Sobre `mu + lam ≤ card X`

Disponível em `exists_eventual_period`, mas **não** aparece nas conclusões
acima: `lam` não é exposto, e expô-lo apenas para carregar o limite seria
hipótese de saída ociosa. Se um gate futuro precisar do limite do período,
ele volta — com justificativa.

---

## Ponte entre encontro e ciclo

### FFG-CYCLE-001 — periódicos que se encontram têm a mesma órbita `CORE`

```lean
theorem periodicOrbit_eq_of_eventuallyMeets {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (hpq : EventuallyMeets f p q) :
    Function.periodicOrbit f p = Function.periodicOrbit f q
```

Rota, **sem aritmética modular**:

```text
obtain m, n  com  f^[m] p = f^[n] q

periodicOrbit f p
  = periodicOrbit f (f^[m] p)     (periodicOrbit_apply_iterate_eq hp m).symm
  = periodicOrbit f (f^[n] q)     reescrita pela igualdade
  = periodicOrbit f q             periodicOrbit_apply_iterate_eq hq n
```

Três passos. A API de órbitas periódicas evita completamente a aritmética
modular, exatamente como o gate pediu.

Orientação conforme a regra de `DEFINITIONS.md`: o primeiro argumento de
`EventuallyMeets` vai à esquerda.

### FFG-CYCLE-002 — recíproca `OPTIONAL`

```lean
theorem eventuallyMeets_of_periodicOrbit_eq {f : X → X} {p q : X}
    (hp : p ∈ Function.periodicPts f)
    (hq : q ∈ Function.periodicPts f)
    (h : Function.periodicOrbit f p = Function.periodicOrbit f q) :
    EventuallyMeets f p q
```

```yaml
classificacao: OPTIONAL
recomendacao: INCLUIR
motivo: >
  A rota eh curta e usa API que ja sera importada:
    self_mem_periodicOrbit hq : q ∈ periodicOrbit f q
    reescrever por h.symm     : q ∈ periodicOrbit f p
    mem_periodicOrbit_iff hp  : ∃ n, f^[n] p = q
    testemunhas (n, 0)        : EventuallyMeets f p q
  Quatro passos. Junto com CYCLE-001 fecha um `iff`, o que torna a
  caracterizacao do ciclo completa em vez de unidirecional.
nao_exigido: >
  Se a execucao encontrar atrito inesperado, pode ser adiada sem afetar o
  teorema principal, que so usa CYCLE-001.
```

---

## Teorema principal

### FFG-MAIN-001 — componente funcional tem ciclo único `CORE`

```lean
theorem functional_component_has_unique_cycle {X : Type*} [Fintype X]
    (f : X → X) (x : X) :
    ∃ p : X,
      IterReachable f x p ∧
      p ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f q = Function.periodicOrbit f p
```

Rota:

```text
1. FFG-REC-001 da p, com IterReachable f x p e p periodico
2. dado q periodico com EventuallyMeets f x q:
     EventuallyMeets f q x   por FFG-MEET-002
     EventuallyMeets f x p   por FFG-MEET-004 sobre IterReachable
     EventuallyMeets f q p   por FFG-MEET-003
3. FFG-CYCLE-001 hq hp (EventuallyMeets f q p)
     : periodicOrbit f q = periodicOrbit f p
```

Composição de resultados anteriores. **Nenhum pigeonhole, nenhuma indução
nova.**

### FFG-MAIN-002 — versão com limite de entrada `CORE`

```lean
theorem functional_component_has_unique_cycle_with_bound
    {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ mu : ℕ,
      mu < Fintype.card X ∧
      f^[mu] x ∈ Function.periodicPts f ∧
      ∀ q : X,
        q ∈ Function.periodicPts f →
        EventuallyMeets f x q →
        Function.periodicOrbit f q = Function.periodicOrbit f (f^[mu] x)
```

Mesma prova, com `p := f^[mu] x` vindo de `FFG-REC-002`.

### O que o teorema principal **não** afirma

```text
NAO afirma que p seja unico.
NAO afirma que mu seja minimo.
NAO afirma que o periodo seja minimo.
NAO afirma que exista exatamente um ponto periodico no componente.
NAO afirma decomposicao em cauda mais arvores.
```

O objeto **único** é `Function.periodicOrbit f p`, não o representante.
Ver `TARGET_RESULT.md`.

---

## Resumo

| Classificação | Teoremas |
|---|---|
| `CORE` | `REACH-001/002`, `MEET-001/002/003`, `REC-001/002`, `CYCLE-001`, `MAIN-001/002` — **11** |
| `COROLLARY` | `MEET-004`, `COMP-001/002`, `REC-000` — **4** |
| `OPTIONAL` | `CYCLE-002` — **1** |
| `DEFERRED` | ponte `SimpleGraph`, árvores, distância mínima, unicidade de `μ` — ver `NOVELTY_BOUNDARY.md` |

Dezesseis enunciados previstos, nenhum provado.

---

# Estado após a revisão

Este documento é **histórico**. As assinaturas vigentes estão em
`FINAL_SIGNATURES.md`.

Alterações aplicadas pela revisão:

```text
FFG-REC-000  IsRecurrent auditado      REMOVIDO   alias retirado
FFG-MAIN-001 e FFG-MAIN-002            COLAPSADOS em
             exists_component_cycle_with_entry_bound
FFG-REC-001  versao sem limite          REMOVIDO   redundante
FFG-REC-002  ->  exists_cyclePoint_reachable_with_bound
FFG-COMP-001 e FFG-COMP-002            DEFERRED   componentSet nao usado
testemunhas da transitividade          CORRIGIDAS para a forma natural
```

Motivo do colapso de `FFG-MAIN-001/002`: o `p` existencial era sempre
`f^[mu] x`, logo redundante. A forma com `∃ mu : ℕ` elimina a duplicação e
põe o limite de entrada no enunciado principal.

