---
document_id: PORTFOLIO-REVIEW-CF-DEPLETION-KERNEL-2026-08-09
reviewed_at: 2026-08-09
conclusion: FOUND-CF-DEPLETION-KERNEL-001_AUTHORIZED
---

# Revisão de portfólio — núcleo de depleção geométrica de Constantin-Fefferman

## Contexto

Pedido explícito do usuário: reavaliar a estrutura de governança para
continuar atacando, com liberdade para registrar frente nova por conta
própria, desde que fundamentada em fontes reais — não na numerologia do
corpus Tamesis mais amplo. Uma exploração completa de cinco clusters do
corpus Tamesis (`01_TAMESIS_CORE`, `90_LEGACY`, `RECURSOS_PARA_PESQUISA`)
não encontrou nenhum conteúdo de análise harmônica/Calderón-Zygmund
utilizável — ver `09_SESSIONS/2026/` para o relatório completo dessa
exploração. A direção escolhida pelo usuário foi: formalizar
Constantin-Fefferman 1993, um resultado real e citável da literatura.

## O que Constantin-Fefferman 1993 realmente diz

**Fonte primária**: P. Constantin, C. Fefferman, "Direction of vorticity
and the problem of global regularity for the Navier-Stokes equations",
*Indiana Univ. Math. J.* 42 (1993), 775-789.

**Enunciado** (restatado com números de equação em Siran Li, "On Vortex
Alignment and Boundedness of L^q Norm of Vorticity", *Acta Math. Sci.*
40(6) (2020), 1700-1708, arXiv:1712.00551, eq. 1.7/1.9): se existem
`Λ, ρ > 0` tais que `|sin φ(t,x,y)| ≤ |x-y|/ρ` sempre que
`|ω(t,x)|, |ω(t,y)| ≥ Λ` (φ = ângulo entre os vetores de vorticidade em
x e y), então uma solução fraca em `[0,T]` é necessariamente uma solução
clássica em `[0,T]`.

**Por que NÃO vamos tentar o teorema completo**: a prova exige teoria
completa de soluções fracas de Leray-Hopf, estimativas de energia/
enstrofia, limitação de operadores integrais singulares em espaços
`L^p`, e a passagem de um limite `L^∞` na vorticidade para regularidade
clássica. Isso está muito além do escopo tratável nesta sessão — seria
exatamente o tipo de tentativa forçada que a governança deste
laboratório proíbe.

## O que VAMOS formalizar: o núcleo algébrico da depleção

O mecanismo geométrico central (Li 2020, eq. 2.1-2.3, citando
Constantin 1994 para a representação integral original):

```text
S(t,x) = (3/8π) p.v. ∫ { (x̂-y)⊗((x̂-y)×ω(t,x)) + ((x̂-y)×ω(t,x))⊗(x̂-y) }
           / |x-y|³  dy                                          (2.1)

S : (ω̂⊗ω̂)(t,x) = (3/4π) p.v. ∫ D(x̂-y, ω̂(t,x), ω̂(t,x-y)) |ω(t,x-y)|
                     / |x-y|³  dy                                 (2.2)

D(e1,e2,e3) := (e1·e3) · det(e1,e2,e3)                            (2.3)
```

`D` é um objeto puramente algébrico (função de três vetores em ℝ³) —
**nenhuma integral singular, nenhuma teoria de solução fraca é
necessária para estudá-lo isoladamente**. Ele é exatamente o mesmo tipo
de "núcleo algébrico dentro de uma estimativa maior" que
`PressureHessianAlgebra.lean` já tratou nesta sessão (`tr(AΩ)=0`).

**Alvo desta frente**: provar formalmente, para `D` como definido acima:

```text
1. D(e1, e2, e2) = 0 -- depleção EXATA quando as direções coincidem
   (determinante com duas colunas iguais).
2. Uma cota quantitativa |D(e1,e2,e3)| <= C * ‖e2 - e3‖ para vetores
   unitarios e1,e2,e3 -- conectando diretamente a hipotese de Lipschitz
   |sin φ| <= |x-y|/ρ do teorema real: quando a direção da vorticidade
   varia pouco (‖e2-e3‖ pequeno), o núcleo de estiramento D também é
   pequeno, mesmo antes de qualquer análise da integral.
```

## O que isso NÃO é

```text
NÃO é uma prova do teorema de Constantin-Fefferman
NÃO prova nada sobre a integral p.v. (2.1)/(2.2) em si, nem sobre
  limitação de operadores integrais singulares
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO afirma que Navier-Stokes ficou alcançável
```

O que fica registrado como gap real e nomeado: a passagem de "D é
pequeno pontualmente" para "a integral p.v. de D contra o núcleo
1/|x-y|³ é controlada" é o passo de análise harmônica genuíno que falta
— e é precisamente NS-GAP-001/004 na sua forma mais precisa. Esta
frente NÃO fecha esse gap; nomeia com mais precisão onde ele está.

## Revisão de governança (pedida explicitamente)

O `stop_condition` de `NS-PRESSURE-001`/`NS-GAP-001` continua proibindo
qualquer tentativa da estimativa não-local completa. Esta frente é
**explicitamente autorizada como exceção nomeada**: reproduzir uma
identidade algébrica de uma fonte publicada e citada, sem estender além
do que a fonte já estabelece.

## Trava

`authorized_action: FORMALIZATION`.
