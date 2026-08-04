---
document_id: FOUND-MONOVARIANT-DESCENT-001-SPECIFICATION-REVIEW
work_item_id: FOUND-MONOVARIANT-DESCENT-001
review_start_head: e3337354a157cf8559271844457ae7d82d8c9bee
decision: FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_REVIEW_APPROVED
defects_found: 1
defects_corrected: 1
---

# Revisão de especificação

## Reexecução

O probe foi **rodado de novo neste gate**.

```text
REAL_PROBE4_EXIT   0
error_lines        0
git_dirty          0
Fintype            0
DecidableEq        0
instancias         0
```

## Pegada, medida agora

```text
Monovariant.iterate_lt            propext, Quot.sound
Monovariant.no_periodic_point     propext, Quot.sound
analyzeAbstractSystem_period_pos  propext, Classical.choice, Quot.sound
monovariant_not_orbitSeparating   propext, Classical.choice, Quot.sound
```

Bate com o esperado. `Classical.choice` entra **apenas** no que atravessa
`analyzeEncodedSystem`, e sua remoção é proibida.

## O defeito, e ele é o segundo seguido

```text
derivado por script   12
declarado             13
soma das partes       12
```

A decomposição — `7` públicas, `1` privado, `2` TEST_ONLY, `2` testes —
estava **correta**. O total é que estava errado, e o campo
`extra_negation_registrations: 1` era espúrio: inventado para fazer a
conta fechar em `13`.

**É o segundo defeito de contagem agregada em duas frentes
consecutivas.** A proibição gravada no gate anterior — *não escrever
contagem agregada sem derivá-la por script no mesmo gate* — foi violada
por mim no gate seguinte ao que a criou.

Correção: contra a derivação. A decomposição não foi mexida.

## Os sete itens

| # | Item | Veredito |
|---|---|---|
| 1 | A medida vive em `Nat`, sem ordem geral | CONFIRMADO |
| 2 | `no_periodic_point` exclui recorrência positiva | CONFIRMADO |
| 3 | `0 < period` recuperado da API pública | CONFIRMADO |
| 4 | A recuperação não toca frente encerrada | CONFIRMADO |
| 5 | O negativo não tem hipótese inventada | CONFIRMADO |
| 6 | `strictDown_not_monovariant` compila | CONFIRMADO |
| 7 | Contagem derivada = declarada | **CORRIGIDO** |

## O item 6, que é o registro honesto

`Nat` é bem fundado e ainda assim `k - 1` **não** é monovariante, porque
falha em zero. A negação compila, e existe para que boa fundação nunca
seja lida como suficiente.

## Decisão

```text
FOUND_MONOVARIANT_DESCENT_001_SPECIFICATION_REVIEW_APPROVED
```

## Ressalva

Mesmo agente, sessão única. Não substitui revisão externa. O que sustenta
a aprovação é o que foi reexecutado — e, de novo, o que a derivação por
script **recusou**.
