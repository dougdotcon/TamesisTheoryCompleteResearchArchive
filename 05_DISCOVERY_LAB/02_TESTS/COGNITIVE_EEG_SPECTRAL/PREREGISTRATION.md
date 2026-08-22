# Pré-registro: Assinatura Espectral em Depressão — MDD vs. HC (Mumtaz)

**Status:** LOCKED
**Data de criação do rascunho:** 2026-08-22 (`PREREGISTRATION_DEPRESSION_DRAFT.md`)
**Data de travamento:** 2026-08-22 (`DISC-DEC-028`)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-22 — rascunho
redigido por um front de agente (mandato `DISC-DEC-027(b)`, item
`EEG-DEPRESSION-PREREG-DRAFT`); travado pela sessão orquestradora após
revisão explícita das duas lacunas nomeadas (§8, §2.1) — ver `DISC-DEC-028`
em `00_GOVERNANCE/DECISION_LEDGER.yaml` para o raciocínio de aprovação.
**Test ID:** `DISC-COGNITIVE-EEG-SPECTRAL-001` (braço depressão, sub-registro)
**Commit em que foi travado:** este arquivo é criado e commitado no mesmo
commit que registra `DISC-DEC-028` — ver `git log` para o hash exato.

> **Este documento é a versão TRAVADA**, promovida sem alteração de conteúdo
> matemático/metodológico de `PREREGISTRATION_DEPRESSION_DRAFT.md` (preservado
> integralmente nesta pasta como registro de auditoria) — apenas o cabeçalho
> acima foi atualizado para refletir o lock. Nenhum dado real de sinal EEG
> havia sido baixado, aberto, ou computado antes deste lock — ver §11
> (histórico, válido no momento do lock). A partir deste lock, o cálculo real
> sobre a sessão `EC` do dataset Mumtaz está autorizado, sujeito a §9
> (`stop_condition`) e ao item 5 de §9 ser entendido como agora superado
> especificamente pela autorização de `DISC-DEC-028` (baixar a sessão `EC`
> dos 64 sujeitos e computar `Ī(X)` — não o dataset completo de 193 arquivos/
> todas as sessões, que continua fora de escopo).

---

## 0. Escopo e o que este pré-registro NÃO cobre

Este documento cobre **exclusivamente** o braço depressão de
`DISC-COGNITIVE-EEG-SPECTRAL-001`: MDD vs. controles saudáveis (HC), dataset
Mumtaz et al. (Figshare 4244171). O braço ansiedade (DASPS, IEEE DataPort)
está **fora de escopo** deste pré-registro — seu acesso real por download
permanece bloqueado por um login IEEE DataPort interativo (criação de conta +
verificação de e-mail) que nenhuma sessão de agente não-interativa pôde
completar até agora (`OPERATIONALIZATION.md` §6.2). Um pré-registro para o
braço ansiedade exige seu próprio documento, escrito depois que uma sessão
com humano no loop obtiver o dado real de DASPS. Isto é reforçado como
proibição explícita em §9 abaixo.

A fonte da alegação testada é `90_LEGACY/08_COGNITIVE_TOPOLOGY/
TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/PAPER_B_SPECTRAL_SIGNATURES.md`
(doravante `PAPER_B`), lida diretamente por este agente (não apenas citada de
`OPERATIONALIZATION.md`) para verificar e resolver, com raciocínio próprio, a
ambiguidade textual nomeada por `DISC-DEC-027(b)` — ver §2.1.

---

## 1. Hipótese exata (`H_Tamesis`)

`PAPER_B` §3.1 ("The 'Entropic Trap' (The Depressive Signature)") descreve a
assinatura espectral prevista para depressão, textualmente (`PAPER_B:48-61`):

> "**Collapse of High Frequencies:** Diminished Gamma activity... **Dominance
> of Low Eigenvalues:** The spectrum is compressed towards λ→0. The brain
> gets 'bass-heavy'... **Low Complexity:** Reduced Lempel-Ziv complexity of
> the signal."

Diferente da classe 3 ("Viscous Medium", §2.1 abaixo), esta descrição **não**
contém a inconsistência interna do `1/f^α` — "colapso de altas frequências" +
"dominância de baixos autovalores" + "baixa complexidade" apontam
consistentemente, sem ambiguidade textual, para uma única direção: um
espectro **mais concentrado/menos uniforme**, isto é, **entropia espectral
menor**. A ponte já fornecida pelo próprio artigo (`PAPER_B` §2.1, tabela
"Rosetta Stone": autovalor baixo do Laplaciano ↔ bandas Delta/Theta;
autovalor alto ↔ Beta/Gamma) permite operacionalizar isto diretamente como
uma afirmação sobre a forma da PSD normalizada — exatamente o que a entropia
de Shannon aplicada à PSD mede (`OPERATIONALIZATION.md` §1.2, reproduzida em
§2 abaixo).

**`H_Tamesis` (enunciado exato, numérico, falsificável):**

```
Ī(X)_MDD < Ī(X)_HC
```

onde `Ī(X)` é a entropia espectral de Shannon normalizada, média sobre os 19
canais EEG, computada exatamente como definido em §2 abaixo, sobre a sessão
`EC` (olhos fechados) do dataset Mumtaz.

---

## 2. Observável discriminante `I(X)` — fórmula fechada

Copiada e finalizada de `OPERATIONALIZATION.md` §1.2, sem alteração de
conteúdo matemático (apenas restrita explicitamente ao braço depressão):

Para um canal `x(t)` amostrado a `f_s` Hz, estima-se a densidade espectral de
potência `P(f)` pelo método de Welch (Welch, P.D. 1967), com janela Hann,
comprimento e sobreposição fixados em §4. Restringindo `P(f)` à banda de
análise `R_λ = [1, 40]` Hz e discretizando em `N` bins de frequência
`f_1,...,f_N ∈ R_λ`:

```
p_i = P(f_i) / Σ_{j=1}^{N} P(f_j)          (PSD normalizada como pmf)

I(X) = SE(x) = − [ Σ_{i=1}^{N} p_i · log2(p_i) ] / log2(N)
```

`I(X) ∈ [0, 1]` por construção (Inouye et al. 1991; normalização por
`log2(N)` seguindo Vakkuri et al. 2004). `I(X) → 0` quando toda a potência se
concentra em um único bin; `I(X) → 1` quando a potência se distribui
uniformemente por todos os bins de `R_λ`.

**Estatística primária reportável por sujeito/condição** — média sobre os 19
canais EEG nomeados em §4.1 (não um subconjunto/ROI escolhido a dedo):

```
Ī(X) = (1/19) Σ_{k=1}^{19} I(X_k)
```

Nenhuma construção de grafo/conectoma/Laplaciano é exigida para esta
estatística primária — a justificativa completa (por que a ponte do próprio
`PAPER_B` já torna isto desnecessário, e por que a variante WPLI+Laplaciano
fica reservada como checagem de robustez futura opcional, não computada
aqui) está em `OPERATIONALIZATION.md` §2.5 e não é repetida aqui; nada nela
muda para o braço depressão.

### 2.1 Resolução declarada da ambiguidade `1/f^α` (`PAPER_B` §3.3, "Viscous
Medium") — exigida por `DISC-DEC-027(b)`, verificada nesta sessão

**Onde a ambiguidade vive, e por que ela NÃO afeta `H_Tamesis` acima.** A
frase ambígua está em `PAPER_B` §3.3 (`PAPER_B:83-86`), **não** em §3.1 (a
seção que define a assinatura de depressão testada por este pré-registro):

> "**Global Amplitude Reduction:** Flattening of the Power Spectral Density
> (PSD) curve (`1/f^α`, where `α` increases)."

Verifiquei este texto lendo `PAPER_B` diretamente (não apenas a citação de
`OPERATIONALIZATION.md`). A contradição é real e reproduzível: em um modelo
`PSD(f) ∝ 1/f^α`, **aumentar** `α` torna a curva **mais** inclinada — mais
potência concentrada em baixa frequência, decaimento mais rápido em alta
frequência — o **oposto** de "achatamento" (que, tomado literalmente,
significa uma curva mais próxima de plana/uniforme, isto é, `α` **menor**,
mais próxima de ruído branco `α→0`).

**Por que isto entra neste documento mesmo não sendo usado pelo teste
primário:** `PAPER_B` §3.3 ("The Viscous Medium") é uma **terceira classe
patológica distinta** ("metabólica/viscosa" — brain fog, fadiga,
processamento lento, depressão resistente a tratamento), rotulada no próprio
artigo como "Depression II" (§4.3) para diferenciá-la de "Depression I"
(a "Entropic Trap" de §3.1, testada aqui). O dataset Mumtaz é uma amostra de
MDD diagnosticado clinicamente **sem subtipagem** por mecanismo teórico —
não há rótulo "viscoso" vs. "aprisionado" nos dados, e nenhum teste desta
classe 3 está proposto ou autorizado aqui (`OPERATIONALIZATION.md` §1.3 já
registrava isto; confirmado nesta sessão: nenhum dataset conhecido rotula
esta condição especificamente). `DISC-DEC-027(b)` exige, ainda assim, que
este rascunho resolva a ambiguidade **explicitamente, com meu próprio
raciocínio**, não apenas repita a sinalização — o que faço abaixo.

**Duas leituras candidatas que considerei:**

1. **Confiar na palavra "flattening"** (χ, o expoente aperiódico
   estimado por FOOOF/specparam, **diminui** — espectro mais próximo de
   ruído branco) e tratar "`α` increases" como o erro de digitação/redação.
2. **Confiar na mecânica física do "amortecedor viscoso"** descrita na mesma
   subseção ("viscous damper on signal propagation") — um amortecedor
   dissipativo linear tipicamente age como filtro passa-baixa, atenuando
   frequências altas mais que baixas, o que **aumentaria** a inclinação
   espectral (χ **maior**) — e tratar a palavra "flattening" como uso frouxo/
   não-técnico (por ex. querendo dizer "traçado clinicamente mais 'achatado'/
   de menor amplitude visível", não literalmente "espectro de potência mais
   plano").

**Minha resolução, e por quê (leitura 1 — χ diminui):**

Adoto a leitura 1: **"achatamento" = expoente aperiódico `χ` menor**
(espectro mais próximo de ruído branco). Razões:

- A literatura técnica estabelecida de expoente `1/f` em EEG usa a palavra
  "flattening"/"achatamento" precisamente neste sentido: Voytek, B., Kramer,
  M.A., Case, J. et al. (2015). "Age-Related Changes in 1/f Neural
  Electrophysiological Noise." *Journal of Neuroscience*, 35(38),
  13257–13265. PMID 26400953, descreve explicitamente o achatamento/aumento
  do "ruído 1/f" associado ao envelhecimento como correspondendo a `χ`
  **decrescente** — é um casamento terminológico direto com uma fonte real,
  publicada, e especificamente sobre o mesmo objeto matemático (expoente
  aperiódico de EEG), não apenas uma inferência da minha parte.
- A analogia do "amortecedor viscoso" em `PAPER_B` §3.3 é uma metáfora física
  informal usada pelo autor para dar intuição fenomenológica ("brain fog",
  "processamento lento"), não uma derivação rigorosa de função de
  transferência — tratar essa metáfora como implicando uma direção específica
  e precisa para `α` seria super-interpretar um recurso retórico como se
  fosse uma dedução técnica, um salto maior do que confiar no termo técnico
  estabelecido ("flattening") que casa com a literatura publicada.
- A fenomenologia adjacente na mesma subseção ("Global Amplitude Reduction",
  "Slow Decay") é compatível com `χ` decrescente: um espectro mais achatado/
  mais próximo de ruído branco, sob potência total fisiologicamente limitada,
  redistribui potência para longe dos picos dominantes de baixa frequência
  (delta/alfa) normalmente proeminentes no EEG de repouso — manifestando-se
  como amplitude reduzida desses picos dominantes, consistente com "redução
  de amplitude global" como tipicamente reportado na literatura de
  achatamento/envelhecimento (o próprio Voytek et al. 2015 associa
  achatamento a redução de amplitude do pico alfa).

**Escopo explícito desta resolução:** esta é a mesma convenção já adotada em
`OPERATIONALIZATION.md` §1.3, e eu a confirmo aqui de forma independente,
tendo lido `PAPER_B` diretamente e avaliado a leitura alternativa acima antes
de decidir — não é uma repetição não-examinada. **Esta resolução não entra em
nenhum lugar da regra de decisão do braço depressão** (§6–§8 abaixo): o
expoente `χ`/FOOOF continua sendo, exatamente como em
`OPERATIONALIZATION.md` §1.3, uma estatística **secundária/exploratória**,
não computada por este pré-registro, sem dataset identificado para a classe
3, e sem papel no critério confirma/refuta/inconclusivo de `H_Tamesis`
(§1 acima) — que depende inteiramente de `Ī(X)` (entropia espectral de
Shannon, §2), não do expoente aperiódico. Registro esta resolução aqui
apenas porque `DISC-DEC-027(b)` explicitamente a exige antes do lock deste
documento, para que a lacuna nomeada não permaneça aberta sem uma posição
tomada e justificada por escrito.

---

## 3. Fonte de dado

- **Dataset:** Mumtaz et al., "MDD Patients and Healthy Controls EEG Data
  (New)", Figshare, artigo 4244171.
- **URL exata (verificada por fetch direto na etapa de operacionalização,
  não nesta etapa — ver §11):** endpoint de API pública
  `https://api.figshare.com/v2/articles/4244171` (retorna HTTP 200 com
  listagem completa); página HTML `https://figshare.com/articles/dataset/
  EEG_Data_New/4244171` (bloqueada por anti-bot, HTTP 403, não usada).
- **DOI:** `10.6084/m9.figshare.4244171.v2`. **Licença:** CC BY 4.0.
- **Paper de origem do dataset:** Mumtaz, W., Ali, S.S.A., Yasin, M.A.M.,
  Malik, A.S. (2018). "A machine learning framework involving EEG-based
  functional connectivity to diagnose major depressive disorder (MDD)."
  *Medical & Biological Engineering & Computing*, 56(2), 233–246. PMID
  28702811.
- **N esperado:** 34 sujeitos MDD + 30 controles saudáveis (HC) — contagem de
  arquivos únicos por prefixo (`MDD *` / `H *`) confirmada via listagem
  completa da API (193 arquivos no total, cobrindo sessões `EC`/`EO`/`TASK`
  por sujeito; a comparação primária usa apenas a sessão `EC`, um arquivo por
  sujeito).
- **Estado de verificação de acesso:** CONFIRMADO por download real de 2
  arquivos de amostra (um `H`, um `MDD`), checksum MD5 idêntico ao fornecido
  pela API, formato EDF válido por parsing de cabeçalho —
  `OPERATIONALIZATION.md` §6.1, `data/DOWNLOAD_VERIFICATION_MUMTAZ.log`,
  `data/figshare_4244171_meta.json`. **Nenhum novo download foi feito nesta
  etapa de redação do pré-registro** — ver §11.

---

## 4. Pipeline de pré-processamento exato (Mumtaz EDF)

Todos os parâmetros de aquisição abaixo foram verificados empiricamente na
etapa de operacionalização por parsing real de cabeçalho EDF de dois
arquivos de amostra (`scripts/edf_header_probe.py`,
`data/DOWNLOAD_VERIFICATION_MUMTAZ.log`) — não assumidos de literatura.

### 4.1 Canais e montagem

- **19 canais EEG** (padrão 10-20): `Fp1, F3, C3, P3, O1, F7, T3, T5, Fz,
  Fp2, F4, C4, P4, O2, F8, T4, T6, Cz, Pz`.
- **Excluídos** da estatística `Ī(X)`: o canal de referência explícito
  `A2-A1`, quaisquer canais auxiliares presentes em alguns arquivos (até 2,
  variando por sujeito — não afeta os 19 canais EEG nomeados, que estão
  presentes de forma idêntica em ambos os arquivos verificados), e o canal de
  anotações (`EDF Annotations`).
- **Referência/montagem:** **orelhas ligadas (Linked Ears, `-LE`, A1+A2)** —
  confirmado diretamente no rótulo de cada canal (`EEG Fp1-LE`, etc.) e pela
  presença do canal explícito `EEG A2-A1`. **Nenhuma re-referenciação é
  aplicada** (ex.: referência média, Laplaciano de superfície) — a montagem
  gravada é usada como está, para não introduzir um parâmetro metodológico
  extra não mandatado pelo texto-fonte nem pelo dataset.
- **Taxa de amostragem:** 256 Hz, todos os 19 canais (confirmado por
  cabeçalho, ambos os arquivos de amostra).
- **Filtro analógico já aplicado pelo hardware (não modificado):**
  `HP: 0.5 Hz, LP: 80 Hz` (campo `prefiltering` do cabeçalho EDF).

### 4.2 Condição/sessão e duração

- **Sessão usada:** `EC` (olhos fechados) — condição de repouso canônica
  nesta literatura; evita confundir com atividade evocada da sessão `TASK`
  (P300) ou possíveis artefatos oculares maiores de `EO`.
- **Duração da gravação `EC`:** ~300 s (confirmado por cabeçalho: 300,0 s no
  arquivo `H` de amostra, 303,0 s no arquivo `MDD` de amostra — pequena
  variação natural entre sujeitos, não um parâmetro ajustável).

### 4.3 Banda de análise `R_λ`

`R_λ = [1, 40]` Hz. Banda ampla deliberada — a alegação de `PAPER_B` §3.1 é
sobre a forma de toda a distribuição espectral disponível, não sobre uma
sub-banda isolada (restringir `R_λ` de antemão a uma sub-banda baixa
tornaria a previsão verdadeira por tautologia). Limite superior 40 Hz para
ficar abaixo da frequência de rede elétrica local (50 Hz na Malásia — Hospital
Universiti Sains Malaysia, confirmado pela filiação institucional de Mumtaz
et al. 2018), evitando exigir um filtro notch adicional como parâmetro
extra. **Nenhum filtro digital adicional é aplicado** além do já presente no
hardware (§4.1) — a restrição a `R_λ` é feita selecionando os bins de
frequência do resultado de Welch já computado, não por um filtro passa-banda
digital extra (que introduziria parâmetros de ordem/ripple não mandatados).

### 4.4 Estimação de PSD — parâmetros de Welch (exatos)

- **Método:** Welch (Welch 1967), janela **Hann**.
- **`nperseg` (comprimento de janela):** `1024` amostras = 4 s a 256 Hz
  (resolução em frequência resultante: `f_s/nperseg = 256/1024 = 0,25` Hz).
- **`noverlap` (sobreposição):** `512` amostras = 50%.
- **`nfft`:** igual a `nperseg` (`1024`), sem zero-padding — evita introduzir
  um parâmetro extra de interpolação espectral não mandatado.
- **Detrend por segmento:** remoção da média por segmento (convenção padrão/
  default de implementação de Welch, ex. `scipy.signal.welch(...,
  detrend='constant')`) — parâmetro não especificado em
  `OPERATIONALIZATION.md`, declarado aqui pela primeira vez usando o valor
  default de biblioteca padrão, para não introduzir uma escolha nova e
  arbitrária.
- **Escala:** densidade espectral de potência (`scaling='density'`, unidades
  µV²/Hz) — a normalização de `I(X)` (§2) torna a escala/unidade irrelevante
  para o resultado final, mas o valor é declarado aqui por completude.
- **Janelas brutas por sujeito (sessão `EC`, ~300 s, antes de rejeição de
  artefato):** ≈149, por 50% de sobreposição sobre ~300 s de sinal.

### 4.5 Regra de rejeição de artefato

Regra de amplitude por época (adaptação declarada do espírito FASTER —
Nolan, Whelan, Reilly 2010 — sem exigir decomposição ICA, pouco confiável em
apenas 19 canais; ver justificativa completa em `OPERATIONALIZATION.md`
§2.4):

- Uma janela de 4 s é **rejeitada** se, em **qualquer** dos 19 canais EEG, a
  amplitude pico-a-pico exceder **±150 μV**.
- Um sujeito é **excluído daquela condição** (`EC`) se mais de **50%** das
  janelas forem rejeitadas por este critério — regra fixa, pré-declarada,
  não ajustada após ver quantos sujeitos sobrariam.
- `Ī(X)` de um sujeito é a média de `I(X)` sobre as janelas **não
  rejeitadas**, por canal, e então a média sobre os 19 canais (§2).

Nenhum critério de exclusão por canal (má qualidade de eletrodo específico) é
definido — herdado sem modificação de `OPERATIONALIZATION.md` §2.4.

---

## 5. Modelo nulo / hipóteses concorrentes

### 5.1 Nulo estatístico padrão (`H0`)

A distribuição de `Ī(X)_EC` é idêntica entre os grupos MDD e HC — nenhum
efeito de grupo.

### 5.2 Modelo concorrente nomeado — Sun et al. 2019 (direção oposta)

> Sun, S., Li, X., Zhu, J., Wang, Y., La, R., Zhang, X., Wei, L., Hu, B.
> (2019). "Graph Theory Analysis of Functional Connectivity in Major
> Depression Disorder With High-Density Resting State EEG Data." *IEEE
> Transactions on Neural Systems and Rehabilitation Engineering*, 27(3),
> 429–439. PMID 30676968.

Encontrou, em 16 MDD vs. 16 controles saudáveis (repouso, EEG 128 canais),
**topologia de rede randomizada** em MDD e coeficiente de clustering (banda
theta) **negativamente correlacionado** com a gravidade da depressão — mais
grave a depressão, **menor** o clustering local.

`PAPER_B` §3.1 descreve a topologia da depressão como um "deep local
attractor" com "high energy barriers", topologia **rígida** — linguagem que
implica um grafo funcional **mais** clusterizado/mais estruturado, não menos.
Sun et al. 2019 é, portanto, uma alegação real, publicada, com previsão
**estrutural** oposta à de `PAPER_B` para a mesma condição clínica.

**Previsão diferente para `Ī(X)`:** Sun et al. 2019 não reportam entropia
espectral de PSD diretamente (usam uma métrica de grafo de conectividade,
não a estatística primária deste documento) — não é reformulado aqui como
uma previsão numérica exata para `Ī(X)`. Mas, qualitativamente: uma
topologia de rede **mais randomizada** (menos estruturada) é, na direção
oposta a "atrator rígido", mais consistente com um sinal de **maior**
desordem/entropia espectral do que menor — ou seja, se o achado de Sun et
al. 2019 se generaliza ao domínio espectral testado aqui, a previsão
correspondente é **`Ī(X)_MDD ≥ Ī(X)_HC`** (não suporte à direção de
`H_Tamesis`, plausivelmente o sinal oposto) — não apenas "o oposto de
Tamesis" genericamente, mas uma alegação nomeável e fisiologicamente
interpretável (§6, critério REFUTA).

### 5.3 Nulo "apenas amplitude" (já nomeado em `OPERATIONALIZATION.md` §3.4)

Modelo alternativo diretamente comparável à estatística escolhida: as
diferenças de grupo em EEG, se existirem, são apenas de **potência total**
(amplitude), não de **forma**/complexidade da distribuição espectral. Como
`I(X)` é computado sobre a PSD **normalizada** (§2), é por construção
invariante a um reescalonamento uniforme de potência — se o efeito real for
"apenas mais/menos potência, mesma forma", `Ī(X)` não mostrará diferença
mesmo que a potência bruta difira entre MDD e HC.

**Controle obrigatório, declarado aqui como parte do pré-registro (não
opcional):** a potência total bruta por banda (`Σ P(f)` sem normalizar, banda
`R_λ=[1,40]` Hz) deve ser reportada lado a lado com `Ī(X)` em qualquer
análise deste pré-registro, para que um resultado nulo em `Ī(X)` não seja
mal-interpretado como "sem diferença nenhuma entre os grupos" quando pode
haver diferença de amplitude não capturada pela entropia. Este controle é
**descritivo/contextual** — não participa da regra confirma/refuta/
inconclusivo de `H_Tamesis` (§6), que depende exclusivamente de `Ī(X)`.

*(Nota de escopo: Qi et al. 2023 — modelo concorrente para o braço ansiedade/
DASPS, `OPERATIONALIZATION.md` §3.3 — não é usado neste documento; fora de
escopo por §0.)*

---

## 6. Estatística de teste e regra de decisão a priori

- **Desenho:** grupos independentes, MDD (N=34) vs. HC (N=30).
- **Condição:** sessão `EC` (§4.2).
- **Estatística primária, única, pré-declarada:** `Ī(X)_EC`, banda
  `R_λ=[1,40]` Hz, média sobre os 19 canais EEG (§2, §4).
- **Teste primário (determina o veredito):** teste t de Welch (duas amostras
  independentes, variâncias não assumidas iguais), bicaudal, `α=0,05` (sujeito
  à convenção de §8).
- **Teste companheiro (robustez, NÃO determina o veredito):** Mann-Whitney U,
  reportado lado a lado, usado apenas para checar consistência qualitativa
  com o teste t — não pode, por si só, produzir CONFIRMA/REFUTA se o teste t
  primário não o fizer (ver §8 sobre por que isto não conta como uma segunda
  comparação que exigiria correção).

**Direção prevista por `H_Tamesis`:** `Ī(X)_MDD < Ī(X)_HC` (§1).

- **CONFIRMA:** o teste t de Welch rejeita `H0` (`p < α_corrigido`, §8) **e**
  a direção observada é `Ī(X)_MDD < Ī(X)_HC`.
- **REFUTA:** o teste t de Welch rejeita `H0` na direção **oposta**
  (`Ī(X)_MDD > Ī(X)_HC`) — interpretável à luz do modelo concorrente §5.2
  (rede mais randomizada/menos estruturada em MDD poderia, plausivelmente,
  correlacionar com entropia espectral *maior*, não menor).
- **INCONCLUSIVO:** o teste t de Welch não rejeita `H0` (`p ≥ α_corrigido`)
  — ver política de reporte obrigatória em §7, que este pré-registro trava
  como parte da própria regra de decisão, não como comentário à parte.

Nenhuma reformulação de `Ī(X)`, da banda `R_λ`, do teste, da direção
prevista, ou deste critério é permitida depois de ver qualquer resultado
real — ver §9.

---

## 7. Poder estatístico a priori e política de reporte de nulo

**Poder já calculado na etapa de operacionalização** (`scripts/
power_analysis.py`, `data/power_analysis_output.log`, distribuição t
não-central exata via `statsmodels.stats.power.TTestIndPower`, convenção de
`d` de Cohen 1988) — reproduzido aqui, sem recomputação nesta etapa:

| Cohen's `d` | Poder (N=34/30, `α=0,05` bicaudal) |
|---|---|
| 0,20 (pequeno) | 0,123 |
| 0,30 | 0,218 |
| 0,50 (médio) | 0,502 |
| 0,80 (grande) | 0,882 |

**`d` mínimo detectável para 80% de poder neste N: `d = 0,713`** — um efeito
**grande**, próximo do limite superior da convenção de Cohen, não do
intervalo pequeno-médio (`d≤0,5`) mais plausível a priori para um
biomarcador de EEG em psiquiatria (Button et al. 2013, PMID 23571845, já
citado em `OPERATIONALIZATION.md` §5.3).

**Isto é reconhecido explicitamente aqui, e travado como parte da própria
regra de decisão (não apenas mencionado à parte):**

1. **Um resultado INCONCLUSIVO (§6) será reportado como genuinamente
   subdimensionado (underpowered) para o intervalo de efeito pequeno-médio,
   NÃO como evidência contra `H_Tamesis`.** O texto do veredito, quando
   `p≥α_corrigido`, deve conter, verbatim ou equivalente: *"este resultado é
   consistente tanto com 'efeito zero' quanto com 'efeito real mas
   `d<0,5`' — a amostra (N=34/30) só tem poder de 80% para `d≥0,71`; um nulo
   aqui não deve ser lido como 'Tamesis refutado' nem como 'Sun et al. 2019
   confirmado', apenas como não-informativo neste N."* Isto é a mesma
   disciplina já aplicada ao Gate de Replicação de
   `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` (`01_PORTFOLIO/TEST_QUEUE.yaml`,
   entrada `gate_replication_result`), onde um resultado não-informativo por
   falta de poder no dataset reservado foi registrado como
   `REPLICATION_FAILED / CLOSED_INCONCLUSIVO`, explicitamente "não por
   contradição com confiança... registrado com o mesmo peso evidencial que
   um `REPLICATION_PASSED`... informativo por si só... não um defeito do
   processo" — o mesmo padrão de honestidade se aplica aqui: um nulo por
   falta de poder é catalogado com peso integral, não escondido, não
   reinterpretado como refutação.
2. **Um resultado que CONFIRMA com `d` observado grande (`≥0,7`) é evidência
   mais forte precisamente porque o desenho só tinha poder para detectar
   efeitos dessa magnitude** — não há inflação de "p-hacking por poder
   excessivo" possível aqui, o oposto do problema usual em amostras grandes.
3. Este pré-registro **não permite**, com este N, estimar com precisão
   razoável um tamanho de efeito pequeno — isto é reportado explicitamente
   junto com qualquer `p≥0,05`, não relegado a uma nota de rodapé.

---

## 8. Correção para comparações múltiplas — resolução declarada

`DISC-DEC-026`/`DISC-DEC-027(b)` nomeiam esta como a segunda lacuna a
resolver explicitamente antes do lock. `OPERATIONALIZATION.md` §4.3
apresentava duas convenções defensáveis sem decidir entre elas (correção de
Bonferroni entre os 2 datasets Mumtaz+DASPS, `α=0,025`, vs. `α=0,05`
independente por sub-hipótese) — mas essa é uma pergunta sobre correção
**entre os dois braços** (depressão vs. ansiedade), que não se aplica a este
documento porque **o braço ansiedade está fora de escopo aqui** (§0). A
pergunta que este documento precisa resolver é diferente e mais específica:
**quantas comparações o braço depressão, sozinho, está fazendo, e que
correção (se alguma) isso exige?**

**Minha resolução: nenhuma correção de Bonferroni é aplicada, porque a
análise primária deste pré-registro é, por desenho, um único teste
estatístico — não uma família de comparações.**

Justificativa, explicitamente contra o custo de poder já documentado em §7:

- A estatística primária `Ī(X)` (§2, §6) é **uma média sobre os 19 canais**,
  não 19 testes por-canal — esta escolha já estava fixada em
  `OPERATIONALIZATION.md` §1.2 ("média sobre um conjunto de canais fixo...
  para não introduzir mais um grau de liberdade não mandatado") e é mantida
  aqui, agora explicitamente como a razão pela qual nenhuma correção
  multi-canal é necessária: há **um** valor de `Ī(X)` por sujeito, não 19.
- A banda de análise é **uma única banda ampla** `R_λ=[1,40]` Hz (§4.3), não
  uma bateria de sub-bandas (delta/theta/alfa/beta/gama) testadas
  separadamente — de novo, **um** teste, não 5.
- A condição é **uma única sessão** (`EC`), não `EC` e `EO` testadas em
  paralelo — **um** teste, não 2.
- O teste companheiro Mann-Whitney U (§6) não conta como uma segunda
  comparação porque não pode, por si só, produzir um veredito — é reportado
  apenas como checagem de consistência sobre a **mesma** estatística
  primária já testada pelo t de Welch, não uma segunda hipótese
  independente.

**Por que rejeito a alternativa (Bonferroni por-canal ou por-banda) em vez
de simplesmente aplicá-la por segurança:** a amostra já é subdimensionada
para o intervalo de efeito mais plausível (§7: `d_min=0,71` para 80% de
poder já usando `α=0,05` sobre **um** teste). Decompor a análise em 19
testes por-canal exigiria `α_corrigido = 0,05/19 ≈ 0,0026`, e decompor em 19
canais × até 5 sub-bandas exigiria `α_corrigido = 0,05/95 ≈ 0,00053` — cada
uma dessas correções eleva ainda mais o `d` mínimo detectável a 80% de
poder, tornando um teste já marginal (que precisa de um efeito **grande**
para ter qualquer poder) efetivamente incapaz de confirmar qualquer coisa
menor que um efeito extremo. Aplicar uma correção multi-comparação a uma
análise que **não precisa fazer múltiplas comparações** (porque a estatística
primária já foi definida como uma média única, precisamente para evitar essa
armadilha) seria pagar um custo de poder por uma proteção estatística contra
um risco que o desenho já eliminou por construção — o oposto do objetivo de
uma correção de comparações múltiplas, que existe para controlar erro tipo I
quando há de fato uma família de testes.

**O que EXIGIRIA correção, e está fora do veredito primário deste
documento:** qualquer análise por-canal, por-sub-banda, ou usando a sessão
`EO` em vez de `EC`, se executada, seria declarada explicitamente como
**secundária/exploratória** e exigiria sua própria correção (Bonferroni ou
FDR, a decidir no momento, com o número exato de comparações declarado antes
de rodar) — e **não conta** para CONFIRMA/REFUTA/INCONCLUSIVO de `H_Tamesis`
neste pré-registro, mesma regra já usada em `OPERATIONALIZATION.md` §4.3
para testes secundários.

---

## 9. `stop_condition` — o que este pré-registro proíbe explicitamente

Este pré-registro (e qualquer execução futura sob ele, depois do lock) **NÃO
PERMITE**:

1. **Qualquer alegação diagnóstica ou clínica**, ou qualquer enquadramento
   que sugira que `Ī(X)` (ou o veredito deste teste) diagnostica, prediz,
   estadia, ou tem qualquer uso clínico para depressão em um indivíduo. Este
   é um teste de uma alegação matemática de teoria espectral de grafos
   (`PAPER_B`) contra estatística de sinal EEG agregada em nível de grupo —
   não é, e não deve ser apresentado, discutido, ou usado como uma
   ferramenta de diagnóstico ou triagem.
2. **Tocar o dataset DASPS ou o braço ansiedade** dentro do escopo deste
   pré-registro. O braço ansiedade permanece bloqueado por acesso (login
   IEEE DataPort, `OPERATIONALIZATION.md` §6.2) e exige seu próprio
   pré-registro, escrito depois que o dado real for obtido por uma sessão
   com humano no loop.
3. **Reformular `I(X)`, `R_λ`, o pipeline de pré-processamento (§4), a regra
   de rejeição de artefato, a estatística de teste, a direção prevista, o
   critério confirma/refuta/inconclusivo, ou a convenção de correção de
   comparações múltiplas (§8) depois de ver qualquer resultado real** —
   qualquer mudança de critério depois de olhar o dado é uma **nova
   hipótese**, exigindo um **novo** pré-registro, não uma correção deste. Isto
   vale mesmo que a mudança pareça uma correção menor ou uma "melhoria
   óbvia" — a mesma regra de `AGENTS.md` ("Proibições") se aplica
   integralmente aqui.
4. **Alegar "Tamesis confirmado", "detectado", ou "favorecido sobre modelos
   concorrentes"** a partir de um único teste sem replicação/reexecução
   adversarial independente (`AGENTS.md`, passo 7 do fluxo obrigatório) —
   mesmo um resultado CONFIRMA (§6) só produz um achado catalogado, não uma
   alegação inflada.
5. **Baixar o dataset completo (193 arquivos, ~903 MB) ou computar `I(X)`
   sobre qualquer dado real de sinal EEG** sob autoridade deste rascunho —
   isso permanece proibido até um lock formal (commit) autorizado
   explicitamente pela sessão orquestradora numa decisão subsequente, per
   `DISC-DEC-027`.

---

## 10. O que NÃO está sendo testado (escopo teórico)

- Isto NÃO é um teste da Teoria Tamesis como um todo, nem de qualquer
  alegação cosmológica/matemática/RH já catalogada nesta trilha — domínio
  inteiramente separado (neurociência computacional).
- Isto NÃO toca, testa, ou implica progresso sobre qualquer Problema do
  Millennium.
- Isto NÃO testa a classe "Viscous Medium" (`PAPER_B` §3.3) nem o expoente
  aperiódico `χ`/FOOOF — nenhum dataset rotulado para essa classe foi
  identificado; a resolução da ambiguidade `1/f^α` em §2.1 é registrada por
  exigência de governança, não porque seja usada pelo teste primário.
- Um resultado CONFIRMA aqui não estabelece causalidade, mecanismo, nem
  generalização além do dataset Mumtaz (amostra única, um hospital, um país)
  — replicação em dataset independente exigiria seu próprio pré-registro.
- Um resultado CONFIRMA não decide entre "atrator rígido" (`PAPER_B`) e
  outras explicações possíveis para entropia espectral reduzida em MDD além
  das nomeadas em §5 — apenas testa a direção prevista contra o nulo
  estatístico e contra a direção qualitativa de Sun et al. 2019.

---

## 11. Verificação de proveniência de dado nesta etapa — referenciado, não recomputado

**Nenhum dado real de sinal EEG foi baixado, aberto, ou computado por este
agente durante a redação deste rascunho.** Todos os fatos sobre o dataset
Mumtaz citados acima (contagem de arquivos, checksums MD5, rótulos de canal,
taxa de amostragem, referência/montagem, filtro de pré-processamento,
duração de gravação) foram **lidos** dos artefatos já produzidos e
verificados na etapa de operacionalização anterior (`DISC-DEC-025`/
`DISC-DEC-026`), presentes neste mesmo diretório:

- `data/DOWNLOAD_VERIFICATION_MUMTAZ.log` — log de download/checksum/parsing
  de cabeçalho EDF dos 2 arquivos de amostra (`H_S1_EC.edf`,
  `MDD_S1_EC.edf`), lido integralmente por este agente nesta sessão.
- `data/figshare_4244171_meta.json` — metadados brutos da API pública do
  Figshare (listagem completa dos 193 arquivos, checksums, licença), lido
  por este agente nesta sessão.
- `OPERATIONALIZATION.md` — documento de operacionalização completo, lido
  integralmente por este agente nesta sessão.
- `90_LEGACY/08_COGNITIVE_TOPOLOGY/TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/
  PAPER_B_SPECTRAL_SIGNATURES.md` — fonte primária da alegação, lida
  integralmente por este agente nesta sessão (não apenas citada de segunda
  mão) especificamente para verificar e resolver a ambiguidade `1/f^α`
  (§2.1) com raciocínio independente.

Nenhum arquivo `.edf` foi baixado, aberto, ou inspecionado nesta etapa;
nenhum script de computação de `I(X)` foi escrito ou executado nesta etapa;
`scripts/edf_header_probe.py` e `scripts/power_analysis.py` (ambos já
existentes, produzidos na etapa de operacionalização) não foram executados
nesta etapa — apenas seus logs de saída já existentes foram lidos.

---

## 12. Inventário de arquivos referenciados por este pré-registro

- `PREREGISTRATION_DEPRESSION_DRAFT.md` — este documento (rascunho, sem
  lock).
- `OPERATIONALIZATION.md` — documento de operacionalização completo
  (já travado por `DISC-DEC-025`/`DISC-DEC-026`, não modificado por este
  rascunho).
- `data/DOWNLOAD_VERIFICATION_MUMTAZ.log`, `data/figshare_4244171_meta.json`
  — proveniência de acesso ao dado Mumtaz (não modificados).
- `scripts/edf_header_probe.py`, `scripts/power_analysis.py` — scripts
  reexecutáveis já existentes (não modificados, não executados nesta
  etapa).
- `90_LEGACY/08_COGNITIVE_TOPOLOGY/TOPOLOGICAL_THEORY_OF_COGNITIVE_STATES/
  PAPER_B_SPECTRAL_SIGNATURES.md` — fonte da alegação (não modificada).

---

## [Preenchido depois do lock e da análise] Resultado

*(Não preenchido — este documento é um rascunho, não travado. Nenhuma
computação sobre dado real foi autorizada ou executada.)*

## [Preenchido depois da reexecução adversarial] Veredito adversarial

*(Não preenchido.)*
