---
document_id: FSG2-INSTANCE-AUDIT
work_item_id: FOUND-SEMIGROUP-002
total_instances: 11
instances_in_math_core: 0
conflicts_found: 0
audit_test: "05_FORMAL/lean/TamesisLab/Tests/FoundSemigroup002InstanceAudit.lean"
---

# FOUND-SEMIGROUP-002 — Auditoria de instâncias

## Achado principal

```text
Reachability.lean          0 instancias
Invariants.lean            0 instancias
EventualPeriodicity.lean   0 instancias
MonoidIteration.lean       0 instancias
Audit.lean                 0 instancias
Counterexamples.lean      11 instancias
```

**O núcleo matemático não declara instância alguma.** Todas as onze
pertencem a modelos de contraexemplo, cada um em namespace próprio.

## As onze instâncias, literalmente

```yaml
- instance: "instance : Fintype St"
  type: Fintype CE001.St
  module: Counterexamples
  namespace: "…FiniteDynamics.Counterexamples.CE001"
  scope: local ao modelo
  purpose: "decidir ∀/∃ sobre os dois estados"
  could_conflict: false
  exported_by_umbrella: true
  acceptable: true

- instance: "instance : Fintype Tr"
  type: Fintype CE001.Tr
  namespace: "…Counterexamples.CE001"
  purpose: "decidir ¬∃ m, m • one = zero"
  could_conflict: false
  acceptable: true

- instance: "instance : Monoid Tr"
  type: Monoid CE001.Tr
  namespace: "…Counterexamples.CE001"
  purpose: "tornar CE-001 uma acao GENUINA de monoide (correcao 5.2)"
  could_conflict: false
  acceptable: true
  note: "leis provadas ANTES da instancia: comp_assoc, idT_comp, comp_idT"

- instance: "instance : MulAction Tr St"
  type: MulAction CE001.Tr CE001.St
  namespace: "…Counterexamples.CE001"
  purpose: "a acao que refuta a simetria"
  could_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE002.St
  namespace: "…Counterexamples.CE002"
  could_conflict: false
  acceptable: true

- instance: "instance : Fintype Tr"
  type: Fintype CE002.Tr
  namespace: "…Counterexamples.CE002"
  could_conflict: false
  acceptable: true

- instance: "instance : Monoid Tr"
  type: Monoid CE002.Tr
  namespace: "…Counterexamples.CE002"
  could_conflict: false
  acceptable: true
  note: "CE002.Tr eh tipo DISTINTO de CE001.Tr; nao ha competicao"

- instance: "instance : MulAction Tr St"
  type: MulAction CE002.Tr CE002.St
  namespace: "…Counterexamples.CE002"
  could_conflict: false
  acceptable: true

- instance: "instance : Fintype St"
  type: Fintype CE003.St
  namespace: "…Counterexamples.CE003"
  purpose: "permitir instanciar exists_eventual_period no modelo com cauda"
  could_conflict: false
  acceptable: true
  note: "CE003 NAO tem monoide — eh Camada C pura, e isso eh correto"

- instance: "instance : Fintype St"
  type: Fintype CE004.St
  namespace: "…Counterexamples.CE004"
  could_conflict: false
  acceptable: true

- instance: "instance : MulAction CE001.Tr St"
  type: MulAction CE001.Tr CE004.St
  namespace: "…Counterexamples.CE004"
  purpose: "o monoide de CE-001 agindo sobre um unico estado (nao fidelidade)"
  could_conflict: false
  acceptable: true
  note: >
    Reutiliza CE001.Tr com um X DIFERENTE. O par (CE001.Tr, CE004.St) eh
    distinto de (CE001.Tr, CE001.St); as duas MulAction coexistem sem
    ambiguidade. Verificado por #synth e por dois `rfl` que resolvem o `•`
    para a acao correta em cada tipo.
```

Distribuição: `CE001` 4, `CE002` 4, `CE003` 1, `CE004` 2, `CE005` 0.

## Exigências do gate

| Exigência | Estado |
|---|---|
| instâncias de contraexemplos em namespaces próprios | **sim**, cinco namespaces distintos |
| sem duas instâncias concorrentes para a mesma combinação de tipos | **sim** — verificado par a par |
| nenhuma instância de `Preorder` | **sim** — `Preorder` aparece 1 vez, num comentário que declara a exclusão |
| nenhuma instância física ou legada importada | **sim** — imports auditados |
| umbrella não causa síntese ambígua | **sim** — teste `#synth` exit 0 |

## Teste de auditoria criado

`TamesisLab/Tests/FoundSemigroup002InstanceAudit.lean`, exit **0**.

Ele **não altera módulo matemático algum**. Verifica:

1. as onze instâncias por `#synth`, nominalmente;
2. que `CE001.Tr.collapse • CE001.St.zero` e
   `CE001.Tr.collapse • CE004.St.pt` resolvem, cada um, para a ação certa
   — por `rfl`;
3. que `(1 : CE001.Tr)` e `(1 : CE002.Tr)` resolvem para monoides
   distintos, sem competição;
4. que `reachable_isRefl`/`reachable_isTrans` typecheck **sem** instância
   global;
5. que, com o agregador importado (portanto com todas as onze instâncias
   em escopo), `exists_eventual_period` continua se aplicando a um tipo
   externo (`Bool`) — ou seja, **a poluição não existe**;
6. as 17 assinaturas públicas, por `#check`.

## Conflitos encontrados

```text
0
```

Nenhuma poluição, nenhuma ambiguidade material. **Nenhuma instância foi
criada nem corrigida nesta revisão.**
