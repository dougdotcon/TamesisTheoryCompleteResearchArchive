# Definições

Estado: `NOT_FORMALIZED` em Lean (nenhum destes objetos existe como tipo
verificado em `FORMAL/` — ver `PROOF_SKETCH.md` para o porquê). Este arquivo
fixa as definições matemáticas usadas pela matriz em
`KNOWN_RESULTS_MATRIX.md`, em linguagem clássica, para que a partição por
hipótese seja legível sem ambiguidade.

Fonte do enunciado clássico da conjectura (formato de referência, não
paráfrase Tamesis — conforme exigido por `AGENTS.md`): resumo extraído via
WebFetch de `en.wikipedia.org/wiki/Birch_and_Swinnerton-Dyer_conjecture` em
2026-08-09 nesta sessão. Marcado como **verificado (fonte secundária)**: o
Wikipedia não é fonte primária, mas a fórmula reproduzida abaixo é o
enunciado padrão presente em qualquer referência primária da área (Wiles,
*The Birch and Swinnerton-Dyer Conjecture*, descrição oficial Clay — PDF
localizado mas não extraível nesta sessão por falta de `pdftotext`/parser
de PDF no ambiente; ver `REVIEWS/AUDIT_REPORT.md`).

## Objetos

- **Curva elíptica `E/Q`**: curva projetiva suave de gênero 1 com ponto
  racional, dada por um modelo de Weierstrass sobre `Q`. Conjectura de
  modularidade (Wiles 1995; Breuil–Conrad–Diamond–Taylor, *"On the
  modularity of elliptic curves over Q"*, 2001) garante que toda `E/Q` é
  modular — hipótese "modular" nos teoremas clássicos (Gross–Zagier,
  Kolyvagin) é hoje incondicional para todo `E/Q`. **Verificado**: citação
  BCDT 2001 recuperada nesta sessão (ver `REVIEWS/AUDIT_REPORT.md`).

- **Posto algébrico `rank_alg(E)`**: posto do grupo abeliano finitamente
  gerado `E(Q)` (teorema de Mordell–Weil).

- **Posto analítico `rank_an(E)`**: ordem de anulação de `L(E,s)` em
  `s = 1`, i.e. o maior `r` tal que `L(E,s) = (s-1)^r · g(s)` com `g(1) ≠ 0`.

- **Conjectura de posto (parte fraca de BSD)**: `rank_alg(E) = rank_an(E)`.

- **Ш(E) (grupo de Tate–Shafarevich)**: `Ш(E) = ker(H¹(Q,E) → ∏_v H¹(Q_v,E))`.
  BSD completa requer `Ш(E)` finito — este é, por si só, um problema aberto
  em geral (não decorre automaticamente de nenhum teorema listado na
  matriz fora dos casos rank 0/1 e CM). Ver `GAP_REGISTER.yaml`
  (`BSD-GAP-002`).

- **Grupo de Selmer `Sel_p(E/Q)`**: grupo intermediário
  `E(Q)/pE(Q) ↪ Sel_p(E/Q)` com `Ш(E)[p]` como quociente; o objeto que os
  sistemas de Euler/Kolyvagin e as Main Conjectures de Iwasawa realmente
  controlam (não `Ш(E)` diretamente).

- **Fórmula refinada (BSD forte)**, para `r = rank_an(E) = rank_alg(E)`:

  ```
  L^(r)(E,1) / r!  =  ( #Ш(E) · Ω_E · Reg(E) · ∏_p c_p ) / (#E(Q)_tors)²
  ```

  onde `Ω_E` é o período real (vezes número de componentes reais), `Reg(E)`
  é o regulador via alturas canônicas, `c_p` são os números de Tamagawa nos
  primos de má redução, `#E(Q)_tors` é a ordem do subgrupo de torção.
  **Verificado (fonte secundária)** — mesma fonte Wikipedia acima; forma
  padrão em qualquer tratamento da conjectura.

- **Redução em `p`**: boa (good), multiplicativa (má, split/non-split),
  aditiva; "semiestável" = boa ou multiplicativa em todo primo. "Primo
  ordinário/supersingular em `p`" refere-se ao comportamento de
  `a_p(E) mod p` (ordinário se `p ∤ a_p`, supersingular se `p | a_p`, para
  boa redução).

- **Primo de Eisenstein**: primo `p` onde a representação de Galois mod `p`
  associada a `E` é redutível (não irreducível) — regime tecnicamente
  distinto e historicamente separado do caso "ordinário com representação
  irredutível" que a maioria dos teoremas de Iwasawa (Skinner–Urban, BCS)
  assume.

## Nota de escopo

Estas definições servem apenas para tornar `KNOWN_RESULTS_MATRIX.md`
legível. Nenhuma delas foi formalizada em Lean nesta sessão — ver
`FORMAL/` para o único artefato Lean produzido (um esboço de lógica
proposicional sobre o padrão de falácia do `stop_condition`, não sobre
BSD em si).
