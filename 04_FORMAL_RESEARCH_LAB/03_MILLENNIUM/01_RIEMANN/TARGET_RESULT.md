# RH-NOGO-001 — Resultado alvo (especificação, sem prova)

## Enunciado candidato (PROPOSED)

> Seja `M` uma variedade riemanniana suave, compacta, sem bordo, de dimensão
> finita `d ≥ 1`, e seja `P` um operador diferencial elíptico clássico de
> ordem inteira fixa `m ≥ 1`, auto-adjunto e positivo, agindo nas seções
> suaves de um fibrado vetorial hermitiano suave sobre `M`, com espectro
> discreto contado com multiplicidade e satisfazendo a lei de Weyl padrão
> `N_P(Λ) ~ C_P · Λ^{d/m}` com `C_P > 0`.
>
> Então o multiconjunto dos autovalores positivos de `P` **não** pode
> coincidir com o multiconjunto `{γ_n}` das ordenadas positivas dos zeros
> não triviais de `ζ`, contadas com multiplicidade. Mais: nenhuma
> coincidência com discrepância limitada, e nenhuma equivalência assintótica
> de densidade (`N_P(T)/N_ζ(T) → 1`), é possível.

## Fundamento da incompatibilidade

Duas leis de contagem incompatíveis:

```text
Contagem dos zeros (Riemann–von Mangoldt, incondicional):
N_ζ(T) = (T/2π) log(T/2π) − T/2π + O(log T)
⟹ N_ζ(T) / (T log T) → 1/(2π)

Contagem espectral (Weyl, na classe auditada):
N_P(T) ~ C_P · T^{d/m},  C_P > 0,  α := d/m > 0
⟹ N_P(T) / T^α → C_P
```

Nenhuma função de contagem pode satisfazer as duas assintóticas
simultaneamente (núcleo abstrato `ASYM-NOGO-001`, ver
`ASYMPTOTIC_CORE.md`): para `α = 1` o fator `log T` diverge; para `α ≠ 1`
as potências dominantes diferem.

## O que o resultado é

- A exclusão de **uma classe convencional estreita e delimitada** de
  candidatos espectrais (ver `OPERATOR_CLASS.md`).
- Uma observação de nível folclórico na literatura de Hilbert–Pólya
  (a contagem `T log T` não é lei de potência), aqui transformada em
  enunciado exato, com classe explícita, e preparada para formalização.
  A novidade matemática é **baixa por construção** (GAP-RH-007);
  o valor está na precisão, na delimitação e na formalização futura.

## O que o resultado NÃO é

- Não exclui a rota de Hilbert–Pólya em geral.
- Não diz nada sobre a verdade ou falsidade da Hipótese de Riemann.
- Não toca as rotas de Connes (espectro de absorção, geometria não
  comutativa), Berry–Keating (`H = xp`, não compacto), Bender–Brody–Müller
  (não hermitiano PT) nem Hedenmalm (semirreta, auto-adjunção adaptada) —
  ver `ESCAPE_ROUTES.md`.

## Decisão deste gate

`SPECIFICATION_READY` (opção A) — com as ressalvas de GAP-RH-002
(fonte primária exata da versão da lei de Weyl usada) e GAP-RH-007
(auditoria de novidade) mantidas abertas e não bloqueantes para a
formalização do núcleo abstrato, que é independente de PDE.
