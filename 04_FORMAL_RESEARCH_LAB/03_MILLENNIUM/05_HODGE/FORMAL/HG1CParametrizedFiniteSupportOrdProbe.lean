/-
HG-1C (Wave 3, item WAVE3-HG-1C) — parametrizar o resultado de finitude de HG-1b
sobre `(a0 : ℤ) (ha0 : a0 ≠ 0)` explícitos, evitando a duplicação `Num`/`Den`
(rascunho formal isolado, NÃO integrado a TamesisLab)

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. Todas as declarações
novas verificadas com o comando de impressão de dependências de prova do Lean:
dependem apenas de `[propext, Classical.choice, Quot.sound]` — nenhum marcador
de prova incompleta escapou pela síntese de instâncias. O arquivo não contém
nenhuma prova incompleta, nenhuma declaração local tomada como verdade sem
prova, e nenhum bloco marcado como inseguro, em nenhum lugar (conferido por
busca textual nesta sessão).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta rodada:
não tocar em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer
parte da máquina de teoria de Hodge necessária para ela. O conteúdo abaixo é
100% álgebra comutativa/geometria de esquemas clássica: NADA aqui usa
estrutura complexa, cohomologia, decomposição de Hodge, ou classe de ciclo.
Mesmo em caso de sucesso total, o resultado permanece a várias camadas
inteiramente ausentes de sequer enunciar formalmente Hodge (1,1), quanto mais
a conjectura geral. Este item é continuação direta de HG-1b
(`AlgebraMapGermToFunctionFieldOrdMulProbe.lean`, mesmo diretório), que
deixou explicitamente registrada, no seu preâmbulo (seção "Nota sobre
duplicação"), a tentativa de generalização aqui reatacada como NÃO bem
sucedida por uma rota ingênua, e como trabalho futuro possível por outra
rota — ver abaixo.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1c, especificado (após revisão
adversarial na etapa de planejamento da Onda 3) como:

  Generalizar o resultado de finitude de HG-1b sobre `(a0 : ℤ)`
  `(ha0 : a0 ≠ 0)` explícitos, usando `haveI` local por lema para a
  instância `Nonempty (testScheme.basicOpen aSec)` construída a partir de
  `a0`/`ha0`, em vez de depender de derivação automática em nível
  `variable`.

RESULTADO: SUCESSO. O diagnóstico exato do preâmbulo de HG-1b está correto —
uma tentativa de tornar `Nonempty (testScheme.basicOpen aSec)` uma `instance`
de seção parametrizada por `a0 ≠ 0` FALHA, pelo motivo já lá documentado
(precisaria de `a0 ≠ 0` como hipótese de instância, o que Lean rejeita). Mas
o teste HG-1c pedia especificamente uma rota DIFERENTE — `haveI` local por
lema, não `instance` de seção — e essa rota funciona, fechando a
generalização pedida sem duplicação `Num`/`Den`.

## O que realmente fechou o teste

Divergência honesta de uma frase inicial deste preâmbulo (corrigida nesta
versão após a primeira tentativa de compilação nesta sessão ter revelado o
erro): a instância `[Nonempty (testScheme.basicOpen aSec)]` é exigida em
DOIS pontos sintáticos da cadeia, não em um só — ambos identificados por
`lake env lean` reportando `failed to synthesize instance` na primeira
tentativa (sem `haveI`), não apenas por inspeção prévia do código-fonte:

1. A assinatura de `Scheme.germToFunctionField`
   (`AlgebraicGeometry/FunctionField.lean:41-43`):
   ```
   noncomputable abbrev Scheme.germToFunctionField [IrreducibleSpace X] (U : X.Opens)
       [h : Nonempty U] : Γ(X, U) ⟶ X.functionField := ...
   ```
   — `[h : Nonempty U]` é argumento de instância. Usada aplicada a
   `basicOpen aSec` apenas no ENUNCIADO de `germToFunctionField_aRes`
   (nenhuma outra declaração do arquivo menciona `germToFunctionField`
   aplicado a `basicOpen aSec` em seu tipo).
2. A assinatura de `Scheme.ord_of_isUnit`
   (`AlgebraicGeometry/OrderOfVanishing.lean:88`):
   ```
   lemma ord_of_isUnit {U : X.Opens} [Nonempty U] {f : Γ(X, U)} (hf : IsUnit f) {x : X}
       (hx' : x ∈ U) : ord (X.germToFunctionField U f) x = 0 := ...
   ```
   — também `[Nonempty U]` de instância. Usada, aplicada a `basicOpen aSec`,
   dentro da PROVA (não do tipo) de `ord_genf_eq_zero_of_mem_basicOpen`.

Cada ponto precisa da sua própria correção, de naturezas ligeiramente
diferentes por estarem em posições sintáticas diferentes (tipo vs. prova):

**Ponto 1 (`germToFunctionField_aRes`, instância exigida no TIPO do lema).**
Em vez de uma `instance` de seção (que precisaria sintetizar `a0 ≠ 0`
automaticamente — o impasse documentado em HG-1b), o enunciado é escrito com
um `haveI` INLINE no próprio TIPO do lema — não apenas na prova:

```
lemma germToFunctionField_aRes :
    haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
    testScheme.germToFunctionField (testScheme.basicOpen (aSec a0)) (aRes a0) = genf a0 := by
  haveI : Nonempty (testScheme.basicOpen (aSec a0)) := nonempty_basicOpen a0 ha0
  ...
```

Este padrão — `haveI` como parte do próprio TIPO de uma declaração, não
apenas da prova, para fornecer a uma parte POSTERIOR do enunciado (aqui, o
lado esquerdo da igualdade) uma instância local sem precisar declará-la como
`instance` de seção — não foi inventado nesta sessão: é um idioma já usado em
Mathlib (confirmado por grep nesta sessão), e.g.
`Mathlib/NumberTheory/NumberField/Cyclotomic/Basic.lean:556`:

```
(hp : haveI : NeZero n := NeZero.of_gt hn; (p : ℤ) ∣ norm ℤ (hζ.toInteger - 1)) :
```

— `haveI` dentro do tipo de um argumento de hipótese, exatamente a mesma
técnica aplicada aqui ao tipo de retorno de um lema. Termos-`have`/`haveI`
elaboram como aplicação de uma função (`(fun h => corpo) valor`), então a
instância `h` fica disponível para busca de instância durante a elaboração
do `corpo` que a segue — sem exigir que `h` seja um argumento de instância
do lema inteiro (o que forçaria a mesma síntese automática que falha em
nível `variable`). A prova (`by` bloco) repete o `haveI` como primeiro passo
tático: isto é redundante em relação ao `haveI` do tipo (o objetivo tático já
chega com a instância disponível, herdada da aplicação da função no tipo),
mas foi mantido por clareza/robustez e não afeta o resultado — confirmado
que o arquivo compila igualmente com ou sem essa repetição.

**Ponto 2 (`ord_genf_eq_zero_of_mem_basicOpen`, instância exigida só na
PROVA).** Aqui o enunciado do lema (`testScheme.ord (genf a0) x = 0`) NÃO
menciona `germToFunctionField`/`basicOpen aSec`, então não precisa do truque
`haveI`-no-tipo — um `haveI := nonempty_basicOpen a0 ha0` comum, como
primeiro passo tático dentro do `by`, já disponibiliza a instância para a
chamada subsequente a `Scheme.ord_of_isUnit` dentro da prova. Esta é
exatamente a forma "canônica" de `haveI` local por lema mencionada na
proposta do teste; o Ponto 1 precisou da variante mais forte (`haveI`
também no tipo) só porque, nesse caso específico, o próprio ENUNCIADO
menciona o termo que carrega a exigência de instância.

Todas as outras 15 declarações do argumento de HG-1/HG-1b (`aSec`,
`aSec_ne_zero`, `genf`, `algebraMap_eq_genf`, `genf_ne_zero`,
`genericPoint_mem_basicOpen`, `nonempty_basicOpen`, `aRes`, `isUnit_aRes`,
`basicOpen_aSec_eq`, `mem_basicOpen_iff`, `mem_asIdeal_of_notMem_basicOpen`,
`isMinimalPrime_of_mem_asIdeal`, `asIdeal_injective`,
`finite_support_ord_genf`, `finite_support_ord_algebraMap`) recebem
`(a0 : ℤ)`, e as que precisam, também `(ha0 : a0 ≠ 0)`, como argumentos
EXPLÍCITOS comuns (não `variable` de seção nem `instance`) — sem precisar de
nenhum `haveI`, porque nenhum outro enunciado ou prova do arquivo, além dos
Pontos 1 e 2 acima, aplica `germToFunctionField`/`ord_of_isUnit` a um aberto
que dependa de `a0`. (Nota: uma tentativa inicial usou `variable (a0)(ha0)`
de seção; falhou com "unknown identifier `ha0`" em toda declaração cujo
ENUNCIADO não menciona `ha0` — o auto-bound de `variable` do Lean4 só inclui
uma variável numa declaração se ela aparecer livre no TIPO declarado, não
basta aparecer na prova. A correção — `include ha0` — foi descartada em
favor de argumentos explícitos porque `include` é "pegajoso" para o resto da
seção e forçaria `ha0` também em `aSec`/`genf`/`aRes`, que não precisam
dele, mudando sua aridade. Argumentos explícitos por declaração evitam essa
armadilha.) A duplicação `Num`/`Den` de HG-1b é assim eliminada: existe
agora uma única cópia parametrizada de todo o argumento, instanciável em
qualquer `a0 : ℤ` não-nulo (em particular em `a0 = 3` e `a0 = 2`,
reproduzindo exatamente as duas instâncias concretas de HG-1b — ver a seção
`Instantiation` ao final deste arquivo).

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados abaixo já foram verificados por leitura direta de
código-fonte em HG-1 (`principal_divisor_algebraic_cycle_bridge.lean`) e/ou
HG-1b (`AlgebraMapGermToFunctionFieldOrdMulProbe.lean`, mesmo diretório —
ver os preâmbulos desses dois arquivos para a lista completa e as
referências de arquivo/linha). Os nomes adicionais verificados nesta sessão,
especificamente para a técnica `haveI`-local (nos dois pontos acima):
  - `Scheme.germToFunctionField` (`AlgebraicGeometry/FunctionField.lean:41-43`
    — assinatura relida nesta sessão para confirmar que `[Nonempty U]` é
    argumento de instância).
  - `Scheme.ord_of_isUnit` (`AlgebraicGeometry/OrderOfVanishing.lean:88` —
    assinatura relida nesta sessão, mesmo motivo; este segundo ponto NÃO
    havia sido antecipado antes da primeira tentativa de compilação, que
    falhou com `failed to synthesize instance` exatamente nesta chamada —
    ver "O que realmente fechou o teste" acima).
  - Padrão `haveI : T := v; corpo` como TIPO de uma declaração (não apenas
    de uma prova), confirmado como idioma já usado em Mathlib por grep
    nesta sessão, e.g. `NumberTheory/NumberField/Cyclotomic/Basic.lean:556`.
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de
saída `0`, após a correção do Ponto 2 acima) e por busca textual (zero
ocorrências dos marcadores proibidos pela governança do laboratório).
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

end Instantiation

end AlgebraicGeometry.HG1C
