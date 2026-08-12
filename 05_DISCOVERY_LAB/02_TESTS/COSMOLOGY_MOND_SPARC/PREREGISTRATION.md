# Pré-registro: EFE em curvas de rotação SPARC reais — aglomerado de Ursa Maior vs. campo

**Status:** LOCKED
**Data de criação:** 2026-08-12
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-12 (Claude Code)
**Commit em que foi travado:** registrado em `01_PORTFOLIO/TEST_QUEUE.yaml` /
`00_GOVERNANCE/CLAIM_LEDGER.yaml` logo após o commit que introduz este
arquivo (ver histórico git de `02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md`).

> Preenchido e commitado ANTES de calcular qualquer estatística sobre as
> curvas de rotação reais. Os arquivos de dado (`data/SPARC_Lelli2016c.mrt`,
> `data/Rotmod_LTG/*.dat`) já foram baixados e verificados
> (`data/PROVENANCE.md`), mas neste momento nenhuma inclinação, média,
> t-teste ou p-valor foi computado a partir deles.

## 0. Por que o desenho original (Virgem vs. campo) foi abandonado

O teste legado (`AUDIT_LEGACY_MOND_EFE_SPARC.md`, Achado 5) comparava 8
galáxias "de Virgem" que não existem no catálogo SPARC público real. Ao
verificar diretamente `data/SPARC_Lelli2016c.mrt`, confirmou-se que
**nenhuma** das 13 espirais de Virgem citadas na literatura pelo script
legado está presente nas 175 galáxias do SPARC real. Refazer o teste
"Virgem vs. campo" exigiria uma fonte externa de membership de aglomerado
não verificável nesta sessão por fetch direto contra o próprio dado em mãos.
Em vez disso, este pré-registro usa uma classificação de ambiente **nativa
do próprio catálogo**: a coluna `f_D` (método de distância), cujo valor `4`
é documentado no cabeçalho do `.mrt` como
`"4 = Ursa Major Cluster of Galaxies"`. Isso troca Virgem (aglomerado
massivo, ausente da amostra) por Ursa Maior (aglomerado real, presente e
identificável na amostra) — uma mudança de escopo, não uma reformulação do
critério depois de ver o resultado (nenhum resultado foi visto ainda).

## 1. Hipótese exata

Fonte teórica: `01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE/efe/index.html:271-309`
(formulação MOND/EFE padrão, $g=g_N/\mu(g/a_0)$ com
$\mu(x)=x/\sqrt{1+x^2}$; para campo externo forte,
$g_{EFE}\approx g_N/\mu(g_{ext}/a_0)$) e `index.html:337-344`
(predição quantitativa: para $g_{ext}/a_0\approx1.25$, supressão de
velocidade de ~65%, ou seja $V_{sat}/V_{iso}\approx0.35\pm0.05$).

Hipótese testável aqui (versão qualitativa da mesma predição, aplicada à
estatística disponível): **galáxias SPARC classificadas como membros do
aglomerado de Ursa Maior (`f_D=4`) têm inclinação externa da curva de
rotação (outer log-log slope) sistematicamente mais negativa (mais
declinante) do que galáxias SPARC não-membro de aglomerado conhecido no
catálogo (`f_D≠4`)**, na direção prevista pelo EFE.

Nota de calibração: o aglomerado de Ursa Maior é substancialmente menos
massivo que Virgem (dispersão de velocidades ~150 km/s vs. ~750 km/s), logo
$g_{ext}/a_0$ esperado para seus membros é menor que o caso $1.25$ usado na
predição quantitativa de 65% acima. Este teste portanto avalia a **direção**
do efeito (sinal do EFE, não sua magnitude de 65%) — ver Seção 7.

## 2. Fonte de dado

- Dataset: SPARC (Lelli, McGaugh & Schombert 2016, AJ 152, 157)
- URL exata (verificada por fetch direto): `https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt`
  e `https://astroweb.case.edu/SPARC/Rotmod_LTG.zip`
- Proveniência completa: `data/PROVENANCE.md`
- Tamanho esperado: 175 galáxias no catálogo; 175 arquivos de curva de
  rotação individual (já verificado antes deste pré-registro, contagem de
  arquivos é proveniência, não é resultado do teste).
- Grupo "aglomerado": galáxias com `f_D=4` no `.mrt` — **N=28**, já contado
  por script de proveniência (lista de nomes registrada em
  `data/PROVENANCE.md`; a contagem N=28 é metadado do catálogo, não uma
  estatística do teste de hipótese, por isso pode ser citada aqui sem violar
  o lock).
- Grupo "campo": as demais 147 galáxias do catálogo (`f_D≠4`) que possuam
  arquivo `Rotmod_LTG/<nome>_rotmod.dat` com pelo menos 4 pontos observados
  (mínimo para a estatística da Seção 4 ter sentido com metade externa
  ≥2 pontos).

## 3. Modelo nulo / hipótese concorrente

ΛCDM / Relatividade Geral não-modificada com halo de matéria escura: pelo
Princípio da Equivalência Forte, a dinâmica interna de uma galáxia não
depende do campo gravitacional externo uniforme em que está embebida
(`efe/index.html:268-269`). Sob o modelo nulo, a inclinação externa média
das curvas de rotação do grupo "aglomerado" (Ursa Maior) e do grupo "campo"
não deve diferir sistematicamente — a diferença esperada é zero, e qualquer
diferença observada é atribuível a ruído amostral, não a um efeito de campo
externo.

## 4. Estatística de teste

Para cada galáxia, usando os pontos `(Rad, Vobs)` reais do arquivo
`Rotmod_LTG/<nome>_rotmod.dat`:

1. Tomar a metade externa dos pontos ordenados por raio (`r_outer = r[n//2:]`,
   `v_outer = v[n//2:]`, mesma definição de
   `sparc_slope_analysis.py:237-242`, agora aplicada a dado real).
2. Se `len(r_outer) < 2`, excluir a galáxia da amostra (registrar exclusão).
3. Ajuste log-log linear: `slope = polyfit(log(r_outer), log(v_outer), 1)[0]`.
4. Comparar a média de `slope` entre o grupo aglomerado e o grupo campo via
   teste t de Welch (variâncias não assumidas iguais, dado os tamanhos de
   amostra muito diferentes: N≈28 vs. N≈147).

Esta é a mesma estatística definida no código legado
(`AUDIT_LEGACY_MOND_EFE_SPARC.md`, "O que é real e reaproveitável"), agora
computada exclusivamente a partir dos arquivos `Rotmod_LTG/*.dat` reais —
nenhum valor literal do código legado é reutilizado.

## 5. Critério de falsificação

- **Suporta EFE:** média(slope, aglomerado) < média(slope, campo) **E**
  p < 0.05 (teste t de Welch, uma cauda, na direção prevista).
- **Falsifica / não suporta EFE:** p ≥ 0.05, OU a diferença observada tem
  sinal oposto ao previsto (aglomerado com slope mais positivo/plano que
  campo).
- **Zona "não distingue" (declarada a priori, não reinterpretável depois):**
  nenhuma — o critério acima já cobre os dois desfechos possíveis
  binariamente pela combinação de sinal e p-valor; não há terceira categoria
  a ser inventada após ver o resultado. Se p estiver marginalmente próximo
  de 0.05 (entre 0.04 e 0.06), o relatório final deve declarar isso
  explicitamente como resultado frágil, mas ainda classificado pelo critério
  binário acima.

## 6. Correção para comparações múltiplas

Esta é uma única comparação planejada (um grupo aglomerado vs. um grupo
campo, uma estatística, um teste). Nenhuma outra partição do catálogo,
nenhum outro subconjunto de galáxias e nenhuma outra estatística (BTFR,
V_flat bruto, etc.) será testada como parte deste pré-registro. Se, depois
de ver o resultado, houver interesse em testar outra partição (ex.
`f_D=1` isolado vs. resto, ou magnitude do efeito em vez de só direção),
isso constitui um **novo** pré-registro (novo arquivo), não uma reanálise
deste.

## 7. O que NÃO está sendo testado

- Este teste **não** avalia a predição quantitativa de 65% de supressão
  (`efe/index.html:343`) — essa predição foi calibrada para
  $g_{ext}/a_0=1.25$ (típico de satélite da Via Láctea), e o aglomerado de
  Ursa Maior tem campo externo esperado mais fraco. Um resultado positivo
  aqui é evidência de **direção** consistente com EFE, não confirmação da
  magnitude de 65%.
- Este teste **não** avalia nem replica a metodologia de Chae, Lelli,
  McGaugh et al. (2020, ApJ 904, 51; verificado via busca nesta sessão),
  que detectou EFE usando estimativas de campo externo de estrutura em
  grande escala — uma abordagem estatisticamente muito mais sofisticada.
  Um resultado nulo ou positivo aqui não confirma nem contradiz aquele
  resultado publicado, dado o desenho e poder estatístico muito diferentes.
- Este teste **não** constitui confirmação de "Tamesis" como framework
  distinto de MOND — testa a predição EFE genérica de MOND/gravidade
  entrópica, da qual Tamesis alega derivar, não uma predição exclusiva de
  Tamesis.
- Nenhum resultado deste teste, seja qual for, implica progresso em
  qualquer Problema do Millennium.
- Este teste não corrige nem controla efeitos de seleção morfológica,
  qualidade da curva (`Q` flag), ou inclinação — essas são limitações
  conhecidas a serem discutidas no relatório final, não motivos para
  reformular o critério de falsificação depois do fato.

---

## [Preenchido depois da análise] Resultado

*(a preencher após execução do script de análise sobre `data/Rotmod_LTG/*.dat`)*

## [Preenchido depois da reexecução adversarial] Veredito adversarial

*(a preencher por um agente independente)*
