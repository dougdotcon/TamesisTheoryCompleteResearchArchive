# RH-NOGO-001 — Classe de operadores excluída (Classe W)

## Definição da classe W (v1)

Um operador `P` pertence à Classe W quando **todas** as condições valem:

| # | Condição |
|---|---|
| W1 | `M` é variedade riemanniana suave, compacta, **sem bordo**, `dim M = d`, `1 ≤ d < ∞` |
| W2 | `E → M` é fibrado vetorial hermitiano suave de posto finito (caso escalar incluído) |
| W3 | `P` é operador **diferencial** clássico de ordem inteira fixa `m ≥ 1`, com coeficientes suaves, agindo em `C^∞(M, E)` |
| W4 | `P` é elíptico (símbolo principal invertível fora da seção nula) |
| W5 | `P` é essencialmente auto-adjunto em `L²(M, E)` a partir de `C^∞(M, E)`, com extensão auto-adjunta `P̄` |
| W6 | `P̄` é positivo (`⟨Pu, u⟩ > 0` para `u ≠ 0`); ver `ASSUMPTIONS.md` para a variante limitado-inferiormente |
| W7 | O espectro de `P̄` é discreto, com autovalores de multiplicidade finita, contados com multiplicidade |
| W8 | Vale a lei de Weyl padrão: `N_P(Λ) = #{λ_j ≤ Λ} ~ C_P · Λ^{d/m}` com `C_P > 0` |

W7 e W8 são consequências conhecidas de W1–W6 na literatura padrão
(elipticidade + compacidade ⟹ resolvente compacto ⟹ espectro discreto;
Weyl/Gårding/Hörmander para a assintótica), mas a Classe W as **postula
explicitamente** para que a exclusão não dependa de reprovar esses fatos —
a prova futura usa W8 como hipótese, e a auditoria de fonte primária da
versão exata de W8 é GAP-RH-002.

## Alvo de exclusão

Para `P` na Classe W, definindo `Spec⁺(P̄)` como o multiconjunto dos
autovalores positivos:

```text
EXCLUÍDO (três níveis, do mais fraco ao mais forte):
(i)   Spec⁺(P̄) = {γ_n} como multiconjuntos (igualdade exata);
(ii)  |N_P(T) − N_ζ(T)| = O(1) (discrepância limitada);
(iii) N_P(T) / N_ζ(T) → 1 (equivalência assintótica de densidade).
```

A prova futura precisa apenas do nível (iii): (i) ⟹ (ii) ⟹ (iii), e (iii)
já contradiz `ASYM-NOGO-001`.

## Parâmetro assintótico

`α := d/m ∈ ℚ, α > 0`. O núcleo abstrato não usa a racionalidade — vale
para todo real `α > 0` — então a formalização não depende de `d` e `m`
individualmente, apenas de `α > 0` e `C_P > 0`.

## O que a Classe W deliberadamente NÃO cobre

Ver `EXCLUSIONS.md` e `ESCAPE_ROUTES.md`. Em particular: espaços não
compactos, bordo, operadores pseudodiferenciais gerais, ordem variável,
não localidade, não auto-adjunção convencional, espectros de absorção,
ressonâncias, pares generalizados de autovalor e espectros em que os zeros
são apenas subconjunto.
