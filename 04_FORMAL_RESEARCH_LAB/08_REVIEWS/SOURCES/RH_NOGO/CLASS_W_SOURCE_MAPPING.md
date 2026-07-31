# Classe W — mapeamento hipótese a hipótese contra fonte primária

Fonte candidata única auditada para o pilar espectral:
**HORMANDER-1968** (`HORMANDER_1968_AUDIT.md`).
Numeração das hipóteses conforme `OPERATOR_CLASS.md`.

Estados permitidos: `SUPPORTED_DIRECTLY`, `SUPPORTED_AFTER_STANDARD_COROLLARY`,
`PARTIALLY_SUPPORTED`, `NOT_SUPPORTED`, `AMBIGUOUS`.

---

| hypothesis | exact_definition | primary_source | page | theorem_or_equation | directly_supported | requires_secondary_source | requires_additional_theorem | status | notes |
|---|---|---|---|---|---|---|---|---|---|
| **W1** `operator_type` / base | `M` variedade riemanniana suave, compacta, sem bordo, `dim M = d < ∞` | HORMANDER-1968 | 193, 196, 214 | Seção 1; Seção 5 | parcialmente | não | não | `PARTIALLY_SUPPORTED` | O artigo supõe `Ω` **paracompacta**, não compacta. Compacidade é usada como *conveniência de prova* („For the sake of simplicity we assume that Ω is compact“, p. 196; „it suffices to prove the theorem when Ω is compact, for example a torus“, p. 214). Ausência de bordo: implícita, nenhuma condição de bordo é formulada. A Classe W é mais restrita que o artigo neste ponto, o que é seguro para o enunciado local — mas a compacidade torna-se **essencial** para W8. |
| **W2** fibrado vetorial | `E → M` fibrado hermitiano suave de posto finito; caso escalar incluído | HORMANDER-1968 | 216 | observação final da Seção 5 | **não** | **sim** | **sim** | `NOT_SUPPORTED` (caso geral) / `PARTIALLY_SUPPORTED` (autovalores distintos) | Literal: „Our methods can be applied with no essential modification in the case of systems for which the eigenvalues of `p(x,ξ)` are **distinct** … However for systems with **multiple eigenvalues** we have **no information** beyond the results of Agmon–Kannai [1] and Hörmander [8].“ O corpo do artigo trabalha em `L²(Ω)` escalar. |
| **W3** ordem inteira fixa `m ≥ 1` | operador diferencial clássico de ordem `m` fixa, coeficientes suaves | HORMANDER-1968 | 193 | Seção 1 | sim, com ressalva | não | não | `PARTIALLY_SUPPORTED` | Ordem fixa: sustentada („principal symbol … real homogeneous polynomial of degree `m`“). **Ressalva não registrada na Classe W:** elipticidade + positividade formal com símbolo principal real forçam `m` **par** para `d ≥ 2` (pois `p(x,−ξ) = (−1)^m p(x,ξ)` e `p > 0` fora de zero). `OPERATOR_CLASS.md` admite `m ≥ 1` qualquer — a classe declarada é, nesse ponto, **vazia para `m` ímpar**, não errada, mas mal formulada. |
| **W4** elipticidade | símbolo principal invertível fora da seção nula | HORMANDER-1968 | 193 | Seção 1, eq. (1.1) | sim | não | não | `SUPPORTED_DIRECTLY` | O artigo usa „elliptic differential operator“ na acepção padrão; a finitude de `∫_{B_x} dξ` em (1.1) com `B_x = {ξ ; p(x,ξ) < 1}` depende dela. |
| **W5** auto-adjunção | `P` essencialmente auto-adjunto em `L²`, extensão única `P̄` | HORMANDER-1968 | 193 | Seção 1 | **não** | sim | sim | `AMBIGUOUS` / divergente | Literal: „by a classical theorem of Friedrichs it has **at least one** self-adjoint extension P̄“. O artigo trabalha com **uma extensão escolhida** (Friedrichs), não com unicidade. A Classe W exige essencial auto-adjunção — hipótese **mais forte** e não a do artigo. A escolha da extensão afeta o espectro; a Classe W precisa ser reformulada ou justificada. |
| **W6** positividade | `⟨Pu,u⟩ > 0` para `u ≠ 0` | HORMANDER-1968 | 193 | Seção 1 | sim, e mais forte | não | não | `SUPPORTED_DIRECTLY` | Literal: „formally positive, that is, `(Pu,u) ≥ c(u,u)`, `u ∈ C_0^∞(Ω)`, where `c > 0`“ — cota inferior positiva uniforme, mais forte que positividade estrita pontual. |
| **W7** espectro discreto, multiplicidade finita | autovalores discretos contados com multiplicidade | HORMANDER-1968 | — | — | **não** | **sim** | **sim** | `NOT_SUPPORTED` | O artigo não prova nem enuncia discretude do espectro. Ele pressupõe uma resolução espectral `{E_λ}` genérica. Em variedade compacta a discretude segue de elipticidade (resolvente compacto), mas **esse teorema não está aqui**. |
| **W8** lei de Weyl global `N_P(Λ) ~ C_P Λ^{d/m}` | contagem global dos autovalores | HORMANDER-1968 | 193, 215 | Teorema 1.1; Teorema 5.1, eq. (5.3) | **não** | **sim** | **sim** | `NOT_SUPPORTED` | **Achado central.** O artigo prova a assíntota **local** da função espectral na diagonal: `\|e(x,x,λ) − (2π)^{−n}∫_{p(x,ξ)<λ}dξ\| ≤ C(1+\|λ\|)^{(n−1)/m}` (5.3), uniforme em compactos. Busca no texto integral por „number of eigenvalues“, „counting function“, `N(λ)`: **nenhuma ocorrência**. A contagem global exige `N_P(Λ) = ∫_Ω e(x,x,Λ) dx` — passo que precisa de compacidade e de uniformidade global, e **não está escrito neste artigo**. |

---

## Síntese

| Estado | Hipóteses |
|---|---|
| `SUPPORTED_DIRECTLY` | W4, W6 |
| `PARTIALLY_SUPPORTED` | W1, W2 (só autovalores distintos), W3 (paridade de `m` não declarada) |
| `AMBIGUOUS` | W5 |
| `NOT_SUPPORTED` | W7, W8 |

**Duas de oito hipóteses estão diretamente sustentadas.** As duas mais
decisivas para o no-go — W7 (discretude) e **W8 (a lei de contagem global,
que é literalmente a hipótese B de `ASYM-NOGO-001`)** — não estão.

## O que NÃO foi feito

Nenhuma reformulação da Classe W foi executada neste gate. As divergências
acima são **registradas**, não corrigidas: alterar `OPERATOR_CLASS.md`
exigiria decidir entre estreitar a classe (para o que Hörmander sustenta)
ou buscar fonte adicional (para o que a classe declara). Essa decisão
pertence ao próximo gate. Ver `UNRESOLVED_SOURCE_QUESTIONS.md` e
`GAP_REGISTER.yaml`.
