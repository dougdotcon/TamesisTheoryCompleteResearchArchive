---
document_id: FFG-COMPONENT-NOTIONS
status: BINDING
decision: EVENTUALLY_MEETS
---

# FOUND-FUNCTIONAL-GRAPH-001 — A escolha de "componente"

Documento vinculante. Esta é a decisão que a especificação existe para
travar, e é o motivo de a revisão da especificação vir **antes** da
formalização: uma definição errada de componente congelada em Lean
contaminaria todo o resto.

## As três candidatas

```yaml
- id: C1
  name: MutuallyReachable
  definition: "IterReachable f x y ∧ IterReachable f y x"
  status: REJEITADA

- id: C2
  name: EventuallyMeets
  definition: "∃ m n, f^[m] x = f^[n] y"
  status: ADOTADA

- id: C3
  name: "componente fracamente conexa do grafo dirigido subjacente"
  definition: "SimpleGraph.ConnectedComponent do grafo nao dirigido induzido"
  status: DIFERIDA
```

## Por que `MutuallyReachable` foi rejeitada

Contraexemplo obrigatório, que a formalização deverá verificar
(`FFG-CE-004`):

```text
a → c
b → c
c → c
```

Neste sistema:

```text
a e b pertencem ao mesmo componente funcional  (ambos caem em c)
a NAO alcanca b
b NAO alcanca a
a e b NAO sao mutuamente alcancaveis
```

`MutuallyReachable` colapsaria os "componentes" a: `{a}`, `{b}`, `{c}` —
três classes, quando geometricamente há **uma** estrutura: um ponto fixo
com dois ramos entrando nele.

Em grafo funcional finito, `MutuallyReachable` identifica exatamente os
estados **do mesmo ciclo**, mais cada estado consigo próprio. É uma
relação útil e será formalizada — mas ela descreve o **ciclo**, não o
componente.

## Por que `EventuallyMeets` foi adotada

O argumento é a própria determinismo da função:

```text
Numa funcao deterministica, depois que duas trajetorias atingem o MESMO
estado, suas continuacoes sao IDENTICAS.
```

Logo, "encontrar-se eventualmente" é a noção correta de "pertencer à mesma
estrutura dinâmica". O componente assim definido inclui:

```text
o ciclo;
a cauda de cada estado;
ramificacoes distintas que entram na mesma trajetoria;
toda a bacia funcional associada ao ciclo.
```

## Risco registrado: tautologia

Um perigo real desta escolha é que o teorema principal fique **verdadeiro
por definição**. Ele não fica, e a razão precisa estar escrita:

```text
EventuallyMeets diz que as trajetorias se ENCONTRAM.
Nao diz que o encontro ocorre num ponto PERIODICO,
nem que exista ponto periodico algum.
```

A existência do ponto periódico vem da **finitude**, via
`exists_eventual_period` (`FOUND-SEMIGROUP-002`), e a unicidade da órbita
vem de `periodicOrbit_apply_iterate_eq` (Mathlib). Nenhuma das duas é
consequência da definição de componente.

Verificação de que não é tautológico: `EventuallyMeets` é definível para
`X` **infinito**, e nesse caso o teorema principal é **falso** — considere
`f : ℕ → ℕ`, `f n = n + 1`. Ali `EventuallyMeets` é falsa para pares
distintos e não há ponto periódico algum. É a hipótese `Fintype X` que faz
o trabalho.

Registrado como `FFG-GAP-003` e como `STOP-009`.

## Por que a ponte com `SimpleGraph` fica diferida

`SimpleGraph` existe no checkout fixado
(`Combinatorics/SimpleGraph/Basic.lean:93`), com
`Reachable` (`Connectivity/Connected.lean:52`) e `ConnectedComponent`
(`:390`, definida como `Quot G.Reachable`).

Ela é **não dirigida**. Para usá-la seria preciso:

1. construir o grafo simples subjacente a `f` (aresta entre `x` e `f x`);
2. provar que `EventuallyMeets` implica `SimpleGraph.Reachable` nesse grafo;
3. provar a recíproca — que é o passo **não trivial**, pois um caminho não
   dirigido pode subir e descer ramos várias vezes.

O passo 3 é uma indução sobre `Walk` que não tem relação com o núcleo. Fica
`DEFERRED_TO_GRAPH_BRIDGE` (`FFG-GAP-012`).

**Consequência vinculante:** enquanto a ponte não existir, "componente"
nesta frente significa **classe de `EventuallyMeets`**, e nenhum texto pode
afirmar que coincide com componente conexa de grafo.

## Resumo vinculante

```text
COMPONENTE FUNCIONAL := classe de equivalencia de EventuallyMeets

NAO eh MutuallyReachable       (FFG-CE-004 refuta)
NAO eh, por ora, componente conexa de SimpleGraph  (ponte diferida)
```
