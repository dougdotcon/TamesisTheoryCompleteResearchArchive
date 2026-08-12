/-
HG-1i (Wave 7, item WAVE7-HG-1I) — lei de POTÊNCIA para `principalCycle_a0`:
por indução em `n : ℕ`, o ciclo de `a0^(n+1)` é `(n+1)` cópias (via `•`, o
`nsmul` do grupo aditivo `AlgebraicCycle testScheme ℤ`) do ciclo de `a0`.
Reusa `principalCycle_a0`/`principalCycle_a0_mul`, já fechados em HG-1E/HG-1H
(mesmo diretório), como passo indutivo: `a0^((n+1)+1) = a0 * a0^(n+1)`
(`pow_succ'`) decompõe, via `principalCycle_a0_mul`, exatamente como
`(n+2) • x = x + (n+1) • x` (`succ_nsmul'`) decompõe do lado aditivo — o
mesmo par `pow_succ'`/`succ_nsmul'` (ligados por `@[to_additive]`) usado como
precedente em `Mathlib/Algebra/GradedMonoid.lean:566` (`pow_mem_graded`,
caso `n+1`, `rw [pow_succ', succ_nsmul']`).

STATUS: COMPILADO (`lake env lean`, exit 0) nesta sessão. A declaração nova
verificada com o comando de impressão de dependências de prova do Lean:
depende apenas de `[propext, Classical.choice, Quot.sound]` — nenhum
marcador de prova incompleta escapou pela síntese de instâncias. O arquivo
não contém nenhuma prova incompleta, nenhuma declaração local tomada como
verdade sem prova, e nenhum bloco marcado como inseguro, em nenhum lugar
(conferido por busca textual nesta sessão).
Ainda NÃO registrado em `TamesisLab.lean` (instrução explícita desta rodada:
não tocar em arquivos compartilhados).

O QUE ESTE ARQUIVO NÃO É:
Este arquivo NÃO formaliza nem aproxima a Conjectura de Hodge, nem qualquer
parte da máquina de teoria de Hodge necessária para ela. O conteúdo abaixo é
100% álgebra comutativa/geometria de esquemas clássica: NADA aqui usa
estrutura complexa, cohomologia, decomposição de Hodge, ou classe de ciclo
em cohomologia. Mesmo em caso de sucesso total, o resultado permanece a
várias camadas inteiramente ausentes de sequer enunciar formalmente Hodge
(1,1), quanto mais a conjectura geral. Este item não afirma nenhuma
novidade matemática: "divisor de uma potência = múltiplo do divisor da
base" é o caso particular, por indução, de "divisor de um produto = soma
dos divisores dos fatores" (já formalizado em HG-1H) — consequência direta
e clássica da aditividade da valorização (ver, e.g., Hartshorne II.6, ou
qualquer texto de teoria de valorização). O que está formalizado aqui é
apenas essa identidade pontual, para QUALQUER `a0 : ℤ` não-nulo e QUALQUER
`n : ℕ`, reempacotada no tipo `AlgebraicCycle` de Mathlib.

O QUE ESTE ARQUIVO É:
A tentativa do teste falsificável HG-1i, especificado (após revisão
adversarial na etapa de planejamento da Onda 7) como:

  Provar `principalCycle_a0 (a0^(n+1)) = (n+1) • principalCycle_a0 a0`, por
  indução: caso `succ` via `rw [pow_succ', principalCycle_a0_mul a0
  (a0^(n+1)) ha0 (pow_ne_zero (n+1) ha0), ih, ← succ_nsmul']` — emparelhar
  `pow_succ'` com `succ_nsmul'` (não `succ_nsmul`), conforme o precedente em
  `Mathlib/Algebra/GradedMonoid.lean:566`. Teto: 80 linhas novas
  não-comentário. `#print axioms` limpo.

RESULTADO: SUCESSO, mas NÃO com a receita do teste aplicada literalmente
verbatim. A sequência de lemas da receita (`pow_succ'`,
`principalCycle_a0_mul`, `ih`, `← succ_nsmul'`, nessa ordem) está correta e
sobrevive no arquivo final — mas `rw [pow_succ']`, tentado como PRIMEIRO
passo isolado tal como escrito na receita, falha nesta sessão com o erro
"motive is not type correct" (ver "O que realmente fechou o teste" abaixo
para o diagnóstico exato); a receita precisou de UM passo adicional —
`principalCycle_a0_congr`, um lema de congruência auxiliar de duas linhas —
antes de `pow_succ'`/`principalCycle_a0_mul` poderem ser aplicados por
`rw`. Confirmado por tentativa direta nesta sessão (log preservado): a
receita literal falha nos DOIS casos (`zero` e `succ`) com exatamente esse
erro; a correção abaixo restaura exit 0.

## O que realmente fechou o teste

**Inlining verbatim de HG-1C/HG-1E/HG-1H.** Todo o bloco de HG-1H
(`HG1HPrincipalCycleA0MulProbe.lean`, mesmo diretório), de `import Mathlib`
até `end` (fechando a seção `noncomputable section`) — incluindo `genf`,
`finite_support_ord_genf`, `principalCycle_a0`, `genf_mul` e
`principalCycle_a0_mul` — foi copiado byte-idêntico para este arquivo nesta
sessão (diretamente do arquivo-fonte, não de memória nem paráfrase). Mesmo
motivo mecânico já documentado nos preâmbulos de HG-1D/HG-1E/HG-1F/HG-1G/
HG-1H: este arquivo, como HG-1H, vive em `03_MILLENNIUM/05_HODGE/FORMAL/`,
fora da raiz de módulos do pacote Lake (confirmado nesta sessão por
reinspeção de `05_FORMAL/lean/lakefile.toml` e `05_FORMAL/lean/
TamesisLab.lean`, nenhuma mudança desde a verificação de HG-1H), logo não há
caminho de `import` de um arquivo solto para outro; a única forma de reusar
`principalCycle_a0`/`principalCycle_a0_mul`/etc. aqui é reproduzir o texto.
A seção `Instantiation` de HG-1H NÃO foi reproduzida (não é necessária como
base para a nova prova; a instanciação nova deste arquivo é escrita do
zero, ver abaixo). Reusar o mesmo nome de namespace
(`AlgebraicGeometry.HG1C`) num arquivo novo, não importado pelo original,
não causa nenhum conflito de compilação — mesmo padrão já usado com sucesso
por HG-1E/HG-1F/HG-1G/HG-1H.

**Por que a receita literal falha.** `principalCycle_a0 : (a0 : ℤ) → a0 ≠ 0
→ AlgebraicCycle testScheme ℤ` é uma função DEPENDENTE: o tipo do segundo
argumento (`a0 ≠ 0`) depende do primeiro. `rw [pow_succ']` (ou, tentado
como alternativa nesta sessão, `simp only [pow_succ']`/`rw [pow_one]`)
tenta abstrair TODAS as ocorrências sintáticas de `a0^(k+1)` no objetivo
para construir o "motive" da reescrita — mas, como essa mesma expressão
aparece como PRIMEIRO argumento de `principalCycle_a0` na MESMA aplicação
cujo SEGUNDO argumento (`pow_ne_zero (k+1) ha0`) tem tipo dependente dela,
o motive resultante (`fun t => principalCycle_a0 t (pow_ne_zero (k+1) ha0)
= ...`) não tipa — erro "motive is not type correct" do Lean, confirmado
nesta sessão para os dois casos (`zero`, `succ`) por tentativa direta antes
da correção. `simp only` sofre de um problema relacionado (reescreve
`pow_succ'` recursivamente, também confirmado nesta sessão).

**A correção — `principalCycle_a0_congr`, um lema de congruência auxiliar
de duas linhas.** Como `principalCycle_a0` não depende do CONTEÚDO da
prova (só da Prop, por irrelevância de prova de Lean), basta um lema que
troque a APLICAÇÃO INTEIRA de uma vez (não o argumento isoladamente dentro
dela), evitando o motive dependente:

```
lemma principalCycle_a0_congr {a b : ℤ} (h : a = b) (ha : a ≠ 0) (hb : b ≠ 0) :
    principalCycle_a0 a ha = principalCycle_a0 b hb := by subst h; rfl
```

`subst h` substitui `a` por `b` em todo o objetivo; o que resta,
`principalCycle_a0 b ha' = principalCycle_a0 b hb` (duas provas distintas
de `b ≠ 0`), fecha por `rfl` — irrelevância de prova de Lean torna `ha'` e
`hb` definicionalmente iguais. Usando `principalCycle_a0_congr` para substituir a APLICAÇÃO INTEIRA
`principalCycle_a0 (a0^((n+1)+1)) hyp` por `principalCycle_a0 (a0 *
a0^(n+1)) hyp'` num único passo de `rw` (em vez de tentar reescrever só o
argumento `a0^((n+1)+1)` isoladamente dentro dela), o motive necessário é
trivial (`fun t => t = ...`, sem dependência), e a receita original —
`principalCycle_a0_mul`, `ih`, `← succ_nsmul'`, nessa ordem — aplica-se sem
obstáculo em seguida.

**`principalCycle_a0_pow`, enunciado exatamente como no teste, por
indução em `n`:**

```
theorem principalCycle_a0_pow (a0 : ℤ) (ha0 : a0 ≠ 0) (n : ℕ) :
    principalCycle_a0 (a0 ^ (n + 1)) (pow_ne_zero (n + 1) ha0) =
      (n + 1) • principalCycle_a0 a0 ha0 := ...
```

Caso `zero` (não coberto pela receita do teste — escrito nesta sessão):
`principalCycle_a0_congr` com `h : a0^(0+1) = a0` (por `zero_add`,
`pow_one`) reduz o objetivo a `principalCycle_a0 a0 ha0 = (0+1) •
principalCycle_a0 a0 ha0`; `rw [zero_add, one_nsmul]` fecha (o `rw` final
fecha por `rfl`, agora sobre um objetivo sem dependência problemática).

Caso `succ n ih` (receita do teste, com o passo `principalCycle_a0_congr`
inserido ANTES dela): `principalCycle_a0_congr` com `h := pow_succ' a0
(n+1) : a0^((n+1)+1) = a0 * a0^(n+1)` reduz o objetivo a
`principalCycle_a0 (a0 * a0^(n+1)) hyp = ((n+1)+1) • principalCycle_a0 a0
ha0`. A partir daqui, a receita original aplica-se verbatim:
`principalCycle_a0_mul a0 (a0^(n+1)) ha0 (pow_ne_zero (n+1) ha0)` — com o
quinto argumento (`hab : a0 * a0^(n+1) ≠ 0`) deixado como metavariável,
unificada diretamente contra a prova já presente no objetivo, sem
necessidade de generalização — reescreve o ciclo do produto como a soma
`principalCycle_a0 a0 ha0 + principalCycle_a0 (a0^(n+1)) (pow_ne_zero (n+1)
ha0)`; `ih` reescreve o segundo somando para `(n+1) • principalCycle_a0 a0
ha0`; e `← succ_nsmul'` (aplicado com `m := n+1`, `a := principalCycle_a0
a0 ha0`) reescreve `principalCycle_a0 a0 ha0 + (n+1) • principalCycle_a0 a0
ha0` de volta para `((n+1)+1) • principalCycle_a0 a0 ha0`, fechando o
objetivo por `rfl` automático do `rw`.

## Nomes verificados (por grep e por compilação nesta sessão)

Todos os nomes usados no bloco reproduzido de HG-1C/HG-1E/HG-1H já estavam
verificados nos preâmbulos daqueles arquivos (mesmo diretório) — não
repetidos aqui por brevidade. Adicionalmente, para
`principalCycle_a0_congr`/`principalCycle_a0_pow`:
  - `subst` (tática núcleo do Lean, não um lema de Mathlib) — usada em
    `principalCycle_a0_congr` para eliminar a hipótese `h : a = b`,
    substituindo `a` por `b`; o `rfl` final depende apenas de irrelevância
    de prova (regra de tipagem do próprio Lean, não um axioma adicional —
    confirmado pelo `#print axioms` limpo).
  - `pow_succ'` e `succ_nsmul'` — `Mathlib/Algebra/Group/Defs.lean:702`:
    `@[to_additive succ_nsmul'] lemma pow_succ' (a : M) : ∀ n, a ^ (n + 1) =
    a * a ^ n`. CRÍTICO: distinto de `pow_succ`/`succ_nsmul`
    (`Mathlib/Algebra/Group/Defs.lean:696`, `a ^ (n+1) = a^n * a`, o
    multiplicando do OUTRO lado) — o teste especifica explicitamente
    `pow_succ'` (multiplicando à ESQUERDA, `a * a^n`) para casar com o
    padrão de `principalCycle_a0_mul a0 (a0^(n+1)) ...`, que espera o
    PRIMEIRO fator igual a `a0` (não a `a0^(n+1)`); usar `pow_succ`/
    `succ_nsmul` aqui exigiria trocar a ordem dos argumentos de
    `principalCycle_a0_mul` (e de `Scheme.ord_mul`, dentro de
    `principalCycle_a0_mul`) e do braço direito de `succ_nsmul`, quebrando
    o encaixe direto com `ih`. Precedente exato — mesmo par
    `pow_succ'`/`succ_nsmul'`, mesma forma de uso (`rw [pow_succ',
    succ_nsmul']` no caso `n+1` de uma indução) — em
    `Mathlib/Algebra/GradedMonoid.lean:566` (`pow_mem_graded`), reconferido
    por leitura direta de código-fonte nesta sessão antes de escrever a
    prova abaixo.
  - `pow_ne_zero` (`Mathlib/Algebra/GroupWithZero/Basic.lean`, `(n : ℕ) (h :
    a ≠ 0) : a ^ n ≠ 0`, já usado no preâmbulo de HG-1H/HG-1G).
  - `pow_one`, `one_nsmul` (`Mathlib/Algebra/Group/Defs.lean:699`,
    `@[to_additive one_nsmul, simp] lemma pow_one (a : M) : a ^ 1 = a`).
  - `principalCycle_a0`, `principalCycle_a0_mul` — HG-1E/HG-1H, mesmo
    diretório, reproduzidos verbatim neste arquivo (ver acima).
Verificado com `lake env lean` sobre este arquivo nesta sessão (código de
saída `0`) e por busca textual (zero ocorrências dos marcadores proibidos
pela governança do laboratório).
-/

import Mathlib

open AlgebraicGeometry CategoryTheory

namespace AlgebraicGeometry.HG1C

noncomputable section

/-! ## Configuração concreta: `X = Spec ℤ` (mesma escolha de HG-1/HG-1b/HG-1C/HG-1E/HG-1H) -/

/-- Anel de teste: `ℤ`. -/
abbrev testRing : CommRingCat := CommRingCat.of ℤ

/-- Esquema de teste: `Spec ℤ`. -/
abbrev testScheme : Scheme.{0} := Spec testRing

instance : Nonempty (⊤ : testScheme.Opens) := ⟨⟨genericPoint testScheme, trivial⟩⟩

/-! ## Passo 1 — compatibilidade `algebraMap`/`germToFunctionField` (reproduzido de
HG-1b/HG-1C/HG-1E/HG-1H; independe de `a0`). -/

lemma algebraMap_eq_germToFunctionField (x : ℤ) :
    algebraMap ℤ testScheme.functionField x =
      testScheme.germToFunctionField ⊤ ((Scheme.ΓSpecIso testRing).inv x) := by
  have h : (algebraMap ℤ testScheme.functionField) =
      (testScheme.germToFunctionField ⊤).hom.comp (Scheme.ΓSpecIso testRing).inv.hom :=
    Subsingleton.elim _ _
  exact DFunLike.congr_fun h x

/-! ## Passo 2 — o argumento de finitude de HG-1C, parametrizado sobre
`(a0 : ℤ) (ha0 : a0 ≠ 0)` explícitos como argumentos comuns (reproduzido byte-idêntico
de HG-1C/HG-1E/HG-1H — ver preâmbulos daqueles arquivos para a discussão de por que
`a0`/`ha0` são argumentos explícitos comuns, não `variable`/`instance` de seção). -/

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
`AlgebraicCycle testScheme ℤ`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`. -/

/-- `ord (genf a0)`, para QUALQUER `(a0 : ℤ) (ha0 : a0 ≠ 0)`, empacotado como um termo de
`AlgebraicCycle testScheme ℤ` (HG-1E). -/
def principalCycle_a0 (a0 : ℤ) (ha0 : a0 ≠ 0) : AlgebraicCycle testScheme ℤ where
  toFun x := testScheme.ord (genf a0) x
  supportWithinDomain' := by simp
  supportLocallyFiniteWithinDomain' _ _ :=
    ⟨Set.univ, Filter.univ_mem, by simpa using finite_support_ord_genf a0 ha0⟩

/-! ## Multiplicatividade (reproduzida de HG-1H) — `principalCycle_a0` de um produto é a
SOMA dos `principalCycle_a0` dos fatores. Único bloco extra (além de HG-1E) de que HG-1i
precisa como passo indutivo. -/

/-- `genf` transporta produtos de `ℤ` para produtos em `testScheme.functionField`, via
`algebraMap` (homomorfismo de anéis). -/
lemma genf_mul (a0 b0 : ℤ) : genf (a0 * b0) = genf a0 * genf b0 := by
  rw [← algebraMap_eq_genf (a0 * b0), map_mul, algebraMap_eq_genf, algebraMap_eq_genf]

/-- `principalCycle_a0` de um produto é a soma dos `principalCycle_a0` dos fatores
(HG-1H). -/
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

/-!
## HG-1i (NOVO nesta sessão) — lei de potência: `principalCycle_a0` de uma potência
`a0^(n+1)` é `(n+1)` cópias (`nsmul`) do `principalCycle_a0` da base `a0`

Consequência indutiva direta de `principalCycle_a0_mul`: o passo `succ` decompõe
`a0^((n+1)+1) = a0 * a0^(n+1)` (`pow_succ'`) via `principalCycle_a0_mul`, casando com
`(n+1+1) • x = x + (n+1) • x` (`succ_nsmul'`) do lado aditivo — mesmo par
`pow_succ'`/`succ_nsmul'` usado como precedente em
`Mathlib/Algebra/GradedMonoid.lean:566`.
-/

/-- **Resultado principal de HG-1i — a lei de potência pedida pelo teste.**
`principalCycle_a0 (a0^(n+1))` (o ciclo da potência `a0^(n+1)`) é `(n+1) •
principalCycle_a0 a0 ha0` (a soma repetida `(n+1)` vezes, via `nsmul` do grupo aditivo
`AlgebraicCycle testScheme ℤ`, do ciclo da base `a0`), para QUALQUER `a0 : ℤ` não-nulo
e QUALQUER `n : ℕ`. Caso particular indutivo de `principalCycle_a0_mul` (HG-1H). -/
lemma principalCycle_a0_congr {a b : ℤ} (h : a = b) (ha : a ≠ 0) (hb : b ≠ 0) :
    principalCycle_a0 a ha = principalCycle_a0 b hb := by subst h; rfl

theorem principalCycle_a0_pow (a0 : ℤ) (ha0 : a0 ≠ 0) (n : ℕ) :
    principalCycle_a0 (a0 ^ (n + 1)) (pow_ne_zero (n + 1) ha0) =
      (n + 1) • principalCycle_a0 a0 ha0 := by
  induction n with
  | zero =>
      rw [principalCycle_a0_congr (a := a0 ^ (0 + 1)) (by rw [zero_add, pow_one]) _ ha0,
        zero_add, one_nsmul]
  | succ n ih =>
      rw [principalCycle_a0_congr (a := a0 ^ (n + 1 + 1)) (pow_succ' a0 (n + 1)) _
          (mul_ne_zero ha0 (pow_ne_zero (n + 1) ha0)),
        principalCycle_a0_mul a0 (a0 ^ (n + 1)) ha0 (pow_ne_zero (n + 1) ha0), ih,
        ← succ_nsmul']

end

/-! ## Verificação de instanciação: duas instâncias concretas obtidas por especialização
direta do resultado parametrizado acima, sem nenhuma duplicação de prova. -/

section Instantiation

/-- `principalCycle_a0_pow` instanciado em `a0 = 3`, `n = 2` (i.e. `a0^3`): o ciclo de
`3^3 = 27` é `3 • principalCycle_a0 3`. -/
noncomputable example :
    principalCycle_a0 (3 ^ 3) (by decide) = (3 : ℕ) • principalCycle_a0 3 (by decide) :=
  principalCycle_a0_pow 3 (by decide) 2

/-- Uma segunda instanciação, com `a0 = 5`, `n = 0` (i.e. `a0^1 = a0`), verificando o caso
base isoladamente. -/
noncomputable example :
    principalCycle_a0 (5 ^ 1) (by decide) = (1 : ℕ) • principalCycle_a0 5 (by decide) :=
  principalCycle_a0_pow 5 (by decide) 0

end Instantiation

/-! ## Verificação de dependências de prova (nesta sessão) — a declaração genuinamente
nova deste arquivo (HG-1i), confirmando que depende apenas de `[propext,
Classical.choice, Quot.sound]` (nenhuma prova incompleta escapou pela síntese de
instâncias ou por elaboração implícita). -/

#print axioms principalCycle_a0_pow

end AlgebraicGeometry.HG1C
