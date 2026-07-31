# FOUND-SEMIGROUP-002 — Teoremas candidatos

Assinaturas apenas. **Nenhum corpo de prova neste gate.**

---

## Camada A — estruturais

### FSG2-REACH-001 — reflexividade

```lean
theorem reachable_refl
    {M X : Type*} [Monoid M] [MulAction M X] (x : X) :
    Reachable (M := M) x x
```

Testemunha: `1 : M`, via `one_smul`. Mathlib já tem a forma para órbitas:
`MulAction.mem_orbit_self (a : α) : a ∈ orbit M a := ⟨1, by simp⟩`.

### FSG2-REACH-002 — transitividade

```lean
theorem reachable_trans
    {M X : Type*} [Monoid M] [MulAction M X] {x y z : X} :
    Reachable (M := M) x y → Reachable (M := M) y z → Reachable (M := M) x z
```

Testemunha: se `m • x = y` e `m' • y = z`, então `(m' * m) • x = z` por
`mul_smul`. **A ordem importa** e segue a convenção já fixada em
`FOUND-SEMIGROUP-001`: `m' * m` aplica `m` primeiro.

### FSG2-REACH-003 — preorder: decisão

Alcançabilidade é reflexiva e transitiva, logo um preorder. A questão é
**como representá-la sem estragar a resolução de instâncias**.

```yaml
opcao_rejeitada: instance Preorder X
  motivo: >
    Seria uma instancia global keyed em X, mas a relacao depende de M, que
    nao aparece no tipo. Duas acoes distintas sobre o mesmo X dariam duas
    instancias Preorder X incompativeis, e X frequentemente ja tem ordem
    propria. Isso quebraria elaboracao em qualquer arquivo que importe o
    modulo.

opcao_adotada: >
  Registrar reflexividade e transitividade como teoremas (FSG2-REACH-001 e
  002) e fornecer um `def` NAO-instancia, para uso explicito com `letI`:

    def reachablePreorder (M : Type*) [Monoid M] [MulAction M X] : Preorder X

  Quem quiser a notacao de ordem opta por ela localmente. Nada e imposto
  globalmente.
```

Gap correspondente: `FSG2-GAP-006`.

### FSG2-ORBIT-001 — pertinência à órbita

```lean
theorem reachable_iff_mem_orbit
    {M X : Type*} [Monoid M] [MulAction M X] {x y : X} :
    Reachable (M := M) x y ↔ y ∈ MulAction.orbit M x
```

**Esperado ser `Iff.rfl`**: `MulAction.mem_orbit_iff` é literalmente
`Iff.rfl` no checkout fixado. Custo estimado: nulo.

### FSG2-INV-001 — invariante preservado por alcançabilidade

```lean
theorem isInvariant_eq_of_reachable
    {M X A : Type*} [Monoid M] [MulAction M X]
    {I : X → A} (hI : IsInvariant (M := M) I) {x y : X} :
    Reachable (M := M) x y → I y = I x
```

### FSG2-INV-002 — invariante de gerador ao longo da iteração

```lean
theorem isInvariantUnder_iterate
    {M X A : Type*} [Monoid M] [MulAction M X]
    {a : M} {I : X → A} (hI : ∀ x, I (a • x) = I x) (n : ℕ) (x : X) :
    I (a ^ n • x) = I x
```

Separado de `FSG2-INV-001` de propósito: a hipótese é estritamente mais
fraca (só `a`, não todo `M`).

---

## Camada C — alvo principal

### FSG2-PER-001 — CORE

```lean
theorem exists_collision
    {X : Type*} [Fintype X] (f : X → X) (x : X) :
    ∃ i j : ℕ, i < j ∧ j ≤ Fintype.card X ∧
      Function.iterate f i x = Function.iterate f j x
```

Rota: aplicar `Fintype.exists_ne_map_eq_of_card_lt` a

```text
g : Fin (Fintype.card X + 1) → X,  g i = f^[i] x
```

com `Fintype.card X < Fintype.card (Fin (card X + 1)) = card X + 1`.
Devolve `i ≠ j`; ordenar por `wlog`/`rcases` em `lt_or_gt_of_ne`.

### FSG2-PER-002 — alvo com limitantes

```lean
theorem exists_eventual_period
    {X : Type*} [Fintype X] [DecidableEq X]
    (f : X → X) (x : X) :
    ∃ μ λ : ℕ,
      μ < Fintype.card X ∧
      0 < λ ∧
      μ + λ ≤ Fintype.card X ∧
      Function.iterate f (μ + λ) x = Function.iterate f μ x
```

Derivação a partir de `FSG2-PER-001`: `μ := i`, `λ := j - i`.

Auditoria dos limitantes, feita **antes** de prometer:

```text
g tem dominio Fin (card X + 1), logo i, j <= card X.
i < j <= card X                 ==>  mu = i < card X          OK
mu + lambda = i + (j - i) = j   ==>  mu + lambda <= card X     OK
i < j                           ==>  lambda = j - i > 0        OK
```

Os três limitantes são **simultaneamente alcançáveis** nesta formulação.
Isto não era óbvio a priori e foi verificado antes de escolher a meta.

Nota sobre `DecidableEq X`: **não é usada** na prova esboçada. Ela aparece
na assinatura sugerida pelo gate, mas seria hipótese ociosa. Decisão,
coerente com a política já aplicada em `COUNTING-LAW-BRIDGE`
(remoção de `0 < c`): **omitir `DecidableEq X`** salvo se a execução
mostrar necessidade. Registrado como `FSG2-GAP-004c`.

### FSG2-PER-003 — PROPAGATION

```lean
theorem iterate_eq_of_eventual_period
    {X : Type*} (f : X → X) (x : X) {μ lam : ℕ}
    (h : Function.iterate f (μ + lam) x = Function.iterate f μ x) (k : ℕ) :
    Function.iterate f (μ + k + lam) x = Function.iterate f (μ + k) x
```

Rota: `Function.iterate_add_apply` mais aritmética de índices em `ℕ`:

```text
f^[mu + k + lam] x = f^[k] (f^[mu + lam] x)
                   = f^[k] (f^[mu] x)
                   = f^[mu + k] x
```

Custo estimado: baixo (dois `rw` e um reordenamento de soma).

### FSG2-PER-004 — ponte com a API de dinâmica da Mathlib

```lean
theorem isPeriodicPt_iterate
    {X : Type*} (f : X → X) (x : X) {μ lam : ℕ}
    (h : Function.iterate f (μ + lam) x = Function.iterate f μ x) :
    Function.IsPeriodicPt f lam (Function.iterate f μ x)
```

Valor: liga o resultado local ao vocabulário oficial
(`Function.IsPeriodicPt`), e explicita que **o ponto periódico é
`f^[μ] x`, não `x`**. É o antídoto formal para a armadilha do
`minimalPeriod` registrada em `DEFINITIONS.md`.

---

## Camada B — corolário para ações

### FSG2-ACT-001

```lean
theorem monoid_element_eventually_periodic
    {M X : Type*} [Monoid M] [Fintype X] [MulAction M X]
    (a : M) (x : X) :
    ∃ μ lam : ℕ, 0 < lam ∧ a ^ (μ + lam) • x = a ^ μ • x
```

**Derivado**, não reprovado. Rota:

```text
1. aplicar FSG2-PER-002 a f := (a . _)
2. reescrever com smul_iterate_apply nos dois lados:
     f^[n] x = a^n . x
3. concluir
```

Nenhuma enumeração, nenhuma indução nova. Fica registrado que `Fintype M`
**não** é necessário: a finitude usada é a de `X`.

---

## Decisão de meta para a primeira execução

```text
ESCOLHIDA:  C. CORE_BOUNDS_AND_PROPAGATION
```

Escopo autorizado a formalizar no gate seguinte: `FSG2-REACH-001/002/003`,
`FSG2-ORBIT-001`, `FSG2-INV-001/002`, `FSG2-PER-001/002/003/004`,
`FSG2-ACT-001`.

Justificativa da escolha, com o custo analisado:

| Componente | Custo | Veredito |
|---|---|---|
| CORE | baixo — pigeonhole direto da Mathlib | incluir |
| BOUNDS | baixo — vêm **de graça** da formulação com `Fin (card X + 1)` | incluir |
| PROPAGATION | baixo — corolário de 3 linhas via `iterate_add_apply` | incluir |
| DECOMPOSITION | **alto** | **excluir** |

### Por que a decomposição fica fora

A decomposição única em cauda + ciclo exige:

```text
minimalidade de mu   (menor pre-periodo) -> Nat.find / boa ordenacao
minimalidade de lam  (menor periodo)     -> divisibilidade de periodos
unicidade do par     -> argumento de minimalidade em duas variaveis
injetividade de f^[.] no segmento inicial [0, mu)
estrutura ciclica em [mu, mu + lam)
```

São cinco obrigações novas, nenhuma delas corolário das anteriores, e a
parte de divisibilidade de períodos depende de lemas de
`Dynamics/PeriodicPts` que ainda não foram auditados. O gate proíbe
autorizar decomposição sem análise de custo; a análise foi feita e o
veredito é **adiar**. Registrado como `FSG2-GAP-004b`.
