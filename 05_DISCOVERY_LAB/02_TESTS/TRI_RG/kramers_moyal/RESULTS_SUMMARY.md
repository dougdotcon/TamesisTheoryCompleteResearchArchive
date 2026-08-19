# Resultado do fechamento dos gaps — `kramers-moyal` (Reconstrução de Fokker-Planck via Coeficientes de Kramers-Moyal)

**Status: FECHADO — nenhuma das 4 combinações domínio/variante produz
um veredito `PKS` significativo com estrutura completa; 2 combinações
(`vfdb`, ambas as variantes) nem chegam a estabelecer `tau_ME`
(propriedade de Markov não estabelecida); as outras 2 (`eurchf`, ambas
as variantes) estabelecem `tau_ME` mas `PKS` fica estruturalmente
INDEFINIDO no POST, não apenas não-significativo.** `beta_D2`/`kappa`
reportados só como diagnóstico (per o adendo de `METHODOLOGY_NOTE.md`,
commit `9d35eeb`), nunca parte de nenhum veredito.

## Validação — recapitulação

Ver `VALIDATION_NOTE.md` para o relato completo. Resumo: `PKS` (canal
único de decisão) tem poder IAAFT real e limpo confirmado em controle
sintético dedicado (`p=0,005` positivo, `p=0,23` negativo, `≈-2,04σ`).
Dois problemas reais de implementação no bootstrap do teste CK foram
encontrados e corrigidos ANTES de qualquer dado real (ver
`km_common.py::ck_test_at_lag` docstring).

## Domínio 1 — PhysioNet `vfdb`, registro 418 (arritmia ventricular maligna)

| Variante | Status | `tau_ME` |
|---|---|---|
| Primária | `markov_property_not_established` | não estabelecido |
| Robustez | `markov_property_not_established` | não estabelecido |

**Achado honesto:** o teste de Chapman-Kolmogorov REJEITA fortemente a
propriedade de Markov em amplitude bruta de ECG em praticamente todos os
lags curtos da grade (`chi2` observado ~5.000-800 contra nula bootstrap
~40-100, `p_ck_test=0,0`), em AMBAS as variantes. Uma única
não-rejeição isolada aparece em lag longo (`lag=130` amostras, `p=0,075`
primária; `p=0,56` robustez), mas os 2 pontos seguintes da grade ficam
`insufficient_samples` (poço de blocos não-sobrepostos esgotado) —
**não há como confirmar a robustez de 3 pontos consecutivos exigida
pela regra de `tau_ME`, então o domínio/segmento é REJEITADO por
propriedade de Markov não estabelecida**, exatamente como
`METHODOLOGY_NOTE.md` Gap (a) instrui para esse caso ("declarado
honestamente antes de qualquer cálculo, não forçado"). Fisiologicamente
plausível: um sinal quase-periódico como o ECG não é Markoviano em
amplitude bruta sem informação de fase do ciclo cardíaco — resultado
teoricamente esperado, não um bug de pipeline (confirmado pelo
diagnóstico de correção de código em `VALIDATION_NOTE.md`, que valida o
teste CK contra processos sintéticos conhecidos).

**`PKS`/`beta_D2`/`kappa`: não computados** (o pipeline retorna cedo
quando `tau_ME` não é estabelecido, per desenho já documentado em
`km_common.py`).

## Domínio 2 — EUR/CHF tick-a-tick, choque de despeg do SNB (15/01/2015)

| Variante | Status | `tau_ME` | `PKS` PRE/POST/Δ/`p` |
|---|---|---|---|
| Primária | `ok` | 5 amostras (1,51s) | 6,157 / **indefinido** / — / — |
| Robustez | `ok` | 2 amostras (0,604s) | 0,641 / **indefinido** / — / — |

**`tau_ME` estabelecido em ambas as variantes** (grade CK confirma
não-rejeição em 3+ pontos consecutivos a partir do lag encontrado —
diferente de `vfdb`, o preço médio de câmbio se comporta como Markoviano
no PRE em lags curtos).

**Achado estrutural honesto — `PKS` INDEFINIDO no POST, não apenas
não-significativo:** o choque do SNB é um dos movimentos cambiais mais
violentos já documentados (~15% num único dia, de um regime de câmbio
fixo — confirmado empiricamente nesta sessão: preço 5min antes do
anúncio = 1,200975, 5min depois = 1,020855). Os 10 bins de quantil,
fixados UMA VEZ a partir do PRE (regra travada, Gap (a) — PRE é o
período pré-choque, faixa de preço extremamente estreita ~1,2009-1,2010),
reaplicados sem recálculo ao POST (que inclui o colapso a ~1,02): **≈50%
de TODO o POST primário cai no bin 0 sozinho** (37.239 de 74.497 ticks),
os 9 bins restantes ficam com 0-2 amostras cada — muito abaixo de
`MIN_SAMPLES_PER_BIN=30`. `reconstruct_stationary_density` retorna
`insufficient_defined_bins` (`n_defined=1<3`) → `PKS_post=None`. Mesmo
padrão, exatamente proporcional, na variante de robustez. **Isso não é
um p-valor não-significativo — é um resultado estruturalmente
indefinido**, consequência honesta e esperada de aplicar a regra já
travada ("bins do PRE, reaplicados sem recálculo") a um domínio com uma
ruptura de regime desse porte. Detalhes completos, incluindo a
verificação de quebra de preço e a distribuição de amostras por bin,
em `data/PROVENANCE_EURCHF.md`.

**`beta_D2`/`kappa` (diagnóstico, nunca em nenhum veredito):**
`beta_D2_pre` = `2,76e-07` (primária) / `-4,69e-07` (robustez);
`kappa_pre` = `0,379` (primária) / `0,211` (robustez). Também
indefinidos no POST pelo mesmo motivo estrutural.

## Sobre a checagem adversarial

Nenhuma das 4 combinações produziu um `PKS` computável E significativo
(2 nem chegam a `tau_ME`, as outras 2 têm `PKS` estruturalmente
indefinido no POST) — não há achado positivo a explicar via reexecução
adversarial completa ou descoberta de nulos.

## Veredito honesto

`kramers-moyal`, como formulado e testado aqui (pipeline `tau_ME` via
teste de Markov-Einstein/Chapman-Kolmogorov + `PKS` como único canal de
decisão, sem reformulação por domínio, aplicado aos 2 domínios reais
declarados em `METHODOLOGY_NOTE.md`), **não produz nenhum veredito de
significância computável em nenhuma das 4 combinações testadas** — mas
por DOIS motivos estruturais DISTINTOS, ambos honestamente diagnosticados
e nenhum deles um problema de poder de IAAFT: (1) `vfdb`, propriedade de
Markov nunca estabelecida na amplitude bruta de ECG (resultado
teoricamente esperado); (2) `eurchf`, `tau_ME` estabelecido mas `PKS`
estruturalmente indefinido no POST devido à magnitude do próprio choque
que motivou a escolha deste domínio — a regra "bins fixados do PRE"
(travada precisamente para evitar confundir mudança genuína de dinâmica
com re-estimação ad hoc) colide, neste caso específico, com um choque
grande demais para os bins do PRE resolverem.

Isso é o **9º candidato** desta linha (`DISC-TRI-RG-001`) a terminar sem
produzir um achado cross-domain sobrevivente: 7 anteriores (6 negativos
em dado real + RQA fechado na validação) + `entropia-de-permutacao`
(negativo em dado real, 8º) + agora `kramers-moyal` (indefinido/não
estabelecido em dado real, ambos os domínios, 9º).

## Nota metodológica para futuras tentativas nesta família (não decidida aqui)

Se esta linha ou uma linha futura tentar Kramers-Moyal/Fokker-Planck de
novo em um domínio com choque de magnitude comparável, a colisão
estrutural encontrada aqui (bins do PRE não cobrindo o POST) sugere que
a regra "bins fixados do PRE" — ótima para choques moderados, onde
preserva contra reestimação ad hoc — precisaria ser reconsiderada
explicitamente para choques de regime extremos (ex. bins definidos
sobre a UNIÃO do intervalo de PRE+POST, ou normalização por log-retorno
em vez de nível de preço). Isso é uma observação, não uma mudança de
metodologia — nenhuma decisão foi tomada ou implementada aqui, fica
registrada para quem avaliar a linha em seguida.

## Arquivos desta etapa

- `analysis/km_common.py` (pipeline, ver `VALIDATION_NOTE.md` para a
  correção do bootstrap do teste CK)
- `analysis/validate_synthetic.py`, `analysis/validation_synthetic.json`
  (validação sintética)
- `analysis/run_real_domain.py` (executor por domínio/variante)
- `data/prepare_vfdb.py`, `data/prepare_eurchf.py` (download + preparação,
  re-executáveis)
- `data/PROVENANCE_VFDB.md`, `data/PROVENANCE_EURCHF.md` (proveniência
  completa)
- `data/vfdb_{pre,post}_{primary,robust}.npy`,
  `data/eurchf_{pre,post}_{primary,robust}.npy` (segmentos derivados)
- `data/vfdb_segments_meta.json`, `data/eurchf_segments_meta.json`
- `analysis/result_vfdb_primary.json`, `analysis/result_vfdb_robust.json`,
  `analysis/result_eurchf_primary.json`, `analysis/result_eurchf_robust.json`
  (resultados completos)
- `VALIDATION_NOTE.md` (validação sintética completa)
- `METHODOLOGY_NOTE.md` (inclui o adendo de demoção de `beta_D2`,
  commit `9d35eeb`)

## Estado da linha e próximo passo

`TEST_QUEUE.yaml` e `DISCOVERY_LAB_STATE.md` NÃO foram atualizados por
este agente (decisão de governança/registro final da linha fica com a
sessão orquestradora, mesmo padrão já usado para `RQA` e
`entropia-de-permutacao`). Reexecução adversarial independente (passo 7
de `AGENTS.md`) e decisão sobre próximos passos da linha
`DISC-TRI-RG-001` (nova busca, considerar a linha suficientemente
explorada, etc.) ficam pendentes de decisão da sessão orquestradora.
