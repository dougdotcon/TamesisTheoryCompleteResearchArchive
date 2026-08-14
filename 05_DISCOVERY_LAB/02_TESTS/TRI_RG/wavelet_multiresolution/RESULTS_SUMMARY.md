# Resultado do fechamento dos gaps — `wavelet-multiresolution-scaling`

**Data:** 2026-08-14. Metodologia fixada em `METHODOLOGY_NOTE.md` (commit
`6da7112`) e pipeline (`analysis/wtmm_common.py`, log-cumulantes de
coeficientes wavelet + teste de substitutos IAAFT) validada contra dado
sintético ANTES de qualquer cálculo real. Aplicada sem modificação aos
2 domínios verificados (sismologia/Tohoku, EEG de crise/CHB-MIT), com
checagem adversarial adicional no domínio de sismologia dado um achado
inicialmente muito significativo.

## Domínio 1 — EEG de crise epiléptica (CHB-MIT, chb01_03)

PRE = 76.800 amostras interictais (5 min completos); POST = 10.240
amostras ictais (~40s, a crise inteira anotada).

| Variante | ΔC2 | p (bicaudal) | ΔC1 | p (bicaudal) |
|---|---|---|---|---|
| Primária (76800 vs 10240) | −0,241 | 0,040 | +0,356 | **0,015** |
| Robustez (10240 vs 10240) | −0,144 | 0,290 | −0,074 | 0,900 |

**Não sobrevive.** A variante primária mostra significância nominal, mas
some quando o PRE é truncado ao mesmo tamanho do POST (eliminando a
diferença de comprimento de segmento como possível confundidor) — e o
sinal de `ΔC1` chega a inverter de sinal. Resultado frágil, dependente
do desenho do teste, não uma detecção robusta.

## Domínio 2 — Sismologia (Tohoku 2011, IU.ANMO/BHZ)

PRE = POST = 144.000 amostras (2h cada, 20 Hz) — ambos os segmentos
vieram completos, então a variante de "robustez" por truncamento não
mudou nada em relação à primária (só um teste de fato, não dois).

Resultado inicial: `ΔC2=+0,356` (`p=0,005`), `ΔC1=+0,942` (`p=0,000`) —
aparentemente muito significativo. Acionada checagem adversarial
completa dado o tamanho do efeito.

**Hipótese de saturação/clipping do sismômetro: REJEITADA.** Pico de
amplitude usa só 31,3% da escala completa de 24 bits do digitalizador
(resposta StationXML real da própria estação/canal/época consultada);
sem valores repetidos exatamente nos picos (assinatura clássica de
clipping); sem platôs achatados; nenhum relato de clipping documentado
para ANMO/GSN durante Tohoku 2011 (relatos de clipping concentram-se em
instrumentos de movimento forte no Japão, não em estações teleseísmicas
da rede global).

**Mas o achado não sobrevive aos outros dois ataques:**
- **Robustez com truncamento genuíno** (N=16.384, ~8,8× menor que os
  144.000 originais): `ΔC2` NÃO desaparece, mas dispara 6,5× (0,356→2,30,
  `p=0,015`) — diagnosticado como artefato de estimador de amostra
  pequena (a escala wavelet mais grosseira sobrevivente tem só 16
  coeficientes, o mínimo permitido pela regra, um ponto de alta
  alavancagem que distorce a regressão de 10 pontos). `ΔC1` perde
  significância por completo (`p=0,000→0,595`).
- **Sensibilidade a amplitudes extremas** (winsorizar só o 1% superior
  das 144.000 amostras do POST, nenhuma delas clipada): `ΔC2` INVERTE DE
  SINAL e perde toda significância (`0,356,p=0,005 → -0,662,p=0,990`).
  `ΔC1` permanece praticamente inalterado.
- **Checagem cruzada:** a razão desvio-padrão POST/PRE (~585×) é ainda
  mais extrema que a razão ~190× que a própria `METHODOLOGY_NOTE.md`
  já havia sinalizado, na validação sintética, como um caso em que
  substitutos IAAFT falham em zerar `C2` corretamente sob marginais
  degeneradas/de cauda muito pesada — uma fraqueza do próprio pipeline
  já documentada antes de tocar dado real, não uma surpresa.

**Veredito: não sobrevive à reexecução adversarial.** Nenhuma variante
tem `ΔC2` E `ΔC1` simultaneamente significativos e estáveis. `ΔC1`
provavelmente reflete apenas movimento telessísmico genuinamente mais
alto/mais alto de amplitude (mais "alto", não necessariamente mais
"multifractal"). `ΔC2` — a estatística que de fato indica mudança de
estrutura multifractal — é frágil a aparar 1% das amostras e a
truncamento de janela, consistente com instabilidade de estimador mais
a limitação já conhecida do IAAFT, não com estrutura de cascata
genuína.

## Conclusão geral

Nos 2 domínios testados, com a metodologia fixada a priori e checagem
adversarial completa onde justificada, `wavelet-multiresolution-scaling`
**não produz um invariante cross-domain confiável** — mesmo veredito já
obtido para `critical-slowing-down`. Isso não invalida o formalismo de
log-cumulantes wavelet como ferramenta (é bem estabelecido na literatura
de turbulência/tráfego de rede/fisiologia), apenas mostra que, nestes 2
domínios/transições específicos, testados com um protocolo genuinamente
cego ao domínio e adversarialmente checado, o sinal não se sustenta.
Nenhum `PREREGISTRATION.md` foi escrito.
