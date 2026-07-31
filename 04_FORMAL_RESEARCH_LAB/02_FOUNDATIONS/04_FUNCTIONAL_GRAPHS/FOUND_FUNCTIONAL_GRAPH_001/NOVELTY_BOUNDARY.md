---
document_id: FFG-NOVELTY-BOUNDARY
status: BINDING
---

# FOUND-FUNCTIONAL-GRAPH-001 — Fronteira de novidade

## Registro literal

```text
Grafos funcionais finitos e sua decomposicao em ciclos e
trajetorias de entrada sao matematica padrao.

Nenhum resultado proposto eh uma descoberta matematica.

O valor da frente esta em:

- formalizacao reutilizavel;
- API de componentes funcionais;
- composicao com periodicidade eventual ja verificada;
- contraexemplos;
- aplicacoes futuras em software;
- separacao precisa entre alcance, componente e ciclo.
```

```yaml
mathematical_novelty: NONE
research_role: FORMAL_FOUNDATION
```

## Proibido

```text
nova teoria de dinamica;
nova teoria do tempo;
lei universal;
descoberta fisica;
entropia;
TRI;
TDTR;
teoria de tudo;
Hipotese de Riemann;
problemas Clay.
```

## Tabela do que dizer

| ❌ Não escrever | ✅ Escrever |
|---|---|
| "Descobrimos a estrutura dos sistemas discretos" | "Formalizamos a decomposição padrão de grafos funcionais finitos" |
| "Cada sistema tem um atrator único" | "Todos os pontos periódicos de um componente determinam a mesma órbita" |
| "Provamos que existe um ponto periódico canônico" | "O objeto único é a órbita, não o representante" |
| "Componente = alcançabilidade mútua" | "Componente = classe de `EventuallyMeets`; `FFG-CE-004` refuta a outra leitura" |
| "Coincide com componente conexa do grafo" | "A ponte com `SimpleGraph` está diferida (`FFG-GAP-012`)" |
| "Isso fundamenta TRI/TDTR" | "Nenhuma ponte com TRI/TDTR foi construída" |
| "Aplicável a máquinas de estado, logo relevante" | "A reutilização em software não transforma o resultado padrão em descoberta" |

## Contexto histórico honesto

A observação de que a iteração de uma função sobre conjunto finito produz
uma "forma rho" — cauda seguida de ciclo — é material introdutório padrão,
e algoritmos que a exploram (Floyd, Brent) são clássicos.

Como `FFG-GAP-014` registra bibliografia `NOT_AUDITED`, **nenhuma
afirmação de prioridade histórica ou atribuição a autor é permitida**.

## A tentação específica desta frente

O vocabulário — "componente", "bacia de atração", "estado recorrente",
"estado transitório" — vem da teoria de sistemas dinâmicos e convida a ler
o resultado como afirmação sobre sistemas reais. Não é. É uma afirmação
sobre `f : X → X` com `X` finito, e nada mais.

Em particular, **"bacia de atração" aqui não tem conteúdo métrico nem
topológico**: é apenas o conjunto de estados cuja trajetória atinge um dado
ciclo.
