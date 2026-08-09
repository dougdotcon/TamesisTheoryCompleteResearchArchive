# Resultado alvo

Particionar teoremas por curva, posto, primo, redução e conclusão, sem unir
resultados condicionais incompatíveis.

## Enunciado clássico da conjectura (mantido ao lado, não substituído)

Conforme `AGENTS.md` ("não substituir o enunciado clássico por linguagem
Tamesis"), o alvo desta frente **não é provar** o enunciado abaixo — é
mapear o que já se sabe sobre ele.

> **Conjectura (Birch e Swinnerton-Dyer, parte de posto).** Para `E/Q`
> curva elíptica, `rank(E(Q)) = ord_{s=1} L(E,s)`.
>
> **Conjectura (parte refinada).** Para `r = rank(E(Q)) = ord_{s=1} L(E,s)`:
> `L^(r)(E,1)/r! = (#Ш(E) · Ω_E · Reg(E) · ∏_p c_p) / (#E(Q)_tors)²`.

(Fonte: resumo padrão recuperado via WebFetch de
`en.wikipedia.org/wiki/Birch_and_Swinnerton-Dyer_conjecture`,
2026-08-09 — ver `DEFINITIONS.md` e `REVIEWS/AUDIT_REPORT.md`.)

## O que o produto desta frente é

Uma matriz (`KNOWN_RESULTS_MATRIX.md`) que, para cada teorema publicado
relevante, registra: hipótese exata, curva/família coberta, posto
analítico coberto, primos excluídos/exigidos, e conclusão exata — mantendo
cada linha isolada das demais.

## O que o produto desta frente NÃO é

- Não é uma prova de BSD, condicional ou não.
- Não é uma estimativa de "% da conjectura provada" (essa aritmética —
  presente no documento legado `ANALISE_CRITICA_BSD.md` — é exatamente o
  padrão de erro que o `stop_condition` desta frente proíbe reproduzir).
- Não é uma alegação de que a união dos casos cobertos pelas linhas da
  matriz se aproxima da cobertura universal da conjectura.
