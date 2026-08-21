# Nota adversarial — reprodução independente da frente u12-universality

**Agente:** reprodução ADVERSARIAL (DISC-CORE-NUMERICS-001 / DISC-DEC-013).
**Data:** 2026-08-21. **Status:** este plano foi gravado ANTES de qualquer
computação adversarial. Nenhum código de `u12_universality/analysis/` nem de
`01_TAMESIS_CORE/06_Universality_Discovery/` foi lido até aqui; a única
leitura permitida e realizada foi `METHODOLOGY_NOTE.md` da frente primária
(definição do ensemble e protocolo de ajuste, que cita as fontes do arquivo
verbatim). A comparação com o código/resultados primários só ocorrerá DEPOIS
que os números adversariais estiverem travados.

## Alvos a refutar (alegações da frente primária)

1. **Expoente:** α ≈ 0.506, IC95 [0.490, 0.522], consistente com 1/2 sob o
   protocolo de ajuste do arquivo (curve_fit não ponderado de `(1+c)^{-α}`
   nas células n=2000, c ∈ {0.5,1,2,5,10,20,50}).
2. **Distinção de classes:** `(1+c)^{-1/2}` decisivamente preferida sobre
   U_0 (degrau), U_1 (`e^{-λc}`), U_2 (`(1+βc)^{-2}`), U_∞ (`1/(1+c^m)`),
   pior ΔAIC ≈ 374.
3. **Anti-alegação:** o "teorema exato" φ → (1+c)^{-1/2} é CONTRADITO —
   desvios sistemáticos que não encolhem com n até 64.000
   (+0.0355±0.0060 em c=0.5; −0.0127±0.0016 em c=50).

## Ensemble (definição operacional pinada, idêntica à da frente primária)

1. π = permutação uniforme de {0,…,n−1}.
2. Para cada i, independentemente com probabilidade p = c/n:
   f(i) = Uniform{0,…,n−1} (com reposição; pode coincidir com π(i));
   caso contrário f(i) = π(i).
3. φ = (# pontos cíclicos do grafo funcional de f)/n.

## Implementação própria (do zero, rota estruturalmente diferente)

- **Reroteamento:** em vez de máscara Bernoulli ponto a ponto, sorteio
  K ~ Binomial(n, c/n), K posições uniformes SEM reposição, K destinos
  uniformes COM reposição (equivalente em distribuição).
- **Detecção de pontos cíclicos:** *pointer doubling* — computo
  g = f^(2^m) com 2^m ≥ n por m composições vetorizadas
  (g ← g∘g); pontos cíclicos = imagem de f^N para N ≥ n; conto o
  tamanho da imagem por scatter booleano por linha. (Rota diferente de
  peeling de Kahn e de caminhada com `path.index`.)
- Lotes (batch × n) em numpy.

## Validação do simulador (antes de qualquer medição)

- **V1 — enumeração exata, n ∈ {4,5,6}, c ∈ {0.5, 2}:**
  E[φ] = Σ_f φ(f)·P(f), com
  P(f) = Σ_{S⊆[n]} (1−p)^{|S|}(p/n)^{n−|S|}·(n−|S|)!/n!·1{f injetiva em S}
  (soma sobre o subconjunto S de pontos "mantidos"; π uniforme integrada
  analiticamente). Cross-check interno da fórmula em n=4,5 contra a média
  bruta sobre todas as n! permutações. MC do simulador no mesmo (n,c) com
  N grande; exige |z| < 3.
- **V2 — benchmark clássico:** c = n ⇒ p = 1 ⇒ random map uniforme puro;
  E[φ] exato = Σ_{k=1}^{n} (n−1)(n−2)…(n−k+1)/n^k / 1 … (fórmula da soma
  de Ramanujan Q(n)/n reescalada), testado em n = 1000. Também c = 0 ⇒ φ = 1.

## Medições (grades e seeds — fixados AQUI, antes de rodar)

Seeds (numpy `SeedSequence`, substreams por `spawn`, um por célula):
- Grade principal / ajuste do expoente: **SeedSequence(424242)**
- Estudo de desvio em n grande: **SeedSequence(31415926)**
- Grade para comparação de modelos (n=4000): **SeedSequence(8675309)**
- Simulação do limite contínuo: **SeedSequence(271828)**
- Validação MC (V1/V2): **SeedSequence(1234321)**

(Todos distintos dos seeds da frente primária: 20260821 e 777.)

### M1 — expoente (espelho do protocolo do arquivo)
n = 2000, c ∈ {0.5,1,2,5,10,20,50}, N = 300 amostras/célula.
Ajuste por mínimos quadrados NÃO ponderado de `(1+c)^{-α}` (curve_fit).
IC95 por bootstrap não paramétrico (B = 4000) sobre as amostras por célula.
Refutação da alegação 1 exigiria IC95 disjunto de [0.490,0.522] ou
inconsistência com 1/2 fora do protocolo declarado.

### M2 — comparação de classes
n = 4000, mesmos 7 c, N = 1000/célula. Mínimos quadrados ponderados
(1/SEM²) para: U_1/2 fixa (k=0), α livre (k=1), U_0 degrau (k=2),
U_1 `e^{-λc}` (k=1), U_2 `(1+βc)^{-2}` (k=1), U_∞ `1/(1+c^m)` (k=1).
AIC = χ² + 2k. Alegação 2 refutada se alguma concorrente tiver
ΔAIC < 10 vs U_1/2 fixa. (O valor 374 depende dos SEMs da frente
primária; o teste adversarial é sobre a ORDENAÇÃO e o limiar ΔAIC ≥ 10.)

### M3 — desvios em n grande (anti-alegação)
c ∈ {0.5, 50}; n ∈ {2000, 4000, 8000, 16000, 32000, 64000}.
N/célula: 8000 (n≤8000), 6000 (16000), 4000 (32000), 3000 (64000).
Δ(n,c) = φ̄ − (1+c)^{-1/2} ± SEM. Anti-alegação refutada se Δ → 0
(encolhimento monotônico consistente com 0 nos maiores n); confirmada se
Δ estabiliza em valor ≠ 0 compatível com o limite contínuo (M4).

### M4 — rota analítica independente: simulação do LIMITE contínuo
Objeto-limite derivado independentemente (sem consultar o arquivo):
ciclos da permutação → partição Poisson–Dirichlet(1) de [0,1]
(stick-breaking com U(0,1), truncado em massa residual < 1e−9);
pontos reroteados → K ~ Poisson(c) posições uniformes em [0,1], cada um
com destino uniforme u_i; o grafo funcional limite é determinado pelo
mapa finito g nos K reroteados (g(i) = primeiro reroteado à frente de
u_i no seu ciclo; absorção se o ciclo de u_i não tem reroteado).
Massa cíclica de uma realização =
  (massa dos ciclos sem reroteados)
  + Σ_{arcos (a,b]} (b − min{u visitado na órbita de b} ∩ (a,b]),
pois y ∈ (a,b] é cíclico sse algum destino visitado pela órbita de b cai
em (a,y]. Estimador não viesado de φ_∞(c) SEM efeitos de n finito.
N = 200.000 realizações para c ∈ {0.5, 50}; 50.000 para os demais c.
Se φ_∞(c) ≠ (1+c)^{-1/2} com significância e coincide com M3, o
"teorema exato" está refutado por DUAS rotas independentes.

## Critérios de veredito (pré-declarados)

- **Item 1 (α):** CONFIRMADO se meu IC95 (protocolo-espelho) intersecta
  [0.490, 0.522] e contém (ou quase contém, |α̂−0.5|<0.02) 0.5;
  REFUTADO se disjunto.
- **Item 2 (classes):** CONFIRMADO se todas as concorrentes (U_0, U_1,
  U_2, U_∞, versões livres) têm ΔAIC ≥ 10 vs U_1/2 fixa em M2;
  REFUTADO se alguma tiver ΔAIC < 10.
- **Item 3 (anti-alegação):** CONFIRMADO se Δ(n, 0.5) e Δ(n, 50) não
  encolhem (razão entre maiores e menores n compatível com 1, não com
  a razão de encolhimento ~1/2 por duplicação esperada p/ correção
  O(1/√n) ou O(1/n)) E os sinais/magnitudes batem com M4;
  REFUTADO se Δ → 0.
- Qualquer bug encontrado (meu ou, depois, do primário) tem precedência
  e será demonstrado com execução, não hipotetizado.

## Orçamento e honestidade

Computação limitada (~15 min de CPU total, 4 núcleos). Se alguma célula
for subamostrada por custo, será dito explicitamente no veredito.
Nenhum número será reportado sem sair de execução gravada em
`.json`/`.log` neste diretório.

*Gravado antes de qualquer execução adversarial. Seeds acima são
definitivos; qualquer alteração exigiria adendo datado.*
