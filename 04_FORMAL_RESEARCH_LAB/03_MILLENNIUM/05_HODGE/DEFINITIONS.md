# Definições — HODGE-CDK-001

Estado: `PARTIAL` (definições em linguagem matemática padrão, citadas;
nenhuma formalizada em Lean nesta rodada — ver `FORMAL/` e
`PROOF_SKETCH.md` para o motivo).

Convenção de rotulagem usada neste documento e em `REVIEWS/AUDIT_REPORT.md`:

- `[V]` = verificado nesta sessão (fonte primária lida e citada abaixo).
- `[A]` = aproximado (documento legado do laboratório e/ou memória de
  treino, sem checagem de fonte primária nesta sessão).

## Enunciado clássico da Conjectura de Hodge `[V]`

Citação direta, extraída do PDF oficial do Clay Mathematics Institute,
"The Hodge Conjecture", por Pierre Deligne
(<https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf>, lido e
extraído nesta sessão):

> "Hodge Conjecture. On a projective non-singular algebraic variety over
> C, any Hodge class is a rational linear combination of classes cl(Z)
> of algebraic cycles."

Este é o enunciado clássico e deve permanecer ao lado de qualquer
linguagem própria do laboratório usada abaixo (proibição de
`AGENTS.md`).

## Classe de Hodge `[V]`

Para `X` projetiva não singular sobre `C`, de dimensão complexa `N`, com
decomposição de Hodge `H^n(X,C) = ⊕_{p+q=n} H^{p,q}`, uma classe
`c ∈ H^{2p}(X,Z)` é dita **classe de Hodge** se sua imagem em
`H^{2p}(X,C)` está em `H^{p,p}`, i.e. tem tipo `(p,p)`.
Fonte: Deligne, "The Hodge Conjecture" (Clay), seção 1.

## Mapa de classe de ciclo `cl(Z)` `[V]`

Se `Z` é um subespaço analítico fechado de `X` de codimensão complexa
`p`, `Z` define uma classe `cl(Z) ∈ H^{2p}(X,Z)`, de tipo `(p,p)`, via
dualidade de Poincaré (a corrente de integração sobre `Z` é uma forma
fechada de tipo `(p,p)` com coeficientes distribucionais que representa
a imagem de `cl(Z)` em `H^{2p}(X,C)`). Por Chow, em variedade projetiva,
ciclo algébrico = subespaço analítico fechado.
Fonte: Deligne, "The Hodge Conjecture" (Clay), seção 1 e observação (i).

## Variação de estrutura de Hodge (VHS) e transversalidade de Griffiths `[V]`

Quando `X` varia em família holomorfa parametrizada por `T`, a filtração
de Hodge `F^p(t) ⊂ H^n(X_t, C)` varia holomorficamente com `t` e obedece
à **transversalidade de Griffiths**: a primeira ordem, ao redor de
`t_0 ∈ T`,

> `F^p(t)` permanece em `F^{p-1}(t_0)`.

Citação direta (mesma fonte, seção 1, parafraseando a notação):
"[the Hodge filtration] varies holomorphically with t, and obeys
Griffiths transversality: at first order around t0 ∈ T, F^p(t) remains
in F^{p−1}(t0)."

Isto é uma condição diferencial (infinitesimal) sobre como a filtração
se move — **não** é, por si, um enunciado sobre estabilidade ou
instabilidade de classes "fantasma" sob deformação (ver nota crítica em
`ASSUMPTIONS.md` sobre a linguagem do documento legado).

Referência primária clássica (não lida diretamente nesta sessão, apenas
citação bibliográfica cruzada — `[A]` quanto aos detalhes de conteúdo,
`[V]` quanto a título/veículo/páginas, confirmados por duas listagens
independentes — IAS Publications e JSTOR):
Phillip Griffiths, "Periods of Integrals on Algebraic Manifolds, I.
Construction and Properties of the Modular Varieties", American Journal
of Mathematics, vol. 90 (1968), pp. 568–626.

## Locus de Hodge (Hodge locus) `[V]`

Para `π : X → S` família suave e projetiva com `S` variedade quase
projetiva lisa e conexa sobre `C`, e `α` seção global de
`R^{2i}π_* Q(i)` que é de tipo `(i,i)` em algum ponto, o **locus de
Hodge** de `π` (relativo a `α`) é o conjunto de pontos `t ∈ S(C)` onde
`α_t` é uma classe de Hodge.

Citação direta (Definição 2.5, François Charles, notas de aula "Hodge
Loci and Absolute Hodge Classes", 30/06/2010,
<https://www2.math.upenn.edu/~siegelch/Notes/Charles.pdf>, lido e
extraído nesta sessão):

> "Definition 2.5 (Hodge Locus). The locus of Hodge classes for π is the
> set of α_t ∈ H^{2i}_dR(X_t/C) such that α_t is a Hodge class."

Este é um objeto que vive no **espaço de parâmetros** `S` da família —
não é, em si, um enunciado sobre um único `X_t` fixo.

## Teorema de Cattani–Deligne–Kaplan (CDK / "DCK") `[V]`

Referência bibliográfica (título, veículo, volume, ano confirmados por
múltiplas listagens independentes — página oficial da AMS/JAMS,
ResearchGate, SciRP; a leitura direta do PDF da AMS falhou nesta sessão,
HTTP 403 — ver `unverified_claims` no relatório de retorno quanto ao
intervalo exato de páginas):

> Eduardo Cattani, Pierre Deligne, Aroldo Kaplan, "On the Locus of Hodge
> Classes", Journal of the American Mathematical Society, vol. 8, no. 2
> (1995).

Enunciado do teorema (citado como Teorema 2.8 nas notas de Charles,
rotulado ali "Deligne-Cattani-Kaplan"; conteúdo confirmado de forma
independente por buscas na literatura secundária — Klingler,
"Hodge loci and atypical intersections: conjectures", e survey "Known
cases of the Hodge conjecture"):

> "Theorem 2.8 (Deligne-Cattani-Kaplan). Let π : X → S as before. Then
> the locus of Hodge classes in H^{2i}(X/S) is a countable union of
> algebraic subvarieties."

Imediatamente após o enunciado, a mesma fonte registra o limite exato do
que foi provado:

> "We don't get information on the field of definition."

Esta frase é o núcleo do gap de arithmetic descent registrado em
`GAP_REGISTER.yaml` (`HODGE-GAP-004`), e ecoa uma observação do próprio
Deligne no documento oficial do Clay: ao introduzir o locus de Hodge
como consequência da conjectura, ele anota explicitamente `(unknown)`
ao lado da afirmação de que esse locus seria uma união denumerável de
subvariedades algébricas de `S_{Q̄}` — i.e., mesmo a versão "sobre
`Q̄`" (não apenas sobre `C`) da algebricidade do locus era, na descrição
de Deligne, um ponto em aberto que CDK endereça apenas parcialmente
(algebricidade sobre `C`, sem controle do corpo de definição).

**Nota de precisão histórica** `[A]`: um refinamento posterior e
distinto — usando geometria tame/o-minimal para obter informação sobre
o corpo de definição — aparece no artigo "Tame topology of arithmetic
quotients and algebraicity of Hodge loci" (Bakker–Klingler–Tsimerman,
encontrado na busca desta sessão, não lido em profundidade). Este é um
resultado **posterior e distinto** de CDK 1995; não deve ser atribuído a
Cattani–Deligne–Kaplan. Mantido aqui apenas como apontador não
verificado, para não ser confundido com CDK 1995 em trabalho futuro.

## Teorema de Lefschetz sobre classes (1,1) `[V]`

Caso codimensão 1 da Conjectura de Hodge — um **teorema**, não uma
conjectura, válido para qualquer variedade Kähler compacta (não apenas
projetiva). Demonstração via a sequência exponencial
`0 → Z → O → O* → 0` (esboçada por Deligne no documento do Clay, seção 2,
observação (iii) e o parágrafo "Hodge conjecture for H^2").
Fonte cruzada: artigo da Wikipedia/HandWiki "Lefschetz theorem on
(1,1)-classes" (consultado nesta sessão; atribuição a Lefschetz e o ano
1924 vêm dessa fonte terciária, não confirmados aqui contra um texto
primário — rotulado `[A]` quanto à data exata).

> "Any smooth, projective variety satisfies the Hodge conjecture in
> codimension one, known as the Lefschetz (1,1) theorem."

## Locus de Noether–Lefschetz `[V]` (caso particular do locus de Hodge)

Para superfícies suaves de grau `d` em `P^3`, `NL_d` é o locus, no
espaço de parâmetros das superfícies de grau `d`, onde o número de
Picard é `> 1` (i.e. onde existe uma classe `(1,1)` primitiva extra além
da seção hiperplana). É historicamente o primeiro exemplo estudado de
locus de Hodge, e um caso particular — codimensão de ciclo `p = 1` — em
que a Conjectura de Hodge já é um teorema (Lefschetz (1,1), acima),
independentemente de CDK. Ver `RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`
para a auditoria passo a passo.

Cota de codimensão (confirmada por múltiplas fontes secundárias
convergentes nesta sessão — resumos de busca sobre arXiv:1404.5717 e
correlatos): toda componente do locus de superfícies de grau `d` em
`P^3` com número de Picard `≠ 1` tem codimensão `≥ d − 3`, com igualdade
para as componentes de superfícies contendo uma reta. Atribuição
precisa (autores/ano exatos do resultado de cota) **não** confirmada
contra fonte primária nesta sessão — rotulada `[A]`.
