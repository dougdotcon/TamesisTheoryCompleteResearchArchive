# Busca de prioridade — ensemble u12 (φ_∞(c) = ∫₀¹e^{−ct²}dt)

**Frente A, DISC-DEC-015.** Data: 2026-08-22. Varredura completa em
`SEARCH_LOG.md` (22 buscas, WebSearch+WebFetch, incluindo negativos e
uma fonte inacessível reportada como tal). Este documento dá o veredito
por componente e a formulação de prioridade recomendada.

Convenção A/B/C: **A** = não encontrado na literatura → potencialmente
novo; **B** = equivalente já existe → resultado deve se conectar a ele;
**C** = versão mais geral já existe → o que sobra de novo é o que a
versão geral não cobre.

---

## Componente 1 — o modelo

> Ensemble u12: π uniforme de [n]; independentemente, cada i com
> probabilidade c/n é redirecionado para um destino uniforme em [n]
> (substituindo f(i)=π(i) por f(i)=uniforme), senão f(i)=π(i).

**Veredito: A — não encontrado.**

A linhagem completa de "mapas aleatórios com componente de permutação/
grau controlado" foi rastreada até sua origem: Jaworski 1984
(modelo geral $(T,\mathbb P_j)$, J. Appl. Probab. 21(1) 186–191) →
Jaworski 1998 (modelo $(T;q)$: imagem = ponto fixo com prob. q, uniforme
nos demais n−1 pontos com prob. (1−q)/(n−1) cada — RSA 13) → Hansen &
Jaworski 2002 (compound random mappings, JAP 39(4) 712) → 2006
(arXiv:math/0603529, in-degrees $\hat D_i$ exchangeable somando n) →
2008 (RSA 33, 105–126) → 2014 (EJC 21(1) #P1.18). **Toda essa família é
parametrizada por sequência de GRAU DE ENTRADA (in-degree)**, não por
uma permutação de fundo perturbada por reroteamento independente por
ponto. O modelo $(T;q)$ de 1998 é o mais próximo em espírito (mistura
entre um regime "estruturado" — ali, ponto fixo — e um regime uniforme)
mas mistura FIXED POINT vs UNIFORME, não PERMUTAÇÃO (com sua estrutura
de ciclos inteira) vs UNIFORME — uma diferença estrutural relevante:
no modelo u12 o objeto de fundo tem CICLOS DE TODOS OS TAMANHOS (PD(1))
antes de qualquer corrupção, o que é o ingrediente essencial da derivação
(DERIVATION.md §1, "arcos" nascem de fatiar os ciclos de π).

Termos de busca "corrupted permutation", "p-mapping" e variações não
retornam a literatura correta (não é terminologia usada na área — a
área usa "random mapping with exchangeable in-degrees" ou, informalmente,
nomeia por autor: modelo $(T,\mathbb P_j)$, modelo $\hat T_n^r$ etc.).
**Ressalva de honestidade:** Kolchin, *Random Mappings* (1986) — tratado
clássico com "cyclic points" indexado — permanece **não verificado por
falta de acesso ao texto completo** (ver SEARCH_LOG.md #6); é o único
candidato remanescente que poderia, em princípio, conter uma variante
equivalente ao modelo u12 sob outro nome, dado que precede toda a
linhagem H-J. Reportado como inacessível, não como "confirmadamente
ausente".

## Componente 2 — o objeto-limite (PD(1) + marcas Poisson)

**Veredito: B — equivalente/componentes conhecidos, combinação é o que
precisa ser conectada.**

Cada peça isolada é clássica: (i) os comprimentos de ciclo normalizados
de uma permutação uniforme convergem para Poisson–Dirichlet(1) — fato
padrão, confirmado nas buscas #17 (Poisson-Dirichlet e Ewens/PD(θ)) e
consistente com Aldous–Pitman 1994 (busca #4, árvores no digrafo via
excursão browniana; mesma base de permutação uniforme). (ii) marcas
Poisson(c) sobre um intervalo/processo contínuo são o mecanismo padrão
de "amostragem de defeitos" em toda a família H-J (o parâmetro a=K é
literalmente o número de marcas). **A combinação específica "PD(1) como
substrato + K marcas Poisson(c) iid uniformes sobre [0,1] definindo o
grafo de reroteamento"** não foi encontrada como objeto nomeado em
nenhuma busca — mas isso é porque a literatura H-J nunca precisa
CONSTRUIR esse objeto-limite explicitamente a partir de uma permutação:
ela already trabalha diretamente no mapa aleatório com grau controlado,
sem passar por PD(1). A construção via PD(1)+marcas é a maneira do u12
de RECUPERAR o mesmo objeto-limite condicional a partir de um ponto de
partida diferente (permutação, não grau) — conectando-se ao componente 3.

## Componente 3 — a lei condicional a K reroteamentos

> φ_K = ∫₀¹(1−t²)^K dt = 4^K(K!)²/(2K+1)!; densidade 2Kx(1−x²)^{K−1}.

**Veredito: B — JÁ CONHECIDA**, confirmado e reforçado nesta varredura
(a onda 2 já havia identificado a citação; esta frente varre
antecedentes/sucessores em torno dela).

**Citação primária (verbatim, verificada por WebFetch do PDF na fonte):**
Jennie C. Hansen & Jerzy Jaworski, "Structural transition in random
mappings", *Electronic Journal of Combinatorics* **21**(1) (2014), #P1.18.
Teorema 7(ii): para $a$ fixo (número de vértices de "defeito", modelo
$\hat T_n^r$ com $a=n-r$) e $k=\lfloor xn\rfloor$,
$P\{\hat X_n^r=k\}\sim \tfrac1n\cdot 2ax(1-x^2)^{a-1}$ — a mesma densidade
condicional-K do u12 (com $a=K$), cuja média é exatamente
$\int_0^1(1-x^2)^a\,dx=4^a(a!)^2/(2a+1)!=\varphi_K$.
Link: https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p18/pdf/

**Antecedentes na linhagem (mapeados nesta frente, buscas #8, #12, #13,
#20, #22):** Jaworski 1984 (JAP 21(1) 186–191, modelo geral $(T,\mathbb
P_j)$, já deriva distribuição de pontos cíclicos e de ancestrais — citado
19× incluindo Hansen–Jaworski 2002) → Jaworski 1998 (RSA 13, modelo
$(T;q)$) → Hansen & Jaworski 2002 (JAP 39(4) 712, "Compound random
mappings") → 2006 (arXiv:math/0603529, in-degrees exchangeable) → 2008
(RSA 33, 105–126, "Predecessors and successors...") → 2014 (EJC, o alvo).
O próprio artigo EJC 2014 contém resultados adicionais não citados na
onda 2: caso a=0 (mapa puramente aleatório) dá √n·(#pontos cíclicos) →
Rayleigh(1) — consistente com φ₀=1 do u12 — e um CLT funcional para o
número de ciclos $K_n(f_n)$ (busca #22).

**Sucessores localizados:** Krapivsky, "Random Maps with Sociological
Flavor" (J. Phys. A 57, 215201, 2024; arXiv:2309.08834) cita H-J 2014
diretamente, mas estuda taxonomia distinta ("experts/followers/
prophets/egocentrics/introverts") sobre mapas SEM restrição — não
estende o Thm 7(ii) condicional-K. Nenhum outro sucessor direto do
Thm 7(ii) foi localizado nesta varredura.

**O que resta de novo aqui:** nada na lei condicional-K em si — ela é
idêntica à de Hansen–Jaworski. O que é novo é a *rota de chegada* (via
permutação + reroteamento Bernoulli, não via grau controlado) e a prova
independente de K=1 por argumento direto sobre PD(1) (DERIVATION.md §5),
que constitui uma re-derivação do caso a=1 do Thm 7(ii) por método
inteiramente diferente — valiosa como verificação cruzada, não como
resultado novo per se.

## Componente 4 — a mistura de Poisson com forma fechada erf

> φ_∞(c) = Σ_K e^{−c}c^K/K! · φ_K = ∫₀¹e^{−ct²}dt = (1/2)√(π/c)erf(√c).

**Veredito: A — não encontrado; candidato mais forte a novidade
genuína.**

Sete buscas dirigidas especificamente a este componente (#14, #15, #16
parcialmente, #17, #21, #22, mais as buscas gerais de fundo #1–13, #18–20)
não localizaram: (i) a forma fechada ∫₀¹e^{−ct²}dt para QUALQUER mistura
de Poisson de $\int_0^1(1-x^2)^K dx$ em qualquer contexto de mapas
aleatórios; (ii) a caracterização equivalente como
$E[e^{-cU^2}]$, $U\sim\text{Unif}(0,1)$; (iii) a série
$\sum_k(-c)^k/(k!(2k+1))$ nesse contexto; (iv) menção do fato — que seria
a assinatura mais fácil de buscar — de que **a mistura de Poisson(c) da
família de densidades de Hansen–Jaworski tem forma fechada em termos de
erf**. O artigo EJC 2014 nunca faz essa mistura (fixa $a$; não soma sobre
$a\sim\text{Poisson}(c)$), porque no modelo H-J (grau controlado) não há
um parâmetro natural análogo a "c" cuja aleatoriedade Poissoniana
produziria essa soma — é uma pergunta que só faz sentido a partir do
ponto de vista do reroteamento Bernoulli (onde #reroteamentos ~
Binomial(n,c/n)→Poisson(c) é imediato). **Isto é consistente com a busca
não encontrar o resultado: a mistura de Poisson é uma pergunta natural
SÓ no framework u12, não no framework H-J**, então não há razão a priori
para esperar que alguém a tenha feito antes a partir do lado H-J.

Achado metodológico correlato (busca #17): "On moment sequences and
mixed Poisson distributions" (Grandell/survey style, *Probability
Surveys* 13, 2016) — framework geral para misturas de Poisson com forma
fechada via transformadas de momento; não contém o resultado específico,
mas confirma que "misturas de Poisson com forma fechada elementar" é uma
classe de resultados estudada em geral — nossa forma se encaixaria como
um caso particular dessa classe, não é um fenômeno isolado.

**Ressalva de busca:** a ausência é negativa (não confirmada por revisão
exaustiva de toda a literatura de mapas aleatórios com grau controlado
publicada 1984–2026), mas a varredura foi ampla o suficiente (22 buscas,
termos em múltiplos ângulos, mais a onda 2 já havia feito 5 buscas
independentes) para que a afirmação "não encontrado nas buscas realizadas"
seja defensável e precisa — não "provado que é novo".

## Componente 5 — a cauda c^{-1/2} e famílias de expoentes

> φ_∞(c) ~ (√π/2)c^{−1/2}, correções apenas exponencialmente pequenas.

**Veredito: C — versão mais geral (o expoente) já é conhecida; o que
sobra de novo é o COEFICIENTE exato e a natureza das correções.**

O expoente 1/2 para a densidade de pontos cíclicos/periódicos é a
assinatura universal de TODA a área de mapas aleatórios: confirmado na
busca #16 para o mapa puramente aleatório clássico (Flajolet–Odlyzko/
Kolchin: #pontos cíclicos ~ √(πn/2), i.e. densidade ~√(π/(2n)) — o caso
c=n do u12) e é o comportamento de escala universal em toda a família
H-J (o próprio Thm 7(ii) tem correções de ordem $n^{-1/2}$ implícitas em
sua estrutura Gaussiana/Rayleigh subjacente, busca #22). **Nenhuma busca
revelou uma família de modelos com expoente de cauda diferente de 1/2**
nesse contexto — 1/2 parece ser universal para "fração de pontos
cíclicos" em qualquer mapa aleatório com grau médio limitado, o que é
consistente com (não contradiz) nosso resultado.

O que É específico do u12 e não localizado em nenhuma busca: o
**coeficiente exato A=√π/2≈0.8862269255** com a declaração de que as
correções ao termo de cauda pura são **exponencialmente pequenas**
(e^{−c}·[potências de 1/c]), não potências adicionais de c^{-1} como é
típico em expansões assintóticas de funções especiais mais gerais. Este
nível de precisão (forma assintótica completa e não apenas o expoente)
não aparece em nenhum resultado H-J localizado — mas, como no componente
4, isso decorre naturalmente de termos a forma fechada exata via erf; a
literatura H-J, sem essa forma fechada, não teria como derivar a mesma
precisão sem primeiro ter a mistura de Poisson.

## A afirmação mais forte legitimamente publicável

Com base no veredito por componente (1: A: não encontrado; 2: B:
componentes conhecidos, combinação nova; 3: B: já conhecida —
Hansen–Jaworski Thm 7(ii); 4: A: não encontrado, candidato central;
5: C: expoente conhecido, coeficiente/forma exata específica do u12),
a frase que o paper pode legitimamente sustentar é:

> **Para o ensemble de mapas aleatórios formado por uma permutação
> uniforme de $[n]$ em que cada ponto é independentemente redirecionado,
> com probabilidade $c/n$, para um destino uniforme (um modelo não
> encontrado sob esta forma na literatura de mapas aleatórios revisada),
> a fração limite de pontos cíclicos é dada pela forma fechada
> $\varphi_\infty(c)=\int_0^1 e^{-ct^2}\,dt=\tfrac12\sqrt{\pi/c}\,
> \mathrm{erf}(\sqrt c)$, com série $\sum_{k\ge0}(-c)^k/(k!(2k+1))$ e
> cauda exata $\varphi_\infty(c)=(\sqrt\pi/2)c^{-1/2}+O(e^{-c})$. A lei
> condicionada ao número exato $K$ de reroteamentos sobreviventes,
> $\varphi_K=\int_0^1(1-t^2)^K\,dt=4^K(K!)^2/(2K+1)!$ com densidade
> $2Kx(1-x^2)^{K-1}$, coincide — apesar do modelo microscópico ser
> estruturalmente distinto (composição de uma permutação com um
> reroteamento Bernoulli independente por ponto, versus uma sequência
> de graus de entrada intercambiáveis) — com o caso de parâmetro fixo
> do Teorema 7(ii) de Hansen & Jaworski, *Structural transition in
> random mappings*, Electronic Journal of Combinatorics 21(1) (2014),
> #P1.18; o resultado deste trabalho identifica o limite do ensemble u12
> como a mistura de Poisson($c$) dessa lei condicional, e — pelas buscas
> aqui documentadas — fornece a primeira forma fechada elementar
> conhecida (via erf) para essa mistura, junto com sua série inteira e
> sua assintótica exata de cauda com correções puramente
> exponenciais.**

Formulação mais curta, para abstract/resumo executivo:

> *Identificamos o ensemble u12 (permutação + reroteamento Bernoulli)
> como um modelo cujo limite condicional-K reproduz exatamente o
> Teorema 7(ii) de Hansen–Jaworski (EJC 2014) a partir de um mecanismo
> microscópico diferente, e cuja mistura de Poisson(c) desse limite tem
> forma fechada elementar em erf — não encontrada na literatura revisada
> — com série e assintótica de cauda exatas.*

### O que NÃO pode ser dito (limites da afirmação, honestos)

- **Não** "novo resultado sobre mapas aleatórios com grau controlado" —
  o modelo u12 não é dessa família; a conexão é só no limite condicional.
- **Não** "primeira vez que se prova a lei condicional-K" — isso já
  estava provado (Thm 7(ii), 2014) para outro modelo microscópico.
- **Não** "prova de que nenhuma referência anterior existe" — a busca é
  ampla (22 consultas) mas não exaustiva; permanece uma fonte
  potencialmente relevante e não verificada (Kolchin 1986, texto
  completo inacessível) e uma API bibliográfica indisponível (Semantic
  Scholar, rate-limited). A frase correta é "não encontrada nas buscas
  realizadas", nunca "não existe" ou "é a primeira".
- **Não** qualquer alegação de prioridade absoluta sem a ressalva acima.

## Arquivos desta frente

- `SEARCH_LOG.md` — 22 buscas registradas (termo, ferramenta, data, top
  resultados), incluindo vazios e a fonte inacessível (Semantic Scholar).
- `PRIORITY_SEARCH.md` — este documento.
