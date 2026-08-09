# Matriz de resultados conhecidos — BSD-HYP-MATRIX-001

Produto desta frente: particionar a literatura sobre BSD por hipótese
exata, curva/família, posto analítico e primos excluídos — **sem** unir
teoremas de hipóteses distintas num enunciado só, e sem tratar a união dos
casos cobertos como cobertura universal da conjectura (`stop_condition`
desta frente; ver `REVIEWS/AUDIT_REPORT.md` para a discussão explícita de
por que o documento legado violou exatamente isso).

Legenda de status de fonte: **V** = verificado nesta sessão (citação
recuperável por WebSearch/WebFetch, ver `REVIEWS/AUDIT_REPORT.md`).
**A** = aproximado (herdado do documento legado ou de memória de treino,
sem confirmação primária nesta sessão).

## Regra de leitura desta tabela

Cada linha é um teorema **independente**, com sua **própria** hipótese.
**Nenhuma linha pode ser combinada com outra para formar um enunciado
"E genérica satisfaz BSD porque a linha X OU a linha Y se aplica"** sem
primeiro provar que toda curva cai em pelo menos uma hipótese listada
(exaustividade) — o que nenhuma fonte aqui afirma. Ver `ASSUMPTIONS.md`.

| # | Teorema / resultado | Autores, publicação | Curva / família | Posto analítico coberto | Hipótese exata (resumida) | Primos `p` excluídos/exigidos | Conclusão exata | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | Gross–Zagier | Gross, Zagier, *Heegner points and derivatives of L-series*, Invent. Math. 84 (1986), 225–320 | `E/Q` modular (= toda `E/Q`, por BCDT 2001) | `rank_an = 1` (fórmula de derivada) | `L(E,1)=0`, `L'(E,1)≠0`; hipótese de Heegner sobre um `K` quadrático imaginário auxiliar | não fixados nesta sessão | Ponto de Heegner tem altura não nula ⇒ existe ponto racional de ordem infinita | V |
| 2 | Kolyvagin (finitude de Ш, igualdade de postos) | Kolyvagin, *Finiteness of E(Q) and Ш(E,Q) for a subclass of Weil curves*, Izv. Akad. Nauk SSSR 52(3) (1988), 523–541; *Euler systems*, Grothendieck Festschrift II (1990) | `E/Q` modular | `rank_an ∈ {0,1}` | `L(E,1)≠0` OU (`L(E,1)=0` e `L'(E,1)≠0`) | não fixados nesta sessão | `rank_alg = rank_an` e `Ш(E)` finito | V |
| 3 | Coates–Wiles | Coates, Wiles, *On the conjecture of Birch and Swinnerton-Dyer*, Invent. Math. 39(3) (1977), 223–251 | `E/Q` com CM por corpo quadrático imaginário de **número de classe 1** | implícito `rank_an = 0` | `L(E,1) ≠ 0` | não fixados nesta sessão | `E(Q)` finito (precursor histórico da parte fraca de BSD em rank 0) | V |
| 4 | Rubin — Iwasawa Main Conjecture (corpos quadráticos imaginários) | Rubin, *The "main conjectures" of Iwasawa theory for imaginary quadratic fields*, Invent. Math. 103 (1991), 25–68 | `E/Q` (ou sobre corpo quadrático imaginário) com **CM** | não restrito a 0/1 pelo IMC em si (ver ressalva abaixo) | CM por corpo quadrático imaginário; Main Conjecture via sistema de Euler de unidades elípticas | condições técnicas por primo (ordinário/supersingular tratados em artigos correlatos de Rubin) não fixadas nesta sessão | Igualdade de ideais característicos (Main Conjecture); combinado com fórmula de Gross–Zagier dá parte-`p` de BSD para CM | V (existência/venue); **A** (escopo exato "qualquer posto" não confirmado linha a linha contra o artigo primário) |
| 5 | Skinner–Urban — Iwasawa Main Conjectures for GL2 | Skinner, Urban, *The Iwasawa Main Conjectures for GL2*, Invent. Math. 195 (2014), 1–277 | `E/Q` (via forma modular associada), ordinária em `p` | não é diretamente "posto"; entra como insumo para BSD via Selmer/Kato | `p` ímpar, boa redução ordinária, representação mod `p` **irredutível**, condições adicionais (H1)-(H4) do documento legado — **lista exata não confirmada nesta sessão** | `p` ímpar; demais exclusões não fixadas nesta sessão | Main Conjecture ordinária para GL2 (Kato) — insumo para BSD, não BSD per se | V (existência/venue/escopo geral); **A** (hipóteses H1–H4 exatas) |
| 6 | Kolyvagin's conjecture (indivisibilidade), caso boa redução | W. Zhang | `E/Q` | `rank_an = 1` | boa redução em `p` | `p` de boa redução | Parte-`p` da fórmula BSD em rank analítico 1 | **A** (citação exata do artigo de W. Zhang não recuperada nesta sessão — apenas mencionado em resultados de busca de terceiros) |
| 7 | Kolyvagin's conjecture (indivisibilidade), caso multiplicativo | Skinner, Zhang, *Indivisibility of Heegner points in the multiplicative case*, arXiv:1407.1099 (2014) | `E/Q`, `p ≥ 5` | `rank_an = 1` | redução multiplicativa em `p` | `p ≥ 5`, multiplicativa em `p` | Parte-`p` da fórmula BSD em rank analítico 1, caso multiplicativo | V |
| 8 | Burungale–Castella–Skinner (base change), "BCS" | Burungale, Castella, Skinner, *Base Change and Iwasawa Main Conjectures for GL2*, IMRN 2025, artigo rnaf082 (aceito/publicado 2025 — legado citava "2024") | `E/Q`, condutor `N` | insumo (Main Conjecture), não posto diretamente | `p` ímpar, boa redução ordinária, `E[p]` **irredutível**; existe `K` quadrático imaginário com todo primo dividindo `Np` split | `p` ímpar; exclusão exata adicional não fixada nesta sessão | Main Conjecture cíclotômica/anticiclotômica sobre `Q` e `K`, sem a hipótese de ramificação de trabalhos anteriores | V (existência/venue/hipóteses gerais); **A** (correspondência exata com "evita H4" do documento legado) |
| 9 | Burungale–Skinner–Tian–Wan, "BSTW" | Burungale, Skinner, Tian, Wan, *Zeta elements for elliptic curves and applications*, arXiv:2409.01350 (2024) | `E/Q` **semiestável**, não-CM incluído | `rank_an ∈ {0,1}` | `p` primo **supersingular**, redução semiestável em todo primo | `p` supersingular (Kobayashi 2002); exclusão exata de primos pequenos não fixada nesta sessão | Main Conjecture de Kobayashi para primos supersingulares; parte-`p` de BSD em rank 0/1; primeiras famílias infinitas não-CM com BSD completa provada (combinando com outros primos) | V |
| 10 | Castella–Grossi–Lee–Skinner, primos de Eisenstein | Castella, Grossi, Lee, Skinner, *On the anticyclotomic Iwasawa theory of rational elliptic curves at Eisenstein primes*, Invent. Math. 227(2) (2022), 517–580 | `E/Q` | insumo (Main Conjecture) | `p` de **Eisenstein** (representação mod `p` redutível) | `p` de Eisenstein — regime **excludente** com a hipótese "irredutível" das linhas 5/8 | Main Conjecture anticiclotômica no caso Eisenstein | V |
| 11 | Castella–Grossi–Skinner, "CGS" | Castella, Grossi, Skinner, *Mazur's main conjecture at Eisenstein primes*, Math. Ann. 393(2) (2025), 2451–2506 (legado citava "2023") | `E/Q` | `rank_an ∈ {0,1}` | `p` de Eisenstein | `p` de Eisenstein | Parte-`p` da fórmula BSD forte para rank analítico 0 ou 1, caso Eisenstein | V |
| 12 | Bhargava–Skinner–Zhang, resultado de **densidade** | Bhargava, Skinner, Zhang, *A majority of elliptic curves over Q satisfy the Birch and Swinnerton-Dyer conjecture*, arXiv:1407.1826 (2014) | `E/Q` ordenadas por altura (família estatística, **não** por hipótese individual) | ≥ 66.48% têm a parte de posto de BSD verificada; ≥ 83.75% têm `rank_an ≤ 1` | nenhuma — é um enunciado de **densidade no limite de altura**, não uma condição verificável em uma curva dada isoladamente | não aplicável (estrutura diferente das demais linhas) | Proporção positiva (maioria) de curvas satisfaz BSD; **não** identifica quais curvas individuais fora dessa maioria estão ou não cobertas | V |
| 13 | Bhargava–Shankar, posto médio | Bhargava, Shankar — resultados de posto médio / proporção positiva em rank 0 (citado via Wikipedia nesta sessão, não confirmado contra arXiv primário) | `E/Q` ordenadas por altura | proporção positiva com `rank_an = 0` | estatística, não hipótese por curva | não aplicável | Proporção positiva de curvas com posto 0 satisfazendo BSD | **A** (citação primária não recuperada nesta sessão, apenas menção secundária) |

## Nota crítica sobre as linhas 12–13 (densidade ≠ partição por hipótese)

As linhas 12 e 13 **não são compatíveis, estruturalmente, com o resto da
tabela**: as linhas 1–11 são teoremas condicionais — "se `E` satisfaz a
hipótese `H_i`, então conclusão `C_i`" — verificáveis curva a curva. As
linhas 12–13 são afirmações assintóticas sobre uma família ordenada por
altura; **não dizem, para uma curva `E` fixa e arbitrária, se `E` está ou
não coberta**. Somar "66% (linha 12) + X% (linhas 1–11 em termos de
frequência)" para produzir um número de "cobertura total" é exatamente o
erro que o documento legado (`ANALISE_CRITICA_BSD.md`) cometeu ao computar
`0.99 × 100% + 0.01 × 95% = 99.95%` — uma aritmética que mistura contagem
de casos condicionais com densidade assintótica e a apresenta como
probabilidade de cobertura de BSD. Esta matriz **recusa-se a repetir esse
cálculo**. Ver `REVIEWS/AUDIT_REPORT.md`.

## O que a tabela deliberadamente NÃO afirma

- Não afirma que as hipóteses das linhas 1–11 são exaustivas sobre o
  conjunto de todas as `E/Q` (não há teorema listado aqui, nem em nenhuma
  fonte encontrada nesta sessão, que prove isso).
- Não afirma que "rank ≥ 2, não-CM, sem hipótese especial" está coberto —
  esse caso permanece **aberto** em geral (consistente com
  `GAP_REGISTER.yaml`, `BSD-GAP-001`).
- Não afirma que a finitude de `Ш(E)` está estabelecida fora dos casos
  rank 0/1 (Kolyvagin) e CM (Rubin) — `BSD-GAP-002`.
- Não afirma que, para uma curva `E` fixa de posto analítico 0 ou 1, a
  fórmula BSD forte (com todos os fatores — `Ш`, `Ω`, `Reg`, `c_p`, torção)
  está provada **simultaneamente para todo primo `p`** — cada linha 5–11
  cobre a parte-`p` para uma classe de primos (ordinário-irredutível,
  supersingular, Eisenstein); combinar essas partes-`p` em uma igualdade
  integral exige que as classes de primos cubram **todo** `p`, o que não
  foi verificado aqui (`GAP_REGISTER.yaml`, `BSD-GAP-006`).
