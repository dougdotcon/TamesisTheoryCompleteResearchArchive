/-
HG-1G (Wave 5, item WAVE5-HG-1G) — parametrizar totalmente sobre `a0` a
identidade "Num/Den" de HG-1F (`principalCycle_f = principalCycle_Num -
principalCycle_Den`, para o par FIXO `Num.a0 = 3`/`Den.a0 = 2`), reusando
`genf`/`finite_support_ord_genf`/`principalCycle_a0`, JÁ parametrizados por
`(a0 : ℤ) (ha0 : a0 ≠ 0)`, de HG-1E (rascunho formal isolado, NÃO integrado
a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. Todas as
declarações novas verificadas com o comando de impressão de dependências de
prova do Lean: dependem apenas de `[propext, Classical.choice, Quot.sound]`
— nenhum marcador de prova incompleta escapou pela síntese de instâncias. O
arquivo não contém nenhuma prova incompleta, nenhuma declaração local
tomada como verdade sem prova, e nenhum bloco marcado como inseguro, em
nenhum lugar (conferido por busca textual nesta sessão).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta
rodada: não tocar em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer
parte da máquina de teoria de Hodge necessária para ela. O conteúdo abaixo
é 100% álgebra comutativa/geometria de esquemas clássica: NADA aqui usa
estrutura complexa, cohomologia, decomposição de Hodge, ou classe de ciclo
em cohomologia. Mesmo em caso de sucesso total, o resultado permanece a
várias camadas inteiramente ausentes de sequer enunciar formalmente Hodge
(1,1), quanto mais a conjectura geral. Este item não afirma nenhuma
novidade matemática: "divisor de um quociente = divisor do numerador menos
divisor do denominador" é clássico (ver, e.g., Hartshorne II.6); o que está
formalizado aqui é apenas essa identidade pontual, agora para QUAISQUER
`a0, b0 : ℤ` não-nulos (não apenas o par fixo `3, 2` de HG-1b/HG-1F),
reempacotada no tipo `AlgebraicCycle` de Mathlib.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1g, especificado (após revisão
adversarial na etapa de planejamento da Onda 5) como:

  Generalizar `principalCycle_f_eq_sub` sobre a base já parametrizada de
  HG-1E (`a0 : ℤ`, `ha0 : a0 ≠ 0`) em vez do par fixo `Num.a0 = 3`/
  `Den.a0 = 2`, reusando `genf`/`finite_support_ord_genf` parametrizados.

RESULTADO: SUCESSO. Mecânico dado HG-1E/HG-1F já fechados — nenhum lema
novo de Mathlib além dos já citados em HG-1E/HG-1F foi necessário. A única
observação estrutural nova (não uma técnica de prova nova) é que, ao
parametrizar sobre `a0` GENÉRICO, o "numerador" e o "denominador" deixam de
precisar de duas construções `AlgebraicCycle` distintas (`principalCycle_Num`/
`principalCycle_Den` de HG-1F, cada uma copiando o mesmo padrão de três
campos para um valor fixo diferente): ambos são agora a MESMA função
`principalCycle_a0`, já definida e provada em HG-1E, apenas avaliada em dois
argumentos `a0`/`b0` distintos — `principalCycle_a0 a0 ha0` e
`principalCycle_a0 b0 hb0`. Isso elimina a duplicação de HG-1F em vez de
apenas parametrizá-la.

## O que realmente fechou o teste

**Inlining verbatim de HG-1C/HG-1E.** Todo o bloco de HG-1E
(`HG1EPrincipalCycleA0Probe.lean`, mesmo diretório), de `import Mathlib` até
`end AlgebraicGeometry.HG1C` (incluindo a seção `noncomputable section` com
`genf`, `finite_support_ord_genf`, `principalCycle_a0`, e a seção
`Instantiation`), foi copiado byte-idêntico para este arquivo nesta sessão
(diretamente do arquivo-fonte, não de memória nem paráfrase) — mesmo motivo
mecânico já documentado nos preâmbulos de HG-1D/HG-1E/HG-1F: este arquivo,
como HG-1E, vive em `03_MILLENNIUM/05_HODGE/FORMAL/`, fora da raiz de
módulos do pacote Lake (confirmado nesta sessão por reinspeção de
`05_FORMAL/lean/lakefile.toml` e `05_FORMAL/lean/TamesisLab.lean`, nenhuma
mudança desde a verificação de HG-1F), logo não há caminho de `import` de
um arquivo solto para outro; a única forma de reusar `genf`/
`finite_support_ord_genf`/`principalCycle_a0`/etc. aqui é reproduzir o
texto. Reusar o mesmo nome de namespace (`AlgebraicGeometry.HG1C`) num
arquivo novo, não importado pelo original, não causa nenhum conflito de
compilação — mesmo padrão já usado com sucesso por HG-1E/HG-1F (que reusam
`AlgebraicGeometry.HG1C`/`AlgebraicGeometry.HG1B` como nomes de namespace em
arquivos novos).

**As declarações genuinamente novas — `f_ab`, `finite_support_ord_f_ab`,
`principalCycle_f_ab`, `principalCycle_f_ab_eq_sub`.** Tudo parametrizado
sobre DOIS `a0 b0 : ℤ` (em vez do par fixo `Num.a0 = 3`/`Den.a0 = 2` de
HG-1F), usando diretamente `genf`/`genf_ne_zero`/`finite_support_ord_genf`/
`principalCycle_a0` de HG-1E — nenhuma redefinição, nenhum novo argumento de
prova além de reindexar `Num.a0 ↦ a0`, `Den.a0 ↦ b0`:

```
def f_ab (a0 b0 : ℤ) : testScheme.functionField := genf a0 / genf b0

theorem finite_support_ord_f_ab (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    (Function.support (fun x : testScheme => testScheme.ord (f_ab a0 b0) x)).Finite := ...

def principalCycle_f_ab (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    AlgebraicCycle testScheme ℤ where ...

theorem principalCycle_f_ab_eq_sub (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    principalCycle_f_ab a0 b0 ha0 hb0 = principalCycle_a0 a0 ha0 - principalCycle_a0 b0 hb0 := ...
```

O padrão de prova de `finite_support_ord_f_ab` é EXATAMENTE o de
`finite_support_ord_f` (HG-1b/HG-1F), com `Num.a0 ↦ a0`, `Den.a0 ↦ b0`,
`Num.algebraMap_eq_genf`/`Num.genf_ne_zero` ↦ `genf_ne_zero a0 ha0`, etc.: a
mesma identidade-chave `f_ab a0 b0 * genf b0 = genf a0` (aqui por
`div_mul_cancel₀`, já que `f_ab` é *definido* como `genf a0 / genf b0`, sem
precisar do desvio por `algebraMap`/`f_eq_div` de HG-1F), e a mesma inclusão
de suporte via `Scheme.ord_mul`, `Function.mem_support`, `Set.mem_union`,
fechada por `Set.Finite.union`/`Set.Finite.subset`.

O padrão de prova de `principalCycle_f_ab_eq_sub` é EXATAMENTE o de
`principalCycle_f_eq_sub` (HG-1f): `Function.locallyFinsuppWithin.ext`
reduz a um objetivo pontual; `Function.locallyFinsuppWithin.coe_sub` +
`Pi.sub_apply` (ambos `simp only`) desdobram o lado direito da subtração de
ciclos; `show` reafirma o objetivo em termos de `testScheme.ord`
(desdobramento definicional de `principalCycle_f_ab`/`principalCycle_a0`,
mesmo truque já usado em HG-1f); `omega` fecha o rearranjo aritmético final
a partir de `hord : ord (f_ab a0 b0) x + ord (genf b0) x = ord (genf a0) x`
(a mesma identidade pontual de `Scheme.ord_mul`, aqui aplicada a `genf a0`/
`genf b0` em vez de `algebraMap ℤ testScheme.functionField Num.a0`/`Den.a0`
— equivalentes por `algebraMap_eq_genf`, mas usar `genf` direto evita esse
passo extra de reescrita e casa diretamente com o `toFun` de
`principalCycle_a0`).

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1C/HG-1E já estavam
verificados nos preâmbulos daqueles arquivos (mesmo diretório) — não
repetidos aqui por brevidade. Adicionalmente, para `f_ab`/
`finite_support_ord_f_ab`/`principalCycle_f_ab`/`principalCycle_f_ab_eq_sub`
— mesmos nomes já citados e reconferidos nos preâmbulos de HG-1E/HG-1F,
aqui reusados sem alteração de assinatura:
  - `AlgebraicGeometry.AlgebraicCycle`, campos `toFun`, `supportWithinDomain'`,
    `supportLocallyFiniteWithinDomain'` (`Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`).
  - `Filter.univ_mem` (`Mathlib/Order/Filter/Basic.lean`).
  - `Function.locallyFinsuppWithin.ext`, `.coe_sub`
    (`Mathlib/Topology/LocallyFinsupp.lean`, mesmas linhas já citadas no
    preâmbulo de HG-1F).
  - `Pi.sub_apply` (`Mathlib/Algebra/Group/Pi/Basic.lean`).
  - `Scheme.ord_mul` (`AlgebraicGeometry/OrderOfVanishing.lean:81-82`) —
    incondicional em `x`, já reconferido em HG-1F.
  - `div_mul_cancel₀` (Mathlib, lema padrão de corpo/`GroupWithZero`, já
    usado em HG-1F para `f_eq_div`/`div_mul_cancel₀`).
  - `Set.Finite.union`, `Set.Finite.subset` (Mathlib, `Data/Set/Finite/Basic.lean`,
    já usados implicitamente em HG-1b/HG-1F via o mesmo padrão de prova).
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de
saída `0`) e por busca textual (zero ocorrências dos marcadores proibidos
pela governança do laboratório).
-/

import Mathlib

open AlgebraicGeometry CategoryTheory

namespace AlgebraicGeometry.HG1C

noncomputable section

/-! ## Configuração concreta: `X = Spec ℤ` (mesma escolha de HG-1/HG-1b/HG-1C/HG-1E) -/

/-- Anel de teste: `ℤ`. -/
abbrev testRing : CommRingCat := CommRingCat.of ℤ

/-- Esquema de teste: `Spec ℤ`. -/
abbrev testScheme : Scheme.{0} := Spec testRing

instance : Nonempty (⊤ : testScheme.Opens) := ⟨⟨genericPoint testScheme, trivial⟩⟩

/-! ## Passo 1 — compatibilidade `algebraMap`/`germToFunctionField` (reproduzido de
HG-1b/HG-1C/HG-1E, `algebraMap_eq_germToFunctionField`; independe de `a0`). -/

lemma algebraMap_eq_germToFunctionField (x : ℤ) :
    algebraMap ℤ testScheme.functionField x =
      testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x) := by
  have h : (algebraMap ℤ testScheme.functionField) =
      (testScheme.germToFunctionField ⊤).hom.comp (Scheme.ΓSpecIso testRing).inv.hom :=
    Subsingleton.elim _ _
  exact DFunLike.congr_fun h x

/-! ## Passo 2 — o argumento de finitude de HG-1C, parametrizado sobre
`(a0 : ℤ) (ha0 : a0 ≠ 0)` explícitos como argumentos comuns (reproduzido byte-idêntico
de HG-1C/HG-1E — ver preâmbulos daqueles arquivos para a discussão de por que `a0`/`ha0`
são argumentos explícitos comuns, não `variable`/`instance` de seção). -/

/-- `a0` visto como seção global de `testScheme`. -/
def aSec (a0 : ℤ) : Γ(testScheme, ⊤) := (Scheme.ΓSpecIso testRing).inv a0

lemma aSec_ne_zero (a0 : ℤ) (ha0 : a0 ≠ 0) : aSec a0 ≠ (0 : Γ(testScheme, ⊤)) := by
  simp only [aSec]
  intro h
  exact ha0 (by simpa using congrArg (Scheme.ΓSpecIso testRing).hom h)

/-- Germe de `aSec a0` no ponto genérico. -/
def genf (a0 : ℤ) : testScheme.functionField := testScheme.germToFunctionField ⊤ (aSec a0)

lemma algebraMap_eq_genf (a0 : ℤ) : algebraMap ℤ testScheme.functionField a0 = genf a0 :=
  algebraMap_eq_germToFunctionField a0

lemma genf_ne_zero (a0 : ℤ) (ha0 : a0 ≠ 0) : genf a0 ≠ 0 := by
  have hinj := testScheme.germToFunctionField_injective (⊤ : testScheme.Opens)
  simp only [genf]
  intro h
  exact aSec_ne_zero a0 ha0 ((map_eq_zero_iff _ hinj).mp h)

lemma genericPoint_mem_basicOpen (a0 : ℤ) (ha0 : a0 ≠ 0) :
    genericPoint testScheme ∈ testScheme.basicOpen (aSec a0) := by
  rw [Scheme.mem_basicOpen_top, isUnit_iff_ne_zero]
  exact genf_ne_zero a0 ha0

/-- A instância `Nonempty (testScheme.basicOpen aSec)`, construída explicitamente a
partir de `a0`/`ha0` — como um LEMA comum (não `instance` de seção), para ser
fornecida via `haveI` local exatamente onde for sintaticamente exigida. -/
lemma nonempty_basicOpen (a0 : ℤ) (ha0 : a0 ≠ 0) :
    Nonempty (testScheme.basicOpen (aSec a0)) :=
  ⟨⟨genericPoint testScheme, genericPoint_mem_basicOpen a0 ha0⟩⟩

/-- Restrição de `aSec a0` ao seu próprio aberto básico. Não exige a instância
`Nonempty (testScheme.basicOpen aSec)`. -/
def aRes (a0 : ℤ) : Γ(testScheme, testScheme.basicOpen (aSec a0)) :=
  testScheme.presheaf.map (homOfLE (testScheme.basicOpen_le (aSec a0))).op (aSec a0)

lemma isUnit_aRes (a0 : ℤ) : IsUnit (aRes a0) :=
  testScheme.toRingedSpace.isUnit_res_basicOpen (aSec a0)

/-- O único ponto do arquivo em que `Nonempty (testScheme.basicOpen aSec)` é
sintaticamente exigida (via `Scheme.germToFunctionField`). Fornecida por `haveI`
LOCAL, inline no próprio tipo do lema. -/
lemma germToFunctionField_aRes (a0 : ℤ) (ha0 : a0 ≠ 0) :
    haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
    testScheme.germToFunctionField (testScheme.basicOpen (aSec a0)) (aRes a0) = genf a0 := by
  haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
  simp only [genf, Scheme.germToFunctionField, aRes]
  rw [TopCat.Presheaf.germ_res_apply]

lemma ord_genf_eq_zero_of_mem_basicOpen (a0 : ℤ) (ha0 : a0 ≠ 0) {x : testScheme}
    (hx : x ∈ testScheme.basicOpen (aSec a0)) :
    testScheme.ord (genf a0) x = 0 := by
  haveI := nonempty_basicOpen a0 ha0
  rw [← germToFunctionField_aRes a0 ha0]
  exact Scheme.ord_of_isUnit (isUnit_aRes a0) hx

lemma basicOpen_aSec_eq (a0 : ℤ) :
    testScheme.basicOpen (aSec a0) = PrimeSpectrum.basicOpen a0 := by
  simp only [aSec]
  exact AlgebraicGeometry.basicOpen_eq_of_affine (R := testRing) a0

lemma mem_basicOpen_iff (a0 : ℤ) (x : testScheme) :
    x ∈ testScheme.basicOpen (aSec a0) ↔ a0 ∉ x.asIdeal := by
  rw [show (x ∈ testScheme.basicOpen (aSec a0)) = (x ∈ PrimeSpectrum.basicOpen a0) from
    congrArg (x ∈ ·) (basicOpen_aSec_eq a0)]
  exact PrimeSpectrum.mem_basicOpen a0 x

lemma mem_asIdeal_of_notMem_basicOpen (a0 : ℤ) {x : testScheme}
    (hx : x ∉ testScheme.basicOpen (aSec a0)) :
    a0 ∈ x.asIdeal := by
  rw [mem_basicOpen_iff, not_not] at hx
  exact hx

lemma isMinimalPrime_of_mem_asIdeal (a0 : ℤ) (ha0 : a0 ≠ 0) {x : testScheme}
    (hx : a0 ∈ x.asIdeal) :
    (Ideal.span {a0}).IsMinimalPrime x.asIdeal := by
  have hle : Ideal.span {a0} ≤ x.asIdeal := (Ideal.span_singleton_le_iff_mem x.asIdeal).mpr hx
  have hxprime : x.asIdeal.IsPrime := x.isPrime
  have hxnebot : x.asIdeal ≠ ⊥ := by
    intro h
    rw [h] at hx
    simp only [Ideal.mem_bot] at hx
    exact ha0 hx
  have hxmax : x.asIdeal.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hxprime hxnebot
  refine ⟨⟨hxprime, hle⟩, ?_⟩
  rintro q ⟨hqprime, hqle⟩ hqx
  have hqnebot : q ≠ ⊥ := by
    intro h
    rw [h] at hqle
    simp only [le_bot_iff, Ideal.span_singleton_eq_bot] at hqle
    exact ha0 hqle
  have hqmax : q.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hqprime hqnebot
  exact (hqmax.eq_of_le hxprime.ne_top hqx).ge

lemma asIdeal_injective : Function.Injective (fun x : testScheme => x.asIdeal) :=
  fun _ _ h => PrimeSpectrum.ext h

theorem finite_support_ord_genf (a0 : ℤ) (ha0 : a0 ≠ 0) :
    (Function.support (fun x : testScheme => testScheme.ord (genf a0) x)).Finite := by
  have hsub : Function.support (fun x : testScheme => testScheme.ord (genf a0) x) ⊆
      {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} := by
    intro x hx
    simp only [Function.mem_support] at hx
    have hxnotmem : x ∉ testScheme.basicOpen (aSec a0) := fun hmem =>
      hx (ord_genf_eq_zero_of_mem_basicOpen a0 ha0 hmem)
    exact isMinimalPrime_of_mem_asIdeal a0 ha0 (mem_asIdeal_of_notMem_basicOpen a0 hxnotmem)
  have hfin : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal}.Finite := by
    have hmp := Ideal.finite_minimalPrimes_of_isNoetherianRing (R := ℤ) (Ideal.span {a0})
    have himg : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} ⊆
        (fun x : testScheme => x.asIdeal) ⁻¹' (Ideal.span {a0}).minimalPrimes := fun _ hx => hx
    exact (Set.Finite.preimage asIdeal_injective.injOn hmp).subset himg
  exact hfin.subset hsub

/-- `ord (genf a0)` tem suporte finito, para QUALQUER `a0 : ℤ` não-nulo (HG-1C/HG-1E). -/
theorem finite_support_ord_algebraMap (a0 : ℤ) (ha0 : a0 ≠ 0) :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField a0) x)).Finite := by
  simpa only [algebraMap_eq_genf] using finite_support_ord_genf a0 ha0

/-! ## Empacotamento (reproduzido de HG-1E) — `genf a0` vira um termo de
`AlgebraicCycle testScheme ℤ`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`. Esta é a única
construção `AlgebraicCycle` de que HG-1g precisa: aplicada duas vezes (a `a0` e a `b0`),
ela produz tanto o ciclo "numerador" quanto o ciclo "denominador" — ver seção HG-1g
abaixo. -/

/-- `ord (genf a0)`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`, empacotado como um termo de
`AlgebraicCycle testScheme ℤ` (HG-1E). -/
def principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (genf a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_genf a0 ha0⟩

/-!
## HG-1g (NOVO nesta sessão) — parametrização total sobre `(a0 b0 : ℤ)` da identidade
Num/Den de HG-1f

`f_ab a0 b0 := genf a0 / genf b0` generaliza `f = 3/2` de HG-1b/HG-1F para QUAISQUER
`a0, b0 : ℤ` não-nulos. `principalCycle_f_ab_eq_sub` é a decomposição pontual pedida pelo
teste HG-1g: o ciclo de `f_ab a0 b0` é a diferença dos ciclos de `a0` e `b0` — ambos
INSTÂNCIAS da MESMA `principalCycle_a0` de HG-1E, em vez de duas construções separadas
`principalCycle_Num`/`principalCycle_Den` como em HG-1F. Mesmo argumento de prova de
`principalCycle_f_eq_sub` (HG-1f): `Function.locallyFinsuppWithin.ext` reduz a um
objetivo pontual, fechado por `coe_sub`/`Pi.sub_apply` do lado da subtração de ciclos e
por rearranjo de uma linha (`omega`) da identidade `ord_mul`.
-/

/-- O quociente `genf a0 / genf b0`, para QUAISQUER `a0, b0 : ℤ` — generaliza `f = 3/2` de
HG-1b/HG-1F à família parametrizada de HG-1E. -/
def f_ab (a0 b0 : ℤ) : testScheme.functionField := genf a0 / genf b0

lemma f_ab_ne_zero (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) : f_ab a0 b0 ≠ 0 :=
  div_ne_zero (genf_ne_zero a0 ha0) (genf_ne_zero b0 hb0)

lemma f_ab_eq_div (a0 b0 : ℤ) : f_ab a0 b0 = genf a0 / genf b0 := rfl

/-- **Generalização de `finite_support_ord_f` (HG-1b/HG-1F).** `ord (f_ab a0 b0)` tem
suporte finito, para QUAISQUER `a0, b0 : ℤ` não-nulos, via `ord_mul` reduzindo às duas
instâncias parametrizadas `finite_support_ord_genf a0 ha0`/`finite_support_ord_genf b0
hb0` de HG-1E/HG-1C. -/
theorem finite_support_ord_f_ab (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    (Function.support (fun x : testScheme => testScheme.ord (f_ab a0 b0) x)).Finite := by
  have hbne : genf b0 ≠ 0 := genf_ne_zero b0 hb0
  -- `f_ab a0 b0 * genf b0 = genf a0`
  have hkey : f_ab a0 b0 * genf b0 = genf a0 := by
    rw [f_ab_eq_div, div_mul_cancel₀ _ hbne]
  have hsub : Function.support (fun x : testScheme => testScheme.ord (f_ab a0 b0) x) ⊆
      Function.support (fun x : testScheme => testScheme.ord (genf a0) x) ∪
      Function.support (fun x : testScheme => testScheme.ord (genf b0) x) := by
    intro x hx
    simp only [Function.mem_support] at hx
    by_contra hcon
    simp only [Set.mem_union, Function.mem_support, not_or, not_not] at hcon
    apply hx
    have hord : testScheme.ord (f_ab a0 b0) x + testScheme.ord (genf b0) x =
        testScheme.ord (genf a0) x := by
      rw [← hkey, Scheme.ord_mul (f_ab_ne_zero a0 b0 ha0 hb0) hbne]
    rw [hcon.1, hcon.2, add_zero] at hord
    exact hord
  exact ((finite_support_ord_genf a0 ha0).union (finite_support_ord_genf b0 hb0)).subset hsub

/-- **Generalização de `principalCycle_f` (HG-1D/HG-1F).** `ord (f_ab a0 b0)`, para
QUAISQUER `a0, b0 : ℤ` não-nulos, empacotado como um termo de `AlgebraicCycle testScheme
ℤ`. -/
def principalCycle_f_ab (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (f_ab a0 b0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_f_ab a0 b0 ha0 hb0⟩

/-- **Resultado principal de HG-1g — a generalização pedida pelo teste.**
`principalCycle_f_ab a0 b0` (o ciclo do quociente `genf a0 / genf b0`) é a diferença, em
`AlgebraicCycle testScheme ℤ`, do ciclo de `a0` menos o ciclo de `b0` —
`principalCycle_a0 a0 ha0 - principalCycle_a0 b0 hb0`, para QUAISQUER `a0, b0 : ℤ`
não-nulos. Generaliza `principalCycle_f_eq_sub` de HG-1F (que só valia para o par fixo
`Num.a0 = 3`/`Den.a0 = 2`) à família parametrizada de HG-1E; note que, diferente de
HG-1F, o lado direito não precisa de duas construções `AlgebraicCycle` separadas: ambos
os termos são a MESMA `principalCycle_a0`, avaliada em `a0` e em `b0`. -/
theorem principalCycle_f_ab_eq_sub (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0) :
    principalCycle_f_ab a0 b0 ha0 hb0 = principalCycle_a0 a0 ha0 - principalCycle_a0 b0 hb0 := by
  apply Function.locallyFinsuppWithin.ext
  intro x
  have hbne : genf b0 ≠ 0 := genf_ne_zero b0 hb0
  have hkey : f_ab a0 b0 * genf b0 = genf a0 := by
    rw [f_ab_eq_div, div_mul_cancel₀ _ hbne]
  have hord : testScheme.ord (f_ab a0 b0) x + testScheme.ord (genf b0) x =
      testScheme.ord (genf a0) x := by
    rw [← hkey, Scheme.ord_mul (f_ab_ne_zero a0 b0 ha0 hb0) hbne]
  simp only [Function.locallyFinsuppWithin.coe_sub, Pi.sub_apply]
  show testScheme.ord (f_ab a0 b0) x = testScheme.ord (genf a0) x - testScheme.ord (genf b0) x
  omega

end

/-! ## Verificação de instanciação: a instância concreta de HG-1b/HG-1F (`a0 = 3`,
`b0 = 2`) obtida por especialização direta do resultado parametrizado acima, sem nenhuma
duplicação de prova. -/

section Instantiation

/-- `principalCycle_f_ab_eq_sub` instanciado em `a0 = 3`, `b0 = 2` — recupera o conteúdo
de `principalCycle_f_eq_sub` (HG-1F, `f = 3/2 = Num.a0/Den.a0`), agora como caso
particular do resultado totalmente parametrizado. (`noncomputable` necessário aqui pelo
mesmo motivo já documentado em HG-1E: fora da seção `noncomputable section`, `example`s
que dependem de declarações `noncomputable` precisam ser marcados explicitamente.) -/
noncomputable example :
    principalCycle_f_ab 3 2 (by decide) (by decide) =
      principalCycle_a0 3 (by decide) - principalCycle_a0 2 (by decide) :=
  principalCycle_f_ab_eq_sub 3 2 (by decide) (by decide)

/-- Uma segunda instanciação, com um par `(a0, b0)` diferente do de HG-1b/HG-1F
(`a0 = 5`, `b0 = 7`), verificando que a parametrização é genuína (não apenas uma
reindexação sintática do caso `3, 2`). -/
noncomputable example :
    principalCycle_f_ab 5 7 (by decide) (by decide) =
      principalCycle_a0 5 (by decide) - principalCycle_a0 7 (by decide) :=
  principalCycle_f_ab_eq_sub 5 7 (by decide) (by decide)

end Instantiation

/-! ## Verificação de dependências de prova (nesta sessão) — as seis declarações
genuinamente novas deste arquivo (HG-1g), confirmando que dependem apenas de
`[propext, Classical.choice, Quot.sound]` (nenhuma prova incompleta escapou pela síntese
de instâncias ou por elaboração implícita). -/

#print axioms f_ab
#print axioms f_ab_ne_zero
#print axioms f_ab_eq_div
#print axioms finite_support_ord_f_ab
#print axioms principalCycle_f_ab
#print axioms principalCycle_f_ab_eq_sub

end AlgebraicGeometry.HG1C
