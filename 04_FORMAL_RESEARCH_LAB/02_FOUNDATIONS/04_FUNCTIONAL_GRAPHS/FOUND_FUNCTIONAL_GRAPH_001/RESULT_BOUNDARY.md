---
document_id: FFG-RESULT-BOUNDARY
status: BINDING
---

# FOUND-FUNCTIONAL-GRAPH-001 — Fronteira do resultado

## Registro literal

```text
Foi provado:

- alcance por iteração é reflexivo e transitivo;
- encontro eventual é reflexivo, simétrico e transitivo;
- alcance por iteração implica encontro eventual;
- pontos periódicos que se encontram eventualmente determinam
  a mesma órbita periódica;
- toda trajetória em um tipo finito alcança, antes de card X
  passos, um ponto periódico;
- todos os pontos periódicos do mesmo componente funcional
  determinam a mesma órbita periódica;
- contraexemplos finitos impedem generalizações indevidas.

Não foi provado:

- ponte com conectividade de SimpleGraph;
- decomposição em árvores;
- distância mínima ao ciclo;
- tempo mínimo de entrada;
- período mínimo no teorema principal;
- representante canônico;
- quociente formal dos componentes;
- classificação completa;
- qualquer resultado sobre sistemas infinitos;
- novidade matemática;
- qualquer interpretação física.
```

## Interpretação vinculante da unicidade

```text
A unicidade provada eh da ORBITA PERIODICA do componente definido por
EventuallyMeets.
```

Não é unicidade:

```text
do ponto periodico       — FFG-CE-005 exibe dois, distintos
do indice de entrada     — mu nao eh afirmado minimo
do periodo               — nao eh afirmado minimo
do representante         — f^[mu] x eh UM representante, nao O representante
de um ciclo global       — FFG-CE-001 exibe dois ciclos
```

E **não** é uma decomposição por `SimpleGraph`.

## Tabela do que dizer

| ❌ Não escrever | ✅ Escrever |
|---|---|
| "Cada sistema tem um atrator único" | "Todos os pontos periódicos de um componente determinam a mesma órbita" |
| "Existe um ponto periódico canônico" | "O objeto único é a órbita, não o representante" |
| "Componente = alcançabilidade mútua" | "Componente = classe de `EventuallyMeets`; `FFG-CE-004` refuta a outra leitura" |
| "Coincide com componente conexa do grafo" | "A ponte com `SimpleGraph` não foi provada" |
| "estado recorrente" | "ponto periódico", ou `x ∈ Function.periodicPts f` |
| "μ é o tempo de entrada" | "μ é **um** índice com `μ < card X`; a minimalidade não foi provada" |
| "Isso fundamenta TRI/TDTR" | "Nenhuma ponte com TRI/TDTR foi construída" |

## Novidade

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

A decomposição "forma rho" da iteração finita é material padrão. Toda a
maquinaria de ciclos já existia na Mathlib; o trabalho desta frente foi
conectá-la a `EventuallyMeets` e ao resultado já verificado de
`FOUND-SEMIGROUP-002`.

`FFG-GAP-014` permanece `OPEN_BIBLIOGRAPHIC`: nenhuma fonte primária foi
obtida. Portanto **nenhuma afirmação de prioridade histórica ou atribuição
a autor é permitida**.

## Relação com `FOUND-SEMIGROUP-002`

Reutilização de **API verificada**, não extensão de escopo. O
`extension_status` daquela frente permanece `NOT_AUTHORIZED`, e nenhum de
seus arquivos matemáticos foi tocado.
