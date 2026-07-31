# COUNTING-LAW-BRIDGE — auditoria da prova

Revisão adversarial do módulo `Bridge/`.

## Auditoria de axiomas do kernel

`#print axioms` nos treze objetos rastreáveis
(`eventually_tLogScale_ne_zero`, `tendsto_tLogScale_atTop`,
`tendsto_const_mul_tLogScale_div`, `subdominantDifference_tendsto_zero`,
`target_normalization_eq`, `eventually_target_normalization_eq`,
`counting_law_bridge`, `TLogCountingLaw.transfer`,
`countingLawBridgeStatement_holds`, `tendsto_tLog_of_eq_main_add_littleO`,
`subdominantTLog_of_eventualEquality`,
`boundedDifference_of_eventualEquality`,
`subdominantTLog_of_boundedDifference`):

```text
[propext, Classical.choice, Quot.sound]
```

em **todos**. Nenhum `sorryAx`, nenhum axioma local. São os três axiomas
padrão do Lean/Mathlib.

## Auditoria de escopo por imports

Imports de toda a pasta `Bridge/`:

```text
Mathlib.Analysis.SpecialFunctions.Log.Basic
Mathlib.Analysis.SpecialFunctions.Pow.Real
Mathlib.Analysis.Asymptotics.Lemmas
(o resto sao imports internos da propria pasta)
```

Busca por menções proibidas (`zeta`, `Riemann`, `Weyl`, `Complex`,
`spectral`, `operator`, `Polya`) em todos os arquivos de `Bridge/`:
**nenhuma ocorrência**.

`Mathlib.Analysis.SpecialFunctions.Pow.Real` entra apenas por causa de
`T ^ exponent` (`Real.rpow`) na interface `PowerCountingLaw`, que **não é
usada** na prova da ponte.

## Checklist adversarial

| Risco | Verificação | Resultado |
|---|---|---|
| **Hipótese ociosa mantida** | Lean mostrou que `0 < c` não é necessária em `counting_law_bridge`; foi **removida** e a positividade ficou só em `TLogCountingLaw` | Corrigido |
| **Hipótese ociosa na identidade algébrica** | `a/s + (b−a)/s = b/s` vale em corpo mesmo com `s = 0`; a versão pontual dispensa não nulidade | Evitada |
| **Afirmação global sobre `Real.log`** | `Real.log T ≤ 0` para `0 < T ≤ 1` e `Real.log` é 0 em `T ≤ 0`; toda positividade é afirmada sob `1 < T` via `filter_upwards` | OK |
| **Reprova manual de `little-o`** | usou-se `IsLittleO.tendsto_div_nhds_zero` da Mathlib, sem desdobrar a definição | OK |
| **Constante alterada na transferência** | `transfer_constant` prova por `rfl` que `constant` é preservada; verificado também no teste isolado | OK |
| **`ASYM-NOGO-001` aplicado** | busca no módulo: nenhuma referência a `asym_nogo_001` nem a `AsymptoticCore` | **Não aplicado** |
| **Dependência circular** | grafo: `Definitions → TLogScale → LittleOTransfer → CountingLawBridge → StrongAsymptoticCorollary → Audit`; acíclico | OK |
| **Import mascarando dependência** | três imports Mathlib, todos elementares; nenhum de teoria analítica dos números, PDE ou geometria | OK |
| **Autoimplícitos silenciosos** | `set_option autoImplicit false` em todos os arquivos da pasta | OK |
| **`decide`/`native_decide` em proposição infinitária** | nenhum uso | OK |
| **Novidade matemática alegada** | `scientific_novelty: STANDARD_ASYMPTOTIC_TRANSFER_FORMALIZED_FOR_LOCAL_USE` em todos os itens | OK |

## Falhas reais ocorridas e corrigidas

1. `Definitions.lean` — falha de síntese de instância em
   `T ^ exponent`: faltava `Mathlib.Analysis.SpecialFunctions.Pow.Real`
   para `Real.rpow`. Import acrescentado.
2. `LittleOTransfer.lean` — `Unknown identifier div_add_div_same`. Trocado
   por `simp only [div_eq_mul_inv]; ring`, que vale em qualquer corpo e não
   depende do nome de um lema específico.
3. `CountingLawBridge.lean` — *"type of theorem `TLogCountingLaw.transfer`
   is not a proposition"*: `TLogCountingLaw` vive em `Type` (carrega o dado
   `constant`), logo a transferência é `def`, não `theorem`. Corrigido.
4. `StrongAsymptoticCorollary.lean` — `rewrite` falhou porque
   `SubdominantTLog` é um `def` não redutível e o alvo não se desdobrava em
   `refine`. Corrigido com `show` explícito em cada prova.

Nenhuma dessas falhas foi contornada com token proibido.

## Alcance — o que foi e o que não foi provado

```text
Foi provado:
uma lei de normalizacao T log T pode ser transferida entre duas
funcoes cuja diferenca seja o(T log T).

Nao foi provado:
que N_zeta satisfaz Riemann-von Mangoldt;
que uma funcao espectral satisfaz Weyl;
que algum operador pertence a W-ELLIPTIC-SCALAR;
que N_P e N_zeta possuem diferenca subdominante;
RH-NOGO-001;
qualquer afirmacao sobre Hilbert-Polya ou RH.
```

O corolário `STRONG-TLOG-COROLLARY` fecha `SB-GAP-010A` — a passagem
genérica "fórmula forte ⟹ limite" — mas **não** `SB-GAP-010B`, que exigiria
provar em Lean que a função `N_ζ` concreta satisfaz a fórmula de
Riemann–von Mangoldt.
