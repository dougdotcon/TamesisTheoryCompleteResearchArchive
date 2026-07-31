# Auditoria de fontes adicionais — RH_NOGO_ADDITIONAL_SOURCE_RETRIEVAL

Sessão de 2026-07-31. Proveniência completa em `SOURCE_MANIFEST.yaml`.

## Fontes obtidas nesta sessão

| Fonte | Acesso | Estado |
|---|---|---|
| Ivrii, *100 years of Weyl's law*, Bull. Math. Sci. 6 (2016) 379–452; arXiv:1608.03963 | **acesso público** (arXiv) | `RETRIEVED`, 90 pp., `PARTIALLY_AUDITED` |
| Coriasco–Doll, *Weyl Law on Asymptotically Euclidean Manifolds*, Ann. Henri Poincaré; arXiv:1912.13402 | **acesso público** (arXiv) | `RETRIEVED`, 26 pp., `PARTIALLY_AUDITED` |

Leitura integral: Ivrii §1.1 e §3.1.1; Coriasco–Doll Introdução e §3.

## Fontes prioritárias NÃO obtidas

| Fonte | Sondagem | Estado |
|---|---|---|
| Safarov–Vassiliev, AMS Transl. Math. Monogr. 155 | página de catálogo AMS respondeu HTTP 200 (`text/html`) | `RETRIEVAL_FAILED` — só catálogo |
| Shubin, *Pseudodifferential Operators and Spectral Theory*, 2ª ed. | página Springer respondeu HTTP 200 (`text/html`) | `RETRIEVAL_FAILED` — só catálogo |
| Ivrii, *Microlocal Analysis and Precise Spectral Asymptotics* (`[Ivr4]`) | — | `RETRIEVAL_FAILED` |

São monografias comerciais. **Nenhuma tentativa foi feita de obter cópias
por meios que violem direitos de acesso**, conforme a instrução do gate.
Consequência: as **provas** da lei global permanecem em textos não lidos;
o que este laboratório possui são **enunciados** em fontes revisadas por
pares que citam essas monografias (ou citam Hörmander 1968).

## Achado principal

Duas fontes independentes, revisadas por pares, enunciam a lei global com
hipóteses precisas:

- **Coriasco–Doll**, p. 1: *"positive elliptic self-adjoint classical
  pseudodifferential operator of order `m > 0` on a compact manifold"*,
  `N(λ) = #{j : λ_j < λ}`, `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`.
- **Ivrii**, (3.1.1)–(3.1.3): `N(0,λ) = κ₀λ^{d/m} + O(λ^{(d−1)/m})` com
  `κ₀ = (2π)^{−d}∬ n(x,ξ)dxdξ`, `n(x,ξ)` = nº de autovalores de `A⁰(x,ξ)`
  em `(0,1)` — **forma correta para sistemas**.

E Ivrii (3.1.11) escreve explicitamente a identidade local→global
`N⁻(λ) = ∫ e(x,x,λ)dx`.

## Achado secundário, de valor epistemológico

**A atribuição corrente é imprecisa.** Coriasco–Doll escrevem *"Hörmander
[15] proved … the Weyl law `N(λ) = γλ^{d/m} + O(λ^{(d−1)/m})`"* com
`[15] = L. Hörmander, The spectral function of an elliptic operator, Acta
Math. 121 (1968), 193–218` — o artigo auditado no gate anterior, que
**não enuncia `N(λ)`**.

A atribuição é matematicamente defensável (a lei global segue por
integração da local sobre variedade compacta) e **bibliograficamente
imprecisa** (o passo não está escrito no artigo).

Regra adotada, conforme a instrução 1 do gate:

```text
Hormander 1968 e citado pelo resultado LOCAL.
A lei GLOBAL e citada por Coriasco-Doll / Ivrii, ou derivada
explicitamente pela ponte documentada.
```

Nenhuma reclassificação de Hörmander 1968 como fonte global direta foi
feita, porque nenhuma passagem literal a sustenta.

## Observação que reduz o requisito

Ivrii, Example 3.1.1(iv): *"Furthermore, without any non-degeneracy
assumption we arrive to **one-term asymptotics** with the remainder estimate
`O(λ^{(d−1+δ)/m})`."*

Para `W-POWER` basta a assintótica de **um termo** — o resto pior é
irrelevante para `N/Λ^α → C`. Portanto as condições de
micro-hiperbolicidade e não periodicidade, exigidas para o resto agudo e
para o segundo termo, **não são necessárias** para a inclusão
`W-ELLIPTIC ⊆ W-POWER`.

## Estados de leitura consolidados

```yaml
CONTENT_AUDITED:
  - RIEMANN-1859 (traducao Wilkins; original alemao nao obtido)
PARTIALLY_AUDITED:
  - VONMANGOLDT-1905   # pp. 1, 2, 18, 19
  - HORMANDER-1968     # Secoes 1 e 5
  - BOMBIERI-CLAY      # Secao I
  - IVRII-2016         # 1.1 e 3.1.1
  - CORIASCO-DOLL-2020 # Introducao e Secao 3
RETRIEVAL_FAILED:
  - SAFAROV-VASSILIEV
  - SHUBIN
  - IVRII-MONOGRAPH
  - RIEMANN-1859-ORIGINAL
```
