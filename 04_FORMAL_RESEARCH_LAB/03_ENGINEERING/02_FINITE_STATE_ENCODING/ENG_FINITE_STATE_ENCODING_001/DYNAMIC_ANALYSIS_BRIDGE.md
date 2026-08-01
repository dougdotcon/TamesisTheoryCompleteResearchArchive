---
document_id: ENC-DYNAMIC-ANALYSIS-BRIDGE
probe_status: PROBE_PROVED
---

# A ponte da análise dinâmica

## Definição

```lean
def analyzeEncodedSystem (e : CertifiedFiniteEncoding S n) (stepS : S → S) (start : S) :
    Except RuntimeCycleError CycleWitness :=
  analyzeTransitionTable (buildTransitionTable e stepS).toRaw
    ((e.encode start : Fin n) : Nat)
```

Uma linha de corpo. Nenhuma lógica nova: constrói a tabela e chama a API
verificada da frente anterior.

## Entradas públicas

```text
CertifiedFiniteEncoding S n
S -> S
S
```

**Zero typeclasses exigidas do consumidor.** Mesma propriedade que a
frente anterior alcançou com `Array Nat` e `Nat`.

## Congelado

```text
a API permanece Except;
nenhum CycleWitness padrao;
nenhum Option.get;
nenhuma totalizacao do detector;
nenhum tipo de erro novo;
nenhum parser;
nenhuma entrada textual.
```

`RuntimeCycleError` é reutilizado **sem alteração**. Os três construtores
continuam existindo, inclusive `internalDetectorFailure`, cuja
impossibilidade é teorema e não motivo de remoção.

## Por que `encode start` e não `tableIndex start`

O argumento de `analyzeTransitionTable` é um `Nat`, e
`tableIndex_val` garante que os dois produzem **o mesmo** `Nat`. Escrever
`encode start` mantém a definição legível e faz o enunciado dos teoremas
falar do objeto do consumidor.

## Resultados medidos

| Teste | Sistema | Tabela | Witness |
|---|---|---|---|
| `ENC-TEST-001` | `Fin 1`, `id` | `#[0]` | `⟨0,1⟩` |
| `ENC-TEST-002` | `Bool`, `id` | `#[0,1]` | `⟨0,1⟩` nos dois estados |
| `ENC-TEST-003` | `Bool`, `not` | `#[1,0]` | `⟨0,2⟩` nos dois estados |
| `ENC-TEST-004` | `Fin 3`, cauda a ponto fixo | `#[1,2,2]` | `⟨2,1⟩` |
| `ENC-TEST-005` | `Fin 4`, cauda a ciclo de 2 | `#[1,2,3,2]` | `⟨2,2⟩` |
| `ENC-TEST-006` | idem, codificação `i ↦ 3-i` | `#[1,0,1,2]` | `⟨2,2⟩` |
| `ENC-TEST-007` | `Empty`, `id` | `#[]` | não há chamada bem tipada |

`ENC-TEST-006` é o resultado que mais importa: **os números da tabela
mudaram, o witness semântico não.**
