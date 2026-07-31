---
document_id: FCD-EXTRACTION-FEASIBILITY
status: READY_FOR_FEASIBILITY_AUDIT
---

# Viabilidade de extração

> Auditoria de viabilidade. **Nenhuma extração foi executada. Nenhuma
> integração externa foi feita.**

## Por definição

```yaml
- definition: CycleWitness
  computable: yes
  uses_classical_choice: no
  uses_noncomputable: no
  proof_fields_erased: n/a — nao ha campos de prova
  works_with_eval: expected_yes
  candidate_export_surface: estrutura de dois Nat
  limitations: nenhuma

- definition: cycleCandidates
  computable: yes
  uses_classical_choice: no
  uses_noncomputable: no
  proof_fields_erased: n/a
  works_with_eval: >
    verificado na sonda com a MESMA forma sobre pares de Nat:
    (List.range n).flatMap (fun m => (List.range (n-m)).map (fun k => (m, k+1)))
    avaliou para n = 1, 3 e 4
  candidate_export_surface: ℕ → List CycleWitness
  limitations: nenhuma

- definition: CycleWitness.Valid
  computable: proposicional, mas DECIDIVEL com DecidableEq X
  uses_classical_choice: no
  uses_noncomputable: no
  proof_fields_erased: n/a
  works_with_eval: >
    a instancia Decidable foi obtida por inferInstance na sonda, para
    X = Bool, com a conjuncao completa
  candidate_export_surface: via decide
  limitations: exige DecidableEq X

- definition: detectCycleWitness?
  computable: expected_yes
  uses_classical_choice: no
  uses_noncomputable: no
  proof_fields_erased: n/a
  works_with_eval: NOT_VERIFIED — exigiria implementar, proibido neste gate
  candidate_export_surface: (X → X) → X → Option CycleWitness
  limitations: >
    depende de List.find? e de decide; ambos executaveis. O risco residual
    eh o TAMANHO do termo gerado por decide sobre a conjuncao, nao a
    computabilidade.

- definition: detectCycleWitness
  computable: expected_yes
  uses_classical_choice: no — o existencial da completude eh consumido em nivel Prop
  uses_noncomputable: no
  proof_fields_erased: expected_yes — Option.get recebe a prova como argumento Prop
  works_with_eval: NOT_VERIFIED
  candidate_export_surface: (X → X) → X → CycleWitness
  limitations: >
    DEFERRED. So sera autorizado no gate de formalizacao, apos checar #eval.
    A API publica v1 permanece baseada em Option.
```

## Mecanismos auditados

| Mecanismo | Estado | Observação |
|---|---|---|
| `#eval` | **auditado na sonda** para `List.range`, `flatMap`, `map`, `find?`, `Fintype.card`, `Nat.iterate` sobre `Bool`, `decide` e `Option.get` | todos avaliaram; `(Option.some 7).get (by decide)` devolveu `7` |
| `lean --run` | **não auditado** | exigiria um `main`, isto é, código; diferido |
| alvo executável em Lake | **não auditado** | exigiria alterar `lakefile`; diferido |
| compilação nativa | **não auditado** | fora do escopo da primeira versão |

## O argumento de erasure

```text
Usar Classical.choice para PROVAR uma proposicao eh inocuo
computacionalmente.

Usa-lo para PRODUZIR DADO torna a definicao noncomputable.
```

Na rota de totalização, `detectCycleWitness?_complete` é consumida apenas
para fornecer `h : (detectCycleWitness? f x).isSome = true`, que é um
argumento `Prop` de `Option.get`. O `∃` **nunca** é projetado para
extrair `mu` e `lam` como dado — isso exigiria `Classical.choose` e é
explicitamente proibido.

## Conclusão

```yaml
CD-GAP-014:
  status: READY_FOR_FEASIBILITY_AUDIT
```

**Não resolvido.** A viabilidade tem argumento favorável e evidência
parcial de sonda, mas a verificação real só pode ocorrer no gate de
formalização.
