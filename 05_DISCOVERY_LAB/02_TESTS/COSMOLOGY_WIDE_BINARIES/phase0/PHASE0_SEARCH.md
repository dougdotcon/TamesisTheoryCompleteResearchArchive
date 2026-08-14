# DISC-COSMOLOGY-MOND-SPARC-003 — Fase 0: busca de formulação

**Data:** 2026-08-14. Três agentes independentes investigaram em
paralelo, a pedido do usuário, o que uma terceira linha de teste
cosmológico/MOND poderia ser, dado que `SPARC-001` (piloto EFE,
`CLOSED_INCONCLUSIVE`) e `SPARC-002` (derivação de `a0`,
`REPLICATION_FAILED_INCONCLUSIVE`) já esgotaram os testes óbvios sobre
o catálogo SPARC.

## Rota 1 — busca exaustiva por nova alegação Tamesis-específica: NEGATIVA

Varredura completa de `01_TAMESIS_CORE` (EFE, Holographic Uniqueness,
Operational Derivation, Cosmology, Killer Prediction, Falsification
Criteria) não encontrou nenhuma previsão quantitativa Tamesis-específica
sobre dinâmica de baixa aceleração ainda não coberta por SPARC-001/002.
Achados relevantes, todos descartados como base de teste:

- A função de interpolação "derivada" por unicidade holográfica
  (`02_Holographic_Uniqueness/interpolation_derivation.py:23`) é
  **numericamente idêntica** (divergência zero) à função "Simple"
  padrão de Milgrom/Famaey & Binney — não é uma forma distinta.
- A função "TAMESIS" `ν(x)=1/(1−e^(−√x))`
  (`MOND_EFE/paper_validacao_galactica/index.html:1100`) é a própria
  curva empírica de McGaugh, Lelli & Schombert (2016) usada para
  *definir* `a0` na literatura — rebatizada, não nova.
- O teste EFE aglomerado-vs-campo (`MOND_EFE/efe/index.html:863-905`)
  usa o MESMO dataset (Ursa Maior) e a mesma classe de teste que
  `SPARC-001` já rodou — repeti-lo seria duplicar, não abrir linha nova.
- A correlação M/L vs. `g_ext` (`efe/index.html:503-645`) já foi
  auto-refutada dentro do próprio corpus (r=0,552, direção oposta à
  prevista; seção 5.5 do mesmo documento atribui isso a confundimento
  por distância, não ao EFE).
- BTFR `v⁴=GMa0` é corolário direto do mesmo `a0` já adjudicado, não
  alegação independente.
- Tensão de Hubble via `η(a)`: sem previsão a priori testável contra
  curvas de rotação, fora de escopo.
- Lente gravitacional em aglomerados (Bullet Cluster): fórmula com termo
  não especificado (`f(N_galaxies)`), sem calibração contra dado real,
  não falsificável como está.

## Rota 2 — discrepância de leverage do holdout de SPARC-002 como germe de teste: NEGATIVA

Investigação com Monte Carlo (5000 subamostras aleatórias de 55 galáxias
do catálogo de 175) mostrou que a concentração de leverage observada no
holdout real (91,7% nas top-3) cai no percentil ~78 da distribuição
esperada por acaso — não é um outlier estatístico. O mecanismo é
genérico (mínimos quadrados não-ponderados em espaço linear dominados
por poucos pontos de `g_bar` extremo, já autodocumentado no próprio
`result_adversarial.json` de SPARC-002 via a comparação linear-vs-log,
~21% de diferença em `g†` só pela escolha de espaço da perda). Mais
importante: não existe, em `01_TAMESIS_CORE`, nenhuma alegação sobre
comportamento/instabilidade em regime de alta aceleração — a função de
interpolação de Tamesis é comprovadamente idêntica à "Simple" MOND
padrão em TODO o domínio, inclusive no limite Newtoniano. Sem modelo
concorrente nomeado possível aqui (Tamesis = MOND padrão neste regime),
a rota falha o requisito de identificabilidade
(`METHODOLOGY_EXTENSIONS.md` Seção 1) na largada.

## Rota 3 — dataset independente para replicar o veredito de SPARC-002: POSITIVA, com achado de integridade grave

Busca por dado real de baixa aceleração fora do catálogo SPARC
confirmou: **binárias largas do Gaia (El-Badry, Rix & Heintz 2021, MNRAS
506, 2269)** são reais, públicas, sem login, volumosas (catálogo
completo ≈1,94 GB, 1.817.594 pares; amostra de 2000 linhas baixada e
inspecionada, conteúdo astrométrico genuíno confirmado) — exatamente o
catálogo usado por Chae (2023, ApJ 952, 128) para testar quebra de
gravidade padrão em regime de aceleração ultra-baixa, de forma
totalmente independente de curvas de rotação galácticas. Anãs
esferoidais (McConnachie 2012) também são reais e públicas, mas
estatisticamente fracas demais para base primária.

**Achado de integridade grave, descoberto durante a mesma busca:**
`01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE/lab_gravity/analysis/gaia_real_analysis.py`
contém uma lista `REAL_GAIA_BINARIES` (linhas 72-109), rotulada no
docstring como dados reais de "El-Badry et al. 2021, Table 1 + Chae
2023" — mas os `source_id` do Gaia são sequenciais/artificiais (padrão
que não ocorre em IDs reais) e a progressão de velocidades é
monotônica demais, projetada para reproduzir o boost MOND esperado. O
achado "MOND DETECTED" citado em `RESEARCH_RESULTS.md:259-261`
(`v/v_N = 1,308 ± 0,216, p=0,000017`) descansa sobre este dado
fabricado — mesmo padrão do achado original que motivou a criação desta
trilha (curvas de rotação de Virgem fabricadas em
`AUDIT_LEGACY_MOND_EFE_SPARC.md`). `lab_gravity/AUDITORIA.md` já
sinaliza contaminação/binárias não-resolvidas de forma genérica, mas
NÃO menciona que o dataset embutido é sintético.

## Formulação recomendada para `DISC-COSMOLOGY-MOND-SPARC-003`

Auditar e refazer o teste de binárias largas com dado REAL do catálogo
El-Badry et al. (2021), substituindo a tabela fabricada, testando as
MESMAS duas hipóteses já travadas em `SPARC-002` (`H_A: a0=cH0/2π` vs.
`H_B: a0=cH0`) — sem reformular a alegação, apenas adaptando o
observável discriminador ao novo sistema físico (binário Kepleriano de
dois corpos, não disco rotativo integrado), conforme
`METHODOLOGY_EXTENSIONS.md` Seção 1 permite. Isso daria um veredito
independente do catálogo SPARC inteiro sobre a pergunta que o Gate de
Replicação de `SPARC-002` deixou inconclusiva (holdout não confirmou
nem refutou `H_A`).

**Antes de qualquer pré-registro, ainda faltaria:** (a) buscar/verificar
por fetch direto a fórmula exata do estimador de velocidade normalizada
de Chae (2023) — razão entre velocidade relativa observada e velocidade
Kepleriana Newtoniana prevista, em função de `g_N=GM/r²` — não assumida
de memória; (b) declarar o corte de qualidade (`R<0.1`, faixa de
separação, remoção de triplas) como parte do pré-registro; (c) declarar
split discovery/holdout novo e próprio (esta fonte nunca foi usada nesta
trilha).

## O que NÃO se recomenda

Não travar `SPARC-003` como teste de uma nova fórmula teórica — a busca
exaustiva (Rota 1) não encontrou nenhuma. O caminho honesto é tratar
`SPARC-003` como réplica independente do veredito de `SPARC-002`, não
como confirmação/refutação de uma alegação nova.
