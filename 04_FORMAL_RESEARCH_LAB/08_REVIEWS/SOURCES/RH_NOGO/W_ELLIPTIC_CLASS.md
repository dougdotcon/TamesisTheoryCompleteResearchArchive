---
class_id: W-ELLIPTIC
kind: geometric-spectral-class
version: 2
supersedes: "Classe W v1 (OPERATOR_CLASS.md)"
source_of_formulation: "CORIASCO-DOLL-2020, Introdução, p. 1 (enunciado citado)"
---

# Classe W-ELLIPTIC (v2) — classe geométrica

Formulação **copiada da fonte**, não construída pelo laboratório. A fonte é
o enunciado que Coriasco–Doll atribuem a Hörmander, transcrito literalmente
em `GLOBAL_WEYL_THEOREM_CANDIDATES.md`.

## Definição

`P` pertence a **W-ELLIPTIC** quando:

| # | Condição | Origem literal |
|---|---|---|
| E1 | `X` é uma **variedade compacta** de dimensão `d` | CORIASCO-DOLL-2020 p. 1 |
| E2 | `P` é um operador **pseudodiferencial clássico** | idem |
| E3 | `P` é **elíptico** | idem |
| E4 | `P` é **auto-adjunto** (uma realização auto-adjunta, não "essencialmente auto-adjunto") | idem; ver `SELF_ADJOINT_REALIZATION_DECISION.md` |
| E5 | `P` é **positivo** | idem |
| E6 | a **ordem** `m > 0` (real, sem restrição de paridade) | idem; ver `ORDER_PARITY_AUDIT.md` |

Conclusão associada, na fonte:

```text
N(λ) = γ · λ^(d/m) + O(λ^((d−1)/m)),    λ → +∞
```

com `N(λ) = #{j : λ_j < λ}` (CORIASCO-DOLL-2020, eq. (1)).

## Mudanças em relação à Classe W v1

| v1 (`OPERATOR_CLASS.md`) | v2 | Motivo |
|---|---|---|
| operador **diferencial** de ordem inteira `m ≥ 1` | pseudodiferencial **clássico**, ordem real `m > 0` | elimina o defeito de paridade (GAP-RH-011): a classe v1 era vazia para `m` ímpar |
| **essencialmente auto-adjunto** (extensão única) | **auto-adjunto** (uma realização) | Hörmander usa uma extensão de Friedrichs; exigir unicidade era hipótese não sustentada (GAP-RH-010) |
| variedade riemanniana compacta **sem bordo** | variedade **compacta** (a fonte não explicita bordo) | ver "Ambiguidades preservadas" |
| fibrado hermitiano de posto finito | **não declarado** na fonte citada | GAP-RH-009 permanece aberto |
| positividade `⟨Pu,u⟩ > 0` | positividade (a fonte diz apenas "positive") | forma equivalente na prática |
| W7 discretude **postulada** | **derivada** de resolvente compacto | ver `HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md`, etapas A–B |
| W8 contagem global **postulada** | **enunciada por fonte** | achado deste gate |

## Ambiguidades preservadas, não resolvidas

1. **Bordo.** CORIASCO-DOLL-2020 diz "compact manifold" sem qualificar
   bordo. Hörmander 1968 não formula condição de bordo alguma, o que
   sugere variedade fechada. Ivrii enuncia a versão com problema de valor
   de contorno (`D(A) = {u : Bu|∂X = 0}`). **Nenhuma das fontes obtidas
   afirma literalmente "closed manifold"** para a forma pseudodiferencial.
   Registrado como `AMBIGUOUS`.
2. **Fibrados / sistemas.** O enunciado citado é escalar por omissão.
   Ivrii (3.1.3) usa `n(x,ξ)` = número de autovalores de `A⁰(x,ξ)` em
   `(0,1)`, que **é** a forma correta para sistemas — mas em contexto de
   problema de contorno. Ver `GLOBAL_WEYL_CONSTANT.md`.
3. **Positividade da constante `γ`.** A fonte citada não a discute.
   Ver `GLOBAL_WEYL_CONSTANT.md`.

## Inclusão pretendida

```text
W-ELLIPTIC ⊆ W-POWER      com  α = d/m,  C = γ
```

Esta inclusão é o conteúdo de `GLOBAL-WEYL-BRIDGE`. **Este gate apenas a
especifica.** Ela não foi formalizada, não foi provada e `ASYM-NOGO-001`
não foi aplicado.
