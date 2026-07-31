# Ponte conceitual — requisitos, sem prova

Mapa lógico das etapas que ligariam as duas leis de contagem ao lema já
formalizado `ASYM-NOGO-001`. **Nenhuma dessas etapas foi executada neste
gate.** Este documento é um mapa de requisitos, não uma demonstração.

Estados: `PROVED_IN_SOURCE`, `ELEMENTARY_COROLLARY`, `REQUIRES_FORMALIZATION`,
`REQUIRES_ADDITIONAL_SOURCE`, `UNRESOLVED`.

---

## A. Definição moderna de `N_ζ(T)`

`N_ζ(T) := #{ρ : ζ(ρ) = 0, 0 < Re ρ < 1, 0 < Im ρ ≤ T}`, com multiplicidade.

| campo | valor |
|---|---|
| status | `PROVED_IN_SOURCE` (como definição equivalente) |
| fonte | VONMANGOLDT-1905 p. 2 (definição por `ξ(t)` e parte real, com multiplicidade); BOMBIERI-CLAY p. 1 (correspondência `ρ = ½ + iα`) |
| observação | Requer a **tradução de notação** registrada em `VON_MANGOLDT_1905_AUDIT.md` q.11 (parte real no plano `t` ↔ ordenada no plano `s`). A convenção de fronteira difere: von Mangoldt escolhe `T` fora de zeros; a definição moderna usa `≤ T`. Reconciliação é elementar mas **não escrita**. |

## B. Fórmula de Riemann–von Mangoldt

`N_ζ(T) = (T/2π)log(T/2π) − T/2π + 7/8 + O(log T)`.

| campo | valor |
|---|---|
| status | `PROVED_IN_SOURCE` |
| fonte | VONMANGOLDT-1905, p. 19, fórmula final, com cota efetiva `0,43200 lT + 1,91662 llT + 12,20373` para `T > 28,558` |
| observação | Incondicional. Não depende da RH. |

## C. Dedução `N_ζ(T)/(T log T) → 1/(2π)`

| campo | valor |
|---|---|
| status | `ELEMENTARY_COROLLARY` + `REQUIRES_FORMALIZATION` |
| fonte | decorre de B por álgebra e `log(T/2π)/log T → 1` |
| observação | Matematicamente trivial; **não formalizado em Lean**. Seria a instância da hipótese A de `ASYM-NOGO-001` com `c = 1/(2π)`. Exigiria formalizar `ζ`, seus zeros e a fórmula B — tarefa muito além de qualquer autorização vigente. |

## D. Definição de `N_P(Λ)`

`N_P(Λ) := #{j : λ_j ≤ Λ}` para `P̄` na Classe W, com multiplicidade.

| campo | valor |
|---|---|
| status | `REQUIRES_ADDITIONAL_SOURCE` |
| fonte | **ausente** em HORMANDER-1968 |
| observação | Pressupõe W7 (espectro discreto de multiplicidade finita), que o artigo não prova. Ver `CLASS_W_SOURCE_MAPPING.md`, linha W7. |

## E. Lei de Weyl para a classe exata

`N_P(Λ) ~ C_P Λ^{d/m}` com `C_P > 0`.

| campo | valor |
|---|---|
| status | `REQUIRES_ADDITIONAL_SOURCE` |
| fonte | **não enunciada** em HORMANDER-1968; o artigo prova a assíntota **local** (5.3) da função espectral na diagonal |
| observação | **Este é o elo faltante do gate.** A passagem `N_P(Λ) = ∫_Ω e(x,x,Λ) dx` requer compacidade de `Ω` e uniformidade global da estimativa (5.3). É corolário padrão na literatura, mas precisa de fonte que o enuncie. Candidatos listados em `UNRESOLVED_SOURCE_QUESTIONS.md` — **nenhum obtido**. |

## F. Dedução `N_P(Λ)/Λ^{d/m} → C_P`

| campo | valor |
|---|---|
| status | `UNRESOLVED` (depende de E) |
| observação | Trivial dado E; impossível de afirmar sem E. |

## G. Hipótese de igualdade ou equivalência entre as funções de contagem

`Spec⁺(P̄) = {γ_n}` como multiconjuntos, ou `N_P(T)/N_ζ(T) → 1`.

| campo | valor |
|---|---|
| status | `REQUIRES_FORMALIZATION` |
| observação | É a **hipótese do no-go**, não um fato a provar: assume-se por contradição. Precisa de definição formal de igualdade de multiconjuntos espectrais (GAP-RH-005) e da escolha entre os três níveis de `OPERATOR_CLASS.md`. |

## H. Aplicação futura de `ASYM-NOGO-001`

| campo | valor |
|---|---|
| status | `REQUIRES_FORMALIZATION` |
| observação | Com C (⟹ hipótese A, `c = 1/2π`) e F (⟹ hipótese B, `α = d/m`, `C = C_P`) instanciadas sobre a **mesma** função de contagem via G, o lema já verificado fecha a contradição. Nada disso está autorizado. |

---

## Diagnóstico

```text
Pilar A (zeros)     : A ✓  B ✓  C = corolário elementar não formalizado
Pilar B (espectral) : D ✗  E ✗  F bloqueado por E
Junção              : G e H requerem formalização; nenhuma autorizada
```

A cadeia está **quebrada em E**. Nenhuma fonte obtida sustenta a lei de
contagem espectral global para a Classe W declarada.
