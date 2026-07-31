---
document_id: FCD-REVIEW-DECISION
decision: A_FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED
---

# Decisão da revisão

```text
A. FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED
```

## Critérios de aprovação

| Critério | Estado |
|---|---|
| `baseIndex` congelado | 40 ocorrências renomeadas; nome antigo proibido |
| `CycleWitness` com apenas dois naturais | congelado |
| `Valid` coincide com a colisão limitada | conferido termo a termo contra o fonte |
| `cycleCandidates` completa | `mem_cycleCandidates_iff` congelado |
| caso de fronteira incluído | medido por filtro para `n = 3` e `n = 4` |
| `detectCycleWitness?` computável | `#eval` em cinco modelos |
| soundness corretamente planejada | `of_decide_eq_true` / `decide_eq_true_eq` |
| completeness reutiliza a prova anterior | transporte de `exists_bounded_iterate_collision` |
| `DecidableEq` limitada | ausente das sete camadas proposicionais |
| `periodicOrbit` proposicional | nunca entra na definição executável |
| minimalidade aberta | `CD-GAP-009`, `CD-GAP-010` |
| totalização classificada | `DEFERRED` / `OPTIONAL_CORE` |
| nenhuma implementação permanente | 0 arquivos Lean no repositório |

Nenhuma das dezesseis condições de `NEEDS_CORRECTIVE_PATCH` ocorreu.

## Correções aplicadas nesta revisão

1. **`prefixIndex` → `baseIndex`**, em 40 ocorrências e 8 documentos.
2. **Instância `CycleWitness.decidableValid` acrescentada às assinaturas
   congeladas.** A especificação inicial supunha que `decide (Valid ...)`
   elaboraria sozinho; o probe mostrou que não — `Valid` é um `def` e a
   resolução de instâncias não o desdobra.
3. **Critério de `Classical.choice` reformulado.** A pegada axiomática de
   `detectCycleWitness?` inclui `Classical.choice`, por `Fintype.card`, e
   isso **não** o torna noncomputável. O critério operacional passou a
   ser: não `noncomputable`, `#eval` funciona, nenhum `Classical.choose`
   produzindo dado.
4. **`CycleWitness.propagates` alinhada** à ordem de argumentos de
   `collision_propagates`: hipótese primeiro, `k` depois.
5. **Rota única de completude selecionada**: `List.find?_isSome` seguido
   de `Option.isSome_iff_exists`. As outras três rotas auditadas ficam
   registradas como alternativas, sem segunda prova pública.

## Sobre o adaptador de componente

`detected_cycle_is_component_cycle` permanece `OPTIONAL_CORE`. Auditoria:
ele replica, com o `f^[baseIndex] x` no lugar do `f^[mu] x`, exatamente o
conteúdo de `exists_component_cycle_with_entry_bound`. **Pode ser omitido
da primeira formalização** e documentado como adaptador futuro. Não é
dependência de soundness nem de completeness.

Se for omitido: `CD-GAP-012` volta a `OPEN_DEFERRED`. Se for incluído:
`READY_FOR_FORMALIZATION`. A escolha é do gate de formalização; a
especificação registra as duas rotas.

## Estado final

```yaml
active_work_item: FOUND-CYCLE-DETECTION-001
work_status: READY
specification_status: APPROVED
current_blocker: null
authorized_action: FOUND_CYCLE_DETECTION_001_FORMALIZATION_AUTHORIZED
```

**Não autorizados**: Floyd, Brent, tabela visitada, extração, integração
e minimalidade.

## Próxima ação

Formalizar a enumeração finita de certificados, o detector parcial
executável, sua soundness e sua completeness por reutilização de
`exists_bounded_iterate_collision`.

A formalização **não** começa neste gate.
