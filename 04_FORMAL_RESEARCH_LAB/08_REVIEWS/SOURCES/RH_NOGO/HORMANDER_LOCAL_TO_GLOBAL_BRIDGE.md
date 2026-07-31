# Ponte local → global — auditoria etapa por etapa

Objetivo: determinar se a lei global de contagem pode ser obtida a partir
do resultado local de Hörmander 1968, e com quais fontes. **Nada aqui é
demonstrado neste gate**; cada seta recebe um estado de sustentação.

Estados: `DIRECTLY_PROVED`, `CITED_STANDARD_RESULT`, `ELEMENTARY_COROLLARY`,
`REQUIRES_ADDITIONAL_SOURCE`, `UNRESOLVED`.

---

## A. Definição do projetor espectral `E_Λ`

```yaml
statement: "P eh uma realizacao auto-adjunta positiva; {E_lambda} eh sua resolucao espectral."
source: HORMANDER-1968
page: 193
theorem_or_equation: "Secao 1, paragrafo 3"
status: DIRECTLY_PROVED
additional_assumptions:
  - "positividade formal (Pu,u) >= c(u,u), c > 0"
  - "extensao de Friedrichs escolhida (NAO unicidade)"
```

Citação: *"by a classical theorem of Friedrichs it has at least one
self-adjoint extension P̄ with a positive lower bound c. Let `{E_λ}` be the
spectral resolution of such an extension."*

## B. Núcleo `e(x,y,Λ)`

```yaml
statement: "e(x,y,lambda) eh o nucleo de E_lambda, elemento de C-infinito(Omega x Omega)."
source: HORMANDER-1968
page: 193
theorem_or_equation: "Secao 1"
status: DIRECTLY_PROVED
additional_assumptions: []
```

Citação: *"let `e(x,y,λ)` be the kernel of `E_λ`. This is an element of
`C^∞(Ω × Ω)` called the spectral function of the self-adjoint extension P̄."*

## C. Identidade `N_P(Λ) = Tr(E_Λ)`

```yaml
statement: "N(lambda) = Tr(integral de 0 a lambda de dE(lambda))."
source: CORIASCO-DOLL-2020
page: "Secao 3 (Wave Trace)"
theorem_or_equation: "formula deslocada apos a definicao da medida espectral"
status: CITED_STANDARD_RESULT
additional_assumptions:
  - "resolvente compacto"
  - "base ortonormal de autofuncoes com 0 < lambda_1 <= lambda_2 <= ... -> +infinito"
  - "E_lambda de posto finito (equivalente a N(lambda) < infinito)"
note: >
  Os autores estabelecem a cadeia no proprio contexto SG:
  "By the compactness of the embedding of SG-Sobolev spaces, the resolvent
  (lambda-P)^(-1) is compact and hence there exists an orthonormal basis
  {psi_j} of L^2 consisting of eigenfunctions of P with eigenvalues
  lambda_j with 0 < lambda_1 <= lambda_2 <= ... -> +infinito."
  Para variedade COMPACTA o analogo eh teoria eliptica padrao
  (Rellich-Kondrachov), mas NAO foi lido em fonte obtida.
gap: GAP-RH-012 permanece parcialmente aberto
```

## D. Identidade `Tr(E_Λ) = ∫_M tr_E e(x,x,Λ) dx`

```yaml
statement: "N^-(lambda) = integral de e(x,x,lambda) dx."
source: IVRII-2016
page: "Secao 3.1.1, 'Rescaling technique'"
theorem_or_equation: "(3.1.11); variante com dois parametros em (3.1.12)"
status: CITED_STANDARD_RESULT
additional_assumptions:
  - "e(x,x,lambda) integravel na diagonal"
  - "para sistemas/fibrados, tr_E (traco fibra a fibra) - NAO explicitado em (3.1.11), que eh escalar"
```

Transcrição: `(3.1.11)  N⁻(λ) = ∫ e(x,x,λ) dx`.

## E. Assíntota local uniforme

```yaml
statement: "|e(x,x,lambda) - (2pi)^(-n) * integral_{p(x,xi)<lambda} d(xi)| <= C(1+|lambda|)^((n-1)/m), uniformemente em subconjuntos compactos de Omega."
source: HORMANDER-1968
page: 215
theorem_or_equation: "Teorema 5.1, eq.(5.3)"
status: DIRECTLY_PROVED
additional_assumptions:
  - "Omega variedade paracompacta; a estimativa eh uniforme em COMPACTOS"
```

**Observação decisiva:** se `M` é compacta, "uniformemente em subconjuntos
compactos de `M`" significa **uniformemente em `M`**. A uniformidade global
exigida pela etapa G é, portanto, gratuita — mas só sob compacidade.

## F. Integração do termo principal

```yaml
statement: "integral_M (2pi)^(-d) * integral_{p(x,xi)<Lambda} d(xi) dx = C_P * Lambda^(d/m)"
source: "consequencia da homogeneidade de grau m do simbolo principal"
page: "HORMANDER-1968 p.193 (p homogeneo de grau m); IVRII-2016 (3.1.3)"
theorem_or_equation: "(1.1) de Hormander; (3.1.3) de Ivrii"
status: ELEMENTARY_COROLLARY
additional_assumptions:
  - "p(x,.) homogeneo de grau m ==> vol{p < Lambda} = Lambda^(d/m) * vol{p < 1}"
  - "x |-> vol(B_x) mensuravel e integravel sobre M compacta"
```

Cálculo (não formalizado): `∫_{p(x,ξ)<Λ} dξ = Λ^{d/m} ∫_{B_x} dξ`, logo o
termo principal integrado é `Λ^{d/m}·(2π)^{−d}∫_M vol(B_x) dx`.

## G. Integração uniforme do erro

```yaml
statement: "integral_M O(Lambda^((d-1)/m)) dx = O(Lambda^((d-1)/m)) quando vol(M) < infinito e a constante C eh uniforme."
source: "combinacao de E (uniformidade em compactos) com M compacta"
page: "HORMANDER-1968 p.215"
theorem_or_equation: "(5.3)"
status: ELEMENTARY_COROLLARY
additional_assumptions:
  - "M compacta ==> vol(M) < infinito e a uniformidade em compactos eh uniformidade global"
  - "a ordem do resto eh preservada: (d-1)/m < d/m, logo o resto eh o(Lambda^(d/m))"
```

---

## O que NÃO é trivial — verificação exigida pelo gate

O gate proíbe chamar a passagem de trivial sem demonstrar cinco pontos.
Estado de cada um:

| Ponto | Estado | Onde |
|---|---|---|
| o projetor possui posto finito | `CITED_STANDARD_RESULT` (via resolvente compacto ⟹ espectro discreto) | etapa C; GAP-RH-012 parcialmente aberto |
| o kernel é integrável na diagonal | `CITED_STANDARD_RESULT` — `e ∈ C^∞(Ω×Ω)` (Hörmander p.193) e `M` compacta ⟹ integrável | etapas B + D |
| a estimativa é uniforme em `x` | `DIRECTLY_PROVED` sob compacidade | etapa E |
| o fibrado/sistema é tratado corretamente | **`UNRESOLVED`** — (3.1.11) de Ivrii é escalar; para sistemas seria preciso `tr_E e(x,x,λ)`, e a constante correta é a de (3.1.3) com `n(x,ξ)` | etapa D; GAP-RH-009 |
| o erro integrado preserva a ordem | `ELEMENTARY_COROLLARY` | etapa G |

## Veredito

A ponte está **documentada** no caso **escalar sobre variedade compacta**:
cinco das sete etapas têm fonte (`DIRECTLY_PROVED` ou
`CITED_STANDARD_RESULT`), duas são corolários elementares explicitados, e a
uniformidade global decorre da compacidade.

Permanece `UNRESOLVED` o tratamento de **fibrados/sistemas** na etapa D, e
`GAP-RH-012` (discretude) está sustentado apenas por analogia com o
argumento SG de Coriasco–Doll, não por leitura de uma fonte que o enuncie
para variedades compactas.

Nenhuma etapa foi formalizada. `ASYM-NOGO-001` não foi aplicado.
