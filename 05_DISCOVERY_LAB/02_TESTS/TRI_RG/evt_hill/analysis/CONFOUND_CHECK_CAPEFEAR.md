# Checagem de confundidor pré-declarada — Lock 1 (Gap (d), acionada)

**Por que esta checagem foi acionada:** `METHODOLOGY_NOTE.md` Gap (d)
exige esta checagem "SE `xi_Hill`/`xi_MLE` mostrar mudança
significativa neste domínio, ANTES de aceitar o achado como genuíno". No
domínio Cape Fear, o canal PRIMÁRIO (`xi_Hill`) NÃO cruza `p<0,05` em
nenhuma das duas variantes de janela (`p=0,185` primária, `p=0,22`
robustez — ver `RESULTS_SUMMARY.md`). O canal COMPANHEIRO (`xi_MLE`)
cruza em UMA das duas variantes: `p=0,09` (primária, não significativo)
e **`p=0,025` (robustez, significativo)**. Como pelo menos um `p<0,05`
apareceu em pelo menos uma combinação canal×variante, esta checagem é
acionada por completude e rigor, mesmo o achado sendo restrito ao canal
companheiro em apenas uma das duas variantes de janela — não escondida
nem descartada sem investigação só porque o canal primário ficou limpo.

## O que está por trás do número (diagnóstico primeiro, antes de buscar registros externos)

`xi_MLE` do POST é fortemente NEGATIVO (`c=-1,063`, `scale=0,106`,
IDÊNTICO nas duas variantes de janela — o ajuste GPD usa o MESMO `k*`
(63-69 excedências) e o MESMO limiar `u=30,58 ft`, que por acaso cai
bem perto do pico observado da cheia). Um `xi_MLE` negativo implica
suporte superior FINITO na GPD ajustada (`u + scale/(-c) = 30,58 +
0,100 = 30,68 ft`) — que bate quase exatamente com a altura máxima
REALMENTE observada na série (`~30,68 ft`, platô de crista entre
19-23/09/2018, ver `data/PROVENANCE_CAPEFEAR.md`). Isso é o padrão
ESPERADO de uma cheia fluvial que atinge uma crista real e physicamente
limitada (o rio sobe, se estabiliza por alguns dias perto do pico, e
recessa) — não o padrão de uma cauda de lei de potência genuína. `xi_Hill`
(canal primário) concorda qualitativamente: cai para ~0 (0,0015-0,0017),
i.e., também indica cauda LEVE/limitada em vez de mais pesada — os dois
canais discordam em MAGNITUDE (esperado, `xi_MLE` de MLE de GPD é
conhecidamente instável com poucas excedências perto de um suporte
limitado, mesmo padrão de instabilidade já documentado na validação
sintética para caudas de convergência lenta) mas concordam na DIREÇÃO
qualitativa (POST não é mais pesado que PRE, é mais LEVE/limitado).
**Isso já é evidência a priori contra uma explicação de "mudança de
regime hidrológico para cauda mais pesada" — e a favor de um efeito
mecânico de crista limitada, exatamente o tipo de coisa que a checagem
de confundidor da comporta deveria isolar.**

## Busca por registros de operação da comporta (Lock and Dam 1)

Duas buscas web realizadas (2026-08-19):

1. Confirma que o Lock and Dam 1 (estrutura de 1915, modificada em 1934,
   elevação de 11 pés) ficou **COMPLETAMENTE SUBMERSO** durante o
   Florence — DVIDS (serviço de imagens do Departamento de Defesa dos
   EUA) documenta fotograficamente a estrutura submersa.
2. Reportagem local (Port City Daily, dez/2018) sobre o futuro da gestão
   da represa cita que, DIAS depois da tempestade, "no one was around to
   monitor Lock and Dam No. 1 as the river was rising" — ninguém estava
   monitorando ativamente a comporta enquanto o rio ainda subia.
3. Nenhum registro público específico de ABERTURA/FECHAMENTO de comporta
   com data/hora exata para setembro/2018 foi encontrado nesta busca —
   o Corpo de Engenheiros do Exército dos EUA (USACE), operador da
   estrutura, não publica log minuto-a-minuto de operação de comporta
   publicamente acessível por busca web comum.

## Veredito honesto desta checagem

**Não foi possível obter um log operacional completo e definitivo da
comporta** (limitação de dado público, declarada explicitamente, não
escondida) — mas a evidência circunstancial disponível PESA CONTRA a
hipótese de confundidor mecânico de operação de comporta como explicação
do achado:

1. A estrutura ficou COMPLETAMENTE SUBMERSA durante o pico da cheia —
   uma vez submersa, a comporta deixa de ser o fator hidraulicamente
   dominante (o perfil de superfície da água passa a ser governado pelo
   escoamento livre de um rio em cheia extrema, não pela posição da
   comporta).
2. Não havia monitoramento ativo/operação deliberada da comporta durante
   o período crítico (segundo a reportagem citada) — consistente com
   "sem controle ativo" em vez de "mudança de operação deliberada", o
   TIPO específico de confundidor que Gap (d) nomeia (mudança
   MECÂNICA/OPERACIONAL, não ausência de operação).
3. O padrão observado (platô de crista limitada, `xi_MLE` negativo com
   suporte finito bem próximo do pico real observado) é EXATAMENTE o que
   a física de uma cheia fluvial real produziria de forma independente
   de qualquer comporta — nenhum mecanismo de comporta é necessário para
   explicar um rio que sobe, estabiliza perto do pico por alguns dias, e
   recessa.
4. Todos os qualificadores USGS nas leituras do pico são `'A'`
   (Approved) — sem sinalização de problema de equipamento/sensor.

**Conclusão: o achado (limitado ao canal companheiro `xi_MLE`, em
apenas uma das duas variantes de janela, e já explicado por um efeito
físico plausível e parcimonioso de crista de cheia limitada) NÃO é
reportado como "confirmadamente causado por operação de comporta" — mas
TAMBÉM não é reportado como um invariante `evt-hill` genuíno, porque
(a) o canal primário `xi_Hill` não é significativo em nenhuma variante,
(b) o padrão observado em ambos os canais é mais bem explicado por um
platô físico de crista de cheia limitada que por uma mudança genuína de
índice de cauda, e (c) a instabilidade de `xi_MLE` perto de um suporte
efetivamente limitado já era um modo de falha conhecido e documentado
na validação sintética (`VALIDATION_NOTE.md` seção 1) antes mesmo de
qualquer dado real ser tocado.** Ver `RESULTS_SUMMARY.md` para o
veredito consolidado do domínio.
