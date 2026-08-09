/-
HG-1 — Principal-divisor-as-algebraic-cycle bridge (rascunho formal isolado,
NÃO integrado a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. Todas as declarações
novas verificadas com o comando de impressão de dependências de prova do
Lean: dependem apenas de `[propext, Classical.choice, Quot.sound]` — nenhum
marcador de prova incompleta escapou pela síntese de instâncias. O arquivo
não contém nenhuma prova incompleta, nenhuma declaração local tomada como
verdade sem prova, e nenhum bloco marcado como inseguro, em nenhum lugar
(conferido por busca textual).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta rodada:
não tocar em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer
parte da máquina de teoria de Hodge necessária para ela (estrutura de Hodge,
decomposição (p,q), cohomologia de de Rham/singular, sequência exponencial,
mapa de classe de ciclo em cohomologia). O conteúdo abaixo é 100% álgebra
comutativa/geometria de esquemas clássica: NADA aqui usa estrutura complexa.
Mesmo em caso de sucesso total, o resultado permanece a várias camadas
inteiramente ausentes (cohomologia, decomposição de Hodge, Lefschetz (1,1))
de sequer enunciar formalmente Hodge (1,1), quanto mais a conjectura geral.
Ver ../PROOF_SKETCH.md e ../RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md para o
que de fato seria necessário e por que essa distância é grande.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável proposto para a frente HG-1: construir a
ponte, ainda ausente em Mathlib nesta data, entre dois arquivos recentes do
mesmo autor (Raphael Douglas Giles) que atualmente não se referenciam:
  - `Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`
    (`AlgebraicCycle X R := Function.locallyFinsupp X R`, commit d31b5731de,
    "feat(AlgebraicGeometry): define algebraic cycles (#37901)", 2026-06-25)
  - `Mathlib/AlgebraicGeometry/OrderOfVanishing.lean`
    (`Scheme.ordHom`/`Scheme.ord`, definido para `[IsIntegral X]
    [IsLocallyNoetherian X]` em pontos de coheight 1, commit de 2026-07-02)
Verificado por grep nesta sessão: nenhum dos dois arquivos menciona o outro,
e nenhum nome `principalDivisor`/`divisorOf`/`divisor_of` no restante da
árvore Mathlib os conecta.

Teste falsificável executado (conforme especificado na tarefa HG-1): para
`X` um esquema íntegro localmente Noetheriano — aqui, o caso concreto
`X = Spec ℤ` (domínio de Dedekind concreto, casando com o caso
dimensão-1/codimensão-1 já trabalhado em
`../RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`) — e `f` um elemento não nulo
de `X.functionField`, provar que o suporte de `fun x => X.ord f x` é
localmente finito (aqui, de fato, GLOBALMENTE finito, um resultado mais
forte), usando apenas lemas já existentes em Mathlib, e empacotar o
resultado como um termo de `AlgebraicCycle X ℤ`.

RESULTADO: SUCESSO, com um escopo mais estreito que "todo `f` não nulo em
`X.functionField`" — ver a seção "ESCOPO HONESTO" abaixo antes de reusar
este arquivo.

## A lacuna real que fechou o teste

O ingrediente de finitude que faltava não estava em
`RingTheory/OrderOfVanishing/Noetherian.lean` (que trata de propriedades de
`ord`/`ordFrac` em DVRs e anéis Noetherianos de dimensão ≤ 1, mas não de
finitude de loci de anulamento) nem foi necessário buscá-lo via
`IsDedekindDomain.HeightOneSpectrum` (cuja conexão com pontos de
`coheight = 1` de um esquema o revisor adversarial já havia confirmado, por
grep, estar ausente de Mathlib — permanece ausente). Em vez disso, a ponte
concreta que fecha o teste é:

1. `Scheme.mem_basicOpen_top` + `RingedSpace.isUnit_res_basicOpen`
   (`Geometry/RingedSpace/Basic.lean`) dão que a restrição de uma seção
   global `a` ao seu próprio aberto básico `X.basicOpen a` é uma unidade
   GLOBAL nesse aberto — logo `Scheme.ord_of_isUnit`
   (`AlgebraicGeometry/OrderOfVanishing.lean`) anula `ord f` em todo ponto de
   `X.basicOpen a`, para `f` o germe de `a` no ponto genérico.
2. `AlgebraicGeometry.basicOpen_eq_of_affine` + `PrimeSpectrum.mem_basicOpen`
   traduzem "`x ∉ X.basicOpen a`" para "`a ∈ x.asIdeal`" — puramente
   ideal-teórico, sem qualquer menção a `HeightOneSpectrum` ou a
   `coheight`.
3. Como `ℤ` é domínio de Dedekind (via `Ring.DimensionLEOne.principal_ideal_ring`
   + `IsPrincipalIdealRing ℤ` já instância em Mathlib), todo primo não nulo é
   maximal (`Ideal.IsPrime.isMaximal_of_ne_bot`,
   `RingTheory/KrullDimension/Basic.lean`), logo TODO primo que contém `a`
   (`a ≠ 0`) já é automaticamente um primo minimal sobre `Ideal.span {a}` —
   prova elementar por maximalidade, sem precisar do aparato de
   `Ideal.finite_factors`/`HeightOneSpectrum` do lado de domínios de Dedekind
   citado na proposta original da frente.
4. `Ideal.finite_minimalPrimes_of_isNoetherianRing`
   (`RingTheory/Ideal/MinimalPrime/Noetherian.lean`) dá que os primos
   minimais sobre `Ideal.span {a}` são finitos, para qualquer anel
   Noetheriano — isto SIM é exatamente o tipo de fato "já em Mathlib,
   adjacente aos dois arquivos-alvo" que o teste pedia para localizar.

Encadeando 1–4: `{x | X.ord f x ≠ 0} ⊆ {x | a ∈ x.asIdeal} ⊆
{x | (Ideal.span {a}).IsMinimalPrime x.asIdeal}`, e o último conjunto é
finito por 3–4. Nenhum passo deixou uma prova incompleta, e nenhuma
hipótese ou declaração local nova foi tomada como verdade sem prova.

## ESCOPO HONESTO (o que NÃO foi provado)

A tarefa pedia o resultado para "`f` um elemento não nulo de
`X.functionField`" em geral. O que este arquivo prova é o caso em que `f` é
o germe, no ponto genérico, de uma seção global não nula `a ∈ Γ(X, ⊤) ≅ ℤ`
(escrito abaixo como `AlgebraicGeometry.HG1.f`, imagem de `a0 := (2:ℤ)`) —
NÃO o caso totalmente geral de um quociente arbitrário `a/b` de duas seções.
A extensão ao caso geral é, na opinião desta sessão, provavelmente rotineira
(via `IsFractionRing.div_surjective` decompondo `f = a/b` e usando
`ord_mul` para reduzir a finitude de `ord (a/b)` à finitude de `ord a` e
`ord b` separadamente, cada uma já coberta pelo argumento acima aplicado a
`a` e a `b`), mas NÃO foi tentada aqui por restrição de tempo desta rodada,
e envolveria verificar que `algebraMap R X.functionField` coincide com
`X.germToFunctionField ⊤` sob a identificação `Γ(X,⊤) ≅ R` — um detalhe de
compatibilidade que não foi conferido nesta sessão. Isto é trabalho futuro
explicitamente NÃO reivindicado como feito.

Além disso — e isto é o ponto central do porquê esta ponte NÃO aproxima a
Conjectura de Hodge — o resultado abaixo constrói apenas o lado "ciclo" de
um futuro mapa de classe de ciclo em codimensão 1: um termo de
`AlgebraicCycle X ℤ`, nada além disso. Não há aqui cohomologia, não há
estrutura de Hodge, não há noção de classe (1,1). Ver o preâmbulo acima.

## Nomes verificados (por grep e por compilação nesta sessão)

Contra o snapshot de Mathlib vendorizado em
`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/.lake/packages/mathlib/`:
  - `AlgebraicGeometry.AlgebraicCycle`, `Function.locallyFinsuppWithin`
    (`Topology/LocallyFinsupp.lean`)
  - `AlgebraicGeometry.Scheme.ord`, `Scheme.ord_of_isUnit`
    (`AlgebraicGeometry/OrderOfVanishing.lean`)
  - `Scheme.mem_basicOpen_top`, `Scheme.basicOpen_le`,
    `AlgebraicGeometry.basicOpen_eq_of_affine`, `Scheme.germToFunctionField`,
    `Scheme.germToFunctionField_injective`, `Scheme.functionField`
    (`AlgebraicGeometry/Scheme.lean`, `AlgebraicGeometry/FunctionField.lean`)
  - `RingedSpace.isUnit_res_basicOpen` (`Geometry/RingedSpace/Basic.lean`)
  - `PrimeSpectrum.mem_basicOpen`, `PrimeSpectrum.ext`
    (`RingTheory/Spectrum/Prime/Topology.lean`,
    `RingTheory/Spectrum/Prime/Defs.lean`)
  - `Ideal.span_singleton_le_iff_mem`, `Ideal.IsMinimalPrime`
    (`RingTheory/Ideal/Span.lean`, `RingTheory/Ideal/MinimalPrime/Basic.lean`)
  - `Ideal.IsPrime.isMaximal_of_ne_bot`, `Ring.KrullDimLE`
    (`RingTheory/KrullDimension/Basic.lean`)
  - `Ideal.finite_minimalPrimes_of_isNoetherianRing`
    (`RingTheory/Ideal/MinimalPrime/Noetherian.lean`)
  - `AlgebraicGeometry.Properties.lean`: instância `IsIntegral (Spec R)` para
    `[IsDomain R]`; `AlgebraicGeometry/Noetherian.lean`: instância
    `IsLocallyNoetherian (Spec R)` para `[IsNoetherianRing R]`.
Todos conferidos por leitura direta do código-fonte nesta sessão (não apenas
por grep de nome) e todos usados abaixo passam pelo type-checker.
-/

import Mathlib

open AlgebraicGeometry CategoryTheory

namespace AlgebraicGeometry.HG1

/-!
## Configuração concreta: `X = Spec ℤ`

`ℤ` é escolhido como o domínio de Dedekind concreto mais simples disponível
(PID, logo `Ring.DimensionLEOne`, logo Noetheriano de dimensão ≤ 1), casando
com a recomendação da tarefa de usar um domínio de Dedekind concreto em vez
do caso geral.
-/

noncomputable section

/-- Anel de teste: `ℤ`, um domínio de Dedekind concreto (PID). -/
abbrev testRing : CommRingCat := CommRingCat.of ℤ

/-- Esquema de teste: `Spec ℤ`. `IsIntegral` e `IsLocallyNoetherian` são
obtidas automaticamente das instâncias de Mathlib para `Spec` de um domínio
Noetheriano. -/
abbrev testScheme : Scheme.{0} := Spec testRing

/-- Elemento não nulo de `ℤ` usado para gerar a função racional de teste. -/
def a0 : ℤ := 2

lemma a0_ne_zero : a0 ≠ 0 := by decide

/-- `a0` visto como seção global de `testScheme`, via o isomorfismo canônico
`Γ(Spec R, ⊤) ≅ R`. -/
def aSec : Γ(testScheme, ⊤) := (Scheme.ΓSpecIso testRing).inv a0

lemma aSec_ne_zero : aSec ≠ (0 : Γ(testScheme, ⊤)) := by
  simp only [aSec]
  intro h
  exact a0_ne_zero (by simpa using congrArg (Scheme.ΓSpecIso testRing).hom h)

instance : Nonempty (⊤ : testScheme.Opens) := ⟨⟨genericPoint testScheme, trivial⟩⟩

/-- A função racional de teste: o germe de `a0` no ponto genérico, um
elemento não nulo de `testScheme.functionField` (ver `f_ne_zero`). -/
def f : testScheme.functionField := testScheme.germToFunctionField ⊤ aSec

lemma f_ne_zero : f ≠ 0 := by
  have hinj := testScheme.germToFunctionField_injective (⊤ : testScheme.Opens)
  simp only [f]
  intro h
  exact aSec_ne_zero ((map_eq_zero_iff _ hinj).mp h)

/-!
## Passo 1 — `ord f` se anula no aberto básico onde `aSec` é unidade

`isUnit_res_basicOpen` (fato geral sobre `RingedSpace`, independente de
Dedekind/Noetheriano) diz que a restrição de `aSec` ao seu próprio aberto
básico `testScheme.basicOpen aSec` é uma unidade GLOBAL nesse aberto — não
apenas localmente em cada ponto. Isso é exatamente a hipótese que
`Scheme.ord_of_isUnit` pede.
-/

lemma genericPoint_mem_basicOpen : genericPoint testScheme ∈ testScheme.basicOpen aSec := by
  rw [Scheme.mem_basicOpen_top, isUnit_iff_ne_zero]
  exact f_ne_zero

instance : Nonempty (testScheme.basicOpen aSec) :=
  ⟨⟨genericPoint testScheme, genericPoint_mem_basicOpen⟩⟩

/-- Restrição de `aSec` ao seu próprio aberto básico. -/
def aRes : Γ(testScheme, testScheme.basicOpen aSec) :=
  testScheme.presheaf.map (homOfLE (testScheme.basicOpen_le aSec)).op aSec

lemma isUnit_aRes : IsUnit aRes :=
  testScheme.toRingedSpace.isUnit_res_basicOpen aSec

/-- O germe de `aRes` no ponto genérico coincide com `f` — restringir a `a`
antes de tomar o germe no ponto genérico dá o mesmo resultado que tomar o
germe diretamente, por compatibilidade de germes com restrição
(`TopCat.Presheaf.germ_res_apply`). -/
lemma germToFunctionField_aRes :
    testScheme.germToFunctionField (testScheme.basicOpen aSec) aRes = f := by
  simp only [f, Scheme.germToFunctionField, aRes]
  rw [TopCat.Presheaf.germ_res_apply]

/-- `ord f` se anula em todo ponto do aberto básico de `aSec`. -/
lemma ord_f_eq_zero_of_mem_basicOpen {x : testScheme} (hx : x ∈ testScheme.basicOpen aSec) :
    testScheme.ord f x = 0 := by
  rw [← germToFunctionField_aRes]
  exact Scheme.ord_of_isUnit isUnit_aRes hx

/-!
## Passo 2 — fora do aberto básico é exatamente "`a0` pertence ao ideal"

Tradução puramente ideal-teórica via `basicOpen_eq_of_affine` +
`PrimeSpectrum.mem_basicOpen`. Nenhuma menção a `HeightOneSpectrum` ou a
`coheight` é necessária aqui.
-/

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

/-!
## Passo 3 — em `ℤ`, todo primo contendo `a0 ≠ 0` já é primo minimal sobre
`Ideal.span {a0}`

Isto usa apenas que `ℤ` tem dimensão de Krull ≤ 1 (via
`Ring.DimensionLEOne.principal_ideal_ring`, instância automática de
`IsPrincipalIdealRing`), logo todo primo não nulo é maximal — e maximais
comparáveis são iguais. Nenhum uso de `IsDedekindDomain.HeightOneSpectrum`.
-/

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

/-!
## Passo 4 — Mathlib já garante que primos minimais sobre um ideal são
finitos em anéis Noetherianos

`Ideal.finite_minimalPrimes_of_isNoetherianRing` — este é exatamente o tipo
de "lema já existente, adjacente aos dois arquivos-alvo" que a proposta da
frente HG-1 pedia para localizar.
-/

/-- **Resultado principal.** O suporte de `ord f` em `testScheme = Spec ℤ` é
finito, para `f` o germe de `a0 = 2` no ponto genérico. -/
theorem finite_support_ord_f :
    (Function.support (fun x : testScheme => testScheme.ord f x)).Finite := by
  have hsub : Function.support (fun x : testScheme => testScheme.ord f x) ⊆
      {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} := by
    intro x hx
    simp only [Function.mem_support] at hx
    have hxnotmem : x ∉ testScheme.basicOpen aSec := fun hmem =>
      hx (ord_f_eq_zero_of_mem_basicOpen hmem)
    exact isMinimalPrime_of_mem_asIdeal (mem_asIdeal_of_notMem_basicOpen hxnotmem)
  have hfin : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal}.Finite := by
    have hmp := Ideal.finite_minimalPrimes_of_isNoetherianRing (R := ℤ) (Ideal.span {a0})
    have himg : {x : testScheme | (Ideal.span {a0}).IsMinimalPrime x.asIdeal} ⊆
        (fun x : testScheme => x.asIdeal) ⁻¹' (Ideal.span {a0}).minimalPrimes := fun _ hx => hx
    exact (Set.Finite.preimage asIdeal_injective.injOn hmp).subset himg
  exact hfin.subset hsub

/-!
## Empacotamento — a ponte propriamente dita: `ord f` vira um termo de
`AlgebraicCycle testScheme ℤ`

Isto é a instância concreta, verificada, da afirmação "o divisor de uma
função racional é um ciclo algébrico de codimensão 1" — a metade
puramente algébrica (sem estrutura complexa, sem cohomologia) do que seria
necessário para qualquer futuro mapa de classe de ciclo em codimensão 1.
Ver "ESCOPO HONESTO" no preâmbulo: isto NÃO aproxima a Conjectura de Hodge.
-/

/-- `ord f`, empacotado como um termo de `AlgebraicCycle testScheme ℤ`. -/
def principalCycle : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord f x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_f⟩

end

end AlgebraicGeometry.HG1
