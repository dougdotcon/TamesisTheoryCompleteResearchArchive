# Pré-registro adversarial — frente u12-limit-characterization (DISC-DEC-014)

**Agente:** verificação ADVERSARIAL (wave 2). **Data:** 2026-08-21.
**Gravado ANTES de qualquer execução numérica e ANTES de ler qualquer
arquivo da frente primária desta wave** (`DERIVATION.md`, `limit_sim.py`,
`RESULTS_SUMMARY.md`, `tabulation.json` etc. — não lidos). Únicos insumos:
o enunciado de uma linha da alegação (fornecido pelo orquestrador) e os
arquivos da wave 1 (`u12_universality/RESULTS_SUMMARY.md`,
`u12_universality/adversarial/ADVERSARIAL_VERDICT.md`) apenas para a
definição do ensemble.

## Alegação sob ataque

Para o ensemble: permutação uniforme de `[n]`, cada ponto
independentemente rerroteado com prob. `c/n` para destino uniforme em
`[n]`; observável φ = fração esperada de pontos cíclicos, `n→∞`:

> φ_∞(c) = ∫₀¹ e^(−c t²) dt = (1/2)√(π/c)·erf(√c)

Consequências alegadas: série Σ_k (−c)^k/(k!(2k+1)) (⇒ a₁ = 1/3);
cauda (√π/2)·c^(−1/2); lei condicional em K rerroteamentos
φ_K = 4^K (K!)² / (2K+1)! (integrais de Wallis); conexão com
Hansen & Jaworski, EJC 21(1) 2014, #P1.18, Teorema 7(ii).

## Quatro superfícies de ataque (implementações próprias, do zero)

### (a) Força bruta exata em n pequeno — `adv2_exact.py`
Enumeração EXATA (sem amostragem): E[fração cíclica] = Σ_f peso(f)·cyc(f)/n
sobre TODOS os n^n mapas f, com peso analítico
`peso(f) = Σ_k e_k(m(f))·(1−p)^k·(p/n)^(n−k)·(n−k)!/n!`, onde `m(f)` são
os tamanhos das classes de pré-imagem de f e `e_k` os polinômios
simétricos elementares (soma sobre subconjuntos A onde f coincide com π,
f|_A injetiva), p = c/n. Validação interna: para n=4, cross-check contra
enumeração tripla direta (todas as n! permutações × subconjuntos
rerroteados × destinos, pesos exatos). n ∈ {4,5,6,7}, c ∈ {0.5, 1, 2, 3}.
Extrapolação: ajuste φ_n = φ_∞ + a/n (+ b/n²) e Richardson; comparar
direção/plausibilidade de convergência ao valor alegado.
Cross-check externo: os valores exatos da wave 1 (c=0.5: 0.8626/0.8595/
0.8579 para n=4/5/6) devem ser reproduzidos pela minha implementação.

### (b) Monte Carlo em n grande — `adv2_mc.py`
Simulador próprio, vetorizado em lote: permutação (Fisher–Yates do numpy),
máscara Bernoulli(c/n), destinos uniformes; pontos cíclicos por
**imagem de f^(2^17) via composição iterada (doubling) + contagem de
valores distintos** (nº de pontos cíclicos = |imagem de f^m|, m ≥ n).
Validação: c=0 ⇒ φ=1 exato; c=n ⇒ mapa aleatório puro,
E[#cíclicos] ≈ √(πn/2); cross-check com detector independente por
caminhada com pilha (stack-walk coloring) em n=256.
Valores de c FRESCOS, fora da grade {0.05..100} usada antes:
**c ∈ {0.37, 2.71828, 7.5, 23}**; n = 65536; N ≥ 6000 amostras/célula;
comparação com φ_∞(c) alegado com barras de erro (SEM) e com o
viés de tamanho finito estimado da superfície (a).

### (b2) Objeto-limite contínuo direto — `adv2_continuum.py`
Construção DIRETA do limite (independente da minha derivação analítica):
comprimentos de ciclo GEM(1)/PD(1) por stick-breaking (resto < 1e−12
tratado como massa cíclica não marcada); K ~ Poisson(c) marcas uniformes;
destinos uniformes; massa cíclica exata por realização = massa dos ciclos
sem marca + soma dos segmentos percorridos nas arestas dos ciclos do
grafo funcional marca→marca (segmentos disjuntos por construção).
N ≥ 4×10⁵ realizações por c, c ∈ {0.37, 0.5, 1, 2.71828, 7.5, 23, 50}.

### (c) Re-derivação analítica própria (feita ANTES de executar código)
Registro para o histórico — três resultados obtidos à mão, de forma
independente, antes de qualquer leitura da derivação da frente:

1. **a₁ = 1/3 (exato, argumento direto):** a O(c), K=1 marca; ciclo
   marcado tem comprimento size-biased ℓ ~ U(0,1) (PD(1)); destino no
   mesmo ciclo (prob ℓ): perda esperada ℓ/2; destino noutro ciclo
   (prob 1−ℓ): perda ℓ. E[perda] = E[ℓ − ℓ²/2] = 1/2 − 1/6 = **1/3**
   ⇒ φ ≈ 1 − c/3. Isso também dá **φ_{K=1} = 2/3** exato (= 4·1/3! ✓).
   Discrimina contra a forma antiga (1+c)^{−1/2} (a₁ = 1/2).

2. **Cauda (√π/2)·c^(−1/2) (assintótica própria):** para c grande,
   P(x cíclico) ≈ E[D]·Σ_t ∏_{s≤t}(1 − massa visitada); arcos entre
   marcas ~ Exp(c), arco visitado é size-biased (média 2/c), logo massa
   visitada após s saltos ≈ 2s/c; Σ_t e^{−t²/c} ≈ √(πc)/2; E[D] = 1/c
   (D uniforme no arco size-biased) ⇒ φ ≈ (√π/2)·c^{−1/2}.
   (Nota: ignorar o size-biasing dos arcos visitados daria √(π/2)·c^{−1/2},
   fator √2 errado — armadilha checada.)

3. **Derivação completa própria (processo de exploração):** revelando a
   órbita de x no limite: com massa explorada s e j saltos feitos,
   hazards por unidade de massa: fechamento-π em x (sucesso) 1/(1−s);
   fechamento-π em cada cabeça u_i (falha) j/(1−s); marca (taxa c) com
   salto caindo em massa explorada (falha, prob s) ou fresca (j→j+1,
   prob 1−s). O produto de sobrevivência telescopa:
   fatores (1−s_i) dos saltos cancelam com os (1−s_i)^{−1} do
   telescópio, sobrando P_J = ∫₀¹ e^{−cs} c^J (1−s)^J s^J / J! ds ⇒
   **φ = Σ_J P_J = ∫₀¹ e^{−cs} e^{cs(1−s)} ds = ∫₀¹ e^{−c s²} ds.**
   Ou seja: minha derivação própria REPRODUZ a forma fechada alegada.
   A verificação numérica (a), (b), (b2) testa esta derivação tanto
   quanto a da frente.

4. **Lei condicional:** dado K, a estrutura (posições/destinos uniformes,
   PD(1)) não depende de c ⇒ φ_K é constante em c; a mistura Poisson
   determina unicamente φ_K a partir de φ(c); e
   ∫₀¹e^{−ct²}dt = e^{−c}Σ_K (c^K/K!)∫₀¹(1−t²)^K dt com
   ∫₀¹(1−t²)^K dt = 4^K(K!)²/(2K+1)! (Wallis) ⇒ a lei alegada é
   equivalente à forma fechada. Verificação independente: K=1 = 2/3
   (analítico próprio, item 1) e K=2 = 8/15 ≈ 0.53333 por MC do objeto
   contínuo com K fixo — `adv2_conditional.py`, N ≥ 4×10⁵.

### (d) Lei condicional numérica — `adv2_conditional.py`
K fixo ∈ {1, 2, 3}: alvo 2/3, 8/15, 16/35. MC do objeto contínuo
(mesma máquina de (b2) com K determinístico).

## Critérios de decisão (fixados agora)

- (a) CONFIRMADO se as extrapolações 1/n dos exatos n=4..7 convergirem
  em direção a φ_∞(c) alegado com resíduo da extrapolação < 0.005 e
  monotonicidade coerente; REFUTADO se tendência apontar para valor
  incompatível (> 0.01 além do alcance da extrapolação).
- (b) CONFIRMADO se |φ_MC(n=65536) − φ_∞(c)| < max(3·SEM, viés finito
  esperado ~O(1/√n)... na prática: coerente com extrapolação de (a) e
  |z| < 4 contra o alvo usando SEM agregado; REFUTADO se |z| > 5 estável
  e na direção oposta ao viés finito medido em (a)/(b2).
- (b2) CONFIRMADO se |z| < 4 por célula contra ∫₀¹e^{−ct²}dt (teste
  conjunto χ², p > 0.01); REFUTADO se desvio sistemático |z| > 5.
- (d) CONFIRMADO se K=1,2 baterem 2/3 e 8/15 com |z| < 4.
- Citação Hansen–Jaworski: verificar via WebFetch se o Teorema 7(ii)
  do artigo EJC 21(1) #P1.18 diz o que é alegado.

## Seeds (fixadas agora)

- validação MC: 13131313
- MC n grande (b): 77003917 (+ índice de célula)
- contínuo (b2): 55510123
- condicional (d): 90210777

Só DEPOIS de todos os números acima estarem gravados em JSON/logs eu
leio `DERIVATION.md` e `limit_sim.py` da frente e comparo.
