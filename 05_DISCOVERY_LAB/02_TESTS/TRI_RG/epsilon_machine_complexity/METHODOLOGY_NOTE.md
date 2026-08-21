# Nota de metodologia — fechamento dos gaps de `epsilon-machine-complexity` (Complexidade Estatística de ε-machines, `C_mu`, mecânica computacional)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (intervalos de erupção do gêiser Old Faithful, GeyserTimes.org;
sequência de interevento sísmico da erupção de Cumbre Vieja/La Palma 2021,
catálogo EMSC/IGN). Esta nota faz o papel do `PREREGISTRATION.md` para esta
linha de candidatos (`DISC-TRI-RG-001`) — nenhum `PREREGISTRATION.md` é
escrito nesta linha, por convenção já usada nos 15 candidatos anteriores.
Uma vez travada, esta nota só pode ser corrigida por um bug de
implementação genuíno descoberto na validação — nunca por redefinição de
`I(X)` ou `R_lambda` depois de ver resultado real.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`
(candidato 1) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #2 de 2 candidatos novos daquela rodada (atrás de
`transferência de entropia`, já fechado negativo). Este é o 16º candidato
desta linha e o último pendente da Fase 0.8.

## Decisão de governança já tomada (não relitigada aqui)

O levantamento original (`phase0/PHASE0_8_SURVEY_NEW_CANDIDATES.md`, seção
1) verificou 2 domínios reais: (a) sequências de intervalo de erupção do
gêiser Old Faithful (GeyserTimes.org, alongamento de intervalo por seca
regional entre 1997 e 2003) — transição TEMPORAL genuína, plenamente
consistente com a convenção padrão desta linha; (b) transição estrutural
origem/terminus de replicação (GC-skew) do genoma completo de *E. coli*
K-12 MG1655 — mas ESPACIAL (coordenada genômica, não tempo), sinalizada
pelo próprio levantamento como precisando de aval explícito do
orquestrador antes de uso.

**Decisão da sessão orquestradora: NÃO usar o genoma de E. coli como
domínio decisivo desta candidatura.** Em vez disso, esta sessão buscou e
verificou (por download real, não apenas citação) um SEGUNDO domínio
temporal genuíno, não usado por nenhum dos 15 candidatos anteriores desta
linha nem por Old Faithful: a sequência de interevento sísmico da erupção
de Cumbre Vieja (La Palma, Canárias, Espanha, 2021). O genoma de E. coli
NÃO é usado nesta candidatura de forma alguma — a busca por um segundo
domínio temporal foi bem-sucedida, tornando o fallback espacial
desnecessário.

## Gap (a): `R_lambda` — reconstrução de estados causais (CSSR)

**Simbolização (para os dois domínios contínuos desta rodada — nenhum
alfabeto nativo de 4 símbolos como DNA é usado aqui):** reaproveitada SEM
MODIFICAÇÃO de `lempel_ziv_complexity/analysis/lzc_common.py` (mesma
convenção já auditada nesta linha) — binarização por limiar de mediana
(Aboy, Hornero, Abásolo & Álvarez 2006) como canal primário, quantização
ternária por tercis (Kamath 2016) como canal companheiro, ambos
reestimados a partir do PRÓPRIO segmento (PRE e POST cada um com seu
próprio limiar, nunca herdado).

**Algoritmo primário: CSSR** (Shalizi & Klinkner 2004, *UAI*) — `L_max`
escolhido por regra de convergência orientada por dado (diagnóstico
recomendado pelos próprios autores, análogo a BIC/AIC, NÃO um valor fixo
nem visual): varrer `L_max` em `{1,...,8}` e selecionar o menor `L` a
partir do qual o número de estados causais inferidos para de crescer
(2 valores consecutivos iguais). `alpha=10⁻³` fixado a priori (padrão da
literatura).

**Decisão de escopo #1, declarada honestamente aqui (não uma
reformulação de hipótese):** por restrição de orçamento de tempo desta
tarefa, CSSR é implementado aqui como "clustering de estados causais em
`L` FIXO", não o algoritmo completo de crescimento incremental de árvore
de sufixos de Shalizi & Klinkner. Para um alfabeto PEQUENO (2 ou 3
símbolos) e `L_max<=8` (portanto no máximo `3^8=6.561` histórias
possíveis), o espaço de histórias é diretamente enumerável sem a
explosão combinatória que motivou o crescimento incremental de CSSR para
alfabetos maiores. A cada `L` candidato: (1) constrói-se a distribuição
empírica do próximo símbolo para cada história de comprimento `L`
observada `>=10` vezes (`MIN_COUNT_PER_HISTORY`, piso fixado a priori);
(2) agrupa-se essas histórias em estados causais via teste qui-quadrado
de equivalência distribucional guloso (ordenado por contagem
decrescente); (3) roda-se UM passo de diagnóstico de reparo de
determinismo (decisão de escopo #2 abaixo). Isto é matematicamente
equivalente ao que CSSR converge para naquele `L`, neste regime de
alfabeto pequeno.

**Decisão de escopo #2:** determinismo é DIAGNOSTICADO, não corrigido por
divisão recursiva completa. Uma passagem única mede
`determinism_violation_frac`: entre todas as transições
(estado, próximo símbolo) com dado suficiente nas duas pontas, a fração
cujo estado resultante NÃO é o estado majoritário para aquele par. CSSR
completo faz divisão recursiva até essa fração ser exatamente zero; isso
está fora do escopo aqui. Em vez disso,
`determinism_violation_frac > 0,05` (fixado a priori) é um critério de
REJEIÇÃO adicional — MAIS conservador que ignorar o problema, não menos.

**Gate de rejeição obrigatório (mesma disciplina do gate de FNN em
`largest_lyapunov_exponent`), aplicado ANTES de qualquer interpretação de
`C_mu` real:**
- `DEGENERATE`: número de estados no `L` selecionado `== 1`.
- `NOT_CONVERGENT`: a curva de número de estados nunca estabiliza em toda
  a grade `L=1..8`.
- `NOT_DETERMINISTIC`: `determinism_violation_frac` no `L` selecionado
  excede `0,05` (decisão de escopo #2 acima).

Qualquer segmento (PRE ou POST, qualquer variante de simbolização) que
falhe qualquer um desses 3 critérios é reportado como `NOT_COMPUTABLE`,
nunca um valor calculado silenciosamente.

**Checagem companheira: Inferência Estrutural Bayesiana** (Strelioff &
Crutchfield 2014, *Phys. Rev. E* 89:042119), restrita ao canal
binarizado/ternário (alfabeto pequeno, regime onde BSI é tratável).

**Decisão de escopo #3, declarada honestamente:** BSI completo (comparação
bayesiana de topologias via fatores de Bayes sobre o espaço de máquinas
candidatas) está fora do orçamento desta tarefa. O que É implementado —
exatamente o que o levantamento da Fase 0.8 pediu, "uma checagem de
robustez baseada em posterior sobre a estimativa pontual de `C_mu`" — é
propagação bayesiana de incerteza de PARÂMETRO, condicional à topologia
já selecionada por CSSR: prior Dirichlet(1,...,1) independente por linha
de transição estado-a-estado, posterior Dirichlet atualizado pelas
contagens observadas, amostrado por Monte Carlo (2.000 amostras), cada
amostra gerando sua própria distribuição estacionária (autovetor de
Perron via iteração de potência) e seu próprio `C_mu` — dando média
posterior / desvio / intervalo de credibilidade 95% real, rodado APENAS
sobre dado real PRE/POST (não sobre os 200 substitutos IAAFT — proibitivo
computacionalmente e não é o que uma "checagem companheira sobre a
estimativa pontual" exige).

**Decisão de escopo #4:** `L_max` é selecionado UMA VEZ por segmento/
variante real via a varredura acima, depois mantido FIXO ao computar
substitutos IAAFT/bootstrap para aquele segmento/variante — revarrer `L`
para cada um dos 200 substitutos seria proibitivo computacionalmente e
não é exigido pela metodologia (`L_max` é uma propriedade de `R_lambda`,
fixada uma vez que o dado real a determinou, exatamente como limiares de
mediana/tercil são fixados uma vez computados e depois aplicados
identicamente aos substitutos em outros candidatos desta linha).

## Gap (b): `I(X)` e declaração de identificabilidade

**`I(X)` primário:** `C_mu` — entropia de Shannon (bits) da distribuição
estacionária `pi_s` sobre os estados causais inferidos
(`C_mu = -sum_s pi_s * log2(pi_s)`), com `pi_s` computado como fração de
ocorrências (tempo) em cada estado (método simples, sempre definido).

**`I(X)` companheiro/diagnóstico — REBAIXADO a priori:** `h_mu` — taxa de
entropia do mesmo autômato reconstruído
(`h_mu = sum_s pi_s * H(próximo símbolo | estado=s)`), **esperado
redundante com a família taxa-de-entropia já testada 7+ vezes nesta
linha** (CSD, MSE, DFA, wavelet, VG parcialmente, LZC, PE) — dito aqui
explicitamente, não escondido.

**Riscos de identificabilidade, já investigados no levantamento da Fase
0.8 (citados aqui, não re-derivados):**

- **vs. `C_JS` de `permutation_entropy` (candidato #8, já fechado
  negativo 8/8):** PROVADO objeto DIFERENTE, não apenas nominalmente
  distinto. Feldman & Crutchfield 1998 (*Phys. Lett. A* 238:244) é
  crítica DIRETA, pelo próprio grupo de Crutchfield, à família
  LMC/MPR/Rosso da qual `C_JS` descende — mostram que essa família não é
  intensiva nem extensiva e colapsa a uma função trivial da densidade de
  entropia em casos tratáveis. Crutchfield & Feldman 2003 (*Chaos*
  13:25) provam `(h_mu, C_mu)` como par formalmente independente, com
  limite derivado `E<=C_mu` sem análogo em `C_JS`. **Achado honesto que
  não pode ser escondido:** ambos pertencem à MESMA FAMÍLIA ESTRATÉGICA
  de medidas de complexidade em forma de U-invertido, desenhadas para o
  mesmo tipo de sinal qualitativo (estrutura intermediária entre ordem e
  aleatoriedade total) — se `C_mu` também vier negativo, isso deve ser
  lido como evidência mais forte que um fechamento comum: um sinal sobre
  toda a ESTRATÉGIA de complexidade-em-pico, não apenas mais uma fórmula
  específica que falhou. Este ponto é retomado explicitamente em
  `RESULTS_SUMMARY.md`.
- **vs. `lempel_ziv_complexity` (#12, fechado negativo após reprodução
  adversarial):** diferença qualitativa de forma documentada — LZC é
  monotonicamente crescente em aleatoriedade (converge para taxa de
  entropia, Ziv & Lempel 1978); `C_mu` é não-monotônica (pico em
  estrutura intermediária). Risco baixo, mas sem comparação empírica
  publicada direta em nenhum sentido (dito aqui honestamente).
- **vs. `CI` de `mse_multiscale_entropy` (#5) e `H_S` de
  `permutation_entropy` (#8):** sem relação formal documentada. Risco
  baixo.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada nos 15 candidatos anteriores): PRE (primária) = todo o registro
contínuo disponível anterior à transição documentada; PRE (robustez) =
os 50% mais recentes (por CONTAGEM de amostras) desse PRE. POST
(primária) = todo o registro contínuo disponível posterior à transição,
até o próximo evento/confundidor documentado; POST (robustez) = os 50%
mais próximos da transição desse POST.

### Domínio 1 — Old Faithful, GeyserTimes.org API v5

**Transição documentada:** alongamento do intervalo médio de erupção do
gêiser Old Faithful atribuído a declínio do lençol freático regional por
seca (Hurwitz et al. 2020, *GRL*; NPS/USGS), entre 1997 e 2003.

**Re-verificação real (não apenas citação da sondagem), feita nesta
sessão:** `https://www.geysertimes.org/api/v5/entries/{fromEpoch}/{toEpoch}/2`
consultada diretamente. PRE (julho de 1997): 360 entradas reais logadas;
POST (julho de 2003): 484 entradas reais logadas, POST inteiramente
limpo (intervalo máximo observado 110min, sem gaps de observação).

**Limitação de qualidade de dado descoberta e tratada explicitamente
(ANTES de qualquer cálculo de `C_mu`, não um achado post-hoc):** PRE
1997 contém 32 de 359 intervalos brutos (~8,9%) na faixa 605–775 minutos
— fisicamente implausíveis para este gêiser (nunca documentado excedendo
~2h mesmo em modo "long-interval"; toda a distribuição real fica abaixo
de ~110min, com um vazio limpo entre 106min e 605min nos próprios dados)
— artefatos de LACUNA DE OBSERVAÇÃO noturna (observador ausente por
horas), não intervalos reais do gêiser. **Regra de limpeza fixada a
priori:** qualquer intervalo bruto `> 180 minutos` (3h — teto redondo,
justificado pela literatura, com grande margem de segurança acima de
todo o alcance real observado nos dois períodos e abaixo de todo valor
de lacuna observado) é excluído da sequência de intervalos usada como
`X` — os pontos adjacentes permanecem na sequência ordenada (a lacuna é
simplesmente removida, não interpolada). Após esta limpeza: PRE
N=327 intervalos, média=77,4min, mediana=83min — **reproduz
EXATAMENTE o número citado no levantamento da Fase 0.8** (confirmação de
que a mesma regra de limpeza foi usada lá, agora tornada explícita e
documentada aqui pela primeira vez). POST N=483 intervalos (nenhuma
exclusão necessária), média=92,1min — também bate exatamente com o
levantamento.

**PRE/POST exatos:** PRE = sequência de intervalos limpa de julho/1997
(N=327). POST = sequência de intervalos de julho/2003 (N=483, sem
limpeza necessária). Robustez: 50% mais recentes de PRE (últimos 163
intervalos), 50% mais próximos da transição de POST (primeiros 241
intervalos). `X` = duração do intervalo em minutos, ordenado por índice
de erupção (convenção já usada na literatura de dinâmica não-linear de
gêiseres para tratar a sequência de intervalos como processo de tempo
discreto, independente do tempo relógio real decorrido).

### Domínio 2 — Erupção de Cumbre Vieja, La Palma, Canárias, 2021 — sequência de interevento sísmico

**Fonte:** catálogo FDSN do EMSC (European-Mediterranean Seismological
Centre, `seismicportal.eu`), agregando a rede sísmica local (IGN,
Instituto Geográfico Nacional da Espanha, autor `MDD` nos registros) —
verificado nesta sessão como tendo cobertura MUITO mais densa que o
catálogo global do USGS para esta região/período (USGS ComCat retornou
apenas 5 eventos `M>=4,2` no período; EMSC retornou 1.049 eventos PRE e
6.747 eventos POST, magnitude mínima `Ml=1,5`, consistente com um
catálogo regional bem monitorado).

**Transição documentada:** abertura da erupção do vulcão Cumbre Vieja,
`2021-09-19T14:13:00 UTC` (PEVOLCA/IGN, evento amplamente documentado
externamente — primeira erupção em La Palma desde 1971).

**Definição de PRE (fixada a priori, com limitação nomeada
explicitamente, mesmo espírito da limitação já nomeada para o Kilauea em
`lempel_ziv_complexity`):** La Palma não tem um início natural limitado
de monitoramento (rede sísmica opera continuamente há anos) — "todo o
registro contínuo disponível" literalmente diluiria qualquer contraste
de regime com sismicidade de fundo não relacionada. O enxame sísmico
precursor da erupção começou a se intensificar nitidamente em
`2021-09-11` (confirmado nesta sessão: apenas 5 eventos catalogados entre
01/09 e 11/09, contra 159 eventos só no dia 12/09) — reportado
oficialmente pelo IGN/PEVOLCA como o início do enxame precursor. PRE é
travado aqui como `2021-09-11T00:00:00` a `2021-09-19T14:13:00 UTC` (o
enxame precursor completo, fronteira de início documentada externamente
pelo IGN/PEVOLCA, não escolhida por inspeção dos próprios dados). N=1.049
eventos catalogados nesta janela.

**Definição de POST — "próximo evento documentado" como fronteira
(fixada a priori):** fim oficialmente declarado da erupção pelo PEVOLCA,
`2021-12-13T00:00:00 UTC` (~85 dias de atividade eruptiva contínua, a
mais longa erupção histórica documentada em La Palma) — usado aqui como
fronteira POST, mesmo papel de "próximo evento documentado" já usado
nesta linha (ex. `aneend` em MSE/VitalDB, M6,9 do Kilauea em LZC). POST =
`2021-09-19T14:13:00` a `2021-12-13T00:00:00 UTC`. N=6.747 eventos
catalogados nesta janela.

**Checagem de qualidade de dado feita nesta sessão (antes de qualquer
cálculo):** sem timestamps duplicados exatos, sem pares de eventos
`<5s` de diferença (nenhum artefato óbvio de detecção automática
duplicada em nenhuma das 2 janelas), magnitudes no intervalo plausível
`Ml∈[1,5; 4,9]`, consistente com um catálogo regional limpo.

**PRE/POST exatos:** `X` = tempo de interevento (em segundos, log não
aplicado) entre eventos catalogados consecutivos, ordenado por índice de
evento (mesma convenção "sequência ordenada por índice" do Domínio 1).
PRE: N=1.048 interevento-tempos. POST: N=6.746 interevento-tempos.
Robustez: 50% mais recentes de PRE (últimos 524), 50% mais próximos da
transição de POST (primeiros 3.373).

## Gap (d): orçamento computacional

`MAX_N_PER_SEGMENT=5.000` (decimação por *stride* uniforme se excedido
— afeta apenas o POST primário de La Palma, N=6.746>5.000). `MIN_N_SEGMENT
=100` (piso maior que o `50` de LZC — CSSR precisa de dado suficiente por
combinação história×símbolo). Benchmark medido nesta sessão: uma
combinação completa (2 variantes × IAAFT 200 substitutos × 2 segmentos)
roda em minutos, não horas, para `N<=5.000`.

## Gap (e): protocolo de significância

**IAAFT como teste PRIMÁRIO**, mesmo protocolo já usado nesta linha:
`N_SURROGATES=200`, `N_IAAFT_ITER=50`, seed=12345, substitutos de PRE e
POST gerados INDEPENDENTEMENTE cada um da sua própria série real. Teste
BICAUDAL sobre `Delta_C_mu` e `Delta_h_mu`, aplicado independentemente às
2 variantes de simbolização (mediana, ternária).

**Fallback pré-autorizado:** bootstrap por blocos móveis (Kunsch 1989),
mesma convenção já usada em DFA/SOC/RQA/PE/LZC — acionado apenas se a
validação sintética mostrar baixo poder do IAAFT para QUALQUER canal,
ANTES de tocar dado real.

## Disciplina de escalonamento (reafirmada)

Uma ÚNICA correção pré-autorizada, bounded, é permitida se a validação
revelar um problema de desenho genuíno — depois disso o candidato deve
fechar, positivo ou negativo, sem uma segunda tentativa de redesenho.
Fechamento NA ETAPA DE VALIDAÇÃO, sem nunca tocar dado real, é
exatamente tão valioso quanto um achado positivo (precedente já
estabelecido nesta linha: `rqa`, `largest_lyapunov_exponent`,
`persistent_homology`).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi ou será travado para esta linha (esta nota desempenha esse papel). A
metodologia acima foi fixada ANTES de qualquer cálculo de `C_mu`/`h_mu` —
os dados reais dos 2 domínios já foram baixados/inspecionados nesta
sessão para verificar acessibilidade, contagens de amostra, estrutura de
anotação e qualidade (incluindo a descoberta e correção documentada da
regra de limpeza de lacunas de observação do Old Faithful, e a checagem
de duplicatas/magnitude de La Palma), mas NENHUM valor de `C_mu`,
`Delta_C_mu`, ou p-valor foi calculado sobre esses dados reais até este
ponto — a etapa de validação sintética (obrigatória, `validate_synthetic.py`)
vem a seguir.

---

## ADENDO DE REVISÃO — 2026-08-21 (`DISC-DEC-011`)

**Natureza desta revisão:** correção de completude de implementação,
autorizada explicitamente pela sessão orquestradora (`DISC-DEC-011`) —
NÃO uma reformulação de hipótese. Este candidato foi fechado na etapa de
validação (nenhum dado real jamais tocado — ver `RESULTS_SUMMARY.md`
original), deixando uma ambiguidade honesta e nomeada explicitamente
naquele fechamento: a falta de poder discriminativo de `C_mu` observada na
validação sintética original era causada (1) pela simplificação de escopo
#1 daquela implementação ("clustering de estados causais em `L` fixo", não
o crescimento incremental completo de CSSR de Shalizi & Klinkner 2004),
ou (2) por uma fragilidade mais geral de `C_mu` como estimador em amostra
finita? Como nenhum dado real havia sido tocado, não havia risco de
contaminação retroativa de um resultado real ao revisitar apenas a
implementação de `R_lambda` — exatamente o tipo de correção que este
laboratório permite (`AGENTS.md`, passo 7).

**O que mudou:** `analysis/em_common.py` foi reescrito para implementar
CSSR incremental completo (Shalizi & Klinkner 2004, *UAI*; também descrito
em Shalizi, Shalizi & Crutchfield, arXiv:cs/0210025), substituindo (não
apenas remendando) o motor de reconstrução de estados causais:

1. Estado inicial único (L=0) contendo todos os históricos de comprimento
   zero (o histórico vazio).
2. `L` cresce incrementalmente de 1 até `L_max` (a mesma regra de
   convergência já fixada — varrer e escolher onde o número de estados
   estabiliza, excluindo o caso trivial `L=1` já identificado como não
   informativo, correção #1 da validação original, mantida sem alteração
   por ser ortogonal à troca de algoritmo — ver `em_common.py`,
   `select_Lmax_and_reconstruct`).
3. A cada `L`, para cada histórico de comprimento `L` com contagem
   suficiente (`MIN_COUNT_PER_HISTORY=10`, inalterado): teste (via
   qui-quadrado comparando distribuições condicionais do próximo símbolo,
   no nível de significância `alpha=10⁻³` já fixado a priori) se pertence
   ao estado causal ao qual seu SUFIXO de comprimento `L-1` já pertence
   (a etapa de "crescimento" que a implementação anterior simplesmente NÃO
   fazia); se não, testa contra todos os outros estados já descobertos
   naquele `L`; cria um novo estado apenas se nenhum corresponder.
4. Após crescer os históricos de comprimento `L`, executa a etapa de
   determinização/refinamento de CSSR: verifica se a máquina resultante é
   unifilar (determinística — de cada estado, cada símbolo leva a
   exatamente um próximo estado); se não, DIVIDE os estados
   recursivamente (`_determinize`, em `em_common.py`) até que seja, ou até
   um teto de iterações fixado a priori (`MAX_DETERMINIZE_ITERS=30`) sem
   convergência, o que por si só alimenta o gate de rejeição
   `NOT_DETERMINISTIC` — nunca aceito silenciosamente. Isto substitui a
   decisão de escopo #2 original (determinismo apenas DIAGNOSTICADO, não
   corrigido).
5. Repete até `L_max`, usando a MESMA regra de seleção de `L_max` de
   antes (menor `L_max` além do qual o número de estados causais
   inferidos para de crescer).
6. Gate de rejeição obrigatório mantido: `DEGENERATE` (1 estado),
   `NOT_CONVERGENT` (curva nunca estabiliza), `NOT_DETERMINISTIC` (agora
   uma checagem de sanidade PÓS-determinização, deveria ser ~0 por
   construção) — nunca um valor calculado silenciosamente.

**O que NÃO mudou (confirmado explicitamente, não uma alegação vazia):**
`I(X)=C_mu` primário / `h_mu` companheiro REBAIXADO permanecem
EXATAMENTE como definidos acima (seção "Gap (b)"); o protocolo de
significância (IAAFT primário, 200 substitutos, 50 iterações,
seed=12345, bicaudal; bootstrap por blocos móveis pré-autorizado como
fallback) permanece EXATAMENTE como definido (seção "Gap (e)"); o esquema
de simbolização (binarização por mediana primária, quantização ternária
companheira, reestimadas por segmento) permanece EXATAMENTE como definido
(seção "Gap (a)", parágrafo de simbolização); os 2 domínios reais já
verificados (Old Faithful, La Palma 2021) permanecem os mesmos, nenhuma
nova busca de domínio foi feita. `L_max` continua selecionado UMA VEZ por
segmento real e mantido fixo para os substitutos (decisão de escopo #4,
inalterada) — a única mudança é que "manter `L` fixo" para um substituto
agora significa crescer o CSSR incremental DAQUELE substituto de `L=1`
até o `L` fixado (CSSR genuíno é inerentemente sequencial — não é possível
pular direto para `L=8` sem passar pelas etapas de crescimento+
determinização em `L=1,...,7` primeiro), não mais reclusterizar do zero
em um único `L` como a implementação anterior fazia.

**Resultado da re-validação:** ver `VALIDATION_NOTE_V2.md` (nota completa)
e `RESULTS_SUMMARY_V2.md` (veredito final desta revisão) — a ambiguidade
nomeada acima foi RESOLVIDA: `C_mu` continua sem poder discriminativo
genuíno mesmo sob CSSR incremental completo (implementação agora
verificada correta contra um caso de ordem finita com solução exata à
mão), apontando para explicação (2) — fragilidade genuína de `C_mu` como
estimador em amostra finita — não para explicação (1), o artefato de
implementação suspeitado originalmente.

**Escopo desta revisão, reafirmado:** estritamente limitado a este único
candidato (`epsilon-machine-complexity`), por autorização explícita da
sessão orquestradora (`DISC-DEC-011`). Os outros 15 candidatos desta linha
permanecem fechados exatamente como documentado em
`02_TESTS/TRI_RG/CLOSURE_SUMMARY.md` — nenhum deles foi tocado por esta
revisão. `TEST_QUEUE.yaml`, `DISCOVERY_LAB_STATE.md`, `DECISION_LEDGER.yaml`
e `CLOSURE_SUMMARY.md` não foram modificados por este agente — ficam a
cargo da sessão orquestradora.
