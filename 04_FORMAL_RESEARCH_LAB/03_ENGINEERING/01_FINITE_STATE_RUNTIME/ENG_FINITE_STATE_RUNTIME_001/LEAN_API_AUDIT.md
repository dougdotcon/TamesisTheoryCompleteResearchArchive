---
document_id: RT-LEAN-API-AUDIT
revision_checked: 79d0395a1825a6264ad5d269e35e60537518955e
toolchain: leanprover/lean4:v4.33.0-rc1
probe: /tmp/FiniteStateRuntimeSpecificationProbe.lean (removido)
---

# Auditoria da API Lean

Assinaturas impressas pelo próprio Lean. Nenhum nome presumido.

## Array e acesso indexado

```yaml
- concept: tamanho do array
  candidate_api: Array.size
  exact_signature: "@Array.size : {α : Type u_1} → Array α → ℕ"
  classification: API_FOUND
  usable: true

- concept: acesso indexado com prova
  candidate_api: Array.get
  exact_signature: "—"
  classification: NOT_FOUND
  usable: false
  limitations: "nao existe como constante nesta revisao"
  fallback: "notacao xs[i] via GetElem, com a prova de limite"

- concept: acesso indexado opcional
  candidate_api: Array.getElem?
  exact_signature: "—"
  classification: NOT_FOUND
  usable: false
  limitations: "nao existe como constante; a notacao xs[i]? funciona e foi USADA no probe"
  fallback: "xs[i]? via a classe GetElem?"

- concept: metodo da classe de acesso
  candidate_api: getElem
  exact_signature: >
    @getElem : {coll idx elem valid} → [GetElem coll idx elem valid] →
      (xs : coll) → (i : idx) → valid xs i → elem
  classification: API_FOUND
  usable: true
  limitations: "usado implicitamente pela notacao xs[i]"

- concept: pertinencia do elemento acessado
  candidate_api: Array.getElem_mem
  exact_signature: "∀ {α} {xs : Array α} {i : ℕ} (h : i < xs.size), xs[i] ∈ xs"
  classification: API_FOUND
  usable: false
  limitations: NOT_NEEDED no plano atual

- concept: conversao para lista
  candidate_api: Array.toList
  exact_signature: "@Array.toList : {α : Type u_1} → Array α → List α"
  classification: API_FOUND
  usable: false
  limitations: "so seria necessaria na formulacao por elementos, nao adotada"

- concept: tamanho de List.toArray
  candidate_api: Array.size_toArray
  classification: NOT_FOUND
  usable: false
  limitations: "nao existe sob esse nome; NOT_NEEDED"
```

## Fin

```yaml
- concept: valor subjacente
  candidate_api: Fin.val
  exact_signature: "@Fin.val : {n : ℕ} → Fin n → ℕ"
  classification: API_FOUND
  usable: true

- concept: limite do valor
  candidate_api: Fin.isLt
  exact_signature: "@Fin.isLt : ∀ {n : ℕ} (self : Fin n), ↑self < n"
  classification: API_FOUND
  usable: true
  limitations: "peca de step?_eq_some_step"

- concept: construtor
  candidate_api: Fin.mk
  exact_signature: "@Fin.mk : {n : ℕ} → (val : ℕ) → val < n → Fin n"
  classification: API_FOUND
  usable: true
```

## Except

```yaml
- concept: tipo de resultado com erro
  candidate_api: Except
  exact_signature: "Except : Type u_1 → Type u_2 → Type (max u_1 u_2)"
  classification: API_FOUND
  usable: true

- concept: construtores
  candidate_api: Except.ok / Except.error
  classification: API_FOUND
  usable: true

- concept: encadeamento monadico
  candidate_api: Except.bind
  exact_signature: "@Except.bind : {ε α β} → Except ε α → (α → Except ε β) → Except ε β"
  classification: API_FOUND
  usable: true
  limitations: "a notacao do sobre Except funcionou no probe"
```

## Iteração

```yaml
- concept: iteracao de funcao
  candidate_api: Nat.iterate
  exact_signature: "@Nat.iterate : {α : Sort u_1} → (α → α) → ℕ → α → α"
  classification: API_FOUND
  usable: true
  limitations: "Function.iterate NAO existe; a notacao f^[n] resolve para Nat.iterate"

- concept: passo sucessor, contagem externa consumindo o passo INTERNO
  candidate_api: Function.iterate_succ_apply
  exact_signature: "∀ {α} (f : α → α) (n : ℕ) (x : α), f^[n.succ] x = f^[n] (f x)"
  classification: API_FOUND
  usable: true
  limitations: >
    ESTA eh a variante que casa com run?, cuja recursao aplica um passo e
    recorre sobre o resto

- concept: passo sucessor, variante linha
  candidate_api: Function.iterate_succ_apply'
  exact_signature: "∀ {α} (f : α → α) (n : ℕ) (x : α), f^[n.succ] x = f (f^[n] x)"
  classification: API_FOUND
  usable: false
  limitations: "orientacao INVERSA a de run?; usar por engano exigiria comutar a inducao"

- concept: caso zero
  candidate_api: Function.iterate_zero_apply
  exact_signature: "∀ {α} (f : α → α) (x : α), f^[0] x = x"
  classification: API_FOUND
  usable: true
```

## Decidibilidade

```yaml
- concept: quantificador universal sobre tipo finito
  candidate_api: Fintype.decidableForallFintype
  exact_signature: >
    {α} {p : α → Prop} → [DecidablePred p] → [Fintype α] → Decidable (∀ a, p a)
  classification: API_FOUND
  usable: true
  limitations: "eh o que torna RawTransitionTable.Valid decidivel na formulacao por Fin"

- concept: quantificador limitado sobre Nat
  candidate_api: Nat.decidableBallLT
  exact_signature: >
    (n : ℕ) → (P : (k : ℕ) → k < n → Prop) → [∀ k h, Decidable (P k h)] →
      Decidable (∀ k h, P k h)
  classification: API_FOUND
  usable: false
  limitations: "serviria a formulacao por Nat, nao adotada"

- concept: sintese com tipo explicito
  candidate_api: inferInstanceAs
  classification: API_FOUND
  usable: true
  limitations: >
    #check @inferInstanceAs nao elabora isoladamente, mas o USO funcionou
    no probe, tanto aqui quanto em CycleWitness.decidableValid
```

## APIs do próprio laboratório

```yaml
- concept: certificado de ciclo
  candidate_api: CycleWitness
  classification: API_FOUND
  usable: true

- concept: contrato do certificado
  candidate_api: CycleWitness.Valid
  exact_signature: "{X} [Fintype X] → (X → X) → X → CycleWitness → Prop"
  classification: API_FOUND
  usable: true

- concept: detector
  candidate_api: detectCycleWitness?
  exact_signature: "{X} [Fintype X] [DecidableEq X] → (X → X) → X → Option CycleWitness"
  classification: API_FOUND
  usable: true
  limitations: "aplicado a t.step, sem copia do corpo"

- concept: correcao do detector
  candidate_api: detectCycleWitness?_sound
  classification: API_FOUND
  usable: true

- concept: completude do detector
  candidate_api: detectCycleWitness?_complete
  classification: API_FOUND
  usable: true
  limitations: "consumido como caixa-preta; a casa dos pombos NAO eh repetida"
```

## Resumo

```text
API_FOUND        20
NOT_FOUND         3   (Array.get, Array.getElem?, Array.size_toArray)
NAME_UNCERTAIN    0
NOT_NEEDED        4   (getElem_mem, toList, decidableBallLT, iterate_succ_apply')
```

As três ausências são todas de **nomes de constante**; a funcionalidade
existe pela notação `xs[i]` e `xs[i]?`, que o probe usou com sucesso.

## Sínteses e avaliações confirmadas

```text
#synth Decidable (RawT.Valid <#[0]>)   resolve para a instancia declarada
#eval validateT                        quatro casos
#eval run?                             cinco casos, incluindo none
#eval analyzeT                         treze casos
example step_val := rfl                fecha por rfl
```

O probe foi removido ao final do gate.
