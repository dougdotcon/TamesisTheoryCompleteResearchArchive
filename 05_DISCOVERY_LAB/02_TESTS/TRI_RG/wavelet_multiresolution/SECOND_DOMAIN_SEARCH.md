# Busca de segundo domínio para `wavelet-multiresolution-scaling`

**Data:** 2026-08-14. Contexto: a Fase 0 (`02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md`)
deixou o candidato `wavelet-multiresolution-scaling` (WTMM / expoente de Hurst
generalizado / largura do espectro multifractal `Δα`) com apenas 1 domínio
robusto o suficiente — sismologia, mainshock de Tohoku 2011, rótulo USGS/GCMT
externo e não-circular. Fisiologia (CHF vs. NSR) é comparação estática de
classe, não transição temporal; tráfego de rede (Bellcore) tem rótulo
fraco/autorreferencial. Usuário pediu para buscar um segundo domínio.

Três agentes independentes investigaram, em paralelo, três candidatos
diferentes, cada um com instrução de verificar dado real (baixar/inspecionar,
nunca apenas citar).

## Resultado: 1 domínio forte encontrado, 1 domínio utilizável com ressalvas, 1 descartado

### ✅ EEG de crise epiléptica (CHB-MIT, PhysioNet) — recomendado como segundo domínio

Banco de dados aberto (Open Data Commons Attribution License, sem
login/conta), registros de EEG pediátrico de escalpo com anotações
clínicas de onset/offset de crise. Verificação real nesta sessão:
`chb01_03.edf` baixado por completo (42.399.744 bytes, HTTP 200),
parseado com um parser EDF escrito do zero (biblioteca `pyedflib`/`mne`
indisponíveis no ambiente) — contagem de bytes bateu exatamente com a
estrutura declarada do formato (6144 bytes de cabeçalho + 3600 registros
× 11776 bytes), forte evidência de extração correta. Rótulo de transição:
`chb01-summary.txt` (arquivo de resumo clínico oficial do banco) declara
onset em 2996s e fim em 3036s dentro do registro contínuo do mesmo
paciente — mesma estrutura de rótulo (externo, não-circular, timestamp
preciso dentro de um registro contínuo) já usada com sucesso em
sismologia (Tohoku/USGS-GCMT) e no domínio cardíaco de
`critical-slowing-down` (PhysioNet SDDB/onset de FV).

Série extraída: canal `FP1-F7`, 256 Hz, janela de ±5 min ao redor da
crise (163.840 amostras), salva em
`wavelet_multiresolution/data/eeg_seizure_prepared.json`.

**Ressalvas honestas:** só 1 crise/1 paciente verificada nesta sessão
(há 182 crises documentadas em 22 pacientes no banco — replicação/
robustez ainda pendente); EEG de escalpo é mais suscetível a artefato de
movimento/piscadas que ECG ou sismômetro (não filtrado nesta extração);
a janela de ±5 min foi uma escolha razoável do agente, não prescrita
pela fonte — precisa ser fixada explicitamente (de preferência como
fração do registro disponível, mesma convenção usada em
`critical-slowing-down`) antes de qualquer pré-registro.

### ⚠️ Turbulência de plasma no vento solar (NASA OMNI + catálogo CfA de choques interplanetários) — domínio alternativo válido, mas não é o domínio histórico do WTMM

A rota mais direta (turbulência hidrodinâmica clássica — túnel de vento,
hot-wire, PIV, o domínio original de Muzy/Bacry/Arneodo 1991) **continua
não encontrada como série livremente baixável sem conta/login/token**
nesta sessão — mesma lacuna já documentada na Fase 0, confirmada de novo
com uma busca honesta e mais extensa (Zenodo, PANGAEA, JHTDB — token de
teste público existe mas o serviço retornou HTTP 404 em todas as rotas
tentadas).

Como alternativa dentro do mesmo campo mais amplo de "turbulência"
(turbulência MHD/de plasma, precedente real na literatura — Bruno &
Carbone 2013), o agente verificou de ponta a ponta: catálogo
independente de choques interplanetários (CfA/Harvard, Denny M. Oliveira,
Zenodo DOI `10.5281/zenodo.15121223`, 167.512 bytes, 650 eventos
1995–2024) cruzado com a série de vento solar de alta resolução (NASA
SPDF OMNI 1-min, 13.392.000 bytes, outubro/2024 completo). Transição real
confirmada NUMERICAMENTE (não apenas citada): velocidade do vento solar
salta de ~400 para ~729 km/s, `|B|` de ~7,7 para ~30,5 nT, no choque de
2024-10-10 14:51 UT — consistente com a tempestade geomagnética G4/G5
documentada de forma independente.

**Ressalvas honestas:** cadência de 1 minuto é muito mais grosseira que
hot-wire de laboratório (kHz), restringe a faixa de escalas úteis para
WTMM; ~20% dos pontos de velocidade/densidade estão faltando (fill
values reais do OMNI, não interpolados); e — mais importante — este é um
domínio FISICAMENTE DIFERENTE do domínio histórico-bandeira do método
(turbulência MHD de plasma vs. turbulência hidrodinâmica de túnel de
vento). Isso precisa ser dito explicitamente em qualquer pré-registro
que o use, não apresentado como "o mesmo domínio de Muzy/Bacry/Arneodo".

Série salva em `wavelet_multiresolution/data/turbulence_prepared.json`.

### ❌ MAWI/MAWILab (tráfego de rede rotulado) — descartado

Dado real baixado e verificado de ponta a ponta (índice MAWI, XML de
anomalias do MAWILab, pcap completo de 15 min / ~98,8 MB parseado do
zero, contagens de pacote/bytes batendo exatamente com os metadados
publicados). O rótulo é genuíno e não-circular PARA O FLUXO ISOLADO (ex.
ping flood de um único IP, 477 pacotes concentrados exatamente na janela
anotada). Mas **falha estruturalmente** como domínio equivalente a
Tohoku: o MAWILab só rotula capturas diárias fixas de 15 minutos (nunca
as capturas contínuas mais longas que o MAWI também hospeda) — isso
força uma escolha ruim: eventos pequenos o bastante para caber na janela
de 15 min ficam invisíveis no sinal agregado (testado: ping flood
indistinguível do ruído de fundo, z-score alto em só 2 de 8997 bins);
eventos grandes o bastante para aparecer no agregado (ex. surto do worm
Sasser) tendem a preencher quase toda a janela de 15 min, sem baseline
"antes" no mesmo registro. Adicionalmente, o MAWILab foi oficialmente
descontinuado pelos próprios mantenedores em dezembro/2024. Nenhum
arquivo de dado preparado foi salvo (resultado negativo, conforme
instruído).

## Recomendação

Usar **EEG de crise epiléptica (CHB-MIT)** como o segundo domínio de
`wavelet-multiresolution-scaling`, junto com sismologia (Tohoku) já
verificado na Fase 0. Turbulência de plasma no vento solar fica como um
terceiro domínio de apoio válido — útil para uma checagem de robustez
extra, mas com a ressalva de domínio explicitada. Antes de qualquer
`PREREGISTRATION.md`, ainda falta: (a) fixar a regra de janela para o
domínio de EEG (mesma convenção de fração-do-registro já usada em
`critical-slowing-down`, ou uma nova regra declarada e aplicada
identicamente aos 2-3 domínios); (b) rodar o método WTMM/wavelet-leader
real (nenhum cálculo de `h(q)`/`Δα` foi feito ainda em nenhum domínio
desta linha — só acesso e rótulo foram verificados até agora); (c)
desenhar o protocolo de dados substitutos (IAAFT) exigido pela própria
Fase 0 para descartar multifractalidade espúria.
