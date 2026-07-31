---
bridge_id: GLOBAL-WEYL-DATA-BRIDGE
status: SPECIFIED_NOT_PROVED
input: "dado geometrico (d, m, C_P) extraido de P : W-ELLIPTIC-SCALAR-BRIDGE"
output: "PowerCountingLaw N_P com exponent = d/m e constant = C_P"
---

# GLOBAL-WEYL-DATA-BRIDGE

## Por que existe

A interface Lean `PowerCountingLaw` (em
`TamesisLab/RHNogo/Bridge/Definitions.lean`) consome exatamente **três
dados** e **uma convergência**:

```lean
structure PowerCountingLaw (N : ℝ → ℝ) where
  exponent : ℝ
  constant : ℝ
  exponent_pos : 0 < exponent
  constant_pos : 0 < constant
  tendsto_normalized :
    Tendsto (fun T : ℝ => N T / T ^ exponent) atTop (nhds constant)
```

O lado geométrico produz `d`, `m` e `C_P`. Este documento diz, campo a
campo, **quem fornece o quê e com que evidência**. É especificação de
interface, não prova.

## Tabela de instanciação

```yaml
- lean_field: exponent
  geometric_value: "d / m"
  supplier: "dimensao de M e ordem do operador"
  evidence: SOURCE_CITED_RESULT
  source: "CORIASCO-DOLL-2020 p.1 (expoente d/m na lei enunciada)"

- lean_field: exponent_pos
  geometric_value: "0 < d/m"
  supplier: "B4 (d >= 1) e S5 (m > 0)"
  evidence: FORMALIZED
  lean: "dimension_div_order_pos"
  note: "d >= 1 eh EXPLICIT_BRIDGE_ASSUMPTION; sem ela a interface falha."

- lean_field: constant
  geometric_value: "C_P = (2pi)^{-d} integral_M vol{p_m(x,.) < 1} dx"
  supplier: "GWB-006"
  evidence: ELEMENTARY_COROLLARY
  source: "HORMANDER-1968 (1.1) p.193; comparar IVRII-2016 (3.1.3)"
  note: >
    Formula ESCALAR. NAO aplicada a sistemas: para sistemas a constante
    correta eh (3.1.3) com n(x,xi).

- lean_field: constant_pos
  geometric_value: "C_P > 0"
  supplier: "GWB-008A + GWB-008B"
  evidence: DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE
  lean: "coefficient_pos_of_factors, measure_pos_of_isOpen_subset"
  note: "nenhuma fonte obtida afirma C_P > 0; ver GAP-RH-014."

- lean_field: "(finitude implicita de constant : R)"
  geometric_value: "C_P < infinito"
  supplier: "GWB-008C"
  evidence: DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE
  gap: GAP-RH-015
  note: >
    Em Lean, `constant : R` ja EXIGE finitude; a obrigacao nao desaparece
    por estar embutida no tipo, apenas fica implicita. Registrada aqui
    para nao se perder.

- lean_field: tendsto_normalized
  geometric_value: "N_P(Lambda)/Lambda^(d/m) -> C_P"
  supplier: "GWB-009"
  evidence: BRIDGE_DOCUMENTED
  note: >
    Duas rotas: (a) cadeia GWB-002..008; (b) citacao direta de
    CORIASCO-DOLL-2020 p.1 e IVRII-2016 (3.1.1). NENHUMA foi provada.

- lean_field: "N (a funcao contada)"
  geometric_value: "N_P(Lambda) = #{j : lambda_j < Lambda}"
  supplier: "GWB-001 + GWB-002"
  evidence: EXPLICIT_CLASS_ASSUMPTION + SOURCE_CITED_RESULT
  note: >
    Desigualdade ESTRITA, convencao fixada por CORIASCO-DOLL-2020 eq.(1).
    Ver SPECTRAL_MATCH_CONVENTIONS.md e SB-GAP-003.
```

## Cadeia completa, com o que está verificado

```text
P : W-ELLIPTIC-SCALAR-BRIDGE
        |
        |  GLOBAL-WEYL-BRIDGE-SCALAR   (GWB-001..009)   NAO PROVADO
        v
GLOBAL-WEYL-DATA-BRIDGE  (este documento)              ESPECIFICADO
        |    nucleo de positividade                     VERIFICADO
        v
PowerCountingLaw N_P  (alpha = d/m, C = C_P)
        |
        |  COUNTING-LAW-BRIDGE                          VERIFICADO
        v
ASYM-NOGO-001                                           VERIFICADO
```

Duas caixas verificadas, duas não. O gargalo é, e continua sendo, a
travessia `GWB-001..009` — que **não** é objeto deste gate.

## Prova de que a instanciação não foi feita

Não existe em Lean nenhum termo do tipo `PowerCountingLaw N_P` para um
`N_P` proveniente de operador. Não existe `N_P`. Não existe operador.
`ASYM-NOGO-001` **não** foi aplicado.

O que existe é a interface `PositiveWeylCoefficient`, que produz o campo
`constant_pos` **quando** alguém fornecer os dois fatores positivos — e
ninguém os forneceu a partir de geometria real.

## Rotas de escape preservadas

Este documento **não** fecha nenhuma das 14 rotas de `ESCAPE_ROUTES.md`. Em
particular:

- Operadores fora de `W-ELLIPTIC-SCALAR-BRIDGE` (sistemas, bordo, ordem
  não pseudodiferencial, `d = 0`, `M` vazia) escapam por construção.
- Hilbert–Pólya **não** é excluído. Nada aqui afirma que não exista
  operador cujo espectro reproduza os zeros; afirma-se apenas que, para
  ser tratado por esta rota, ele teria de estar nesta classe estreita.
