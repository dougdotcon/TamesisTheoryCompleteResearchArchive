# HÖRMANDER 1968 — auditoria de fonte primária

Fonte: L. Hörmander, *The spectral function of an elliptic operator*,
Acta Mathematica **121** (1968), 193–218. DOI 10.1007/BF02391913.
Cópia: `pdf/hormander_1968_acta121.pdf`, sha256 `a633994c…`.
Estado de leitura: `PARTIALLY_AUDITED` — Seção 1 (pp. 193–196) e Seção 5
(pp. 214–216) lidas integralmente; Seções 2–4 e 6 percorridas por busca
dirigida. As 17 perguntas do gate são sobre **hipóteses e enunciados** e
estão todas respondidas pelas seções lidas; a verificação da prova não faz
parte deste mandato.

Citações abaixo transcrevem o texto da cópia (a camada de texto tem ruído
tipográfico de digitalização: `HSrmander`, `2` no lugar de `λ`, `Gs` por
`Gårding`; as fórmulas foram conferidas contra o layout).

## Respostas literais às 17 perguntas do gate

### 1. Qual classe de operadores é considerada?

Seção 1, p. 193:

> „Let Ω be a paracompact C^∞ manifold and let P be an elliptic differential
> operator in Ω with C^∞ coefficients.“

Seção 5, p. 214, repete: „a positive self-adjoint extension P̄ of an elliptic
differential operator with C^∞ coefficients on a paracompact manifold Ω of
dimension n“.

### 2. O operador é diferencial ou pseudodiferencial?

**Ambos, em papéis diferentes.** O título e o abstract falam de „an
arbitrary elliptic (pseudo-)differential operator“. A Seção 4 trata de um
operador **pseudodiferencial elíptico de ordem 1** sobre variedade compacta;
a Seção 5 transporta o resultado para **operadores diferenciais de ordem m**
via `A = P̄^{1/m}`, que é pseudodiferencial (Seeley).

### 3. Qual é sua ordem?

`m`, fixa. p. 193: „Let p be the principal symbol of P, which is a real
homogeneous polynomial of degree m on the cotangent bundle T*(Ω).“

**Observação crítica:** o símbolo principal é dito **polinômio homogêneo
real de grau m**. Combinado com elipticidade e positividade formal, isto
força `p(x,ξ) > 0` para `ξ ≠ 0`, o que por sua vez força **`m` par** (para
`n ≥ 2`, pois `p(x,−ξ) = (−1)^m p(x,ξ)`). A Classe W declarada no
laboratório admite `m ≥ 1` inteiro qualquer — ver
`CLASS_W_SOURCE_MAPPING.md`, linha W3.

### 4. Qual é a hipótese de elipticidade?

O artigo diz „elliptic differential operator“ sem repetir a definição; usa-a
na forma padrão (símbolo principal invertível fora da seção nula), o que na
p. 193 se manifesta pela exigência implícita de que
`B_x = {ξ ∈ T*_x ; p(x,ξ) < 1}` seja um conjunto de medida finita em (1.1).

### 5. Há auto-adjunção?

**Sim, mas não por unicidade.** p. 193:

> „the operator P with domain C_0^∞(Ω) is symmetric, and by a classical
> theorem of Friedrichs it has **at least one** self-adjoint extension P̄
> with a positive lower bound c.“

O artigo trabalha com **uma extensão auto-adjunta escolhida**, não com
auto-adjunção essencial. `{E_λ}` é a resolução espectral *dessa* extensão e
`e(x,y,λ)` é o núcleo de `E_λ`, „the spectral function of the self-adjoint
extension P̄“.

Isto **não coincide** com a hipótese W5 do laboratório, que exige
essencial auto-adjunção (extensão única).

### 6. Há positividade ou apenas semilimitação?

Positividade formal com cota inferior positiva. p. 193:

> „We assume that P is formally positive, that is, (Pu,u) ≥ c(u,u),
> u ∈ C_0^∞(Ω), where c > 0“

e a extensão de Friedrichs herda „a positive lower bound c“. É mais forte
que semilimitação. (Na Seção 3 aparece o caso „formally self-adjoint
semibounded elliptic pseudo-differential operator of order 1“, contexto
auxiliar.)

### 7. O espaço de base é compacto?

**Não por hipótese.** `Ω` é „paracompact C^∞ manifold“. A compacidade é
usada como **conveniência de prova**:

- p. 196: „For the sake of simplicity we assume that Ω is compact, but in
  view of Theorem 5.3 in Hörmander [8] this is no essential restriction in
  the proof of Theorem 1.1.“
- p. 214: „Note first of all that by Theorem 5.3 in Hörmander [8] it
  suffices to prove the theorem when Ω is compact, for example a torus.“
- Seção 4 estuda „an elliptic pseudo-differential operator of order 1 on a
  **compact** manifold“.

### 8. Há bordo?

**Não.** Nenhuma condição de bordo é formulada em nenhuma das seções lidas.
`Ω` é variedade sem bordo.

### 9. O operador atua em funções escalares ou sistemas/fibrados?

**Escalares no corpo principal.** O espaço é `L²(Ω)` obtido completando
`C_0^∞(Ω)`, com `(u,v) = ∫ u v̄ dx` para uma densidade `C^∞` positiva fixa.

Sistemas aparecem apenas como observação final, p. 216:

> „Our methods can be applied with no essential modification in the case of
> **systems for which the eigenvalues of p(x,ξ) are distinct**. … However
> for systems with **multiple eigenvalues** we have **no information beyond**
> the results of Agmon–Kannai [1] and Hörmander [8].“

Ou seja: fibrados/sistemas só são cobertos sob a hipótese extra de
autovalores distintos do símbolo principal. A hipótese W2 do laboratório
(fibrado hermitiano de posto finito arbitrário) **não** é sustentada em
geral.

### 10. Qual função espectral é definida?

`e(x,y,λ)` = núcleo de `E_λ`, elemento de `C^∞(Ω × Ω)`, chamada „the
spectral function of the self-adjoint extension P̄“ (p. 193).

### 11. Qual assíntota local é provada?

Definindo (1.1), p. 193:

```
R(x,λ) = λ^{−n/m}·[ e(x,x,λ) − (2π)^{−n}·λ^{n/m}·∫_{B_x} dξ ]
```

com `B_x = {ξ ∈ T*_x ; p(x,ξ) < 1}`, o **Teorema 1.1** afirma que
`R(x,λ) = O(λ^{−1/m})` uniformemente em todo subconjunto compacto de `Ω`.

A forma explícita está no **Teorema 5.1**, p. 215, equação (5.3):

```
| e(x,x,λ) − (2π)^{−n} ∫_{p(x,ξ)<λ} dξ | ≤ C(1 + |λ|)^{(n−1)/m}
```

uniformemente em subconjuntos compactos de `Ω`. Há também (5.2) para
`e(x,y,λ)` com `x` próximo de `y`, e (5.4) fora da diagonal.

Por homogeneidade de grau `m` de `p`:
`∫_{p(x,ξ)<λ} dξ = λ^{n/m}·∫_{B_x} dξ`, de modo que a assíntota local é
`e(x,x,λ) ~ (2π)^{−n} λ^{n/m} vol(B_x)`, com resto `O(λ^{(n−1)/m})`.

### 12. Como a lei global de contagem é obtida?

**NÃO É OBTIDA NESTE ARTIGO.** Esta é a constatação central desta auditoria.

Busca no texto completo por „number of eigenvalues“, „counting function“,
`N(λ)`, „eigenvalues less than“: **nenhuma ocorrência**. O artigo não define
nem enuncia a função de contagem global
`N_P(Λ) = #{j : λ_j ≤ Λ}`.

Os únicos resultados globais adjacentes são o Teorema 5.2 (convergência de
médias de Riesz de expansões em autofunções, p. 215) e as observações sobre
médias de Riesz `e^α(x,x,λ)` (pp. 215–216) — nenhum deles é a lei de
contagem.

A passagem de (5.3) para `N_P(Λ)` exige integrar a diagonal sobre `Ω`,
`N_P(Λ) = ∫_Ω e(x,x,Λ) dx`, o que requer `Ω` **compacta** (para que a
integral e o espectro discreto façam sentido) e um argumento de
uniformidade. Esse passo é **corolário padrão da literatura, mas não está
escrito neste artigo**.

### 13. Qual potência de Λ aparece?

`Λ^{n/m}` no termo principal local; `Λ^{(n−1)/m}` no resto. Com
`n = dim Ω`. Corresponde ao expoente `α = d/m` da Classe W.

### 14. Qual constante principal aparece?

Localmente, `(2π)^{−n}·vol(B_x)` com `B_x = {ξ ; p(x,ξ) < 1}`. A constante
global `C_P = (2π)^{−n} ∫_Ω vol(B_x) dx` **não é escrita no artigo** — ela
só existe depois do passo de integração da questão 12.

### 15. Qual termo de erro aparece?

`C(1 + |λ|)^{(n−1)/m}` na forma (5.3). O artigo afirma na Seção 6 que este
resto é ótimo em geral (contraexemplo de Avakumović para o laplaciano na
esfera `S³ ⊂ R⁴`, generalizado à `n`-esfera).

### 16. O resultado cobre exatamente W1–W8?

**Não.** Ver a matriz linha a linha em `CLASS_W_SOURCE_MAPPING.md`.
Resumo: W1 (parcialmente — compacidade é conveniência, não hipótese),
W3 (ordem fixa sim; paridade de `m` não declarada na Classe W),
W4 (elipticidade, sim), W6 (positividade, sim) são sustentados;
W2 (fibrados) **não** em geral; W5 (auto-adjunção essencial) **difere** da
hipótese do artigo; W7 (espectro discreto) **não é provado**;
W8 (contagem global) **não é enunciado**.

### 17. Quais itens da Classe W não são sustentados diretamente pelo artigo?

1. **W8 — a lei de contagem global** `N_P(Λ) ~ C_P Λ^{d/m}`: ausente.
   Exige fonte adicional ou corolário documentado.
2. **W2 — fibrados vetoriais / sistemas**: só com autovalores distintos do
   símbolo principal; explicitamente sem informação no caso de
   multiplicidade.
3. **W5 — auto-adjunção**: o artigo usa *uma* extensão de Friedrichs; a
   Classe W exige essencial auto-adjunção.
4. **W7 — espectro discreto com multiplicidade finita**: não provado aqui;
   é consequência padrão de elipticidade + compacidade, mas fora deste
   artigo.
5. **W1 — compacidade sem bordo**: satisfeita mas por hipótese externa; o
   artigo trabalha em variedade paracompacta e usa compacidade como
   simplificação.

## Nenhuma afirmação de que „Hörmander prova a Classe W“

Conforme exigido pelo gate, nenhuma linha desta auditoria atribui ao artigo
a Classe W. O artigo prova uma **lei espectral local ótima**, mais forte e
mais geral em alguns aspectos (cobre pseudodiferenciais, variedades
paracompactas, resto ótimo) e mais fraca em outro decisivo (não enuncia a
contagem global).

## Veredito para o pilar B

**PARCIALMENTE SUSTENTADO.** A lei de Weyl local está diretamente provada.
A hipótese B de `ASYM-NOGO-001` — `N_P(Λ)/Λ^α → C_P > 0` — **não** decorre
literalmente deste artigo e requer fonte adicional. Ver
`UNRESOLVED_SOURCE_QUESTIONS.md`.
