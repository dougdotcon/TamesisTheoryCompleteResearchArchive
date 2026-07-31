# Constante global `C_P` — auditoria

## Forma escalar (candidata)

A forma proposta pelo gate,

```text
C_P = (2π)^{−d} ∫_{T*M} 1_{p_m(x,ξ) ≤ 1} dx dξ
```

é **compatível** com as fontes obtidas no caso escalar:

- Hörmander 1968, eq. (1.1), p. 193, usa localmente
  `(2π)^{−n} ∫_{B_x} dξ` com `B_x = {ξ ∈ T*_x ; p(x,ξ) < 1}`;
- integrando sobre `M` (etapa F de `HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md`)
  obtém-se exatamente a expressão acima.

Estado: `ELEMENTARY_COROLLARY` a partir de Hörmander (1.1) + compacidade.
**Não escrita nesta forma em nenhuma fonte obtida.**

## Forma para sistemas / fibrados — a fonte usa outra expressão

Ivrii 2016, eq. (3.1.3):

```text
κ₀ = (2π)^{−d} ∬ n(x,ξ) dx dξ
```

onde, literalmente, *"`n(x,ξ)` is the number of eigenvalues of `A⁰(x,ξ)` in
`(0,1)`"* e `m = m_A` é a ordem de `A`.

Consequência registrada, conforme exigido pelo gate:

> **Não usar a fórmula escalar para sistemas sem justificativa.**

No caso escalar, `A⁰(x,ξ)` é um número e `n(x,ξ) ∈ {0,1}` é a função
indicadora de `{p(x,ξ) < 1}` — as duas fórmulas coincidem. No caso de
sistemas ou fibrados de posto `r > 1`, `n(x,ξ)` conta autovalores **com
multiplicidade**, o que corresponde a uma soma sobre os autovalores do
símbolo principal, **não** a um simples volume. Registrado como a forma
correta.

| Caso | Constante | Fonte |
|---|---|---|
| escalar | `(2π)^{−d} ∫_M vol{ξ : p(x,ξ) < 1} dx` | corolário elementar de Hörmander (1.1) |
| sistema / fibrado | `(2π)^{−d} ∬ n(x,ξ) dx dξ`, `n` = nº de autovalores de `A⁰(x,ξ)` em `(0,1)` | Ivrii (3.1.3) |

Itens que o gate mandou verificar:

- **traço:** aparece indiretamente — `n(x,ξ)` é o traço do projetor
  espectral do símbolo principal sobre `(0,1)`;
- **soma sobre autovalores do símbolo principal:** sim, é exatamente isso;
- **multiplicidades:** contadas por `n(x,ξ)`;
- **densidade escolhida:** Hörmander fixa *"some positive `C^∞` density
  `dx`, kept fixed throughout"* (p. 193); a constante depende dessa escolha,
  e a medida `dξ` na fibra é a de Lebesgue determinada por `dx`.

## Positividade `C_P > 0`

**Não afirmada por nenhuma fonte obtida.** Registro do que seria preciso:

Argumento elementar (não formalizado, não citado): sendo `P` elíptico e
positivo, `p(x,ξ) > 0` para `ξ ≠ 0` e `p(x,·)` é homogênea de grau `m > 0`;
logo `B_x = {p(x,·) < 1}` é uma vizinhança aberta não vazia da origem em
`T*_xM`, portanto de medida positiva. Como `M` é compacta e `x ↦ vol(B_x)`
é contínua e positiva, a integral é positiva.

Estado: `ELEMENTARY_COROLLARY`, **hipótese necessária registrada, não
demonstrada nem citada**. Sem `C_P > 0` a pertinência a `W-POWER` falha,
pois `W-POWER` exige `C > 0`.

## Dependência com a ordem

`α = d/m`. Com a reformulação pseudodiferencial (`m > 0` real), `α` é um
real positivo arbitrário — o que é exatamente a generalidade de
`ASYM-NOGO-001`, cujo enunciado quantifica sobre `α > 0` real.
