---
schema: tamesis-bridge-specification/1
work_item_id: RH-NOGO-001
gate: RH_NOGO_SOURCE_BRIDGE_SPECIFICATION
decision: SOURCE_BRIDGE_SPECIFICATION_READY
proof_executed: false
---

# Especificação da ponte entre leis de contagem

Documento-índice. **Nada aqui é provado.** O gate especifica interfaces e
enumera obrigações.

## Arquitetura

```text
W-ELLIPTIC-SCALAR                     (classe geométrica estreita)
        ↓ GLOBAL-WEYL-BRIDGE-SCALAR   (9 obrigações GWB-001..009)
W-POWER                               (interface assintótica abstrata)
        ↓ COUNTING-LAW-BRIDGE         (o(T log T) ⟹ mesma lei T log T)
ASYM-NOGO-001                         (VERIFIED em Lean)
```

O ponto da arquitetura é que `W-POWER` **não menciona operadores**. Qualquer
estreitamento futuro de `W-ELLIPTIC-SCALAR` — ou sua eventual rejeição —
deixa `ASYM-NOGO-001` intacto.

## Documentos

| Arquivo | Conteúdo |
|---|---|
| `W_ELLIPTIC_SCALAR_V2.md` | classe geométrica estreita; distinção operador formal / domínio / realização |
| `W_ELLIPTIC_SYSTEM_DEFERRED.md` | sistemas e fibrados, **fora** da v2 |
| `GLOBAL_WEYL_BRIDGE_OBLIGATIONS.md` | GWB-001 a GWB-009, com fonte e estado |
| `RVM_LIMIT_BRIDGE.md` | `N_ζ`, RVM-STRONG, RVM-LIMIT |
| `COUNTING_LAW_RELATIONS.md` | níveis E0–E3 e a hierarquia |
| `COUNTING_LAW_BRIDGE_SPEC.md` | o lema-ponte central |
| `NARROW_NOGO_STATEMENT.md` | enunciado estreito candidato |
| `SPECTRAL_MATCH_CONVENTIONS.md` | convenções de identificação espectro ↔ zeros |
| `SOURCE_BRIDGE_DEPENDENCY_DAG.yaml` | DAG com estado por seta |
| `SOURCE_BRIDGE_GAP_REGISTER.yaml` | lacunas desta especificação |
| `SOURCE_BRIDGE_LEAN_FEASIBILITY.md` | viabilidade e assinaturas |

`W-POWER` continua definida em
`08_REVIEWS/SOURCES/RH_NOGO/W_POWER_CLASS.md`; reproduzida abaixo em forma
normativa.

## W-POWER (forma normativa)

```yaml
class_id: W-POWER
data:
  counting_function: "N_P : ℝ → ℝ"
  exponent: "α : ℝ"
  leading_constant: "C_P : ℝ"
assumptions:
  alpha_positive: "0 < α"
  leading_constant_positive: "0 < C_P"
  power_limit: "N_P(Λ) / Λ^α → C_P quando Λ → +∞"
not_presupposed:
  - operador
  - espaço de Hilbert
  - auto-adjunção
  - elipticidade
  - variedade
  - PDE
  - função zeta
```

`ASYM-NOGO-001` recebe **exatamente** os dados de `W-POWER` mais uma
normalização positiva por `Λ log Λ`:

```lean
theorem asym_nogo_001 (N : ℝ → ℝ) (α c C : ℝ)
    (hα : 0 < α) (hc : 0 < c) (hC : 0 < C)
    (hTLog : Tendsto (fun T => N T / (T * Real.log T)) atTop (nhds c))
    (hPower : Tendsto (fun T => N T / T ^ α) atTop (nhds C)) : False
```

`hPower` **é** a pertinência a `W-POWER`.

## Mudança central em relação aos gates anteriores

O alvo **deixa de ser** igualdade espectral exata. A relação central passa a
ser

```text
N_P(T) − N_ζ(T) = o(T log T)                     (nível E2)
```

que cobre igualdade exata, igualdade eventual, discrepância `O(1)` e
equivalência por razão. O alvo resultante é estreito **e** mais robusto:
exclui não só coincidência perfeita, mas qualquer modelo da classe cuja
contagem difira da dos zeros apenas por termo subdominante.

## Evidência canônica

A identidade local→global de Ivrii, eq. (3.1.11)
`N⁻(λ) = ∫ e(x,x,λ) dx`, não pôde ser verificada independentemente por
fontes públicas fora deste laboratório. **A cópia preservada em
`08_REVIEWS/SOURCES/RH_NOGO/pdf/ivrii_2016_100years_weyl.pdf`
(`sha256 9ca07737…`, 90 pp.) é a evidência canônica dessa identidade**, com
página e proveniência no `SOURCE_MANIFEST.yaml`.

## O que este gate NÃO fez

- não provou nenhuma obrigação;
- não formalizou operadores pseudodiferenciais;
- não formalizou Riemann–von Mangoldt;
- não formalizou a lei de Weyl;
- não aplicou `ASYM-NOGO-001`;
- não estendeu nada a sistemas, fibrados ou problemas de bordo;
- não afirmou nada sobre Hilbert–Pólya nem sobre a Hipótese de Riemann.
