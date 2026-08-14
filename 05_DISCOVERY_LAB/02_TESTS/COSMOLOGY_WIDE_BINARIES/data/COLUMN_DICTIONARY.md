# Dicionário de colunas — catalog.dat (El-Badry, Rix & Heintz 2021, MNRAS 506, 2269)

Fonte: `ReadMe` oficial do catálogo VizieR `J/MNRAS/506/2269`,
baixado integralmente de
`https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/506/2269/ReadMe` em 2026-08-14
(84965 bytes, cópia em `data/ReadMe`). Transcrito programaticamente do
bloco "Byte-by-byte Description of file: catalog.dat" (linhas 115-667
do ReadMe), com verificação de que a soma das larguras dos 217 campos +
216 separadores de 1 byte = 2844 bytes = Lrecl declarado.

## Formato real do arquivo (achado, não assumido)

O "byte-by-byte" do ReadMe segue o template CDS padrão (que
normalmente descreve colunas de largura fixa sem delimitador), mas a
inspeção direta do `catalog.dat.gz` mostra que os 217 campos são
efetivamente **separados por "|" (pipe)**, com cada campo ocupando
exatamente a largura declarada e um separador de 1 byte entre eles —
confirmado por amostra real (primeiros ~53 MB comprimidos
descomprimidos = 19611 linhas, todas com exatamente 2844 caracteres +
quebra de linha e 217 campos ao fazer split por "|"). Ou seja, o
arquivo pode ser lido com segurança via `pandas.read_csv(sep="|")`
usando a ordem de colunas abaixo, sem precisar de parsing por posição
de coluna (fixed-width).

## Convenção de valores nulos (achado, do próprio ReadMe)

- 78 das 217 colunas são documentadas como opcionais no ReadMe (prefixo
  "?" na explicação).
- Dentro dessas, a maioria (colunas ligadas à solução astrométrica
  eDR3: pseudocolor, scan-direction-strength, etc.) usa a sentinela
  numérica **`1.0E20`** para indicar ausência de valor (confirmado por
  amostra real: campo `pscol1` continha literalmente `1.0E20` numa
  linha real).
- As colunas ligadas ao cross-match com Gaia DR2 (`dr2plx*`,
  `dr2pmRA*`, `dr2pmDE*` e seus erros) usam **campo vazio** (string
  vazia entre pipes) quando a fonte não tem contraparte em DR2, não a
  sentinela 1e20.
- Nenhuma conversão de sentinela -> NaN foi aplicada nesta etapa de
  preparação (ver PROVENANCE.md) — os valores brutos (incluindo
  `1.0E20` literal) foram preservados no parquet para não tomar essa
  decisão de tratamento antes do pré-registro.

## Colunas-chave para o teste DISC-COSMOLOGY-MOND-SPARC-003

- `Source1`/`Source2`: `source_id` do Gaia EDR3 de cada componente.
- `RAdeg`/`DEdeg` (+ `RA2deg`/`DE2deg`): posição ICRS Ep=2016.0 de
  cada componente.
- `Plx1`/`Plx2` + `e_Plx1`/`e_Plx2`: paralaxe e erro (mas).
- `pmRA1`/`pmRA2`, `pmDE1`/`pmDE2` + erros: movimento próprio (mas/yr).
- `Gmag1`/`Gmag2`, `BPmag1`/`BPmag2`, `RPmag1`/`RPmag2`: magnitudes
  Gaia G/BP/RP de cada componente (usadas para derivar massa via
  relação massa-luminosidade — ver PROVENANCE.md, catálogo NÃO traz
  massa estelar diretamente).
- `theta`: separação angular do par (deg).
- `sepAU`: separação projetada (AU) — usada por Chae (2023) como
  proxy de separação física.
- `BinType`: classificação MS/WD de cada componente do par (MSMS,
  WDWD, WDMS, MS??, WD??, ????).
- `Sigma18`: métrica auxiliar de qualidade astrométrica ("Sigma 18",
  definição completa não detalhada além do nome no ReadMe — checar o
  paper El-Badry+2021 antes de usar em corte).
- `R`: razão KDE densidade-de-alinhamentos-por-acaso /
  densidade-de-candidatos no espaço de parâmetros 7D — proxy de
  probabilidade de alinhamento casual (quanto menor, mais confiável o
  par). É o `R_chance_align` citado por Chae (2023) e outros para
  cortes de pureza da amostra. Definição verificada por fetch direto do
  texto do paper (ar5iv.labs.arxiv.org/html/2101.05282, Seção 3.2,
  Eq. 8): denotando a densidade KDE-estimada de alinhamentos casuais no
  ponto x⃗ do espaço de parâmetros 7D como N_chance_align(x⃗), e a de
  candidatos binários como N_candidates(x⃗) (soma esperada de
  alinhamento-casual + binária verdadeira), R(x⃗) =
  N_chance_align(x⃗)/N_candidates(x⃗) — aproximadamente a
  probabilidade de que o par seja um alinhamento casual. Os autores
  recomendam `R<0.1` para selecionar binárias de alta confiança (essa
  recomendação NÃO foi aplicada nesta etapa de preparação de dado —
  fica para o pré-registro).
- `RUWE1`/`RUWE2`: qualidade do ajuste astrométrico de cada
  componente (renormalised unit weight error), usado tipicamente para
  cortes de qualidade (ex. RUWE<1.4).

## Tabela completa (217 colunas, ordem exata do arquivo)

| # | Coluna | Bytes | Formato | Unidade | Nome CDS interno | Nulo | Descrição |
|---|---|---|---|---|---|---|---|
| 1 | `SolID1` | 1-19 | I19 | --- | `solution_id1` | não | Solution Identifier |
| 2 | `SolID2` | 21-39 | I19 | --- | `solution_id2` | não | Solution Identifier |
| 3 | `Source1` | 41-59 | I19 | --- | `source_id1` | não | Unique source identifier from Gaia EDR3 (I/350) |
| 4 | `Source2` | 61-79 | I19 | --- | `source_id2` | não | Unique source identifier from Gaia EDR3 (I/350) |
| 5 | `RandomI1` | 81-90 | I10 | --- | `random_index1` | não | Random index used to select subsets |
| 6 | `RandomI2` | 92-101 | I10 | --- | `random_index2` | não | Random index used to select subsets |
| 7 | `refEpoch1` | 103-108 | F6.1 | yr | `ref_epoch1` | não | [2016] Reference epoch |
| 8 | `refEpoch2` | 110-115 | F6.1 | yr | `ref_epoch2` | não | [2016] Reference epoch |
| 9 | `RAdeg` | 117-137 | E21.19 | deg | `ra1` | não | Right ascension (ICRS) at Ep=2016.0 |
| 10 | `RA2deg` | 139-159 | E21.19 | deg | `ra2` | não | Right ascension (ICRS) at Ep=2016.0 |
| 11 | `e_RAdeg` | 161-172 | F12.10 | mas | `ra_error1` | não | Standard error of right ascension |
| 12 | `e_RA2deg` | 174-185 | F12.10 | mas | `ra_error2` | não | Standard error of right ascension |
| 13 | `DEdeg` | 187-208 | E22.19 | deg | `dec1` | não | Declination (ICRS) at Ep=2016.0 |
| 14 | `DE2deg` | 210-231 | E22.19 | deg | `dec2` | não | Declination (ICRS) at Ep=2016.0 |
| 15 | `e_DEdeg` | 233-244 | F12.10 | mas | `dec_error1` | não | Standard error of declination |
| 16 | `e_DE2deg` | 246-257 | F12.10 | mas | `dec_error2` | não | Standard error of declination |
| 17 | `Plx1` | 259-278 | F20.16 | mas | `parallax1` | não | Parallax |
| 18 | `Plx2` | 280-299 | F20.16 | mas | `parallax2` | não | Parallax |
| 19 | `e_Plx1` | 301-312 | F12.10 | mas | `parallax_error1` | não | Standard error of parallax |
| 20 | `e_Plx2` | 314-325 | F12.10 | mas | `parallax_error2` | não | Standard error of parallax |
| 21 | `RPlx1` | 327-339 | F13.7 | --- | `parallax_over_error1` | não | Parallax divided by its standard error |
| 22 | `RPlx2` | 341-353 | F13.7 | --- | `parallax_over_error2` | não | Parallax divided by its standard error |
| 23 | `PM1` | 355-369 | F15.10 | mas/yr | `pm1` | não | Total proper motion |
| 24 | `PM2` | 371-385 | F15.10 | mas/yr | `pm2` | não | Total proper motion |
| 25 | `pmRA1` | 387-408 | E22.19 | mas/yr | `pmra1` | não | Proper motion in right ascension direction |
| 26 | `pmRA2` | 410-431 | E22.19 | mas/yr | `pmra2` | não | Proper motion in right ascension direction |
| 27 | `e_pmRA1` | 433-444 | F12.10 | mas/yr | `pmra_error1` | não | Standard error of proper motion in right ascension direction |
| 28 | `e_pmRA2` | 446-457 | F12.10 | mas/yr | `pmra_error2` | não | Standard error of proper motion in right ascension direction |
| 29 | `pmDE1` | 459-480 | E22.19 | mas/yr | `pmdec1` | não | Proper motion in declination direction |
| 30 | `pmDE2` | 482-503 | E22.19 | mas/yr | `pmdec2` | não | Proper motion in declination direction |
| 31 | `e_pmDE1` | 505-516 | F12.10 | mas/yr | `pmdec_error1` | não | Standard error of proper motion in declination direction |
| 32 | `e_pmDE2` | 518-529 | F12.10 | mas/yr | `pmdec_error2` | não | Standard error of proper motion in declination direction |
| 33 | `RADEcor1` | 531-544 | E14.10 | --- | `ra_dec_corr1` | não | [-1/1] Correlation between right ascension and declination |
| 34 | `RADEcor2` | 546-559 | E14.10 | --- | `ra_dec_corr2` | não | [-1/1] Correlation between right ascension and declination |
| 35 | `RAplxcor1` | 561-574 | E14.10 | --- | `ra_parallax_corr1` | não | [-1/1] Correlation between right ascension and parallax |
| 36 | `RAplxcor2` | 576-589 | E14.10 | --- | `ra_parallax_corr2` | não | [-1/1] Correlation between right ascension and parallax |
| 37 | `RApmRAcor1` | 591-604 | E14.10 | --- | `ra_pmra_corr1` | não | [-1/1] Correlation between right ascension and proper motion in right ascension |
| 38 | `RApmRAcor2` | 606-619 | E14.10 | --- | `ra_pmra_corr2` | não | [-1/1] Correlation between right ascension and proper motion in right ascension |
| 39 | `RApmDEcor1` | 621-634 | E14.10 | --- | `ra_pmdec_corr1` | não | [-1/1] Correlation between right ascension and proper motion in declination |
| 40 | `RApmDEcor2` | 636-649 | E14.10 | --- | `ra_pmdec_corr2` | não | [-1/1] Correlation between right ascension and proper motion in declination |
| 41 | `DEplxcor1` | 651-664 | E14.10 | --- | `dec_parallax_corr1` | não | [-1/1] Correlation between declination and parallax |
| 42 | `DEplxcor2` | 666-679 | E14.10 | --- | `dec_parallax_corr2` | não | [-1/1] Correlation between declination and parallax |
| 43 | `DEpmRAcor1` | 681-694 | E14.10 | --- | `dec_pmra_corr1` | não | [-1/1] Correlation between declination and proper motion in right ascension |
| 44 | `DEpmRAcor2` | 696-709 | E14.10 | --- | `dec_pmra_corr2` | não | [-1/1] Correlation between declination and proper motion in right ascension |
| 45 | `DEpmDEcor1` | 711-724 | E14.10 | --- | `dec_pmdec_corr1` | não | [-1/1] Correlation between declination and proper motion in declination |
| 46 | `DEpmDEcor2` | 726-739 | E14.10 | --- | `dec_pmdec_corr2` | não | [-1/1] Correlation between declination and proper motion in declination |
| 47 | `plxpmRAcor1` | 741-754 | E14.10 | --- | `parallax_pmra_corr1` | não | [-1/1] Correlation between parallax and proper motion in right ascension |
| 48 | `plxpmRAcor2` | 756-769 | E14.10 | --- | `parallax_pmra_corr2` | não | [-1/1] Correlation between parallax and proper motion in right ascension |
| 49 | `plxpmDEcor1` | 771-784 | E14.10 | --- | `parallax_pmdec_corr1` | não | [-1/1] Correlation between parallax and proper motion in declination |
| 50 | `plxpmDEcor2` | 786-799 | E14.10 | --- | `parallax_pmdec_corr2` | não | [-1/1] Correlation between parallax and proper motion in declination |
| 51 | `pmRApmDEcor1` | 801-814 | E14.10 | --- | `pmra_pmdec_corr1` | não | [-1/1] Correlation between proper motion in right ascension and proper motion in declination |
| 52 | `pmRApmDEcor2` | 816-829 | E14.10 | --- | `pmra_pmdec_corr2` | não | [-1/1] Correlation between proper motion in right ascension and proper motion in declination |
| 53 | `NAL1` | 831-834 | I4 | --- | `astrometric_n_obs_al1` | não | [63/1498] Total number of observations AL |
| 54 | `NAL2` | 836-839 | I4 | --- | `astrometric_n_obs_al2` | não | [67/1445] Total number of observations AL |
| 55 | `NAC1` | 841-844 | I4 | --- | `astrometric_n_obs_ac1` | não | [0/1479] Total number of observations AC |
| 56 | `NAC2` | 846-849 | I4 | --- | `astrometric_n_obs_ac2` | não | [0/1268] Total number of observations AC |
| 57 | `NgAL1` | 851-854 | I4 | --- | `astrometric_n_good_obs_al1` | não | [55/1498] Number of good observations AL |
| 58 | `NgAL2` | 856-859 | I4 | --- | `astrometric_n_good_obs_al2` | não | [60/1439] Number of good observations AL |
| 59 | `NbAL1` | 861-863 | I3 | --- | `astrometric_n_bad_obs_al1` | não | [0/224] Number of bad observations AL |
| 60 | `NbAL2` | 865-867 | I3 | --- | `astrometric_n_bad_obs_al2` | não | [0/210] Number of bad observations AL |
| 61 | `gofAL1` | 869-882 | E14.10 | --- | `astrometric_gof_al1` | não | Goodness of fit statistic of model wrt along-scan observations |
| 62 | `gofAL2` | 884-897 | E14.10 | --- | `astrometric_gof_al2` | não | Goodness of fit statistic of model wrt along-scan observations |
| 63 | `chi2AL1` | 899-912 | F14.6 | --- | `astrometric_chi2_al1` | não | AL chi-square value |
| 64 | `chi2AL2` | 914-927 | F14.6 | --- | `astrometric_chi2_al2` | não | AL chi-square value |
| 65 | `epsi1` | 929-940 | E12.10 | mas | `astrometric_excess_noise1` | não | Excess noise of the source |
| 66 | `epsi2` | 942-953 | E12.10 | mas | `astrometric_excess_noise2` | não | Excess noise of the source |
| 67 | `sepsi1` | 955-967 | E13.10 | --- | `astrometric_excess_noise_sig1` | não | Significance of excess noise |
| 68 | `sepsi2` | 969-981 | E13.10 | --- | `astrometric_excess_noise_sig2` | não | Significance of excess noise |
| 69 | `Solved1` | 983-984 | I2 | --- | `astrometric_params_solved1` | não | Which parameters have been solved for? |
| 70 | `Solved2` | 986-987 | I2 | --- | `astrometric_params_solved2` | não | Which parameters have been solved for? |
| 71 | `APF1` | 989-993 | A5 | --- | `astrometric_primary_flag1` | não | Primary or secondary |
| 72 | `APF2` | 995-999 | A5 | --- | `astrometric_primary_flag2` | não | Primary or secondary |
| 73 | `nueff1` | 1001-1009 | E9.7 | um-1 | `nu_eff_used_in_astrometry1` | sim — sentinela `1e+20` | ?=1e+20 Effective wavenumber of the source used in the astrometric solution |
| 74 | `nueff2` | 1011-1019 | E9.7 | um-1 | `nu_eff_used_in_astrometry2` | sim — sentinela `1e+20` | ?=1e+20 Effective wavenumber of the source used in the astrometric solution |
| 75 | `pscol1` | 1021-1032 | E12.9 | um-1 | `pseudocolour1` | sim — sentinela `1e+20` | ?=1e+20 Astrometrically estimated pseudocolour of the source |
| 76 | `pscol2` | 1034-1046 | E13.10 | um-1 | `pseudocolour2` | sim — sentinela `1e+20` | ?=1e+20 Astrometrically estimated pseudocolour of the source |
| 77 | `e_pscol1` | 1048-1059 | E12.10 | um-1 | `pseudocolour_error1` | sim — sentinela `1e+20` | ?=1e+20 Standard error of the pseudocolour of the source |
| 78 | `e_pscol2` | 1061-1072 | E12.10 | um-1 | `pseudocolour_error2` | sim — sentinela `1e+20` | ?=1e+20 Standard error of the pseudocolour of the source |
| 79 | `RApscolCorr1` | 1074-1087 | E14.10 | --- | `ra_pseudocolour_corr1` | sim — sentinela `1e+20` | ?=1e+20 Correlation between right ascension and pseudocolour |
| 80 | `RApscolCorr2` | 1089-1102 | E14.10 | --- | `ra_pseudocolour_corr2` | sim — sentinela `1e+20` | ?=1e+20 Correlation between right ascension and pseudocolour |
| 81 | `DEpscolCorr1` | 1104-1117 | E14.10 | --- | `dec_pseudocolour_corr1` | sim — sentinela `1e+20` | ?=1e+20 Correlation between declination and pseudocolour |
| 82 | `DEpscolCorr2` | 1119-1132 | E14.10 | --- | `dec_pseudocolour_corr2` | sim — sentinela `1e+20` | ?=1e+20 Correlation between declination and pseudocolour |
| 83 | `PlxpscolCorr1` | 1134-1147 | E14.10 | --- | `parallax_pseudocolour_corr1` | sim — sentinela `1e+20` | ?=1e+20 Correlation between parallax and pseudocolour |
| 84 | `PlxpscolCorr2` | 1149-1162 | E14.10 | --- | `parallax_pseudocolour_corr2` | sim — sentinela `1e+20` | ?=1e+20 Correlation between parallax and pseudocolour |
| 85 | `pmRApscolCorr1` | 1164-1177 | E14.10 | --- | `pmra_pseudocolour_corr1` | sim — sentinela `1e+20` | ?=1e+20 Correlation between proper motion in right ascension and pseudocolour |
| 86 | `pmRApscolCorr2` | 1179-1192 | E14.10 | --- | `pmra_pseudocolour_corr2` | sim — sentinela `1e+20` | ?=1e+20 Correlation between proper motion in right ascension and pseudocolour |
| 87 | `pmDEpscolCorr1` | 1194-1207 | E14.10 | --- | `pmdec_pseudocolour_corr1` | sim — sentinela `1e+20` | ?=1e+20 Correlation between proper motion in declination and pseudocolour |
| 88 | `pmDEpscolCorr2` | 1209-1222 | E14.10 | --- | `pmdec_pseudocolour_corr2` | sim — sentinela `1e+20` | ?=1e+20 Correlation between proper motion in declination and pseudocolour |
| 89 | `MatchObsA1` | 1224-1226 | I3 | --- | `astrometric_matched_transits1` | não | [9/172] Matched FOV transits used in the AGIS solution |
| 90 | `MatchObsA2` | 1228-1230 | I3 | --- | `astrometric_matched_transits2` | não | [9/165] Matched FOV transits used in the AGIS solution |
| 91 | `Nper1` | 1232-1233 | I2 | --- | `visibility_periods_used1` | não | [9/33] Number of visibility periods used in Astrometric solution |
| 92 | `Nper2` | 1235-1236 | I2 | --- | `visibility_periods_used2` | não | [9/33] Number of visibility periods used in Astrometric solution |
| 93 | `amax1` | 1238-1249 | F12.10 | mas | `astrometric_sigma5d_max1` | não | The longest semi-major axis of the 5-d error ellipsoid |
| 94 | `amax2` | 1251-1262 | F12.10 | mas | `astrometric_sigma5d_max2` | não | The longest semi-major axis of the 5-d error ellipsoid |
| 95 | `MatchObs1` | 1264-1266 | I3 | --- | `matched_transits1` | não | [10/313] The number of transits matched to this source |
| 96 | `MatchObs2` | 1268-1270 | I3 | --- | `matched_transits2` | não | [9/269] The number of transits matched to this source |
| 97 | `NewMatchObs1` | 1272-1274 | I3 | --- | `new_matched_transits1` | não | [1/313] The number of transits newly incorporated into an existing source in the current cycle |
| 98 | `NewMatchObs2` | 1276-1278 | I3 | --- | `new_matched_transits2` | não | [0/260] The number of transits newly incorporated into an existing source in the current cycle |
| 99 | `MatchObsrm1` | 1280-1281 | I2 | --- | `matched_transits_removed1` | não | [0/72] The number of transits removed from an existing source in the current cycle |
| 100 | `MatchObsrm2` | 1283-1285 | I3 | --- | `matched_transits_removed2` | não | [0/117] The number of transits removed from an existing source in the current cycle |
| 101 | `IPDgofha1` | 1287-1299 | E13.10 | --- | `ipd_gof_harmonic_amplitude1` | não | Amplitude of the IPD GoF versus position angle of scan |
| 102 | `IPDgofha2` | 1301-1313 | E13.10 | --- | `ipd_gof_harmonic_amplitude2` | não | Amplitude of the IPD GoF versus position angle of scan |
| 103 | `IPDgofhp1` | 1315-1327 | E13.10 | deg | `ipd_gof_harmonic_phase1` | não | Phase of the IPD GoF versus position angle of scan |
| 104 | `IPDgofhp2` | 1329-1340 | E12.10 | deg | `ipd_gof_harmonic_phase2` | não | Phase of the IPD GoF versus position angle of scan |
| 105 | `IPDfmp1` | 1342-1344 | I3 | --- | `ipd_frac_multi_peak1` | não | Percent of successful-IPD windows with more than one peak |
| 106 | `IPDfmp2` | 1346-1348 | I3 | --- | `ipd_frac_multi_peak2` | não | Percent of successful-IPD windows with more than one peak |
| 107 | `IPDfow1` | 1350-1352 | I3 | --- | `ipd_frac_odd_win1` | não | Percent of transits with truncated windows or multiple gate |
| 108 | `IPDfow2` | 1354-1356 | I3 | --- | `ipd_frac_odd_win2` | não | Percent of transits with truncated windows or multiple gate |
| 109 | `RUWE1` | 1358-1368 | F11.8 | --- | `ruwe1` | não | Renormalised unit weight error |
| 110 | `RUWE2` | 1370-1380 | F11.8 | --- | `ruwe2` | não | Renormalised unit weight error |
| 111 | `SDSk11` | 1382-1394 | E13.10 | --- | `scascan_direction_strength_k11` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 112 | `SDSk12` | 1396-1407 | E12.10 | --- | `scascan_direction_strength_k12` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 113 | `SDSk21` | 1409-1420 | E12.10 | --- | `scascan_direction_strength_k21` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 114 | `SDSk22` | 1422-1433 | E12.10 | --- | `scascan_direction_strength_k22` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 115 | `SDSk31` | 1435-1447 | E13.10 | --- | `scascan_direction_strength_k31` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 116 | `SDSk32` | 1449-1461 | E13.10 | --- | `scascan_direction_strength_k32` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 117 | `SDSk41` | 1463-1474 | E12.10 | --- | `scascan_direction_strength_k41` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 118 | `SDSk42` | 1476-1487 | E12.10 | --- | `scascan_direction_strength_k42` | sim — sentinela `1e+20` | ?=1e+20 Degree of concentration of n directions across the source |
| 119 | `SDMk11` | 1489-1501 | E13.10 | deg | `scan_direction_mean_k11` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 120 | `SDMk12` | 1503-1515 | E13.10 | deg | `scan_direction_mean_k12` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 121 | `SDMk21` | 1517-1529 | E13.10 | deg | `scan_direction_mean_k21` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 122 | `SDMk22` | 1531-1543 | E13.10 | deg | `scan_direction_mean_k22` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 123 | `SDMk31` | 1545-1557 | E13.10 | deg | `scan_direction_mean_k31` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 124 | `SDMk32` | 1559-1572 | E14.10 | deg | `scan_direction_mean_k32` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 125 | `SDMk41` | 1574-1586 | E13.10 | deg | `scan_direction_mean_k41` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 126 | `SDMk42` | 1588-1600 | E13.10 | deg | `scan_direction_mean_k42` | sim — sentinela `1e+20` | ?=1e+20 Mean position angle of scan directions across the source |
| 127 | `Dup1` | 1602-1606 | A5 | --- | `duplicated_source1` | não | Source with multiple source identifiers |
| 128 | `Dup2` | 1608-1612 | A5 | --- | `duplicated_source2` | não | Source with multiple source identifiers |
| 129 | `o_Gmag1` | 1614-1617 | I4 | --- | `phot_g_n_obs1` | não | [0/2349] Number of observations contributing to G photometry |
| 130 | `o_Gmag2` | 1619-1622 | I4 | --- | `phot_g_n_obs2` | não | [0/2289] Number of observations contributing to G photometry |
| 131 | `FG1` | 1624-1643 | E20.17 | e-/s | `phot_g_mean_flux1` | não | G-band mean flux |
| 132 | `FG2` | 1645-1664 | E20.17 | e-/s | `phot_g_mean_flux2` | não | G-band mean flux |
| 133 | `e_FG1` | 1666-1676 | E11.8 | e-/s | `phot_g_mean_flux_error1` | não | Error on G-band mean flux |
| 134 | `e_FG2` | 1678-1692 | F15.8 | e-/s | `phot_g_mean_flux_error2` | não | Error on G-band mean flux |
| 135 | `RFG1` | 1694-1706 | F13.7 | --- | `phot_g_mean_flux_over_error1` | não | G-band mean flux divided by its error |
| 136 | `RFG2` | 1708-1719 | F12.6 | --- | `phot_g_mean_flux_over_error2` | não | G-band mean flux divided by its error |
| 137 | `Gmag1` | 1721-1730 | F10.7 | mag | `phot_g_mean_mag1` | não | G-band mean magnitude |
| 138 | `Gmag2` | 1732-1741 | F10.7 | mag | `phot_g_mean_mag2` | não | G-band mean magnitude |
| 139 | `o_BPmag1` | 1743-1745 | I3 | --- | `phot_bp_n_obs1` | não | [0/261] Number of observations contributing to BP photometry |
| 140 | `o_BPmag2` | 1747-1749 | I3 | --- | `phot_bp_n_obs2` | não | [0/251] Number of observations contributing to BP photometry |
| 141 | `FBP1` | 1751-1770 | E20.17 | e-/s | `phot_bp_mean_flux1` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean flux |
| 142 | `FBP2` | 1772-1791 | E20.17 | e-/s | `phot_bp_mean_flux2` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean flux |
| 143 | `e_FBP1` | 1793-1804 | E12.10 | e-/s | `phot_bp_mean_flux_error1` | sim — sentinela `1e+20` | ?=1e+20 Error on the integrated BP mean flux |
| 144 | `e_FBP2` | 1806-1817 | E12.10 | e-/s | `phot_bp_mean_flux_error2` | sim — sentinela `1e+20` | ?=1e+20 Error on the integrated BP mean flux |
| 145 | `RFBP1` | 1819-1828 | E10.8 | --- | `phot_bp_mean_flux_over_error1` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean flux divided by its error |
| 146 | `RFBP2` | 1830-1840 | E11.8 | --- | `phot_bp_mean_flux_over_error2` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean flux divided by its error |
| 147 | `BPmag1` | 1842-1851 | E10.7 | mag | `phot_bp_mean_mag1` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean magnitude |
| 148 | `BPmag2` | 1853-1862 | E10.7 | mag | `phot_bp_mean_mag2` | sim — sentinela `1e+20` | ?=1e+20 Integrated BP mean magnitude |
| 149 | `o_RPmag1` | 1864-1866 | I3 | --- | `phot_rp_n_obs1` | não | [0/260] Number of observations contributing to RP photometry |
| 150 | `o_RPmag2` | 1868-1870 | I3 | --- | `phot_rp_n_obs2` | não | [0/254] Number of observations contributing to RP photometry |
| 151 | `FRP1` | 1872-1891 | E20.17 | e-/s | `phot_rp_mean_flux1` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean flux |
| 152 | `FRP2` | 1893-1912 | E20.17 | e-/s | `phot_rp_mean_flux2` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean flux |
| 153 | `e_FRP1` | 1914-1924 | E11.9 | e-/s | `phot_rp_mean_flux_error1` | sim — sentinela `1e+20` | ?=1e+20 Error on the integrated RP mean flux |
| 154 | `e_FRP2` | 1926-1937 | E12.10 | e-/s | `phot_rp_mean_flux_error2` | sim — sentinela `1e+20` | ?=1e+20 Error on the integrated RP mean flux |
| 155 | `RFRP1` | 1939-1948 | E10.8 | --- | `phot_rp_mean_flux_over_error1` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean flux divided by its error |
| 156 | `RFRP2` | 1950-1959 | E10.8 | --- | `phot_rp_mean_flux_over_error2` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean flux divided by its error |
| 157 | `RPmag1` | 1961-1970 | E10.7 | mag | `phot_rp_mean_mag1` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean magnitude |
| 158 | `RPmag2` | 1972-1981 | E10.7 | mag | `phot_rp_mean_mag2` | sim — sentinela `1e+20` | ?=1e+20 Integrated RP mean magnitude |
| 159 | `NBPcont1` | 1983-1987 | I5 | --- | `phot_bp_n_contaminated_transits1` | não | [0/16959] Number of BP contaminated transits |
| 160 | `NBPcont2` | 1989-1993 | I5 | --- | `phot_bp_n_contaminated_transits2` | não | [0/16959] Number of BP contaminated transits |
| 161 | `NBPblend1` | 1995-1999 | I5 | --- | `phot_bp_n_blended_transits1` | não | [0/16959] Number of BP blended transits |
| 162 | `NBPblend2` | 2001-2005 | I5 | --- | `phot_bp_n_blended_transits2` | não | [0/16959] Number of BP blended transits |
| 163 | `NRPcont1` | 2007-2011 | I5 | --- | `phot_rp_n_contaminated_transits1` | não | [0/16959] Number of RP contaminated transits |
| 164 | `NRPcont2` | 2013-2017 | I5 | --- | `phot_rp_n_contaminated_transits2` | não | [0/16959] Number of RP contaminated transits |
| 165 | `NRPblend1` | 2019-2023 | I5 | --- | `phot_rp_n_blended_transits1` | não | [0/16959] Number of RP blended transits |
| 166 | `NRPblend2` | 2025-2029 | I5 | --- | `phot_rp_n_blended_transits2` | não | [0/16959] Number of RP blended transits |
| 167 | `Mode1` | 2031-2031 | I1 | --- | `phot_proc_mode1` | não | [0/2] Photometry processing mode |
| 168 | `Mode2` | 2033-2033 | I1 | --- | `phot_proc_mode2` | não | [0/2] Photometry processing mode |
| 169 | `E(BP/RP)1` | 2035-2044 | E10.8 | --- | `phot_bp_rp_excess_factor1` | sim — sentinela `1e+20` | ?=1e+20 Excess factor |
| 170 | `E(BP/RP)2` | 2046-2055 | E10.8 | --- | `phot_bp_rp_excess_factor2` | sim — sentinela `1e+20` | ?=1e+20 Excess factor |
| 171 | `BP-RP1` | 2057-2069 | E13.10 | mag | `bp_rp1` | sim — sentinela `1e+20` | ?=1e+20 BP-RP colour |
| 172 | `BP-RP2` | 2071-2083 | E13.10 | mag | `bp_rp2` | sim — sentinela `1e+20` | ?=1e+20 BP-RP colour |
| 173 | `BP-G1` | 2085-2097 | E13.10 | mag | `bp_g1` | sim — sentinela `1e+20` | ?=1e+20 BP-G colour |
| 174 | `BP-G2` | 2099-2112 | E14.10 | mag | `bp_g2` | sim — sentinela `1e+20` | ?=1e+20 BP-G colour |
| 175 | `G-RP1` | 2114-2126 | E13.10 | mag | `rp1` | sim — sentinela `1e+20` | ?=1e+20 G-RP colour |
| 176 | `G-RP2` | 2128-2140 | E13.10 | mag | `rp2` | sim — sentinela `1e+20` | ?=1e+20 G-RP colour |
| 177 | `dr2RV1` | 2142-2154 | E13.10 | km/s | `dr2_radial_velocity1` | sim — sentinela `1e+20` | ?=1e+20 Radial velocity from Gaia DR2 |
| 178 | `dr2RV2` | 2156-2168 | E13.10 | km/s | `dr2_radial_velocity2` | sim — sentinela `1e+20` | ?=1e+20 Radial velocity from Gaia DR2 |
| 179 | `e_dr2RV1` | 2170-2180 | E11.9 | km/s | `dr2_radial_velocity_error1` | sim — sentinela `1e+20` | ?=1e+20 Radial velocity error from Gaia DR2 |
| 180 | `e_dr2RV2` | 2182-2192 | E11.9 | km/s | `dr2_radial_velocity_error2` | sim — sentinela `1e+20` | ?=1e+20 Radial velocity error from Gaia DR2 |
| 181 | `o_dr2RV1` | 2194-2196 | I3 | --- | `dr2_rv_nb_transits1` | não | [0/196] Number of transits used to compute radial velocity in Gaia DR2 |
| 182 | `o_dr2RV2` | 2198-2200 | I3 | --- | `dr2_rv_nb_transits2` | não | [0/147] Number of transits used to compute radial velocity in Gaia DR2 |
| 183 | `dr2RVtempTeff1` | 2202-2207 | E6.2 | K | `dr2_rv_template_teff1` | sim — sentinela `1e+20` | ?=1e+20 Teff of the template used to compute radial velocity in Gaia DR2 |
| 184 | `dr2RVtempTeff2` | 2209-2214 | E6.2 | K | `dr2_rv_template_teff2` | sim — sentinela `1e+20` | ?=1e+20 Teff of the template used to compute radial velocity in Gaia DR2 |
| 185 | `dr2RVtemplogg1` | 2216-2221 | E6.2 | [cm/s2] | `dr2_rv_template_logg1` | sim — sentinela `1e+20` | ?=1e+20 Logg of the template used to compute radial velocity in Gaia DR2 |
| 186 | `dr2RVtemplogg2` | 2223-2228 | E6.2 | [cm/s2] | `dr2_rv_template_logg2` | sim — sentinela `1e+20` | ?=1e+20 Logg of the template used to compute radial velocity in Gaia DR2 |
| 187 | `dr2RVtemp[Fe/H]1` | 2230-2235 | E6.2 | --- | `dr2_rv_template_fe_h1` | sim — sentinela `1e+20` | ?=1e+20 Template's [Fe/H] used to compute radial velocity in Gaia DR2 |
| 188 | `dr2RVtemp[Fe/H]2` | 2237-2242 | E6.2 | --- | `dr2_rv_template_fe_h2` | sim — sentinela `1e+20` | ?=1e+20 Template's [Fe/H] used to compute radial velocity in Gaia DR2 |
| 189 | `GLON1` | 2244-2264 | E21.19 | deg | `l1` | não | Galactic longitude |
| 190 | `GLON2` | 2266-2286 | E21.19 | deg | `l2` | não | Galactic longitude |
| 191 | `GLAT1` | 2288-2309 | E22.19 | deg | `b1` | não | Galactic latitude |
| 192 | `GLAT2` | 2311-2332 | E22.19 | deg | `b2` | não | Galactic latitude |
| 193 | `ELON1` | 2334-2354 | E21.19 | deg | `ecl_lon1` | não | Ecliptic longitude |
| 194 | `ELON2` | 2356-2376 | E21.19 | deg | `ecl_lon2` | não | Ecliptic longitude |
| 195 | `ELAT1` | 2378-2399 | E22.19 | deg | `ecl_lat1` | não | Ecliptic latitude |
| 196 | `ELAT2` | 2401-2422 | E22.19 | deg | `ecl_lat2` | não | Ecliptic latitude |
| 197 | `theta` | 2424-2444 | E21.19 | deg | `pairdistance` | não | Angular separation |
| 198 | `sepAU` | 2446-2467 | F22.15 | AU | `sep_AU` | não | Projected separation |
| 199 | `BinType` | 2469-2472 | A4 | --- | `binary_type` | não | Binary type |
| 200 | `Sigma18` | 2474-2492 | F19.14 | --- | `Sigma18` | não | Sigma 18 |
| 201 | `R` | 2494-2516 | E23.19 | --- | `R_chance_align` | não | R chance align |
| 202 | `dr2Source1` | 2518-2536 | I19 | --- | `dr2_source_id1` | não | Source identifier from Gaia DR2 (I/345) |
| 203 | `dr2Source2` | 2538-2556 | I19 | --- | `dr2_source_id2` | não | Source identifier from Gaia DR2 (I/345) |
| 204 | `dr2plx1` | 2558-2579 | E22.19 | mas | `dr2_parallax1` | sim — campo vazio | ? Parallax from Gaia DR2 |
| 205 | `dr2plx2` | 2581-2602 | E22.19 | mas | `dr2_parallax2` | sim — campo vazio | ? Parallax from Gaia DR2 |
| 206 | `e_dr2plx1` | 2604-2623 | F20.18 | mas | `dr2_parallax_error1` | sim — campo vazio | ? dr2plx1 uncertainty |
| 207 | `e_dr2plx2` | 2625-2644 | F20.18 | mas | `dr2_parallax_error2` | sim — campo vazio | ? dr2plx2 uncertainty |
| 208 | `dr2pmRA1` | 2646-2667 | E22.19 | mas/yr | `dr2_pmra1` | sim — campo vazio | ? Proper motion in right ascension from Gaia DR2 |
| 209 | `dr2pmRA2` | 2669-2690 | E22.19 | mas/yr | `dr2_pmra2` | sim — campo vazio | ? Proper motion in right ascension from Gaia DR2 |
| 210 | `dr2pmDE1` | 2692-2713 | E22.19 | mas/yr | `dr2_pmdec1` | sim — campo vazio | ? Proper motion in declination from Gaia DR2 |
| 211 | `dr2pmDE2` | 2715-2736 | E22.19 | mas/yr | `dr2_pmdec2` | sim — campo vazio | ? Proper motion in declination from Gaia DR2 |
| 212 | `e_dr2pmRA1` | 2738-2757 | F20.18 | mas/yr | `dr2_pmra_error1` | sim — campo vazio | ? dr2pmRA1 uncertainty |
| 213 | `e_dr2pmRA2` | 2759-2778 | F20.18 | mas/yr | `dr2_pmra_error2` | sim — campo vazio | ? dr2pmRA2 uncertainty |
| 214 | `e_dr2pmDE1` | 2780-2799 | F20.18 | mas/yr | `dr2_pmdec_error1` | sim — campo vazio | ? dr2pmDE1 uncertainty |
| 215 | `e_dr2pmDE2` | 2801-2820 | F20.18 | mas/yr | `dr2_pmdec_error2` | sim — campo vazio | ? dr2pmDE2 uncertainty |
| 216 | `dr2RUWE1` | 2822-2832 | F11.8 | --- | `dr2_ruwe1` | não | Renormalised unit weight error from Gaia DR2 |
| 217 | `dr2RUWE2` | 2834-2844 | F11.8 | --- | `dr2_ruwe2` | não | Renormalised unit weight error from Gaia DR2 |
