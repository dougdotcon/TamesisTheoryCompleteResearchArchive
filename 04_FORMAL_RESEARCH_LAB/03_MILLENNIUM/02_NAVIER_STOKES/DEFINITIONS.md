# Definições

status: `PARTIALLY_FORMALIZED` (matemática clássica definida em prosa;
nada disto foi formalizado em Lean nesta rodada além do fragmento de
álgebra linear em `FORMAL/PressureHessianAlgebra.lean`).

Estas definições seguem a literatura padrão (ver `REVIEWS/AUDIT_REPORT.md`
para as fontes verificadas). Onde o documento legado usa notação
própria, o enunciado clássico é dado ao lado, conforme exigido por
`AGENTS.md`.

## Sistema

Navier–Stokes incompressível em `ℝ³` (ou `𝕋³`), sem forçante externo,
enunciado clássico do CMI (Clay Mathematics Institute):

```
∂u/∂t + (u·∇)u = -∇p + ν Δu ,     ∇·u = 0 ,     u(·,0) = u₀
```

## Solução fraca de Leray–Hopf

`u ∈ L∞(0,T; L²) ∩ L²(0,T; H¹)` satisfazendo a formulação fraca das
equações acima com a desigualdade de energia; existência global para
`u₀ ∈ L²` provada por Leray (1934) — ver referência verificada em
`REVIEWS/AUDIT_REPORT.md`. Unicidade e suavidade global em 3D
permanecem em aberto; é exatamente o problema do Milênio.

## Solução forte / suave

`u` suave em `[0,T)` (localmente em espaço, ou globalmente se o domínio
é periódico/todo o espaço com decaimento adequado). Toda solução forte
é fraca; a questão de blow-up é sobre até quando a solução forte pode
ser continuada.

## Vorticidade

`ω := ∇ × u` (rotacional do campo de velocidade).

## Gradiente de velocidade, decomposição strain/rotation

`M := ∇u` (matriz jacobiana, `M_ij = ∂u_i/∂x_j`).
`A := (M + Mᵀ)/2` — parte simétrica ("rate-of-strain tensor"), sem
traço por incompressibilidade (`tr A = ∇·u = 0`).
`Ω := (M - Mᵀ)/2` — parte antissimétrica ("rotation tensor"), associada
ao vetor de vorticidade via `Ω x = (ω/2) × x` (convenção; fatores de 2
variam entre autores — usar consistentemente).

## Autovalores/autovetores da taxa de deformação

`A` é simétrica real 3×3 ⟹ diagonalizável com autovalores reais
`λ_min ≤ λ_mid ≤ λ_max` (com `λ_min + λ_mid + λ_max = 0` por
incompressibilidade) e autovetores ortonormais `e_min, e_mid, e_max`.
No documento legado, `e₁ := e_max` (autovetor do maior autovalor,
direção "mais extensional").

## Cosseno de alinhamento

`α₁ := cos²(ω, e₁) = ⟨ω̂, e₁⟩²`, onde `ω̂ = ω/|ω|`. Quantidade
adimensional em `[0,1]`; `α₁=1` significa vorticidade perfeitamente
alinhada com `e₁`.

## Hessiano de pressão

`H_p := ∇²p` (matriz de derivadas segundas da pressão). Via divergente
da equação de momento e incompressibilidade:

```
-Δp = tr(M²) = tr(A²) + tr(Ω²)         (verificado algebricamente
                                          nesta sessão, ver
                                          FORMAL/PressureHessianAlgebra.lean
                                          e COMPUTATION/restricted_euler.py)
```

`H_p` se decompõe em parte isotrópica `(Δp/3) I` (local, dada pela
identidade acima) e parte anisotrópica sem traço `H_p - (Δp/3)I` — esta
última é **não-local**: dada por uma integral singular (tipo
Biot–Savart/Riesz) do campo de deformação sobre todo o domínio, não uma
função pontual de `A(x)`, `ω(x)`. Este é o objeto central e não
resolvido da hipótese sob auditoria.

## Critério de Beale–Kato–Majda (BKM)

Solução suave em `[0,T)` deixa de existir suavemente em `T` se e
somente se `∫₀ᵀ ‖ω(·,t)‖_∞ dt = ∞`. Ver referência verificada em
`REVIEWS/AUDIT_REPORT.md`.

## "Alignment Gap" (hipótese sob auditoria, linguagem Tamesis — NÃO um
   enunciado clássico da literatura)

`⟨α₁⟩_Ω ≤ 1 - δ₀` para algum `δ₀ > 0` fixo, uniformemente ao longo do
tempo, em regiões de vorticidade intensa `Ω = {x : |ω(x)| > \text{limiar}}`.
Este enunciado é próprio do documento legado
(`ANALISE_CRITICA_NS.md`), não uma citação da literatura padrão; ver
`ASSUMPTIONS.md` e `REVIEWS/AUDIT_REPORT.md` para a distinção entre o
que é citação recuperável e o que é formulação interna.
