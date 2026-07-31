---
bridge_id: RVM-LIMIT
status: SPECIFIED_NOT_FORMALIZED
---

# `N_ζ` e a lei `T log T`

## Definição de `N_ζ(T)`

Forma moderna, **compatível com a auditoria primária** de
`08_REVIEWS/SOURCES/RH_NOGO/VON_MANGOLDT_1905_AUDIT.md`:

```text
N_ζ(T) := numero de zeros nao triviais de zeta com ordenada positiva
          ate T, contados com multiplicidade.
```

Convenções fixadas pela fonte primária (von Mangoldt 1905, p. 2):

| Item | Convenção | Citação |
|---|---|---|
| objeto contado | zeros de `ξ(t)` por **parte real** | „deren reelle Teile zwischen 0 und `T` liegen“ |
| multiplicidade | **incluída** | „jede so oft gezählt, als ihre **Ordnungszahl** angibt“ |
| fronteira | `T` **escolhido fora de zeros** | „daß die letztere Parallele durch keine Nullstelle der Funktion ξ(t) hindurchgeht“ |
| faixa | zeros não triviais | região `|Im t| ≤ 1/2` ⟷ `0 ≤ Re s ≤ 1` (Riemann; Bombieri) |
| tradução | `Re t` ⟷ `Im ρ` | eq. (1) de von Mangoldt: `t = T − ia ⟹ s = 1/2 + a + iT` |

**Divergência de convenção registrada, não resolvida:** von Mangoldt evita
zeros na fronteira escolhendo `T`; a definição moderna usa
`0 < Im ρ ≤ T` (ou `< T`). A reconciliação é elementar — as duas contagens
diferem no máximo pela multiplicidade dos zeros com ordenada exatamente `T`,
um conjunto discreto — mas **não está escrita**. Ver
`SPECTRAL_MATCH_CONVENTIONS.md`, obrigação SMC-002.

Choque de notação a evitar: na Fig. 1 da p. 2 de von Mangoldt o zero
genérico é escrito `β + iγ` no plano `t`, com `β` sendo a **parte real** —
isto é, a ordenada moderna. Inverso da convenção `ρ = β + iγ` do plano `s`.

## RVM-STRONG

```text
N_ζ(T) = (T/2π)·log(T/2π) − T/(2π) + 7/8 + O(log T)
```

```yaml
source: VONMANGOLDT-1905
page: 19
equation_or_theorem: "formula final do artigo"
literal_form: >
  N = (T/2pi) l(T/2pi) - T/2pi + 7/8
      + eta*(0,43200 lT + 1,91662 llT + 12,20373),  (-1 < eta < 1),
  valida para T > 28,558
evidence_status: SOURCE_DIRECT
conditional_on_RH: false
requires_formalization: true
note: >
  Termo de erro EFETIVO, com constantes explicitas. Consistencia interna
  verificada: 12,20373 + 7/8 = 13,07873, que eh a cota da p.1 na forma sem
  o termo 7/8.
```

## RVM-LIMIT

```text
N_ζ(T) / (T log T) → 1/(2π)
```

```yaml
derivation_from: RVM-STRONG
evidence_status: ELEMENTARY_COROLLARY_REQUIRING_FORMALIZATION
requires_formalization: true
steps_sketched_not_proved:
  - "log(T/2pi)/log T -> 1"
  - "(T/2pi)*log(T/2pi) / (T log T) -> 1/(2pi)"
  - "T/(2pi) / (T log T) -> 0"
  - "7/8 / (T log T) -> 0"
  - "O(log T) / (T log T) -> 0"
constant: "c = 1/(2pi) > 0"
```

**Não formalizado neste gate.** A formalização exigiria `ζ`, seus zeros e a
fórmula RVM-STRONG — muito além de qualquer autorização vigente.

## Papel na arquitetura

`RVM-LIMIT` fornece a hipótese `hTLog` de `ASYM-NOGO-001` **para `N_ζ`**,
com `c = 1/(2π)`. Ela é transportada para `N_P` pelo `COUNTING-LAW-BRIDGE`,
não diretamente.

```text
VON-MANGOLDT-1905 → RVM-STRONG → RVM-LIMIT
                                      ↓ (via COUNTING-LAW-BRIDGE, com E2)
                                 TLOG-LAW-FOR-NP
```
