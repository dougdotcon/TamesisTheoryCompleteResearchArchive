---
document_id: ENC-COMPUTABILITY-RESULT
verdict: COMPUTABLE
---

# Resultado de computabilidade

## Confirmado

```text
CertifiedFiniteEncoding    dados executaveis fornecidos
encodedStep                computavel
buildTransitionTable       computavel
tableIndex                 computavel
analyzeEncodedSystem       computavel
```

Verificado por avaliação em sete modelos concretos, todos como teoremas
de regressão por `decide`:

```text
#[0]           Fin 1
#[0, 1]        Bool, id
#[1, 0]        Bool, not
#[1, 2, 2]     Fin 3
#[1, 2, 3, 2]  Fin 4, identidade
#[1, 0, 1, 2]  Fin 4, permutada
#[]            Empty
```

## Tokens proibidos

```text
sorry             0
admit             0
axiom             0
unsafe            0
noncomputable     0
Classical.choose  0
Classical.decEq   0
Fintype.equivFin  0
Trunc.out         0
```

Busca sobre os cinco módulos, o agregador e os três testes. Saída vazia,
código `1`.

## Correções silenciosas

```text
%, mod, getD, clamp, fallback, min, max   0
```

Busca sobre os módulos da frente. Saída vazia, código `1`. Nenhuma
ocorrência sequer textual — melhor que a frente anterior, onde duas
apareciam em documentação.

`Fin.cast` é transporte de tipo e preserva o valor natural, o que é o
conteúdo de `tableIndex_val`.

## A distinção que importa

```yaml
axioma_usado_por_prova:
  onde: campo closed de buildTransitionTable, via Array.getElem_ofFn
  onde: analyzeTransitionTable e seus teoremas, via Fintype.card
  efeito_na_execucao: nenhum — sao Prop, apagados

escolha_classica_produzindo_dado_executavel:
  ocorrencias: 0
  evidencia: sete tabelas concretas verificadas por decide
```

## `decide` não é extração

```yaml
extraction_status: NOT_AUTHORIZED
cli_status: NOT_AUTHORIZED
parser_status: NOT_AUTHORIZED
integration_status: NOT_AUTHORIZED
```

Nenhum binário, alvo Lake executável, `main`, `IO`, arquivo, JSON,
servidor, rede ou banco.
