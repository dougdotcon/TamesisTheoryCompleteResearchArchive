# Hipóteses e distinções auditadas — HODGE-CDK-001

Estado: `AUDITED` quanto à distinção central; `NOT_AUDITED` quanto ao
restante da literatura de CDK (Voisin, período rígido, motivos
absolutos, etc. — fora do escopo desta rodada).

## A hipótese sob auditoria

> "Algebricidade do locus não é sobrejetividade do mapa de ciclos."

Esta frase (já presente no scaffold deste diretório antes desta sessão)
é **confirmada** pela leitura de fonte primária feita nesta sessão — não
é uma suposição do laboratório, é o que a literatura efetivamente diz.
Ver `DEFINITIONS.md` (Teorema 2.8/CDK) e
`RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`.

## Hipóteses do teorema CDK (o que ele exige para valer) `[V]`

Do enunciado citado em `DEFINITIONS.md` (Charles, Teorema 2.8, "as
before"), reconstruindo o contexto do parágrafo anterior nas mesmas
notas:

1. `π : X → S` morfismo suave e projetivo (Charles usa "smooth,
   projective" explicitamente no enunciado do "Principle B", Teorema
   2.2, imediatamente anterior).
2. `S` variedade quase projetiva, lisa, conexa, sobre `C`.
3. `α` seção global de `R^{2i}π_* Q(i)` (um sistema local racional de
   peso `2i`, subjacente a uma VHS polarizável — implícito pela
   construção via cohomologia de fibras de família algébrica).
4. Conclusão: o locus de Hodge de `α` (Definição 2.5) é união
   contável de subvariedades **algébricas** de `S` — algebricidade
   sobre `C`, sem informação sobre corpo de definição (citação exata em
   `DEFINITIONS.md`).

Não há, no enunciado citado, nenhuma hipótese ou conclusão sobre:

- existência de um ciclo algébrico realizando `α_t` para um `t`
  específico onde `α_t` é Hodge;
- sobrejetividade do mapa `cl` de ciclos algébricos sobre as classes de
  Hodge racionais de um `X_t` fixo.

## Distinção central que este trabalho audita `[V]`

| Afirmação | O que CDK prova | O que CDK NÃO prova |
|---|---|---|
| Sobre o **espaço de parâmetros** `S` | O conjunto de `t` onde `α_t` é Hodge é uma união contável de subvariedades algébricas de `S`. | Nada — CDK não fala do espaço de parâmetros exceto essa afirmação. |
| Sobre uma **fibra fixa** `X_t` | Nada diretamente. | Que toda classe de Hodge racional em `H^{2p}(X_t,Q)` seja `cl(Z)` para algum ciclo algébrico `Z ⊂ X_t` — isto é exatamente a Conjectura de Hodge, que continua aberta em geral. |
| Sobre o **corpo de definição** das componentes do locus | Nada — "we don't get information on the field of definition" (Charles, citação em `DEFINITIONS.md`). | Que as subvariedades algébricas do locus estejam definidas sobre `Q̄` (aspecto aritmético, distinto da algebricidade sobre `C`). |

## Onde a inferência ilegítima entraria (stop_condition, `AGENTS.md`)

A inferência proibida por esta frente — "tratar transversalidade de um
loci como sobrejetividade sobre as classes de Hodge" — teria a forma:

> "CDK prova que o locus de Hodge é algébrico (uma consequência da
> transversalidade de Griffiths sobre a filtração). Logo, para cada
> `t` no locus, a classe `α_t` correspondente é a classe de um ciclo
> algébrico."

Essa segunda frase **não segue** da primeira. `DEFINITIONS.md` documenta
por que: o locus de Hodge é um objeto sobre `S` (onde a propriedade
`(p,p)` é preservada), não um enunciado sobre existência de pré-imagem
sob o mapa de ciclos em nenhuma fibra individual.
`RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md` mostra, num caso onde a
conclusão da segunda frase é de fato verdadeira (codimensão 1), que ela
é verdadeira por um teorema **inteiramente diferente e independente**
(Lefschetz (1,1)) — não como consequência de CDK. Esta sessão parou
nesse ponto e não tentou generalizar o argumento para codimensão ≥ 2,
onde não há teorema análogo a Lefschetz (1,1) — fazer isso seria
exatamente cometer a inferência proibida. Ver `stop_condition_detail` no
retorno estruturado desta sessão.

## O que a nota crítica legada (`ANALISE_CRITICA_HODGE.md`) acerta e o que precisa de correção `[A]`/`[V]`

Acerta (compatível com a leitura de fonte primária feita aqui, `[V]`):

- que CDK prova algo **sobre** o locus, não uma prova da conjectura;
- que há um "gap de construção" entre eliminar contraexemplos e exibir
  um ciclo.

Precisa de correção ou é `[A]` não verificado:

- a linguagem "classes fantasma são instáveis sob deformação" para
  descrever transversalidade de Griffiths não corresponde ao enunciado
  que localizamos (uma condição infinitesimal sobre a filtração de
  Hodge, `F^p(t) ⊂ F^{p-1}(t_0)` — ver `DEFINITIONS.md`); pode ser uma
  paráfrase de argumentos de semicontinuidade usados em provas de
  densidade/Noether–Lefschetz (Green, Voisin), mas isso não foi
  confirmado nesta sessão e não deve ser atribuído a "Griffiths 1968"
  sem qualificação;
  a percentagem "~85-90% / pronto para Clay: 85%" no documento legado
  é rejeitada nesta sessão como formato de relato — não há métrica
  aceita no laboratório para "percentual de resolução" de um Problema
  do Milênio (`AGENTS.md`, proibição de declarar resolução ou
  proximidade), e o número não tem justificativa metodológica no
  próprio documento além de comparação impressionística com outras
  frentes.
