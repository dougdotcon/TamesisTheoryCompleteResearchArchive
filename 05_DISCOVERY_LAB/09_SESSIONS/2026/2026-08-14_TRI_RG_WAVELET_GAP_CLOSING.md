# Sessão 2026-08-14 (continuação) — Fechamento dos gaps de `wavelet-multiresolution-scaling`

## Contexto

Após `critical-slowing-down` não sobreviver ao fechamento de gaps
(resultado negativo, ver `2026-08-14_TRI_RG_PHASE0_AND_CSD_GAP_CLOSING.md`)
e a busca de um segundo domínio para `wavelet-multiresolution-scaling`
ter recomendado EEG de crise epiléptica (CHB-MIT), usuário pediu para
fechar os gaps restantes desse candidato.

## Metodologia fixada antes do cálculo

`METHODOLOGY_NOTE.md` (commit `6da7112`): substituição honesta do
método WTMM/wavelet-leader completo (mencionado na Fase 0) pelo método
de log-cumulantes de coeficientes wavelet (WCM — Castaing, Gagne &
Hopfinger 1990; Delbeke & Abry 2000; Wendt, Abry & Jaffard 2007),
tratável computacionalmente para um protocolo de 200 substitutos IAAFT.
`R_lambda` permanece a mesma projeção multirresolução wavelet (`R_2λ =
R_λ'∘R_λ` por construção). `I(X)` passa a ser o log-cumulante de segunda
ordem `C2` (0=monofractal, <0=cascata multifractal genuína).

Regra de janela: até 2h de dado disponível de cada lado da transição (ou
todo o disponível se menor), variante de robustez truncando ao menor dos
dois lados — mesma regra verbal nos 2 domínios. Protocolo IAAFT
bicaudal (sem previsão direcional a priori, diferente de CSD).

**Validação contra dado sintético revelou uma ressalva real do IAAFT
antes de tocar dado real:** um primeiro controle multifractal (cascata
binomial clássica) tinha marginal degenerada (razão max/min ~190×) e
substitutos IAAFT não zeraram `C2` corretamente. Controle substituto
(ruído gaussiano modulado por envelope de cascata log-normal, marginal
bem-comportada) validou a pipeline corretamente: multifractal real
`C2=-1,81` vs. substitutos `-0,37` a `-0,84` (`p=0,000`); nulo
mono-vs-mono corretamente não-significativo.

## Execução nos 2 domínios

**EEG (CHB-MIT, chb01_03):** PRE=76.800 amostras interictais (5 min),
POST=10.240 amostras ictais (~40s, a crise inteira anotada). Variante
primária: `ΔC2=-0,241` (`p=0,040`), `ΔC1=+0,356` (`p=0,015`) —
nominalmente significativo. Variante de robustez (PRE truncado a 10.240,
igualando POST): `ΔC2=-0,144` (`p=0,290`), `ΔC1=-0,074` (`p=0,900`) —
some completamente, `ΔC1` até inverte de sinal. Resultado frágil,
artefato de tamanho de amostra desigual entre PRE/POST, não uma
detecção robusta.

**Sismologia (Tohoku 2011, IU.ANMO/BHZ):** PRE=POST=144.000 amostras (2h
cada, 20 Hz) — ambos vieram completos, então a variante de "robustez"
por truncamento não mudou nada em relação à primária. Resultado inicial
muito significativo: `ΔC2=+0,356` (`p=0,005`), `ΔC1=+0,942` (`p=0,000`).

## Checagem adversarial completa (dado o tamanho do efeito)

Um agente adversário investigou três ataques:

1. **Saturação/clipping do sismômetro — REJEITADA.** Pico de amplitude
   usa só 31,3% da escala de 24 bits do digitalizador (resposta
   StationXML real consultada para a estação/canal/época exatos); sem
   valores repetidos nos picos, sem platôs; nenhum relato de clipping
   documentado para ANMO/GSN durante Tohoku 2011.

2. **Robustez com truncamento genuíno** (`N=16.384`, ~8,8× menor):
   `ΔC2` NÃO desaparece, mas dispara 6,5× (`0,356→2,30`, `p=0,015`) —
   diagnosticado como artefato de estimador de amostra pequena (a escala
   wavelet mais grosseira sobrevivente tem só 16 coeficientes, o mínimo
   permitido, um ponto de alta alavancagem que distorce a regressão de
   10 pontos). `ΔC1` perde significância por completo (`p=0,595`).

3. **Sensibilidade a amplitudes extremas** (winsorizar só o 1% superior
   do POST, nenhuma amostra clipada): `ΔC2` INVERTE DE SINAL e perde
   toda significância (`0,356,p=0,005 → -0,662,p=0,990`). `ΔC1`
   permanece praticamente inalterado.

**Checagem cruzada:** razão de desvio-padrão POST/PRE (~585×) ainda mais
extrema que a razão ~190× já sinalizada como problemática na própria
validação sintética do IAAFT desta metodologia — a mesma limitação
conhecida do pipeline, não uma surpresa nova.

## Veredito: NEGATIVO nos 2 domínios

Nenhuma variante, em nenhum dos 2 domínios, tem `ΔC2` E `ΔC1`
simultaneamente significativos e estáveis. `ΔC1` no domínio sísmico
provavelmente reflete apenas movimento telessísmico mais forte/alto
amplitude (não necessariamente "mais multifractal"). `ΔC2` — a
estatística que de fato indica multifractalidade — é frágil em ambos os
domínios, consistente com instabilidade de estimador mais a limitação
já conhecida do IAAFT.

`wavelet-multiresolution-scaling`, testado com protocolo genuinamente
cego ao domínio e checagem adversarial completa, não produz um
invariante cross-domain confiável — mesmo veredito já obtido para
`critical-slowing-down`. Nenhum `PREREGISTRATION.md` foi escrito.

## Estado final da linha DISC-TRI-RG-001

Dois dos três candidatos viáveis da Fase 0 (`critical-slowing-down`,
`wavelet-multiresolution-scaling`) fecharam gaps completos, com checagem
adversarial onde justificada, e ambos resultaram negativos. Resta
`dfa-multiscale-entropy` (rank 3), que precisaria de reformulação em
torno de uma transição temporal genuína (em vez da comparação de classe
estática usada na Fase 0) antes de poder ser testado da mesma forma.

## Próxima decisão (não tomada nesta sessão)

Usuário decide: reformular `dfa-multiscale-entropy`, nova rodada de
busca por candidatos ainda não considerados, ou considerar
`DISC-TRI-RG-001` suficientemente explorada por ora (3 candidatos
formulados e rigorosamente testados, 2 com fechamento completo de gaps
e checagem adversarial) e priorizar outra linha.
