# Hipóteses — YM-LIMIT-001

Status anterior: `NOT_AUDITED`. Esta rodada audita explicitamente a cadeia
de hipóteses usada por construções candidatas ao mass gap de Yang–Mills, e
identifica qual elo dessa cadeia não é uma implicação lógica automática.

## A cadeia tal como costuma ser apresentada (informalmente)

```text
(H1) Balaban: bounds UV uniformes, weak coupling, SU(2), regime β grande
(H2) Strong coupling: area law, string tension > 0, regime β pequeno
(H3) Continuidade/monotonicidade de m(β) interpolando os dois regimes
(H4) Svetitsky–Yaffe: universalidade da transição de deconfinamento
(H5) Tightness da família de medidas de rede ⇒ limite contínuo existe
(H6) Gap de volume finito uniforme ⇒ gap sobrevive no limite contínuo
──────────────────────────────────────────────────────────────────────
(C)  ⇒ existe teoria de Yang–Mills contínua, única, não trivial, com gap
```

Esta auditoria (YM-LIMIT-001) não reexamina H1, H2 ou H4 como resultados
per se — trata da validade lógica de H5 e H6 como passos de inferência,
que é o escopo definido pelo `target_statement` desta frente.

## H5 — Tightness ⇒ limite contínuo (único, não trivial)

**Não tratar como cadeia automática.** O que Prokhorov de fato entrega:

- tightness ⇒ toda sequência tem subsequência fracamente convergente
  (compacidade relativa fraca-*).
- tightness **não** entrega: que a sequência completa converge; que o
  limite é independente da subsequência escolhida; que o limite é não
  trivial; que o limite satisfaz os axiomas de Osterwalder–Schrader.

Ver `PROOF_SKETCH.md` e `COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md` para
o contraexemplo abstrato que demonstra a insuficiência de H5 sozinha.

## H6 — Gap uniforme em volume finito ⇒ gap sobrevive no limite

**Não tratar como cadeia automática.** Dois sub-problemas distintos, que a
literatura às vezes funde num só:

1. **H6a** (uniformidade em si): mostrar que \(m(a,L) \ge c > 0\) para
   *todo* \(a,L\) no regime intermediário (nem puramente UV nem puramente
   IR) — este é exatamente o "GAP 1" identificado no documento legado
   (`ANALISE_CRITICA_YM.md`, seção 4), decorrente de H3 não ser um teorema
   e sim uma extrapolação de monotonicidade.
2. **H6b** (semicontinuidade): mesmo assumindo H6a, mostrar que a
   convergência dos operadores (ou medidas) associados é forte o
   suficiente para que o gap não feche no limite. Convergência fraca de
   medidas, ou mesmo convergência forte de resolvente, **não bastam** em
   geral — o espectro do limite pode "contrair repentinamente" mesmo sob
   convergência forte de resolvente (ver `REVIEWS/AUDIT_REPORT.md`,
   seção Verificado).

## Balaban (SU(2) → SU(N)) — não tratar como automático

A extensão dos bounds de Balaban de SU(2) para SU(N) geral é tratada na
literatura secundária/no documento legado como "por universalidade" — esta
auditoria **não verifica** essa extensão (fora de escopo desta frente;
não confirmado nesta sessão) e não a assume como dada.

## Svetitsky–Yaffe — não tratar como teorema de gap a T=0

O resultado de Svetitsky–Yaffe (1982) é sobre a classe de universalidade
da **transição de deconfinamento a temperatura finita** (mapeamento para
o modelo de spin \((D{-}1)\)-dimensional com a simetria de centro de
\(G\)) — confirmado como formulado em termos de universalidade de
transição de fase térmica (ver `REVIEWS/AUDIT_REPORT.md`). Isso não é,
por si, um enunciado sobre ausência de transição a \(T=0\) no limite
euclidiano infinito, que é o que o argumento de interpolação da cadeia
acima precisaria.

## Hipótese adicional exigida (não presente na cadeia original)

Para que H6 valha, é necessária uma hipótese extra do tipo:

```text
(H6') inf_{a,L} m(a,L) > 0   [uniformidade explícita, não derivada de H1+H2]
```

sem a qual o contraexemplo de `FORMAL/InsufficiencyToyModel.lean`
(`toyFiniteVolumeGap_not_uniform`) mostra que gap positivo em cada volume
finito, sozinho, é compatível com gap nulo no limite.
