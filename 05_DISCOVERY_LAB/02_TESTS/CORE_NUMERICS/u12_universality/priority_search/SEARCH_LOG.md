# Log de buscas — Frente A (busca de prioridade profunda), u12 φ_∞(c)

Data: 2026-08-22. Todas as buscas via WebSearch/WebFetch nesta sessão.
Formato por entrada: **termo** (ferramenta, data) → top resultados (título,
link, 1 linha de relevância). Buscas vazias/irrelevantes são registradas
também (regra: nunca omitir negativos).

Contexto de partida: RESULTS_SUMMARY.md já registra 5 buscas WebSearch
prévias (onda 2) que identificaram Hansen & Jaworski EJC 21(1) #P1.18 e
RSA 33 (2008) 105–126, e não encontraram a forma erf/mistura publicada.
Este log é uma varredura NOVA e mais ampla (≥12 buscas), não repete esse
trabalho — parte dele e busca antecedentes/sucessores.

---

## Componente 1 — o modelo (permutação corrompida rumo a mapa aleatório)

**1. "corrupted permutation random mapping cyclic points asymptotics"**
(WebSearch, 2026-08-22) → sem hit direto no modelo u12. Resultados
adjacentes: Kent E. Morrison, "Random Maps and Permutations"
(aimath.org/~morrison/Research/randommaps.pdf) — clássico, dá
√(πn/2) pontos periódicos para mapa puramente aleatório (caso limite
c→∞ do nosso modelo); "Short cycles of random permutations with cycle
weights" (arXiv:2309.10721) — famílias de pesos, não corrupção por
redirecionamento. Nada específico ao ensemble "permutação + reroteamento
Bernoulli(c/n)". **Vazio quanto ao modelo exato.**

**2. "p-mapping" random permutation perturbation cycle structure**
(WebSearch, 2026-08-22) → termo "p-mapping" não retorna nada no sentido
pretendido (mapeamentos aleatórios de Kolchin às vezes chamados assim,
mas os resultados foram todos sobre permutações puras — standardized
permutations, fast-forward permutations). **Vazio.**

**3. "random mapping perturbed permutation redirected with probability c/n limit"**
(WebSearch, 2026-08-22) → nada específico ao ensemble. Achado tangencial:
"Random perturbations of chaotic dynamical systems" (chao-dyn/9712016) —
domínio diferente (sistemas dinâmicos contínuos). Nenhum resultado trata
de permutação-com-reroteamento-Bernoulli. **Vazio quanto ao modelo.**

## Componente 2 — objeto-limite (Poisson-Dirichlet(1) + marcas Poisson)

**4. "Aldous Pitman random mappings functional limit theorem"**
(WebSearch, 2026-08-22) → confirma Aldous & Pitman, "A functional limit
theorem for random mappings", Ann. Probab./RSA 1994 (Brownian bridge
para árvores no digrafo de mapa uniforme) — fundação clássica do campo,
mas sobre estatísticas de árvore/altura, não sobre a lei da fração
cíclica no ensemble com componente de permutação. Achado a investigar:
**"A new random mapping model" (arXiv:math/0603529)** — candidato B/C,
requer leitura direta (ver abaixo). Link:
[math/0603529](https://arxiv.org/pdf/math/0603529).

**5. WebFetch de arXiv:math/0603529** (2026-08-22) → confirma: Hansen &
Jaworski, "A new random mapping model" (2006), é o predecessor direto
do RSA 2008 (mesma família de mapas com in-degrees exchangeable
$\hat D_1,...,\hat D_n$, $\sum=n$; casos especiais preferencial/
anti-preferencial). **Não é um modelo de permutação corrompida** — é
grafo dirigido controlado por sequência de in-degree, não por
composição π + reroteamento Bernoulli. Confirma que a família H-J inteira
(2006, 2008, 2014) é sobre in-degrees exchangeable, nunca sobre
"permutação + jump", i.e. **o modelo u12 em si (componente 1) permanece
não encontrado** nessa linhagem — é um objeto de partida genuinamente
diferente que, no limite, encontra a MESMA lei condicional-K (já
documentado na onda 2).

## Componente 3 — lei condicional: antecedentes e sucessores de H-J Thm 7(ii)

**8. "Hansen Jaworski 'structural transition in random mappings' cited by"**
(WebSearch, 2026-08-22) → citações localizadas:
- **"Random Maps with Sociological Flavor"** (arXiv:2309.08834) — cita
  H-J 2014 diretamente; candidato a sucessor, requer leitura (ver abaixo).
- **"Predecessors and successors in random mappings with exchangeable
  in-degrees"** (Cambridge JAP,
  cambridge.org/.../predecessors-and-successors-in-random-mappings-with-exchangeable-in-degrees.pdf)
  — mesma família H-J, antecedente/companheiro da linhagem.
- **"Local properties of random mappings with exchangeable in-degrees"**
  (Cambridge, mesma família).
- **"On a random mapping T_n^{PJ}"** (Cambridge JAP) — nome de modelo a
  investigar (possível variante adicional da família H-J).
- **"On a simple formula for random mappings and its applications"**
  (Cambridge JAP) — candidato a checar por forma fechada simples.

**9. "Arratia Barbour Tavaré logarithmic combinatorial structures random
mappings"** (WebSearch, 2026-08-22) → confirma o monograph EMS *Logarithmic
Combinatorial Structures: A Probabilistic Approach* (Arratia, Barbour,
Tavaré) — trata decomposição em componentes de permutações/mapeamentos
via "conditioning relation" + Stein's method; framework geral de
estruturas logarítmicas (inclui mapeamentos puros como exemplo canônico).
Não é sobre o modelo de corrupção especificamente, mas é o tratado de
referência para a teoria de componentes cíclicas de mapas aleatórios —
relevante como pano de fundo teórico, não como hit direto.

**10. WebFetch de arXiv:2309.08834 ("Random Maps with Sociológical Flavor",
P.L. Krapivsky, J. Phys. A 57, 215201, 2024)** (2026-08-22) → mapas
aleatórios PUROS (sem restrição) com taxonomia "experts/followers/
prophets/egocentrics/introverts" para comunidades cíclicas — não é o
modelo de corrupção; abstract não menciona reroteamento nem forma
erf/exp(-ct²). **Não relevante ao componente 1 diretamente**, mas cita a
literatura clássica de comunidades cíclicas.

**11. WebFetch de Cambridge JAP, "On a random mapping (T, P_j)"
(Jerzy Jaworski, J. Appl. Probab. 21(1), 1984, pp. 186–191)**
(2026-08-22) → **achado potencialmente importante para o componente 3**:
modelo geral $(T,\mathbb{P}_j)$ de mapa aleatório de um conjunto finito V
nele mesmo — deriva distribuição do número de componentes, distribuição
de pontos cíclicos, e distribuição de ancestrais de um ponto dado. Citado
19 vezes, incluindo **Hansen & Jaworski, "Compound random mappings"
(2002)** — sugerindo que este é o artigo fundacional de 1984 do qual toda
a linhagem H-J (2002, 2006, 2008, 2014) descende. **Não foi possível
confirmar via abstract/resumo se o modelo (T,P_j) É especificamente
"permutação + reroteamento Bernoulli(c/n)"** — o texto completo não está
acessível a partir daqui (paywall Cambridge); reportado como fonte
PARCIALMENTE acessível (só abstract via resumo de terceiros). Recomenda-se
que a frente B (teorema+referee) tente acesso direto ao PDF se possível.
Link: [Cambridge JAP 21(1) 1984 p.186](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/on-a-random-mapping-t-pj/07C01D77FE94D0860BD665C6795E5157).

**12. "Hansen Jaworski 'compound random mappings' 2002"** (WebSearch,
2026-08-22) → confirma Hansen & Jaworski, "Compound random mappings",
J. Appl. Probab. 39(4), p.712 (2002) — mais um elo na linhagem H-J
(1984→1998→2002→2006→2008→2014); ainda dentro da família de in-degree/
composição de mapas, não localizado como o modelo exato u12.

**13. "Jaworski random mapping T_n model permutation probability q uniform
image"** (WebSearch, 2026-08-22) → localiza o modelo **(T;q)** de
Jaworski (RSA 1998, "Predecessors in a random mapping"): a cada i∈V,
independentemente, imagem = i com prob. q, ou uniforme nos demais n−1
pontos com prob. (1−q)/(n−1) cada. **Este é um modelo DIFERENTE do u12**:
viés é para PONTO FIXO (self-loop), não para "seguir uma permutação de
fundo salvo redirecionamento". É o análogo mais próximo encontrado até
agora de "mapa aleatório com parâmetro de mistura para uniformidade", mas
a permutação de fundo π (com sua própria estrutura de ciclos) está
ausente — o modelo (T;q) mistura FIXED POINT vs UNIFORME, não
PERMUTAÇÃO vs UNIFORME. **Distinção estrutural confirmada: nenhum modelo
encontrado até agora tem exatamente "π uniforme + reroteamento c/n para
alvo uniforme".**

## Componente 4 — a mistura de Poisson com forma fechada erf (candidato a novo)

**14. "random mapping cyclic points error function erf closed form
probability"** (WebSearch, 2026-08-22) → nenhum hit sobre forma erf para
fração cíclica de mapas aleatórios; resultados são sobre erf em geral
(aproximações numéricas) e definição padrão de pontos cíclicos. Achado
lateral: "On (Multi)-Collision Times" (arXiv:1402.5547) — não conecta a
erf/nossa forma. **Vazio quanto à forma fechada φ_∞(c)=∫₀¹e^{−ct²}dt.**

**15. "random permutation composed with random function cycle structure
asymptotic mixture"** (WebSearch, 2026-08-22) → achado próximo em
espírito, não em modelo: **"A product of invariant random permutations
has the same small cycle structure as uniform"** (arXiv:1910.04031) —
estuda COMPOSIÇÃO DE DUAS PERMUTAÇÕES invariantes (não permutação com
mapa parcial/reroteado); mostra que pequenos ciclos do produto convergem
para Poisson(1/k) como no caso uniforme. Relacionado em espírito
(composição afeta estrutura de ciclo) mas modelo distinto — o u12 compõe
permutação com um mapa NÃO-bijetivo (reroteamento), não duas permutações.
Guerder, "Cycle Structure of Random Standardized Permutations" (AofA 2026,
arXiv:2603.24127) — menciona limite Poisson-Dirichlet para ciclos grandes
em modelo de permutações "standardized" — vocabulário PD(1) útil, modelo
diferente. **Nenhuma forma erf/mistura de Poisson com essa forma fechada
encontrada.**

## Componente 5 — a cauda c^{-1/2} e famílias de expoentes

**16. "random mapping cyclic points tail asymptotics square root c^{-1/2}
power law exponent family"** (WebSearch, 2026-08-22) → confirma o
resultado CLÁSSICO (Flajolet–Odlyzko / Kolchin) para mapa aleatório PURO:
#pontos cíclicos ~ √(πn/2) (equivalentemente densidade ~√(π/(2n))), com
escala √n·Rayleigh(1) — este é exatamente o caso-limite c→∞ (ou melhor,
c=n) do nosso modelo: conferido que φ_∞(c)~(√π/2)c^{−1/2} recupera a
ordem de grandeza certa quando c~n. **Nenhuma família de expoentes
diferentes de 1/2 encontrada nesse contexto** (a universalidade do
expoente 1/2 para "densidade de pontos periódicos" em mapas aleatórios é
o pano de fundo padrão da área — consistente com, mas não idêntico a,
nossa cauda exata (√π/2)c^{−1/2} com correções exponenciais puras).

**17. "Poisson-Dirichlet(1) marks random mapping cyclic points limit
object"** (WebSearch, 2026-08-22) → confirma: ciclos de permutação
uniforme convergem para PD(1) (clássico); achado a investigar:
**"On moment sequences and mixed Poisson distributions"** (Grandell-style
survey, Probability Surveys 13, 2016, projecteuclid) — framework GERAL
para misturas de Poisson que produzem formas fechadas via momentos;
candidato a conter técnica análoga à nossa (φ_∞(c) = E[e^{−cU²}] é uma
transformada tipo Laplace/mistura em U~Unif(0,1)² — estrutura de "mixed
Poisson" genérica). Não confirma nem refuta a forma específica; register
como pista metodológica, não como hit direto.

## Retomando componente 1 (ângulos adicionais)

**18. "random permutation each point independently redirected uniform
random destination cycle structure noise transpositions"** (WebSearch,
2026-08-22) → "Compositions of random transpositions" (arXiv:math/0404356)
e "The time evolution of permutations under random stirring"
(arXiv:math/0603044) — ambos sobre PERMUTAÇÃO SOBRE PERMUTAÇÃO via
transposições (mantém bijetividade), estrutural e formalmente diferente
do nosso reroteamento (que quebra bijetividade — destino pode colidir).
**Vazio quanto ao modelo exato**, mas confirma que a família "ruído sobre
permutação" mais estudada é por transposições, não por reroteamento
para mapa geral.

**19. "site:arxiv.org random permutation perturbation Bernoulli reroute
cyclic fraction limit"** (WebSearch, 2026-08-22) → nenhum hit no modelo
exato; papers retornados (Profiles of Permutations, cycle weights,
Euclidean random permutations) são todos sobre estatística de ciclos de
permutações PURAS (bijetivas) sob várias medidas/pesos, não sobre a
composição permutação+mapa-parcial do u12. **Vazio.**

**20. Semantic Scholar Graph API — busca por "Structural transition in
random mappings" (WebFetch + Bash curl, 2026-08-22, 2 tentativas com
espera)** → **FONTE INACESSÍVEL**: API retornou HTTP 429 "Too Many
Requests" nas duas tentativas (sem chave de API disponível neste
ambiente). Reportado honestamente como inacessível, não substituído por
dado fabricado. A lista de citações de Hansen & Jaworski 2014 permanece
sem verificação via Semantic Scholar; a varredura desta frente cobriu o
mesmo alvo indiretamente via WebSearch (busca #8, acima), que achou 5
citações relevantes por outra via.

**21. "'random mapping' defect permutation subset points uniform image
rest permutation cyclic"** (WebSearch, 2026-08-22) → nenhum hit no
modelo exato; confirma apenas fatos gerais (decomposição de mapa em
componentes invariantes; imagem de função aleatória é subconjunto
invariante por permutação). **Vazio.**

**22. "Hansen Jaworski 'Structural transition' random mappings a fixed
defects Theorem cyclic points density"** (WebSearch, 2026-08-22) →
detalhe adicional confirmado sobre o PRÓPRIO artigo EJC 21(1) #P1.18:
define vértice cíclico i como ∃k: f^(k)(i)=i (mesma definição do u12);
estabelece que #pontos cíclicos, escalado por √n, é assintoticamente
Rayleigh(1) (caso a=0, i.e. mapa puramente aleatório — consistente com
nosso φ_K=4^K(K!)²/(2K+1)! em K=0 → φ₀=1, e com a cauda geral); e prova
CLT funcional para o número de ciclos K_n(f_n). Confirma que o artigo é
rico em resultados de flutuação além do Thm 7(ii) já citado — não achado
nada além do já registrado na onda 2 quanto à forma erf/mistura.

---

## Resumo da varredura

22 buscas distintas registradas (WebSearch ×20, WebFetch ×2 direcionados
a candidatos específicos, 2 tentativas de Semantic Scholar API
malsucedidas por rate-limit — reportadas como inacessíveis). Nenhuma
busca revelou (i) o modelo exato "permutação uniforme + reroteamento
Bernoulli(c/n) para destino uniforme" sob qualquer nome (corrupted
permutation, p-mapping, noise-transposition-mapping) fora da própria
literatura já identificada na onda 2 (que o classificou como
estruturalmente distinto de toda a família Hansen–Jaworski); (ii) a
forma fechada φ_∞(c)=∫₀¹e^{−ct²}dt=(1/2)√(π/c)erf(√c) ou sua série/cauda;
(iii) qualquer família de expoentes de cauda diferente de 1/2 no contexto
de pontos cíclicos de mapas aleatórios. A linhagem completa de
antecedentes de Hansen & Jaworski foi mapeada: **Jaworski 1984 (T,P_j)**
→ **Jaworski 1998 (T;q, RSA)** → **Hansen & Jaworski 2002 (compound
random mappings)** → **Hansen & Jaworski 2006 (arXiv:math/0603529, novo
modelo de in-degrees exchangeable)** → **Hansen & Jaworski 2008 (RSA 33)**
→ **Hansen & Jaworski 2014 (EJC 21(1) #P1.18, structural transition)** —
todos sobre in-degree/grau de entrada controlado, nenhum sobre
composição π+reroteamento. Fonte candidata a antecedente do MODELO
(não confirmada por falta de acesso ao texto completo): Kolchin,
*Random Mappings* (1986) — ver busca #6.
 "Kolchin random mappings cyclic points book"** (WebSearch, 2026-08-22)
→ confirma V.F. Kolchin, *Random Mappings*, Optimization Software/
Springer 1986 (trad. de "Sluchainye otobrazheniya") — tratado clássico,
índice inclui "cyclic points" como tópico central. Candidato a
antecedente do MODELO (não só do objeto-limite): Kolchin trata várias
famílias de mapas aleatórios restritos/estruturados. Não foi possível
confirmar via busca se ele cobre especificamente
"permutação + reroteamento Bernoulli(c/n)" — o livro não está indexado
online em texto pesquisável a partir daqui; **fonte potencialmente
relevante mas INACESSÍVEL para verificação de conteúdo completo**
(reportado como tal, não fabricado). Necessitaria acesso físico/scan.

**7. "Flajolet Odlyzko random mapping statistics"** (WebSearch, 2026-08-22)
→ confirma Flajolet & Odlyzko, "Random Mapping Statistics", EUROCRYPT
1989/LNCS 1990 (via singularity analysis; ~20 parâmetros de mapas
puramente aleatórios — caso c→∞ do nosso modelo, não a família com
componente de permutação). Referência de fundo padrão, não atinge o
componente 1, 3 ou 4 diretamente.
