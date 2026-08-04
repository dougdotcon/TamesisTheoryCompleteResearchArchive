---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-GAPS
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
gaps_opened: 9
gaps_closed_at_specification: 0
---

# Lacunas, declaradas antes de começar

| id | conteúdo | estado |
|---|---|---|
| `CB-GAP-001` | `Primrec₂ analyzeTransitionTable`, o nível uniforme | **DELIBERADAMENTE ABERTA** |
| `CB-GAP-002` | modelo de custo, e portanto qualquer complexidade | **DELIBERADAMENTE ABERTA** |
| `CB-GAP-003` | `Nat.Partrec.Code` e máquinas de Turing — não tocados | ABERTA |
| `CB-GAP-004` | `analyzeTransitionTable_sound` perde o contrato `Valid` | ABERTA |
| `CB-GAP-005` | invariância da classificação sob recodificação | ABERTA |
| `CB-GAP-006` | sistemas não determinísticos | ABERTA |
| `CB-GAP-007` | `Primcodable` para `CertifiedFiniteAbstraction` | ABERTA |
| `CB-GAP-008` | definição de `P_phys` e `NP_phys` de `PVSNP-PHYS-001` | ABERTA |
| `CB-GAP-009` | bibliografia de teoria da computação | **DELIBERADAMENTE ABERTA** |

## `CB-GAP-001`, que é a lacuna com conteúdo

Sobre `RawTransitionTable × Nat` o domínio é **infinito**.
`Primrec.dom_finite` não se aplica, e a classificação passa a depender do
algoritmo: seria preciso mostrar que a lista de candidatos, o `find?` e
a iteração da tabela são primitivos recursivos.

O enunciado elabora — `UniformPrimrecStatement` existe para provar isso.
A demonstração **não é tentada**, e afirmar que ela vale está proibido
por `STOP-CB-006`.

É a única lacuna desta frente cuja resolução produziria informação
algorítmica genuína.

## `CB-GAP-002`, que a frente fecha pela negativa

A pergunta 5 registrada em `ATTACK_READINESS.md` era: existe noção de
custo formalizável **sem** modelo de máquina?

Resposta desta frente: **não neste nível**. `Primrec` e `Computable` são
constantes sobre domínio finito, logo não medem nada. Um custo exige
comprometer-se com um modelo — e comprometer-se está fora do recorte.

A lacuna fica aberta de propósito: fechá-la é escolher um modelo, e
escolher um modelo é decisão de portfólio, não de frente.

## `CB-GAP-004`, a dívida de API que já cobrou juros

```text
detectCycle?_sound            entrega CycleWitness.Valid inteiro
analyzeTransitionTable_sound  devolve 3 clausulas, perde as outras
```

`FOUND-MONOVARIANT-DESCENT-001` reproduziu a redução privada do bloco
`do` para recuperar `0 < period`. Esta frente reproduz **de novo**, para
recuperar `baseIndex + period ≤ size`. São duas cópias fora da frente de
origem, e uma terceira ocorrência do mesmo padrão.

A correção própria é alargar `analyzeTransitionTable_sound`. Isso toca
`ENG-FINITE-STATE-RUNTIME-001`, que está **ENCERRADA**, e exigiria gate
próprio. Enquanto não houver, a duplicação fica declarada.

## `CB-GAP-008`, que é o destino e não o passo

Definir `P_phys` e `NP_phys` era o alvo de `PVSNP-PHYS-001`. Esta frente
é **pré-requisito**, não tentativa: ela mostra que a hierarquia do
Mathlib alcança os objetos do laboratório, e mostra que esse alcance,
sozinho, não define classe nenhuma.

Qualquer definição de classe depende de `CB-GAP-001` e `CB-GAP-002`
estarem fechadas. Nenhuma das duas fecha aqui.
