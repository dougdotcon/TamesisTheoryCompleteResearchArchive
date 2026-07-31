---
document_id: GEOMETRIC-LEAN-SCOPE
lean_root: "05_FORMAL/lean/TamesisLab/RHNogo/Geometry/"
status: VERIFIED
---

# Escopo do núcleo Lean geométrico

## Decisão sobre criar ou não o wrapper

O gate autorizava não criar o wrapper caso fosse mera duplicação da API
Mathlib. A decisão foi **criar**, por três razões concretas, e **não**
criar mais do que isso.

1. `measure_pos_of_isOpen_subset` **não** existe em Mathlib nessa forma.
   Mathlib tem `IsOpen.measure_pos` (aberto ⟹ medida positiva) e
   `measure_mono` separadamente. A composição *"o conjunto **contém** um
   aberto não vazio"* é exatamente o formato do passo 5 de `GWB-008A`, onde
   `B_x` não é dado como aberto por hipótese, mas como superconjunto de uma
   vizinhança da origem. O wrapper economiza a composição no ponto de uso e
   documenta a obrigação.
2. `PositiveWeylCoefficient` é interface, não matemática. Ela nomeia o
   único dado que `PowerCountingLaw.constant_pos` consome e torna
   verificável que nada mais é consumido.
3. `dimension_div_order_pos` justifica a nova hipótese `d ≥ 1` (B4) num
   objeto compilado em vez de num parágrafo.

`integral_pos_of_nonneg_of_support_measure_pos` **é** essencialmente
reexportação de `integral_pos_iff_support_of_nonneg`; foi mantida apenas
porque fixa a direção usada (`mpr`) e o nome da obrigação. Registrada aqui
como duplicação consciente.

## Inventário

| Objeto | Tipo | Obrigação |
|---|---|---|
| `PositiveWeylCoefficient` | `structure` | interface de saída |
| `PositiveWeylCoefficient.ofFactors` | `def` | construtor |
| `PositiveWeylCoefficient.ofFactors_coefficient` | `theorem` (`rfl`, `@[simp]`) | interface |
| `dimension_div_order_pos` | `theorem` | B4 |
| `measure_pos_of_isOpen_subset` | `theorem` | GWB-008A passo 5 |
| `coefficient_pos_of_factors` | `theorem` | GWB-008B |
| `integral_pos_of_nonneg_of_support_measure_pos` | `theorem` | variante integral do passo 6 |

Quatro teoremas próprios, uma estrutura, um construtor, um lema `rfl`.

## Lemas Mathlib reutilizados

Inspecionados na revisão fixada (`v4.33.0-rc1`, rev
`79d0395a1825a6264ad5d269e35e60537518955e`) e registrados em `Audit.lean`:

```text
IsOpen.measure_pos
  {X} [TopologicalSpace X] {m : MeasurableSpace X} (mu : Measure X)
  [mu.IsOpenPosMeasure] {U} : IsOpen U -> U.Nonempty -> 0 < mu U

measure_mono : s subset t -> mu s <= mu t

Measure.IsOpenPosMeasure  (classe)

integral_pos_iff_support_of_nonneg :
  0 <= f -> Integrable f mu -> (0 < integral f <-> 0 < mu (support f))

Measure.measure_pos_of_nonempty_interior :
  (interior s).Nonempty -> 0 < mu s
```

Nota de assinatura: a `MeasurableSpace` é **implícita** (`{m : ...}`), não
instância. Os wrappers locais espelham essa escolha; a primeira versão os
declarava com `[MeasurableSpace X]` e falhava por incompatibilidade com
`MeasureSpace.toMeasurableSpace` no ponto de uso.

## O que o núcleo **não** define — lista vinculante

```text
manifold
cotangent bundle
pseudodifferential operator
principal symbol
Liouville measure
concrete Weyl coefficient
spectral counting function of an operator
```

Nenhum desses aparece no diretório. A verificação é mecânica: busca por
`manifold`, `cotangent`, `pseudodiff`, `symbol`, `Liouville`, `Weyl`,
`zeta`, `Riemann`, `operator`, `spectral`, `Polya` nos arquivos `.lean` de
`Geometry/`.

## Imports

`PositiveCoefficient.lean` importa exatamente:

```text
Mathlib.MeasureTheory.Measure.OpenPos
Mathlib.MeasureTheory.Integral.Bochner.Basic
```

O teste isolado importa adicionalmente
`Mathlib.MeasureTheory.Measure.Lebesgue.Basic`, apenas para exibir
instâncias concretas em `ℝ`. Nenhum import de geometria diferencial,
análise complexa ou teoria espectral.

## O que este núcleo **não prova**

```text
NAO prova que B_x eh aberto (exigiria p_m).
NAO prova que vol(B_x) eh finito (GWB-008C, GAP-RH-015).
NAO prova que x |-> vol(B_x) eh continua.
NAO prova a lei de Weyl, local ou global.
NAO constroi operador algum.
NAO instancia PowerCountingLaw a partir de geometria.
NAO aplica ASYM-NOGO-001.
```

Um invólucro de teoria da medida não prova a lei de Weyl. Ele prova que
*se* alguém entregar um aberto não vazio dentro de um conjunto, *então* a
medida desse conjunto é positiva — e nada além.
