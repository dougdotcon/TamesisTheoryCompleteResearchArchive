# Checagem adversarial de multiplicidade oculta — `DISC-COSMOLOGY-MOND-SPARC-004`

**Agente:** adversarial (passo 7, `AGENTS.md`), execução independente do primeiro agente.
**Gatilho:** `g/g_N` real bruto (bin 0) = 1,0099 > 1 — gatilho pré-declarado (Seção 4/Gap (e) da `PREREGISTRATION.md`) acionado.
**Dados brutos completos:** `analysis/hidden_companion_check.json` (deste script). Reprodução cega da Parte 1 (independente, sem olhar `run_primary_analysis.py` até ter meu próprio resultado): `analysis/result_adversarial_reproduction.json`.

Fontes de literatura usadas (todas de segunda mão via o texto integral já baixado
de Chae 2023, arXiv:2305.04613, verificado nesta sessão): Seções 2.3, 3.2 e 3.3
daquele artigo. `f_multi` observacional (0,25–0,47) vem de Tokovinin (2014b),
Riddle et al. (2015), Moe & Stefano (2017) e Raghavan et al. (2010), citados por
Chae. O mecanismo de "wobble" de fotocentro é atribuído por Chae a Belokurov et
al. (2020) e Penoyre et al. (2022) — referências de segunda mão, não
rebaixadas/reverificadas nesta sessão.

## Resumo executivo

| item | resultado |
|---|---|
| 1. estimativa analítica (só inflação de massa) | magnitude ~0,03–0,06 dex (f_multi 0,25–0,5) — **ordem de grandeza compatível** com o bin 0 (+0,227), mas **forma prevista é CONSTANTE por bin** (não decai com g_N) |
| 2. teste direto RUWE alto vs. baixo | diferença **grande e estatisticamente significativa em todos os 5 bins** (RUWE alto sempre maior, IC95% não se sobrepõe) — evidência direta a favor do mecanismo |
| 3. simulação MC de injeção (massa + wobble) | reproduz a **magnitude** em bins 0–3 razoavelmente bem para f_multi≈0,4–0,5, mas **não reproduz a forma** — no bin 4 (maior g_N) o sinal sintético fica sistematicamente maior que o real, na direção oposta ao declínio observado |

**Veredito da Parte 2:** multiplicidade oculta não corrigida é **claramente parte
da explicação** (item 2 é evidência direta e forte, com a direção certa e
magnitude grande) e explica sozinha uma fração substancial do sinal no bin de
menor g_N — mas **não explica o padrão completo**, especialmente (a) a forma de
declínio suave e monotônico com g_N, que o mecanismo puro de inflação de massa
não prevê (previsão: efeito ~constante) e que o mecanismo de wobble, na
implementação aqui testada, não reproduz corretamente na ponta de maior g_N; e
(b) mesmo no subconjunto "limpo" (RUWE baixo), ainda resta um resíduo
declinante de +0,156 (bin 0) a −0,009 (bin 4) — menor que o valor bruto, mas
não zero, e maior que o piso de ruído (~0,02–0,07 dex) já estabelecido pelo
controle negativo do pré-registro.

---

## Item 1 — estimativa analítica de magnitude (Chae Eqs. 11–13)

Mecanismo: um componente com companheira oculta não resolvida tem sua luz
combinada (host + companheira) interpretada pelo pipeline de massa
(relação massa-magnitude, aproximação `L ∝ M^3.5` que o próprio Chae usa
"quando uma relação aproximada basta", exatamente este caso) como se fosse
uma única estrela. Como a função `M(L) = L^(1/3.5)` é côncava, dividir a
luminosidade entre duas estrelas produz `M_host + M_companheira > M_single-star-equivalente`
— um viés de subestimação de massa PURO, na direção certa (infla `g/g_N`
porque a velocidade real reflete a massa verdadeira, mas `g_N` usa a massa
catalogada, não-corrigida).

Fator de inflação `B(κ) = κ^(1/3.5) + (1-κ)^(1/3.5) ≥ 1`, `κ` = fração de
luminosidade do host (Eq. 12 de Chae, distribuição de `ΔM_G` via poder
`γ_M=-0,7`, Tokovinin 2008, Eq. 13). Simulação com 2×10⁶ sorteios: mediana
de `B(κ)` = 1,594 (log₁₀ = 0,203 dex) quando um componente é afetado.

Ponderando pela regra de atribuição de Chae (40% só o componente brilhante,
30% só o fraco, 30% ambos) e por `f_multi ∈ {0,25; 0,4; 0,5}` (faixa
observacional 0,25–0,47 e faixa auto-calibrada de Chae 0,3–0,5), o
deslocamento médio esperado em `log₁₀(g/g_N)` sobre **toda** a amostra
(não só os sistemas afetados) é:

- `f_multi=0,25`: **+0,028 dex**
- `f_multi=0,4`: **+0,045 dex**
- `f_multi=0,5`: **+0,056 dex**

**Comparação com o observado:** o bin 0 real é +0,227 dex — cerca de 4–8×
maior que esta estimativa pura de inflação de massa. Mesmo no limite
superior otimista (`f_multi=0,5`), o efeito de massa sozinho cobre só
~25% do bin 0. **E, crucialmente, este mecanismo não depende de `g_N`/
separação — previsão é um deslocamento aproximadamente CONSTANTE em todos
os bins**, o que **não bate com a forma observada** (declínio de +0,227
para +0,047, fator ~5×). Isso motiva testar o mecanismo de wobble de
fotocentro (Item 3), que tem uma dependência natural de escala.

## Item 2 — teste direto: RUWE alto vs. RUWE baixo

RUWE (Renormalized Unit Weight Error) é um indicador astrométrico de
ajuste de fonte única malsucedido — convenção comum usa `RUWE>1,2` como
sinal de possível não-resolução/perturbação (Lindegren et al. 2021,
documentação Gaia DR2/EDR3). Usamos `RUWE_max = max(RUWE1, RUWE2)` por
sistema.

- **31,06%** da amostra de descoberta (9.380/30.203 sistemas) tem
  `RUWE_max>1,2`.
- Rodei a pipeline travada (`run_delta_obs_newt`, `n_mc=200`,
  `n_bootstrap=300`) **separadamente** nos dois subconjuntos:

| bin | δ (RUWE alto, n~1421-2969) | δ (RUWE baixo, n~3073-4621) | diferença | IC95% se sobrepõe? |
|---|---|---|---|---|
| 0 | +0,495 | +0,156 | **+0,339** | não |
| 1 | +0,422 | +0,077 | **+0,345** | não |
| 2 | +0,367 | +0,046 | **+0,322** | não |
| 3 | +0,299 | +0,025 | **+0,274** | não |
| 4 | +0,149 | −0,009 | **+0,157** | não |

Em **todos os 5 bins**, sistemas com RUWE elevado mostram excesso muito
maior (0,16–0,35 dex a mais) que sistemas com RUWE baixo, com os
intervalos de confiança de 95% claramente não se sobrepondo — **evidência
direta e forte, na direção certa, a favor da explicação de multiplicidade
oculta**. Além disso, o subconjunto RUWE baixo, sozinho, já mostra δ
próximo de zero no bin 4 (−0,009, compatível com zero) e valores bem
menores que o pleno da amostra em todos os bins — consistente com RUWE
alto sendo, ao menos parcialmente, responsável pelo sinal.

**Confundidor importante, verificado explicitamente:** a fração de
sistemas com RUWE alto **aumenta** com o bin de g_N (23,5% no bin 0 até
49,1% no bin 4 — ver tabela abaixo), na direção OPOSTA à necessária para
que a composição RUWE-por-bin explique, por si só, o declínio observado
de δ com g_N. Se a hipótese fosse "bin 0 tem δ maior simplesmente porque
tem mais sistemas com RUWE alto", esperaríamos a fração de RUWE alto mais
alta no bin 0 — o oposto é observado. Isso não invalida a evidência
"dentro de cada bin" do item 2 (que é robusta e consistente em todos os 5
bins), mas mostra que a variação de composição por RUWE NÃO é, por si só,
o mecanismo que produz o padrão de declínio com g_N — outro fator
(provavelmente físico, ligado à escala orbital, como testado no Item 3)
precisa estar em jogo para explicar por que RUWE se correlaciona tão
fortemente com δ EM CADA bin, mesmo com essa composição invertida.

| bin | n | fração RUWE_max>1,2 | mediana RUWE_max |
|---|---|---|---|
| 0 | 6042 | 23,52% | 1,079 |
| 1 | 6040 | 25,56% | 1,084 |
| 2 | 6040 | 26,64% | 1,091 |
| 3 | 6039 | 30,42% | 1,108 |
| 4 | 6042 | 49,14% | 1,193 |

(Nota honesta: RUWE mais alto em bin 4 também é esperado por um efeito de
seleção não-relacionado à multiplicidade — sistemas de g_N maior tendem a
ter separações menores e/ou massas maiores, muitas vezes associados a
estrelas mais próximas/brilhantes onde a sensibilidade astrométrica do
Gaia a QUALQUER perturbação, incluindo ruído instrumental comum, é maior.
Não isolamos aqui se o aumento de RUWE com o bin reflete mais
multiplicidade real ou maior sensibilidade de detecção — ambos são
plausíveis e não mutuamente exclusivos.)

## Item 3 — simulação Monte Carlo própria de injeção (reimplementação do zero)

Reimplementei do zero (não reaproveitando `generate_synthetic_vp_newtonian`
do primeiro agente, embora eu chame as funções auxiliares já travadas
`dc.sample_eccentricity`/`dc.sample_orbital_geometry` para a órbita
externa, exigido pela mesma metodologia) um gerador de `v_p` sintético
para um conjunto **puramente Newtoniano** (zero física MOND) com a MESMA
distribuição real de massa/separação/excentricidade da amostra de
descoberta, injetando:

1. **Inflação de massa** (Chae Eqs. 11–13, Item 1 acima) — companheira
   oculta atribuída a 40%/30%/30% (brilhante só / fraco só / ambos),
   `ΔM_G` via lei de potência `γ_M=-0,7`.
2. **Wobble de fotocentro** (versão aproximada de Chae Eqs. 19–20):
   semi-eixo interno `a_in` log-uniforme em `[0,01; d_pc]` UA (Belokurov
   et al. 2020, citado por Chae), órbita interna Kepleriana própria
   (fase orbital sorteada uniformemente — simplificação declarada, não
   ponderada pelo tempo como a órbita externa), fator `η_phot` (Eq. 20,
   ramo não-resolvido), somado ao `v_p` externo por soma vetorial com
   ângulo relativo aleatório (órbita interna não-correlacionada com a
   externa).

`M_tot` passado à pipeline (para ambos os ramos, real e mock) é sempre a
massa **catalogada, não-corrigida** — exatamente como o pipeline real
opera (ele não sabe da companheira oculta).

| cenário | δ bin0 | δ bin1 | δ bin2 | δ bin3 | δ bin4 |
|---|---|---|---|---|---|
| **real observado** | +0,227 | +0,172 | +0,131 | +0,103 | +0,047 |
| f_multi=0,3, com wobble | +0,128 | +0,121 | +0,108 | +0,097 | +0,092 |
| f_multi=0,4, com wobble | +0,167 | +0,157 | +0,140 | +0,125 | +0,115 |
| f_multi=0,5, com wobble | +0,218 | +0,218 | +0,203 | +0,153 | +0,141 |
| f_multi=0,4, SÓ massa (sem wobble) | +0,041 | +0,032 | +0,033 | +0,029 | +0,052 |

**Leitura honesta:**
- A magnitude em `f_multi≈0,4–0,5` (dentro da faixa auto-calibrada de
  Chae, 0,3–0,5) reproduz razoavelmente bem os bins 0–3 (razão
  sintético/real entre 0,7 e 1,5 nesses bins para f_multi=0,4–0,5).
- **A forma não bate no bin 4** (maior g_N): o real cai para +0,047, mas
  o sintético permanece em +0,09 a +0,14 — 2 a 3× MAIOR que o real nesse
  bin, na direção ERRADA (o mecanismo de wobble aqui implementado não
  desliga rápido o suficiente em alta g_N). Isso é esperado em parte pela
  simplificação de fase orbital uniforme (não ponderada pelo tempo) e
  pela aproximação de `a_in` usando `d_mean_pc` do sistema em vez da
  distância específica do componente — mas o desalinhamento de forma é
  grande demais para atribuir só a essas simplificações; sugere que o
  mecanismo de wobble sozinho (nesta implementação aproximada) tem uma
  dependência de escala mais fraca com `g_N` do que o padrão real exige.
- Sem wobble (só inflação de massa), a magnitude fica muito abaixo do
  real em todos os bins (~0,03–0,05 dex vs. 0,05–0,23 observado),
  confirmando o Item 1: massa sozinha não é suficiente.

## Veredito consolidado da Parte 2

A multiplicidade oculta não corrigida **certamente contribui** para o
sinal observado — o Item 2 é evidência empírica direta, forte e
consistente em todos os 5 bins (RUWE alto sempre e significativamente
maior que RUWE baixo). A magnitude é plausivelmente compatível com
`f_multi` na faixa observacional/auto-calibrada de Chae (0,3–0,5) quando o
mecanismo de wobble de fotocentro é incluído, não só a inflação de massa
fotométrica (que sozinha é ~4-8× pequena demais).

Mas o padrão **não é explicado inteiramente** por este mecanismo mundano:
(a) mesmo no subconjunto de RUWE baixo (mais "limpo"), resta um resíduo
declinante de +0,156 a −0,009 — menor que o bruto, mas não nulo nos bins
de menor g_N, e maior que o piso de ruído puro (~0,02–0,07 dex) já
estabelecido no controle negativo pré-registrado; (b) a composição de
RUWE por bin vai na direção ERRADA para explicar a forma via mistura
populacional; (c) a simulação de injeção física direta, mesmo com
`f_multi` no limite superior da faixa da literatura, não reproduz a forma
monotônica completa — superestima o resíduo no bin de maior g_N.

**Conclusão:** o sinal bruto positivo (`+0,227` a `+0,047`) **não pode
ser tratado como puramente um artefato de multiplicidade oculta não
corrigida** — parte substancial dele parece ser. Isso reforça, em vez de
enfraquecer, a conclusão do resultado primário: com ambos os `a0` de teste
(H_A e H_B) já fora do IC 95% mesmo ANTES de qualquer correção de
multiplicidade (que só reduziria ainda mais o sinal real na direção de
`g/g_N=1`, não na direção de recuperar H_A/H_B), a checagem adversarial
não encontra motivo para reverter o veredito `BOTH_FALSIFIED` — mas
recomenda fortemente, em qualquer trabalho futuro sobre este canal, a
implementação completa e não-simplificada da correção de `f_multi` de
Chae antes de qualquer interpretação física mais forte do padrão
residual restante (especialmente nos bins de menor g_N, onde o resíduo
"limpo" de RUWE baixo ainda não é zero).

## Limitações desta checagem adversarial

- O modelo de wobble usa fase orbital interna uniforme (não ponderada
  pelo tempo, ao contrário da órbita externa) e `a_in` amostrado com base
  na distância do sistema, não do componente específico — simplificações
  declaradas para viabilizar a simulação no escopo desta checagem, não
  uma reprodução literal de Chae Eqs. 19–20.
- RUWE é um proxy imperfeito e incompleto de multiplicidade oculta —
  não detecta todas as companheiras não resolvidas (períodos muito curtos
  ou muito longos, ou razões de massa muito desiguais, podem não
  perturbar RUWE o suficiente para cruzar o limiar de 1,2) — o resíduo
  não-nulo no subconjunto "RUWE baixo" é consistente com isso, não
  necessariamente com um sinal físico independente de multiplicidade.
- Não implementei a calibração completa (auto-calibração de `f_multi`
  contra a convergência ao Newtoniano em alta aceleração, como Chae faz)
  — usei valores fixos da faixa observacional/da faixa auto-calibrada de
  Chae, não uma re-derivação própria.
