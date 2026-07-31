---
document_id: FCD-PROOF-AUDIT
pigeonhole_repeated: false
---

# Auditoria das provas

## Contagens

```text
estruturas    1
definicoes    3     Valid, cycleCandidates, detectCycleWitness?
instancias    1     CycleWitness.decidableValid
teoremas      8
arquivos      6 + 1 agregador + 3 testes
linhas        609
agregadores   2     Foundations.lean e TamesisLab.lean
```

## Auditorias de contagem zero

```text
tokens de prova incompleta            0
marca de nao-computabilidade          0
escolha classica extraindo dado       0
lema de contagem do pigeonhole        0
imports proibidos                     0
objeto de orbita quociente            0
sorryAx                               0
```

Todas verificadas por `grep` sobre os seis módulos, o agregador e os três
testes. As menções documentais que antes quebravam a contagem foram
movidas para `COMPUTABILITY_RESULT.md`.

## Dois atritos reais e como foram resolvidos

### 1. Unificação de ordem superior em `List.find?_some`

A forma ingênua

```lean
exact of_decide_eq_true (List.find?_some h)
```

falhou: Lean escolheu `p := @decide (CycleWitness.Valid f x w)` — uma
função **constante** — em vez do predicado pretendido. Erro reportado:

```text
Application type mismatch: ... has type
  List.find? (fun w => decide (Valid f x w)) (cycleCandidates ...) = some w
but is expected to have type
  List.find? (@decide (Valid f x w)) ?m = some ?m
```

Resolvido passando o predicado explicitamente:

```lean
List.find?_some (p := fun v => decide (CycleWitness.Valid f x v)) h
```

### 2. Instância decidível não encontrada por resolução automática

Já previsto no gate de revisão: `Valid` é um `def`, e a resolução de
instâncias não o desdobra. A instância explícita
`CycleWitness.decidableValid`, por `inferInstanceAs`, resolve — e o
`#synth` do teste de axiomas confirma que é ela que é escolhida.

## Reutilização, não reimplementação

```text
exists_bounded_iterate_collision   -> detectCycleWitness?_complete
periodic_tail_of_collision         -> CycleWitness.isPeriodicPt
collision_propagates               -> CycleWitness.propagates
Function.mk_mem_periodicPts        -> CycleWitness.mem_periodicPts
```

Os três teoremas de `Periodicity.lean` têm **uma linha de prova cada**, e
são aplicações diretas. Nenhum corpo de teorema anterior foi copiado.
`Function.iterate_add_apply` não aparece.

## O que as provas **não** estabelecem

```text
que o certificado devolvido eh o de menor baseIndex;
que o period devolvido eh o periodo minimo;
que a testemunha devolvida coincide com a do teorema existencial;
qualquer limite de complexidade;
ausencia de duplicatas na enumeracao.
```
