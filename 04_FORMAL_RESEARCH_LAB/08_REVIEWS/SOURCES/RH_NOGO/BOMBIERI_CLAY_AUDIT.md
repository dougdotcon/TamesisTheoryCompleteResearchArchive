# BOMBIERI / CLAY — auditoria de contextualização oficial

Fonte: E. Bombieri, *Problems of the Millennium: the Riemann Hypothesis*,
Clay Mathematics Institute.
Cópia: `pdf/bombieri_clay_rh.pdf`, sha256 `1454b290…`, 11 páginas.
Estado: `PARTIALLY_AUDITED` — Seção I (o problema) e o início da Seção II
lidas integralmente; o restante (história, significância, evidência,
generalizações) não lido.

Classificação: **contextualização oficial moderna**. Não é substituto da
prova original de von Mangoldt e não é usado como tal em lugar algum.

## Definição moderna da RH (p. 1)

> „ζ(s) extends to C as a meromorphic function with only a simple pole at
> s = 1, with residue 1, and satisfies the functional equation
> π^{−s/2}Γ(s/2)ζ(s) = π^{−(1−s)/2}Γ((1−s)/2)ζ(1−s).“   (1)

> „Riemann introduces the function of the complex variable t defined by
> ξ(t) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s) with s = ½ + it, and shows that ξ(t)
> is an even entire function of t whose zeros have imaginary part between
> −i/2 and i/2.“

> „**The statement that all zeros of the function ξ(t) are real is the
> Riemann hypothesis.**“

> „The function ζ(s) has zeros at the negative even integers −2, −4, … and
> one refers to them as the trivial zeros. The other zeros are the complex
> numbers ½ + iα where α is a zero of ξ(t). Thus, in terms of the function
> ζ(s), we can state
> **Riemann hypothesis. The nontrivial zeros of ζ(s) have real part equal to ½.**“

## Descrição da contagem dominante (p. 1)

> „He further **states, sketching a proof**, that in the range between 0 and
> T the function ξ(t) has about (T/2π) log(T/2π) − T/2π zeros.“

Dois pontos registrados:

1. A fonte oficial atribui a contagem a **Riemann**, e qualifica
   explicitamente como *„states, sketching a proof“* — coerente com a
   auditoria de `RIEMANN_1859_AUDIT.md`.
2. A fonte oficial **não** enuncia o termo `7/8` nem um termo de erro
   efetivo. Para isso a fonte é von Mangoldt 1905.

## Verificação cruzada da tradução de notação

Bombieri confirma independentemente a correspondência usada em
`VON_MANGOLDT_1905_AUDIT.md`, questão 11: os zeros não triviais de `ζ` são
`½ + iα` com `α` zero de `ξ(t)`; contar zeros de `ξ` „in the range between 0
and T“ (parte real de `t`) é contar ordenadas `Im ρ ∈ (0,T)`.

Normalização: a definição de Bombieri, `ξ(t) = ½ s(s−1)π^{−s/2}Γ(s/2)ζ(s)`,
difere por fator constante e por `Π` versus `Γ` da usada por Riemann e por
von Mangoldt (eq. (1) da p. 2 daquele artigo). **Fatores constantes não
alteram o conjunto de zeros**, logo a contagem é a mesma. Registrado para
que nenhuma citação futura confunda as normalizações.

## Status do problema

> „In the opinion of many mathematicians the Riemann hypothesis, and its
> extension to general classes of L-functions, is probably today the most
> important **open problem** in pure mathematics.“

Confirma que nenhuma prova é aceita. Este laboratório não afirma o
contrário em nenhum artefato.

## Uso permitido

- Fonte do **enunciado oficial** da RH.
- Fonte de **contextualização** e da atribuição histórica.
- **Não** é fonte para o termo de erro, para o termo `7/8`, nem para
  qualquer afirmação sobre operadores ou a Classe W.
