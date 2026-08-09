# Relatório de auditoria — HODGE-CDK-001

Autorização: `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09` (onda
`PARALLEL_AUDIT_WAVE_IN_PROGRESS`).

target_statement (herdado): "Formalizar exatamente o que o teorema de
Cattani-Deligne-Kaplan (variações de estrutura de Hodge, loci de
Hodge) prova, e o que ele explicitamente não prova sobre a conjectura
de Hodge geral."

Esta sessão tentou reconstruir, a partir de literatura que só pôde ler
em parte, um resultado sem acesso direto ao artigo original (PDF da
AMS/JAMS retornou HTTP 403). Por instrução explícita do documento de
revisão de portfólio, as duas seções abaixo são mantidas separadas e
não misturadas.

---

## Verificado

Nesta sessão, "verificado" significa: fonte primária foi buscada,
obtida (via WebFetch/WebSearch) e, nos casos em que o PDF pôde ser
baixado, o texto foi extraído diretamente do stream comprimido do PDF
(sem depender de resumo de modelo intermediário) e citado literalmente
abaixo. Onde apenas um resumo de busca esteve disponível, isso é
indicado explicitamente.

1. **Enunciado oficial da Conjectura de Hodge.** Extraído diretamente
   do PDF do Clay Mathematics Institute, "The Hodge Conjecture" por
   Pierre Deligne
   (<https://www.claymath.org/wp-content/uploads/2022/06/hodge.pdf>):

   > "Hodge Conjecture. On a projective non-singular algebraic variety
   > over C, any Hodge class is a rational linear combination of
   > classes cl(Z) of algebraic cycles."

2. **Transversalidade de Griffiths**, mesma fonte, citação literal:

   > "[the Hodge filtration] varies holomorphically with t, and obeys
   > Griffiths transversality: at first order around t0 ∈ T, F^p(t)
   > remains in F^{p−1}(t0)."

   É uma condição infinitesimal sobre como a filtração de Hodge se
   move em família — não, por si, um enunciado sobre "instabilidade de
   classes fantasma".

3. **Codimensão 1 é um teorema, não uma conjectura.** Deligne (mesma
   fonte, §2) esboça a prova via sequência exponencial
   `0 → Z → O → O* → 0` para classes de tipo `(1,1)`. Confirmado de
   forma cruzada por fonte terciária (Wikipedia/HandWiki, "Lefschetz
   theorem on (1,1)-classes"): "Any smooth, projective variety
   satisfies the Hodge conjecture in codimension one, known as the
   Lefschetz (1,1) theorem." — único caso da conjectura provado para
   toda variedade Kähler.

4. **Cattani–Deligne–Kaplan existe, com este título/veículo.**
   Confirmado por três listagens independentes (página oficial da
   AMS/JAMS, ResearchGate, SciRP), todas concordando: "On the Locus of
   Hodge Classes", Journal of the American Mathematical Society, vol.
   8, no. 2, 1995, autores Eduardo Cattani, Pierre Deligne, Aroldo
   Kaplan. O PDF oficial da AMS não pôde ser lido diretamente (HTTP
   403 nesta sessão).

5. **Enunciado exato do teorema CDK**, citado quase literalmente como
   "Theorem 2.8 (Deligne-Cattani-Kaplan)" nas notas de aula de
   François Charles, "Hodge Loci and Absolute Hodge Classes" (30 de
   junho de 2010), texto extraído diretamente do PDF nesta sessão
   (<https://www2.math.upenn.edu/~siegelch/Notes/Charles.pdf>):

   > "Let π : X→S as before. Then the locus of Hodge classes in
   > H^{2i}(X/S) is a countable union of algebraic subvarieties."

   Imediatamente seguido, na mesma fonte, pela delimitação exata do
   que não foi provado:

   > "We don't get information on the field of definition."

6. **Definição do locus de Hodge**, mesma fonte, Definição 2.5, citação
   literal:

   > "The locus of Hodge classes for π is the set of α_t ∈
   > H^{2i}_dR(X_t/C) such that α_t is a Hodge class."

7. **CDK usado como ferramenta de redução, não como prova.** Mesma
   fonte, Teorema 2.9: mostra que CDK ("DCK"), combinado com o Teorema
   do Ciclo Invariante Global, permite *reduzir* a Conjectura de Hodge
   para uma classe específica à Conjectura de Hodge sobre um corpo de
   números — não a prova.

8. **Deligne já registrava, no documento oficial do Clay, que a
   algebricidade do locus é conhecida (citando CDK) e que o corpo de
   definição é o que permanece em aberto.** **Correção** (revisão
   adversarial de 2026-08-09): a citação abaixo, na versão original
   desta seção, fundia duas cláusulas distintas numa só, perdendo o
   qualificador `(known: see [4])`. Re-extraída diretamente do PDF:

   > "The Hodge conjecture implies that the locus where this happens
   > is a denumerable union of algebraic subvarieties of S
   > **(known: see [4])**, and is defined over Q̄ **(unknown)**."

   A referência `[4]` na bibliografia do próprio documento do Clay é
   Deligne–Cattani–Kaplan, JAMS 8 (1995), 483–505 — Deligne cita CDK
   como a fonte do "known". Isso é mais preciso do que — e reforça, em
   vez de enfraquecer — a leitura desta frente: CDK estabelece a
   algebricidade (creditada por Deligne), e o corpo de definição é o
   gap que permanece aberto (`HODGE-GAP-004`).

9. **Decomposição de Deligne da Conjectura de Hodge em duas
   sub-conjecturas** ("classes de Hodge são absolutas" +
   "classes de Hodge absolutas são algébricas"), e o teorema de
   Deligne de que classes de Hodge em variedades abelianas são
   absolutas. Mesma fonte (Charles 2010), Definições 1.4/1.5, Teorema
   1.8.

10. **Griffiths, "Periods of integrals on algebraic manifolds, I."**
    Título, veículo (American Journal of Mathematics), volume 90,
    páginas 568–626, ano 1968 — confirmados por duas listagens
    independentes (página de publicações do IAS, registro no JSTOR).
    Conteúdo detalhado do artigo não lido diretamente nesta sessão.

11. **Locus de Noether–Lefschetz — definição e cota de codimensão
    `≥ d-3`** para superfícies de grau `d ≥ 4` em `P^3`, confirmada por
    múltiplas fontes secundárias convergentes (resumos de busca sobre
    arXiv:1404.5717 e correlatos), embora a atribuição exata (autor/ano
    do resultado de cota) não tenha sido confirmada contra fonte
    primária.

O caso especial auditado passo a passo a partir destes fatos está em
`../RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`.

---

## Aproximado

Itens abaixo vêm do documento legado `ANALISE_CRITICA_HODGE.md`, de
resumos gerados por busca (sem leitura direta do PDF primário), ou de
memória de treino — **não** checados contra fonte primária nesta
sessão.

1. Página exata do artigo CDK 1995 (483–506) — vista em resumo de
   busca (SciRP/ResearchGate), não confirmada por leitura direta do
   PDF da AMS (bloqueado por HTTP 403 nesta sessão).

2. Atribuição do método de prova de CDK a "métodos transcendentais" e
   caracterização de que "não constrói ciclos" — plausível e
   consistente com o que foi lido (Teorema 2.8 fala só do locus,
   Teorema 2.9 usa CDK como ferramenta de redução), mas a descrição
   detalhada da técnica de prova do artigo original de 1995 não foi
   lida.

3. Refinamento de Bakker–Klingler–Tsimerman sobre geometria
   tame/o-minimal e corpo de definição do locus de Hodge — encontrado
   em resultado de busca ("Tame topology of arithmetic quotients and
   algebraicity of Hodge loci"), não lido em profundidade. Citado aqui
   apenas para não ser confundido com CDK 1995 — é um resultado
   posterior e distinto.

4. Atribuição exata (autores, ano) da cota de codimensão `d-3` do
   locus de Noether–Lefschetz — um resumo de busca mencionou "Voisin,
   Green and others" sem confirmação primária.

5. Data "1924" e método de prova original ("normal functions") do
   teorema de Lefschetz (1,1) — de fonte terciária (Wikipedia/
   HandWiki), não confirmado contra texto primário de Lefschetz.

6. Todo o conteúdo do documento legado `ANALISE_CRITICA_HODGE.md`
   sobre "Period Rigidity" / conjectura de períodos de Grothendieck —
   mantido como estava, não investigado nesta sessão além do que já
   constava no scaffold anterior.

7. A caracterização do documento legado de que a transversalidade de
   Griffiths mostra que "classes fantasma se dissolvem sob deformação"
   — **não confirmada** e provavelmente imprecisa à luz do que foi
   verificado (item 2 da seção "Verificado" acima): o enunciado
   localizado da transversalidade é puramente sobre a filtração, não
   sobre estabilidade de classes específicas. Ver `HODGE-GAP-004`.

8. As percentagens de "status real" (~85-90%) e "pronto para Clay: 85%"
   do documento legado — não são reproduzidas nem endossadas por esta
   auditoria; ver crítica em `ASSUMPTIONS.md`.

---

## Aplicação do stop_condition

`stop_condition`: "tratar transversalidade de um loci como
sobrejetividade sobre as classes de Hodge."

Esta sessão chegou a esse limite de forma controlada, no caso auditado
em `../RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md` (Passo 4–5): a
extensão natural do argumento — de codimensão 1 (onde a conclusão
"existe ciclo" é verdadeira, mas por Lefschetz (1,1), não por CDK) para
codimensão `≥ 2` (onde nenhuma fonte consultada fornece um análogo) —
é exatamente a inferência proibida. A sessão **parou nesse ponto e não
tentou produzir, sugerir, ou aproximar** um argumento para codimensão
`≥ 2`. Isso é reportado como `stop_condition_triggered: true` no
retorno estruturado — não como uma violação desta auditoria, mas como
a fronteira correta que a auditoria foi desenhada para localizar e
respeitar.

## O que esta auditoria não afirma

Consistente com `PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md` e
`AGENTS.md`: esta frente não declara a Conjectura de Hodge resolvida,
aproximada, ou "alcançável"; não afirma novidade matemática; e a
auditoria de literatura feita aqui não equivale a um resultado formal
(`F ≠ T`, nenhum enunciado deste documento foi verificado em Lean —
apenas o contraexemplo lógico abstrato em
`../FORMAL/hodge_locus_fallacy_sketch.lean`, que não formaliza nenhum
enunciado de Hodge/CDK/Lefschetz).
