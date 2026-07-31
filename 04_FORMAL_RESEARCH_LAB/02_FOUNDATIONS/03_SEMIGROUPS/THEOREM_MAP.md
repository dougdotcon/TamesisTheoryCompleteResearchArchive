# FOUND-SEMIGROUP-001 — Mapa de teoremas

Arquivos Lean em `05_FORMAL/lean/TamesisLab/Foundations/Semigroups/`;
namespace `TamesisLab.Foundations.Semigroups`. Auditoria computacional em
`06_COMPUTATION/results/FOUND-SEMIGROUP-001-computational-audit.json`
(`COMPUTATIONAL_FINITE_CROSS_CHECK_ONLY`).

Campos comuns a todas as entradas:

```yaml
novelty: STANDARD_KNOWN_RESULT_OR_FINITE_MODEL_PROPERTY
scientific_value: FOUNDATIONAL_FORMALIZATION_ONLY
```

---

```yaml
- theorem_id: FOUND-SG-001
  human_statement: "comp a b sempre produz uma transição de Shift3 (fechamento)."
  lean_signature: "def Shift3.comp : Shift3 → Shift3 → Shift3"
  lean_file: "Semigroups/Regime3.lean"
  dependencies: [Shift3]
  proof_method: "closure is enforced by construction — garantido pelo tipo de retorno; registrado como propriedade estrutural, não como teorema"
  scope: FINITE_MODEL
  computational_cross_check: checks.closure

- theorem_id: FOUND-SG-002
  human_statement: "A composição de transições é associativa."
  lean_signature: "theorem comp_assoc (a b c : Shift3) : Shift3.comp (Shift3.comp a b) c = Shift3.comp a (Shift3.comp b c)"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [FOUND-SG-001]
  proof_method: "decide (análise finita exaustiva, 27 casos, verificada pelo kernel)"
  scope: FINITE_MODEL
  computational_cross_check: checks.associativity

- theorem_id: FOUND-SG-003
  human_statement: "identity é identidade à esquerda da composição."
  lean_signature: "theorem identity_comp (a : Shift3) : Shift3.comp .identity a = a"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [FOUND-SG-001]
  proof_method: "rfl (computação definicional)"
  scope: FINITE_MODEL
  computational_cross_check: checks.left_identity

- theorem_id: FOUND-SG-004
  human_statement: "identity é identidade à direita da composição."
  lean_signature: "theorem comp_identity (a : Shift3) : Shift3.comp a .identity = a"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [FOUND-SG-001]
  proof_method: "cases a <;> rfl (análise finita de casos)"
  scope: FINITE_MODEL
  computational_cross_check: checks.right_identity

- theorem_id: FOUND-SG-005
  human_statement: "A ação é compatível com a composição na convenção adotada: aplicar comp a b equivale a aplicar b e depois a."
  lean_signature: "theorem apply_comp (a b : Shift3) (r : Regime3) : (Shift3.comp a b).apply r = a.apply (b.apply r)"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [FOUND-SG-001]
  proof_method: "decide (27 casos)"
  scope: FINITE_MODEL
  computational_cross_check: checks.action_compatibility

- theorem_id: FOUND-SG-006
  human_statement: "forward aplicada três vezes retorna ao regime inicial."
  lean_signature: "theorem forward_cycle (r : Regime3) : Shift3.forward.apply (Shift3.forward.apply (Shift3.forward.apply r)) = r"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: []
  proof_method: "cases r <;> rfl"
  scope: FINITE_MODEL
  computational_cross_check: NOT_APPLICABLE (implícito na tabela de ação)

- theorem_id: FOUND-SG-007
  human_statement: "Regime3 possui exatamente três elementos."
  lean_signature: "theorem card_regime3 : Fintype.card Regime3 = 3"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [instância Fintype Regime3]
  proof_method: "decide"
  scope: FINITE_MODEL
  computational_cross_check: model_size.regimes

- theorem_id: FOUND-SG-008
  human_statement: "Shift3 possui exatamente três elementos."
  lean_signature: "theorem card_shift3 : Fintype.card Shift3 = 3"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [instância Fintype Shift3]
  proof_method: "decide"
  scope: FINITE_MODEL
  computational_cross_check: model_size.transitions

- theorem_id: FOUND-SG-009
  human_statement: "identity e forward são transições distintas."
  lean_signature: "theorem identity_ne_forward : Shift3.identity ≠ Shift3.forward"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [DecidableEq Shift3]
  proof_method: "decide"
  scope: FINITE_MODEL
  computational_cross_check: NOT_APPLICABLE (sintático)

- theorem_id: FOUND-SG-010
  human_statement: "identity e forward2 são transições distintas."
  lean_signature: "theorem identity_ne_forward2 : Shift3.identity ≠ Shift3.forward2"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [DecidableEq Shift3]
  proof_method: "decide"
  scope: FINITE_MODEL
  computational_cross_check: NOT_APPLICABLE (sintático)

- theorem_id: FOUND-SG-011
  human_statement: "forward e forward2 são transições distintas."
  lean_signature: "theorem forward_ne_forward2 : Shift3.forward ≠ Shift3.forward2"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [DecidableEq Shift3]
  proof_method: "decide"
  scope: FINITE_MODEL
  computational_cross_check: NOT_APPLICABLE (sintático)

- theorem_id: FOUND-SG-012
  human_statement: "A ação é fiel: transições com a mesma ação em todos os regimes são iguais."
  lean_signature: "theorem apply_faithful (a b : Shift3) (h : ∀ r, Shift3.apply a r = Shift3.apply b r) : a = b"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [Fintype Regime3, DecidableEq Shift3]
  proof_method: "decide (quantificação finita decidível)"
  scope: FINITE_MODEL
  computational_cross_check: checks.faithful_action

- theorem_id: FOUND-SG-013
  human_statement: "O modelo é transitivo: para quaisquer regimes x e y existe transição s com apply s x = y. Propriedade do modelo cíclico C3, não de semigrupos em geral."
  lean_signature: "theorem apply_transitive (x y : Regime3) : ∃ s : Shift3, s.apply x = y"
  lean_file: "Semigroups/Theorems.lean"
  dependencies: [Fintype Shift3]
  proof_method: "decide (existência finita decidível)"
  scope: FINITE_MODEL_ONLY
  computational_cross_check: checks.transitivity
```

## Instâncias estruturais (não são teoremas novos)

```yaml
- instance: "Monoid Shift3"
  lean_file: "Semigroups/Action.lean"
  built_from: [FOUND-SG-002, FOUND-SG-003, FOUND-SG-004]
  note: "Criada após as leis; fornece Semigroup Shift3 por herança."

- instance: "MulAction Shift3 Regime3"
  lean_file: "Semigroups/Action.lean"
  built_from: [FOUND-SG-005, "aplicação definicional da identidade"]
  note: "Criada após as leis; fornece SemigroupAction Shift3 Regime3 por herança. Verificações de coincidência notacional em Audit.lean."
```

Nenhum item deste mapa é uma descoberta.
