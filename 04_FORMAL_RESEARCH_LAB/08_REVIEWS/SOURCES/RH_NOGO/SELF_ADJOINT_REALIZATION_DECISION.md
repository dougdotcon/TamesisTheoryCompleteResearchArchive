# Auto-adjunção — decisão sobre a hipótese mínima

## Distinção exigida pelo gate

| Noção | Significado | Nas fontes obtidas |
|---|---|---|
| `formal_self_adjointness` | `⟨Pu,v⟩ = ⟨u,Pv⟩` para `u,v ∈ C_0^∞` | Hörmander p. 193: `P` com domínio `C_0^∞(Ω)` é **simétrico** |
| `symmetric_minimal_operator` | o fecho de `P|_{C_0^∞}` | implícito em Hörmander |
| `essential_self_adjointness` | o operador mínimo é auto-adjunto (extensão **única**) | **não aparece em nenhuma fonte obtida** |
| `chosen_self_adjoint_realization` | escolhe-se uma extensão auto-adjunta | **Hörmander p. 193** |
| `Friedrichs_extension` | a extensão canônica de um operador semilimitado | **Hörmander p. 193**, explicitamente |
| `positive_self_adjoint_operator` | operador auto-adjunto com espectro em `(0,∞)` | **Coriasco–Doll p. 1** ("self-adjoint positive operator") |

Citação decisiva (Hörmander 1968, p. 193):

> *"the operator `P` with domain `C_0^∞(Ω)` is symmetric, and by a classical
> theorem of Friedrichs it has **at least one** self-adjoint extension `P̄`
> with a positive lower bound `c`. Let `{E_λ}` be the spectral resolution
> of **such an** extension."*

O artigo **não** afirma unicidade e trabalha com uma extensão escolhida.

## Hipótese mínima necessária para o no-go

O argumento assintótico consome apenas:

1. um operador **auto-adjunto** (para existir resolução espectral `{E_λ}`);
2. **positividade** (para o espectro estar em `(0,∞)` e a contagem em
   `[0,Λ)` fazer sentido);
3. **espectro discreto** com multiplicidade finita (para `N_P(Λ)` estar
   definida e ser finita).

Ele **não** consome:

- unicidade da extensão auto-adjunta;
- essencial auto-adjunção do operador mínimo;
- qualquer afirmação sobre *todas* as realizações possíveis.

## Decisão

```text
positive_self_adjoint_operator  (uma realizacao escolhida)
```

Resultado registrado, na forma que o gate previu — e que as fontes de fato
sustentam:

> o argumento assintótico necessita de uma realização auto-adjunta com
> espectro e função de contagem definidos; não necessita provar essencial
> auto-adjunção de toda realização possível.

Isto **não foi forçado**: é literalmente a hipótese de Coriasco–Doll
("self-adjoint positive operator") e é compatível com a construção de
Hörmander (extensão de Friedrichs escolhida).

## Consequência para o enunciado do no-go

O no-go, quando for enunciado, deve dizer **qual realização**. A forma
correta é quantificar sobre realizações:

```text
Para toda realizacao auto-adjunta positiva P de um operador
pseudodiferencial classico eliptico de ordem m > 0 sobre M compacta,
o espectro de P nao coincide com {gamma_n}.
```

e não

```text
O operador P (essencialmente auto-adjunto) nao tem espectro {gamma_n}.
```

A primeira forma é **mais forte** (cobre todas as realizações) e **melhor
sustentada** (cada realização satisfaz as hipóteses da fonte). GAP-RH-010
fica fechado por reformulação.
