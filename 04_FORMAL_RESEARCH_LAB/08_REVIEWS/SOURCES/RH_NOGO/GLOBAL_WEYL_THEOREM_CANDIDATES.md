# Candidatos a teorema de Weyl global — matriz

Fontes obtidas nesta sessão em `pdf/`, com `sha256` no
`SOURCE_MANIFEST.yaml`.

---

## Candidato 1 — Coriasco–Doll 2020 (enunciado citado)

```yaml
source: "S. Coriasco, M. Doll, 'Weyl Law on Asymptotically Euclidean Manifolds', Ann. Henri Poincaré 22 (2021); arXiv:1912.13402"
retrieval_status: RETRIEVED
file: "pdf/coriasco_doll_2020_weyl_ae.pdf"
sha256: "501d9bae1f898f7d450373f7755016c22e06adab4b4570c11e19b596c8a7f51b"
pages: 26
content_audited: PARTIALLY_AUDITED   # Introducao e Secao 3 lidas integralmente
theorem_number: "enunciado da Introducao, p.1 (NAO e teorema proprio dos autores)"
pages_cited: "p.1, linhas 38-41; definicao de N em eq.(1), p.1; identidade de traco na Secao 3"
operator_type: "operador pseudodiferencial classico"
differential_or_pseudodifferential: PSEUDODIFFERENTIAL_CLASSICAL
scalar_or_system: "nao declarado (escalar por omissao)"
base_space: "compact manifold"
boundary: "nao declarado"
order: "m > 0 (real; sem restricao de paridade)"
ellipticity: "eliptico"
positivity: "positive"
self_adjointness: "self-adjoint (uma realizacao; NAO 'essentially self-adjoint')"
extension_or_domain: "nao especificado no enunciado citado"
discrete_spectrum: "pressuposto pelo enunciado; provado pelos autores apenas no proprio contexto SG (resolvente compacto por mergulho compacto de Sobolev)"
counting_function_defined: "SIM - eq.(1): N(lambda) = #{j : lambda_j < lambda}"
asymptotic: "N(lambda) = gamma * lambda^(d/m) + O(lambda^((d-1)/m)), lambda -> +infinito"
leading_constant: "gamma - NAO explicitada para o caso compacto"
remainder: "O(lambda^((d-1)/m)); os autores observam que e otimo em geral (esfera)"
direct_match_to_W_ELLIPTIC: "SIM - e a fonte da formulacao de W-ELLIPTIC v2"
status: CITED_STANDARD_RESULT
limitations: >
  Os autores CITAM o resultado, nao o provam: a referencia dada e
  [15] = Hormander, Acta Math. 121 (1968), 193-218 - exatamente o artigo
  auditado no gate anterior, que NAO enuncia N(lambda). Ver a secao
  "Discrepancia de atribuicao" abaixo.
```

Transcrição literal (p. 1):

> "Hörmander [15] proved, for a positive elliptic self-adjoint classical
> pseudodifferential operator of order `m > 0` on a compact manifold, the
> Weyl law
> `N(λ) = γ · λ^{d/m} + O(λ^{(d−1)/m})`, `λ → +∞`."

e (eq. 1): `N(λ) = #{j : λ_j < λ}`.

---

## Candidato 2 — Ivrii 2016, survey (enunciado citado)

```yaml
source: "V. Ivrii, '100 years of Weyl's law', Bull. Math. Sci. 6 (2016), 379-452; arXiv:1608.03963"
retrieval_status: RETRIEVED
file: "pdf/ivrii_2016_100years_weyl.pdf"
sha256: "9ca077375f21487c66c644ca6fa847360b63ffd051e24790181f4af2459bbf3f"
pages: 90
content_audited: PARTIALLY_AUDITED   # 1.1 e 3.1.1 lidas integralmente
theorem_number: "Example 3.1.1, eq.(3.1.1)-(3.1.3); tambem (3.1.11)-(3.1.12)"
pages_cited: "Secao 3.1.1 (p.32-33 da numeracao interna); Secao 1.1"
operator_type: "operador auto-adjunto A eliptico com problema de contorno eliptico (A,B)"
differential_or_pseudodifferential: "ambos (o survey e semiclassico/microlocal)"
scalar_or_system: "SISTEMAS TRATADOS - a constante usa n(x,xi) = numero de autovalores do simbolo principal"
base_space: "X com bordo (D(A) = {u : Bu|dX = 0})"
boundary: "SIM - o exemplo e formulado com condicao de contorno"
order: "m = m_A, ordem de A"
ellipticity: "A eliptico e o problema (A,B) eliptico"
positivity: "no item (ii): A_B positivo definido"
self_adjointness: "A auto-adjunto com dominio D(A)"
discrete_spectrum: "pressuposto"
counting_function_defined: "SIM - N(0,lambda), numero de autovalores de A em [0,lambda)"
asymptotic: "(3.1.1) N(0,lambda) = kappa_0 * lambda^(d/m) + O(lambda^((d-1)/m))"
leading_constant: "(3.1.3) kappa_0 = (2*pi)^(-d) * int-int n(x,xi) dx d(xi), n(x,xi) = numero de autovalores de A^0(x,xi) em (0,1)"
remainder: "O(lambda^((d-1)/m)); dois termos sob condicao de nao periodicidade"
direct_match_to_W_ELLIPTIC: "PARCIAL - formulado com bordo; cobre sistemas"
status: CITED_STANDARD_RESULT
limitations: >
  As provas sao deferidas a [Ivr4] = monografia de Ivrii, NAO obtida.
  O enunciado exige condicoes de micro-hiperbolicidade para o resto agudo.
```

Duas observações **importantes** do mesmo texto:

- item (iv), p. 33: *"For scalar operators, one can replace
  microhyperbolicity by a weaker non-degeneracy assumption. Furthermore,
  **without any non-degeneracy assumption we arrive to one-term asymptotics
  with the remainder estimate `O(λ^{(d−1+δ)/m})`**."*
  → Para W-POWER **basta a assintótica de um termo**, e esta vale sem
  hipóteses de não degenerescência. O resto pior é irrelevante para
  `N/Λ^α → C`.
- eq. (3.1.11): `N⁻(λ) = ∫ e(x,x,λ) dx` — a identidade local→global,
  escrita explicitamente.

---

## Candidatos 3–5 — monografias: NÃO OBTIDAS

```yaml
- source: "Yu. Safarov, D. Vassiliev, 'The Asymptotic Distribution of Eigenvalues of Partial Differential Operators', AMS, Transl. Math. Monogr. 155"
  retrieval_status: LISTING_CONFIRMED       # pagina de catalogo AMS: HTTP 200, text/html
  content_audited: false
  note: "monografia comercial; texto integral nao obtenivel por acesso publico legitimo nesta sessao"

- source: "M. A. Shubin, 'Pseudodifferential Operators and Spectral Theory', 2a ed., Springer"
  retrieval_status: LISTING_CONFIRMED       # link.springer.com/book/10.1007/978-3-642-56579-3: HTTP 200, text/html
  content_audited: false
  note: "monografia comercial; idem"

- source: "V. Ivrii, 'Microlocal Analysis and Precise Spectral Asymptotics' ([Ivr4] no survey)"
  retrieval_status: LISTING_CONFIRMED
  content_audited: false
  note: "contem as provas citadas pelo survey; nao obtida"
```

Nenhuma dessas foi lida. Nenhuma pode ser citada como contendo o enunciado
até ser auditada. Conforme a instrução do gate, não houve tentativa de
obter cópias por meios que violem direitos de acesso.

---

## Discrepância de atribuição — achado desta sessão

O gate anterior estabeleceu, por leitura do original, que **Hörmander 1968
não enuncia `N(λ)`**: prova a assíntota **local** `e(x,x,λ)` (eq. 5.3) e o
texto integral não contém "number of eigenvalues", "counting function" nem
`N(λ)`.

Esta sessão constata que **a literatura moderna atribui a lei global àquele
artigo**: Coriasco–Doll escrevem literalmente *"Hörmander [15] proved …
the Weyl law `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`"* com `[15]` sendo
precisamente Acta Math. 121 (1968), 193–218.

Leitura correta da discrepância:

1. A atribuição é **padrão na área** e matematicamente **defensável**: a lei
   global segue por integração da lei local sobre variedade compacta
   (`HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md`).
2. Mas é **bibliograficamente imprecisa**: o passo de integração não está
   escrito no artigo de 1968.
3. Portanto, **este laboratório não citará Hörmander 1968 pela lei global**.
   Citará: Hörmander 1968 pela lei **local**, e a ponte explicitamente,
   com as fontes de cada etapa.

Este é exatamente o tipo de imprecisão que a auditoria existia para
capturar antes que virasse premissa de prova.
