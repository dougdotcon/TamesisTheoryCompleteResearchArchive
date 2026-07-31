---
document_id: FFG-KNOWN-RESULTS-MATRIX
bibliographic_audit: NOT_AUDITED
---

# FOUND-FUNCTIONAL-GRAPH-001 — Matriz de resultados conhecidos

## Aviso de método

Nenhuma fonte primária sobre grafos funcionais foi obtida ou auditada
(`FFG-GAP-014`). A coluna "literatura" reflete **conhecimento geral
elementar**, não auditoria.

```text
Nenhuma afirmacao de prioridade historica eh permitida.
Nenhuma atribuicao a autor eh permitida.
```

## Matriz

| Resultado | Literatura | Mathlib fixada | Aqui |
|---|---|---|---|
| alcançabilidade por iteração | elementar | não como definição própria | a definir (`IterReachable`) |
| encontro eventual de trajetórias | elementar | **ausente** | a definir (`EventuallyMeets`) |
| ponto periódico, período mínimo | padrão | `periodicPts`, `minimalPeriod` | reutilizar |
| órbita periódica como ciclo | padrão | `periodicOrbit : Cycle α` | **reutilizar** |
| invariância da órbita por iteração | padrão | `periodicOrbit_apply_iterate_eq` | **reutilizar** |
| toda trajetória finita atinge ciclo | elementar | ausente | já provado em `FOUND-SEMIGROUP-002` |
| um ciclo por componente | padrão | ausente **nesta forma** | a formalizar |
| decomposição em cauda + árvores | padrão | ausente | **adiada** |
| contagem de componentes | padrão | ausente | **fora de escopo** |

## O achado que importa

Ao contrário de `FOUND-SEMIGROUP-002` — onde o alvo simplesmente **não
existia** na Mathlib —, aqui **toda a maquinaria de ciclos já existe**. O
que falta é a relação de componente e a ponte com o resultado da frente
anterior.

Consequência honesta: o conteúdo matemático próprio desta frente é ainda
**menor** que o da anterior. O valor é de **API e integração**.

## Posição em relação a `FOUND-SEMIGROUP-002`

| Pergunta | `FOUND-SEMIGROUP-002` | `FOUND-FUNCTIONAL-GRAPH-001` |
|---|---|---|
| escala | uma trajetória | estrutura global |
| objeto central | `μ`, `λ`, propagação | componente e órbita |
| finitude usada em | tudo da Camada C | apenas `FFG-REC-*` |
| pigeonhole | **consumido aqui** | reutilizado, não reaplicado |
