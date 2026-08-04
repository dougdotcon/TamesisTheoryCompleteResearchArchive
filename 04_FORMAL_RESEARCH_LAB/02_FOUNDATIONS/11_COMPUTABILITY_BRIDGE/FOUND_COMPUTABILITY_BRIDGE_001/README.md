---
document_id: FOUND-COMPUTABILITY-BRIDGE-001-README
work_item_id: FOUND-COMPUTABILITY-BRIDGE-001
specification_status: READY_FOR_REVIEW
research_role: FORMAL_BRIDGE
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# FOUND-COMPUTABILITY-BRIDGE-001

## A pergunta que abriu a frente

Doze frentes encerradas provam coisas sobre sistemas finitos
**executáveis e certificados**. O Mathlib tem `ComputablePred`,
`Nat.Partrec`, `Nat.Partrec.Code` e máquinas de Turing. Nenhum arquivo
sob `TamesisLab/` menciona qualquer um deles.

A frente liga as duas metades — e mede **quanto** essa ligação vale.

## A ponte, que é uma linha

```lean
def encodingPrimcodable (e : CertifiedFiniteEncoding S n) : Primcodable S :=
  Primcodable.ofEquiv (Fin n) (encodingEquiv e)
```

`CertifiedFiniteEncoding` tem exatamente os quatro campos de uma
equivalência. Ela **é** um `S ≃ Fin n`, e `Primcodable.ofEquiv` se aplica
direto. Toda codificação certificada coloca seu tipo dentro da hierarquia
de computabilidade do Mathlib.

## O resultado que importa é NEGATIVO

A ponte existe e **não carrega informação algorítmica nenhuma**.

```lean
theorem primrec_of_encoding (e : CertifiedFiniteEncoding S n) {σ} [Primcodable σ]
    (f : S → σ) : Primrec f
```

Toda função que sai de um tipo com codificação certificada é primitiva
recursiva, e **a prova não olha a função**. Ela é `Primrec.dom_finite`,
que só usa a finitude do domínio.

Consequência, escrita sem rodeio:

```text
o detector e Primrec              SIM
porque a busca e limitada         NAO
porque o dominio e finito         SIM
a classificacao distingue o
detector de uma tabela de
consulta                          NAO
```

Quem quisesse usar "o detector do laboratório é `Primrec`" como degrau
para classe de complexidade **não pode**. A afirmação é verdadeira e
vazia de conteúdo algorítmico.

## As cinco perguntas, respondidas

| # | pergunta | resposta | onde |
|---|---|---|---|
| 1 | `analyzeEncodedSystem` é `Computable`/`ComputablePred`? | **SIM** — por finitude | `Classification.lean` |
| 2 | `CertifiedFiniteEncoding` induz `Primcodable`? | **SIM** — direto | `Encoding.lean` |
| 3 | o detector é `Primrec`, não só `Computable`? | **SIM** — e a busca limitada é irrelevante para isso | `Classification.lean` |
| 4 | `baseIndex + period ≤ n` é cota de RECURSOS? | **NÃO** — é cota do CERTIFICADO | `WitnessBound.lean` |
| 5 | há custo formalizável sem modelo de máquina? | **NÃO neste nível** | `Classification.lean` |

## Onde a pergunta deixa de ser vácua

No nível **uniforme**, sobre `RawTransitionTable × Nat`, o domínio é
infinito, `dom_finite` não se aplica, e a classificação passa a depender
do algoritmo.

```lean
def UniformPrimrecStatement : Prop := Primrec₂ analyzeTransitionTable
```

O enunciado **elabora**. A prova **não é tentada nesta frente** — ver
`CB-GAP-001`. Localizar a pergunta não-vácua é entrega; respondê-la
exigiria gate próprio.

## A armadilha de vacuidade, exposta antes de cair nela

```lean
theorem isEmpty_of_encoding_zero (e : CertifiedFiniteEncoding S 0) : IsEmpty S
```

Em `n = 0` o tipo é vazio e tudo que se diga sobre ele é vácuo — o mesmo
defeito que derrubou `FOUND-MONOVARIANT-DESCENT-001`. A instância
positiva desta frente é `Bool` com `n = 2`, tipo habitado, análise
avaliada concretamente por `decide`.

## O que a frente NÃO entrega

```text
nenhuma classe de complexidade
nenhum custo, nenhuma complexidade assintotica
nenhuma afirmacao sobre P vs NP
nenhuma prova no nivel uniforme
nenhum problema de milenio atacado
```
