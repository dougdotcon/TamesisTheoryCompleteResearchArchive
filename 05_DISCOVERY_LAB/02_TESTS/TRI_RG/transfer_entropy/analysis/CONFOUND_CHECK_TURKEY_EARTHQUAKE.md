# Checagem de confundidor/reprodução adversarial — domínio Terremotos da Turquia

**Acionada por:** `result_turkeyeq_primary.json` mostrar `p<0,05` em 3
combinações canal/nulo: `TE_net` (`p_iaaft=0,04`), `TE_sum`
(`p_iaaft=0,005`, `p_circular_shift=0,0`), `STE_sum`
(`p_iaaft=0,0`). Script: `confound_check_turkey_eq.py`. Saída bruta:
`confound_check_turkey_eq_results.json`,
`confound_check_turkey_eq_check_b_corrected.json`,
`confound_check_turkey_eq.log`.

## Descoberta feita ao inspecionar o dado real (não hipotetizada antes, não fabricada)

A série de RMS-por-bloco de `PRE/X` (GAZ, 24h de fundo antes do M7,8)
tem uma anomalia grande, suave e monotonicamente decrescente ocupando os
primeiros `320` de `720` blocos (`t=[0,638]min`, ~10,6h do INÍCIO da
janela PRE) — de `1.677.000` (já no primeiro bloco) subindo levemente a
`1.963.000` por volta do bloco `~317`, caindo abruptamente para o nível
de fundo normal (`~7.300`) no bloco `~320`, e permanecendo estável
(`mediana=7.195`, `máx=9.814`) pelos `400` blocos restantes (últimas
~13,3h da janela PRE). **`PRE/Y` (BNN) não mostra NADA de anormal no
mesmo intervalo de tempo absoluto** (mediana `~10.877` estável do início
ao fim) — um evento sísmico regional real apareceria, mesmo que
atenuado, nas DUAS estações; um artefato específico da estação GAZ não.
A queda abrupta coincide, em tempo absoluto, com as pequenas lacunas de
dado já documentadas em `PROVENANCE_TURKEY_EARTHQUAKE.md`
(`2023-02-05T11:55:32`-`11:57:31 UTC`, muito próximo do bloco `~319`,
`t=638min` após `01:17:34` = `~11:55 UTC`).

**Interpretação:** consistente com um transiente instrumental de longa
duração e baixa frequência em GAZ (p.ex. recentralização de massa de
sismômetro de banda larga, fenômeno bem documentado na literatura de
instrumentação sismológica), NÃO um sinal sísmico real — confirmado
diretamente pela checagem (c) abaixo: um filtro passa-alta padrão de
1Hz remove a anomalia quase inteiramente (mediana filtrada cai de
`~1.8 milhão` para `17,2`), demonstrando que a energia está concentrada
em frequências MUITO abaixo do que se espera de energia sísmica local
genuína.

## Checagem (a) — MANDATÓRIA: divisão placebo dentro do PRE (sem transição real nenhuma)

`pseudo-PRE` = blocos `[0,360)` do PRE real (majoritariamente
contaminado); `pseudo-POST` = blocos `[360,720)` do PRE real
(majoritariamente limpo) — NENHUMA transição real, é o MESMO regime de
fundo do início ao fim.

| Canal | `p` IAAFT | `p` deslocamento circular |
|---|---|---|
| `TE_net` | 0,115 | 0,985 |
| `TE_sum` | 0,12 | 0,035 |
| `STE_net` | 0,135 | 0,095 |
| `STE_sum` | **0,0** | 0,93 |

**`STE_sum` mostra significância EXTREMA (`p=0,0`) numa divisão placebo
sem transição real nenhuma** — evidência direta de que a "significância"
de `STE_sum` no teste real não é confiável: o próprio artefato de
contaminação, sozinho, sem qualquer terremoto envolvido, já produz esse
padrão.

## Checagem (b) — re-teste PRE-vs-POST real usando SOMENTE o PRE limpo

**Correção de rótulo, nomeada honestamente:** a primeira tentativa desta
checagem (`confound_check_turkey_eq_results.json`, `check_b_clean_pre`)
usou por engano o CORTE ERRADO (`bins[0:303)`, que na verdade é a
região MAIS contaminada, não a limpa) — um erro de rotulagem cometido
durante a implementação da checagem adversarial, corrigido na mesma
sessão antes de reportar qualquer conclusão baseada nele. A versão
CORRIGIDA (`confound_check_turkey_eq_check_b_corrected.json`) usa
`bins[320:720)` do PRE real (verificado limpo: mediana `7.195`, máximo
`9.814`) contra o POST real (inalterado):

| Canal | `Delta` real | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|
| `TE_net` | `None` (embedding não resolve subjanela válida no PRE limpo curto, ver nota) | `None` | `None` |
| `TE_sum` | `None` | `None` | `None` |
| `STE_net` | -0,0248 | 0,965 | 1,0 |
| `STE_sum` | +0,1807 | 0,79 | 1,0 |

**Nenhuma significância em canal nenhum.** `TE_net`/`TE_sum` (KSG)
retornam `None` honestamente — diagnosticado: com o PRE limpo reduzido a
`400` blocos, o embedding de Ragwitz-Kantz escolhido em `X` (`m=7,
tau=37`) exige `>=222` amostras de história, excedendo
`L_SUB=200` (o comprimento de subjanela da regra de sub-janelamento) —
`0` subjanelas KSG válidas no PRE, reportado como `None`, não um valor
espúrio. Isto é uma falha de diagnóstico HONESTA (mesma disciplina desta
linha de nunca substituir silenciosamente), não uma evidência a favor
OU contra a hipótese — mas `STE_net`/`STE_sum` (que NÃO dependem dessa
restrição de sub-janela tão severa) mostram ausência TOTAL de
significância (`p` entre `0,79` e `1,0`).

## Checagem (c) — reprodução com filtro passa-alta (1Hz), dado rebaixado

Forma de onda bruta rebaixada nesta sessão (`GAZ`/`BNN`, PRE e POST),
`detrend(linear)` + `highpass(1Hz, 4 polos, fase zero)` aplicado ANTES
do *binning* de RMS — remove exatamente o tipo de deriva instrumental de
baixa frequência identificado acima.

| Canal | `Delta` real | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|
| `TE_net` (PRIMÁRIO) | +0,028 | 0,305 | 0,41 |
| `TE_sum` (companheiro) | -0,017 | 0,61 | 0,545 |
| `STE_net` | -0,089 | 0,82 | 0,37 |
| `STE_sum` | -0,590 | 0,04 | **0,0** |

**O canal PRIMÁRIO (`TE_net`) e seu companheiro (`TE_sum`) — os ÚNICOS
com achado `p<0,05` no dado bruto sob AMBOS os nulos — NÃO sobrevivem à
filtragem correta.** `STE_sum` continua mostrando `p` baixo mesmo
filtrado — mas já demonstrado na checagem (a) que `STE_sum` dispara
significância mesmo numa divisão placebo SEM transição real, um padrão
de sobre-sensibilidade genérica do estimador simbólico neste domínio de
`N` pequeno (esparsidade combinatória, `24³=13.824` estados possíveis
contra `~100`-`700` pontos — risco nomeado a priori em
`METHODOLOGY_NOTE.md`), não uma assinatura de acoplamento real.

## Checagem (d) — isolamento/exclusão do início do POST (primeiras 2h após o M7,8)

| Variante | `TE_net` `p` IAAFT/circular | `TE_sum` `p` IAAFT/circular | `STE_sum` `p` IAAFT/circular |
|---|---|---|---|
| Só as primeiras 2h do POST | `None`/`None` (amostra insuficiente) | `None`/`None` | 0,02 / 1,0 |
| Excluindo as primeiras 2h do POST | 0,91 / 0,985 | 0,195 / 0,815 | 0,0 / 1,0 |

Mesmo padrão: `TE_net`/`TE_sum` nunca mostram significância consistente
sob os dois nulos em nenhuma das duas variantes; `STE_sum` continua
errático (significante sob IAAFT, nunca sob deslocamento circular) —
consistente com o diagnóstico de esparsidade, não com um sinal robusto.

## Conclusão adversarial

**O achado `p<0,05` original de `TE_net`/`TE_sum` (canais PRIMÁRIO e
companheiro, os únicos formalmente centrais desta candidatura) é um
ARTEFATO explicado por um transiente instrumental de baixa frequência
específico da estação GAZ no início da janela PRE — não sobrevive à
filtragem passa-alta padrão que remove exatamente esse artefato
(checagem c), nem é replicável usando somente a porção verificadamente
limpa do PRE (checagem b, onde os canais KSG não puderam sequer ser
calculados por amostra insuficiente, mas os canais simbólicos mostram
ausência total de sinal).** O achado de `STE_sum` (canal de
robustez/companheiro do estimador simbólico) é separadamente
descartado: ele dispara significância mesmo numa divisão PLACEBO sem
nenhuma transição real (checagem a) — sinal claro de sobre-sensibilidade
do estimador simbólico à esparsidade combinatória neste domínio de `N`
pequeno, um risco nomeado a priori em `METHODOLOGY_NOTE.md`, agora
confirmado empiricamente, não apenas hipotético.

**Nenhum dos 2 achados `p<0,05` originais deste domínio sobrevive à
reprodução adversarial.** Mesmo padrão de refutação já visto em
`dmd_koopman`/Kīlauea (achado explicado por um mecanismo mundano
concreto, não por dinâmica genuína ligada à hipótese original) — aqui
ainda mais decisivo, porque o mecanismo mundano nem é um terremoto real,
é um artefato de instrumentação.
