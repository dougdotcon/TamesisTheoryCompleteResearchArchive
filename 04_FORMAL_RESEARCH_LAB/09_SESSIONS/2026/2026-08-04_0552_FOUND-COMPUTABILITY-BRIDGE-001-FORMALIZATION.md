---
session_id: 2026-08-04_0552_FOUND-COMPUTABILITY-BRIDGE-001-FORMALIZATION
started_at: 2026-08-04T05:52:00-03:00
ended_at: 2026-08-04T05:52:00-03:00
agent: claude-opus-5
git_commit_before: aaab4f9798b8e42de6697dcecad089c667a24b74
git_commit_after: PENDING
active_work_item: FOUND-COMPUTABILITY-BRIDGE-001
authorized_action: FOUND_COMPUTABILITY_BRIDGE_001_FORMALIZATION_AUTHORIZED
result_status: FORMALIZATION_VERIFIED
claims_changed: []
gaps_opened: 0
gaps_closed: 0
---

## Objetivo autorizado

Formalizar as 29 declarações congeladas.

## O que entrou na árvore

```text
Foundations/ComputabilityBridge/Encoding.lean        4 publicas
Foundations/ComputabilityBridge/ResultCodes.lean     8 publicas
Foundations/ComputabilityBridge/Classification.lean  5 publicas
Foundations/ComputabilityBridge/WitnessBound.lean    2 publicas + 1 privado
Foundations/ComputabilityBridge/Instance.lean        2 TEST_ONLY
Foundations/ComputabilityBridge.lean                 agregador
Tests/FoundComputabilityBridge001.lean               7 testes
Tests/FoundComputabilityBridge001Axioms.lean         28 #print axioms
```

Dois agregadores modificados: `Foundations.lean` e `TamesisLab.lean`.

## Build

```text
REAL_LAKE_BUILD_EXIT   0
jobs                   8802
error_lines            0
sorry_lines            0
warning desta frente   0
warning preexistente   1  RHNogo/AsymptoticCore/Incompatibility.lean:49
```

## Contagem, derivada da árvore instalada

```text
publicas   19   (7 def, 4 instance, 8 teoremas)
privado     1
TEST_ONLY   2
testes      7
TOTAL      29
```

Bate **termo a termo** com a especificação congelada. Derivada por
script a partir dos arquivos instalados, não da memória de quem
escreveu.

## Pegada

```text
livres de axioma                  9
propext, Classical.choice, Quot.sound   19
```

Idêntica à do probe. Medida no `#print axioms` do próprio build.

## A correção do gate

A palavra `sorry` aparecia numa **docstring** de `Classification.lean`,
explicando por que a lacuna uniforme não foi preenchida com ela. A
varredura de tokens proibidos encontrou **a própria documentação**.

Precedente já registrado em `FOUND-CYCLE-DETECTION-001`, que moveu sua
lista de proibições para fora dos arquivos Lean pelo mesmo motivo. Texto
movido para `STOP_CONDITIONS.md`; nenhuma assinatura mudou.

Vira proibição: **docstring Lean não carrega token proibido.**

## O que a formalização confirmou

O enunciado negativo sobreviveu:

```lean
theorem primrec_analyzeEncodedSystem (e) (stepS) : Primrec (analyzeEncodedSystem e stepS) :=
  primrec_of_encoding e _          -- uma linha

theorem primrec_of_encoding (e) [Primcodable σ] (f : S → σ) : Primrec f :=
  ...
  Primrec.dom_finite f             -- nunca consulta f
```

E `boolEncoding_primrec_canonical` compila com `Primrec.dom_finite _` sob
a instância **canônica** do Mathlib — mesma conclusão, mesma linha.

## Estado final

```text
formalization_status  VERIFIED
authorized_action     FOUND_COMPUTABILITY_BRIDGE_001_RESULT_REVIEW_AUTHORIZED
claims promovidas     0   (a promocao e do gate seguinte)
nivel uniforme        ENUNCIADO, NAO PROVADO
```
