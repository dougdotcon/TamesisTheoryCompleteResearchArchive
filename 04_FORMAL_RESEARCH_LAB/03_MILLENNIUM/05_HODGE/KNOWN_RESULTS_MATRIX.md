# Matriz de resultados conhecidos — HODGE-CDK-001

`[V]` = verificado nesta sessão contra fonte primária ou cruzada por
múltiplas fontes independentes. `[A]` = aproximado (documento legado
`ANALISE_CRITICA_HODGE.md` e/ou memória de treino, não checado contra
fonte primária nesta sessão).

| Item | O que prova | Estado da conjectura geral | Rótulo | Fonte |
|---|---|---|---|---|
| Lefschetz (1,1) | Toda classe `(1,1)` inteira em variedade Kähler compacta é `c_1` de fibrado em retas → em variedade projetiva, classe de divisor. | **Teorema**, não conjectura. Único caso da Conjectura de Hodge provado para toda variedade Kähler (não só projetiva). | `[V]` | Deligne, "The Hodge Conjecture" (Clay), §2, obs. (iii); Wikipedia/HandWiki "Lefschetz theorem on (1,1)-classes" (data 1924 `[A]`). |
| Cattani–Deligne–Kaplan (CDK/DCK), 1995 | Locus de Hodge de uma VHS polarizável sobre base quase-projetiva lisa é união contável de subvariedades **algébricas** (sobre `C`) — sem assumir a Conjectura de Hodge. | Não prova nem se aproxima da Conjectura de Hodge; é um resultado **sobre o espaço de parâmetros**, não sobre existência de ciclo numa fibra fixa. Não dá informação sobre corpo de definição. | `[V]` (enunciado, Teorema 2.8 nas notas de Charles); `[A]` (páginas exatas 483–506, não lidas na fonte primária, PDF da AMS retornou HTTP 403 nesta sessão) | Cattani–Deligne–Kaplan, JAMS 8(2), 1995; F. Charles, "Hodge Loci and Absolute Hodge Classes" (2010). |
| Griffiths, "Periods of integrals..." (1968) | Introduz o mapa de períodos e a transversalidade de Griffiths: condição infinitesimal `F^p(t) ⊂ F^{p-1}(t_0)` sobre como a filtração de Hodge varia em família. | Não é, por si, um resultado sobre existência de ciclos algébricos; é a estrutura diferencial que sustenta a definição de VHS usada depois por CDK. | `[V]` (enunciado da transversalidade, via Deligne/Clay); `[A]` (atribuição exata de "instabilidade de classes fantasma" ao artigo de 1968 — não confirmada). | Griffiths, AJM 90 (1968), 568–626; Deligne, "The Hodge Conjecture" (Clay), §1. |
| Locus de Noether–Lefschetz `NL_d` | Caso particular do locus de Hodge (codimensão de ciclo `p=1`) para superfícies de grau `d ≥ 4` em `P^3`. Componentes têm codimensão `≥ d-3` no espaço de parâmetros. | Conjectura de Hodge NESTE caso (`p=1`) é teorema via Lefschetz (1,1) — não depende de CDK para a parte "existência de ciclo". CDK garante, adicionalmente, que o locus onde a classe extra aparece é algébrico. | `[V]` (definição, cota de codimensão via múltiplas fontes secundárias); `[A]` (atribuição exata autor/ano da cota `d-3`). | Ver `RESULTS/WORKED_CASE_NOETHER_LEFSCHETZ.md`. |
| Classes de Hodge absolutas (Deligne) | Decompõe a Conjectura de Hodge em duas: (1) classes de Hodge são absolutas (i.e. estáveis sob `Aut(C)`), (2) classes de Hodge absolutas são algébricas. Deligne prova (1) para variedades abelianas. | Ambas as sub-conjecturas seguem em geral abertas; CDK é usado (com o Teorema do Ciclo Invariante Global) como ferramenta de **redução** entre fibras de uma família, não como prova. | `[V]` | F. Charles, "Hodge Loci and Absolute Hodge Classes" (2010), Teoremas 1.8, 2.2, 2.8, 2.9. |
| Períodos / rigidez de período (Grothendieck) | Framework conjectural (Period Conjecture) sobre origem geométrica de relações racionais entre períodos. | Aberta. Não é usada nesta sessão para nenhuma inferência — citada apenas porque aparece no documento legado. | `[A]` — não investigada com fonte primária nesta sessão; mantida como aberta conforme já registrado no scaffold anterior. | `ANALISE_CRITICA_HODGE.md` (legado, não fonte final). |
| Hodge geral (codimensão `p ≥ 2` arbitrária) | — | **Aberta.** Nenhum resultado desta matriz fecha ou aproxima este caso. | `[V]` (é consenso da literatura consultada: nenhuma fonte lida nesta sessão afirma o contrário) | Todas as fontes acima, por omissão. |

## Leitura da matriz

A única linha desta matriz em que "Conjectura de Hodge" é um teorema
comprovado é a de **Lefschetz (1,1)** (codimensão 1). CDK entra nessa
linha apenas como resultado auxiliar sobre o locus, não como a razão
pela qual a conjectura vale ali. Para codimensão `p ≥ 2`, não há linha
nesta matriz — nem no documento legado, nem na literatura consultada
nesta sessão — que forneça um análogo de Lefschetz (1,1). Essa lacuna é
exatamente `HODGE-GAP-001` em `GAP_REGISTER.yaml`.
