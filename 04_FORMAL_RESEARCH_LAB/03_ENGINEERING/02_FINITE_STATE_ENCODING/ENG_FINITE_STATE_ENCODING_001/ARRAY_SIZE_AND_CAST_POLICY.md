---
document_id: ENC-ARRAY-SIZE-AND-CAST-POLICY
central_risk: true
probe_status: PROBE_PROVED
---

# Política de tamanho e de casts

## O risco

```text
Fin n  NAO eh definicionalmente igual a  Fin (Array.ofFn f).size
```

`Array.size_ofFn` é um **teorema**, não uma definição. Este é o risco que
o gate de portfólio classificou como o que custaria tempo, e é
`STOP-ENC-005`.

## Orientação única

```lean
theorem buildTransitionTable_size (e) (stepS) :
    (buildTransitionTable e stepS).next.size = n :=
  Array.size_ofFn
```

Orientação **`size = n`**. Congelada. Termo de uma linha: a defeq
`(buildTransitionTable e stepS).next ≡ Array.ofFn f` é aceita em modo
termo, embora **não** por `rw`/`simp`, que trabalham em transparência
reduzida. Esse contraste é o achado técnico central deste gate.

Não existirão `table_size_eq`, `size_table_eq` nem `stateCount`. Onde a
orientação inversa for necessária, usa-se `.symm` **desta** igualdade.

## Ponto único de transporte

```lean
def CertifiedFiniteEncoding.tableIndex (e) (stepS) (s : S) :
    Fin (buildTransitionTable e stepS).next.size :=
  Fin.cast (buildTransitionTable_size e stepS).symm (e.encode s)
```

Regra vinculante:

```text
Todo transporte Fin n <-> Fin table.next.size passa por tableIndex
ou pelo lema central de leitura. Nenhum outro ponto da API transporta.
```

## Lema central de leitura

```lean
theorem buildTransitionTable_getElem (e) (stepS)
    (i : Fin (buildTransitionTable e stepS).next.size) :
    (buildTransitionTable e stepS).next[i]
      = ((e.encodedStep stepS (Fin.cast (buildTransitionTable_size e stepS) i) : Fin n) : Nat) :=
  Array.getElem_ofFn (f := fun j => ((e.encodedStep stepS j : Fin n) : Nat)) i.isLt
```

**Termo de uma linha, por defeq.** Este é o segundo — e último — ponto de
transporte, e ele usa a igualdade na orientação direta, sem `.symm`.

Quatro rotas foram testadas no probe:

| Variante | Tática | Resultado |
|---|---|---|
| `cv1` | `simp [buildTransitionTable]` | **falhou**, objetivo intacto |
| `cv2` | `show` + `rw [Array.getElem_ofFn]` | quase; deixou um objetivo residual trivial |
| `cv3` | `unfold` + `simp` | **falhou**, objetivo intacto |
| `cv4` | termo puro `Array.getElem_ofFn ... i.isLt` | **PASSOU** |

A rota escolhida é `cv4`. A lição é a mesma do teorema de tamanho: **em
modo termo a defeq resolve; em modo tático ela não é vista.**

## Proibições

```text
cast avulso em cada prova
Eq.ndrec manual
Classical.choice para transportar
heq
modulo, clamp, fallback
```

Se a formalização precisar de um terceiro ponto de transporte,
`STOP-ENC-005` dispara e a frente para.


---

## Revisão — `2066edc`

**Superado** por `FINAL_CAST_POLICY.md`.

Confirmado: dois pontos de transporte, orientação `size = n`,
`tableIndex_val` por `rfl`. Acrescentado pela revisão: `@[simp]` em
`tableIndex_val`, e a medição explícita de que
`(Array.ofFn f).size` **não** é definicionalmente igual a `n` para `n`
genérico — erro reproduzido no probe de axiomas.
