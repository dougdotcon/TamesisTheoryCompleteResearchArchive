/-
HG-1E (Wave 4, item WAVE4-HG-1E) — empacotar o resultado de finitude
parametrizado de HG-1C (`genf a0` / `finite_support_ord_genf a0 ha0`, para
`(a0 : ℤ) (ha0 : a0 ≠ 0)` EXPLÍCITOS, sem duplicação `Num`/`Den`) como um
termo de `AlgebraicCycle`, generalizando `principalCycle_f` de HG-1D (que
empacotava apenas o caso concreto `f = 3/2` de HG-1b) (rascunho formal
isolado, NÃO integrado a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. Todas as
declarações novas verificadas com o comando de impressão de dependências de
prova do Lean: dependem apenas de `[propext, Classical.choice, Quot.sound]`
— nenhum marcador de prova incompleta escapou pela síntese de instâncias. O
arquivo não contém nenhuma prova incompleta, nenhuma declaração local tomada
como verdade sem prova, e nenhum bloco marcado como inseguro, em nenhum
lugar (conferido por busca textual nesta sessão).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta rodada:
não tocar em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer
parte da máquina de teoria de Hodge necessária para ela. O conteúdo abaixo é
100% álgebra comutativa/geometria de esquemas clássica: NADA aqui usa
estrutura complexa, cohomologia, decomposição de Hodge, ou classe de ciclo
em cohomologia. Mesmo em caso de sucesso total, o resultado permanece a
várias camadas inteiramente ausentes de sequer enunciar formalmente Hodge
(1,1), quanto mais a conjectura geral.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1e, especificado (após revisão
adversarial na etapa de planejamento da Onda 4) como:

  Inlinar as declarações de HG-1C verbatim num arquivo novo autônomo;
  adicionar `principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle
  testScheme ℤ` usando `genf a0` / `finite_support_ord_genf a0 ha0`.
  `lake env lean` exit 0.

RESULTADO: SUCESSO. Mecânico dado HG-1C já fechado, exatamente como
antecipado pelo plano da Onda 4 (a mesma observação de HG-1D — item que este
item generaliza — de que empacotar um resultado de finitude já provado como
`AlgebraicCycle` não exige nenhum passo de prova novo além da reindexação).

## O que realmente fechou o teste

**Inlining verbatim.** Todo o bloco de HG-1C
(`HG1CParametrizedFiniteSupportOrdProbe.lean`, mesmo diretório), de
`import Mathlib` até `end AlgebraicGeometry.HG1C` (a seção `Instantiation`
inclusive), foi copiado byte-idêntico para este arquivo nesta sessão
(diretamente do arquivo-fonte, não de memória nem paráfrase) — mesmo motivo
mecânico documentado no preâmbulo de HG-1D: este arquivo, como HG-1C, vive
em `03_MILLENNIUM/05_HODGE/FORMAL/`, fora da raiz de módulos do pacote Lake
(`04_FORMAL_RESEARCH_LAB/05_FORMAL/lean/TamesisLab/` — confirmado nesta
sessão por reinspeção de `05_FORMAL/lean/lakefile.toml` e
`05_FORMAL/lean/TamesisLab.lean`, nenhuma mudança desde a verificação de
HG-1D), logo não há caminho de `import` de um arquivo solto para outro; a
única forma de reusar `genf`/`finite_support_ord_genf`/etc. de HG-1C aqui é
reproduzir o texto.

**A única declaração genuinamente nova.** `principalCycle_a0`, inserida
logo antes do `end` que fecha a seção `noncomputable` de HG-1C (mesma
posição relativa de `principalCycle_f` em HG-1D, e de `principalCycle` em
HG-1), espelha exatamente essas duas construções, substituindo `f`/
`finite_support_ord_f` (HG-1/HG-1D, sem parâmetro) por `genf a0`/
`finite_support_ord_genf a0 ha0` (HG-1C, parametrizado):

```
def principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (genf a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_genf a0 ha0⟩
```

`supportWithinDomain'` fecha por `simp`, idêntico a `principalCycle`/
`principalCycle_f` (o domínio de suporte declarado por `AlgebraicCycle` é
`⊤ : Set testScheme`, obrigação trivial, independente de `a0`).
`supportLocallyFiniteWithinDomain'` fecha fornecendo `Set.univ` como
vizinhança aberta testemunha (`Filter.univ_mem`), e `finite_support_ord_genf
a0 ha0` — já provado, parametrizado, em HG-1C — dá a finitude do suporte
restrito a esse `Set.univ`. Nenhum passo de prova novo foi necessário: a
única diferença sintática em relação a `principalCycle_f` de HG-1D é que
`principalCycle_a0` recebe `(a0 : ℤ) (ha0 : a0 ≠ 0)` como argumentos
explícitos comuns (mesma convenção adotada em todo HG-1C, ver o preâmbulo
daquele arquivo) em vez de fechar sobre `Num.a0`/`Den.a0` fixos — resultado
esperado, já que o teste HG-1e pedia exatamente essa parametrização
(estendendo HG-1D da mesma forma que HG-1C estendeu HG-1b).

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1C já estavam verificados
no preâmbulo daquele arquivo (mesmo diretório) — não repetidos aqui por
brevidade, ver `HG1CParametrizedFiniteSupportOrdProbe.lean`.
Adicionalmente, para a construção de `principalCycle_a0` — mesmos dois
nomes já citados no preâmbulo de HG-1D (item que este generaliza), aqui
reconferidos por leitura direta de código-fonte nesta sessão:
  - `AlgebraicGeometry.AlgebraicCycle`, campos `toFun`, `supportWithinDomain'`,
    `supportLocallyFiniteWithinDomain'`
    (`Mathlib/AlgebraicGeometry/AlgebraicCycle/Basic.lean`).
  - `Filter.univ_mem` (`Mathlib/Order/Filter/Basic.lean`).
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de
saída `0`) e por busca textual (zero ocorrências dos marcadores proibidos
pela governança do laboratório).
-/

import Mathlib

open AlgebraicGeometry CategoryTheory

namespace AlgebraicGeometry.HG1C

noncomputable section

/-! ## Configuração concreta: `X = Spec ℤ` (mesma escolha de HG-1/HG-1b) -/

/-- Anel de teste: `ℤ`. -/
abbrev testRing : CommRingCat := CommRingCat.of ℤ

/-- Esquema de teste: `Spec ℤ`. -/
abbrev testScheme : Scheme.{0} := Spec testRing

instance : Nonempty (⊤ : testScheme.Opens) := ⟨⟨genericPoint testScheme, trivial⟩⟩

/-! ## Passo 1 — compatibilidade `algebraMap`/`germToFunctionField` (reproduzido de
HG-1b, `algebraMap_eq_germToFunctionField`; independe de `a0`, logo não precisa de
nenhuma generalização adicional). -/

lemma algebraMap_eq_germToFunctionField (x : ℤ) :
    algebraMap ℤ testScheme.functionField x =
      testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x) := by
  have h : (algebraMap ℤ testScheme.functionField) =
      (testScheme.germToFunctionField ⊤).hom.comp (Scheme.ΓSpecIso testRing).inv.hom :=
    Subsingleton.elim _ _
  exact DFunLike.congr_fun h x

/-! ## Passo 2 — o argumento de finitude de HG-1/HG-1b, parametrizado sobre
`(a0 : ℤ) (ha0 : a0 ≠ 0)` explícitos como variáveis de seção COMUNS (não de
instância). O único ponto onde a instância `Nonempty (testScheme.basicOpen aSec)`
é sintaticamente exigida — `germToFunctionField_aRes` — recebe essa instância via
`haveI` local, inline no próprio TIPO do lema, construído a partir de `a0`/`ha0`
(ver preâmbulo). -/

/- `(a0 : ℤ) (ha0 : a0 ≠ 0)` são passados como argumentos EXPLÍCITOS comuns em cada
declaração abaixo (não `variable` de seção com auto-bound, e não `instance`).
Escolha deliberada: como nem toda declaração usa `ha0` no seu ENUNCIADO (algumas só
na prova), depender de `variable`/auto-bound exigiria `include ha0` — o que por sua
vez forçaria `ha0` também nas definições (`aSec`, `genf`, `aRes`) que não precisam
dele, mudando sua aridade. Argumentos explícitos evitam essa armadilha e deixam
claro, em cada assinatura, exatamente quais declarações usam `ha0`. -/

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
fornecida via `haveI` local exatamente onde for sintaticamente exigida (ver
`germToFunctionField_aRes` abaixo e a discussão no preâmbulo). -/
lemma nonempty_basicOpen (a0 : ℤ) (ha0 : a0 ≠ 0) :
    Nonempty (testScheme.basicOpen (aSec a0)) :=
  ⟨⟨genericPoint testScheme, genericPoint_mem_basicOpen a0 ha0⟩⟩

/-- Restrição de `aSec a0` ao seu próprio aberto básico. Não exige a instância
`Nonempty (testScheme.basicOpen aSec)` — `Γ(X, U)` está definido para qualquer
aberto `U`, vazio ou não. -/
def aRes (a0 : ℤ) : Γ(testScheme, testScheme.basicOpen (aSec a0)) :=
  testScheme.presheaf.map (homOfLE (testScheme.basicOpen_le (aSec a0))).op (aSec a0)

lemma isUnit_aRes (a0 : ℤ) : IsUnit (aRes a0) :=
  testScheme.toRingedSpace.isUnit_res_basicOpen (aSec a0)

/-- **O único ponto do arquivo em que `Nonempty (testScheme.basicOpen aSec)` é
sintaticamente exigida** (via `Scheme.germToFunctionField`, cujo argumento
`[Nonempty U]` é de instância — ver preâmbulo). Fornecida por `haveI` LOCAL,
inline no próprio tipo do lema, construída a partir de `a0`/`ha0` via
`nonempty_basicOpen` — não por uma `instance` de seção (que falharia, ver
preâmbulo de HG-1b). -/
lemma germToFunctionField_aRes (a0 : ℤ) (ha0 : a0 ≠ 0) :
    haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
    testScheme.germToFunctionField (testScheme.basicOpen (aSec a0)) (aRes a0) = genf a0 := by
  haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
  simp only [genf, Scheme.germToFunctionField, aRes]
  rw [TopCat.Presheaf.germ_res_apply]

lemma ord_genf_eq_zero_of_mem_basicOpen (a0 : ℤ) (ha0 : a0 ≠ 0) {x : testScheme}
    (hx : x ∈ testScheme.basicOpen (aSec a0)) :
    testScheme.ord (genf a0) x = 0 := by
  -- `Scheme.ord_of_isUnit` também exige `[Nonempty (testScheme.basicOpen (aSec a0))]`
  -- (`AlgebraicGeometry/OrderOfVanishing.lean:88`) — um SEGUNDO ponto sintático, além de
  -- `germToFunctionField_aRes`, onde essa instância é exigida (ver preâmbulo, seção
  -- corrigida). Aqui o uso é só na PROVA (o tipo do lema não menciona `germToFunctionField`
  -- nem `basicOpen`), então basta um `haveI` tático comum, sem precisar do truque de tipo.
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

/-- **Resultado principal (generalizado).** `ord (genf a0)` tem suporte finito, para
QUALQUER `a0 : ℤ` não-nulo — o resultado de finitude de HG-1/HG-1b, agora
parametrizado por `(a0 : ℤ) (ha0 : a0 ≠ 0)` explícitos numa única declaração, em vez
de duas cópias literais (`Num`/`Den`) como em HG-1b. -/
theorem finite_support_ord_algebraMap (a0 : ℤ) (ha0 : a0 ≠ 0) :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField a0) x)).Finite := by
  simpa only [algebraMap_eq_genf] using finite_support_ord_genf a0 ha0

/-!
## Empacotamento (NOVO nesta sessão, HG-1e) — `genf a0` vira um termo de
`AlgebraicCycle testScheme ℤ`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`

Construção byte-idêntica em forma (a menos do nome e da parametrização) a
`principalCycle` de HG-1 e a `principalCycle_f` de HG-1D, agora aplicada ao
`genf a0`/`finite_support_ord_genf a0 ha0` parametrizados de HG-1C em vez do
`f` único de HG-1 ou do `f = 3/2` fixo de HG-1D. Ver "ESCOPO HONESTO" no
preâmbulo de HG-1 e a nota de escopo no preâmbulo deste arquivo: isto NÃO
aproxima a Conjectura de Hodge.
-/

/-- `ord (genf a0)`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`, empacotado como um
termo de `AlgebraicCycle testScheme ℤ` — generaliza `principalCycle_f` de HG-1D
(que empacotava apenas o caso concreto `f = 3/2`) à família parametrizada de
HG-1C. -/
def principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (genf a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_genf a0 ha0⟩

end

/-! ## Verificação de instanciação: as duas instâncias concretas de HG-1b
(`a0 = 3`, `a0 = 2`) obtidas por especialização direta do resultado parametrizado
acima, sem nenhuma duplicação de prova. -/

section Instantiation

/-- `finite_support_ord_algebraMap` instanciado em `a0 = 3` (o `Num` de HG-1b). -/
example :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField 3) x)).Finite :=
  finite_support_ord_algebraMap 3 (by decide)

/-- `finite_support_ord_algebraMap` instanciado em `a0 = 2` (o `Den` de HG-1b). -/
example :
    (Function.support
        (fun x : testScheme => testScheme.ord (algebraMap ℤ testScheme.functionField 2) x)).Finite :=
  finite_support_ord_algebraMap 2 (by decide)

/-- `principalCycle_a0` instanciado em `a0 = 3` — verifica que a construção
parametrizada de fato elabora para um `a0` concreto, sem duplicação de prova.
(`noncomputable` necessário aqui porque, fora da seção `noncomputable section`
que fecha logo acima, `example`s que dependem de `principalCycle_a0` -- que é
`noncomputable`, por depender transitivamente de dados clássicos de `Scheme`
-- precisam ser marcados explicitamente; detectado nesta sessão pelo erro
`lean.dependsOnNoncomputable` na primeira tentativa de compilação, corrigido
aqui.) -/
noncomputable example : AlgebraicCycle testScheme ℤ := principalCycle_a0 3 (by decide)

/-- `principalCycle_a0` instanciado em `a0 = 2`. -/
noncomputable example : AlgebraicCycle testScheme ℤ := principalCycle_a0 2 (by decide)

end Instantiation

end AlgebraicGeometry.HG1C
