---
bridge_id: GLOBAL-WEYL-BRIDGE-SCALAR
status: SPECIFIED_NOT_PROVED
version: 2
input: "P : W-ELLIPTIC-SCALAR-BRIDGE"
output: "N_P pertence a W-POWER com α = d/m e C_P > 0"
---

# GLOBAL-WEYL-BRIDGE-SCALAR — obrigações

Onze obrigações (a `GWB-008` foi dividida em três). **Nenhuma é provada.**

Estados: `SOURCE_DIRECT`, `SOURCE_CITED_RESULT`, `BRIDGE_DOCUMENTED`,
`EXPLICIT_CLASS_ASSUMPTION`, `ELEMENTARY_COROLLARY`,
`DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE`,
`ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE`,
`DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE`, `UNRESOLVED`.

---

```yaml
- id: GWB-001
  statement: "P possui espectro discreto enumeravel, com multiplicidades finitas."
  source: "W_ELLIPTIC_SCALAR_V3.md (hipotese incorporada B6)"
  page: null
  equation_or_theorem: null
  evidence_status: EXPLICIT_CLASS_ASSUMPTION
  additional_assumptions: ["compacidade de M"]
  requires_formalization: false
  classification_document: DISCRETENESS_CLASSIFICATION.md
  note: >
    Incorporada a definicao da classe, NAO derivada. Coriasco-Doll
    estabelecem a cadeia analoga no contexto SG deles, que NAO eh o de
    variedade compacta; usar isso como fonte seria transportar enunciado
    entre contextos. GAP-RH-012 aberto.

- id: GWB-002
  statement: "N_P(Lambda) = #{j | lambda_j < Lambda} esta bem definida e eh finita para cada Lambda finito."
  source: CORIASCO-DOLL-2020
  page: "p.1"
  equation_or_theorem: "eq. (1)"
  evidence_status: SOURCE_CITED_RESULT
  additional_assumptions: ["GWB-001"]
  requires_formalization: true
  classification_document: DISCRETENESS_CLASSIFICATION.md
  note: >
    Definicao e convencao de desigualdade ESTRITA sao de fonte literal; a
    finitude eh corolario elementar DADO GWB-001. Ver
    SPECTRAL_MATCH_CONVENTIONS.md e SB-GAP-003.

- id: GWB-003
  statement: "N_P(Lambda) = Tr(E_Lambda)."
  source: CORIASCO-DOLL-2020
  page: "Secao 3 (Wave Trace)"
  equation_or_theorem: "N(lambda) = Tr integral_0^lambda dE(lambda)"
  evidence_status: SOURCE_CITED_RESULT
  additional_assumptions: ["E_Lambda de posto finito", "GWB-001"]
  requires_formalization: true

- id: GWB-004
  statement: "Tr(E_Lambda) = integral_M e(x,x,Lambda) dx."
  source: IVRII-2016
  page: "Secao 3.1.1, 'Rescaling technique'"
  equation_or_theorem: "(3.1.11)"
  evidence_status: SOURCE_CITED_RESULT
  additional_assumptions: ["e(x,x,Lambda) integravel na diagonal", "CASO ESCALAR (B1)"]
  requires_formalization: true
  note: >
    (3.1.11) eh ESCALAR. A versao fibrada com tr_E nao foi lida em fonte
    alguma - ver W_ELLIPTIC_SYSTEM_DEFERRED.md. Evidencia canonica:
    pdf/ivrii_2016_100years_weyl.pdf, sha256 9ca07737...

- id: GWB-005
  statement: "A assintota local eh uniforme em x."
  source: HORMANDER-1968
  page: "p.215"
  equation_or_theorem: "Teorema 5.1, eq. (5.3)"
  evidence_status: SOURCE_DIRECT
  additional_assumptions: ["a estimativa eh uniforme em COMPACTOS; M compacta torna isso uniformidade global"]
  requires_formalization: true
  note: >
    UNICA obrigacao sustentada por leitura direta do artigo original.
    Hormander 1968 eh citado aqui pelo resultado LOCAL, conforme GAP-RH-013.

- id: GWB-006
  statement: "A integracao do termo principal produz C_P * Lambda^(d/m)."
  source: "HORMANDER-1968 (1.1) p.193 + homogeneidade de grau m do simbolo principal (B5)"
  page: "p.193"
  equation_or_theorem: "(1.1); comparar IVRII-2016 (3.1.3)"
  evidence_status: ELEMENTARY_COROLLARY
  additional_assumptions:
    - "p_m(x,.) homogeneo de grau m ==> vol{p_m < Lambda} = Lambda^(d/m) vol{p_m < 1}"
    - "x |-> vol(B_x) integravel sobre M compacta"
  requires_formalization: true
  note: >
    Formula ESCALAR. NAO aplicada a sistemas: a constante correta para
    sistemas eh IVRII (3.1.3) com n(x,xi).

- id: GWB-007
  statement: "A integracao do erro preserva ordem inferior ao termo principal."
  source: "HORMANDER-1968 (5.3) + compacidade de M"
  page: "p.215"
  equation_or_theorem: "(5.3)"
  evidence_status: ELEMENTARY_COROLLARY
  additional_assumptions: ["vol(M) < infinito", "(d-1)/m < d/m", "d >= 1 (B4)"]
  requires_formalization: true

- id: GWB-008A
  statement: >
    vol(B_x) > 0 para cada x, e integral_M vol(B_x) dx > 0, onde
    B_x = {xi : p_m(x,xi) < 1}.
  source: "nenhuma fonte obtida afirma"
  page: null
  equation_or_theorem: null
  evidence_status: DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE
  additional_assumptions:
    - "B5: p_m real, > 0 fora da secao nula, homogeneo de grau m > 0"
    - "B3: M nao vazia"
    - "B4: d >= 1"
    - "continuidade de x |-> vol(B_x) (NAO lida em fonte; ver GAP-RH-015)"
  requires_formalization: partial
  argument_document: WEYL_COEFFICIENT_POSITIVITY.md
  formalized_core: "measure_pos_of_isOpen_subset (passo 5 de 6)"
  note: >
    Argumento em seis passos. Passos 1-4 e 6 sao DOCUMENTAIS. Somente o
    passo 5 - "contem aberto nao vazio logo tem medida positiva" - tem
    nucleo abstrato verificado em Lean. O invólucro NAO prova a lei de Weyl.

- id: GWB-008B
  statement: "C_P = (2pi)^(-d) * integral_M vol(B_x) dx > 0."
  source: "nenhuma fonte obtida afirma"
  page: null
  equation_or_theorem: null
  evidence_status: ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE
  additional_assumptions: ["GWB-008A", "(2pi)^(-d) > 0"]
  requires_formalization: partial
  formalized_core: "coefficient_pos_of_factors"
  note: >
    Produto de dois positivos. GAP-RH-014 passa a
    RESOLVED_DOCUMENTALLY_FOR_SCALAR_BRIDGE_CLASS_ONLY - nao a CLOSED.

- id: GWB-008C
  statement: "C_P < infinito."
  source: "nenhuma fonte obtida afirma"
  page: null
  equation_or_theorem: null
  evidence_status: DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE
  additional_assumptions:
    - "cota inferior uniforme p_m(x,xi) >= c |xi|^m sobre o fibrado cosferico"
    - "compacidade de S*M"
  requires_formalization: false
  gap: GAP-RH-015
  note: >
    Obrigacao SEPARADA: W-POWER exige constante real, logo finita. Em Lean
    a finitude fica implicita no tipo `constant : R`; nao desaparece por
    isso. Formaliza-la exigiria definir fibrado cosferico e simbolo -
    PROIBIDO neste gate.

- id: GWB-009
  statement: "N_P(Lambda)/Lambda^(d/m) -> C_P."
  source: "consequencia de GWB-002..008C, ou citacao direta"
  page: null
  equation_or_theorem: null
  evidence_status: BRIDGE_DOCUMENTED
  additional_assumptions: ["todas as anteriores"]
  requires_formalization: true
  note: >
    Enunciado equivalente citado por CORIASCO-DOLL-2020 p.1
    (N(lambda) = gamma*lambda^(d/m) + O(lambda^((d-1)/m))) e por
    IVRII-2016 (3.1.1). Duas rotas independentes; NENHUMA provada.
```

---

## Redução do requisito

Para `W-POWER` basta a **assintótica de um termo**. Ivrii, Example
3.1.1(iv): *"without any non-degeneracy assumption we arrive to one-term
asymptotics with the remainder estimate `O(λ^{(d−1+δ)/m})`"*.

Consequência: micro-hiperbolicidade e não periodicidade **não são
necessárias** para GWB-009. Qualquer resto `o(Λ^{d/m})` basta.

## Resumo por estado

| Estado | Obrigações |
|---|---|
| `SOURCE_DIRECT` | GWB-005 |
| `SOURCE_CITED_RESULT` | GWB-002, GWB-003, GWB-004, (GWB-009 por citação) |
| `ELEMENTARY_COROLLARY` | GWB-006, GWB-007 |
| `DOCUMENTED_ARGUMENT_WITH_FORMALIZED_CORE` | GWB-008A |
| `ELEMENTARY_COROLLARY_WITH_FORMALIZED_CORE` | GWB-008B |
| `DOCUMENTED_STANDARD_ARGUMENT_REQUIRING_SOURCE` | GWB-008C |
| `EXPLICIT_CLASS_ASSUMPTION` | GWB-001 |
| `BRIDGE_DOCUMENTED` | GWB-009 (pela ponte) |

Nenhuma `UNRESOLVED` no caso escalar. A `UNRESOLVED` de dois gates atrás —
fibrados na etapa D — foi **removida por estreitamento da classe**, não
resolvida; `GAP-RH-009` continua **aberto**.

## Nenhuma prova executada

Este documento enumera obrigações. Nenhuma foi demonstrada. O único
conteúdo em Lean é o núcleo de teoria da medida descrito em
`GEOMETRIC_LEAN_SCOPE.md`, que cobre um passo de um argumento de seis.
