/-
HG-1B (Wave 2, item WAVE2-HG-1B) — algebraMap/germToFunctionField compatibility via
ord_mul decomposition of f = 3/2 (rascunho formal isolado, NÃO integrado a TamesisLab)

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
comutativa/geometria de esquemas clássica: NADA aqui usa estrutura complexa, cohomologia,
decomposição de Hodge, ou classe de ciclo. Mesmo em caso de sucesso total, o resultado
permanece a várias camadas inteiramente ausentes de sequer enunciar formalmente Hodge
(1,1), quanto mais a conjectura geral. Este item é continuação direta de HG-1
(`principal_divisor_algebraic_cycle_bridge.lean`, mesmo diretório), que deixou
explicitamente como trabalho futuro NÃO reivindicado como feito exatamente o passo que
este arquivo agora ataca — ver a seção "ESCOPO HONESTO" daquele arquivo.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1b, especificado (após revisão adversarial na etapa
de planejamento da Onda 2) como:

  Provar `algebraMap ℤ testScheme.functionField x =
  testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x)` para `x : ℤ`
  não-nulo via `Scheme.ΓSpecIso_inv` + desdobramento de `StructureSheaf.toStalk`.
  Decompor `f = 3/2` via `IsFractionRing.div_surjective (A := ℤ)`, aplicar a
  numerador/denominador, invocar `ord_mul`, reduzir a duas aplicações do argumento
  `finite_support_ord_f` de HG-1 (uma para `a0 = 3`, uma para `a0 = 2`).

RESULTADO: SUCESSO — mas por uma rota tecnicamente diferente da citada na proposta do
teste. Ver "O QUE REALMENTE FECHOU O TESTE" abaixo antes de reusar este arquivo.

## O que realmente fechou o teste (divergência honesta da proposta original)

**Passo 1 (compatibilidade `algebraMap`/`germToFunctionField`).** A rota citada na
proposta (`Scheme.ΓSpecIso_inv` + desdobrar `StructureSheaf.toStalk`) foi investigada e
o desdobramento manual (`rfl`, depois `simp [Scheme.ΓSpecIso_inv]` seguido de `rfl`) FALHA
— não por a igualdade ser falsa, mas por um obstáculo de síntese de instâncias mais
interessante do que o antecipado: a instância `Algebra ℤ X.functionField` que o Lean
efetivamente encontra para elaborar `algebraMap ℤ testScheme.functionField` NÃO é a
instância específica `Algebra R (Spec R).functionField` definida em
`FunctionField.lean:116` (via `StructureSheaf.toStalk`, indexada por `R : CommRingCat`),
e sim a instância canônica e completamente genérica `Ring.toIntAlgebra` (todo anel é
unicamente uma ℤ-álgebra). As duas instâncias são propositionalmente iguais — mas não
sintaticamente idênticas — logo `rfl`/`simp`+`rfl` sobre a forma desdobrada de
`toStalk`/`ΓSpecIso_inv` falha (confirmado por `set_option pp.all` nesta sessão: a
instância impressa para `Algebra ℤ testScheme.functionField` é literalmente
`Ring.toIntAlgebra`, não a instância indexada por `CommRingCat`).

A consequência prática MAIS relevante desse diamante de instâncias, descoberta também
nesta sessão: `IsFractionRing ℤ testScheme.functionField` **falha a sintetizar**
(`synthInstanceFailed`), mesmo com `functionField_isFractionRing_of_affine` instanciada
em Mathlib para `R := testRing`, porque essa instância de Mathlib é indexada pela
`Algebra R (Spec R).functionField` "certa" (a de `toStalk`), não pela `Ring.toIntAlgebra`
que a síntese de `algebraMap ℤ testScheme.functionField` efetivamente usa. Por isso este
arquivo evita `IsFractionRing.injective`/`IsFractionRing.div_surjective` para provar
qualquer fato de não-anulamento sobre `algebraMap ℤ testScheme.functionField` — usa em
vez disso a ponte `algebraMap_eq_genf` (abaixo) para reduzir sempre a
`germToFunctionField_injective`, que não depende dessa instância problemática.

O que efetivamente fecha o Passo 1: `Int.subsingleton_ringHom`
(`Data/Int/Cast/Lemmas.lean:351`, `Subsingleton (ℤ →+* R)`) — quaisquer dois
homomorfismos de anel `ℤ → R` coincidem, pois `ℤ` é objeto inicial em `CommRing`. Tanto
`algebraMap ℤ testScheme.functionField` quanto a composta
`(testScheme.germToFunctionField ⊤).hom.comp (Scheme.ΓSpecIso testRing).inv.hom` são
homomorfismos de anel `ℤ →+* testScheme.functionField`, logo são iguais por
`Subsingleton.elim`, e a igualdade pontual segue de `DFunLike.congr_fun`. Isto é, na
prática, **mais rotineiro** do que a rota original (nenhum desdobramento manual de
`toStalk`/`ΓSpecIso_inv` foi necessário) — confirmando a expectativa já registrada no
plano de ataque da Onda 2 de que esta extensão seria "mais rotineira do que o próprio
candidato ou o HG-1 original previam", ainda que pelo motivo técnico específico (unicidade
de homomorfismos de `ℤ`) não tivesse sido identificado antecipadamente.

**Passo 2 (decomposição `f = 3/2` e `ord_mul`).** `IsFractionRing.div_surjective (A := ℤ)`
(`RingTheory/Localization/FractionRing.lean:260`) garante, para QUALQUER
`z : testScheme.functionField`, a existência de `n d : ℤ` com `d ∈ nonZeroDivisors ℤ` e
`z = algebraMap n / algebraMap d` — mas a prova de existência em Mathlib usa escolha e não
garante devolver exatamente `n = 3, d = 2` para o `f` construído abaixo (poderia devolver,
em princípio, qualquer par equivalente, e.g. `6/4`). Como o teste pedia explicitamente
"reduzir a duas aplicações ... (a0=3, a0=2)" — isto é, quer as DUAS instâncias concretas
`a0 = 3` e `a0 = 2`, não um par arbitrário — `f` é *definido* diretamente na forma
`algebraMap Num.a0 / algebraMap Den.a0` (`Num.a0 := 3`, `Den.a0 := 2`), que já é,
por construção, um par testemunha válido da existência que `div_surjective` afirma (ver
`f_div_surjective_witness` abaixo, que empacota exatamente essa observação). Isto evita
depender do valor não-canônico que a prova de existência de Mathlib escolheria, mantendo
a álgebra honesta: a proposição geral de `div_surjective` é citada e usada como
justificativa de forma, mas os testemunhos concretos vêm de construção direta, não de
`obtain`.

A partir daí: `f * algebraMap Den.a0 = algebraMap Num.a0` (via `div_mul_cancel₀`, usando
`algebraMap Den.a0 ≠ 0`), depois `Scheme.ord_mul f_ne_zero hdmapne` dá
`ord f x + ord (algebraMap Den.a0) x = ord (algebraMap Num.a0) x` em todo ponto `x`, logo
`{x | ord f x ≠ 0} ⊆ {x | ord (algebraMap Num.a0) x ≠ 0} ∪ {x | ord (algebraMap Den.a0)
x ≠ 0}` — união de dois conjuntos finitos por reaplicação do argumento de HG-1
(`finite_support_ord_f`, aqui reproduzido duas vezes, como `Num.finite_support_ord_genf`
e `Den.finite_support_ord_genf`, um para `a0 = 3` e outro para `a0 = 2`, exatamente como
pedido pelo teste).

Nota sobre duplicação: o argumento de HG-1 (passos "básico aberto onde `aSec` é unidade" →
"fora do aberto é `a0 ∈ x.asIdeal`" → "em ℤ, primo contendo `a0≠0` é minimal sobre
`span{a0}`" → "primos minimais são finitos em anel Noetheriano") foi reproduzido
literalmente duas vezes (namespaces `Num` e `Den`), em vez de generalizado numa única
declaração parametrizada por `a0 : ℤ`, `a0 ≠ 0`. Uma tentativa de generalização com `a0`
como variável de seção falhou porque `Scheme.germToFunctionField` e `RingedSpace.
isUnit_res_basicOpen` exigem uma instância `[Nonempty (testScheme.basicOpen aSec)]`
disponível já na ELABORAÇÃO do enunciado das lemas subsequentes, e essa instância só pode
ser construída a partir da hipótese `a0 ≠ 0` (não é `instance` incondicional) — logo não
pode ser um argumento de instância comum sem também tornar `a0 ≠ 0` uma hipótese de
instância (o que Lean rejeita: "argument ... cannot be inferred using typeclass
synthesis"). A duplicação explícita evita esse impasse; é mecânica e verificada
independentemente em cada cópia.

## Nomes verificados (por grep e por compilação nesta sessão)

Contra o snapshot de Mathlib vendorizado em
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib/`, além de todos os nomes
já verificados em `principal_divisor_algebraic_cycle_bridge.lean` (HG-1, mesmo
diretório, cujas definições `testRing`/`testScheme`/o argumento de finitude são
replicadas aqui sob os namespaces `Num`/`Den` — ver nota de duplicação acima):
  - `Scheme.ΓSpecIso`, `Scheme.ΓSpecIso_inv` (`AlgebraicGeometry/Scheme.lean:623,642`)
  - `Int.subsingleton_ringHom` (`Data/Int/Cast/Lemmas.lean:351`)
  - `DFunLike.congr_fun` (`Mathlib/Logic/Basic.lean`/`Mathlib/Data/FunLike/Basic.lean`)
  - `IsFractionRing.div_surjective`
    (`RingTheory/Localization/FractionRing.lean:260`)
  - `mem_nonZeroDivisors_iff_ne_zero` (`RingTheory/Localization/Defs.lean` e cognatos)
  - `div_mul_cancel₀`, `div_ne_zero`
    (`Algebra/GroupWithZero/Units/Basic.lean:337,291`)
  - `functionField_isFractionRing_of_affine`, instância anônima `Algebra R (Spec
    R).functionField` (`AlgebraicGeometry/FunctionField.lean:113-118` — a instância cujo
    diamante com `Ring.toIntAlgebra` está documentado acima)
Todos conferidos por leitura direta do código-fonte nesta sessão (não apenas por grep de
nome) e todos usados abaixo passam pelo type-checker. Verificado com `lake env lean`
sobre este arquivo nesta sessão (código de saída `0`) e por busca textual (zero
ocorrências dos marcadores proibidos pela governança do laboratório).
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

end

end AlgebraicGeometry.HG1B
