# Caso especial verificável, auditado passo a passo — Noether–Lefschetz em `P^3`

Produto esperado da tarefa HODGE-CDK-001: "um caso especial verificável
(baixa dimensão/codimensão) onde a inferência é auditada passo a
passo". Este documento é esse produto.

Rótulos: `[V]` verificado nesta sessão contra fonte primária/fontes
cruzadas independentes; `[A]` aproximado.

## Configuração `[V]`

Seja `S_d` o espaço (aberto de Zariski de um espaço projetivo) que
parametriza superfícies suaves de grau `d` em `P^3_C`, e
`π : X → S_d` a família universal correspondente, `d ≥ 4`. Para cada
`t ∈ S_d`, seja `H^2_prim(X_t, Z)` a cohomologia primitiva (ortogonal à
classe de seção hiperplana `h`), com sua estrutura de Hodge de peso 2
induzida. Isto é um caso particular da configuração de `DEFINITIONS.md`
("VHS e transversalidade de Griffiths"): `π` é suave e projetiva, `S_d`
é quase-projetiva lisa e conexa.

## Passo 1 — Definição do locus auditado `[V]`

Fixe uma classe primitiva `ξ_0 ∈ H^2_prim(X_{t_0}, Z)` de tipo `(1,1)`
para algum `t_0` (i.e. Picard rank `> 1` em `t_0`). Por transporte
paralelo local (Gauss–Manin), `ξ_0` se estende a uma seção local `ξ_t`
do sistema local `R^2π_*Z` numa vizinhança de `t_0`. O **locus de
Noether–Lefschetz** associado, `NL_d(ξ_0) ⊂ S_d`, é o conjunto dos `t`
onde `ξ_t` permanece de tipo `(1,1)` — exatamente a instância da
Definição 2.5 citada em `DEFINITIONS.md`, com `i = 1`.

## Passo 2 — O que CDK garante aqui, e só aqui `[V]`

Pelo Teorema 2.8 (CDK/DCK, citado em `DEFINITIONS.md`), `NL_d(ξ_0)` —
e, tomando a união sobre todas as classes primitivas possíveis, o locus
completo `NL_d` — é uma **união contável de subvariedades algébricas**
de `S_d`. Este é um enunciado sobre o **espaço de parâmetros** `S_d`:
ele diz onde (para quais superfícies `X_t`) uma classe extra de tipo
`(1,1)` aparece. Ele não diz, e não foi desenhado para dizer, se essa
classe `ξ_t`, uma vez que existe, é a classe de uma curva algébrica em
`X_t`.

Cota adicional (independente de CDK, geralmente obtida por cálculo
explícito com o anel Jacobiano — não conferida contra fonte primária
nesta sessão, `[A]` quanto à atribuição exata): toda componente de
`NL_d` tem codimensão `≥ d − 3` em `S_d`, com igualdade para as
componentes formadas por superfícies contendo uma reta.

## Passo 3 — O que garante a existência do ciclo aqui, e é INDEPENDENTE de CDK `[V]`

Para **todo** `t ∈ S_d` (não apenas os que estão em `NL_d`) e **toda**
classe `ζ ∈ H^2(X_t, Z) ∩ H^{1,1}(X_t)`, o **teorema de Lefschetz sobre
classes `(1,1)`** (ver `DEFINITIONS.md`, `KNOWN_RESULTS_MATRIX.md`)
garante `ζ = c_1(L)` para algum fibrado em retas `L`; como `X_t` é
projetiva, isso é a classe de um divisor efetivo (diferença de
divisores) — i.e. `ζ` **é** algébrica. Esta prova usa a sequência
exponencial `0 → Z → O → O* → 0` e não usa, em nenhum passo, o Teorema
2.8 de CDK. É um teorema anterior, mais elementar, e vale para toda
variedade Kähler compacta, não só para membros de uma família algébrica
com locus de Hodge algébrico.

## Passo 4 — A inferência que este trabalho audita, e por que ela falha em geral `[V]`+`[A]` (a falha é lógica, verificável sem depender de nenhuma citação adicional)

Um argumento ilegítimo do tipo proibido pelo `stop_condition` desta
frente teria a forma:

> "Passo 2 mostra que `NL_d` (o locus) é algébrico. Logo, para todo
> `t ∈ NL_d`, a classe extra `ξ_t` é a classe de uma curva algébrica em
> `X_t`."

A conclusão desta frase **é verdadeira** neste caso — mas **não por
causa do Passo 2**. Ela é verdadeira por causa do Passo 3 (Lefschetz
(1,1)), que é logicamente independente do Passo 2: o Passo 3 vale para
toda superfície `X_t`, esteja `t` em `NL_d` ou não, e não faz nenhuma
referência à geometria do locus `NL_d` em `S_d`. Se alguém removesse o
Passo 3 da matemática conhecida e tentasse derivar sua conclusão só do
Passo 2 (algebricidade do locus / transversalidade de Griffiths), não
haveria como fechar o argumento — "o conjunto de parâmetros onde uma
propriedade se mantém é algébrico" não implica logicamente "a
propriedade, quando se mantém, vem de um objeto geométrico explícito".
Um locus algébrico pode perfeitamente ser vazio, ou não vazio sem que
nada na prova de sua algebricidade exiba um representante.

## Passo 5 — Onde a auditoria para (stop_condition) `[V]`

Codimensão `p = 1` é o único caso, entre os listados em
`KNOWN_RESULTS_MATRIX.md`, em que existe um teorema tipo-Lefschetz
independente que fecha o Passo 3. Para `p ≥ 2` (por exemplo, classes de
Hodge em `H^4` de uma variedade de dimensão `≥ 4`, como no "Example 1"
de Deligne sobre componentes de Künneth da diagonal, citado em
`DEFINITIONS.md`/fonte Clay), nenhuma fonte consultada nesta sessão
fornece um análogo do Passo 3. Repetir o Passo 4 nesse regime — tratar
a algebricidade do locus (obtida por CDK, ou por transversalidade de
Griffiths) como se implicasse sobrejetividade do mapa de ciclos sobre
as classes de Hodge — é exatamente a inferência que o `stop_condition`
desta frente proíbe. Esta sessão identifica esse ponto e **para aqui**:
não tenta produzir, nem sugerir, um argumento análogo ao Passo 3 para
`p ≥ 2`. Isso permaneceria um problema aberto (a própria Conjectura de
Hodge geral), e nenhuma parte deste documento afirma o contrário.

## Resumo da auditoria

| Passo | Afirmação | Depende de CDK? | Status |
|---|---|---|---|
| 2 | `NL_d` é união contável de subvariedades algébricas de `S_d` | Sim (Teorema 2.8) | `[V]` |
| 3 | Toda classe `(1,1)` em `X_t` é classe de divisor | Não — Lefschetz (1,1), independente | `[V]` |
| 4→5 | Generalizar "locus algébrico ⇒ existe ciclo" para `p ≥ 2` | Seria a inferência proibida | **Não tentado — stop_condition** |
