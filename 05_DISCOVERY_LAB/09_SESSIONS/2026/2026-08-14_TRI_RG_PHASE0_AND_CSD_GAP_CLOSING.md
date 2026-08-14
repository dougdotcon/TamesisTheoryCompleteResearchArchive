# Sessão 2026-08-14 — Início da linha TRI-RG e fechamento de gaps de critical-slowing-down

## Contexto

Com a linha RH-REAL considerada suficientemente explorada por ora (dois
sub-testes concluídos, ambos com Gate de Replicação completo acionado),
usuário pediu para iniciar `DISC-TRI-RG-001` — a linha de busca de
invariante cross-domain via lente de renormalização/coarse-graining para
a Theory of Regime Interfaces.

## Fase 0: levantamento de 5 candidatos

Workflow com 5 agentes de pesquisa independentes em paralelo, cada um
avaliando um candidato de par `(R_lambda, I(X))` com instrução explícita
de verificar dado real (baixar/inspecionar, não só citar), seguido de um
agente de síntese que aplicou a mesma régua adversarial a todos os 5
resultados. Relato completo em `02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md`.

**3/5 `viable: true`:** `critical-slowing-down` (rank 1 — variância/
autocorrelação lag-1 crescentes perto de bifurcação, 3 domínios com
transição real dentro do mesmo sistema no tempo: GISP2/Younger Dryas,
PhysioNet SDDB/onset de FV, NASDAQ/crash pontocom); `wavelet-
multiresolution-scaling` (rank 2 — R_lambda mais rigoroso
matematicamente, mas só 1 domínio robusto: sismologia/Tohoku 2011);
`dfa-multiscale-entropy` (rank 3 — execução empírica mais sólida, mas os
2 domínios usados são comparações estáticas de classe, não transições
temporais).

**2/5 `viable: false`**, corretamente rejeitados pelos próprios agentes:
`box-covering-network-renorm` (toda "transição" fractal↔não-fractal vem
de modelos sintéticos, dado real só mostra classificação estática) e
`spacing-statistics-rmt-non-zeta` (reconfirma consenso BGS/RMT de 40
anos sem discriminador Tamesis-específico, nenhum R_lambda genuíno
implementado).

Nenhum candidato foi travado. Usuário instruído a decidir.

## Fechamento dos 3 gaps de `critical-slowing-down`

Usuário pediu para prosseguir com `critical-slowing-down`, fechando os 3
gaps identificados na Fase 0.

**Metodologia fixada ANTES de qualquer cálculo real** (commit `b43fde0`,
`METHODOLOGY_NOTE.md`): regra de `lambda` cross-domain (todos os
parâmetros de escala expressos como frações fixas do comprimento do
segmento — bandwidth=20%, janela=50%, passo=2% — convenção de Dakos et
al. 2012 *PLOS ONE*, não inventada); protocolo de nulo substituto (AR(1)
de parâmetro constante, 1000 substitutos, teste unicaudal de Kendall's
tau — método de Dakos et al. 2008 *PNAS*). Pipeline única
(`csd_common.py`) implementada uma vez e testada contra dado sintético
ANTES de tocar qualquer dado real (caso nulo AR(1) constante: sem
tendência significativa; caso com CSD injetado, coeficiente AR rampando
0,1→0,95: `τ=1,000`, `p=0,000`, detectado com sucesso).

Três agentes independentes, cada um proibido de modificar
`csd_common.py`, baixaram e prepararam o dado real de cada domínio já
verificado na Fase 0 e chamaram a pipeline sem alteração:

- **GISP2** (paleoclima): 764 amostras (registro completo) e 382 (50%
  mais recentes). Primária: `τ_AC1=0,218` (`p=0,398`), `τ_var=-0,366`
  (`p=0,718`) — sem sinal. Robustez: `τ_AC1=0,848` (`p=0,032`, único
  resultado significativo de todos), `τ_var=0,804` (`p=0,058`, marginal).
- **PhysioNet SDDB** (cardíaco, registro 30): série de intervalos RR
  extraída via `wfdb` (131.512 anotações, filtro table-driven padrão
  MIT-BIH excluindo apenas os 2 símbolos não-batimento). 35.382 (primária)
  e 17.691 (robustez) intervalos. AC1 fortemente NEGATIVO em ambas:
  `τ=-0,820` (`p=0,985`) e `τ=-0,947` (`p=1,000`) — direção oposta à
  prevista por CSD. Variância positiva mas não-significativa em ambas.
- **NASDAQ** (financeiro): log(NASDAQCOM), 7.351 (primária) e 3.675
  (robustez) observações diárias. Primária: AC1 e variância ambos
  negativos (`τ=-0,372`, `τ=-0,218`, `p=1,000` ambos). Robustez:
  direção correta mas não-significativa (`p=0,851`, `p=1,000` — este
  último com um efeito-teto documentado: `log(NASDAQCOM)` é quase um
  passeio aleatório puro, coeficiente AR(1) ajustado ligeiramente
  explosivo, `a≈1,001-1,002`).

## Resultado: NEGATIVO

Das 12 combinações (3 domínios × 2 variantes × 2 canais), só 1 cruzou
`p<0,05` — estatisticamente consistente com ruído puro sob múltiplas
comparações sem correção (esperado ~0,6 falsos positivos ao acaso). Em 2
dos 3 domínios o canal de AC1 (o mais diretamente ligado à teoria) mostrou
tendência na direção OPOSTA à prevista. `critical-slowing-down`, testado
com uma regra de `lambda` genuinamente cega ao domínio — a exigência
central de `DISC-TRI-RG-001` — não produz um invariante cross-domain
confiável nestes 3 domínios/transições.

Isso não invalida critical slowing down como fenômeno geral (bem
documentado na literatura usando janelas informadas por conhecimento
específico de cada sistema) — mostra que esta instanciação cross-domain
específica, cega por desenho, não sobrevive. Nenhum `PREREGISTRATION.md`
foi escrito; o próprio passo de fechamento de gaps evitou travar um
pré-registro fadado ao fracasso.

## Estado final

`DISC-TRI-RG-001` segue `CANDIDATE_FORMULATING`. `critical-slowing-down`
não é mais o candidato líder. Restam `wavelet-multiresolution-scaling`
(precisa de 2º domínio robusto) e `dfa-multiscale-entropy` (precisa de
reformulação em torno de transição temporal genuína) como candidatos
viáveis não descartados.

## Próxima decisão (não tomada nesta sessão)

Usuário decide: perseguir `wavelet-multiresolution-scaling` (buscar 2º
domínio), reformular `dfa-multiscale-entropy`, nova rodada de busca por
candidatos, ou considerar `DISC-TRI-RG-001` suficientemente explorada
por ora.
