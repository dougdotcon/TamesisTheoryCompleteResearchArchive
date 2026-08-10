/-
HG-1D (Wave 3, item WAVE3-HG-1D) — empacotar o resultado de finitude f=3/2 de HG-1b
como um termo de `AlgebraicCycle` (rascunho formal isolado, NÃO integrado a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. Todas as declarações novas
verificadas com o comando de impressão de dependências de prova do Lean: dependem
apenas de `[propext, Classical.choice, Quot.sound]` — nenhum marcador de prova
incompleta escapou pela síntese de instâncias. O arquivo não contém nenhuma prova
incompleta, nenhuma declaração local tomada como verdade sem prova, e nenhum bloco
marcado como inseguro, em nenhum lugar (conferido por busca textual nesta sessão).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta rodada: não tocar
em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer parte da
máquina de teoria de Hodge necessária para ela. O conteúdo abaixo é 100% álgebra
comutativa/geometria de esquemas clássica: NADA aqui usa estrutura complexa,
cohomologia, decomposição de Hodge, ou classe de ciclo em cohomologia. Mesmo em caso
de sucesso total, o resultado permanece a várias camadas inteiramente ausentes de
sequer enunciar formalmente Hodge (1,1), quanto mais a conjectura geral.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1d, especificado (após revisão adversarial na
etapa de planejamento da Onda 3) como:

  Construir `principalCycle_f : AlgebraicCycle testScheme ℤ` a partir de `f` e
  `finite_support_ord_f` (já definidos em HG-1b), espelhando verbatim a construção
  `principalCycle` já provada em HG-1.

RESULTADO: SUCESSO, com uma ressalva mecânica de organização de arquivo (não de
conteúdo matemático) explicada abaixo antes de reusar este arquivo.

## O que realmente fechou o teste

**A construção em si é trivial dado o que HG-1b já provou.** `principalCycle_f`
abaixo é byte-idêntica, a menos do nome, a `principalCycle` de HG-1
(`principal_divisor_algebraic_cycle_bridge.lean`, mesmo diretório):

```
def principalCycle_f : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord f x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_f⟩
```

`supportWithinDomain'` fecha por `simp` (o domínio de suporte declarado por
`AlgebraicCycle` é `⊤ : Set testScheme`, então a obrigação é trivial) e
`supportLocallyFiniteWithinDomain'` fecha fornecendo `Set.univ` como a vizinhança
aberta testemunha — `Filter.univ_mem` dá que é vizinhança de qualquer ponto no filtro
`𝓝`, e `finite_support_ord_f` (agora sobre `f = 3/2`, não sobre o `f` germe único de
HG-1) dá a finitude do suporte restrito a esse `Set.univ`, exatamente como em HG-1.
Nenhum passo novo de prova foi necessário além da reindexação de `f`/
`finite_support_ord_f` para as versões de HG-1b — confirmando a expectativa do plano
de ataque da Onda 3 de que este item seria mecânico dado HG-1b fechado.

**A única complicação real, puramente de organização de arquivo, não de matemática:**
`AlgebraMapGermToFunctionFieldOrdMulProbe.lean` (HG-1b) vive em
`03_MILLENNIUM/05_HODGE/FORMAL/`, FORA da raiz de módulos do pacote Lake
(`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/`) — confirmado nesta sessão por
inspeção de `05_FORMAL/lean/lakefile.toml` (`[[lean_lib]] name = "TamesisLab"`) e de
`05_FORMAL/lean/TamesisLab.lean` (lista de `import TamesisLab.*`, nenhuma entrada para
arquivos de `03_MILLENNIUM/`). Ou seja: HG-1b é, tal como
`HolomorphicTransitionProbe.lean`/`ConjugationNotHolomorphicProbe.lean` citados na
tarefa deste item, um arquivo autônomo "import Mathlib apenas" fora do pacote Lake —
não existe um caminho de módulo Lean (`import ...`) que o alcance a partir de um novo
arquivo neste mesmo diretório solto. Por isso `f` e `finite_support_ord_f` não podem
ser referenciados por `import`; em vez disso, este arquivo reproduz o corpo de HG-1b
(de `import Mathlib` até `end AlgebraicGeometry.HG1B`, inclusive todas as declarações
intermediárias das quais `f`/`finite_support_ord_f` dependem: `testRing`, `testScheme`,
`algebraMap_eq_germToFunctionField`, os namespaces `Num`/`Den` completos, `f`,
`f_ne_zero`, `f_eq_div`, `f_div_surjective_witness`, `finite_support_ord_f`) **byte-
idêntico**, copiado diretamente do arquivo-fonte nesta sessão (não de memória nem
paráfrase), dentro do mesmo namespace `AlgebraicGeometry.HG1B`, e acrescenta apenas
`principalCycle_f` ao final, antes do `end` de fechamento da seção `noncomputable`.
Isto NÃO é uma nova prova do conteúdo de HG-1b — é reprodução textual do que já estava
comprovado, necessária apenas pela ausência de mecanismo de import entre arquivos
soltos fora do pacote Lake. A única linha genuinamente nova de conteúdo matemático
neste arquivo é a definição de `principalCycle_f` e seu comentário-docstring.

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1b já estavam verificados no
preâmbulo daquele arquivo (mesmo diretório) — não repetidos aqui por brevidade, ver
`AlgebraMapGermToFunctionFieldOrdMulProbe.lean`. Adicionalmente, para a construção de
`principalCycle_f`:
  - `AlgebraicGeometry.AlgebraicCycle`, campos `toFun`, `supportWithinDomain'`,
    `supportLocallyFiniteWithinDomain'` (`Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`)
    — mesma citação já verificada em HG-1 (`principal_divisor_algebraic_cycle_bridge.lean`).
  - `Filter.univ_mem` (`Mathlib/Order/Filter/Basic.lean`).
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de saída `0`) e
por busca textual (zero ocorrências dos marcadores proibidos pela governança do
laboratório).
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

end

end AlgebraicGeometry.HG1B
