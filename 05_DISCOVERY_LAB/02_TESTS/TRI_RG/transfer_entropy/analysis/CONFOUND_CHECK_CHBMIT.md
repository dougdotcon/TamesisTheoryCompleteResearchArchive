# Checagem de confundidor/reprodução adversarial — domínio CHB-MIT EEG

**Acionada por:** `result_chbmit_robust.json` mostrar UM `p<0,05`
isolado: `STE_sum`, substituto de deslocamento circular, `p=0,025` — o
MESMO canal/variante sob IAAFT dá `p=0,725` (nulo, sem qualquer
tendência de significância), e a variante PRIMÁRIA (não robustez) do
MESMO canal dá `p=0,425`/`0,18`. Nenhum outro canal (`TE_net`, `TE_sum`,
`STE_net`) mostra `p<0,05` em nenhuma combinação variante/nulo em todo
o domínio CHB-MIT. Script: `confound_check_chbmit.py`. Saída bruta:
`confound_check_chbmit_results.json`.

## Avaliação a priori da força da evidência

Já fraco/isolado por construção antes de qualquer checagem adicional:
(a) aparece em SÓ 1 dos 2 nulos pré-registrados para o MESMO
canal/variante (o IAAFT, nulo PRIMÁRIO desta linha, dá `p=0,725` —
completamente não-significativo); (b) é um canal de ROBUSTEZ (TE
Simbólica, não KSG); (c) não replica na variante primária do mesmo
canal. `VALIDATION_NOTE.md` já havia observado uma taxa de
falso-positivo de base `~8,3%` (`2/24`) no controle negativo sintético
sob condições NULAS conhecidas — este único `p=0,025` isolado é
plenamente compatível com esse nível de ruído esperado, não
necessariamente um sinal real.

## Checagem — pares de eletrodo alternativos (condução de volume, Nolte et al. 2008)

Risco nomeado a priori em `METHODOLOGY_NOTE.md`: condução de volume
entre eletrodos fisicamente próximos pode produzir "acoplamento"
espúrio. Dois pares adversariais testados na MESMA transição real
(onset `t=2996s`, `chb01_03.edf`), pipeline `run_te_analysis`
INALTERADA:

1. **Par PRÓXIMO** (`F7-T7`/`T7-P7`) — compartilha o eletrodo `T7` com
   o canal `Y` real (`T7-P7`), risco MÁXIMO de condução de volume entre
   os dois pares.
2. **Par DISTANTE/implausível** (`P4-O2`/`F8-T8`) — parieto-occipital
   direito vs. fronto-temporal direito, sem eletrodo compartilhado,
   sem relevância fisiológica óbvia para a zona de início ictal deste
   paciente.

| Par | Canal | `p` IAAFT | `p` deslocamento circular |
|---|---|---|---|
| Próximo (`F7-T7`/`T7-P7`) | `TE_net` | 0,115 | 0,16 |
| Próximo | `TE_sum` | 0,56 | 0,49 |
| Próximo | `STE_net` | 0,805 | 0,765 |
| Próximo | `STE_sum` | 0,805 | 0,63 |
| Distante (`P4-O2`/`F8-T8`) | `TE_net` | 0,135 | 0,155 |
| Distante | `TE_sum` | 0,075 | 0,08 |
| Distante | `STE_net` | 0,4 | 0,555 |
| Distante | `STE_sum` | 0,375 | 0,45 |

**Nenhum `p<0,05` em NENHUM canal, em NENHUM dos dois pares
adversariais.** O par PRÓXIMO (risco máximo de condução de volume) NÃO
mostra significância maior que o par DISTANTE/implausível — não há
evidência de que condução de volume esteja produzindo um efeito
genérico e sistemático nesta pipeline/domínio. Mas também: o achado
original isolado (`STE_sum` robustez, `FP1-F7`/`T7-P7`) simplesmente
NÃO REPLICA em nenhum par alternativo — nem mesmo no par mais
predisposto a artefato.

## Conclusão adversarial

**O único achado `p<0,05` deste domínio (`STE_sum`, robustez,
deslocamento circular apenas) não se replica em pares de eletrodo
alternativos, é contradito pelo nulo IAAFT no MESMO canal/variante, e é
plenamente compatível com a taxa de falso-positivo de base já
observada na validação sintética (`~8%`).** Não há evidência de
condução de volume como mecanismo sistemático (o par mais suscetível
não mostra efeito maior que um par arbitrário/implausível). Veredito
honesto: este achado isolado é mais bem explicado como ruído estatístico
esperado sob a nula do que como uma assinatura genuína de sincronização
ictal — nenhuma reprodução adversarial adicional é necessária além
desta.
