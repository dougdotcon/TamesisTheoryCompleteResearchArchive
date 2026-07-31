---
class_id: W-POWER
kind: abstract-asymptotic-class
depends_on_PDE: false
---

# Classe W-POWER — classe assintótica abstrata

## Definição

Um **dado de contagem de potência** é uma tripla `(N, α, C)` com

```text
N : ℝ → ℝ        função de contagem
α > 0            expoente
C > 0            constante
```

satisfazendo

```text
N(Λ) / Λ^α  →  C     quando Λ → +∞.
```

Dizemos que um objeto espectral **pertence a W-POWER** quando sua função de
contagem admite tal tripla.

## O que W-POWER NÃO exige

```text
PDE
elipticidade
variedade
símbolo principal
auto-adjunção
fibrado
operador de qualquer espécie
```

`N` é uma função real arbitrária. Nenhuma estrutura geométrica ou
analítica é pressuposta.

## Relação com ASYM-NOGO-001

O lema já verificado em Lean
(`05_FORMAL/lean/TamesisLab/RHNogo/AsymptoticCore/`) tem exatamente esta
forma:

```lean
theorem asym_nogo_001 (N : ℝ → ℝ) (α c C : ℝ)
    (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
    (hTLog : Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c))
    (hPower : Tendsto (fun T => N T / T ^ α) atTop (nhds C)) : False
```

A hipótese `hPower` **é** a pertinência a W-POWER. A hipótese `hTLog` é a
segunda normalização, por `Λ log Λ`.

Registro exigido pelo gate:

```text
ASYM-NOGO-001 aplica-se diretamente a W-POWER quando uma segunda
normalização positiva por Λ log Λ é assumida.
```

**Esta aplicação NÃO foi executada neste gate.**

## Papel arquitetural

W-POWER é a interface que isola o núcleo formal já verificado de qualquer
lacuna de EDP. Uma eventual falha, estreitamento ou reformulação da classe
geométrica não afeta `ASYM-NOGO-001`, porque o lema nunca menciona
operadores.

```text
operador geométrico  ⟹  lei de potência  ⟹  lema assintótico
   (W-ELLIPTIC)          (W-POWER)           (ASYM-NOGO-001, VERIFIED)
```

A inclusão `W-ELLIPTIC ⊆ W-POWER` é o objeto de
`HORMANDER_LOCAL_TO_GLOBAL_BRIDGE.md` e permanece **não formalizada**.
