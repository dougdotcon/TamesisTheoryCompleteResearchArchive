---
document_id: FCD-SPECIFICATION-REVIEW
gate: FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW
reviewed_commit: 03e1ec36b97233df481597980f0a5383b2decc65
decision: A_SPECIFICATION_REVIEW_APPROVED
probe: /tmp/CycleDetectionReviewProbe.lean (removido)
permanent_lean_files: 0
---

# Revisão da especificação

Revisão, correção e congelamento da especificação antes de autorizar a
formalização. **Nenhum módulo Lean permanente. Nenhuma prova permanente.
Nenhum `lake build`.**

## Correção obrigatória aplicada

```text
prefixIndex  ->  baseIndex
```

Quarenta ocorrências substituídas em oito documentos da especificação. Os
registros históricos **fora** da pasta de especificação — o JSON de
resultado do gate anterior, a sessão daquele gate e o changelog — **não
foram reescritos**; a decisão anterior está marcada como superada em
`DATA_MODEL.md` e na tabela de renomeações de
`SPECIFICATION_DECISION.md`.

Motivo vinculante:

```text
baseIndex eh o indice-base da igualdade

f^[baseIndex + period] x = f^[baseIndex] x.

Ele NAO eh necessariamente o menor indice de entrada no ciclo.
```

`prefix` ainda podia ser lido como "o prefixo antes do ciclo", isto é,
como minimalidade. `baseIndex` não tem essa leitura.

## Probe descartável

Criado, executado e removido: `/tmp/CycleDetectionReviewProbe.lean`.
Contém versões **descartáveis** de `CycleWitness`, `cycleCandidates` e
`detectCycleWitness?`, cinco modelos concretos e `#eval`. **Sem `axiom`,
`sorry`, `admit`, `unsafe`, `noncomputable`, `Classical.choose` ou
teoremas permanentes.** Executado com `lake env lean` em 28 s, **sem
erros**. `lake build` **não** foi executado.

## Resultados concretos medidos

### Enumeração

```text
cycleCandidates 0          = []                    (por rfl)
cycleCandidates 1          = [<0,1>]               (por rfl)
(cycleCandidates 3).length = 6
(cycleCandidates 4).length = 10
(cycleCandidates 5).length = 15
```

Fronteira `baseIndex + period = n`, medida por filtro:

```text
n = 3  ->  <0,3>, <1,2>, <2,1>
n = 4  ->  <0,4>, <1,3>, <2,2>, <3,1>
```

**Incluída.** A observação de que o comprimento é `n(n+1)/2` agora tem
três medidas concordantes (6, 10, 15) — e continua **não sendo um lema**.

### Os cinco casos obrigatórios

| Caso | Modelo | Esperado | **Medido** |
|---|---|---|---|
| unitário | `Fin 1`, `id` | `⟨0,1⟩` | **`some ⟨0,1⟩`** |
| `Bool` fixo | `id` | `⟨0,1⟩` | **`some ⟨0,1⟩`** nos dois estados |
| alternância | `not` | `⟨0,2⟩` | **`some ⟨0,2⟩`** nos dois estados |
| cauda + ponto fixo | `Fin 3`, `0→1→2→2` | `⟨2,1⟩` | **`some ⟨2,1⟩`** a partir de `0` |
| cauda + ciclo de dois | `Fin 4`, `0→1→2→3→2` | `⟨2,2⟩` | **`some ⟨2,2⟩`** a partir de `0` |

**Os cinco bateram.** Nenhuma função e nenhuma ordem foi alterada para
satisfazer expectativa.

Resultados adicionais, a partir dos demais estados iniciais:

```text
Fin 3:  de 1 -> <1,1>      de 2 -> <0,1>
Fin 4:  de 1 -> <1,2>      de 2 -> <0,2>      de 3 -> <0,2>
```

Estes ilustram, concretamente, o que `CD-TEST-005` previa: o `period`
testemunhado é o mesmo dentro do componente, e o `baseIndex` **não** é —
ele depende do estado inicial.

## Achado de auditoria: pegada axiomática

```text
#print axioms cycleCandidates      does not depend on any axioms
#print axioms detectCycleWitness?  [propext, Classical.choice, Quot.sound]
```

Origem localizada com um segundo probe:

```text
List.range        sem axiomas
List.flatMap      sem axiomas
List.find?        sem axiomas
Nat.iterate       sem axiomas
cycleCandidates   sem axiomas

Fintype.card      [propext, Classical.choice, Quot.sound]
Finset.univ       [propext, Classical.choice, Quot.sound]
```

Uma variante `detectAt? (n : ℕ)`, que recebe a cota explicitamente em vez
de calculá-la, **não depende de axioma algum** — e também avalia.

Conclusão vinculante:

```text
Pegada axiomatica NAO eh o mesmo que noncomputabilidade.
```

`Fintype.card` é computável — `#eval Fintype.card (Fin 3)` devolveu `3` —
e ainda assim carrega `Classical.choice` na pegada, porque a
infraestrutura de `Finset` da Mathlib usa escolha em **provas**. O
critério operacional correto para "sem `Classical.choice`" é:

```text
a definicao nao eh marcada noncomputable;
#eval funciona;
nenhum Classical.choose produz DADO.
```

Os três foram confirmados. Ver `COMPUTABILITY_REVIEW.md`.

## Efeito sobre `ValidAt`

O achado poderia sugerir adotar `ValidAt n` para obter um núcleo sem
axiomas. **Não adotado**, e agora com razão medida: `detectCycleWitness?`
precisa **calcular** `Fintype.card X` para saber onde parar, de modo que a
pegada retorna de qualquer maneira. `ValidAt` mudaria o predicado sem
mudar o detector.

```yaml
ValidAt: DEFERRED
```

## Verificação item a item

| Item do gate | Estado |
|---|---|
| algoritmo congelado | `BOUNDED_CERTIFICATE_SEARCH` |
| Floyd, tabela visitada, Brent fora da v1 | confirmado — nenhum é dependência |
| `prefixIndex` corrigido | 40 ocorrências → `baseIndex` |
| `period` como testemunha não mínima | reafirmado em todos os documentos públicos |
| `CycleWitness` com dois naturais | congelado |
| `Valid` coincide com a colisão limitada | conferido termo a termo contra o fonte |
| enumeração completa | `mem_cycleCandidates_iff` congelado |
| caso `n = 0` e `n = 1` | verificados por `rfl` no probe |
| fronteira de soma | verificada por filtro |
| detector computável | `#eval` em cinco modelos |
| soundness | `List.find?_some` + `decide_eq_true_eq` |
| completeness | transporte de `exists_bounded_iterate_collision` |
| pigeonhole | não repetido |
| `DecidableEq` limitada | confirmado |
| `periodicOrbit` proposicional | confirmado |
| minimalidade aberta | `CD-GAP-009`, `CD-GAP-010` |
| totalização classificada | `DEFERRED`, `OPTIONAL_CORE` |
| nenhuma implementação permanente | 0 arquivos Lean no repositório |

## Decisão

```text
A. FOUND_CYCLE_DETECTION_001_SPECIFICATION_REVIEW_APPROVED
```
