# Checagem de confundidor / reprodução adversarial — Kīlauea (canal `spectral_gap`)

**Acionada por:** `p_spectral_gap=0,0` em AMBAS as variantes reais de
Kīlauea (`result_kilauea_primary.json`, `result_kilauea_robust.json`) —
per a regra obrigatória desta linha ("se qualquer achado mostrar
`p<0,05`, rodar reprodução adversarial/checagem de nulo antes de reportar
como real"). **O canal PRIMÁRIO desta candidatura (`f_dom`, `zeta`) NÃO
mostrou significância em NENHUMA das duas variantes** (`p_f_dom=0,765` e
`p_zeta=1,0` na primária; `p_f_dom=0,455` e `p_zeta=0,345` na robustez) —
só o canal COMPANHEIRO (`spectral_gap`) cruzou `p<0,05`, e só ele é
investigado aqui.

Script: `analysis/confound_check_kilauea.py`. Resultado completo:
`analysis/confound_check_kilauea_results.json`. 4 checagens, `n_mc=50`
(reduzido do `N_SURROGATES=200` travado — checagens exploratórias
adversariais, não o teste confirmatório primário, que já está fechado em
`result_kilauea_{primary,robust}.json` e não é recalculado aqui).

## Resumo honesto, sem suavizar: o achado NÃO sobrevive a NENHUMA das 4 checagens

| Checagem | `spectral_gap`: PRE→POST | Δ | `p` | Veredito |
|---|---|---|---|---|
| (a) Placebo, divisão arbitrária dentro do PRE (sem transição real) | 0,00201→0,00621 | +0,0042 | **0,02** | Significativo MESMO sem transição real — risco de falso-positivo genérico do canal/domínio confirmado |
| (b) Exclusão do M6,9 (POST primária truncado 6h antes do mainshock) | 0,00479→0,01149 | +0,0067 | 0,08 | Perde significância; magnitude cai ~73x frente ao POST completo (0,495→0,011) |
| (c) Bootstrap, primária (`n_bootstrap=50`) | delta médio bootstrap ≈0,00076 (real: 0,490) | — | **0,615** | Contradiz o IAAFT (`p=0,0`) — não significativo, delta bootstrap ~640x menor que o delta real |
| (c) Bootstrap, robustez (`n_bootstrap=50`) | delta médio bootstrap ≈−0,0009 (real: +0,0228, SINAL TROCADO) | — | **1,0** | Contradiz o IAAFT (`p=0,0`) — não significativo, delta bootstrap com sinal INVERTIDO ao real |

## (a) Placebo — divisão arbitrária dentro do PRE, sem transição real

`PRE` (24h) dividido ao meio (`12h`/`12h`), tratado como
pseudo-PRE/pseudo-POST, SEM qualquer transição documentada entre as duas
metades — ambas são tremor de fundo ANTES da abertura de fissura.
`spectral_gap`: `0,00201→0,00621` (Δ=+0,0042), **`p=0,02`** — cruza o
limiar `p<0,05` mesmo sem nenhuma transição real. **Achado adicional não
solicitado, mas honesto:** o próprio canal PRIMÁRIO (`zeta`) TAMBÉM
mostrou `p=0,02` neste placebo (`zeta`: `0,408→0,999`), apesar de NÃO
mostrar significância na transição REAL em nenhuma das duas variantes
(`p_zeta=1,0` primária, `0,345` robustez). Isto é um sinal de alerta
GENÉRICO sobre a especificidade deste domínio/pipeline para dado sísmico
real longo e fortemente não-estacionário: divisões arbitrárias de tremor
de fundo já produzem `p<0,05` ocasionalmente, tanto no canal companheiro
quanto no primário — não é exclusivo do `spectral_gap`.

## (b) Exclusão do terremoto M6,9 — teste direto do confundidor mais óbvio deste domínio

A janela POST primária (`2018-05-03T18:00` a `2018-05-04T22:32:54 UTC`)
TERMINA exatamente na hora de origem do terremoto M6,9 de flanco sul —
ou seja, a janela POST completa captura o abalo principal e sua forte
sismicidade associada bem no fim do registro. Truncando POST para
terminar 6h ANTES do M6,9 (removendo diretamente o sinal de forte
movimento do abalo principal): `spectral_gap` POST cai de `0,495` (janela
completa) para `0,0115` (truncada) — **queda de ~43x no valor absoluto**,
e o Δ cai de `0,490` para `0,0067` (**queda de ~73x**), perdendo
significância (`p: 0,0→0,08`). **Isto identifica diretamente a causa
mais provável do efeito extremo da variante PRIMÁRIA: o terremoto M6,9
em si, cuja forma de onda de altíssima energia domina trivialmente
qualquer decomposição espectral/modal de uma janela que o contenha —
sem relação alguma com uma assinatura precursora de bifurcação
oscilatória tipo Hopf, a hipótese original deste candidato.**

## (c) Bootstrap por blocos móveis (Kunsch 1989) — método de significância alternativo pré-autorizado

Reaproveita `run_block_bootstrap_test_dmd` (já implementado em
`dmd_common.py`, pré-autorizado como fallback em `METHODOLOGY_NOTE.md`),
aplicado aqui como CHECAGEM ADVERSARIAL (não como substituição do teste
primário) sobre os `(tau,d)` já travados de cada variante real,
`n_bootstrap=50` (reduzido de `N_BOOTSTRAP=1000` por custo computacional
— suficiente para uma checagem de direção/ordem de grandeza).

**Resultado, em ambas as variantes: o bootstrap CONTRADIZ o IAAFT.**
Reamostras de blocos móveis (`L=10`, comprimento ligado a `tau`) do PRE
real e do POST real, respectivamente, produzem valores de
`spectral_gap` tipicamente muito mais PRÓXIMOS entre si do que os valores
REAIS de PRE/POST — o delta médio bootstrap (`≈0,00076` na primária,
`≈−0,0009` na robustez, esta última com SINAL INVERTIDO ao delta real
`+0,0228`) é uma fração minúscula do delta real observado (`0,490` na
primária). Interpretação honesta: o embaralhamento de blocos (que
preserva estrutura de curto alcance mas destrói continuidade/coerência
temporal de longo alcance) impede que o DMD recupere o mesmo modo
dominante artificialmente extremo que aparece na série REAL contínua —
consistente diretamente com a checagem (b): o efeito extremo depende de
um evento CONTÍNUO e LOCALIZADO (o M6,9 na primária) cuja coerência
temporal é destruída pelo embaralhamento de blocos. Para a ROBUSTEZ
(que não contém o M6,9), o mesmo padrão de contradição aparece de forma
ainda mais direta (sinal invertido) — reforçando que mesmo o achado da
variante robustez não é uma propriedade estável/replicável da dinâmica
típica de POST, é sensível à ordem temporal exata da série específica
observada.

## Veredito honesto e completo

**O achado `spectral_gap` de Kīlauea (`p=0,0` em ambas as variantes sob
IAAFT) NÃO sobrevive a NENHUMA das 4 checagens adversariais.** Padrão
mais decisivo do que o já visto nesta linha para `lempel_ziv_complexity`
(cujo achado de Daphnet sobreviveu a 3 checagens de confundidor antes de
falhar em generalização entre sujeitos e em substituto alternativo) — aqui
o achado falha já na checagem de confundidor mais óbvia e específica do
domínio (b), falha na checagem de especificidade genérica (a), e falha
de forma ainda mais direta no método de significância alternativo
pré-autorizado (c), em AMBAS as variantes. **Conclusão: o `p=0,0` de
`spectral_gap` em Kīlauea é um artefato — primariamente o terremoto
M6,9 dominando trivialmente a decomposição espectral da variante
primária, e mais genericamente uma sensibilidade do canal/domínio a
divisões arbitrárias de tremor sísmico longo e não-estacionário — não
uma assinatura genuína de bifurcação oscilatória relacionada à erupção.**

Nota adicional, para registro: este resultado é sobre o canal
COMPANHEIRO (`spectral_gap`), que nunca teve seu poder discriminativo
formalmente estabelecido pela validação sintética obrigatória (ver
`VALIDATION_NOTE.md` — `p_spectral_gap` nunca cruzou `0,05` em nenhum dos
4 controles de Stuart-Landau, incluindo um valor de `p=0,07` no controle
NEGATIVO v1, um sinal de alerta de risco de falso-positivo já visível
antes de qualquer dado real). O canal PRIMÁRIO desta candidatura
(`f_dom`, `zeta`) — o único cuja validação sintética estabeleceu poder
real (`zeta`, seção 3 de `VALIDATION_NOTE.md`) — permanece SEM
significância em NENHUMA das duas variantes reais de Kīlauea, em nenhum
momento desta investigação.
