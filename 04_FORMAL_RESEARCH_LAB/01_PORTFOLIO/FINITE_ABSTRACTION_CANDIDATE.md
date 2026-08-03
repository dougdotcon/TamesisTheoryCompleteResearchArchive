---
document_id: PR-FINITE-ABSTRACTION-CANDIDATE
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
previous_candidate_id: FOUND-FINITE-ABSTRACTION-001
status: READY
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SEMANTIC_FOUNDATION
---

# Candidato selecionado — abstração finita certificada

## Objetivo preliminar

```text
Relacionar um sistema concreto C com um sistema abstrato finito A por
uma funcao de abstracao que comuta com as transicoes.

Provar o que pode ser transportado do abstrato para o concreto, e
identificar condicoes suficientes para refletir uma repeticao abstrata
como repeticao concreta.
```

## Escopo congelado como proposta

```text
tipo concreto C;
tipo abstrato A;
tamanho n;
stepC : C → C;
stepA : A → A;
abstract : C → A;
semiconjugacao;
CertifiedFiniteEncoding A n;
analise do sistema abstrato;
recorrencia observacional no sistema concreto;
condicao de separacao na orbita;
reflexao da recorrencia sob essa condicao;
contraexemplo sem a condicao.
```

## O que NÃO está decidido

```text
estrutura Lean final;
nomes definitivos;
uso de Set.InjOn como formulacao primaria;
relacao de simulacao geral;
bissimulacao;
concretizacao γ : A → C;
quocientes;
extracao;
CLI;
integracao externa.
```

Pertencem ao gate de especificação.

## As três peças, já compiladas em probe

### 1. Correspondência de iteradas

```lean
theorem abstract_iterate (abstract : C → A) (stepC : C → C) (stepA : A → A)
    (h : Function.Semiconj abstract stepC stepA) (k : Nat) (start : C) :
    abstract (stepC^[k] start) = stepA^[k] (abstract start) :=
  h.iterate_right k start
```

Um termo. Axiomas `[propext]`. É o mesmo `Function.Semiconj.iterate_right`
que a codificação certificada já usa — a terceira frente seguida a
consumi-lo.

### 2. Soundness **observacional**

```lean
theorem analyzeAbstract_observational_sound
    (hsemi : Function.Semiconj abstract stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C) {w : CycleWitness}
    (h : analyzeEncodedSystem encoding stepA (abstract start) = .ok w) :
    abstract (stepC^[w.baseIndex + w.period] start)
      = abstract (stepC^[w.baseIndex] start)
```

Três linhas de prova. A conclusão é uma igualdade **entre abstrações** de
dois estados concretos. Ela é verdadeira com **apenas** a semiconjugação,
e é tudo o que se pode afirmar sem hipótese adicional.

### 3. O contraexemplo, como teorema

```lean
theorem naive_cycle_reflection_is_false :
    ¬ (∀ (C A : Type) (stepC : C → C) (stepA : A → A) (abstract : C → A),
        Function.Semiconj abstract stepC stepA →
        ∀ start : C,
          abstract (stepC start) = abstract start → stepC start = start)
```

**Compilado, e sem depender de axioma nenhum.**

```text
C = Bool          stepC = not
A = Unit          stepA = id
abstract          constante
```

```text
Semiconj vale                          rfl
abstract (stepC false) = abstract false  rfl, periodo abstrato 1
stepC false ≠ false                      decide
```

Registrado:

```yaml
naive_cycle_reflection:
  status: FALSE
  counterexample: BOOL_TO_UNIT
```

O contraexemplo **não** denuncia defeito da abstração. Ele exibe
exatamente a perda de informação que uma abstração existe para produzir.

## A condição de reflexão

```lean
def OrbitSeparating (abstract : C → A) (stepC : C → C) (start : C) : Prop :=
  ∀ i j : Nat,
    abstract (stepC^[i] start) = abstract (stepC^[j] start) →
      stepC^[i] start = stepC^[j] start
```

```lean
theorem concrete_cycle_of_orbit_separating
    (hsemi : Function.Semiconj abstract stepC stepA)
    (encoding : CertifiedFiniteEncoding A n) (start : C)
    (hsep : OrbitSeparating abstract stepC start) {w : CycleWitness}
    (h : analyzeEncodedSystem encoding stepA (abstract start) = .ok w) :
    stepC^[w.baseIndex + w.period] start = stepC^[w.baseIndex] start :=
  hsep (w.baseIndex + w.period) w.baseIndex
    (observational_sound abstract stepC stepA hsemi encoding start h)
```

Um termo, sobre o resultado observacional.

### Classificação, verificada

```yaml
reflection_condition:
  non_tautological: true
  consumer_checkable: true
  reusable: true
  requires_global_injectivity: false
  requires_only_orbit_injectivity: true
```

- **Não tautológica**: `boolToUnit_not_orbitSeparating` prova que a
  condição **falha** exatamente no contraexemplo. Compilado, sem axiomas.
  Se ela fosse consequência da semiconjugação, valeria ali.
- **Não assume a conclusão**: a hipótese quantifica sobre **todos** os
  pares `i, j` da órbita; a conclusão compara **um** par específico,
  `b + p` e `b`. A implicação é estrita.
- **Satisfazível**: `orbitSeparating_of_injective` mostra que toda
  abstração injetiva a satisfaz — e a cadeia completa foi instanciada com
  a identidade sobre `Fin 4`.
- **Local**: exige injetividade só **sobre a órbita alcançada**, não
  globalmente.

## `OrbitSeparating` contra `Set.InjOn`

```lean
theorem orbitSeparating_iff_injOn (abstract) (stepC) (start) :
    OrbitSeparating abstract stepC start
      ↔ Set.InjOn abstract (Set.range fun k : Nat => stepC^[k] start)
```

**Compilado, sem axiomas.** As duas formulações são equivalentes.

| Critério | `OrbitSeparating` | `Set.InjOn` sobre `Set.range` |
|---|---|---|
| prova de reflexão | aplicação direta: `hsep (b+p) b h` | precisa de `Set.mem_range_self` duas vezes |
| verificação pelo consumidor | quantificador sobre `Nat`, imediato | exige raciocinar sobre pertinência a `Set.range` |
| reutilização Mathlib | nenhuma API herdada | herda o ferramental de `Set.InjOn` |
| dependência | nenhuma além de `Nat.iterate` | `Set`, `Set.range`, `Set.InjOn` |

Recomendação **preliminar**: `OrbitSeparating` como formulação primária,
por ser mais direta na prova e na verificação; `Set.InjOn` exposto como
**vista equivalente**, exatamente como `Equiv` foi tratado na frente
anterior. O nome definitivo **não** está congelado.

## APIs auditadas

Todas encontradas, em probe descartável já removido:

```text
Function.Semiconj                : (α → β) → (α → α) → (β → β) → Prop
Function.Semiconj.iterate_right  : Semiconj f ga gb → ∀ n, Semiconj f ga^[n] gb^[n]
Function.Injective
Set.InjOn                        : (α → β) → Set α → Prop
Set.range                        : (ι → α) → Set α
Set.mem_range_self               : ∀ (i), f i ∈ Set.range f
Set.Pairwise
Nat.iterate                      notacao f^[n]
Function.iterate_succ_apply
Option.some.inj
```

### Pegada axiomática medida

```text
abstract_iterate                     [propext]
OrbitSeparating                      NENHUM
orbitSeparating_iff_injOn            NENHUM
boolToUnit_not_orbitSeparating       NENHUM
orbitSeparating_of_injective         NENHUM
naive_cycle_reflection_is_false      NENHUM
observational_sound                  [propext, Classical.choice, Quot.sound]
concrete_cycle_of_orbit_separating   [propext, Classical.choice, Quot.sound]
```

A camada nova é quase toda **livre de axiomas**. Os três aparecem apenas
onde a cadeia anterior entra, por `analyzeEncodedSystem`.

## O que a frente **não** exigirá

```text
C finito             NAO   — C : Type*, sem Fintype
DecidableEq C        NAO   — nenhuma instancia
Nonempty C           NAO
concretizacao γ      NAO
bissimulacao         NAO
integracao externa   NAO
```

Verificado por compilação: os probes usam `C : Type*` sem qualquer
typeclass.

## PoC de trinta dias

```text
1 definicao;
cerca de 8 teoremas;
1 contraexemplo;
0 fontes primarias;
0 dependencias externas;
reutilizacao integral de analyzeEncodedSystem_sound.
```

`thirty_day_poc: YES`. Todas as peças centrais já compilaram.

## Duplicata

```text
15 itens na fila; nenhum contem ABSTRACTION.
```

## Resultados candidatos

```text
ABS-CORE-001 — abstracao deterministica certificada
ABS-CORE-002 — correspondencia de iteradas por semiconjugacao
ABS-CORE-003 — analyzeAbstractSystem
ABS-CORE-004 — soundness observacional
ABS-CORE-005 — condicao OrbitSeparating
ABS-CORE-006 — reflexao sob OrbitSeparating
ABS-CORE-007 — completeness da analise abstrata
ABS-CORE-008 — contraexemplo a reflexao ingenua
```

Nem todos serão necessariamente públicos. Nenhuma claim é promovida.

## Gaps iniciais — vinte, nenhum fechado

```text
ABS-GAP-001  representacao da abstracao
ABS-GAP-002  orientacao da semiconjugacao
ABS-GAP-003  correspondencia de iteradas
ABS-GAP-004  integracao com CertifiedFiniteEncoding
ABS-GAP-005  analise do sistema abstrato
ABS-GAP-006  soundness observacional
ABS-GAP-007  formulacao de OrbitSeparating
ABS-GAP-008  relacao com Set.InjOn
ABS-GAP-009  reflexao da repeticao
ABS-GAP-010  contraexemplo BOOL_TO_UNIT
ABS-GAP-011  necessidade de DecidableEq C
ABS-GAP-012  necessidade de finitude de C
ABS-GAP-013  completude abstrata
ABS-GAP-014  ciclos espurios
ABS-GAP-015  bissimulacao
ABS-GAP-016  quocientes
ABS-GAP-017  integracao externa
ABS-GAP-018  extracao futura
ABS-GAP-019  bibliografia
ABS-GAP-020  complexidade
```

## Stop conditions — dezesseis

```text
STOP-ABS-001  ciclo abstrato tratado como concreto sem hipotese
STOP-ABS-002  contraexemplo BOOL_TO_UNIT nao formalizavel
STOP-ABS-003  semiconjugacao orientada incorretamente
STOP-ABS-004  soundness termina em igualdade concreta sem hipotese
STOP-ABS-005  OrbitSeparating assume diretamente a conclusao
STOP-ABS-006  abstracao exige C finito sem necessidade
STOP-ABS-007  DecidableEq C exigida sem necessidade
STOP-ABS-008  encoding anterior eh modificado
STOP-ABS-009  runtime adapter eh modificado
STOP-ABS-010  detector eh copiado
STOP-ABS-011  bissimulacao assumida sem dados
STOP-ABS-012  integracao externa declarada correta
STOP-ABS-013  parser ou CLI no nucleo
STOP-ABS-014  novidade inflada
STOP-ABS-015  frente duplica item existente
STOP-ABS-016  PoC nao cabe em 30 dias
```

`STOP-ABS-002` e `STOP-ABS-005` já foram testadas por antecipação neste
gate: o contraexemplo **é** formalizável, e a condição **não** assume a
conclusão.

## Fronteira epistemológica

```text
Uma semiconjugacao prova que a trajetoria concreta eh observada
corretamente no sistema abstrato.

Uma igualdade entre estados abstratos demonstra apenas que os estados
concretos possuem a mesma observacao.

Ela nao demonstra, por si so, que os estados concretos sao iguais.

A reflexao de uma repeticao abstrata exige uma hipotese adicional, como
injetividade da abstracao sobre a orbita alcancada.

Mesmo quando essa hipotese eh formalizada, continua sendo
responsabilidade do adaptador da aplicacao provar que a funcao de
abstracao representa corretamente o sistema externo real.
```

Proibido afirmar: todo ciclo abstrato é concreto; toda simulação é
bissimulação; abstrações finitas não produzem ciclos espúrios; qualquer
workflow externo foi modelado corretamente; correção universal de
sistemas; algoritmo novo; novidade matemática.
