# Hipóteses testadas e refutadas (ou não sobreviventes) — Discovery Lab

**Por que este documento existe.** O Discovery Lab publica seus
negativos com o mesmo peso que publicaria um positivo. Um laboratório
que só mostra o que "deu certo" não é auditável — não há como distinguir
sorte de método sem ver a taxa de base de tentativas. Esta tabela lista,
sem exceção, toda hipótese/candidato que passou pelo processo formal do
laboratório (pré-registro ou fechamento formal em `TEST_QUEUE.yaml`) e
seu veredito exato, com uma linha honesta do porquê. Nenhuma linha aqui
foi omitida por ser embaraçosa; nenhuma foi suavizada para parecer menos
negativa do que o registro original.

**Convenção de veredito:** ✅ sobreviveu (por enquanto) · ❌ refutado/não
sobrevive · ⚠️ inconclusivo (nem confirmado nem refutado, por limite
estrutural ou de dado, não por erro).

---

## 1. Linha TRI-RG — busca de invariante cross-domain (`DISC-TRI-RG-001`)

16 candidatos genuinamente distintos testados ao longo de 5 rodadas de
busca (Fase 0, 0.5, 0.6, 0.7, 0.8). Fonte:
`05_DISCOVERY_LAB/02_TESTS/TRI_RG/CLOSURE_SUMMARY.md`. Status final da
linha: **`CLOSED_NULL`** (`DISC-DEC-010`, reafirmado em `DISC-DEC-012`).

| # | Candidato | Domínios reais tocados | Veredito | Por quê |
|---|---|---|---|---|
| 1 | critical-slowing-down | GISP2, PhysioNet SDDB, NASDAQ | ❌ | 12 combinações testadas, só 1 cruzou p<0,05 (esperado por acaso sob múltiplas comparações); 2/3 domínios mostraram tendência na direção OPOSTA à prevista |
| 2 | wavelet-multiresolution-scaling | Tohoku 2011, CHB-MIT EEG | ❌ | achado inicial forte em sismologia não sobrevive a truncamento de amostra nem a aparar 1% dos extremos; EEG desaparece ao balancear PRE/POST |
| 3 | dfa-multiscale-entropy | Apneia-ECG, GISP2 | ❌ | achado forte (6 testes bootstrap) explicado por mecanismo fisiológico já conhecido há 40 anos (CVHR); não replicou no 2º domínio |
| 4 | soc-avalanches | Ridgecrest (sismicidade), flares solares GOES | ❌ | achado inicial refutado por nulo ETAS subcrítico (decaimento Omori-Utsu comum, não SOC); sem sinal em flares |
| 5 | mse-multiscale-entropy | Tempestade geomagnética 1989, rolamento FEMTO | ❌ | sem sinal em nenhuma das 8 combinações testadas |
| 6 | grafo-de-visibilidade | Geomagnetismo 2015, furacão Harvey | ❌ | canal primário (`d_B`) estruturalmente não computável (grafos small-world, nunca atingem o piso de diâmetro exigido); canal companheiro (`C`) sem sinal nos 2 domínios |
| 7 | RQA (Recurrence Quantification Analysis) | — (dado real nunca tocado) | ❌ | fechado na própria validação sintética: FNN nunca resolve `m≤10` para ruído fraco; após correção de desenho (Rössler), `p_DET=p_ENTR=1,0`, sem poder |
| 8 | permutation-entropy | Anestesia VitalDB, isquemia European ST-T | ❌ | sem sinal cross-domain |
| 9 | Kramers-Moyal | EUR/CHF (choque SNB), vfdb | ⚠️ | não-computável por 2 razões estruturais distintas do dado real |
| 10 | EVT/Hill | Heat dome PDX, hidrologia Cape Fear | ⚠️/❌ | negativo/não-testável |
| 11 | persistent-homology/TDA | — (dado real nunca tocado) | ❌ | fechado na validação: sem poder discriminativo vs. controle caótico, alta correlação (r≈0,92) com RQA (redundante) |
| 12 | lempel-ziv-complexity | Daphnet FoG, Kīlauea 2018 | ❌ | achado intra-sujeito refutado por reexecução adversarial (falha de generalização entre sujeitos) |
| 13 | largest-lyapunov-exponent | — (dado real nunca tocado) | ❌ | fechado na validação: mesma parede de FNN do RQA (Eixo C compartilhado) |
| 14 | dmd-koopman | Itália COVID-19, Kīlauea 2018 | ❌ | achado dominado trivialmente pelo terremoto M6,9 (artefato de decomposição, não estrutura) |
| 15 | transfer-entropy | CHB-MIT EEG, terremotos Kahramanmaraş | ❌ | achado forte refutado: artefato instrumental de baixa frequência numa estação sísmica, eliminado por filtro passa-alta padrão |
| 16 | epsilon-machine-complexity (`C_mu`) | — (dado real nunca tocado, mesmo após revisão CSSR completa) | ❌ | sem poder discriminativo em 3/3 controles sintéticos computáveis; revisão delimitada confirmou fragilidade genuína do estimador, não bug de implementação |

**Achado estrutural da própria linha** (retrospectiva antes da Fase 0.8):
14 dos 16 candidatos colapsam em apenas ~4 eixos matemáticos latentes
independentes (persistência/taxa de entropia; taxa de relaxação local;
densidade de recorrência via embedding de Takens/Hankel; estatística de
cauda) — a maior parte do espaço de estatísticas não-lineares "óbvias"
da literatura de séries temporais já estava efetivamente coberta antes
de qualquer candidato individual ser testado.

---

## 2. Linha SPARC/MOND (`DISC-COSMOLOGY-MOND-SPARC-00{1..4}`)

Fonte: `05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md`.

| ID | Teste | Veredito | Por quê |
|---|---|---|---|
| SPARC-001 | EFE via curvas de rotação SPARC reais (aglomerado Ursa Maior vs. campo) | ⚠️ | p=0,049373 — cruza 0,05 na direção prevista, mas cai na zona frágil já pré-declarada como tal; excluir 4 galáxias com ajuste de inclinação de 2 pontos inverte o veredito (p→0,0635) |
| SPARC-002 | Qual derivação de `a₀` sobrevive: `a₀=cH₀/2π` vs. `a₀=cH₀` | ⚠️ | achado positivo na amostra de descoberta (H_A sobrevive) NÃO confirmado no Gate de Replicação (holdout de 55 galáxias): `g†` saiu 3,5× maior, IC largo demais |
| SPARC-003 | Réplica via binárias largas Gaia (velocidade projetada) | ⚠️ | estatística pré-registrada estruturalmente incapaz de produzir veredito válido — modelo MOND tem imagem `(1,+∞)`, as 5 medianas reais são todas `<1` (diluição por projeção, efeito conhecido na literatura) |
| SPARC-004 | Réplica via binárias largas Gaia (desprojeção Monte Carlo completa) | ⚠️ | veredito bruto `BOTH_FALSIFIED`, mas checagem adversarial de multiplicidade oculta mostrou que companheiras não resolvidas, em magnitude plausível pela literatura, cobrem sozinhas de 23% a 146% do sinal por bin — nenhum veredito aceito |

---

## 3. Linha RH-REAL — testes numéricos sobre zeros de zeta

Fonte: `05_DISCOVERY_LAB/DISCOVERY_LAB_STATE.md`.

| ID | Teste | Veredito | Por quê |
|---|---|---|---|
| DISC-RH-ZERO-GAP-RUNS-001 | Correlação serial de gaps grandes consecutivos | ✅ (mas hipótese direcional errada) | `INVERSE_SIGNAL`: gaps grandes são MENOS comuns em sequência do que sob reordenação aleatória — oposto do previsto, `REPLICATION_PASSED` em holdout #10²¹ |
| DISC-RH-GAP-EXTREME-VALUE-SCALING-001 | Escala do gap mínimo: GUE (`N^-1/3`) vs. Poisson (`N^-1`) vs. GOE (`N^-1/2`) | ✅ primário / ⚠️ replicação | `β̂=-0,3395` ≈ GUE, exclui Poisson e GOE; `REPLICATION_FAILED` no holdout #10²² só por amostra pequena demais para a grade travada (0 blocos possíveis) — não é contradição |
| DISC-RH-FHK-SHORT-INTERVAL-MAX-001 | Regra ternária pré-registrada: lado iid/REM vs. curva CUE canônica | ⚠️ | lado iid excluído a ≥8,8σ, mas a curva CUE canônica TAMBÉM é rejeitada (-3,62σ) — nenhuma das duas hipóteses sobrevive; confirmado adversarialmente |

---

## 4. `DISC-CORE-NUMERICS-001` — adjudicação de 4 alegações internas do núcleo Tamesis

Fonte: `05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml` (wave1_results).

| Front | Alegação testada | Veredito | Por quê |
|---|---|---|---|
| mc-internal-consistency | `M_c=5,2927e-16 kg` consistente com o resto do núcleo | ❌ | usa o ramo de `a₀` já desfavorecido por SPARC-002; os 4 valores de `M_c` do núcleo divergem em até 189,7× (2,28 ordens); expoente 1/8 veio de varredura de frações contra janela-alvo, não derivação |
| knot-quark-mass | Ajuste `M~exp(αL/D)` sobre rope-length de nós ideais, R²>0,99 | ❌ | R² alegado nunca foi computado pelo script (real: 0,986/0,935, provável confusão com Pearson r); leave-one-out falha em 5/6 quarks; nulo de permutação no percentil 86/70 (limiar 95) |
| constant-fit-adjudication | `sin²θ_W=3/13`, `α⁻¹=Ω^1.03`, `n_s=0,967` de bounce | ❌ | `sin²θ_W`: 7,5σ mesmo no esquema mais caridoso, tuning confessado no código; `α⁻¹`: ajuste de 1 parâmetro a 1 número (0 g.l.); `n_s`: não-identificável, `ξ` escaneado até `n_s=1-2/N` automático |
| **u12-universality** | `φ(c)=(1+c)^{-1/2}` é classe de universalidade real e distinta | ⚠️→✅ (parcial) | forma `(1+c)^{-1/2}` **refutada** (desvios não encolhem até n=64.000, χ² p~5e-227); expoente 1/2 **confirmado**; um achado adversarial não previsto pelo pré-registro revelou a forma correta `φ_∞(c)=∫₀¹e^{-ct²}dt` — única linha da mesa que gerou um resultado sobrevivente, tratado nas ondas seguintes (ver §5) |

---

## 5. A única sobrevivente: cycle survival (`φ_∞(c)=∫₀¹e^{-ct²}dt`)

A única linha desta mesa de adjudicação que não terminou em refutação
foi `u12-universality` — e mesmo essa só sobreviveu depois que a forma
originalmente alegada no arquivo (`(1+c)^{-1/2}`) foi refutada. O que
sobrevive não é a alegação original do arquivo Tamesis, mas um resultado
matemático distinto, encontrado durante a verificação adversarial
(onda 1), depois caracterizado (onda 2) e consolidado com prova rigorosa
e status explícito por afirmação (onda 3) — ver
`tamesis-cycle-survival/`; se essa forma fechada é ou não previamente
não-publicada é o veredito qualificado da frente de prioridade (§5,
"Prioridade parcial" abaixo), não uma alegação livre feita aqui.

Mesmo essa sobrevivente carrega ressalvas explícitas, não é uma vitória
sem condições:

- **Provado incondicionalmente**: a forma fechada no objeto-limite
  `L(c)`, sua série, sua assintótica de cauda com erro rigoroso, a média
  condicional-K para todo K, e a densidade condicional-K=1.
- **Condicional, não teorema**: a convergência finita-n→∞ completa
  depende de um lema aberto (K≥2) nem provado nem refutado.
- **Conjectura, não prova**: a densidade condicional-K completa para
  K≥2 e a lei distribucional incondicional completa — apoiadas por
  testes numéricos (Kolmogorov–Smirnov), não demonstradas.
- **Prioridade parcial**: a lei condicional-K já era conhecida
  (Hansen & Jaworski, EJC 2014, Teorema 7(ii), para um modelo
  microscópico diferente); apenas a forma fechada da mistura de
  Poisson (via erf) não foi encontrada na busca de literatura realizada
  — "não encontrada", nunca "nova" ou "primeira".

---

## Aviso final

**Sobreviver aos testes deste laboratório não é o mesmo que verdade
matematicamente ou fisicamente estabelecida.** Um candidato marcado ✅ ou
⚠️ aqui sobreviveu ao escrutínio adversarial *até agora*, com o rigor e
os dados disponíveis nesta sessão — não mais que isso. A tabela acima
existe justamente para que a única linha sobrevivente (§5) seja lida no
contexto de quantas outras tentativas, igualmente sérias e igualmente
bem-instrumentadas, não sobreviveram. Um resultado matemático provado
(como o Teorema 1 de `tamesis-cycle-survival/`) tem um status diferente
de um resultado empírico que passou em testes estatísticos — mas mesmo
o teorema depende de uma citação estrutural externa (§2.3 de
`THEOREM.md`) e deixa lacunas explícitas não fechadas. Nenhuma linha
desta tabela, sobrevivente ou não, deve ser lida como validação do
programa de pesquisa Tamesis como um todo.
