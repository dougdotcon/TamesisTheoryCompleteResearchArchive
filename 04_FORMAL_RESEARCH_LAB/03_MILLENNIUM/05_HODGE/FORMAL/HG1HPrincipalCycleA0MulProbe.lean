/-
HG-1H (Wave 6, item WAVE6-HG-1H) — versão MULTIPLICATIVA do resultado
aditivo/de-subtração de HG-1G: em vez de decompor o ciclo de um QUOCIENTE
`genf a0 / genf b0` como a DIFERENÇA `principalCycle_a0 a0 - principalCycle_a0
b0` (HG-1G, `principalCycle_f_ab_eq_sub`), este arquivo tenta a identidade
"dual": o ciclo de um PRODUTO `a0 * b0` é a SOMA `principalCycle_a0 a0 +
principalCycle_a0 b0`, reusando `genf`/`finite_support_ord_genf`/
`principalCycle_a0`, JÁ parametrizados por `(a0 : ℤ) (ha0 : a0 ≠ 0)`, de
HG-1E (rascunho formal isolado, NÃO integrado a TamesisLab).

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
novidade matemática: "divisor de um produto = soma dos divisores dos
fatores" é clássico (ver, e.g., Hartshorne II.6, ou qualquer texto de
teoria de valorização — é a própria definição de valorização estendida
multiplicativamente); o que está formalizado aqui é apenas essa identidade
pontual, para QUAISQUER `a0, b0 : ℤ` não-nulos com `a0 * b0 ≠ 0`
(automático em `ℤ`, mas mantido como hipótese explícita para casar
exatamente com o enunciado do teste), reempacotada no tipo `AlgebraicCycle`
de Mathlib.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1h, especificado (após revisão
adversarial na etapa de planejamento da Onda 6) como:

  `principalCycle_a0_mul (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0)
  (hab : a0 * b0 ≠ 0) : principalCycle_a0 (a0 * b0) hab =
  principalCycle_a0 a0 ha0 + principalCycle_a0 b0 hb0`, via `ext` +
  `Function.locallyFinsuppWithin.coe_add` + `algebraMap_eq_genf` +
  `RingHom.map_mul` + `Scheme.ord_mul` + `Pi.add_apply` + `omega`/`ring`.

RESULTADO: SUCESSO. Mecânico dado HG-1E já fechado — nenhum lema novo de
Mathlib além dos já citados em HG-1E/HG-1G foi necessário; a única peça
extra é `map_mul` (`algebraMap` é um `RingHom`, logo uma instância de
`MonoidHomClass`) para obter `genf (a0 * b0) = genf a0 * genf b0` a partir
de `algebraMap_eq_genf`, o análogo EXATO — trocando divisão por
multiplicação — do papel que `div_mul_cancel₀` desempenhava em HG-1G para
obter `f_ab a0 b0 * genf b0 = genf a0`.

## O que realmente fechou o teste

**Inlining verbatim de HG-1C/HG-1E.** Todo o bloco de HG-1E
(`HG1EPrincipalCycleA0Probe.lean`, mesmo diretório), de `import Mathlib` até
`end AlgebraicGeometry.HG1C` (incluindo a seção `noncomputable section` com
`genf`, `finite_support_ord_genf`, `principalCycle_a0`, e a seção
`Instantiation`), foi copiado byte-idêntico para este arquivo nesta sessão
(diretamente do arquivo-fonte, não de memória nem paráfrase) — mesmo motivo
mecânico já documentado nos preâmbulos de HG-1D/HG-1E/HG-1F/HG-1G: este
arquivo, como HG-1E, vive em `03_MILLENNIUM/05_HODGE/FORMAL/`, fora da raiz
de módulos do pacote Lake (confirmado nesta sessão por reinspeção de
`05_FORMAL/lean/lakefile.toml` e `05_FORMAL/lean/TamesisLab.lean`, nenhuma
mudança desde a verificação de HG-1G), logo não há caminho de `import` de
um arquivo solto para outro; a única forma de reusar `genf`/
`finite_support_ord_genf`/`principalCycle_a0`/etc. aqui é reproduzir o
texto. Reusar o mesmo nome de namespace (`AlgebraicGeometry.HG1C`) num
arquivo novo, não importado pelo original, não causa nenhum conflito de
compilação — mesmo padrão já usado com sucesso por HG-1E/HG-1F/HG-1G.

**As declarações genuinamente novas — `genf_mul`, `principalCycle_a0_mul`.**
Parametrizadas sobre DOIS `a0 b0 : ℤ` mais a hipótese `hab : a0 * b0 ≠ 0`
(explícita no enunciado do teste, embora derivável de `ha0`/`hb0` em `ℤ` via
`mul_ne_zero` — mantida como argumento independente para casar exatamente
com a assinatura pedida), usando diretamente `genf`/`genf_ne_zero`/
`algebraMap_eq_genf`/`principalCycle_a0` de HG-1E — nenhuma redefinição:

```
lemma genf_mul (a0 b0 : ℤ) : genf (a0 * b0) = genf a0 * genf b0 := by
  rw [← algebraMap_eq_genf (a0 * b0), map_mul, algebraMap_eq_genf, algebraMap_eq_genf]

theorem principalCycle_a0_mul (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0)
    (hab : a0 * b0 ≠ 0) :
    principalCycle_a0 (a0 * b0) hab = principalCycle_a0 a0 ha0 + principalCycle_a0 b0 hb0 := ...
```

`genf_mul` é a chave: reescreve `genf (a0 * b0)` de volta para
`algebraMap ℤ testScheme.functionField (a0 * b0)` (via `algebraMap_eq_genf`,
sentido `←`), aplica `map_mul` (o fato de `algebraMap` ser homomorfismo de
anéis — instância genérica `MonoidHomClass`, o mesmo lema citado no teste
como `RingHom.map_mul`; `map_mul` é o nome atual em Mathlib para essa
instância genérica, ver seção "Nomes verificados"), e reescreve os dois
fatores resultantes de volta para `genf a0`/`genf b0` via `algebraMap_eq_genf`
(sentido `→`, duas vezes).

`principalCycle_a0_mul` segue EXATAMENTE o padrão de prova de
`principalCycle_f_ab_eq_sub` (HG-1G): `Function.locallyFinsuppWithin.ext`
reduz a um objetivo pontual; `Function.locallyFinsuppWithin.coe_add` +
`Pi.add_apply` (ambos `simp only`) desdobram o lado direito da SOMA de
ciclos (dual exato de `coe_sub`/`Pi.sub_apply` em HG-1G); `show` reafirma o
objetivo em termos de `testScheme.ord` (desdobramento definicional de
`principalCycle_a0`, mesmo truque já usado em HG-1G); `omega` fecha o
rearranjo aritmético final a partir de `hord : ord (genf (a0*b0)) x = ord
(genf a0) x + ord (genf b0) x` — obtida por `rw [genf_mul, Scheme.ord_mul
(genf_ne_zero a0 ha0) (genf_ne_zero b0 hb0)]`, a mesma identidade pontual de
`Scheme.ord_mul` já usada em HG-1G, aqui aplicada diretamente ao produto
`genf a0 * genf b0` (via `genf_mul`) em vez de à decomposição `f_ab * genf
b0 = genf a0` do quociente.

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1C/HG-1E já estavam
verificados nos preâmbulos daqueles arquivos (mesmo diretório) — não
repetidos aqui por brevidade. Adicionalmente, para `genf_mul`/
`principalCycle_a0_mul`:
  - `AlgebraicGeometry.AlgebraicCycle`, campos `toFun`, `supportWithinDomain'`,
    `supportLocallyFiniteWithinDomain'` (`Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`).
  - `Function.locallyFinsuppWithin.ext`, `.coe_add`
    (`Mathlib/Topology/LocallyFinsupp.lean`, linhas 348/352 nesta sessão —
    `coe_add` é o dual exato de `coe_sub`, já citado no preâmbulo de HG-1G,
    mesma declaração `[AddMonoid Y]`, aplicável aqui pois `AlgebraicCycle
    testScheme ℤ` tem estrutura de `AddCommGroup`/`AddMonoid` herdada de
    `ℤ`-valores).
  - `Pi.add_apply` (`Mathlib/Algebra/Group/Pi/Basic.lean`), dual de
    `Pi.sub_apply` já citado em HG-1G.
  - `Scheme.ord_mul` (`AlgebraicGeometry/OrderOfVanishing.lean:81-82`) —
    incondicional em `x`, já reconferido em HG-1F/HG-1G.
  - `map_mul` (Mathlib, `Mathlib/Algebra/Group/Hom/Defs.lean`, lema genérico
    de `MonoidHomClass`; `algebraMap ℤ testScheme.functionField` é um
    `RingHom`, que tem instância `RingHomClass`/`MonoidHomClass`, logo
    `map_mul (algebraMap ℤ testScheme.functionField) a0 b0` tem o tipo
    pedido — o teste cita `RingHom.map_mul`, nome mais antigo/específico
    para `RingHom`; `map_mul` é a forma atual, genérica, confirmada nesta
    sessão por compilação bem-sucedida via `rw`, que resolve o nome por
    elaboração de tipo).
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
construção `AlgebraicCycle` de que HG-1h precisa: aplicada duas vezes (a `a0` e a `b0`) e
uma terceira vez (a `a0 * b0`), ela é o único bloco necessário para o teste — ver seção
HG-1h abaixo. -/

/-- `ord (genf a0)`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`, empacotado como um termo de
`AlgebraicCycle testScheme ℤ` (HG-1E). -/
def principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (genf a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_genf a0 ha0⟩

/-!
## HG-1h (NOVO nesta sessão) — versão multiplicativa: `principalCycle_a0` de um produto
é a SOMA dos `principalCycle_a0` dos fatores

`genf_mul` mostra que `genf` transporta a multiplicação de `ℤ` para a multiplicação em
`testScheme.functionField`, via `algebraMap` (que já é um homomorfismo de anéis).
`principalCycle_a0_mul` é a decomposição pontual pedida pelo teste HG-1h: o ciclo de
`a0 * b0` é a SOMA dos ciclos de `a0` e `b0` — o análogo aditivo/multiplicativo exato de
`principalCycle_f_ab_eq_sub` (HG-1G), trocando quociente/diferença por produto/soma.
-/

/-- `genf` transporta produtos de `ℤ` para produtos em `testScheme.functionField`, via
`algebraMap` (homomorfismo de anéis). -/
lemma genf_mul (a0 b0 : ℤ) : genf (a0 * b0) = genf a0 * genf b0 := by
  rw [← algebraMap_eq_genf (a0 * b0), map_mul, algebraMap_eq_genf, algebraMap_eq_genf]

/-- **Resultado principal de HG-1h — a identidade pedida pelo teste.**
`principalCycle_a0 (a0 * b0)` (o ciclo do produto `a0 * b0`) é a SOMA, em
`AlgebraicCycle testScheme ℤ`, do ciclo de `a0` mais o ciclo de `b0` —
`principalCycle_a0 a0 ha0 + principalCycle_a0 b0 hb0`, para QUAISQUER `a0, b0 : ℤ`
não-nulos com `a0 * b0 ≠ 0`. Análogo multiplicativo exato de
`principalCycle_f_ab_eq_sub` de HG-1G (que decompunha o ciclo de um QUOCIENTE como
DIFERENÇA de ciclos); aqui o ciclo de um PRODUTO se decompõe como SOMA de ciclos —
ambos casos particulares da aditividade da valorização `ord` sobre `Scheme.ord_mul`. -/
theorem principalCycle_a0_mul (a0 b0 : ℤ) (ha0 : a0 ≠ 0) (hb0 : b0 ≠ 0)
    (hab : a0 * b0 ≠ 0) :
    principalCycle_a0 (a0 * b0) hab = principalCycle_a0 a0 ha0 + principalCycle_a0 b0 hb0 := by
  apply Function.locallyFinsuppWithin.ext
  intro x
  have hord : testScheme.ord (genf (a0 * b0)) x =
      testScheme.ord (genf a0) x + testScheme.ord (genf b0) x := by
    rw [genf_mul, Scheme.ord_mul (genf_ne_zero a0 ha0) (genf_ne_zero b0 hb0)]
  simp only [Function.locallyFinsuppWithin.coe_add, Pi.add_apply]
  show testScheme.ord (genf (a0 * b0)) x = testScheme.ord (genf a0) x + testScheme.ord (genf b0) x
  omega

end

/-! ## Verificação de instanciação: duas instâncias concretas obtidas por especialização
direta do resultado parametrizado acima, sem nenhuma duplicação de prova. -/

section Instantiation

/-- `principalCycle_a0_mul` instanciado em `a0 = 3`, `b0 = 2` (o par usado desde
HG-1b/HG-1F como caso concreto de referência): o ciclo de `3 * 2 = 6` é a soma dos
ciclos de `3` e `2`. -/
noncomputable example :
    principalCycle_a0 (3 * 2) (by decide) =
      principalCycle_a0 3 (by decide) + principalCycle_a0 2 (by decide) :=
  principalCycle_a0_mul 3 2 (by decide) (by decide) (by decide)

/-- Uma segunda instanciação, com um par `(a0, b0)` diferente (`a0 = 5`, `b0 = 7`),
verificando que a parametrização é genuína (não apenas uma reindexação sintática do caso
`3, 2`). -/
noncomputable example :
    principalCycle_a0 (5 * 7) (by decide) =
      principalCycle_a0 5 (by decide) + principalCycle_a0 7 (by decide) :=
  principalCycle_a0_mul 5 7 (by decide) (by decide) (by decide)

end Instantiation

/-! ## Verificação de dependências de prova (nesta sessão) — as duas declarações
genuinamente novas deste arquivo (HG-1h), confirmando que dependem apenas de
`[propext, Classical.choice, Quot.sound]` (nenhuma prova incompleta escapou pela síntese
de instâncias ou por elaboração implícita). -/

#print axioms genf_mul
#print axioms principalCycle_a0_mul

end AlgebraicGeometry.HG1C
