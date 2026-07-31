# RIEMANN 1859 — auditoria de fonte histórica

Fonte lida: *On the Number of Prime Numbers less than a Given Quantity*,
tradução inglesa de **David R. Wilkins** (versão preliminar, dezembro de
1998, © D. R. Wilkins 1998), hospedada pelo Clay Mathematics Institute.
Cópia: `pdf/riemann_1859_wilkins_translation.pdf`, sha256 `6b24341e…`.
Estado: `CONTENT_AUDITED` — tradução lida integralmente (9 páginas).

**Ressalva de proveniência:** o **original alemão** (Monatsberichte der
Berliner Akademie, novembro de 1859; Gesammelte Werke) **não foi obtido**.
Todas as citações abaixo são da tradução. Nenhuma afirmação literal sobre a
redação alemã de Riemann é feita neste laboratório.

## Separação: conjectura, esboço e afirmação demonstrada

A passagem relevante (tradução, p. 4) é uma só e contém os três registros:

> „The number of roots of ξ(t) = 0, whose real parts lie between 0 and T is
> approximately
>
>   = (T/2π) log(T/2π) − T/2π ;
>
> because the integral ∫ d log ξ(t), taken in a positive sense around the
> region consisting of the values of t whose imaginary parts lie between
> ½i and −½i and whose real parts lie between 0 and T, is (up to a fraction
> of the order of magnitude of the quantity 1/T) equal to
> [T log(T/2π) − T] i; this integral however is equal to the number of roots
> of ξ(t) = 0 lying within this region, multiplied by 2πi. One now finds
> indeed approximately this number of real roots within these limits, and it
> is very probable that all roots are real. **Certainly one would wish for a
> stricter proof here; I have meanwhile temporarily put aside the search for
> this after some fleeting futile attempts, as it appears unnecessary for
> the next objective of my investigation.“**

Classificação:

| Registro | Conteúdo |
|---|---|
| **Afirmação de contagem** | o número de raízes de `ξ(t) = 0` com parte real em `(0,T)` é *aproximadamente* `(T/2π)log(T/2π) − T/2π` |
| **Esboço de justificativa** | o princípio do argumento sobre a região `|Im t| ≤ 1/2`, `0 < Re t < T`, com erro „of the order of magnitude of 1/T“ |
| **Conjectura (a RH)** | „it is very probable that all roots are real“ |
| **Reconhecimento explícito de lacuna** | „Certainly one would wish for a stricter proof here … I have temporarily put aside the search for this“ |

## Consequências para a auditoria

1. **A fórmula rigorosa moderna NÃO deve ser atribuída a Riemann.** Riemann
   dá a expressão e um argumento por contorno, mas declara ele próprio que
   falta uma prova estrita. O rigor — inclusive o termo `7/8` e um termo de
   erro efetivo `O(log T)` — é de **von Mangoldt 1905**
   (`VON_MANGOLDT_1905_AUDIT.md`).
2. Riemann já conta **por parte real de `t`**, exatamente a convenção que
   von Mangoldt formaliza e que corresponde à ordenada moderna `Im ρ`.
3. Riemann restringe a região a `|Im t| ≤ 1/2`, o que corresponde à faixa
   crítica `0 ≤ Re s ≤ 1`. A contagem é, portanto, dos zeros não triviais.
4. Riemann **não** menciona multiplicidades nesta passagem; von Mangoldt as
   inclui explicitamente („jede so oft gezählt, als ihre Ordnungszahl
   angibt“).
5. Nada nesta memória tem relação com operadores, espectros de operadores
   diferenciais ou a Classe W. A memória é sobre `π(x)`, a fórmula
   explícita `f(x) = Li(x) − Σ_α [Li(x^{1/2+αi}) + Li(x^{1/2−αi})] + ∫ … +
   log ξ(0)` e a inversão de Möbius para `F(x)`.

## Definições fixadas por Riemann e usadas adiante

- `ξ(t) = Π(s/2)(s−1)π^{−s/2} ζ(s)` com `s = ½ + ti` (tradução, p. 3).
- Os zeros de `ζ` em inteiros pares negativos são identificados na
  continuação analítica (tradução, p. 2), o que fixa a distinção
  trivial/não trivial.
- Riemann denota por `α` as raízes de `ξ(α) = 0` — a mesma letra usada por
  von Mangoldt na p. 18 para os valores `14,134725`, `21,022040`,
  `25,010856`.

## Nenhuma promoção

Esta fonte é **histórica**. Nenhuma afirmação dela é usada como resultado
estabelecido nesta frente; o pilar A repousa em von Mangoldt 1905.
