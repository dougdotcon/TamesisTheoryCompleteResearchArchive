# SEARCH_LOG — busca por mecanismo intrínseco natural com α ∈ (1/2, 1)

**Data:** 2026-08-22. Todas as buscas via `WebSearch`; verificação de
citações via `WebFetch`. Toda query é registrada, incluindo as que não
deram achado direto. Nenhuma citação é usada em `FINDINGS.md` sem ter
sido checada por fetch direto (ou, quando o fetch falhou por limitação
técnica de extração de PDF, isso é declarado explicitamente e a
afirmação correspondente é tratada como suporte, não como citação
primária verificada).

## Frente (a): existe um processo NOMEADO conhecido que É um mecanismo
tipo M-q com β∈(0,1), ou análogo direto do problema (fração cíclica de
permutação sob redirecionamento pontual, expoente de cauda de φ_∞(c))?

| # | Ferramenta | Query | Resultado (resumo) |
|---|---|---|---|
| 1 | WebSearch | `Pitman-Yor process number of tables power law exponent discount parameter` | Confirma: CRP de dois parâmetros (Pitman-Yor), discount d∈[0,1), número de mesas ocupadas cresce ~ N^d (tamanhos de mesa seguem lei de potência com expoente 1+d). Processo real, nomeado, bem estabelecido — mas é sobre CONTAGEM DE PARTIÇÕES/CLUSTERS, não sobre fração cíclica de um mapeamento f:[n]→[n]. Não é um mecanismo M-q. |
| 2 | WebSearch | `Weibull intensity nonhomogeneous Poisson process decreasing hazard rate infant mortality` | Confirma processo de Poisson não-homogêneo com intensidade Weibull, forma λ(x)=αβx^(β−1); β<1 dá taxa decrescente ("mortalidade infantil"), padrão em confiabilidade/sobrevivência. Usado na Seção 2 (derivação própria) — NÃO é por si só um mecanismo de permutação. |
| 3 | WebSearch | `renewal process regularly varying infinite mean renewal function power law growth theorem` | Confirma: gaps de renovação com cauda regularmente variável de índice α∈(0,1) (média infinita) dão função de renovação U(t) ~ crescimento em lei de potência de índice relacionado a α — teoria clássica (renewal theorem caso de média infinita). Não é um mecanismo de permutação; usado como pano de fundo teórico. |
| 4 | WebSearch | `Hawkes process power law kernel Omori law self-exciting aftershock decay exponent` | Confirma Hawkes/ETAS (Ogata 1988) com kernel em lei de potência reproduz Omori-Utsu μ(t)=K/(t+c)^p. Processo real, nomeado, expoente livre p. Não mapeia diretamente ao problema de permutação, mas é o precedente mais próximo para "taxa de evento com memória em lei de potência" — usado como inspiração/contexto na Seção 2. |
| 5 | WebSearch | `generalized Polya urn reinforcement function power exponent fractional limit theorem` | Confirma família de urnas de Pólya generalizadas com função de reforço f(n)~n^γ; γ<1 dá limites determinísticos, γ=1 clássico (Beta), γ>1 monopólio quase certo. Related, but não é diretamente um M-q. |
| 6 | WebSearch | `random permutation cycle structure perturbation power law tail exponent survival probability` | Nenhum acerto direto: resultados sobre estrutura de ciclos de permutações COM PESOS (cycle weights), não sobre redirecionamento/perturbação como neste arquivo. Nenhum mecanismo do tipo M-q identificado na literatura. |
| 7 | WebSearch | `fractional Poisson process Mittag-Leffler waiting time inverse stable subordinator continuous time random walk` | Confirma processo de Poisson fracionário = processo de Poisson clássico com tempo trocado por subordinador estável inverso (Meerschaert-Straka 2013 e correlatos); função de sobrevivência de "zero eventos" = Mittag-Leffler E_β(−ct^β), cauda algébrica (NÃO exponencial) para β<1. Ferramenta-chave considerada para a Seção 3 (não usada na versão final por complexidade de correlação; ver `FINDINGS.md`). |
| 8 | WebSearch | `age-dependent branching process regularly varying lifetime distribution intermediate exponent survival` | Confirma processos de ramificação idade-dependentes (Sevastyanov, Bellman-Harris) com cauda de vida regularmente variável; achado mais relevante veio depois na query #12/13 (teorema de Slack). |
| 9 | WebSearch | `record process point process decreasing rate 1/t renewal counts logarithmic vs power law` | Sem achado direto de um "processo de recordes" com expoente de potência livre — a estrutura clássica de recordes dá crescimento LOGARÍTMICO (não lei de potência com expoente livre), distinto do que precisamos. Descartado como candidato de front (a). |
| 10 | WebSearch | `random mapping functional graph rho length tau length tail exponent perturbation redirection` | Achou a literatura clássica de "random mapping" (ρ, τ de Flajolet-Odlyzko / Pollard-rho): ρ_m/√m → √(π/2), μ_m/√m → √(π/8) — a MESMA classe de universalidade √n do problema base (M-U), não um mecanismo com expoente ajustável. Nenhum mecanismo de "redirecionamento parcial com expoente livre" encontrado nessa literatura. |
| 11 | WebSearch | `Beta-coalescent regularly varying merger rate fragmentation power law index tunable` | Confirma processos de fragmentação-coalescência com mecanismos regularmente variáveis Φ(n)~dn^(β+1), μ(n)~b/n^(α+1) — expoentes α,β livres, comportamento de "explosão" governado por α+β vs 1. Real, nomeado, mas não mapeável diretamente ao M-q (estrutura de blocos/partições, não fração cíclica de f:[n]→[n]). |
| 12 | WebSearch | `critical branching process regularly varying offspring distribution survival probability Slack theorem` | **Achado mais próximo/relevante:** teorema de Slack (1968) — GW crítico com pgf de prole h(s)=s+(1−s)^(1+α)ℓ(1−s), α∈(0,1], dá probabilidade de sobrevivência decaindo como função regularmente variável de índice −1/α (generaliza Kolmogorov, α=1, expoente −1). Estrutura MUITO próxima em espírito ao que se busca (expoente de cauda ajustável via variação regular), mas em processo de ramificação, não em fração cíclica de permutação. Usado como precedente/analogia na Seção 2, NÃO como realização direta. |
| 13 | WebSearch | `"Slack" 1968 branching process survival probability regularly varying offspring generating function` | Confirmação repetida do achado #12 com mais detalhe (Yaglom-type limit, constantes de normalização Q_n). |
| 14 | WebSearch | `random permutation partial rewiring probability fraction of points remaining periodic cyclic asymptotic formula` | Sem achado de um mecanismo de "rewiring parcial" com expoente ajustável — resultados voltaram para ciclos de permutações COM PESOS (cycle weights) e dinâmica de "random stirring" (não perturbação por redirecionamento pontual à la M-q). |
| 15 | WebSearch | `small-world network rewiring probability age-dependent tunable exponent power law rewiring rate` | Redes small-world (Watts-Strogatz) com probabilidade de rewiring — expoentes de potência aparecem em DISTRIBUIÇÃO DE GRAU ou tamanho de avalanche, não na fração de pontos "cíclicos" sob um mecanismo à la M-q. Nenhum mapeamento direto. |

**Veredito da frente (a):** em 15 buscas cobrindo os candidatos mais
plausíveis (CRP/Pitman-Yor, urnas de Pólya generalizadas, Hawkes/Omori,
renovação de cauda pesada, Poisson fracionário, ramificação idade-
dependente com variação regular — teorema de Slack, coalescência-
fragmentação, mapeamentos aleatórios clássicos ρ/τ, redes small-world),
**nenhum processo nomeado da literatura foi encontrado que seja, por
reinterpretação direta, um mecanismo M-q com β∈(0,1)** (i.e., que
produza especificamente uma probabilidade de "matar" q(s) que se anula
em s=0 mas mais devagar que linear). O candidato estruturalmente mais
próximo em espírito — o teorema de Slack para processos de ramificação
críticos com prole de variação regular — vive num objeto DIFERENTE
(probabilidade de extinção de uma árvore, não fração cíclica de uma
função [n]→[n]) e usa a variação regular na FUNÇÃO GERADORA DE PROLE,
não numa probabilidade condicional q(s)∈[0,1]. Este padrão (variação
regular entra sempre via uma TAXA ou FUNÇÃO GERADORA, nunca via uma
probabilidade limitada com a forma exigida por q(s)~as^β) é o achado
central usado na Seção 2 de `FINDINGS.md` para motivar a rota da
derivação própria (Frente 2).

## Frente (b) — verificação de citações usadas na derivação própria
(Seção 2 de `FINDINGS.md`)

| # | Ferramenta | URL | Resultado |
|---|---|---|---|
| 16 | WebFetch | `en.wikipedia.org/wiki/Pitman–Yor_process` | Confirma existência do parâmetro de desconto d e menção qualitativa a caudas em lei de potência; **não** contém a fórmula explícita de crescimento N^d no texto extraído. |
| 17 | WebFetch | `docs.tibco.com/.../GUID-E94B660B-...` (Weibull) | **VERIFICADO por fetch direto:** "The early ('infant mortality') phase... can be approximated by a Weibull hazard function with shape parameter c<1; the constant hazard phase... c=1... 'wear-out' stage... c>1." Confirma exatamente a curva-banheira Weibull usada na Seção 2. |
| 18 | WebFetch | `arxiv.org/pdf/0801.0461` | Falha de extração (PDF binário não decodificado pela ferramenta) — declarado, não usado como citação primária. |
| 19 | WebFetch | `emergentmind.com/topics/pitman-yor-process` | Extração corrompida/parcial; não produziu a fórmula limpa — declarado, não usado como citação primária. |
| 20 | WebFetch | `cocosci.princeton.edu/tom/papers/typetoken.pdf` | Falha de extração (PDF) — declarado, não usado. |
| 21 | WebFetch | `arxiv.org/abs/1007.5051` | **VERIFICADO por fetch direto:** "a traditional Poisson process, with the time variable replaced by an independent inverse stable subordinator, is also a fractional Poisson process" — confirma a construção padrão citada na Seção 3 (via alternativa considerada e descartada). |
| 22 | WebFetch | `en.wikipedia.org/wiki/Chinese_restaurant_process` | **VERIFICADO por fetch direto:** fornece a fórmula exata (finito-n) do número esperado de mesas no CRP de dois parâmetros, da qual o crescimento ~n^α segue por assintótica padrão de função Gama (não uma citação adicional, mas uma fórmula primária confirmada). |
| 23 | WebFetch | `cambridge.org/.../critical-markov-branching-process...pdf` (Pakes) | Falha de extração (PDF) — tentativa de verificar o teorema de Slack na fonte secundária; não confirmado por fetch. O achado do teorema de Slack (#12/#13) fica, portanto, com o status "corroborado por resumo de busca com URLs, não verificado por fetch direto de texto completo" — declarado honestamente em `FINDINGS.md`, usado apenas como contexto/precedente, não como base de nenhuma alegação numérica. |
| 24 | WebFetch | `grokipedia.com/page/Branching_process` | HTTP 403 (bloqueado) — declarado, não usado. |

**Nota sobre falhas de extração:** várias tentativas de `WebFetch` em
PDFs acadêmicos (arXiv, Cambridge Core) retornaram apenas metadados de
estrutura (streams comprimidos não decodificados pela ferramenta), não
o texto. Isto é reportado honestamente linha a linha acima; nenhuma
afirmação numérica em `FINDINGS.md` depende de uma citação que não foi
verificada por fetch bem-sucedido — as duas citações estruturalmente
usadas na derivação (curva-banheira Weibull; equivalência Poisson-
fracionário/subordinador-estável-inverso) **foram** verificadas por
fetch direto com sucesso (linhas 17 e 21).
