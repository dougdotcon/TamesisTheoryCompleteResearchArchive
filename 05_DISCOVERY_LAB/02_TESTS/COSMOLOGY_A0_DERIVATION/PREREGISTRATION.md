# Pré-registro: qual derivação interna de a₀ sobrevive ao dado real SPARC

**Status:** LOCKED
**Data de criação:** 2026-08-12
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-12 (Claude Code)
**Test ID:** `DISC-COSMOLOGY-MOND-SPARC-002` (pivotado — ver `TEST_QUEUE.yaml` e `DISC-DEC-004`)
**Commit em que foi travado:** ver histórico git do commit que introduz este arquivo.

> Preenchido e commitado ANTES de calcular `g†` a partir do dado real. O
> split discovery/holdout (`data/discovery_holdout_split.json`) já foi
> gerado com seed declarado, mas nenhuma análise sobre os dados foi feita.

## 0. Por que este teste existe (não é o desenho original de SPARC-002)

`DISC-COSMOLOGY-MOND-SPARC-002` foi originalmente concebido como "Tamesis
vs. modelo concorrente nomeado" — comparação preditiva fora da amostra.
Investigação obrigatória do `next_action` (extrair a previsão Tamesis exata
de `01_TAMESIS_CORE`, com fonte arquivo:linha, antes de qualquer
pré-registro) encontrou que **não existe** tal previsão: todo lugar do
repositório que toca dinâmica galáctica usa `a₀=1,2×10⁻¹⁰ m/s²` citado
diretamente de McGaugh et al. (2016) e a função de interpolação "simple"
padrão (Famaey & Binney 2005) — nenhuma forma numericamente distinta.

O que existe, e é genuinamente Tamesis-específico, é uma **inconsistência
interna**: duas derivações diferentes de `a₀` a partir de primeiros
princípios, no mesmo corpo teórico, nunca testadas uma contra a outra:

- **Derivação A** ("Ponte Holográfica"),
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Operational_Derivation/03_Holographic_Bridge/mond_derivation_proof.py:28`:
  $a_0 = \dfrac{c H_0}{2\pi}$. Com $H_0=70$ km/s/Mpc (mesmo valor usado no
  próprio arquivo, linha 17), isso dá $a_0^A \approx 1{,}08\times10^{-10}$
  m/s² (verificado por recálculo direto nesta sessão).
- **Derivação B** ("MOND Emergence"),
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/02_MOND_Emergence/index.html:282`:
  $a_0 = c^2/R_H = cH_0 \approx 1{,}2\times10^{-10}$ m/s². Verificação
  numérica direta nesta sessão: com $H_0=70$ km/s/Mpc, $cH_0 \approx
  6{,}8\times10^{-10}$ m/s² — a própria alegação "$\approx 1{,}2\times
  10^{-10}$" na linha 282 é aritmeticamente incorreta por um fator de
  ~5,7, **mesmo sem comparar com nenhum dado externo**. Isso é uma
  inconsistência interna do próprio arquivo, não deste teste.

Este teste pergunta: qual das duas (se alguma) é compatível com o valor de
`g†` obtido ajustando a relação de aceleração radial diretamente ao dado
real SPARC nesta sessão — não ao número de 1,2×10⁻¹⁰ citado de memória da
literatura.

## 1. Hipótese exata

- **H_A:** o valor de `g†` que melhor ajusta a relação
  $g_{\text{obs}} = g_{\text{bar}} / (1-e^{-\sqrt{g_{\text{bar}}/g^\dagger}})$
  ao dado real SPARC (amostra de descoberta, ver Seção 2) é estatisticamente
  compatível (dentro do intervalo de confiança bootstrap de 95%, Seção 4)
  com $a_0^A \approx 1{,}08\times10^{-10}$ m/s².
- **H_B:** o mesmo `g†` ajustado é compatível com
  $a_0^B \approx 6{,}8\times10^{-10}$ m/s².
- H_A e H_B não são mutuamente exclusivas por desenho — mas dado que
  $a_0^A$ e $a_0^B$ diferem por fator ~6,3, o intervalo de confiança do
  ajuste real não deveria cobrir os dois simultaneamente, a menos que o
  ajuste seja extremamente mal restringido (o que também seria um
  resultado informativo).
- Fonte teórica exata: ver Seção 0 acima.

## 2. Fonte de dado

- Dataset: SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157) — mesmos
  arquivos já baixados e verificados em
  `02_TESTS/COSMOLOGY_MOND_SPARC/data/` (`SPARC_Lelli2016c.mrt` +
  `Rotmod_LTG/*.dat`, proveniência em
  `02_TESTS/COSMOLOGY_MOND_SPARC/data/PROVENANCE.md`). Reaproveitado
  diretamente — mesma proveniência, sem novo download.
- Split discovery/holdout: gerado nesta sessão com seed determinístico
  `20260812` (data de lock), `random.Random(20260812).shuffle` sobre a
  lista ordenada dos 175 nomes de galáxia, primeiros 55 (pós-shuffle) para
  holdout, restantes 120 para descoberta. Lista exata em
  `data/discovery_holdout_split.json` (sha256:
  `1ce2d16090ff717fca57367c3b747d6e29a36572418b4e7666ebd40e233493da`),
  commitado junto com este pré-registro. **O holdout (55 galáxias)
  permanece selado até o Gate de Replicação** — nenhuma análise deste
  pré-registro pode tocá-lo.
- Fórmula de $g_{\text{bar}}$ e $g_{\text{obs}}$ (verificada por fetch
  direto de McGaugh, Lelli & Schombert 2016, PRL 117, 201101,
  arXiv:1609.05917, nesta sessão — não assumida de memória):
  - $V_{\text{bar}}^2 = \Upsilon_{\text{disk}} V_{\text{disk}}^2 +
    \Upsilon_{\text{bul}} V_{\text{bul}}^2 + \text{sign}(V_{\text{gas}})
    V_{\text{gas}}^2$ (quadratura com preservação de sinal, convenção
    padrão SPARC — $V_{\text{gas}}$ pode ser negativo nas regiões centrais).
  - $\Upsilon_{\text{disk}} = 0{,}50$, $\Upsilon_{\text{bul}} = 0{,}7$
    $M_\odot/L_\odot$ em 3,6 μm (McGaugh, Lelli & Schombert 2016).
  - $g_{\text{bar}} = V_{\text{bar}}^2/r$, $g_{\text{obs}} = V_{\text{obs}}^2/r$
    (unidades SI: $r$ em metros, $V$ em m/s).

## 3. Modelo nulo / hipótese concorrente

Não há um "modelo nulo" único aqui no sentido do piloto anterior — este é
um teste de **consistência interna** entre duas alegações do próprio corpo
teórico Tamesis, calibrado contra dado real. O papel do "nulo" é
preenchido pelo valor de literatura $a_0 = 1{,}20\times10^{-10}$
(McGaugh et al. 2016, $\pm0{,}02$ stat $\pm0{,}24$ sys) — usado apenas como
checagem de sanidade de que o ajuste desta sessão reproduz o resultado
publicado, não como parte do critério de decisão entre H_A e H_B.

## 4. Estatística de teste

1. Para cada galáxia da amostra de descoberta (120), calcular
   $(g_{\text{bar}}(r), g_{\text{obs}}(r))$ para cada ponto observado
   (fórmulas da Seção 2).
2. Ajuste não-linear de mínimos quadrados de $g^\dagger$ na fórmula da
   Seção 1, pooling todos os pontos de todas as 120 galáxias (mesmo
   método agregado do paper original).
3. Intervalo de confiança de 95% em $g^\dagger$ via bootstrap por galáxia
   (reamostragem com reposição de quais das 120 galáxias entram em cada
   réplica — não reamostragem de pontos individuais, para não quebrar a
   correlação dentro de cada curva de rotação), 1000 réplicas.
4. Verificar se $a_0^A$ e/ou $a_0^B$ caem dentro do IC de 95%.

## 5. Critério de falsificação

- **H_A falsificada** se $a_0^A \approx 1{,}08\times10^{-10}$ estiver fora
  do IC de 95% do $g^\dagger$ ajustado.
- **H_B falsificada** se $a_0^B \approx 6{,}8\times10^{-10}$ estiver fora
  do IC de 95%.
- Se apenas uma sobreviver: resultado registrado como suporte a essa
  derivação especificamente (não a "Tamesis" em geral — ver Seção 7).
- Se nenhuma sobreviver: ambas as derivações internas são falsificadas por
  este teste — resultado válido e informativo, a ser reportado como tal.
- Se as duas sobreviverem: o IC é largo demais para distinguir — reportado
  como INCONCLUSIVO quanto à escolha entre A e B, não como suporte a
  ambas.
- Checagem de sanidade (não afeta o veredito H_A/H_B): o `g†` ajustado por
  esta sessão deve estar em ordem de grandeza compatível com
  $1{,}2\times10^{-10}$ (o valor publicado) — se não estiver, é sinal de
  erro de implementação, e o teste para até isso ser resolvido.

## 6. Correção para comparações múltiplas

Duas hipóteses pré-registradas (H_A, H_B) testadas contra o mesmo IC de um
único ajuste agregado — não há busca sobre múltiplos subconjuntos,
múltiplas estatísticas, ou múltiplos valores candidatos de $a_0$ além dos
dois já declarados nesta seção. Nenhuma correção de Bonferroni/FDR
aplicável além de declarar explicitamente que são duas hipóteses, não uma.

## 7. O que NÃO está sendo testado

- Isto NÃO testa "Tamesis vs. ΛCDM" — ambas H_A e H_B são internas a
  Tamesis; ΛCDM não faz nenhuma previsão sobre $a_0$ para comparar.
- Isto NÃO testa a relação de aceleração radial em si (já estabelecida na
  literatura, McGaugh et al. 2016) — o ajuste desta sessão é uma
  replicação de método para obter um IC comparável, não uma nova alegação
  sobre a RAR.
- Um resultado aqui NÃO decide entre MOND e dark matter, nem entre Tamesis
  e MOND padrão (Tamesis já reduz a MOND padrão neste domínio, ver Seção
  0) — decide apenas qual (se alguma) das duas derivações internas de
  $a_0$ documentadas em `01_TAMESIS_CORE` é compatível com dado real.
- Nenhum resultado implica progresso em qualquer Problema do Millennium.
- O holdout (55 galáxias) só é aberto no Gate de Replicação — a análise
  desta sessão (discovery, 120 galáxias) não decide sozinha o veredito
  final; é `ANALYZED`, não `REPLICATION_PASSED`.

---

## [Preenchido depois da análise] Resultado

## [Preenchido depois da reexecução adversarial] Veredito adversarial
