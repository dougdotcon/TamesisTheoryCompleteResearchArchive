# Operacionalização — DISC-COGNITIVE-EEG-SPECTRAL-001

**Autorizado por:** `DISC-DEC-025` (`00_GOVERNANCE/DECISION_LEDGER.yaml`).
**Escopo:** *apenas* a etapa de operacionalização — definir `I(X)`, `R_λ`/
pré-processamento, modelo concorrente, regra de decisão a priori, poder
estatístico a priori, e verificar acesso real aos dados por download.
**Explicitamente FORA de escopo aqui** (proibido por `DISC-DEC-025` e por
este próprio documento): computar `I(X)` sobre qualquer dado real, escrever
ou travar `PREREGISTRATION.md`, ou fazer/implicar qualquer alegação
médica/diagnóstica/clínica. Este é um teste de uma alegação matemática de
teoria espectral de grafos contra estatísticas de sinal EEG — não é, e não
deve ser lido como, uma ferramenta de diagnóstico.
**Fonte da alegação:** `90_LEGACY/08_COGNITIVE_TOPOLOGY/
TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/PAPER_B_SPECTRAL_SIGNATURES.md`
(doravante `PAPER_B`), identificada por `DISC-ARCHIVE-PHASE0-SURVEY-001`
(`02_TESTS/ARCHIVE_PHASE0_SURVEY/SURVEY.md`, Bloco 7.1).

---

## 0. Como ler este documento

Cada item abaixo (1–6) corresponde a um dos seis itens do mandato da sessão
orquestradora. Todas as citações foram verificadas nesta sessão por fetch
direto (PubMed/NCBI eutils, arXiv/ar5iv, ou a API pública do Figshare/IEEE
DataPort) — nenhuma foi assumida de memória, conforme exigido por
`00_GOVERNANCE/AGENTS.md` ("Proibições"). Os PMIDs/DOIs citados podem ser
conferidos nos mesmos endpoints usados aqui
(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<PMID>&rettype=abstract&retmode=text`).

---

## 1. Operacionalização de `I(X)` — uma fórmula fechada

### 1.1 Diagnóstico do problema no texto-fonte

`PAPER_B` §3 descreve três regimes patológicos em linguagem qualitativa,
sem nenhum limiar numérico:

- **Depressão ("Entropic Trap", `PAPER_B:48-61`):** "Collapse of High
  Frequencies", "Dominance of Low Eigenvalues... spectrum compressed
  towards λ→0", "Low complexity: Reduced Lempel-Ziv complexity".
- **Ansiedade ("Oscillatory Chaos", `PAPER_B:63-74`):** "High-Frequency
  Noise... not phase-locked", "High Entropy. But 'bad' entropy
  (randomness), not structural complexity".
- **Classe metabólica/viscosa ("The Viscous Medium", `PAPER_B:76-86`):**
  "Flattening of the Power Spectral Density (PSD) curve (1/f^α, where α
  increases)".

Nenhuma dessas três frases é, como está escrita, uma fórmula computável.
Além disso, a frase da classe 3 é **internamente inconsistente** tal como
escrita: em um modelo `PSD(f) ∝ 1/f^α`, **aumentar** `α` torna a curva
**mais** inclinada (mais energia concentrada em baixa frequência, queda
mais rápida em alta frequência) — o oposto de "achatamento". Esta
inconsistência não é resolvida aqui por adivinhação; é registrada como uma
ambiguidade real do texto-fonte e tratada explicitamente na seção 1.3
abaixo, com a convenção adotada declarada e justificada, não escondida.

### 1.2 Fórmula primária escolhida: Entropia Espectral de Shannon normalizada

**Justificativa da escolha (por que este e não outro):** o próprio "Rosetta
Stone" de `PAPER_B` (§2.1, tabela `PAPER_B:34-40`) já estabelece a ponte:
autovalor baixo do Laplaciano ↔ bandas Delta/Theta; autovalor alto ↔
Beta/Gamma. Ou seja, o próprio artigo trata a densidade espectral de
potência (PSD) do EEG como a observável direta que instancia a "densidade
espectral de autovalores" do Laplaciano do conectoma — **não exige**,
para ser testável, a construção independente de um grafo de conectividade
(ver §2.6 sobre por que essa etapa extra é deliberadamente evitada como
observável primário). Sob essa ponte já fornecida pelo próprio artigo,
"dominância de autovalores baixos" e "alta entropia ruim de alta
frequência" são, literalmente, afirmações sobre a **forma da distribuição
de potência espectral normalizada** — exatamente o que a entropia de
Shannon aplicada à PSD normalizada mede, por construção, sem parâmetro
livre extra.

O método tem precedente estabelecido e citável na literatura de EEG:
Inouye et al. (1991) introduziram a entropia da PSD como um "índice de
irregularidade" do EEG (Inouye, T., Shinosaki, K., Sakamoto, H. et al.
(1991). "Quantification of EEG irregularity by use of the entropy of the
power spectrum." *Electroencephalography and Clinical Neurophysiology*,
79(3), 204–210. PMID 1714811); Vakkuri et al. (2004) formalizaram uma
versão normalizada, com faixa de frequência fixa e normalização por
`log(N)` (a "State Entropy" usada em monitoramento clínico de profundidade
anestésica) — Vakkuri, A., Yli-Hankala, A., Talja, P. et al. (2004).
"Time-frequency balanced spectral entropy as a measure of anesthetic drug
effect in central nervous system during sevoflurane, propofol, and
thiopental anesthesia." *Acta Anaesthesiologica Scandinavica*, 48(2),
145–153. PMID 14995935. É a mesma família estatística (entropia de sinal
fisiológico) já usada em `DISC-TRI-RG-001` (`02_TESTS/TRI_RG/
permutation_entropy/`) — mas o objeto matemático é diferente (entropia da
PSD normalizada, não entropia de permutação de Bandt-Pompe sobre a série
temporal), então não há redundância de método, apenas continuidade de
família estatística já auditada nesta trilha.

**Por que não Lempel-Ziv (LZC), citado literalmente no texto-fonte
`PAPER_B:59`?** Decisão deliberada: LZC exige binarizar o sinal (ex.:
mediana ou média como limiar) antes de contar padrões — um parâmetro livre
adicional não mandatado pelo texto-fonte, exatamente o tipo de escolha
arbitrária que este laboratório evita introduzir (`AGENTS.md`: "não
inventar uma fórmula ad hoc"). A entropia espectral de Shannon sobre a PSD
normalizada não exige nenhuma binarização. LZC aplicado a EEG tem
precedente citável (Zhang, X.S., Roy, R.J., Jensen, E.W. (2001). "EEG
complexity as a measure of depth of anesthesia for patients." *IEEE
Transactions on Biomedical Engineering*, 48(12), 1424–1433. PMID 11759923)
e fica registrado aqui como candidato de robustez para uma frente futura,
não como `I(X)` primário desta operacionalização.

**Fórmula fechada:**

Para um canal (ou média de canais, ver §2) `x(t)` amostrado a `f_s` Hz,
estima-se a densidade espectral de potência `P(f)` pelo método de Welch
(Welch, P.D. (1967). "The use of fast Fourier transform for the estimation
of power spectra: A method based on time averaging over short, modified
periodograms." *IEEE Transactions on Audio and Electroacoustics*, 15(2),
70–73. — verificado via WebSearch nesta sessão, artigo pré-PubMed/pré-DOI
mas identidade bibliográfica confirmada por múltiplas fontes secundárias
independentes, incluindo o PDF do artigo original hospedado publicamente),
com janela Hann, comprimento e sobreposição fixados em §2.4.

Restringindo `P(f)` à banda de análise pré-declarada `R_λ = [f_lo, f_hi]`
(§2.1) e discretizando em `N` bins de frequência `f_1,...,f_N ∈ R_λ`:

```
p_i = P(f_i) / Σ_{j=1}^{N} P(f_j)          (PSD normalizada como pmf)

I(X) = SE(x) = − [ Σ_{i=1}^{N} p_i · log2(p_i) ] / log2(N)
```

`I(X) ∈ [0, 1]` por construção (Inouye et al. 1991; normalização por
`log2(N)` seguindo Vakkuri et al. 2004). `I(X) → 0` quando toda a potência
se concentra em um único bin (espectro puro/dominado por um autovalor);
`I(X) → 1` quando a potência se distribui uniformemente por todos os bins
de `R_λ` (espectro "branco" dentro da banda).

**Estatística primária reportável por sujeito/condição:** a média de
`I(X)` sobre um conjunto de canais fixo e nomeado — **todos** os canais
EEG disponíveis na montagem do dataset (não um subconjunto/ROI escolhido a
dedo, para não introduzir mais um grau de liberdade não mandatado):

```
Ī(X) = (1/K) Σ_{k=1}^{K} I(X_k)
```

onde `K` é o número de canais EEG (excluindo canais de referência,
mastoide, EOG/ECG auxiliares e anotações — ver §2.3).

### 1.3 Resolução declarada da ambiguidade `1/f^α` (classe 3, "Viscous
Medium") e estatística secundária/exploratória

A classe 3 não tem dataset real identificado por `SURVEY.md` (nem Mumtaz
nem DASPS testam uma condição "metabólica/viscosa" rotulada como tal) —
portanto **nenhum teste desta classe está autorizado ou é proposto nesta
operacionalização**. Ela é operacionalizada aqui apenas por completude
metodológica, para que uma frente futura que localize um dataset
apropriado (ex.: EEG em fadiga inflamatória/pós-COVID, ou "brain fog") não
precise refazer este trabalho de tradução qualitativo→quantitativo.

Adota-se o expoente aperiódico (`1/f`) estimado por parametrização
espectral, método `specparam`/FOOOF: Donoghue, T., Haller, M., Peterson,
E.J. et al. (2020). "Parameterizing neural power spectra into periodic and
aperiodic components." *Nature Neuroscience*, 23(12), 1655–1665. PMID
33230329. O método ajusta `P(f) = 10^b · f^{−χ} + Σ_gaussianas(picos
oscilatórios)` sobre uma banda definida, retornando o expoente aperiódico
`χ` isolado da atividade oscilatória — resolvendo por construção a
ambiguidade "oscilação vs. fundo aperiódico" que a frase qualitativa de
`PAPER_B` não distingue.

**Convenção declarada para a contradição textual:** adota-se a leitura em
que "achatamento" (a fenomenologia clínica descrita: redução de amplitude
global, decaimento lento) corresponde a `χ` **menor** (espectro mais
próximo de ruído branco, menos inclinado) — convenção consistente com o
uso do termo "flattening"/"achatamento" na literatura de EEG e
envelhecimento/excitação-inibição cortical (Voytek, B., Kramer, M.A.,
Case, J. et al. (2015). "Age-Related Changes in 1/f Neural
Electrophysiological Noise." *Journal of Neuroscience*, 35(38),
13257–13265. PMID 26400953, onde "achatamento"/aumento do ruído 1/f com a
idade é explicitamente associado a `χ` **decrescente**). Isto é o
**oposto** da leitura literal de "α aumenta" em `PAPER_B:85`. Esta
inversão é registrada aqui como uma correção declarada e justificada da
formulação original — não uma invenção nova, mas a única leitura que torna
a frase de `PAPER_B` internamente consistente com a fenomenologia clínica
que ela mesma descreve ("Global Amplitude Reduction... Flattening").
**Nenhuma computação usa esta estatística secundária nesta etapa.**

---

## 2. `R_λ` e pré-processamento — fixado ANTES de tocar em dado real

Todos os parâmetros de aquisição citados abaixo para Mumtaz foram
**verificados empiricamente** nesta sessão, lendo o cabeçalho EDF de dois
arquivos reais baixados (ver §6 e `data/DOWNLOAD_VERIFICATION_MUMTAZ.log`)
— não apenas citados de um paper. Os parâmetros de DASPS foram verificados
pela leitura do preprint associado ao dataset (arXiv, ver abaixo), já que o
download de arquivo real não foi possível nesta sessão (§6.2).

### 2.1 Bandas de frequência e banda de análise `R_λ`

Convenção de bandas padrão adotada (delta 1–4 Hz, theta 4–8 Hz, alfa 8–13
Hz, beta 13–30 Hz, gama 30–45 Hz), citável via revisão específica de bandas
EEG em transtornos psiquiátricos: Newson, J.J., Thiagarajan, T.C. (2019).
"EEG Frequency Bands in Psychiatric Disorders: A Review of Resting State
Studies." *Frontiers in Human Neuroscience*, 12, 521. PMID 30687041. (O
próprio paper da DASPS usa uma convenção ligeiramente distinta na fronteira
beta/gama — δ 1–4, θ 4–8, α 8–13, β 13–32, Γ 32–64 Hz, ver §2.2 — registrado
aqui para transparência; a banda de análise `R_λ` usada em `I(X)` abaixo
não depende de qual convenção de sub-bandas se usa, pois `I(X)` é computado
sobre o espectro contínuo dentro de `R_λ`, não sobre potência por sub-banda
discreta.)

**`R_λ` para o teste de depressão (Mumtaz):** `[1, 40]` Hz. Banda ampla
deliberadamente — a alegação de `PAPER_B` é sobre a **forma** de toda a
distribuição espectral disponível ("dominância de baixos autovalores" só é
uma afirmação testável em relação ao resto do espectro); restringir `R_λ`
de antemão a uma sub-banda baixa tornaria a previsão verdadeira por
tautologia. Limite superior 40 Hz escolhido para ficar abaixo da frequência
de rede elétrica local (50 Hz na Malásia, onde Mumtaz et al. foi coletado —
Hospital Universiti Sains Malaysia, confirmado pela filiação institucional
no abstract de Mumtaz et al. 2018, ver §2.2), evitando a necessidade de um
filtro notch adicional como parâmetro extra.

**`R_λ` para o teste de ansiedade (DASPS):** `[4, 40]` Hz. Limite inferior
de 4 Hz **imposto pelo hardware/pré-processamento do próprio dataset**
(filtro FIR passa-banda 4–45 Hz aplicado pelos autores originais antes da
distribuição — Baghdadi, A., Aribi, Y., Fourati, R., Halouani, N., Siarry,
P., Alimi, A.M. (2019). "DASPS: A Database for Anxious States based on a
Psychological Stimulation." arXiv:1901.02942 — verificado por fetch direto
do texto renderizado nesta sessão), não uma escolha nossa: a banda Delta
não é recuperável neste dataset. Isto significa que o teste de ansiedade
**não pode, com este dataset, testar a componente Delta/Theta da alegação
de `PAPER_B`** — mas a alegação de ansiedade (`PAPER_B:63-74`) é
especificamente sobre ruído de **alta** frequência não travado em fase, já
dentro da faixa 4–40 Hz disponível, então esta restrição não invalida o
teste de ansiedade. Fica registrado como limitação explícita para qualquer
tentativa futura de comparar diretamente valores de `I(X)` ENTRE os dois
datasets (não planejada aqui — os dois testes são independentes, cada um
julgado dentro do seu próprio dataset, ver §4).

### 2.2 Parâmetros de aquisição por dataset (verificados)

**Mumtaz et al. (Figshare 4244171) — verificado por leitura de cabeçalho
EDF real (`scripts/edf_header_probe.py`, `data/DOWNLOAD_VERIFICATION_MUMTAZ.log`):**

| Parâmetro | Valor verificado |
|---|---|
| Formato | EDF (European Data Format), válido — Kemp, B., Värri, A., Rosa, A.C., Nielsen, K.D., Gade, J. (1992). "A simple format for exchange of digitized polygraphic recordings." *Electroencephalography and Clinical Neurophysiology*, 82(5), 391–393. PMID 1374708 |
| Taxa de amostragem | 256 Hz (todos os 19 canais EEG, confirmado por header, ambos arquivos de amostra) |
| Nº de canais | 19 EEG + 1 referência (`A2-A1`) + até 2 auxiliares + anotações (23 sinais no arquivo `H`, 21 no arquivo `MDD` — variação de quantos canais auxiliares foram incluídos, não afeta os 19 canais EEG nomeados) |
| Rótulos de canal | `Fp1,F3,C3,P3,O1,F7,T3,T5,Fz,Fp2,F4,C4,P4,O2,F8,T4,T6,Cz,Pz` — 10-20 padrão, sufixo `-LE` |
| **Montagem/referência** | **`-LE` = Linked Ears (referência de orelhas ligadas, A1+A2)** — confirmado diretamente no rótulo de cada canal (`EEG Fp1-LE`, etc.) e pelo canal explícito `EEG A2-A1` presente no arquivo. Esta é uma leitura empírica direta do dado, não uma suposição de literatura. |
| Filtro analógico (pré-filtragem) | `HP:0.5Hz LP:80Hz` (campo `prefiltering` do header EDF, ambos arquivos) |
| Sessões | `EC` (olhos fechados), `EO` (olhos abertos), `TASK` (P300) — confirmado pela descrição do dataset via API do Figshare |
| N | 34 MDD + 30 HC (102 arquivos `MDD *`, 91 arquivos `H *`, listagem completa via API, ver §6.1) |
| Local/instituição | Hospital Universiti Sains Malaysia — Mumtaz, W., Ali, S.S.A., Yasin, M.A.M., Malik, A.S. (2018). "A machine learning framework involving EEG-based functional connectivity to diagnose major depressive disorder (MDD)." *Medical & Biological Engineering & Computing*, 56(2), 233–246. PMID 28702811 (afiliação: Department of Psychiatry, Hospital Universiti Sains Malaysia) |
| Licença | CC BY 4.0 (confirmado via API do Figshare) |

**DASPS (IEEE DataPort) — verificado por leitura do preprint associado
(download do arquivo real bloqueado por login, ver §6.2), portanto estes
valores são de literatura, não de bytes baixados:**

| Parâmetro | Valor (fonte: Baghdadi et al. 2019, arXiv:1901.02942) |
|---|---|
| Dispositivo | Emotiv EPOC (consumer-grade, sem fio) |
| Taxa de amostragem | 128 Hz |
| Nº de canais | 14 EEG (`AF3,F7,F3,FC5,T7,P7,O1,O2,P8,T8,FC6,F4,F8,AF4`) + 2 mastoides |
| **Montagem/referência** | 1 mastoide = terra (ground); o outro mastoide = referência indireta (redução de interferência elétrica) |
| Filtro (pré-processamento) | FIR passa-banda 4–45 Hz |
| Estrutura de trial | 6 minutos totais; 6 situações × 30s (15s narrativa do terapeuta + 15s rememoração do sujeito) |
| Rótulo de estado (ground truth) | Duplo: HAM-A (escala clínica, pré/pós) + SAM (Self-Assessment Manikin, valência/excitação, por trial) — classificação em quadrante valência-excitação: "ansioso" = baixa valência + alta excitação |
| N | 23 sujeitos (13 mulheres, 10 homens, idade média 30) |

### 2.3 Janela de análise e estimação de PSD (Welch)

Fixado de forma consistente com a convenção (Hann, 50% sobreposição) mas
com comprimento de janela adaptado à taxa de amostragem/duração nativa de
cada dataset — a mesma disciplina já usada em `DISC-TRI-RG-001`
(`permutation_entropy/METHODOLOGY_NOTE.md`) de declarar o parâmetro ANTES
de tocar no dado real, não ajustá-lo depois de ver o resultado:

- **Mumtaz (EC, ~300s @ 256 Hz):** janelas Hann de 4s (1024 amostras,
  resolução em frequência 0,25 Hz), sobreposição 50% → ~149 janelas brutas
  por sujeito antes de rejeição de artefato (§2.5).
- **DASPS (segmento de 15s de rememoração por trial @ 128 Hz):** janelas
  Hann de 2s (256 amostras, resolução em frequência 0,5 Hz), sobreposição
  50% → ~14 janelas brutas por trial antes de rejeição de artefato.

Ambos seguem o método de Welch (Welch 1967, citado em §1.2).

### 2.4 Regra de rejeição de artefato (aplicada identicamente dentro de
cada dataset)

Regra de amiplitude por época, no espírito do princípio de threshold
estatístico do pipeline FASTER (Nolan, H., Whelan, R., Reilly, R.B.
(2010). "FASTER: Fully Automated Statistical Thresholding for EEG artifact
Rejection." *Journal of Neuroscience Methods*, 192(1), 152–162. PMID
20654646), **adaptada** para não exigir decomposição ICA (que é pouco
confiável com apenas 14 canais no caso de DASPS — FASTER original assume
denso o suficiente para ICA robusta):

- Uma janela (4s Mumtaz / 2s DASPS) é **rejeitada** se, em **qualquer**
  canal EEG, a amplitude pico-a-pico exceder `±150 μV`.
- Um sujeito é **excluído daquela condição/comparação** se mais de 50% das
  janelas daquela condição forem rejeitadas por este critério — regra fixa
  e pré-declarada, não decidida após ver quantos sujeitos sobrariam.
- `Ī(X)` de um sujeito/condição é a média de `I(X)` sobre as janelas **não
  rejeitadas**, por canal, depois média sobre canais (§1.2).

Esta é uma adaptação declarada, não a aplicação literal e completa de
FASTER (que envolve também métricas de variância/gradiente/curtose e
rejeição de componente ICA) — escolhida deliberadamente mais simples para
ser aplicável identicamente aos dois hardwares muito diferentes (EEG
clínico 19 canais vs. Emotiv 14 canais consumer-grade) sem introduzir um
parâmetro que dependa do número de canais.

### 2.5 Sobre a construção de grafo/Laplaciano — decisão de NÃO exigi-la
no teste primário

`PAPER_B` propõe "Laplacian Eigenvalues" como o objeto formal, mas o
próprio artigo (tabela §2.1) já mapeia autovalor diretamente para banda de
EEG, sem exigir a construção explícita de um grafo de conectividade
funcional a partir dos canais brutos. Construir esse grafo exigiria uma
escolha adicional e **não mandatada pelo texto-fonte** — qual estimador de
conectividade (coerência? PLV? correlação?), qual limiar/densidade de
grafo, qual normalização do Laplaciano — cada uma dessas é um grau de
liberdade extra que o próprio `AGENTS.md` instrui a evitar ("não inventar
fórmula ad hoc"). Por isso, **o teste primário desta operacionalização usa
`Ī(X)` diretamente sobre a PSD do canal (§1.2), sem etapa de grafo.**

Para uma frente futura que queira preservar literalmente o enquadramento
"Laplaciano do conectoma" como checagem de robustez (não como teste
primário), a representação fica especificada aqui, com métodos e citações
reais, para não exigir nova pesquisa bibliográfica:

1. Conectividade por par de canais: Weighted Phase Lag Index (WPLI), que é
   robusto a condução de volume/artefato de referência comum — Vinck, M.,
   Oostenveld, R., van Wingerden, M., Battaglia, F., Pennartz, C.M.A.
   (2011). "An improved index of phase-synchronization for
   electrophysiological data in the presence of volume-conduction, noise
   and sample-size bias." *NeuroImage*, 55(4), 1548–1565. PMID 21276857.
2. Matriz de adjacência ponderada `W` (WPLI por par de canais, por banda).
3. Laplaciano normalizado simétrico `L_sym = I − D^{−1/2} W D^{−1/2}`,
   convenção padrão de teoria espectral de grafos — von Luxburg, U.
   (2007). "A tutorial on spectral clustering." *Statistics and
   Computing*, 17(4), 395–416.
4. `I(X)` seria então a mesma entropia de Shannon normalizada (§1.2), mas
   aplicada à distribuição dos autovalores `λ_i` de `L_sym` em vez de à PSD
   — matematicamente a mesma operação, objeto diferente.

**Nenhuma computação desta seção (2.5) foi executada nesta etapa.**

---

## 3. Modelo(s) concorrente(s)/nulo nomeado(s)

### 3.1 Nulo estatístico padrão

`H0`: a distribuição de `Ī(X)` (ou de `ΔĪ(X)` no caso pareado de DASPS) é
idêntica entre os grupos/condições comparados — nenhum efeito.

### 3.2 Modelo concorrente nomeado — depressão (Mumtaz)

Literatura real e publicada de grafo-teoria clínica em MDD faz uma
previsão **estrutural** diferente da de `PAPER_B`. `PAPER_B:56-58`
descreve a topologia da depressão como um "deep local attractor" com
"high energy barriers", topologia "rígida" — linguagem que implica um
grafo funcional **mais** clusterizado/mais conectado localmente, não
menos. Em contraste:

> Sun, S., Li, X., Zhu, J., Wang, Y., La, R., Zhang, X., Wei, L., Hu, B.
> (2019). "Graph Theory Analysis of Functional Connectivity in Major
> Depression Disorder With High-Density Resting State EEG Data." *IEEE
> Transactions on Neural Systems and Rehabilitation Engineering*, 27(3),
> 429–439. PMID 30676968.

encontrou, em 16 MDD vs. 16 controles saudáveis (EEG 128 canais,
repouso), **topologia de rede randomizada** em MDD ("randomized network
structure were found in MDD") e coeficiente de clustering (banda theta,
região centro-esquerda) **negativamente correlacionado** com a gravidade
da depressão — ou seja, quanto mais grave a depressão, **menor** o
clustering local, não maior. Isto é uma previsão **direcionalmente oposta**
à leitura natural de "atrator local profundo/rígido" de `PAPER_B` para a
mesma condição clínica.

Este não é reformulado aqui para prever um número exato de `Ī(X)` (o
estudo usa uma métrica de grafo, não entropia espectral de PSD) — ele serve
como **modelo concorrente qualitativo/estrutural nomeado**, nos termos que
`METHODOLOGY_EXTENSIONS.md` §1 exige: uma alegação real, publicada, com
direção diferente da de Tamesis para a mesma condição clínica.

### 3.3 Modelo concorrente nomeado — ansiedade (DASPS)

`PAPER_B:67-69` prevê, para ansiedade, "Overfitting... excessive
short-range loops (**high** Clustering Coefficient)" de forma uniforme.
Em contraste:

> Qi, X., Fang, J., Sun, Y., Xu, W., Li, G. (2023). "Altered Functional
> Brain Network Structure between Patients with High and Low Generalized
> Anxiety Disorder." *Diagnostics*, 13(7), 1292. PMID 37046509.

encontrou, em 21 HGAD (alta ansiedade) vs. 30 LGAD (baixa ansiedade), EEG
de repouso, um padrão **misto e específico por banda**: índice PLI
(conectividade de fase) **aumentado** em alfa2 mas **diminuído** em
theta/alfa1 no grupo HGAD, e small-worldness (organização de rede)
**diminuindo** com a gravidade do GAD em theta e alfa2 — não um aumento
uniforme de clustering em todas as bandas de alta frequência como a
formulação simples de `PAPER_B` prevê. Serve como modelo concorrente
nomeado: uma alegação de mudança estrutural **heterogênea/específica por
banda**, não a assinatura uniforme de "ruído de alta frequência" prevista
por `PAPER_B`.

### 3.4 Nulo "apenas amplitude" (diretamente comparável a `I(X)`)

Modelo alternativo mais simples e **diretamente comparável** à estatística
escolhida (§1): as diferenças de grupo observadas em EEG, se existirem, são
apenas de **potência total** (amplitude), não de **forma**/complexidade da
distribuição espectral. Como `I(X)` é computado sobre a PSD **normalizada**
(§1.2), `I(X)` é por construção invariante a um reescalonamento uniforme da
potência — se o efeito real for "apenas mais/menos potência, mesma forma",
`I(X)` não mostrará diferença mesmo que a potência bruta difira. **Controle
obrigatório:** a potência total bruta por banda (`Σ P(f)`, sem normalizar)
deve ser reportada lado a lado com `Ī(X)` em qualquer análise futura, para
que um resultado nulo em `Ī(X)` não seja mal-interpretado como "sem
diferença nenhuma" quando na verdade há diferença de amplitude não
capturada pela entropia. Isto não é computado nesta etapa.

---

## 4. Regra de decisão a priori

Duas comparações **independentes**, cada uma julgada dentro do seu próprio
dataset — não são combinadas em um único p-valor agregado.

### 4.1 Mumtaz — depressão

- **Desenho:** grupos independentes, MDD (N=34) vs. HC (N=30).
- **Condição:** sessão `EC` (olhos fechados) — condição de repouso
  canônica nesta literatura, evita confundir com atividade evocada da
  sessão `TASK`.
- **Estatística primária, única, pré-declarada:** `Ī(X)_EC`, banda
  `R_λ=[1,40]` Hz, média sobre os 19 canais EEG (§1.2, §2.1).
- **Teste:** teste t de Welch (duas amostras independentes, variâncias não
  assumidas iguais) bicaudal, `α=0,05`; teste de Mann-Whitney U como
  companhia não-paramétrica de robustez (reportado, não usado para o
  veredito primário).
- **Direção prevista por Tamesis:** `Ī(X)_MDD < Ī(X)_HC` (potência
  concentrada em baixa frequência/baixos autovalores → menor entropia).
- **CONFIRMA:** rejeita `H0` (`p<0,05`, com correção de §4.3) **e** direção
  observada é `MDD < HC`.
- **REFUTA:** rejeita `H0` na direção **oposta** (`MDD > HC`) — interpretável
  à luz do modelo concorrente §3.2 (rede mais randomizada/menos
  estruturada em MDD poderia, plausivelmente, correlacionar com entropia
  espectral *maior*, não menor).
- **INCONCLUSIVO:** não rejeita `H0` (`p≥0,05`) — reportado como nulo
  honesto, mesmo padrão de `DISC-TRI-RG-001`.

### 4.2 DASPS — ansiedade

- **Desenho:** pareado, dentro do sujeito, N=23. Para cada sujeito, agrupar
  os segmentos de 15s de rememoração dos trials classificados como
  "ansioso" (baixa valência + alta excitação no SAM, por trial, seguindo a
  própria convenção de Baghdadi et al. 2019) vs. os classificados como
  "calmo" (os demais trials do mesmo sujeito).
- **Estatística primária, única, pré-declarada:** `ΔĪ(X) = Ī(X)_ansioso −
  Ī(X)_calmo`, banda `R_λ=[4,40]` Hz, média sobre os 14 canais EEG.
- **Teste:** teste t pareado bicaudal, `α=0,05`; teste de Wilcoxon
  signed-rank como companhia de robustez.
- **Direção prevista por Tamesis:** `ΔĪ(X) > 0` (entropia maior no estado
  ansioso — ruído de alta frequência não travado em fase).
- **CONFIRMA:** rejeita `H0` **e** `ΔĪ(X) > 0`.
- **REFUTA:** rejeita `H0` com `ΔĪ(X) < 0` — interpretável como
  "estreitamento espectral" (hiperexcitação concentrando energia em uma
  banda específica, reduzindo a entropia apesar do aumento de potência
  localizado), uma alternativa fisiológica real e nomeável, não apenas "o
  oposto de Tamesis".
- **INCONCLUSIVO:** não rejeita `H0`.

### 4.3 Correção para múltiplas comparações

Um teste primário por dataset (2 no total, Mumtaz + DASPS). Se ambos forem
interpretados como parte da mesma alegação de `PAPER_B` (não duas
alegações totalmente independentes), aplicar correção de Bonferroni:
`α_corrigido = 0,05/2 = 0,025` por teste. Este documento **recomenda**
`α=0,025` como o padrão mais conservador para uma futura pré-registro, mas
deixa explícito que a alternativa (tratar como duas sub-hipóteses
pré-registradas independentes, cada uma com `α=0,05` próprio) também é
defensável — a decisão final de qual convenção travar cabe ao
`PREREGISTRATION.md`, não a este documento. Qualquer teste secundário/de
robustez (sessão `EO` em vez de `EC`, banda alternativa, por-canal em vez
de média) declarado como tal exigiria correção adicional e **não conta**
para o veredito primário de confirmação/refutação.

### 4.4 Veredito conjunto (apenas para contexto, não é um único teste)

- Ambos os datasets CONFIRMAM na direção prevista → suporte cross-domain
  fraco-mas-real (dois testes independentes, mesma família estatística,
  mesma direção qualitativa em duas condições clínicas distintas).
- Um confirma, o outro é inconclusivo/refuta → resultado misto, reportado
  como tal, sem inflar para "parcialmente confirmado" além do que os
  números sustentam.
- Nenhum confirma → nulo honesto para a linha inteira, mesmo espírito do
  fechamento de `DISC-TRI-RG-001`.

---

## 5. Poder estatístico a priori

**Método:** distribuição t não-central exata (Cohen, J. (1988).
*Statistical Power Analysis for the Behavioral Sciences* (2ª ed.),
Lawrence Erlbaum Associates — referência padrão para a convenção `d =
0,2/0,5/0,8` pequeno/médio/grande usada aqui), calculada via
`statsmodels.stats.power` (`TTestIndPower` para Mumtaz, grupos
independentes; `TTestPower` para DASPS, pareado). Script completo e
reexecutável: `scripts/power_analysis.py`; saída completa:
`data/power_analysis_output.log`.

### 5.1 Mumtaz (N_MDD=34, N_HC=30, teste t independente, `α=0,05` bicaudal)

| Cohen's d | Poder |
|---|---|
| 0,20 (pequeno) | 0,123 |
| 0,30 | 0,218 |
| 0,50 (médio) | 0,502 |
| 0,80 (grande) | 0,882 |

`d` mínimo detectável para 80% de poder neste N: **`d = 0,713`** — um
efeito **grande**, quase no limite superior da convenção de Cohen.

### 5.2 DASPS (N=23, teste t pareado, `α=0,05` bicaudal)

| Cohen's d (da diferença pareada) | Poder |
|---|---|
| 0,20 | 0,151 |
| 0,30 | 0,280 |
| 0,50 (médio) | 0,630 |
| 0,80 (grande) | 0,956 |

`d` mínimo detectável para 80% de poder neste N: **`d = 0,611`** — também
um efeito grande, embora o desenho pareado (remove variância
entre-sujeito) seja mais eficiente que o desenho independente de Mumtaz
para o mesmo N nominal.

### 5.3 Interpretação honesta

**Ambos os datasets são subdimensionados (underpowered) para detectar
efeitos pequenos-a-médios** (`d≤0,5`), a faixa mais plausível a priori para
um biomarcador de EEG em psiquiatria: a literatura de meta-análise de
poder estatístico em neurociência documenta que estudos individuais
pequenos tendem a superestimar o tamanho de efeito verdadeiro e que o
poder mediano de estudos em neurociência é baixo — Button, K.S.,
Ioannidis, J.P.A., Mokrysz, C., Nosek, B.A., Flint, J., Robinson, E.S.J.,
Munafò, M.R. (2013). "Power failure: why small sample size undermines the
reliability of neuroscience." *Nature Reviews Neuroscience*, 14(5),
365–376. PMID 23571845. Isto não impede o teste (`d` grande ainda é uma
previsão honesta e falsificável, e `PAPER_B` descreve os efeitos em
linguagem categórica forte — "collapse", "dominância", "colapso" — que, se
literalmente verdadeira, deveria produzir um efeito grande, não sutil), mas
significa que:

1. Um resultado **INCONCLUSIVO** (§4) não pode ser lido como "Tamesis
   refutado" — pode ser simplesmente falta de poder para um efeito
   pequeno-médio real. O `PREREGISTRATION.md` futuro precisa declarar essa
   limitação explicitamente no texto do veredito, não só nos números.
2. Um resultado que **CONFIRMA** com `d` observado grande (`≥0,7`) é
   evidência mais forte precisamente porque o desenho só tinha poder para
   detectar efeitos dessa magnitude — não há inflação de "p-hacking por
   poder excessivo" aqui, o oposto do problema usual.
3. Nenhum dos dois datasets permite, com poder aceitável, **também**
   estimar um tamanho de efeito pequeno com precisão razoável — um
   resultado nulo aqui é consistente tanto com "efeito zero" quanto com
   "efeito real mas `d<0,5`", e o `PREREGISTRATION.md` deve dizer isso
   explicitamente ao reportar qualquer `p≥0,05`.

O precedente mais próximo já fechado nesta trilha (`DISC-TRI-RG-001`,
`permutation_entropy/RESULTS_SUMMARY.md`) usa uma família estatística
correlata (entropia/complexidade de sinal fisiológico) mas um desenho
estruturalmente diferente (transição de estado dentro do mesmo sujeito ao
longo do tempo, N=1 segmento por domínio, não classificação
entre-sujeitos) — seu resultado negativo (`p∈[0,275; 0,995]` nas 8
combinações testadas) não é diretamente comparável em poder, mas é
reportado aqui como contexto honesto: esta família estatística já produziu
8 nulos consecutivos nesta trilha em outros domínios fisiológicos.

---

## 6. Verificação de acesso real aos dados — por download, não só busca

### 6.1 Mumtaz (Figshare 4244171) — download bem-sucedido, integridade
verificada

A página HTML pública (`figshare.com/articles/dataset/EEG_Data_New/4244171`)
retorna **HTTP 403** nesta sessão (mesmo bloqueio anti-bot já encontrado em
`SURVEY.md`). Porém o **endpoint de API pública e legível por máquina**
(`api.figshare.com/v2/articles/4244171`) retorna **HTTP 200** com a
listagem completa dos 193 arquivos, cada um com URL de download direto
(`ndownloader.figshare.com/files/<id>`) e checksum MD5 fornecido pela
própria plataforma — este endpoint **não é** bloqueado.

Baixados e verificados nesta sessão:

| Arquivo | Tamanho | MD5 esperado (API) | MD5 obtido | Resultado |
|---|---|---|---|---|
| `H S1 EC.edf` | 3.538.944 bytes | `1dc454cf1c06402b78264c1bcbe39086` | `1dc454cf1c06402b78264c1bcbe39086` | ✅ idêntico |
| `MDD S1 EC.edf` | 3.263.488 bytes | `a04d5788e83c2bc7b6a214fd9d7702b5` | `a04d5788e83c2bc7b6a214fd9d7702b5` | ✅ idêntico |

Ambos os arquivos foram então parseados por um leitor de cabeçalho EDF
próprio, sem dependências externas (`scripts/edf_header_probe.py`,
implementado a partir da especificação EDF de Kemp et al. 1992, §1.2) —
**formato EDF válido confirmado**, 19 canais EEG a 256 Hz cada, consistente
com a documentação do dataset (§2.2). Log completo:
`data/DOWNLOAD_VERIFICATION_MUMTAZ.log` (metadados de paciente/gravação
redigidos nesta cópia do log — ver nota de privacidade abaixo).
Metadados brutos da API: `data/figshare_4244171_meta.json`.

**Nota de privacidade:** os dois arquivos EDF baixados continham, em campos
de cabeçalho padrão do formato EDF (`patient_id`), strings que se parecem
com nomes reais de sujeitos — um artefato do dataset público original
(CC BY 4.0), não algo introduzido por esta sessão. Os arquivos binários
brutos **foram removidos** deste diretório após a verificação de
integridade (não commitados), e o campo de nome no log de texto foi
redigido, para não republicar essa string em um segundo repositório sem
necessidade — a verificação de integridade (checksum + parse de formato)
não depende de reter o binário nem de reproduzir esse campo.
**O download completo (903.228.416 bytes, 193 arquivos) não foi feito** —
fora de escopo desta etapa (nenhuma computação de `I(X)` é permitida
aqui); a verificação de dois arquivos de amostra (um `H`, um `MDD`) já
estabelece que (a) o dataset existe, (b) é publicamente baixável via API,
(c) o formato é o documentado, (d) os parâmetros de aquisição batem com a
literatura — o suficiente para a pergunta desta etapa ("é dado real e
acessível?").

### 6.2 DASPS (IEEE DataPort) — acesso NÃO verificável nesta sessão

A página de listagem (`ieee-dataport.org/open-access/dasps-database`) é
alcançável (**HTTP 200**, sem bloqueio anti-bot, diferente do Figshare) e
confirma explicitamente: "Open Access dataset files are accessible to all
**logged in** users." Os 5 arquivos do dataset (≈156 MB no total — dados
brutos `.mat`, dados pré-processados, rótulos HAM-A) só ficam disponíveis
**após login**; não há endpoint de API pública análogo ao do Figshare —
tentativas de acesso direto a URLs de download plausíveis
(`.../dasps-database/download`, `.../sites/default/files/DASPS.zip`)
retornaram **HTTP 404**. Log completo: `data/DOWNLOAD_VERIFICATION_DASPS.log`.

**Criar uma conta IEEE gratuita** é o caminho oficial e documentado
(`ieee.org/profile/public/createwebaccount/...`), mas exige um passo
interativo (verificação de e-mail, e tipicamente aceite de termos/CAPTCHA)
que esta sessão de agente não-interativa **não pode completar**: não há
uma caixa de entrada de e-mail que esta sessão possa ler para confirmar um
cadastro, e criar uma conta usando a identidade do usuário sem sua
participação explícita e em tempo real está fora do escopo desta etapa de
operacionalização não-supervisionada.

**Veredito honesto, declarado explicitamente como pedido:** o **acesso ao
dado real de DASPS por download NÃO foi verificado** nesta sessão. O que
foi verificado: (1) a página do dataset é real, pública, e não bloqueada
por anti-bot; (2) o dataset é genuíno (citado de forma consistente por
múltiplas fontes secundárias independentes — Baghdadi et al. 2019 arXiv,
PLOS ONE, ScienceDirect); (3) o mecanismo de acesso é exatamente o
descrito em `SURVEY.md` (login gratuito, sem aprovação institucional) —
não há evidência de que o dataset seja inacessível em definitivo, apenas
que **este tipo de sessão não pode completar o passo de cadastro**. Uma
sessão futura com um humano disponível para completar o cadastro (ou
credenciais IEEE já existentes do usuário) deveria conseguir baixar o
dataset sem obstáculo adicional — isso não foi testado aqui, e não deve ser
apresentado como testado.

---

## 7. Veredito desta etapa e o que falta antes de um `PREREGISTRATION.md`

**O que esta etapa entrega, cumprindo o mandato de `DISC-DEC-025`:**

1. `I(X)` tem agora uma fórmula fechada, única, citada de método
   estabelecido (entropia espectral de Shannon normalizada sobre PSD de
   Welch, §1.2) — não mais "colapso"/"dominância" qualitativos.
2. `R_λ`, montagem/referência (verificada empiricamente para Mumtaz, de
   literatura para DASPS), janela de análise, e regra de rejeição de
   artefato estão fixados com números exatos, antes de qualquer dado real
   ser computado (§2).
3. Dois modelos concorrentes reais, publicados, e citados, com previsão
   direcional diferente da de Tamesis, um para cada condição clínica (§3).
4. Regra de decisão confirma/refuta/inconclusivo, com direção numérica
   exata e critério de correção por múltiplas comparações, pronta para
   ser travada verbatim em um pré-registro futuro (§4).
5. Poder estatístico calculado a priori para os dois N reais — resultado
   honesto: **ambos os datasets só têm poder aceitável (≥80%) para efeitos
   grandes (`d≥0,6-0,7`)**, não para o range pequeno-médio mais plausível a
   priori (§5).
6. Acesso real verificado por download de fato, não só busca: **Mumtaz
   CONFIRMADO** (dois arquivos baixados, checksum MD5 batendo
   exatamente com a API, formato EDF válido, 903 MB / 193 arquivos
   totais catalogados); **DASPS NÃO confirmado** — página alcançável e
   não bloqueada, mas arquivo real não obtido porque o cadastro IEEE
   exige um passo interativo que este tipo de sessão não pode completar
   (§6).

**Isto está pronto para um `PREREGISTRATION.md`?**

**Parcialmente.** Nada aqui é um bloqueio de princípio (nenhuma
"impossibilidade de operacionalizar sem escolha arbitrária" foi
encontrada — ao contrário do que `SURVEY.md` temia como risco, `PAPER_B`
acabou sendo operacionalizável com métodos estabelecidos e citados, com
poucas ambiguidades genuínas, todas declaradas e resolvidas explicitamente
acima em vez de escondidas). Mas dois gaps concretos permanecem, e devem
ser nomeados com precisão, não empurrados para debaixo do tapete:

- **Gap 1 — acesso real a DASPS ainda não obtido.** Um `PREREGISTRATION.md`
  para a frente de ansiedade não pode ser escrito com dado em mãos até que
  uma sessão com capacidade de completar o cadastro IEEE DataPort (humano
  no loop, ou credenciais já existentes) baixe de fato os arquivos e
  repita a verificação de integridade feita aqui para Mumtaz (§6.1). Isto
  **não impede** um `PREREGISTRATION.md` para a frente de **depressão**
  isoladamente (Mumtaz), que já tem acesso confirmado por bytes.
- **Gap 2 — a convenção de correção por múltiplas comparações (`α=0,025`
  vs. `α=0,05` por teste, §4.3) e a convenção de resolução da ambiguidade
  `1/f^α` (§1.3) precisam de uma decisão final e explícita da sessão
  orquestradora/usuário antes de serem travadas em um pré-registro — este
  documento recomenda uma convenção para cada uma e justifica a escolha,
  mas não é este agente quem decide qual convenção final trava (fora do
  escopo desta etapa, e a escolha entre duas convenções igualmente
  defensáveis é precisamente o tipo de decisão que, feita unilateralmente
  aqui, poderia depois parecer uma reformulação pós-hoc se revertida).

Nenhum resultado real de EEG foi computado, visualizado, ou usado para
ajustar qualquer parâmetro acima — todas as escolhas de §1–§5 foram
fixadas usando apenas metadados (contagem de arquivos, cabeçalho EDF,
tamanhos, checksums) e literatura publicada, nunca o conteúdo do sinal
EEG em si.

---

## 8. Inventário de arquivos desta etapa

- `OPERATIONALIZATION.md` — este documento.
- `scripts/edf_header_probe.py` — parser de cabeçalho EDF sem dependências
  externas, reexecutável, usado para verificar formato/parâmetros de
  aquisição sem decodificar nenhum dado de sinal.
- `scripts/power_analysis.py` — cálculo de poder a priori (§5),
  reexecutável, usa apenas `numpy`/`statsmodels`.
- `data/figshare_4244171_meta.json` — metadados brutos da API pública do
  Figshare (listagem completa dos 193 arquivos, checksums, licença) — sem
  PII.
- `data/DOWNLOAD_VERIFICATION_MUMTAZ.log` — log completo da verificação de
  download/integridade/formato de Mumtaz (§6.1), com metadados de paciente
  redigidos.
- `data/DOWNLOAD_VERIFICATION_DASPS.log` — log completo da tentativa de
  acesso a DASPS e do motivo exato do bloqueio (§6.2).
- `data/power_analysis_output.log` — saída completa de `power_analysis.py`.

Nenhum arquivo de dado EEG bruto (`.edf`/`.mat`) foi retido neste
diretório — apenas metadados, logs de verificação, e scripts
reexecutáveis.
