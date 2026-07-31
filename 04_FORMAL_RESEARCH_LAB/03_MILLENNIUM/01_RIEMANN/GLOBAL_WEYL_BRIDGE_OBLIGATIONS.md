---
bridge_id: GLOBAL-WEYL-BRIDGE-SCALAR
status: SPECIFIED_NOT_PROVED
input: "P : W-ELLIPTIC-SCALAR"
output: "N_P pertence a W-POWER com α = d/m e C_P > 0"
---

# GLOBAL-WEYL-BRIDGE-SCALAR — obrigações

Nove obrigações. **Nenhuma é provada neste gate.**

Estados: `SOURCE_DIRECT`, `SOURCE_CITED_RESULT`, `BRIDGE_DOCUMENTED`,
`EXPLICIT_CLASS_ASSUMPTION`, `ELEMENTARY_COROLLARY`, `UNRESOLVED`.

---

```yaml
- id: GWB-001
  statement: "P possui espectro discreto enumeravel, com multiplicidades finitas."
  source: "W_ELLIPTIC_SCALAR_V2.md (hipotese incorporada); analogia com CORIASCO-DOLL-2020 Secao 3"
  page: "Coriasco-Doll, Secao 3 (contexto SG, nao variedade compacta)"
  equation_or_theorem: "cadeia resolvente compacto -> base ortonormal -> 0 < lambda_1 <= ... -> +infinito"
  evidence_status: EXPLICIT_CLASS_ASSUMPTION
  additional_assumptions: ["compacidade de M"]
  requires_formalization: false
  note: >
    Incorporada a definicao da classe, NAO derivada. GAP-RH-012 aberto.
    Se um gate futuro obtiver fonte para variedades compactas, passa a
    SOURCE_CITED_RESULT e pode sair da definicao.

- id: GWB-002
  statement: "N_P(Lambda) = #{j | lambda_j < Lambda} esta bem definida e eh finita para cada Lambda finito."
  source: CORIASCO-DOLL-2020
  page: "p.1"
  equation_or_theorem: "eq. (1)"
  evidence_status: SOURCE_CITED_RESULT
  additional_assumptions: ["GWB-001"]
  requires_formalization: true
  note: "Convencao de desigualdade ESTRITA (<), fixada pela fonte. Ver SPECTRAL_MATCH_CONVENTIONS.md."

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
  additional_assumptions: ["e(x,x,Lambda) integravel na diagonal", "CASO ESCALAR"]
  requires_formalization: true
  note: >
    (3.1.11) eh ESCALAR. A versao fibrada com tr_E nao foi lida em fonte
    alguma - ver W_ELLIPTIC_SYSTEM_DEFERRED.md. Evidencia canonica desta
    identidade: a copia preservada em pdf/ivrii_2016_100years_weyl.pdf,
    sha256 9ca07737..., dado que nao foi possivel verificacao publica
    independente.

- id: GWB-005
  statement: "A assintota local eh uniforme em x."
  source: HORMANDER-1968
  page: "p.215"
  equation_or_theorem: "Teorema 5.1, eq. (5.3)"
  evidence_status: SOURCE_DIRECT
  additional_assumptions: ["a estimativa eh uniforme em COMPACTOS; M compacta torna isso uniformidade global"]
  requires_formalization: true
  note: >
    Esta eh a UNICA obrigacao sustentada por leitura direta do artigo
    original. Hormander 1968 eh citado aqui pelo resultado LOCAL, conforme
    a regra de citacao adotada em GAP-RH-013.

- id: GWB-006
  statement: "A integracao do termo principal produz C_P * Lambda^(d/m)."
  source: "HORMANDER-1968 (1.1) p.193 + homogeneidade de grau m do simbolo principal"
  page: "p.193"
  equation_or_theorem: "(1.1); comparar IVRII-2016 (3.1.3)"
  evidence_status: ELEMENTARY_COROLLARY
  additional_assumptions:
    - "p(x,.) homogeneo de grau m ==> vol{p < Lambda} = Lambda^(d/m) vol{p < 1}"
    - "x |-> vol(B_x) integravel sobre M compacta"
  requires_formalization: true

- id: GWB-007
  statement: "A integracao do erro preserva ordem inferior ao termo principal."
  source: "HORMANDER-1968 (5.3) + compacidade de M"
  page: "p.215"
  equation_or_theorem: "(5.3)"
  evidence_status: ELEMENTARY_COROLLARY
  additional_assumptions: ["vol(M) < infinito", "(d-1)/m < d/m"]
  requires_formalization: true

- id: GWB-008
  statement: "C_P > 0."
  source: "nenhuma fonte obtida afirma"
  page: null
  equation_or_theorem: null
  evidence_status: ELEMENTARY_COROLLARY_PENDING_FORMAL_ARGUMENT
  additional_assumptions:
    - "elipticidade + positividade ==> p(x,xi) > 0 para xi != 0"
    - "p(x,.) homogenea de grau m > 0 ==> B_x eh vizinhanca aberta nao vazia da origem"
    - "M compacta e x |-> vol(B_x) contınua positiva"
  requires_formalization: true
  note: >
    GAP-RH-014 aberto. Sem C_P > 0 a pertinencia a W-POWER FALHA, pois
    W-POWER exige constante positiva. Obrigacao critica.

- id: GWB-009
  statement: "N_P(Lambda)/Lambda^(d/m) -> C_P."
  source: "consequencia de GWB-002..008"
  page: null
  equation_or_theorem: null
  evidence_status: BRIDGE_DOCUMENTED
  additional_assumptions: ["todas as anteriores"]
  requires_formalization: true
  note: >
    Enunciado equivalente citado diretamente por CORIASCO-DOLL-2020 p.1
    (N(lambda) = gamma*lambda^(d/m) + O(lambda^((d-1)/m))) e por
    IVRII-2016 (3.1.1). Duas rotas independentes: pela ponte GWB-002..008,
    ou por citacao direta das duas fontes.
```

---

## Redução do requisito

Para `W-POWER` basta a **assintótica de um termo**. Ivrii, Example
3.1.1(iv): *"without any non-degeneracy assumption we arrive to one-term
asymptotics with the remainder estimate `O(λ^{(d−1+δ)/m})`"*.

Consequência: as condições de **micro-hiperbolicidade** e de **não
periodicidade** — exigidas para o resto agudo e o segundo termo — **não são
necessárias** para GWB-009. Isto simplifica materialmente as obrigações
GWB-006 e GWB-007: qualquer resto `o(Λ^{d/m})` basta.

## Resumo por estado

| Estado | Obrigações |
|---|---|
| `SOURCE_DIRECT` | GWB-005 |
| `SOURCE_CITED_RESULT` | GWB-002, GWB-003, GWB-004, (GWB-009 por citação) |
| `ELEMENTARY_COROLLARY` | GWB-006, GWB-007 |
| `ELEMENTARY_COROLLARY_PENDING` | GWB-008 |
| `EXPLICIT_CLASS_ASSUMPTION` | GWB-001 |
| `BRIDGE_DOCUMENTED` | GWB-009 (pela ponte) |

Nenhuma `UNRESOLVED` no caso escalar. A única `UNRESOLVED` do gate anterior
— tratamento de fibrados na etapa D — foi **removida por estreitamento da
classe**, não resolvida.

## Nenhuma prova executada

Este documento enumera obrigações. Nenhuma foi demonstrada, e nenhuma foi
formalizada em Lean.
