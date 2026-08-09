/-
NS-3 — item do lote Wave-1 (27 itens, `DEC-086`). Rascunho isolado, NÃO
integrado a `TamesisLab.lean`. Segue exatamente a convenção dos arquivos
irmãos desta pasta (`CalderonZygmundKernelDefinitions.lean`,
`ConstantinFeffermanDepletionKernel.lean`, `PressureHessianAlgebra.lean`):
arquivo Lean autônomo, verificado via `lake env lean` diretamente contra
o mesmo projeto Mathlib, fora da árvore de import compartilhada.

## Que frente é esta (e que frente NÃO é)

Linha: Navier-Stokes (Clay oficial) — sub-linha do núcleo de depleção de
Constantin-Fefferman / integrais singulares de Calderón-Zygmund.

Ataque frontal ao núcleo real (3D, contínuo) está bloqueado nesta
biblioteca por falta de infraestrutura de valor principal (p.v.),
decomposição de Calderón-Zygmund e interpolação de Marcinkiewicz (ver
`CalderonZygmundKernelDefinitions.lean`, cabeçalho, para a busca
exaustiva que confirmou essa ausência). Este arquivo NÃO tenta essa
frente. Em vez disso, ataca um objeto genuinamente DIFERENTE, mais
simples: a transformada de Fourier discreta em `ZMod N` (círculo
finito), aplicada a um núcleo-proxy ímpar explícito, como teste de
sanidade mecânico e autocontido da estratégia "núcleo → multiplicador de
Fourier → operador limitado" — SEM nenhuma das peças em falta acima.

Resultado esperado, honestamente enunciado no bloco final "O que NÃO é
afirmado": mesmo um sucesso total aqui não diz NADA sobre o núcleo real
de Constantin-Fefferman, sobre Navier-Stokes, ou mesmo sobre a
transformada de Hilbert contínua (não-periódica). É um objeto clássico
separado da análise harmônica 1D finita/periódica. Seu único valor para
esta linha de pesquisa é como validação de metodologia reutilizável.

## Teste falsificável tentado (versão revisada pelo revisor adversarial)

Teste original proposto: `N = 8`, núcleo-proxy ímpar sawtooth em
`ZMod 8`, calcular `𝓕 k` via `dft` "por decide/norm_num/soma finita
explícita" e comparar com `N = 16` para checar limitação uniforme.

Veredito do revisor adversarial: `NEEDS_NARROWING`. Razão: citações
verificadas exatas (`ZMod.dft`, `ZMod.dft_dft`, `ZMod.dft_odd_iff` em
`Mathlib.Analysis.Fourier.ZMod`; `Complex.cot_series_rep` em
`Mathlib.Analysis.SpecialFunctions.Trigonometric.Cotangent`; ausência de
"periodic/discrete Hilbert transform" ou "conjugate function" em
qualquer lugar do Mathlib, confirmada por grep), mas `ZMod.dft` é
definida via `ZMod.stdAddChar`, ou seja, raízes da unidade genuínas
(`exp(2πi·j/N)`) — não amenizável a `decide` puro (`ℂ` não tem
`DecidableEq` computável relevante aqui); para `N = 8` isso exige
identidades de ângulo especial (múltiplos de `π/4`) ainda não
verificadas. `N = 4` evita esse custo: as únicas raízes envolvidas são
`{1, i, -1, -i}`, todas cobertas por lemas `@[simp]` já presentes no
Mathlib (`Complex.exp_pi_div_two_mul_I`, `Complex.exp_pi_mul_I`, etc.),
então o cálculo genuinamente fecha por `simp`/`norm_num`/reescrita
explícita, sem lemas novos de ângulo especial.

Teste efetivamente tentado aqui (versão revisada, exatamente como
prescrita): fixar `N = 4`, o núcleo-proxy ímpar explícito
`sawtooth N j := if j = 0 then 0 else (N:ℝ)/2 - (j.val:ℝ)` (mesma
fórmula sawtooth do teste original, apenas com `N = 4` em vez de `8`),
calcular `𝓕 (sawtooth 4) k` para os quatro valores de `k : ZMod 4` via
`ZMod.dft_apply` mais reescrita explícita das quatro raízes da unidade
envolvidas, e verificar que os quatro valores obtidos são exatamente
`0, -2i, 0, 2i` — limitados por uma constante (`2`) uniforme nos quatro
casos, exatamente o comportamento "limitado após normalização" previsto
pela teoria clássica (a transformada discreta de um núcleo ímpar tipo
sinal/sawtooth tem magnitude limitada por uma constante independente do
índice de frequência, para `N` fixo). NÃO se tenta `N = 8`, `N = 16`,
nem a cota uniforme-em-`N` geral (isso ficaria para uma frente separada,
autorizada apenas se este teste fechasse — ver bloco final).

## Resultado

FECHOU. Os quatro valores foram calculados explicitamente e verificados
por `lake env lean` com `#print axioms` limpo (apenas
`[propext, Classical.choice, Quot.sound]`) em cada declaração — ver
bloco final do arquivo.
-/

import Mathlib.Analysis.Fourier.ZMod
import Mathlib.Tactic

namespace TamesisNSDiscreteHilbertToySanityCheck

open ZMod Complex

/-! ## Núcleo-proxy ímpar (sawtooth), para `N` geral

Mesma fórmula do teste falsificável original: `sawtooth N j := 0` se
`j = 0`, e `(N:ℝ)/2 - j.val` caso contrário — a versão discreta mais
simples do proxy `1/x`-tipo, mudando de sinal sob `j ↦ -j` (ver
`sawtooth_odd` abaixo), exatamente a estrutura exigida para que
`ZMod.dft_odd_iff` seja aplicável de forma não-vazia. -/

/-- Núcleo-proxy sawtooth ímpar em `ZMod N`: `0` na origem, e
`N/2 - j.val` caso contrário. -/
noncomputable def sawtooth (N : ℕ) [NeZero N] (j : ZMod N) : ℂ :=
  if j = 0 then 0 else (N : ℂ) / 2 - (j.val : ℂ)

/-- **Fato estrutural geral (vale para todo `N`, não só `N=4`)**: `sawtooth
N` é uma função ímpar (`Function.Odd`). Caso `j = 0`: ambos os lados são
`0` triviamente. Caso `j ≠ 0`: usa `ZMod.neg_val` (Mathlib,
`(-j).val = if j = 0 then 0 else N - j.val`) para reduzir a uma
igualdade de naturais subtraídos, fechada por `push_cast`/`ring` usando
`j.val ≤ N` (de `ZMod.val_lt`). Esta é exatamente a hipótese estrutural
citada no teste ("qualquer núcleo tipo p.v. é ímpar") instanciada de
forma concreta e não-vazia para o proxy discreto. -/
theorem sawtooth_odd (N : ℕ) [NeZero N] : Function.Odd (sawtooth N) := by
  intro j
  unfold sawtooth
  by_cases h : j = 0
  · simp [h]
  · have hnj : -j ≠ 0 := neg_ne_zero.mpr h
    rw [if_neg h, if_neg hnj, ZMod.neg_val j, if_neg h]
    have hle : j.val ≤ N := (ZMod.val_lt j).le
    push_cast [Nat.cast_sub hle]
    ring

/-- **Corolário estrutural imediato, citando exatamente `ZMod.dft_odd_iff`
(Mathlib, `Analysis.Fourier.ZMod`, linha 197 na revisão citada pelo
revisor adversarial)**: a DFT de `sawtooth N` é ímpar, para todo `N`.
Vale para todo `N`; a instância concreta `N = 4` abaixo verifica os
valores exatos, que de fato satisfazem esta propriedade (ver
`dft_sawtooth4_one`/`dft_sawtooth4_three` abaixo: `𝓕(1) = -2i`,
`𝓕(3) = 𝓕(-1) = 2i = -𝓕(1)`). -/
theorem dft_sawtooth_odd (N : ℕ) [NeZero N] : Function.Odd (ZMod.dft (sawtooth N)) :=
  ZMod.dft_odd_iff.mpr (sawtooth_odd N)

/-! ## Instância concreta `N = 4` (o teste revisado propriamente dito)

Valores explícitos de `sawtooth 4` nos quatro pontos de `ZMod 4`. -/

theorem sawtooth4_zero : sawtooth 4 0 = 0 := by simp [sawtooth]

theorem sawtooth4_one : sawtooth 4 1 = 1 := by
  unfold sawtooth
  rw [if_neg (by decide)]
  have h : (1 : ZMod 4).val = 1 := by decide
  rw [h]; norm_num

theorem sawtooth4_two : sawtooth 4 2 = 0 := by
  unfold sawtooth
  rw [if_neg (by decide)]
  have h : (2 : ZMod 4).val = 2 := by decide
  rw [h]; norm_num

theorem sawtooth4_three : sawtooth 4 3 = -1 := by
  unfold sawtooth
  rw [if_neg (by decide)]
  have h : (3 : ZMod 4).val = 3 := by decide
  rw [h]; norm_num

/-! ### Os quatro valores do caractere aditivo padrão em `ZMod 4`

`ZMod.stdAddChar j = exp(2π i · j.val / N)`, via `ZMod.stdAddChar_apply`
e `ZMod.toCircle_apply`. Para `N = 4`, os quatro valores são exatamente
as quatro raízes quartas da unidade `1, i, -1, -i`, cada uma fechada por
um lema `@[simp]` já presente no Mathlib
(`Complex.exp_pi_div_two_mul_I`, `Complex.exp_pi_mul_I`,
`Complex.exp_add`) — exatamente o ponto em que o revisor adversarial
identificou que `N = 4` (ao contrário de `N = 8`) não exige nenhuma
identidade de ângulo especial nova. -/

theorem stdAddChar_zero_four : (ZMod.stdAddChar (0 : ZMod 4) : ℂ) = 1 := by simp

theorem stdAddChar_one_four : (ZMod.stdAddChar (1 : ZMod 4) : ℂ) = Complex.I := by
  rw [ZMod.stdAddChar_apply, ZMod.toCircle_apply]
  have hv : (1 : ZMod 4).val = 1 := by decide
  rw [hv]
  norm_num
  rw [show (2 * (Real.pi : ℂ) * I / 4 : ℂ) = (Real.pi / 2 : ℂ) * I by ring]
  simp

theorem stdAddChar_two_four : (ZMod.stdAddChar (2 : ZMod 4) : ℂ) = -1 := by
  rw [ZMod.stdAddChar_apply, ZMod.toCircle_apply]
  have hv : (2 : ZMod 4).val = 2 := by decide
  rw [hv]
  norm_num
  rw [show (2 * (Real.pi : ℂ) * I * 2 / 4 : ℂ) = (Real.pi : ℂ) * I by ring]
  simp

theorem stdAddChar_three_four : (ZMod.stdAddChar (3 : ZMod 4) : ℂ) = -Complex.I := by
  rw [ZMod.stdAddChar_apply, ZMod.toCircle_apply]
  have hv : (3 : ZMod 4).val = 3 := by decide
  rw [hv]
  norm_num
  rw [show (2 * (Real.pi : ℂ) * I * 3 / 4 : ℂ)
      = (Real.pi : ℂ) * I + (Real.pi / 2 : ℂ) * I by ring]
  rw [Complex.exp_add]
  simp

/-! ### Expansão explícita da soma finita que define `𝓕 (sawtooth 4)`

`Finset.univ : Finset (ZMod 4)` é reescrito para `{0,1,2,3}` (por
`decide`, `ZMod 4` tem `DecidableEq` computável) e a soma de quatro
termos é expandida via `Finset.sum_insert`/`Finset.sum_singleton` — a
"soma finita explícita" citada no teste, sem `decide` sobre valores
complexos (que não é viável, ver nota do cabeçalho). -/

theorem huniv4 : (Finset.univ : Finset (ZMod 4)) = {0, 1, 2, 3} := by decide

theorem dft_sawtooth4_apply (k : ZMod 4) :
    ZMod.dft (sawtooth 4) k
      = ZMod.stdAddChar (-((0 : ZMod 4) * k)) * sawtooth 4 0
        + ZMod.stdAddChar (-((1 : ZMod 4) * k)) * sawtooth 4 1
        + ZMod.stdAddChar (-((2 : ZMod 4) * k)) * sawtooth 4 2
        + ZMod.stdAddChar (-((3 : ZMod 4) * k)) * sawtooth 4 3 := by
  rw [ZMod.dft_apply, huniv4]
  simp only [smul_eq_mul]
  rw [Finset.sum_insert (by decide), Finset.sum_insert (by decide),
    Finset.sum_insert (by decide), Finset.sum_singleton]
  ring

/-! ## Os quatro valores exatos de `𝓕 (sawtooth 4)`

O núcleo central do teste falsificável: os quatro valores calculados
mecanicamente abaixo. -/

/-- `𝓕 (sawtooth 4) 0 = 0`. -/
theorem dft_sawtooth4_zero : ZMod.dft (sawtooth 4) 0 = 0 := by
  rw [dft_sawtooth4_apply, sawtooth4_zero, sawtooth4_one, sawtooth4_two, sawtooth4_three]
  simp

/-- `𝓕 (sawtooth 4) 1 = -2i`. -/
theorem dft_sawtooth4_one : ZMod.dft (sawtooth 4) 1 = -2 * Complex.I := by
  rw [dft_sawtooth4_apply]
  rw [show (-((0 : ZMod 4) * (1 : ZMod 4)) : ZMod 4) = (0 : ZMod 4) by decide,
      show (-((1 : ZMod 4) * (1 : ZMod 4)) : ZMod 4) = (3 : ZMod 4) by decide,
      show (-((2 : ZMod 4) * (1 : ZMod 4)) : ZMod 4) = (2 : ZMod 4) by decide,
      show (-((3 : ZMod 4) * (1 : ZMod 4)) : ZMod 4) = (1 : ZMod 4) by decide]
  rw [sawtooth4_zero, sawtooth4_one, sawtooth4_two, sawtooth4_three,
    stdAddChar_zero_four, stdAddChar_three_four, stdAddChar_two_four, stdAddChar_one_four]
  ring

/-- `𝓕 (sawtooth 4) 2 = 0`. -/
theorem dft_sawtooth4_two : ZMod.dft (sawtooth 4) 2 = 0 := by
  rw [dft_sawtooth4_apply]
  rw [show (-((0 : ZMod 4) * (2 : ZMod 4)) : ZMod 4) = (0 : ZMod 4) by decide,
      show (-((1 : ZMod 4) * (2 : ZMod 4)) : ZMod 4) = (2 : ZMod 4) by decide,
      show (-((2 : ZMod 4) * (2 : ZMod 4)) : ZMod 4) = (0 : ZMod 4) by decide,
      show (-((3 : ZMod 4) * (2 : ZMod 4)) : ZMod 4) = (2 : ZMod 4) by decide]
  rw [sawtooth4_zero, sawtooth4_one, sawtooth4_two, sawtooth4_three,
    stdAddChar_zero_four, stdAddChar_two_four]
  ring

/-- `𝓕 (sawtooth 4) 3 = 2i`. -/
theorem dft_sawtooth4_three : ZMod.dft (sawtooth 4) 3 = 2 * Complex.I := by
  rw [dft_sawtooth4_apply]
  rw [show (-((0 : ZMod 4) * (3 : ZMod 4)) : ZMod 4) = (0 : ZMod 4) by decide,
      show (-((1 : ZMod 4) * (3 : ZMod 4)) : ZMod 4) = (1 : ZMod 4) by decide,
      show (-((2 : ZMod 4) * (3 : ZMod 4)) : ZMod 4) = (2 : ZMod 4) by decide,
      show (-((3 : ZMod 4) * (3 : ZMod 4)) : ZMod 4) = (3 : ZMod 4) by decide]
  rw [sawtooth4_zero, sawtooth4_one, sawtooth4_two, sawtooth4_three,
    stdAddChar_zero_four, stdAddChar_one_four, stdAddChar_two_four, stdAddChar_three_four]
  ring

/-- **Fechamento do teste falsificável**: os quatro valores de
`𝓕 (sawtooth 4)` são uniformemente limitados por `2` — o comportamento
"limitado, independente do índice de frequência `k`" previsto pela
teoria clássica (para `N` fixo). Combina os quatro valores exatos
acima; a disjunção de casos sobre `k : ZMod 4` é decidida por `decide`
(tipo finito, proposição sobre igualdade decidível), não sobre os
valores complexos em si. -/
theorem norm_dft_sawtooth4_le (k : ZMod 4) : ‖ZMod.dft (sawtooth 4) k‖ ≤ 2 := by
  have hk : k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 := by revert k; decide
  rcases hk with hk | hk | hk | hk <;> subst hk
  · rw [dft_sawtooth4_zero]; norm_num
  · rw [dft_sawtooth4_one]; simp
  · rw [dft_sawtooth4_two]; norm_num
  · rw [dft_sawtooth4_three]; simp

end TamesisNSDiscreteHilbertToySanityCheck

/-! ## O que NÃO é afirmado

```text
NÃO prova nada sobre o núcleo real de Constantin-Fefferman em ℝ³
NÃO prova nada sobre a integral p.v. (2.1)/(2.2), nem sobre limitação de
  operadores integrais singulares reais
NÃO prova NS-GAP-001/004 nem qualquer regularidade condicional real
NÃO prova nada sobre a transformada de Hilbert CONTÍNUA (não-periódica)
NÃO estabelece a cota uniforme-em-N (`N = 8`, `N = 16`, ou geral) —
  essa é uma frente FUTURA, separada, que ficaria licenciada por este
  resultado mas não é tentada aqui (ver nota do cabeçalho sobre o
  veredito do revisor adversarial)
NÃO usa `Complex.cot_series_rep` (Mittag-Leffler da cotangente) — essa
  identidade só entraria na etapa de `N` geral/uniforme, fora do escopo
  deste teste estreito
NÃO afirma que Navier-Stokes ficou alcançável
NÃO afirma novidade matemática — os quatro valores calculados são um
  exercício de álgebra elementar de raízes da unidade, o valor está
  inteiramente na verificação mecânica ponta-a-ponta dentro deste
  snapshot do Mathlib, não no resultado numérico em si
```

O que este arquivo estabelece, com honestidade: (1) o núcleo-proxy
`sawtooth N` é estruturalmente ímpar para todo `N` (`sawtooth_odd`), o
que instancia de forma não-vazia a hipótese "núcleo tipo p.v. é ímpar"
citada no teste original; (2) para `N = 4`, os quatro valores exatos de
sua DFT foram calculados mecanicamente (`0, -2i, 0, 2i`) e são
uniformemente limitados por `2` (`norm_dft_sawtooth4_le`) — exatamente
o resultado que o teste falsificável revisado pedia, sem precisar de
nenhuma peça da infraestrutura de CZ/p.v./dyadic ausente do Mathlib. O
resultado é POSITIVO neste sentido estreito: licencia (mas não realiza)
investir na etapa seguinte de `N` geral/uniforme, citada no cabeçalho e
no teste original como próximo passo, usando possivelmente
`Complex.cot_series_rep`.
-/

#print axioms TamesisNSDiscreteHilbertToySanityCheck.sawtooth_odd
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth_odd
#print axioms TamesisNSDiscreteHilbertToySanityCheck.sawtooth4_zero
#print axioms TamesisNSDiscreteHilbertToySanityCheck.sawtooth4_one
#print axioms TamesisNSDiscreteHilbertToySanityCheck.sawtooth4_two
#print axioms TamesisNSDiscreteHilbertToySanityCheck.sawtooth4_three
#print axioms TamesisNSDiscreteHilbertToySanityCheck.stdAddChar_zero_four
#print axioms TamesisNSDiscreteHilbertToySanityCheck.stdAddChar_one_four
#print axioms TamesisNSDiscreteHilbertToySanityCheck.stdAddChar_two_four
#print axioms TamesisNSDiscreteHilbertToySanityCheck.stdAddChar_three_four
#print axioms TamesisNSDiscreteHilbertToySanityCheck.huniv4
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth4_apply
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth4_zero
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth4_one
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth4_two
#print axioms TamesisNSDiscreteHilbertToySanityCheck.dft_sawtooth4_three
#print axioms TamesisNSDiscreteHilbertToySanityCheck.norm_dft_sawtooth4_le
