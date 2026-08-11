/-
HG-1F (Wave 4, item WAVE4-HG-1F) — expressar `principalCycle_f` de HG-1D
(o `f = 3/2` empacotado como termo de `AlgebraicCycle`) como a diferença
`principalCycle_Num - principalCycle_Den` de dois novos termos de
`AlgebraicCycle`, construídos a partir dos namespaces `Num`/`Den` já
existentes de HG-1D (rascunho formal isolado, NÃO integrado a TamesisLab)

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
novidade matemática: a decomposição "divisor de um quociente = divisor do
numerador menos divisor do denominador" é clássica; o que está formalizado
aqui é apenas essa identidade pontual, num caso concreto (`X = Spec ℤ`,
`f = 3/2`), reempacotada no tipo `AlgebraicCycle` de Mathlib.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1f, especificado (após revisão
adversarial na etapa de planejamento da Onda 4) como:

  A partir dos namespaces Num/Den existentes de HG-1D, definir
  principalCycle_Num, principalCycle_Den via o mesmo padrão de três
  campos; provar principalCycle_f = principalCycle_Num - principalCycle_Den
  via Function.locallyFinsuppWithin.ext, fechando o objetivo pontual com
  coe_sub mais rearranjo de uma linha (sub_eq_of_eq_add/omega) da
  identidade ord_mul já derivada em finite_support_ord_f.

RESULTADO: SUCESSO. Mecânico dado HG-1D já fechado — nenhum lema novo de
Mathlib além dos já citados em HG-1D foi necessário; a única adição real de
técnica é `Function.locallyFinsuppWithin.coe_sub`/`.ext` (ambos em
`Topology/LocallyFinsupp.lean`, mesmo arquivo já citado no preâmbulo de
HG-1 para `AlgebraicCycle`/`locallyFinsuppWithin`) e `omega` para o
rearranjo aritmético final.

## O que realmente fechou o teste

**Inlining verbatim de HG-1D.** Todo o bloco de HG-1D
(`HG1DPrincipalCycleFProbe.lean`, mesmo diretório), de `import Mathlib` até
`end AlgebraicGeometry.HG1B` (`principalCycle_f` inclusive), foi copiado
byte-idêntico para este arquivo nesta sessão (diretamente do arquivo-fonte,
não de memória nem paráfrase) — mesmo motivo mecânico já documentado nos
preâmbulos de HG-1D/HG-1E: este arquivo, como HG-1D, vive em
`03_MILLENNIUM/05_HODGE/FORMAL/`, fora da raiz de módulos do pacote Lake
(confirmado nesta sessão por reinspeção de `05_FORMAL/lean/lakefile.toml` e
`05_FORMAL/lean/TamesisLab.lean`, nenhuma mudança desde a verificação de
HG-1D/HG-1E), logo não há caminho de `import` de um arquivo solto para
outro; a única forma de reusar `Num.a0`/`Den.a0`/`f`/`principalCycle_f`/etc.
aqui é reproduzir o texto. Reusar o mesmo nome de namespace
(`AlgebraicGeometry.HG1B`) num arquivo novo, não importado pelo original,
não causa nenhum conflito de compilação — o mesmo padrão já usado com
sucesso por HG-1E (que reusa `AlgebraicGeometry.HG1C` como nome de
namespace num arquivo novo).

**As duas declarações genuinamente novas — `principalCycle_Num` e
`principalCycle_Den`.** Mesmo padrão de três campos de `principalCycle_f`
(HG-1D) / `principalCycle` (HG-1), aplicados a
`algebraMap ℤ testScheme.functionField Num.a0` /
`algebraMap ℤ testScheme.functionField Den.a0` em vez de `f`, usando os
resultados de finitude já provados em HG-1D — `Num.finite_support_ord_algebraMap`
e `Den.finite_support_ord_algebraMap` — sem nenhum passo de prova novo além
da reindexação (mesma observação mecânica já feita nos preâmbulos de
HG-1D/HG-1E para `principalCycle_f`/`principalCycle_a0`):

```
def principalCycle_Num : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using Num.finite_support_ord_algebraMap⟩

def principalCycle_Den : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using Den.finite_support_ord_algebraMap⟩
```

**A terceira declaração nova — `principalCycle_f_eq_sub` — o resultado
principal pedido pelo teste.** `Function.locallyFinsuppWithin.ext`
(`Topology/LocallyFinsupp.lean`, o mesmo arquivo que define
`AlgebraicCycle X R := Function.locallyFinsupp X R`, já citado no preâmbulo
de HG-1) reduz a igualdade de dois termos de `AlgebraicCycle` a um objetivo
pontual `∀ a, D₁ a = D₂ a`. Para cada `x`, o lado direito
`(principalCycle_Num - principalCycle_Den) x` se reduz a
`principalCycle_Num x - principalCycle_Den x` via
`Function.locallyFinsuppWithin.coe_sub` (`(↑(D₁ - D₂) : X → Y) = D₁ - D₂`,
tag `@[simp]`) seguido de `Pi.sub_apply` — ambos por `simp only`. O que
resta, após desdobrar as três definições (`principalCycle_f`,
`principalCycle_Num`, `principalCycle_Den` — desdobramento definicional,
igual ao já usado em `supportWithinDomain' := by simp` nas três
construções), é exatamente

  `testScheme.ord f x = testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x
     - testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x`

que segue por rearranjo de uma linha (`omega`, tratando os três valores de
`ord` como átomos inteiros opacos) da identidade

  `testScheme.ord f x + testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x
     = testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x`

— esta última é EXATAMENTE `hord`, já derivada dentro da prova de
`finite_support_ord_f` em HG-1D (`hkey` via `f_eq_div`/`div_mul_cancel₀`,
seguido de `Scheme.ord_mul f_ne_zero hdmapne`), reproduzida aqui
verbatim (mesmos dois `have`s, `hdmapne`/`hkey`, e a mesma linha `rw [←
hkey, Scheme.ord_mul f_ne_zero hdmapne]` para `hord`) porque `hord` na
prova original de HG-1D é local àquela prova (não exportada como lema
próprio) — não há aqui nenhuma prova nova de `ord_mul`, apenas reuso local
do mesmo argumento já fechado.

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1D já estavam verificados
no preâmbulo daquele arquivo (mesmo diretório) — não repetidos aqui por
brevidade, ver `HG1DPrincipalCycleFProbe.lean`. Adicionalmente, para
`principalCycle_Num`/`principalCycle_Den`/`principalCycle_f_eq_sub`:
  - `AlgebraicGeometry.AlgebraicCycle`, campos `toFun`, `supportWithinDomain'`,
    `supportLocallyFiniteWithinDomain'` (`Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`)
    — mesma citação já verificada em HG-1/HG-1D/HG-1E.
  - `Filter.univ_mem` (`Mathlib/Order/Filter/Basic.lean`) — idem.
  - `Function.locallyFinsuppWithin.ext`
    (`Mathlib/Topology/LocallyFinsupp.lean:146-148`,
    `@[ext] lemma ext [Zero Y] {D₁ D₂ : locallyFinsuppWithin U Y}
    (h : ∀ a, D₁ a = D₂ a) : D₁ = D₂ := DFunLike.ext _ _ h`) — assinatura
    relida nesta sessão; `AlgebraicCycle X R` é `abbrev` de
    `Function.locallyFinsupp X R := locallyFinsuppWithin (Set.univ : Set X) R`
    (mesmo arquivo, linha 61), logo o lema se aplica diretamente.
  - `Function.locallyFinsuppWithin.coe_sub`
    (`Mathlib/Topology/LocallyFinsupp.lean:352-353`,
    `@[simp] lemma coe_sub [AddGroup Y] (D₁ D₂ : locallyFinsuppWithin U Y) :
    (↑(D₁ - D₂) : X → Y) = D₁ - D₂ := rfl`) — assinatura relida nesta
    sessão; `AddGroup ℤ` é instância padrão.
  - `Pi.sub_apply` (Mathlib, `Algebra/Group/Pi/Basic.lean` — lema padrão de
    biblioteca, já usado implicitamente em construções anteriores desta
    linha via `simp`).
  - `Scheme.ord_mul` (`AlgebraicGeometry/OrderOfVanishing.lean:81-82`,
    `lemma ord_mul {x : X} {f g : X.functionField} (hf : f ≠ 0) (hg : g ≠ 0) :
    ord (f * g) x = ord f x + ord g x`) — já citado/usado em HG-1D (mesma
    prova de `finite_support_ord_f`), reconferido nesta sessão: incondicional
    em `x` (não requer `coheight x = 1` como hipótese explícita — o caso
    `coheight x ≠ 1` é tratado dentro da própria prova de `ord_mul`), logo
    `hord` vale para TODO `x : testScheme`, não apenas para `x` no suporte —
    exatamente o que a prova pontual de `principalCycle_f_eq_sub` precisa.
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de
saída `0`) e por busca textual (zero ocorrências dos marcadores proibidos
pela governança do laboratório).
-/

import Mathlib

open AlgebraicGeometry CategoryTheory

namespace AlgebraicGeometry.HG1B

noncomputable section

/-! ## Configuração concreta: `X = Spec ℤ` (mesma escolha de HG-1) -/

/-- Anel de teste: `ℤ`. -/
abbrev testRing : CommRingCat := CommRingCat.of ℤ

/-- Esquema de teste: `Spec ℤ`. -/
abbrev testScheme : Scheme.{0} := Spec testRing

instance : Nonempty (⊤ : testScheme.Opens) := ⟨⟨genericPoint testScheme, trivial⟩⟩

/-! ## Passo 1 — compatibilidade `algebraMap`/`germToFunctionField`

Enunciado exato pedido pelo teste HG-1b. Fecha por unicidade de homomorfismos de anel
`ℤ →+* R` (`Int.subsingleton_ringHom`) — ver preâmbulo para a discussão de por que a rota
originalmente citada (`Scheme.ΓSpecIso_inv` + desdobrar `StructureSheaf.toStalk`) não
funciona por `rfl`/`simp` direto neste caso concreto. -/

lemma algebraMap_eq_germToFunctionField (x : ℤ) :
    algebraMap ℤ testScheme.functionField x =
      testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x) := by
  have h : (algebraMap ℤ testScheme.functionField) =
      (testScheme.germToFunctionField ⊤).hom.comp (Scheme.ΓSpecIso testRing).inv.hom :=
    Subsingleton.elim _ _
  exact DFunLike.congr_fun h x

/-! ## Passo 2 — o argumento de finitude de HG-1 (`finite_support_ord_f`), reproduzido
para `a0 = 3` (`Num`) e `a0 = 2` (`Den`)

Estrutura idêntica à de HG-1 (`principal_divisor_algebraic_cycle_bridge.lean`), agora
expressa via `algebraMap` (usando `algebraMap_eq_germToFunctionField` do Passo 1) em vez
de diretamente via `germToFunctionField`, para que se conecte com `f = 3/2` no Passo 3. -/

namespace Num

/-- Numerador: `a0 = 3`. -/
def a0 : ℤ := 3

lemma a0_ne_zero : a0 ≠ 0 := by decide

def aSec : Γ(testScheme, ⊤) := (Scheme.ΓSpecIso testRing).inv a0

lemma aSec_ne_zero : aSec ≠ (0 : Γ(testScheme, ⊤)) := by
  simp only [aSec]
  intro h
  exact a0_ne_zero (by simpa using congrArg (Scheme.ΓSpecIso testRing).hom h)

/-- Germe de `aSec` no ponto genérico. -/
def genf : testScheme.functionField := testScheme.germToFunctionField ⊤ aSec

lemma algebraMap_eq_genf : algebraMap ℤ testScheme.functionField a0 = genf :=
  algebraMap_eq_germToFunctionField a0

lemma genf_ne_zero : genf ≠ 0 := by
  have hinj := testScheme.germToFunctionField_injective (⊤ : testScheme.Opens)
  simp only [genf]
  intro h
  exact aSec_ne_zero ((map_eq_zero_iff _ hinj).mp h)

lemma genericPoint_mem_basicOpen : genericPoint testScheme ∈ testScheme.basicOpen aSec := by
  rw [Scheme.mem_basicOpen_top, isUnit_iff_ne_zero]
  exact genf_ne_zero

instance : Nonempty (testScheme.basicOpen aSec) :=
  ⟨⟨genericPoint testScheme, genericPoint_mem_basicOpen⟩⟩

def aRes : Γ(testScheme, testScheme.basicOpen aSec) :=
  testScheme.presheaf.map (homOfLE (testScheme.basicOpen_le aSec)).op aSec

lemma isUnit_aRes : IsUnit aRes :=
  testScheme.toRingedSpace.isUnit_res_basicOpen aSec

lemma germToFunctionField_aRes :
    testScheme.germToFunctionField (testScheme.basicOpen aSec) aRes = genf := by
  simp only [genf, Scheme.germToFunctionField, aRes]
  rw [TopCat.Presheaf.germ_res_apply]

lemma ord_genf_eq_zero_of_mem_basicOpen {x : testScheme} (hx : x ∈ testScheme.basicOpen aSec) :
    testScheme.ord genf x = 0 := by
  rw [← germToFunctionField_aRes]
  exact Scheme.ord_of_isUnit isUnit_aRes hx

lemma basicOpen_aSec_eq : testScheme.basicOpen aSec = PrimeSpectrum.basicOpen a0 := by
  simp only [aSec]
  exact AlgebraicGeometry.basicOpen_eq_of_affine (R := testRing) a0

lemma mem_basicOpen_iff (x : testScheme) :
    x ∈ testScheme.basicOpen aSec ↔ a0 ∉ x.asIdeal := by
  rw [show (x ∈ testScheme.basicOpen aSec) = (x ∈ PrimeSpectrum.basicOpen a0) from
    congrArg (x ∈ ·) basicOpen_aSec_eq]
  exact PrimeSpectrum.mem_basicOpen a0 x

lemma mem_asIdeal_of_notMem_basicOpen {x : testScheme} (hx : x ∉ testScheme.basicOpen aSec) :
    a0 ∈ x.asIdeal := by
  rw [mem_basicOpen_iff, not_not] at hx
  exact hx

lemma isMinimalPrime_of_mem_asIdeal {x : testScheme} (hx : a0 ∈ x.asIdeal) :
    (Ideal.span {a0}).IsMinimalPrime x.asIdeal := by
  have hle : Ideal.span {a0} ≤ x.asIdeal := (Ideal.span_singleton_le_iff_mem x.asIdeal).mpr hx
  have hxprime : x.asIdeal.IsPrime := x.isPrime
  have hxnebot : x.asIdeal ≠ ⊥ := by
    intro h
    rw [h] at hx
    simp only [Ideal.mem_bot] at hx
    exact a0_ne_zero hx
  have hxmax : x.asIdeal.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hxprime hxnebot
  refine ⟨⟨hxprime, hle⟩, ?_⟩
  rintro q ⟨hqprime, hqle⟩ hqx
  have hqnebot : q ≠ ⊥ := by
    intro h
    rw [h] at hqle
    simp only [le_bot_iff, Ideal.span_singleton_eq_bot] at hqle
    exact a0_ne_zero hqle
  have hqmax : q.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hqprime hqnebot
  exact (hqmax.eq_of_le hxprime.ne_top hqx).ge

lemma asIdeal_injective : Function.Injective (fun x : testScheme => x.asIdeal) :=
  fun _ _ h => PrimeSpectrum.ext h

theorem finite_support_ord_genf :
    (Function.support (fun x : testScheme => testScheme.ord genf x)).Finite := by
  have hsub : Function.support (fun x : testScheme => testScheme.ord genf x) ⊆
      {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} := by
    intro x hx
    simp only [Function.mem_support] at hx
    have hxnotmem : x ∉ testScheme.basicOpen aSec := fun hmem =>
      hx (ord_genf_eq_zero_of_mem_basicOpen hmem)
    exact isMinimalPrime_of_mem_asIdeal (mem_asIdeal_of_notMem_basicOpen hxnotmem)
  have hfin : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal}.Finite := by
    have hmp := Ideal.finite_minimalPrimes_of_isNoetherianRing (R := ℤ) (Ideal.span {a0})
    have himg : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} ⊆
        (fun x : testScheme => x.asIdeal) ⁻¹' (Ideal.span {a0}).minimalPrimes := fun _ hx => hx
    exact (Set.Finite.preimage asIdeal_injective.injOn hmp).subset himg
  exact hfin.subset hsub

/-- `finite_support_ord_f` de HG-1, aqui expressa via `algebraMap` (a0 = 3). -/
theorem finite_support_ord_algebraMap :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField a0) x)).Finite := by
  simpa only [algebraMap_eq_genf] using finite_support_ord_genf

end Num

namespace Den

/-- Denominador: `a0 = 2`. -/
def a0 : ℤ := 2

lemma a0_ne_zero : a0 ≠ 0 := by decide

def aSec : Γ(testScheme, ⊤) := (Scheme.ΓSpecIso testRing).inv a0

lemma aSec_ne_zero : aSec ≠ (0 : Γ(testScheme, ⊤)) := by
  simp only [aSec]
  intro h
  exact a0_ne_zero (by simpa using congrArg (Scheme.ΓSpecIso testRing).hom h)

def genf : testScheme.functionField := testScheme.germToFunctionField ⊤ aSec

lemma algebraMap_eq_genf : algebraMap ℤ testScheme.functionField a0 = genf :=
  algebraMap_eq_germToFunctionField a0

lemma genf_ne_zero : genf ≠ 0 := by
  have hinj := testScheme.germToFunctionField_injective (⊤ : testScheme.Opens)
  simp only [genf]
  intro h
  exact aSec_ne_zero ((map_eq_zero_iff _ hinj).mp h)

lemma genericPoint_mem_basicOpen : genericPoint testScheme ∈ testScheme.basicOpen aSec := by
  rw [Scheme.mem_basicOpen_top, isUnit_iff_ne_zero]
  exact genf_ne_zero

instance : Nonempty (testScheme.basicOpen aSec) :=
  ⟨⟨genericPoint testScheme, genericPoint_mem_basicOpen⟩⟩

def aRes : Γ(testScheme, testScheme.basicOpen aSec) :=
  testScheme.presheaf.map (homOfLE (testScheme.basicOpen_le aSec)).op aSec

lemma isUnit_aRes : IsUnit aRes :=
  testScheme.toRingedSpace.isUnit_res_basicOpen aSec

lemma germToFunctionField_aRes :
    testScheme.germToFunctionField (testScheme.basicOpen aSec) aRes = genf := by
  simp only [genf, Scheme.germToFunctionField, aRes]
  rw [TopCat.Presheaf.germ_res_apply]

lemma ord_genf_eq_zero_of_mem_basicOpen {x : testScheme} (hx : x ∈ testScheme.basicOpen aSec) :
    testScheme.ord genf x = 0 := by
  rw [← germToFunctionField_aRes]
  exact Scheme.ord_of_isUnit isUnit_aRes hx

lemma basicOpen_aSec_eq : testScheme.basicOpen aSec = PrimeSpectrum.basicOpen a0 := by
  simp only [aSec]
  exact AlgebraicGeometry.basicOpen_eq_of_affine (R := testRing) a0

lemma mem_basicOpen_iff (x : testScheme) :
    x ∈ testScheme.basicOpen aSec ↔ a0 ∉ x.asIdeal := by
  rw [show (x ∈ testScheme.basicOpen aSec) = (x ∈ PrimeSpectrum.basicOpen a0) from
    congrArg (x ∈ ·) basicOpen_aSec_eq]
  exact PrimeSpectrum.mem_basicOpen a0 x

lemma mem_asIdeal_of_notMem_basicOpen {x : testScheme} (hx : x ∉ testScheme.basicOpen aSec) :
    a0 ∈ x.asIdeal := by
  rw [mem_basicOpen_iff, not_not] at hx
  exact hx

lemma isMinimalPrime_of_mem_asIdeal {x : testScheme} (hx : a0 ∈ x.asIdeal) :
    (Ideal.span {a0}).IsMinimalPrime x.asIdeal := by
  have hle : Ideal.span {a0} ≤ x.asIdeal := (Ideal.span_singleton_le_iff_mem x.asIdeal).mpr hx
  have hxprime : x.asIdeal.IsPrime := x.isPrime
  have hxnebot : x.asIdeal ≠ ⊥ := by
    intro h
    rw [h] at hx
    simp only [Ideal.mem_bot] at hx
    exact a0_ne_zero hx
  have hxmax : x.asIdeal.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hxprime hxnebot
  refine ⟨⟨hxprime, hle⟩, ?_⟩
  rintro q ⟨hqprime, hqle⟩ hqx
  have hqnebot : q ≠ ⊥ := by
    intro h
    rw [h] at hqle
    simp only [le_bot_iff, Ideal.span_singleton_eq_bot] at hqle
    exact a0_ne_zero hqle
  have hqmax : q.IsMaximal := Ideal.IsPrime.isMaximal_of_ne_bot hqprime hqnebot
  exact (hqmax.eq_of_le hxprime.ne_top hqx).ge

lemma asIdeal_injective : Function.Injective (fun x : testScheme => x.asIdeal) :=
  fun _ _ h => PrimeSpectrum.ext h

theorem finite_support_ord_genf :
    (Function.support (fun x : testScheme => testScheme.ord genf x)).Finite := by
  have hsub : Function.support (fun x : testScheme => testScheme.ord genf x) ⊆
      {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} := by
    intro x hx
    simp only [Function.mem_support] at hx
    have hxnotmem : x ∉ testScheme.basicOpen aSec := fun hmem =>
      hx (ord_genf_eq_zero_of_mem_basicOpen hmem)
    exact isMinimalPrime_of_mem_asIdeal (mem_asIdeal_of_notMem_basicOpen hxnotmem)
  have hfin : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal}.Finite := by
    have hmp := Ideal.finite_minimalPrimes_of_isNoetherianRing (R := ℤ) (Ideal.span {a0})
    have himg : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} ⊆
        (fun x : testScheme => x.asIdeal) ⁻¹' (Ideal.span {a0}).minimalPrimes := fun _ hx => hx
    exact (Set.Finite.preimage asIdeal_injective.injOn hmp).subset himg
  exact hfin.subset hsub

/-- `finite_support_ord_f` de HG-1, aqui expressa via `algebraMap` (a0 = 2). -/
theorem finite_support_ord_algebraMap :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField a0) x)).Finite := by
  simpa only [algebraMap_eq_genf] using finite_support_ord_genf

end Den

/-! ## Passo 3 — Montagem: `f = 3/2` via `IsFractionRing.div_surjective`, `ord_mul`, e as
duas instâncias acima -/

/-- A função de teste: `f = 3/2` em `testScheme.functionField`, construída diretamente via
`algebraMap ℤ` (`Num.a0 = 3`, `Den.a0 = 2` por definição). -/
def f : testScheme.functionField :=
  algebraMap ℤ testScheme.functionField Num.a0 / algebraMap ℤ testScheme.functionField Den.a0

lemma f_ne_zero : f ≠ 0 := by
  rw [f, Num.algebraMap_eq_genf, Den.algebraMap_eq_genf]
  exact div_ne_zero Num.genf_ne_zero Den.genf_ne_zero

lemma f_eq_div : f = algebraMap ℤ testScheme.functionField Num.a0 /
    algebraMap ℤ testScheme.functionField Den.a0 := rfl

/-- `f` já está na forma `algebraMap n / algebraMap d` com `n = 3`, `d = 2` — o par
numerador/denominador concreto cuja existência `IsFractionRing.div_surjective (A := ℤ)`
garante em geral (ver preâmbulo: `f` é *definido* diretamente nessa forma, então
`n := 3`, `d := 2` testemunham a existencial sem precisar invocar escolha). -/
lemma f_div_surjective_witness :
    ∃ n d : ℤ, d ∈ nonZeroDivisors ℤ ∧
      algebraMap ℤ testScheme.functionField n / algebraMap ℤ testScheme.functionField d = f :=
  ⟨Num.a0, Den.a0, mem_nonZeroDivisors_iff_ne_zero.mpr Den.a0_ne_zero, f_eq_div.symm⟩

/-- **Resultado principal.** `ord f` tem suporte finito, para `f = 3/2 :
testScheme.functionField`, via `ord_mul` reduzindo às duas instâncias
`Num.finite_support_ord_algebraMap` (numerador `3`) e `Den.finite_support_ord_algebraMap`
(denominador `2`), exatamente como especificado pelo teste HG-1b. -/
theorem finite_support_ord_f :
    (Function.support (fun x : testScheme => testScheme.ord f x)).Finite := by
  have hdmapne : algebraMap ℤ testScheme.functionField Den.a0 ≠ 0 :=
    Den.algebraMap_eq_genf ▸ Den.genf_ne_zero
  -- `f * algebraMap Den.a0 = algebraMap Num.a0`
  have hkey : f * algebraMap ℤ testScheme.functionField Den.a0 =
      algebraMap ℤ testScheme.functionField Num.a0 := by
    rw [f_eq_div, div_mul_cancel₀ _ hdmapne]
  have hsub : Function.support (fun x : testScheme => testScheme.ord f x) ⊆
      Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x) ∪
      Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x) := by
    intro x hx
    simp only [Function.mem_support] at hx
    by_contra hcon
    simp only [Set.mem_union, Function.mem_support, not_or, not_not] at hcon
    apply hx
    have hord : testScheme.ord f x + testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x =
        testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x := by
      rw [← hkey, Scheme.ord_mul f_ne_zero hdmapne]
    rw [hcon.1, hcon.2, add_zero] at hord
    exact hord
  exact (Num.finite_support_ord_algebraMap.union Den.finite_support_ord_algebraMap).subset hsub


/-!
## Empacotamento — `f` (o `f = 3/2` de HG-1b) vira um termo de
`AlgebraicCycle testScheme ℤ`

Construção byte-idêntica (a menos do nome) à `principalCycle` de HG-1
(`principal_divisor_algebraic_cycle_bridge.lean`, mesmo diretório), agora aplicada a
`f`/`finite_support_ord_f` de HG-1b (`f = 3/2`) em vez do `f` germe único de HG-1. Ver
"ESCOPO HONESTO" no preâmbulo de HG-1 e a nota de escopo no preâmbulo deste arquivo:
isto NÃO aproxima a Conjectura de Hodge.
-/

/-- `ord f`, para `f = 3/2` (HG-1b), empacotado como um termo de
`AlgebraicCycle testScheme ℤ` — espelha verbatim `principalCycle` de HG-1. -/
def principalCycle_f : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord f x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_f⟩

/-!
## HG-1f (NOVO nesta sessão) — `principalCycle_f` como diferença
`principalCycle_Num - principalCycle_Den`

`principalCycle_Num`/`principalCycle_Den` empacotam `ord` do numerador (`Num.a0 = 3`) e
do denominador (`Den.a0 = 2`) como termos de `AlgebraicCycle testScheme ℤ`, mesmo padrão
de três campos de `principalCycle_f` acima, aplicado a
`algebraMap ℤ testScheme.functionField Num.a0`/`Den.a0` em vez de `f`, e reusando
`Num.finite_support_ord_algebraMap`/`Den.finite_support_ord_algebraMap` (já provados
acima, ingredientes da própria prova de `finite_support_ord_f`) para a finitude de
suporte. `principalCycle_f_eq_sub` é a decomposição pontual pedida pelo teste: segue de
`Function.locallyFinsuppWithin.ext` reduzindo a um objetivo pontual, fechado por
`coe_sub`/`Pi.sub_apply` do lado da subtração de ciclos e por rearranjo de uma linha
(`omega`) da identidade `ord_mul` já derivada (como `hord` local) dentro da prova de
`finite_support_ord_f` acima.
-/

/-- `ord` do numerador `algebraMap ℤ testScheme.functionField Num.a0`, empacotado como
um termo de `AlgebraicCycle testScheme ℤ` — mesmo padrão de três campos de
`principalCycle_f`, aplicado a `Num.a0` em vez de `f`. -/
def principalCycle_Num : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using Num.finite_support_ord_algebraMap⟩

/-- `ord` do denominador `algebraMap ℤ testScheme.functionField Den.a0`, empacotado da
mesma forma. -/
def principalCycle_Den : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using Den.finite_support_ord_algebraMap⟩

/-- **Resultado principal de HG-1f.** `principalCycle_f` (o ciclo de `f = 3/2`) é a
diferença, em `AlgebraicCycle testScheme ℤ`, do ciclo do numerador `Num.a0 = 3` menos o
ciclo do denominador `Den.a0 = 2`. -/
theorem principalCycle_f_eq_sub :
    principalCycle_f = principalCycle_Num - principalCycle_Den := by
  apply Function.locallyFinsuppWithin.ext
  intro x
  have hdmapne : algebraMap ℤ testScheme.functionField Den.a0 ≠ 0 :=
    Den.algebraMap_eq_genf ▸ Den.genf_ne_zero
  have hkey : f * algebraMap ℤ testScheme.functionField Den.a0 =
      algebraMap ℤ testScheme.functionField Num.a0 := by
    rw [f_eq_div, div_mul_cancel₀ _ hdmapne]
  have hord : testScheme.ord f x + testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x =
      testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x := by
    rw [← hkey, Scheme.ord_mul f_ne_zero hdmapne]
  simp only [Function.locallyFinsuppWithin.coe_sub, Pi.sub_apply]
  show testScheme.ord f x = testScheme.ord (algebraMap ℤ testScheme.functionField Num.a0) x -
      testScheme.ord (algebraMap ℤ testScheme.functionField Den.a0) x
  omega

end

end AlgebraicGeometry.HG1B
