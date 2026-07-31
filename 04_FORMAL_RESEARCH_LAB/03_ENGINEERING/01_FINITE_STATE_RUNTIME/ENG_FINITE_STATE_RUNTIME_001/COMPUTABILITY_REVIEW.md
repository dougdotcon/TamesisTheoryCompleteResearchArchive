---
document_id: RT-COMPUTABILITY-REVIEW
stage: SPECIFICATION_REVIEW
verdict: COMPUTABLE
---

# Revisão de computabilidade

## Confirmado por probe

```text
validateTransitionTable   #eval
validateStart             #eval, atraves de analyzeT
step                      reducao concreta (step_val por rfl)
step?                     #eval, atraves de run?
run?                      #eval
detectCycle?              #eval, atraves de analyzeT
analyzeTransitionTable    #eval em treze casos
```

## Proibições verificadas nos corpos executáveis

```text
marca de nao-computabilidade    ausente
escolha classica extraindo dado  ausente
igualdade decidivel classica     ausente
modulo                           ausente
clamp                            ausente
getD                             ausente
objeto de orbita quociente       ausente
grafos simples                   ausente
```

## Pegada axiomática medida

```text
validateT                  [propext, Quot.sound]
validateStartT             [propext, Quot.sound]
run?_eq_iterate_step       [propext, Quot.sound]
analyzeT                   [propext, Classical.choice, Quot.sound]
detectCycle?_raw_repeat    [propext, Classical.choice, Quot.sound]
```

Achado que a revisão destaca: **as duas camadas de validação e o teorema
central de correspondência não dependem de `Classical.choice`.** A pegada
só aparece onde o detector entra, por `Fintype.card`/`Finset.univ` — a
origem já localizada em `FOUND-CYCLE-DETECTION-001`.

Isso confirma a arquitetura em camadas: a ponte `Array → Fin` é
axiomaticamente mais leve que o detector que ela alimenta.

## Regra reafirmada

```text
a presenca infraestrutural de propext, Classical.choice e Quot.sound nao
bloqueia a especificacao se:

  nenhuma definicao for noncomputable;
  #eval funcionar;
  nenhum Classical.choose produzir dado.
```

Os três confirmados.

## Hipóteses públicas

```text
o consumidor fornece Array Nat e Nat.
```

Não são exigidos `Fintype`, `DecidableEq`, `Fin`, `Nonempty`,
`Inhabited`, provas ou funções Lean. As instâncias `Fintype (Fin n)` e
`DecidableEq (Fin n)` são inferidas **internamente**, no ponto em que
`detectCycle?` aplica o detector.

## Execução bruta fora dos limites — auditada

```text
run? 0 999 = some 999      inclusive para tabela vazia
run? 1 999 = none          primeiro lookup invalido
```

A semântica de zero passos **não** foi corrigida. `run?` é semântica
bruta parcial e fiel ao array; `validateStart` é a barreira de segurança
da API dinâmica. Essa separação é o que permite enunciar
`detectCycle?_raw_repeat` sobre a tabela original sem hipótese extra.

## `#eval` não é extração

`extraction_status` permanece `READY_FOR_FEASIBILITY_AUDIT` e
`extraction_authorized` permanece `false`. Nenhum binário, alvo Lake,
CLI, JSON, arquivo, rede ou banco pertence a esta frente.
