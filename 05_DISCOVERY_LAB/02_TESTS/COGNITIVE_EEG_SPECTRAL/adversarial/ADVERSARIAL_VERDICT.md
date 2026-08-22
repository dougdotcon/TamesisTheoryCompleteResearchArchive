# Veredito adversarial — Assinatura Espectral em Depressão (Mumtaz MDD vs. HC)

**Test ID:** `DISC-COGNITIVE-EEG-SPECTRAL-001` (braço depressão)
**Pré-registro travado:** `PREREGISTRATION.md` (`DISC-DEC-028`) — lido em
íntegra, sozinho, ANTES de qualquer código ou resultado do agente primário.
**Papel deste agente:** reexecução adversarial obrigatória (`00_GOVERNANCE/
AGENTS.md`, passo 7) — segundo agente, independente, instruído a tentar
refutar o achado do agente primário, não confirmá-lo.
**Disciplina seguida:** implementação própria travada (leitor EDF próprio,
Welch próprio, entropia própria, rejeição de artefato própria, testes
estatísticos próprios) **antes** de ler `analysis/run_primary_analysis.py`,
`RESULTS_PRIMARY.md`, ou `results/*.json`. Ordem real desta sessão: (1) ler
`AGENTS.md` §passo 7 e `PREREGISTRATION.md` na íntegra; (2) escrever e
validar cada componente do pipeline contra bibliotecas de referência
(`pyedflib`, `scipy`) usando dado sintético — nunca contra o código do
agente primário; (3) baixar e processar os 64 arquivos `EC` de forma
independente; (4) travar meus próprios números; (5) só então ler
`RESULTS_PRIMARY.md`/`run_primary_analysis.py`/`result_primary.json` e
comparar.

---

## VEREDITO: **CONFIRMADO**

A reexecução adversarial **não encontrou nenhum bug, nenhuma discrepância
metodológica, e nenhuma diferença numérica além de ruído de ponto
flutuante/arredondamento de exibição**. O resultado REFUTA relatado pelo
agente primário é reproduzido de forma independente, com direção,
significância e tamanho de efeito praticamente idênticos, usando um
pipeline construído do zero a partir apenas do texto travado de
`PREREGISTRATION.md`.

```
Ī(X)_MDD > Ī(X)_HC   (t de Welch, p<0,05)  →  REFUTA (PREREGISTRATION.md §6)
```

---

## 1. O que foi implementado de forma independente (antes de olhar o código primário)

Todos os arquivos abaixo estão em `adversarial/scripts/`, escritos e
validados nesta sessão sem consultar `analysis/run_primary_analysis.py`:

| Componente | Arquivo | Validação (contra biblioteca de referência, com dado sintético — nunca contra o código do agente primário) |
|---|---|---|
| Leitor EDF do zero | `edf_reader.py` | Cabeçalho ASCII de largura fixa + amostras int16 little-endian, implementado diretamente da especificação EDF/EDF+ (Kemp et al. 1992). Cross-validado contra `pyedflib` no canal `Fp1` do arquivo `H S1 EC.edf`: diferença máxima absoluta `2,84×10⁻¹³` µV (ruído de ponto flutuante). |
| Welch PSD do zero | `welch_entropy.py` | Janela Hann **periódica** (`fftbins=True`, confirmado empiricamente ser o default de `scipy.signal.get_window`/`scipy.signal.welch`, não a convenção simétrica), detrend por remoção de média, escala de densidade, dobramento de bins unilateral. Cross-validado contra `scipy.signal.welch(..., nperseg=1024, noverlap=512, nfft=1024, window='hann', detrend='constant', scaling='density')` em ruído branco sintético: diferença máxima absoluta `4,44×10⁻¹⁵`, relativa `1,36×10⁻¹⁵`. |
| Entropia espectral de Shannon | `welch_entropy.py` | Fórmula fechada de `PREREGISTRATION.md` §2, `N` = número de bins **dentro de `R_λ`** (157 bins para `[1,40]` Hz a 0,25 Hz de resolução — **não** os 513 bins totais do FFT unilateral), `log2(N)` no denominador. Sanidade: ruído branco sintético → `I(X)≈0,999` (esperado, próximo de 1). |
| Rejeição de artefato + pipeline por sujeito | `pipeline.py` | Janela = segmento Welch (1024 amostras, grade de 50% sobreposição), máscara de rejeição **compartilhada** entre os 19 canais (`window_rejected = channel_exceeds.any(axis=0)`), `Ī(X)` = média sobre janelas não rejeitadas por canal → média sobre 19 canais. Interpretação de "janela" resolvida a partir da leitura literal de `PREREGISTRATION.md` §4.5 ("média de `I(X)` sobre as janelas") — decidida **antes** de ler o código primário. |
| Download + MD5 | `pipeline.py`/`run_all.py` | `curl` com até 3 tentativas por arquivo, verificação de MD5 contra o checksum fornecido pela API do Figshare antes de qualquer uso. |
| Teste t de Welch | `stats_own.py` | Fórmula fechada (df de Welch-Satterthwaite, CDF de `t` via função beta incompleta regularizada, `scipy.special.betainc`). Cross-validado contra `scipy.stats.ttest_ind(..., equal_var=False)` em dado sintético: `t`, `df`, `p` idênticos a `~10⁻¹⁶`. |
| Mann-Whitney U | `stats_own.py` | Ranks com correção de empate, aproximação normal com correção de continuidade. Cross-validado contra `scipy.stats.mannwhitneyu(..., alternative='two-sided')`: `U`, `p` idênticos a `~10⁻¹⁶`. |

---

## 2. Etapa 1 — Acesso ao dado (independente, própria busca na API)

Busquei `https://api.figshare.com/v2/articles/4244171` diretamente nesta
sessão (não usei `data/figshare_4244171_meta.json` já existente no
diretório do teste). Resultado: 193 arquivos, 64 com nome terminando em
` EC.edf` (34 `MDD *`, 30 `H *`) — confirma `PREREGISTRATION.md` §3.

**Tentei baixar os 64, cada um com até 3 tentativas.** Resultado:

- **58/64 baixados com sucesso**, MD5 do arquivo efetivamente baixado
  conferido contra `supplied_md5` da API — **100% de correspondência**,
  nenhum arquivo com MD5 divergente foi usado.
- **6/64 retornaram HTTP 404 de forma reprodutível** (3/3 tentativas cada):
  `H S12 EC.edf`, `H S18 EC.edf`, `MDD S4 EC.edf`, `MDD S8 EC.edf`,
  `MDD S12 EC.edf`, `MDD S16  EC.edf`.
- **Corroboração independente do 404** (não apenas confiei no HTTP 404):
  verifiquei nos metadados já baixados da API que exatamente esses 6
  arquivos — e nenhum outro entre os 64 `EC` — têm `computed_md5: ""` e
  `mimetype: "undefined"`, contra um `computed_md5` real para todos os
  outros 58. Isto é evidência independente de que o objeto de arquivo está
  genuinamente ausente do backend de armazenamento do Figshare, não um
  problema desta sessão. (Verifiquei também que esse padrão aparece em mais
  6 arquivos `EO`/`TASK` do artigo completo, fora de escopo aqui, reforçando
  que é uma lacuna de armazenamento geral do artigo, não específica à
  sessão `EC`.)

**Comparação com o agente primário:** os mesmos 6 arquivos, exatamente,
foram reportados como indisponíveis por `RESULTS_PRIMARY.md` §1.1 — coincidência
completa, obtida de forma totalmente independente (nova busca na API, novo
download, nova verificação de MD5, nova checagem de `computed_md5`/`mimetype`).

---

## 3. Etapa 2 — Duplicatas de conteúdo (checagem independente)

Antes mesmo de rodar o pipeline de sinal, computei MD5 dos 58 arquivos
efetivamente baixados nesta sessão e busquei grupos com MD5 idêntico:

```
723217c6472d66e05cfef4fb122ccafe → H S27 EC.edf, H S30 EC.edf
4c16e8636fca72ae59711c0ba803349f → MDD S33 EC.edf, MDD S34 EC.edf
```

Exatamente os **2 mesmos pares** reportados por `RESULTS_PRIMARY.md` §1.2,
confirmados aqui de forma totalmente independente (MD5 dos bytes
efetivamente baixados nesta sessão, não uma leitura do `computed_md5`/
`supplied_md5` já presente na listagem da API — embora eu também tenha
conferido que a API já os lista como idênticos, segunda corroboração).
Nenhum outro par duplicado existe entre os 58.

`PREREGISTRATION.md` não declara regra de deduplicação — segui a mesma
lógica do agente primário (não introduzir uma regra nova depois de ver o
dado): veredito primário usa todos os 58 arquivos disponíveis que passam a
regra de artefato, sem deduplicação; uma checagem de sensibilidade
secundária com deduplicação é reportada à parte (§6 abaixo).

---

## 4. Etapa 3 — Pipeline de sinal (independente, resultado travado antes de ler o código primário)

**Regra de rejeição de artefato aplicada:** 2 sujeitos excluídos, ambos HC:

| Sujeito | Janelas rejeitadas/totais | Fração |
|---|---|---|
| `H S5 EC.edf` | 150/150 | 100,0% |
| `H S19 EC.edf` | 113/149 | 75,8% |

**N final (antes de dedup, como pré-registrado):** MDD = 30, HC = 26 — dos
64 nominais, `64 − 6 (indisponíveis) − 2 (regra de artefato, ambos HC) = 56`
com `Ī(X)` computável; `30` sobreviveram no grupo MDD (nenhum excluído por
artefato) e `26` no grupo HC.

---

## 5. Etapa 4 — Estatística de teste (travada, computada antes de ler qualquer resultado primário)

| Estatística | Meu resultado independente |
|---|---|
| `Ī(X)` média MDD (N=30) | `0,761322` (DP `0,059954`) |
| `Ī(X)` média HC (N=26) | `0,655848` (DP `0,085486`) |
| Teste t de Welch, bicaudal | `t = 5,267803`, `df = 43,97` |
| `p` (t de Welch) | `3,9699×10⁻⁶` |
| Mann-Whitney U | `U₁ = 668,0`, `p = 5,1399×10⁻⁶` |
| Cohen's `d` (SD combinado) | `1,44692` |
| Direção observada | `Ī(X)_MDD > Ī(X)_HC` (oposta à prevista por `H_Tamesis`) |
| **Veredito por `PREREGISTRATION.md` §6** | **REFUTA** |

**Controle de potência bruta de banda (§5.3, descritivo, não decide o veredito):**

| | MDD (N=30) | HC (N=26) |
|---|---|---|
| Potência bruta média (µV²) | `334,04` | `386,49` |

Direção: **HC > MDD** em potência bruta — **oposta** à direção de `Ī(X)`
(onde MDD > HC). `t = −0,90`, `p = 0,372` (teste t, não significativo);
Mann-Whitney `p = 0,046` (marginal). Isto confirma independentemente a
observação do agente primário de que `Ī(X)` não é simplesmente um
reflexo de reescalonamento de amplitude — as duas estatísticas nem sequer
vão na mesma direção entre os grupos.

**Checagem de sensibilidade com deduplicação (secundária, não decide o
veredito):** removendo um membro de cada par duplicado (`HC_S30`,
`MDD_S34`): N=29 MDD/25 HC, `t=4,981`, `p=1,192×10⁻⁵`, `d=1,399`, mesma
direção. O resultado é robusto à anomalia de duplicação.

---

## 6. Comparação número-a-número com o agente primário (lido só depois do lock acima)

| Estatística | Agente primário (`result_primary.json`) | Este agente (independente) | Diferença |
|---|---|---|---|
| N (MDD/HC) | 30 / 26 | 30 / 26 | 0 |
| `Ī(X)` média MDD | `0,7613215123803535` | `0,7613215123803535` | `0` |
| `Ī(X)` média HC | `0,6558480762744361` | `0,6558480762744361` | `0` |
| `t` de Welch | `5,267803241827417` | `5,267803241827418` | `8,9×10⁻¹⁶` |
| `p` (t de Welch) | `3,9698512229958×10⁻⁶` | `3,969851223084575×10⁻⁶` | `~9×10⁻¹⁴` (relativa) |
| Mann-Whitney U | `668,0` | `668,0` | `0` |
| Mann-Whitney `p` | `5,136148×10⁻⁶` | `5,139892×10⁻⁶` | `~4×10⁻⁹` (relativa) |
| Cohen's `d` | `1,4469207347494795` | `1,4469207347494795` | `0` |
| Potência bruta MDD | `334,0443537423731` | `334,04435374237306` | `~10⁻¹³` |
| Potência bruta HC | `386,4900509788417` | `386,4900509788417` | `0` |
| Sujeitos excluídos (artefato) | `H S5 (100%)`, `H S19 (75,8%)` | idêntico | — |
| Arquivos indisponíveis (404) | 6, mesma lista exata | idêntico | — |
| Pares duplicados | `H S27≡H S30`, `MDD S33≡MDD S34` | idêntico | — |
| Dedup: `t`/`p`/`d` | `4,980577` / `1,1922×10⁻⁵` / `1,398538` | `4,980577366434373` / `1,1922×10⁻⁵` / `1,3985380255830155` | `<10⁻⁹` |
| Direção | `Ī(X)_MDD > Ī(X)_HC` | idêntica | — |
| Veredito | `REFUTA` | `REFUTA` | — |

**Valores por sujeito** (`Ī(X)`, potência bruta, contagem de janelas
rejeitadas) foram comparados individualmente contra a tabela completa de
`RESULTS_PRIMARY.md` §5 para todos os 56 sujeitos válidos: diferença
máxima absoluta em `Ī(X)` de `4,8×10⁻⁵` — inteiramente explicada pelo
arredondamento de exibição a 4 casas decimais da tabela do relatório
primário (não uma diferença real de cálculo). Os dois sujeitos excluídos
(`H S5`, `H S19`) e as duas frações de rejeição de janela correspondentes
batem exatamente. Ver `adversarial/results/result_adversarial.json` →
`comparison_to_primary_analysis` para os números completos gerados por
script (não digitados manualmente).

As diferenças remanescentes (`~10⁻¹³` a `~10⁻⁹`, sempre no nível de
precisão de ponto flutuante) são consistentes com ordem de soma diferente
entre duas implementações de Welch/entropia escritas de forma
independente, e com o agente primário usar `scipy.special`/`scipy.stats`
diretamente para o p-valor onde eu implementei minha própria avaliação da
função beta incompleta — **não** indicam nenhuma divergência de método.

---

## 7. Checagens específicas de bug pedidas pela tarefa adversarial

| Checagem pedida | Resultado |
|---|---|
| Convenção da janela Hann (periódica vs. simétrica) | **Periódica** (`fftbins=True`), confirmada empiricamente como o comportamento real de `scipy.signal.get_window('hann', N)`/`scipy.signal.welch(window='hann')`, e é o que ambos os pipelines (o meu e o primário) implementam. Usar a convenção simétrica por engano teria introduzido um viés sistemático pequeno mas real; não foi o caso em nenhum dos dois. |
| Normalização da entropia (`log2(N)`, `N` = bins em `R_λ`, não bins totais do FFT) | Confirmado: `N=157` (banda `[1,40]`Hz a 0,25Hz de resolução), não `513` (bins totais do FFT unilateral de 1024 pontos). Usar `N=513` por engano teria deflacionado artificialmente todo `Ī(X)` (denominador maior) sem afetar a diferença de grupo de forma óbvia, mas seria um desvio do texto de `PREREGISTRATION.md` §2 ("`N` bins de frequência ... `∈ R_λ`"). Não ocorreu em nenhum pipeline. |
| Máscara de rejeição compartilhada entre os 19 canais (não independente por canal) | Confirmado em ambos os pipelines: `window_rejected = channel_exceeds.any(axis=0)` (meu) / `reject[wi] = True` atualizado dentro de um loop sobre os 19 canais que escreve no mesmo array `reject` (primário) — mesma semântica, uma única máscara por sujeito. |
| Ordem de médias (janela→canal→sujeito, não outra ordem) | Confirmado em ambos: `I(X)` por janela por canal → média sobre janelas não rejeitadas (por canal) → média sobre 19 canais. Esta é uma leitura não trivial de `PREREGISTRATION.md` (§2 sozinho sugeriria "um `I(X)` por canal a partir do PSD já médio-Welch do sinal inteiro"; §4.5 exige explicitamente "média de `I(X)` sobre as janelas"). Cheguei a essa leitura **antes** de ler o código do agente primário, que documenta exatamente o mesmo raciocínio textual em um comentário (`run_primary_analysis.py`, linhas ~526-530) — convergência independente sobre a mesma ambiguidade, não cópia. |
| Direção "oposta, efeito grande" é real ou artefato (rotulagem de canal, erro de unidade, bug de escala do Welch, peculiaridade do parsing EDF+ deste dataset) | Nenhum artefato encontrado. Rótulos de canal conferem (`EEG {nome}-LE`, 19/19 presentes e idênticos entre grupos); unidades em µV (`phys_dim='uV'`) processadas corretamente (cross-validado contra `pyedflib`); escala de densidade do Welch cross-validada contra `scipy.signal.welch` a `10⁻¹⁵`; o canal de anotações EDF+ (`EDF Annotations`) e os até 2 canais auxiliares (`23A-23R`, `24A-24R`) são corretamente excluídos dos 19 canais nomeados (nunca entram no cálculo). O efeito é reproduzido de forma numericamente idêntica por um pipeline construído do zero. |
| Direção da potência de banda bruta (§5.3) | Confirmada de forma independente: HC > MDD em potência bruta, oposta à direção de `Ī(X)` — mesmo padrão relatado pelo agente primário. |

---

## 8. Achados adicionais / ressalva honesta (não invalida o veredito)

- **Os 2 pares de arquivo duplicado permanecem no N=30/26 primário sem
  deduplicação** (nem `PREREGISTRATION.md` nem `RESULTS_PRIMARY.md`
  declaram uma regra de dedup). Isto significa que, tecnicamente, 2 dos 56
  pontos de dado não são estatisticamente independentes das suas
  contrapartes (`HC_S27`≡`HC_S30`, `MDD_S33`≡`MDD_S34`), uma violação leve
  do pressuposto de independência do teste t/Mann-Whitney. Isto **não** é
  um bug de nenhum dos dois pipelines — é uma característica do dataset
  publicado em si (upload duplicado, dois IDs de sujeito para a mesma
  gravação) — e a checagem de sensibilidade com dedup (§5–§6 acima) mostra
  que o resultado sobrevive removendo a duplicação (`p=1,19×10⁻⁵`, mesma
  direção). Ambos os relatórios (primário e este) marcam isto explicitamente
  como uma anomalia de proveniência do dataset, não escondida.
- Nenhuma outra anomalia foi encontrada: contagem de canais (19/19),
  taxa de amostragem (256 Hz exato) e presença dos rótulos `-LE` conferem
  para todos os 58 sujeitos com dado disponível.

---

## 9. Conclusão

**Veredito adversarial: CONFIRMADO.** Um pipeline construído inteiramente
do zero por um agente diferente — leitor EDF próprio, estimador de Welch
próprio, entropia de Shannon própria, regra de rejeição de artefato
própria, teste t de Welch e Mann-Whitney próprios, nova busca e novo
download independentes do dataset via a API pública do Figshare —
reproduz o resultado REFUTA do agente primário com concordância numérica
até a precisão de ponto flutuante em toda estatística de decisão (`t`,
`p`, `d`, `U`, médias/DP de grupo) e até arredondamento de exibição em
todo valor por sujeito. As mesmas 6 ausências de arquivo (404, corroboradas
independentemente via `computed_md5`/`mimetype` da própria API) e os mesmos
2 pares de conteúdo duplicado (confirmados por MD5 dos bytes efetivamente
baixados nesta sessão) foram encontrados de forma totalmente independente.
Nenhum bug foi encontrado nas checagens específicas pedidas (convenção de
janela, normalização de entropia, compartilhamento da máscara de rejeição
entre canais, ordem de médias, direção do controle de potência bruta).

Por `AGENTS.md`, este veredito de reexecução adversarial (passo 7) autoriza
o resultado `DISC-COGNITIVE-EEG-SPECTRAL-001` (braço depressão) a ser
catalogado em `01_PORTFOLIO/TEST_QUEUE.yaml`/`00_GOVERNANCE/CLAIM_LEDGER.yaml`
como **REFUTA, reproduzido de forma independente** — não como "Tamesis
refutado" em sentido amplo, nem como "Sun et al. 2019 confirmado": apenas
como o resultado deste teste único, pré-registrado, sobre este dataset,
nesta condição (`EC`), agora com reexecução adversarial concluída conforme
exigido. Nenhuma alegação diagnóstica, clínica, ou sobre Problemas do
Millennium é feita aqui (`AGENTS.md`, "Proibições"; `PREREGISTRATION.md`
§9).

**Nenhum arquivo `.edf` bruto foi retido** após o cálculo — os 58 arquivos
baixados e verificados por MD5 nesta sessão foram removidos imediatamente
após o processamento de cada um (mesmo precedente de privacidade já
documentado em `data/DOWNLOAD_VERIFICATION_MUMTAZ.log` e em
`RESULTS_PRIMARY.md` §9, dado que o campo `patient_id` do cabeçalho EDF
deste dataset contém strings que se parecem com nomes reais de sujeitos).

---

## 10. Inventário de arquivos desta reexecução adversarial

- `adversarial/scripts/edf_reader.py` — leitor EDF próprio.
- `adversarial/scripts/welch_entropy.py` — Welch PSD e entropia de Shannon próprios.
- `adversarial/scripts/pipeline.py` — download/MD5, rejeição de artefato, pipeline por sujeito.
- `adversarial/scripts/stats_own.py` — teste t de Welch e Mann-Whitney U próprios.
- `adversarial/scripts/run_all.py` — script executor que baixa e processa os 64 arquivos.
- `adversarial/scripts/build_result_adversarial.py` — script que computa as estatísticas de grupo finais e a comparação com o resultado primário (gerado por código, não digitado manualmente).
- `adversarial/results/figshare_4244171_meta_adversarial_fetch.json` — metadados da API do Figshare, buscados de forma independente nesta sessão.
- `adversarial/results/adversarial_per_subject.json` — resultado completo por sujeito (todos os 64 arquivos tentados, incluindo os 6 indisponíveis).
- `adversarial/results/adversarial_download_log.txt` — log completo de download/processamento desta sessão.
- `adversarial/results/result_adversarial.json` — sumário final de decisão + comparação número-a-número com o resultado primário.
- `adversarial/ADVERSARIAL_VERDICT.md` — este documento.

**Nenhum arquivo do agente primário foi modificado** (`PREREGISTRATION.md`,
`RESULTS_PRIMARY.md`, `results/*.json`, `analysis/run_primary_analysis.py`
permanecem exatamente como estavam antes desta sessão).
