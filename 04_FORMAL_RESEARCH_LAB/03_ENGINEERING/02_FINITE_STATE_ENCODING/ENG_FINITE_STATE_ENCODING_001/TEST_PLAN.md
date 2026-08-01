---
document_id: ENC-TEST-PLAN
tests: 8
all_executed_in_probe: true
---

# Plano de testes

Os oito casos foram **executados no probe**, não apenas planejados.

## `ENC-TEST-001` — tipo unitário

```text
S = Fin 1, n = 1, stepS = id
tabela   #[0]
witness  ⟨0, 1⟩          medido
```

## `ENC-TEST-002` — `Bool` com identidade

```text
codificacao   false ↔ 0, true ↔ 1
tabela        #[0, 1]
witness       ⟨0, 1⟩ para false e para true      medido
```

## `ENC-TEST-003` — `Bool` com negação

```text
tabela   #[1, 0]
witness  ⟨0, 2⟩ para false e para true      medido
```

`period = 2`, `baseIndex = 0`. **Sem afirmar minimalidade geral** — o
witness é *um* certificado, e o fato de este ser o de menor período é
observação sobre o caso, não teorema.

## `ENC-TEST-004` — cauda para ponto fixo

```text
sistema  0 → 1 → 2 → 2
tabela   #[1, 2, 2]
witness  ⟨2, 1⟩ a partir de 0        medido
```

## `ENC-TEST-005` — cauda para ciclo de dois

```text
sistema  0 → 1 → 2 → 3 → 2
tabela   #[1, 2, 3, 2]
witness  ⟨2, 2⟩ a partir de 0        medido
```

## `ENC-TEST-006` — codificação permutada

Mesmo sistema, codificação `i ↦ 3 - i` nos dois sentidos.

```text
tabela   #[1, 0, 1, 2]     DIFERENTE de #[1, 2, 3, 2]
witness  ⟨2, 2⟩            IGUAL
```

Este é o teste que justifica a frente. Os números da tabela mudaram
completamente; o witness semântico não mudou.

Registrado explicitamente: **não** se exige o mesmo array, e a igualdade
dos witnesses **não** é elevada a teorema — isso exigiria provar
invariância da ordem de busca do detector, que não é resultado desta
frente.

## `ENC-TEST-007` — tipo vazio

```text
Empty → Fin 0
tabela   #[]        medido
```

Nenhum `start : Empty` é fornecido — não existe. A ausência de chamada é
garantida pelo tipo.

## `ENC-TEST-008` — anti-correção do índice

```lean
example : ((permEnc.tableIndex tailStep ⟨0, _⟩ : Fin _) : Nat) = 3 := by decide
```

Passou. Sob codificação permutada, o transporte preserva o valor natural.

## Método

```text
por decide e por rfl;
sem native_decide;
sem benchmark;
sem afirmacao de desempenho.
```

Mesma política das duas frentes anteriores.
