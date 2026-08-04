---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-RESULT-REVIEW
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
review_start_head: 73897d2c9c1532460dd4e0e3fbce4645d153d1b4
decision: FOUND_COMPUTABILITY_BRIDGE_001_RESULT_REVIEW_APPROVED
defects_found: 1
defects_corrected: 1
signatures_divergent: 0
---

# Revisão de resultado

## Reexecução

```text
REAL_LAKE_BUILD_EXIT   0
jobs                   8802
error_lines            0
sorry_lines            0
warning desta frente   0
```

## Confronto assinatura a assinatura

Script comparando os **nomes instalados** com os **nomes congelados** na
`SPECIFICATION_DECISION.md`:

```text
instaladas            29
na spec, ausentes      0
duplicadas             0
divergentes            0
```

O comparador acusou uma "instalada a mais": `analyze_reduce_cb`. **Não é
divergência** — é o auxiliar privado, que a especificação declara em
prosa e não em bloco de código, e por isso o regex não o vê.

Defeito do **comparador**, não do resultado. Registrado como
`RES-REV-CB-001`; a correção é declarar a assinatura do privado em bloco,
feita agora.

## Pegada, medida no build

```text
livres de axioma                         9
propext, Classical.choice, Quot.sound   19
cobertura                               28 de 29
```

O auxiliar privado não é alcançável do arquivo de testes; sua pegada é
medida no probe. Idêntica à prevista.

## Os onze itens

| # | Item | Veredito |
|---|---|---|
| 1 | `lake build` exit 0, 0 error, 0 sorry | CONFIRMADO |
| 2 | 29 declarações, derivadas da árvore instalada | CONFIRMADO |
| 3 | Nomes instalados = nomes congelados | CONFIRMADO |
| 4 | Pegada 9 / 19, como previsto | CONFIRMADO |
| 5 | O enunciado central permanece NEGATIVO | CONFIRMADO |
| 6 | `primrec_of_encoding` não consulta `f` | CONFIRMADO |
| 7 | O nível uniforme segue enunciado e não provado | CONFIRMADO |
| 8 | Instância positiva em tipo habitado | CONFIRMADO |
| 9 | Nenhuma frente encerrada tocada | CONFIRMADO |
| 10 | `0` tokens proibidos nos arquivos Lean | CONFIRMADO |
| 11 | Assinatura do auxiliar privado ausente do bloco | **CORRIGIDO** |

## O item 5, que é o que a revisão existia para proteger

O revisor procurou, no código instalado, qualquer coisa que sugerisse
que a classificação diga algo sobre o algoritmo. O que encontrou:

```lean
theorem primrec_analyzeEncodedSystem (e) (stepS) : Primrec (...) :=
  primrec_of_encoding e _

theorem primrec_of_encoding (e) [Primcodable σ] (f : S → σ) : Primrec f :=
  ... Primrec.dom_finite f
```

Duas linhas de corpo, e nenhuma menciona a análise. O enunciado negativo
não foi diluído pela formalização — foi **confirmado por ela**.

E `boolEncoding_primrec_canonical` compila sob a instância **canônica**
do Mathlib, sem `haveI`, com o mesmo `Primrec.dom_finite _`. Duas
codificações diferentes, mesma conclusão, mesma linha: a codificação não
importa porque quem trabalha é a finitude.

## O que a frente entregou que NÃO é trivial

Ser honesto sobre a vacuidade não obriga a fingir que nada foi feito:

```text
analyzeTransitionTable_bound   cota do certificado, recuperada da
analyzeEncodedSystem_bound     terceira clausula de Valid que
                               analyzeTransitionTable_sound perde

4 instancias Primcodable       sem elas o enunciado central nao e
                               sequer escrevivel

isEmpty_of_encoding_zero       a armadilha n = 0, nomeada antes de
                               alguem cair nela
```

O que é trivial é a **conclusão de computabilidade**, não o trabalho de
tornar o laboratório enunciável dentro da hierarquia.

## Decisão

`FOUND_COMPUTABILITY_BRIDGE_001_RESULT_REVIEW_APPROVED`.

Uma claim promovida, `COMPUTABILITY-CLASSIFICATION-VACUITY-FORMAL-001`,
com nível de evidência `F` e os qualificadores obrigatórios. Dez lacunas
seguem abertas, `CB-GAP-001` à frente.
