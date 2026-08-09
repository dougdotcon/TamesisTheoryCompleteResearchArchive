# Matriz de resultados conhecidos

status: `AUDITED` — cada linha marcada `verificado` tem citação
recuperável nesta sessão via WebSearch (ver `REVIEWS/AUDIT_REPORT.md`
para os detalhes e ressalvas de cada uma); linhas `aproximado` vêm do
documento legado ou de memória de treino, sem fonte primária conferida
agora.

| # | Resultado | Autores/ano | Onde publicado | O que prova exatamente | Fonte nesta sessão |
|---|---|---|---|---|---|
| 1 | Existência global de solução fraca | Leray, 1934 | *Acta Math.* 63 | Existência global de solução fraca em `L²` a partir de qualquer `u₀ ∈ L²`; não dá unicidade nem suavidade | aproximado (clássico, não re-verificado por WebSearch nesta sessão) |
| 2 | Regularidade parcial (dimensão do conjunto singular) | Caffarelli, Kohn, Nirenberg, 1982 | *Comm. Pure Appl. Math.* 35, 771–831 | Para soluções fracas adequadas, o conjunto singular espaço-tempo tem medida de Hausdorff parabólica 1-dimensional nula (≤1) | **verificado** (WebSearch, citação recuperada) |
| 3 | Critério de blow-up via vorticidade `L∞` (BKM) | Beale, Kato, Majda, 1984 | *Comm. Math. Phys.* 94 | `T*` é tempo de blow-up ⟺ `∫₀^{T*}‖ω‖_∞ dt = ∞` (originalmente para Euler; usado também como critério para Navier–Stokes) | **verificado** (WebSearch, citação recuperada) |
| 4 | Direção da vorticidade Lipschitz ⟹ regularidade | Constantin, Fefferman, 1993 | *Indiana Univ. Math. J.* 42, 775–789 | Se a direção `ω/\|ω\|` é Lipschitz-contínua em espaço (uniformemente no tempo) nas regiões de vorticidade intensa, a solução é regular | **verificado** (WebSearch, citação e enunciado recuperados) |
| 5 | Rigidez de soluções autossimilares de Leray | Nečas, Růžička, Šverák, 1996 | *Acta Math.* 176, 283–294 | Soluções autossimilares de Leray (blow-up autossimilar no sentido restrito) precisam ser identicamente nulas | **verificado** (WebSearch, citação recuperada) — atenção: exclui só a classe autossimilar, não "blow-up Tipo I" em geral (ver ressalva abaixo) |
| 6 | Cota inferior de pressão / blow-up Tipo I | Seregin, Šverák, 2002 / 2009 | *Arch. Ration. Mech. Anal.* (2002); *Comm. PDE* (axissimétrico, 2009) | Exclui blow-up Tipo I sob hipóteses adicionais (cota de pressão / axissimetria) — **não** é exclusão incondicional de Tipo I geral | **verificado parcialmente** (WebSearch confirma existência e tema dos papers; enunciado exato de cada versão não foi recuperado com precisão total nesta sessão) |
| 7 | Alinhamento vorticidade–deformação em DNS | Ashurst, Kerstein, Kerr, Gibson, 1987 | *Phys. Fluids* 30, 2343 | Em DNS (grade 128³, escoamento isotrópico e cisalhamento homogêneo), vorticidade se alinha preferencialmente com o autovetor **intermediário** da deformação, não com o mais extensional; atribuído a conservação de momento angular via modelo de Euler restrita | **verificado** (WebSearch, citação e achado recuperados) |
| 8 | Equação de Euler restrita, blow-up em tempo finito | Vieillefosse, 1982 | (citado via literatura secundária nesta sessão) | Truncar o Hessiano de pressão pela parte isotrópica leva a blow-up em tempo finito para quase toda condição inicial ("Vieillefosse tail") | **aproximado** (citação recuperada via literatura secundária que a cita; artigo original de 1982 não foi acessado diretamente nesta sessão) — **reproduzido e verificado por computação própria** nesta sessão, ver `COMPUTATION/restricted_euler.py` |
| 9 | Solução exata da Euler restrita | Cantwell, 1992 | *Phys. Fluids A* 4, 782–792 | Forma fechada (funções elípticas de Jacobi) da dinâmica de Vieillefosse; geometria assintótica do gradiente de velocidade quase independente da condição inicial | **verificado** (WebSearch, citação e conteúdo recuperados) |
| 10 | Fechamento (closure) do Hessiano de pressão anisotrópico — "Recent Fluid Deformation" | Chevillard, Meneveau, 2006 | *Phys. Rev. Lett.* 97 (RFD original); ver também Chevillard, Meneveau, Biferale, Toschi, *Phys. Fluids* 20, 101504, 2008 | Modelo estocástico de fechamento para o Hessiano de pressão e o laplaciano viscoso ao longo de trajetórias lagrangianas; reproduz várias estatísticas geométricas de DNS, mas **admite explicitamente** que certas propriedades em regiões dominadas por rotação não são bem reproduzidas | **verificado** (WebSearch, citação e ressalva recuperadas) |
| 11 | Critério de regularidade via autovalor intermediário da deformação | Evan Miller, 2020 | *Arch. Ration. Mech. Anal.* 235 | Deriva identidade de crescimento de enstrofia dependente só da história do autovalor intermediário da deformação (sem interação não-local explícita com vorticidade); condições necessárias e suficientes de blow-up críticas em escala | **verificado** (WebSearch, citação e achado recuperados) — relevante porque é uma via **alternativa**, já publicada e passando por revisão por pares, ao mesmo tipo de pergunta que a hipótese Tamesis tenta responder por outro caminho |
| 12 | Cadeia "pressão–alinhamento ⟹ regularidade" (Passos 1–6, Lemma 3.1, Theorem 3.2) | Sistema Tamesis / documento legado interno | `ANALISE_CRITICA_NS.md`, 2026-02-05 (não é publicação externa, não é peer-reviewed) | Estrutura de 6 passos citada no documento legado, com Lemma 3.1 e Theorem 3.2 explicitamente marcados `🔴 NÃO PROVADO` no próprio documento | **não é uma referência externa** — é o objeto sob auditoria, não uma fonte de apoio. Citado aqui só para registro, não como resultado estabelecido |

## Ressalva geral sobre a linha 6

O documento legado (`ANALISE_CRITICA_NS.md`) lista "Seregin-Šverák:
Type I blow-up excluído" na coluna de "resultados clássicos usados
(100% rigorosos)" sem qualificação. A auditoria desta sessão não pôde
confirmar que a exclusão de blow-up Tipo I é incondicional em geral
(fora de axissimetria ou hipóteses adicionais de pressão) — ver
`REVIEWS/AUDIT_REPORT.md`, seção "Aproximado". Recomenda-se tratar essa
linha como aproximada até que uma sessão futura confirme o enunciado
exato.
