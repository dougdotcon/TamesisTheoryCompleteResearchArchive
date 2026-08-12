# Auditoria: `01_TAMESIS_CORE/02_Experimental_Validation/{MOND_EFE,Cosmology}`

**Data:** 2026-08-12
**Escopo:** os scripts e páginas ligados ao teste de External Field Effect
(EFE) com dados SPARC/Gaia, e o texto publicado em `efe/README.md` e
`efe/index.html`. Esta auditoria não afirma más intenções — documenta o que
o código e os dados realmente fazem, para que a trilha de descoberta possa
refazer o teste com disciplina.

## Achado 1 — URL de download quebrada, nunca funcional

`efe/simulations/sparc_real_download.py:41-48`:

```python
SPARC_SOURCES = [
    "http://astroweb.cwru.edu/SPARC/",
    "https://raw.githubusercontent.com/ManuelBeh);rendt/sparc/main/data/",
    "https://zenodo.org/record/sparc/files/",
]
```

A segunda URL contém um typo estrutural (`ManuelBeh);rendt` — parêntese e
ponto-e-vírgula no meio do path) que a torna sintaticamente inválida como
nome de usuário GitHub; nunca poderia ter resolvido. A primeira URL usa o
domínio antigo do SPARC (`astroweb.cwru.edu`), que não é mais o domínio
correto (a versão atual está em `astroweb.case.edu`, confirmado por fetch
direto nesta sessão — ver `data/PROVENANCE.md`). `sparc_loader.py:26-27` usa
o mesmo domínio antigo.

## Achado 2 — Verificação TLS desabilitada

`efe/simulations/sparc_real_download.py:28-31`:

```python
# Disable SSL verification for problematic servers
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

Desabilitar a verificação de certificado para "resolver" uma falha de rede é
exatamente a prática que `00_GOVERNANCE/AGENTS.md` desta trilha proíbe
explicitamente.

## Achado 3 — Fallback silencioso para catálogo embutido, disfarçado de dado real

`sparc_real_download.py:520-522`:

```python
if not downloaded:
    print("\n[!] Could not download SPARC files from server.")
    print("    Using embedded catalog data instead.")
```

O catálogo embutido (`SPARC_CATALOG`, linhas 59-209, ~150 galáxias com
distância/luminosidade/V_flat digitados diretamente no código-fonte) é usado
sempre, já que o download nunca teve chance de funcionar (Achado 1). A
função que efetivamente roda a análise (`analyze_real_sparc`, linha 346) lê
exclusivamente desse catálogo embutido via `parse_sparc_catalog()` (linha
276) — nunca há um caminho de código que leia um arquivo `.mrt` real baixado.
O nome da função (`analyze_real_sparc`) e os prints ("REAL SPARC", linha
371) descrevem o resultado como dado real quando é, na prática, sempre dado
digitado à mão no próprio script.

## Achado 4 — O resultado manchete ("EFE CONFIRMED", p<0.000001) vem de um segundo script com curvas de rotação inteiramente digitadas à mão

O badge de status em `efe/README.md:1-5` ("CONFIRMED", "EFE_DETECTED",
"p-value < 0.000001") e a tabela de 8 galáxias de Virgem "100% declining"
(`efe/README.md:24-37`) não vêm de `sparc_real_download.py` — vêm de
`efe/simulations/sparc_slope_analysis.py`. Esse script define
`VIRGO_ROTATION_CURVES` e `FIELD_ROTATION_CURVES`
(`sparc_slope_analysis.py:32-217`) como dicionários Python com pares
`(raio_kpc, velocidade_km/s)` digitados diretamente no código-fonte,
comentados como `"ACTUAL SPARC ROTATION CURVE DATA"` (linha 25) e
`"REAL observed rotation curves"` (linhas 31, 115) — mas **não há, em
nenhum lugar do script, uma chamada de leitura de arquivo, download, ou
parsing de dado externo**. A função `analyze_rotation_curves` (linha 255) e
`main()` (linha 286) operam inteiramente sobre esses literais.

## Achado 5 — As 8 galáxias de Virgem "reais" da manchete não existem no catálogo público SPARC real

Verificação direta nesta sessão: nenhuma das 13 galáxias listadas como
`VIRGO_MEMBERS` em `sparc_real_download.py:212-216` (NGC4192, NGC4254,
NGC4303, NGC4321, NGC4501, NGC4535, NGC4536, NGC4548, NGC4569, NGC4579,
NGC4654, NGC4689, NGC4698 — todas espirais de Virgem bem conhecidas na
literatura, ex. M100=NGC4321, M99=NGC4254, M98=NGC4192, M88=NGC4501,
M90=NGC4569, M58=NGC4579) aparece no catálogo `SPARC_Lelli2016c.mrt` real
baixado nesta sessão (175 galáxias, verificado por busca exata de string —
ver `data/PROVENANCE.md`). Isso é consistente com um fato astronômico real e
documentado na literatura SPARC: o SPARC prioriza galáxias com curvas HI
estendidas de alta qualidade, e espirais de Virgem sofrem deficiência de HI
por "ram-pressure stripping" do meio intra-aglomerado, o que historicamente
reduz sua representação em amostras baseadas em HI como o SPARC. Ou seja: as
8 galáxias "reais" do resultado manchete não são apenas digitadas à mão —
elas nem sequer fazem parte da amostra pública que o repositório cita como
sua fonte. Os números de velocidade/raio usados para elas em
`sparc_slope_analysis.py` não têm proveniência rastreável nesta auditoria.

## Achado 6 — Heurística grosseira para campo externo (afeta `sparc_real_download.py`, não usada no resultado manchete)

`sparc_real_download.py:322-339` (`estimate_g_external`) assume que **toda**
galáxia de Virgem está a exatamente 500 kpc do centro do aglomerado
(`calculate_external_field(500, VIRGO_MASS)`, linha 331) e toda galáxia de
Fornax a 400 kpc (linha 335) — não usa nenhuma posição 3D real medida por
galáxia. Isso não afeta o resultado manchete (Achado 4-5), mas é um segundo
problema metodológico independente no mesmo arquivo.

## Achado 7 — `sparc_loader.py` nunca implementa o parser real, mesmo quando o arquivo `.mrt` real está presente

`sparc_loader.py:195-210` (`load_real_sparc`): mesmo se o arquivo `.mrt` real
existir em disco, a função imprime `"Note: Full SPARC parser not
implemented. Using synthetic data."` (linha 209) e chama
`_create_synthetic_data()` (linha 113) incondicionalmente. Os dados
sintéticos (linhas 117-193) não são nem mesmo uma amostra de um catálogo —
são gerados a partir do **próprio modelo MOND que o teste deveria estar
avaliando** (`_generate_synthetic_rc`, linha 153, chama
`MONDCalculator.rotation_velocity` com `include_efe=(g_ext > 0)`, linha 178).
Isso é circular: usar o modelo MOND/EFE para gerar os dados e depois "testar"
se os dados mostram o sinal MOND/EFE testaria apenas se o gerador e o
detector são consistentes entre si, não se MOND/EFE é real.

## Achado 8 — Correções pós-hoc já existentes no arquivo, mas incompletas

`01_TAMESIS_CORE/.../MOND_EFE/AUDITORIA.md` (2026-07-29) já reconhece que
"a previsão de 65–70% é uma saída preliminar do modelo, não observação" e que
"seleção de satélites, tides, anisotropia, binaries e ambiente devem entrar
no likelihood" — mas essa nota de auditoria não alcançou o badge
`Status-CONFIRMED` e a tabela "EFE CONFIRMED IN REAL DATA" que continuam em
`efe/README.md` e `efe/index.html` (linha ~900), nem o achado 5 acima (que a
amostra de Virgem citada não está no catálogo real). O texto de
`efe/index.html:227-229` já contém uma linguagem de pré-registro
("testável apenas após amostra pré-registrada, modelo de nuisance, e
baselines Newtoniano/ΛCDM/MOND fixados") — mas essa condição nunca foi
operacionalizada com um pré-registro real antes da análise, exatamente o
problema que esta trilha existe para corrigir.

## O que é real e reaproveitável nesta base legada

- A formulação teórica MOND/EFE em `efe/index.html:271-309` (interpolação
  $\mu(x)=x/\sqrt{1+x^2}$, $g_{EFE}\approx g_N/\mu(g_{ext}/a_0)$) é a
  formulação padrão de Milgrom (1983), citável e correta como definição do
  que está sendo testado — não é o problema. O problema é exclusivamente a
  proveniência dos dados usados para testá-la.
- A predição quantitativa em `efe/index.html:337-344`
  ($V_{sat}/V_{iso}\approx 0.35\pm0.05$ para $g_{ext}/a_0=1.25$, "EFE
  suppression: 65%") é a predição numérica citável usada como base da
  hipótese em `PREREGISTRATION.md` desta pasta.
- A estatística "inclinação externa da curva de rotação" (outer log-log
  slope), definida em `sparc_slope_analysis.py:224-252`, é uma estatística
  de teste legítima e bem definida — reaproveitada em `PREREGISTRATION.md`,
  mas recomputada a partir de dado real (`data/Rotmod_LTG/*.dat`), nunca dos
  literais hardcoded.

## Veredito da auditoria

Os resultados numéricos e a linguagem "CONFIRMED"/"DETECTED" em
`01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE/efe/` e `lab_gravity/`
**não são citáveis como evidência válida** por esta trilha ou por qualquer
trabalho futuro, até que sejam refeitos com dado real e proveniência
documentada — precisamente o que `PREREGISTRATION.md` e a execução
subsequente desta pasta (`02_TESTS/COSMOLOGY_MOND_SPARC/`) se propõem a
fazer. Isso não é uma alegação de má-fé — é uma alegação verificável, com
citação exata de arquivo:linha, de que os fallbacks e dados embutidos
descritos acima produziram uma manchete "CONFIRMED" sem nunca ter processado
o dado público real que alegam usar.
