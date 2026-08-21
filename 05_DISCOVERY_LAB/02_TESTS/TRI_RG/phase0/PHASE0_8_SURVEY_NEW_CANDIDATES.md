# Fase 0.8 — nova busca de candidatos para `DISC-TRI-RG-001` (2026-08-20)

Usuário pediu para formalizar como busca dedicada duas ideias discutidas em
conversa (reformulações da premissa "tudo no universo é computacional, o
princípio básico é adicionar complexidade construindo um novo sistema em
prol de economia de energia", traduzida para hipóteses falsificáveis a
partir da lição honesta extraída dos 14 candidatos anteriores: quase todos
colapsam em ~4 eixos matemáticos latentes já testados repetidamente
— ver ranking desta seção abaixo). 2 agentes independentes em paralelo
investigaram 2 candidatos genuinamente novos, cada um com instrução
explícita de verificar dado real por download direto e checar
identificabilidade contra TODOS os 14 candidatos já fechados nesta linha.

Isto reabre a linha na prática logo após a pausa de `DISC-DEC-009`
(5ª vez que isso acontece nesta linha) — `status` permanece
`CANDIDATE_FORMULATING`, nenhum novo `DISC-DEC-00N` é registrado agora; o
registro formal da reabertura fica para quando a rodada atual for
encerrada, mesmo padrão já seguido em todas as reaberturas anteriores.

**Resultado: 2 `viable=true` — os dois primeiros candidatos desta linha
inteira que NÃO caem em nenhum dos 4 eixos matemáticos latentes já
identificados (persistência/taxa-de-entropia; taxa de relaxação local;
densidade de recorrência via embedding; estatística de cauda).**

## 1. Complexidade estatística de ε-machines (`C_mu`, mecânica computacional) — `viable: true`

`R_lambda`: reconstrução de estados causais via CSSR (Shalizi & Klinkner
2004) como primário — `L_max` escolhido por convergência do número de
estados inferidos (regra análoga a BIC/AIC, não visual), `alpha=10⁻³`
fixado a priori (convenção da literatura) — mais Inferência Estrutural
Bayesiana (Strelioff & Crutchfield 2014) como checagem companheira
restrita ao canal binarizado/ternário (alfabeto pequeno, regime onde BSI é
tratável). Simbolização reaproveitada de `lempel_ziv_complexity` (mediana/
ternário) para domínios contínuos; DNA usa alfabeto nativo de 4 símbolos,
sem escolha de simbolização.

`I(X)`: `C_mu` (entropia de Shannon da distribuição de estados causais,
primário) + `h_mu` (taxa de entropia do mesmo autômato reconstruído,
companheiro/diagnóstico — REBAIXADO a priori, esperado redundante com a
família taxa-de-entropia já testada 7+ vezes nesta linha).

**Risco de identificabilidade central, investigado a fundo (não
superficialmente):** o risco óbvio era `C_mu` ser apenas mais uma
reformulação do `C_JS` (entropia de permutação, candidato #8, já fechado
negativo 8/8). Investigação de literatura confirma que são objetos
DIFERENTES, não apenas nominalmente distintos: Feldman & Crutchfield 1998
é uma crítica DIRETA, pelo próprio grupo de Crutchfield, à família
LMC/MPR/Rosso da qual `C_JS` descende — mostram que essa família não é
nem intensiva nem extensiva e colapsa a uma função trivial da densidade de
entropia em casos analiticamente tratáveis. `C_mu` foi construído
historicamente como a alternativa rigorosamente fundamentada a essa
heurística. Crutchfield & Feldman 2003 provam `(h_mu,C_mu)` como par
formalmente independente, com um limite derivado (`E<=C_mu`) que não tem
análogo para `C_JS`. **Achado honesto que não pode ser escondido:** os
dois pertencem à mesma FAMÍLIA ESTRATÉGICA de medidas de complexidade em
forma de U-invertido, desenhadas para o mesmo tipo de sinal qualitativo —
se `C_mu` também vier negativo, isso deve ser lido como evidência mais
forte que um fechamento comum: um sinal de que toda a ESTRATÉGIA de
complexidade-em-pico pode não carregar sinal cross-domain nas transições
já testadas nesta linha, não apenas mais uma fórmula específica que falhou.

**2 domínios novos verificados por download real:** (a) intervalos de
erupção do gêiser Old Faithful (GeyserTimes.org API, alongamento
documentado de intervalo por seca regional entre 1997 e 2003, externo à
própria estatística); (b) genoma completo de *E. coli* K-12 MG1655 (NCBI,
4.641.652 pb reais, transição origem/terminus de replicação via GC-skew,
batendo em ~4kb com a literatura — mas domínio ESPACIAL, não temporal,
extensão da convenção desta linha que precisa de aval explícito antes de
`METHODOLOGY_NOTE.md`).

## 2. Transferência de entropia / fluxo de informação direcionado — `viable: true`

`R_lambda`: embedding de história própria via minimização de erro de
predição local (Ragwitz & Kantz 2002 — critério estruturalmente
DIFERENTE do FNN que já travou RQA/LLE), estimador KSG (Kraskov,
Stögbauer & Grassberger 2004, k-vizinhos-mais-próximos, `k_NN=4` fixo,
sem escolha de largura de bin), implementação de referência mantida
(IDTxl/TRENTOOL) para evitar risco de bug de implementação. Escolha
deliberada do ramo da literatura que evita o modo de falha dominante
desta linha (não-convergência de FNN).

`I(X)`: `TE_net = TE(X->Y) - TE(Y->X)` (fluxo direcionado líquido,
primário) + `TE_sum` (acoplamento total bidirecional, companheiro) +
Transferência de Entropia Simbólica (Staniek & Lehnertz 2008, reaproveita
o embedding ordinal já auditado de `permutation_entropy`) como estimador
de robustez.

**Diferença estrutural central desta candidatura:** é a PRIMEIRA
candidatura bivariada/direcional de toda a linha — os 14 anteriores são
todos estatísticas univariadas de um único canal. Risco de redundância
matemática: BAIXO (nenhuma identidade algébrica encontrada com nenhum dos
14, ao contrário do colapso MF-DFA/wavelet ou DMD/critical-slowing-down
já documentados). **Riscos práticos nomeados honestamente:** viés de
amostra finita do estimador KSG (mitigado pois `Delta=POST-PRE` cancela
viés aproximadamente constante); não-estacionariedade dentro das janelas
PRE/POST (risco real, análogo ao que já fechou `kramers_moyal`/afetou
`dmd_koopman`); desenho de nulo substituto para acoplamento é território
genuinamente novo nesta linha — substituto de deslocamento circular
(Quian Quiroga et al. 2002) pré-autorizado como companheiro do IAAFT
padrão; crítica de confundidor comum a TE (James, Barnett & Crutchfield
2016) — risco real e nomeado para os 2 domínios especificamente, com
mitigação pré-declarada (não achado post-hoc).

**2 domínios verificados por download real:** (a) CHB-MIT EEG
multi-eletrodo (`chb01_03.edf`, 23 canais simultâneos reais, convulsão
documentada em 2996-3036s) — domínio já usado nesta linha, mas eixo de
acoplamento entre eletrodos nunca testado, reuso do tipo explicitamente
pré-autorizado; risco de condução de volume nomeado e parcialmente
mitigado (montagem bipolar); (b) par de terremotos de Kahramanmaraş,
Turquia, 06/02/2023 (M7,8 seguido por M7,5 ~9h depois, IRIS rede `KO`,
estações `GAZ`/`BNN` reais, formas de onda decodificadas, salto de
amplitude batendo com o segundo-origem do USGS) — domínio genuinamente
novo; risco de confundidor de fonte comum (mesma onda sísmica atingindo
2 estações) nomeado e mitigado a priori (usar envelope RMS/taxa de
eventos em janelas de minutos, não forma de onda bruta, evitando o
mesmo modo de falha que já enganou `dmd_koopman` em Kilauea).

**Direção pré-declarada, não post-hoc:** literatura de sincronização
ictal prevê aumento de acoplamento direcionado (domínio EEG); literatura
de transferência de tensão sísmica prevê aumento de acoplamento
inter-estação em sequências de réplicas (domínio sísmico) — ambas
testadas bicaudalmente pelo protocolo IAAFT padrão desta linha, não
apenas na direção prevista.

## Ranking honesto (não travado — decisão de qual perseguir fica com o usuário)

1. **Transferência de entropia** — estruturalmente mais distinta de toda
   a linha (primeira candidatura bivariada/direcional), `R_lambda`
   deliberadamente escolhido para evitar o modo de falha dominante desta
   linha (FNN), 2 domínios fortes e verificados, riscos práticos reais
   mas do tipo esperado/administrável (não uma identidade matemática
   fatal). Fraqueza: introduz um desenho de nulo substituto genuinamente
   novo (deslocamento circular) que nunca foi testado nesta linha.
2. **Complexidade estatística de ε-machines** — matematicamente provado
   distinto de `C_JS` (não apenas nominalmente), mas compartilha a MESMA
   estratégia de detecção (complexidade em pico) que já falhou 8/8 sob
   esse nome — um segundo fechamento negativo aqui teria peso
   epistemológico maior que um fechamento comum. Domínio do DNA precisa
   de aval explícito por ser espacial, não temporal.

Nenhum candidato foi travado. `DISC-TRI-RG-001` permanece
`CANDIDATE_FORMULATING`. Toda a infraestrutura desta busca (domínios
verificados, achados de identificabilidade) fica commitada e disponível
para retomada futura.
