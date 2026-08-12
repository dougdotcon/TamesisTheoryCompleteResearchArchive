# Proveniência dos dados — DISC-COSMOLOGY-MOND-SPARC-001

## Fonte 1: Catálogo principal SPARC

- **Arquivo:** `SPARC_Lelli2016c.mrt`
- **URL exata (verificada por fetch direto em 2026-08-12):**
  `https://astroweb.case.edu/SPARC/SPARC_Lelli2016c.mrt`
- **Publicação de origem:** Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016).
  "SPARC. I. Mass Models for 175 Disk Galaxies with Spitzer Photometry and
  Accurate Rotation Curves." *The Astronomical Journal*, 152(6), 157.
  DOI: 10.3847/0004-6256/152/6/157.
- **Data de acesso:** 2026-08-12
- **sha256:** `5aa0501f6b0d881fa579030e315e7b5b6ef561a5bd3a07472f9929c7e5728243`
- **Tamanho:** 28259 bytes
- **Registros:** 175 galáxias (header de 98 linhas de documentação byte-a-byte
  seguido de 175 linhas de dados, campos separados por espaço:
  `Galaxy T D e_D f_D Inc e_Inc L[3.6] e_L[3.6] Reff SBeff Rdisk SBdisk MHI RHI Vflat e_Vflat Q Ref`).
  Verificado por parsing direto (`data_lines = 175`, confere com o título do
  paper "175 Disk Galaxies").

## Fonte 2: Curvas de rotação individuais

- **Arquivo original:** `Rotmod_LTG.zip` (extraído para `Rotmod_LTG/`)
- **URL exata (verificada por fetch direto em 2026-08-12):**
  `https://astroweb.case.edu/SPARC/Rotmod_LTG.zip`
- **Data de acesso:** 2026-08-12
- **sha256 do zip original:** `0a80cc90714828cc28b7dd57923576714d209f2490328c087c4a4ad607faf588`
- **Conteúdo extraído:** 175 arquivos `<Galaxy>_rotmod.dat`, um por galáxia do
  catálogo principal (contagem de arquivos == contagem de linhas de dados do
  `.mrt`, verificado).
- **Formato de cada arquivo** (verificado por inspeção direta, ex.
  `NGC3726_rotmod.dat`): comentário com a distância adotada, depois colunas
  `Rad[kpc] Vobs[km/s] errV[km/s] Vgas[km/s] Vdisk[km/s] Vbul[km/s] SBdisk[L/pc²] SBbul[L/pc²]`.
- **Tamanho total:** 716K (175 arquivos).

## Diferença em relação à fonte legada

O script legado (`01_TAMESIS_CORE/.../efe/simulations/sparc_real_download.py`)
apontava para `http://astroweb.cwru.edu/SPARC/...` — domínio incorreto (SPARC
migrou de `astroweb.cwru.edu` para `astroweb.case.edu`; a versão antiga do
Case Western Reserve não resolve mais como esperado pelo script, ver
`AUDIT_LEGACY_MOND_EFE_SPARC.md`). Os dados desta pasta foram baixados
diretamente da URL correta, com HTTPS e verificação TLS padrão (nenhum
`ssl.CERT_NONE`), e nenhum dado embutido/fallback foi usado em nenhum momento.

## Classificação de ambiente usada nesta trilha

Ao contrário do script legado (que usava uma lista externa, não verificável a
partir do próprio catálogo, de "membros do aglomerado de Virgem"), esta
trilha usa **exclusivamente** um campo já presente no catálogo oficial SPARC:
a coluna `f_D` ("Distance Method", nota 2 do cabeçalho do `.mrt`), cujo valor
`4` é documentado no próprio arquivo como `"4 = Ursa Major Cluster of Galaxies"`.
Isso permite classificar ambiente (aglomerado vs. campo) sem depender de
nenhuma fonte externa de membership não verificada nesta sessão — ver
`PREREGISTRATION.md` para a contagem exata e a justificativa desta escolha,
incluindo por que a amostra real do SPARC não permite reproduzir o desenho
original "Virgem vs. campo" do script legado.
