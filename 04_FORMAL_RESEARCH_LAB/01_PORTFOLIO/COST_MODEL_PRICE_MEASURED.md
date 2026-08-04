---
document_id: COST-MODEL-PRICE-MEASURED-2026-08-04
measured_at: 2026-08-04
refines: PORTFOLIO-REVIEW-COST-MODEL-2026-08-04
probe_exit: 0
verdict: RESEARCH_SCALE_FRONT_MAY_NOT_CLOSE
---

# O preco do modelo de custo, agora com numeros

`DEC-046` registrou que instanciar `TM2ComputableInPolyTime` seria
"caro". Isso era adjetivo. Agora e medido.

## `FinTM2` exige 14 campos

```text
dados explicitos (8)   k0, k1, Gamma, Lambda, main, sigma, initialState, m
tipo implicito (1)     K
instancias (5)         DecidableEq K, Fintype K, Fintype Lambda,
                       Fintype sigma, Fintype (Gamma k0)
```

`Fintype Lambda` e o campo decisivo. Volta no item da ponte.

## O unico exemplo do Mathlib custa 20 linhas e nao computa nada

`Computable.lean` tem 292 linhas. `idComputer` (204-213) e
`idComputableInPolyTime` (221-230) somam **20 linhas**, sob
`noncomputable section`.

O que ha dentro: `K := Unit`, `Lambda := Unit`, `sigma := Unit`, e o
programa inteiro e `m _ := halt`. A maquina para no passo 1 sem tocar em
pilha nenhuma, e por isso `evals_in_steps` fecha com `rfl`.

**Zero computacao e verificada nessas 20 linhas.** O piso medido e vacuo:
ele nao estabelece quanto custa uma maquina que faz alguma coisa.

## `TM2OutputsInTime` e `Type`, nao `Prop`

```text
TM2OutputsInTime : (tm : FinTM2) -> ... -> Nat -> Type
```

`outputsFun` **produz dado**: para cada entrada e preciso CONSTRUIR o
traco de execucao — `steps`, `evals_in_steps`, `steps_le_m` — e nao
apenas afirmar que existe. Nao ha saida por existencia classica.

## Nao ha segundo exemplo, e nao ha composicao

```text
grep -rl FinTM2 em todo o Mathlib   ->  1 arquivo
TM2ComputableInPolyTime.comp        ->  proof_wanted (284-288)
```

As quatro construcoes nomeadas derivam todas da mesma identidade. E o
Mathlib **nao sabe compor** dois objetos desses: sem lema de composicao a
construcao nao e modular, e nao ha como montar `analyzeTransitionTable`
por pecas.

## A ponte que parecia existir vai na direcao certa e entrega a moeda errada

`ToPartrec.lean`, 1290 linhas, compila `Code` em programa TM2.

```text
direcao          Partrec -> TM2      (de Primrec ainda faltaria
                                      Primrec -> Partrec -> Code)
produz FinTM2?   NAO. FinTM2 nao aparece uma vez no arquivo.
pode produzir?   NAO. Fintype PartrecToTM2.Lambda' e FALSE, medido.
                 Lambda'.move e recursivo; o tipo e genuinamente infinito.
                 O Mathlib contorna com TM2.Supports + codeSupp, condicao
                 ESTRITAMENTE MAIS FRACA que o Fintype exigido por FinTM2.
contagem de passos?  NENHUMA. So tr_eval, igualdade extensional.
```

E o proprio cabecalho do arquivo, linhas 47-48, diz: *"We don't prove it
here, but in anticipation of the complexity class P, the simulation is
actually polynomial-time as well."* **O limite polinomial e um
nao-teorema declarado no Mathlib.**

`primrec_analyzeTransitionTable`, que o laboratorio provou, tambem nao
ajuda: `Primrec` nao carrega modelo de custo algum.

## Falta ainda a camada de codificacao

`Mathlib/Computability/Encoding.lean`, 267 linhas, so oferece `Encoding`
para `Nat`, `Bool`, `List a` e `Prod`. Nao ha nada para `Array`, `Except`
ou struct. `RawTransitionTable`, `CycleWitness` e `RuntimeCycleError`
exigiriam `Encoding` escritos a mao com prova de injetividade.

## Veredito

```text
frente de escala de PESQUISA, 4 digitos de linhas Lean,
com risco de NAO FECHAR
```

Para instanciar `TM2ComputableInPolyTime` em `analyzeTransitionTable`
seria preciso, nesta ordem:

```text
1. Encodings a mao para Array, Except e dois structs
2. uma TM2 concreta para validacao + validacao + deteccao com laco
3. o traco de execucao COMO DADO, por inducao, nao por rfl
4. um limite polinomial uniforme  <- o Mathlib NUNCA fez isso
                                     para funcao nenhuma
5. tudo sem lema de composicao, que e proof_wanted
```

O passo 4 e o que decide: **nao existe precedente no Mathlib de limite
de passos polinomial sobre uma TM2 concreta.** O laboratorio nao estaria
aplicando teoria existente; estaria criando-a.

## Consequencia para `PVSNP-PHYS-001`

Nao e pre-requisito que se resolva com incremento. E a frente inteira, e
o produto dela ainda seria uma **definicao de classe** — nao um ataque.
