# Pré-registro: Pico espectral da ressonância de Schumann (~7.83 Hz) na estação ELF de Sierra Nevada

**Status:** LOCKED
**Data de criação:** 2026-08-27 (Fase 0, `DISC-DEC-101`)
**Data de travamento:** 2026-08-27 (`DISC-DEC-102`)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-27 — Fase 0
conduzida por agente de pesquisa dedicado (mandato `DISC-DEC-101`); redigido
e travado pela sessão orquestradora após revisão explícita da proveniência
do dado e da tolerância numérica proposta.
**Origem:** `PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §2.1;
`DISC-SCHUMANN-RESONANCE-001` em `01_PORTFOLIO/TEST_QUEUE.yaml`.

> Preenchido e commitado ANTES de tocar em qualquer dado real. Depois deste
> commit de lock, nenhum campo abaixo pode ser alterado sem abrir um novo
> pré-registro.

## 1. Hipótese exata

A ressonância de Schumann fundamental (cavidade eletromagnética entre a
superfície terrestre e a ionosfera, Schumann 1952) é fisicamente real e
mensurável: em qualquer segmento contínuo de pelo menos 24h de dado bruto
real dos canais NS ou EW da estação ELF de Sierra Nevada, o pico dominante
da densidade espectral de potência (PSD) na janela de busca 5–10 Hz cai
dentro da banda de tolerância pré-registrada (Seção 5). Esta é uma
verificação de reprodutibilidade de um fenômeno físico de 70+ anos de
literatura estabelecida — não uma alegação teórica nova do arcabouço
Tamesis.

## 2. Fonte de dado

- **Dataset:** "Four-year measurements from Sierra Nevada ELF station"
  (Salinas, Rodríguez-Camacho, Portí, Carrión, Fornieles-Callejón,
  Toledo-Redondo, 2022)
- **URL exata (verificada por fetch direto — `WebFetch` na página +
  `curl` HTTP 206 Partial Content no arquivo `2014.zip`):**
  https://zenodo.org/records/6348691 (DOI `10.5281/zenodo.6348691`,
  concept DOI `10.5281/zenodo.6348690`), licença CC-BY-4.0
- **Paper/citação de origem do dataset:** Salinas et al. (2022), "Schumann
  resonance data processing programs and four-year measurements from
  Sierra Nevada ELF station," *Computers & Geosciences*,
  https://www.sciencedirect.com/science/article/pii/S0098300422001030
  (não aberto por fetch direto nesta Fase 0 — bloqueado por 403; mirror
  aberto em https://digibug.ugr.es/handle/10481/75094, não confirmado por
  fetch direto). Companheiro com dado numérico de tolerância, verificado
  por fetch direto: Toledo-Redondo et al., "Four Year Study of the
  Schumann Resonance Regular Variations Using the Sierra Nevada Station
  Ground-Based Magnetometers," *JGR Atmospheres*,
  https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021JD036051 —
  Tabela 1 fornece as faixas aceitáveis de frequência do primeiro modo por
  canal (ver Seção 5).
- **Tamanho esperado:** dado bruto em arquivos horários binários (~1.8 MB
  cada) dentro de arquivos zip anuais (~26.7 GB/ano), março 2013–fevereiro
  2017, canais NS e EW, calibrados na banda 6–25 Hz. Esta análise usará
  apenas um subconjunto pequeno e deliberadamente escolhido (Seção 4), não
  o arquivo completo.

## 3. Modelo nulo / hipótese concorrente

Se a ressonância de Schumann NÃO for capturada de forma confiável por este
instrumento/dataset específico (falha instrumental, calibração incorreta,
ou dominância de ruído de rede elétrica/outra fonte), a PSD não mostrará
nenhum pico distinguível do ruído de fundo dentro da banda de tolerância —
ou mostrará um pico dominante fora dela (ex. em 50/60 Hz de rede elétrica,
ou com o segundo modo ~14 Hz dominando em vez do primeiro modo).

## 4. Estatística de teste

Para cada segmento analisado (Seção 6 do processo): ler a taxa de
amostragem real diretamente dos metadados/arquivo de informação
acompanhando os dados brutos horários (NÃO assumir os 256 Hz mencionados
na literatura secundária sem confirmação direta do próprio arquivo, por
não ter sido confirmado por leitura direta do texto do paper na Fase 0 —
ver `confidence_notes` da Fase 0). Concatenar os arquivos horários do
segmento contínuo escolhido; computar a PSD via método de Welch
(`scipy.signal.welch`), janela Hann, `nperseg` = amostras equivalentes a
64 segundos na taxa real confirmada, sobreposição de 50%. Identificar o
pico de maior potência na sub-banda 5–10 Hz.

## 5. Critério de falsificação

**Tolerância travada:** banda `[6.70, 8.35]` Hz — união das faixas
aceitáveis por canal publicadas em Toledo-Redondo et al. (2022), Tabela 1
(NS: 6.80–8.35 Hz; EW: 6.70–8.22 Hz), a única fonte com número exato
confirmado por fetch direto nesta Fase 0.

- **SUPORTA a hipótese:** o pico dominante de PSD na janela 5–10 Hz cai
  dentro de `[6.70, 8.35]` Hz, em pelo menos um dos dois canais (NS, EW)
  testados, e é claramente separado (não confundível por proximidade) dos
  picos do 2º/3º modo (~14 Hz, ~21 Hz) e de ruído de banda larga.
- **FALSIFICA a hipótese:** nenhum pico distinguível de ruído de fundo
  existe dentro de `[6.70, 8.35]` Hz, em NENHUM dos dois canais testados,
  no(s) segmento(s) analisado(s).
- **Zona de "não distingue":** um pico existe mas sua proeminência acima
  do ruído de fundo local (razão pico/mediana da vizinhança ±1 Hz) é
  inferior a 3× — registrado como tal, não reinterpretado como suporte ou
  refutação.

## 6. Correção para comparações múltiplas

Esta análise testa até 2 canais (NS, EW) × N segmentos de 24h escolhidos a
priori (N declarado antes de abrir qualquer arquivo de dado — recomendado
N=3, espalhados por estações do ano distintas dentro do período
2013–2017, para checar robustez sazonal mencionada na literatura). Cada
canal/segmento é reportado individualmente, sem agregação p-valor — o
critério de suporte/falsificação da Seção 5 já é binário por
canal×segmento, não uma família de testes de hipótese estatística
formal, então nenhuma correção de Bonferroni/FDR é aplicável aqui; a
declaração de N a priori serve para impedir escolha seletiva post-hoc de
qual segmento reportar.

## 7. O que NÃO está sendo testado

- Nenhuma alegação de conexão neural, telepatia, ou transmissão de
  consciência via ressonância de Schumann — sem mecanismo biofísico
  conhecido, explicitamente fora de escopo (`PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md`
  §6).
- Nenhuma alegação teórica específica do arcabouço Tamesis — este é um
  teste de reprodutibilidade de um fenômeno físico já estabelecido na
  literatura, não uma previsão derivada de `01_TAMESIS_CORE`.
- Nenhuma generalização para outras estações/instrumentos a partir de um
  resultado nesta estação específica (Sierra Nevada é uma estação de
  latitude média; suas faixas aceitáveis por canal são específicas do
  instrumento e local).
- Nenhuma alegação sobre a causa física exata da variação diurna/sazonal
  observada (fora do escopo desta verificação de existência do pico).

---

## [Preenchido depois da análise] Resultado

## [Preenchido depois da reexecução adversarial] Veredito adversarial
