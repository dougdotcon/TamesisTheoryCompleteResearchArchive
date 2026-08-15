# Sessão 2026-08-14 (continuação) — retomada de DISC-TRI-RG-001, fechamento de dfa-multiscale-entropy

## Contexto

Após `DISC-TRI-RG-001` ficar pausada (`DISC-DEC-005`) e a trilha
SPARC/MOND ser encerrada (`DISC-COSMOLOGY-MOND-SPARC-003`
`CLOSED_INCONCLUSIVE`), usuário pediu explicitamente: "retome a linha
DISC-TRI-RG-001".

## Busca de domínio para o terceiro candidato

O candidato `dfa-multiscale-entropy` (rank 3 na Fase 0) tinha a execução
técnica mais sólida dos 5 candidatos avaliados, mas foi rebaixado por usar
comparações ESTÁTICAS de classe (saudável vs. insuficiência cardíaca;
continental vs. oceânico) em vez de transições temporais dentro do mesmo
sistema — exigência central da linha. Um agente de busca dedicado
investigou 4 bancos PhysioNet e encontrou: **Apnea-ECG Database, registro
`a04`** (AHI=77,4, apneia severa) — 35 min de sono normal seguidos
imediatamente por 140 min contínuos de apneia, mesmo paciente, mesmo
registro, rótulo clínico externo minuto-a-minuto. Segundo domínio
cross-domain: paleoclima GISP2, reaproveitado de `critical-slowing-down`
(mesma transição Younger Dryas→Preboreal, mesmo dado já verificado).

## Metodologia e uma correção pré-dado-real

Metodologia de fechamento de gaps (regra de escala DFA, definição PRE/
POST, protocolo de substitutos) fixada e commitada em
`METHODOLOGY_NOTE.md` ANTES de qualquer cálculo final. A validação
sintética obrigatória (executada antes de tocar dado real) revelou que o
teste IAAFT bicaudal originalmente especificado tem baixo poder para
`alpha` — o controle positivo sintético (H=0,5→H=0,9, mudança inequívoca
por construção) não atingiu `p<0,05` (`p=0,255`), porque substitutos
IAAFT preservam o espectro linear exato de cada segmento, e `alpha` é
essencialmente uma quantidade espectral. **Corrigido antes de qualquer
dado real**: adicionado teste complementar de bootstrap por blocos
móveis (Künsch 1989), que passou a ser o teste PRIMÁRIO de significância
desta linha — mesma disciplina já registrada em `METHODOLOGY_EXTENSIONS.md`
Seção 1 após o achado estrutural de SPARC-003 (validar comportamento da
estatística contra sintético/nulo ANTES de gastar tempo em dado real).
Revalidação confirmou poder recuperado no controle positivo (`p=0,0`) e
controle negativo corretamente não-significativo (`p=0,384`).

## Análise real e checagem adversarial

Pipeline aplicada sem modificação aos 2 domínios por 2 agentes
independentes. **Apneia-ECG:** sinal forte nos 6 testes de bootstrap
(3 canais × 2 variantes, `p<0,05`, maioria `p<0,001`). Dado o tamanho do
efeito, acionada checagem adversarial completa (Extensão de Metodologia
5), mesmo padrão já usado para o achado inicial de Tohoku em
`wavelet-multiresolution-scaling`:

- **Reexecução adversarial cega** (extração de RR do zero, sem ler
  código/resultado do primeiro agente): segmentos primários batem ~byte a
  byte. Efeito sobrevive a winsorização (não é outlier), mas o canal
  `alpha` completo perde significância sob truncamento severo do POST;
  trajetória dentro do POST é flutuante, não monotônica (consistente com
  a natureza cíclica da apneia, já declarada a priori).
- **Descoberta adversarial de nulos**: rejeitou desequilíbrio de N (nulo
  sintético com mesmo N não reproduz o efeito) e contaminação por
  ectópico (winsorização FORTALECE o efeito, o oposto do esperado).
  Encontrou um mecanismo mundano positivo: **CVHR** (Cyclical Variation of
  Heart Rate, Guilleminault et al. 1984) — pico espectral de ~41-48
  batimentos no POST (73,7% da potência relevante) batendo exatamente com
  o AHI documentado do paciente. Confundidor de estágio do sono não
  totalmente descartável com um único registro (literatura mostra DFA
  discrimina estágio do sono melhor que severidade de apneia — Penzel et
  al. 2003). Viés de seleção não resolvido (3 registros de backup nunca
  executados).

**GISP2** não replicou o sinal: 5 dos 6 testes de bootstrap não
significativos.

## Veredito

`dfa-multiscale-entropy`, como os outros 2 candidatos antes dele, **não
produz um invariante cross-domain confiável**. O achado isolado em
apneia-ECG é real e sobrevive a checagem de artefato, mas é explicado por
fisiologia já conhecida (CVHR), não por qualquer ingrediente novo de
`DISC-TRI-RG-001`, e não replica no segundo domínio já calculado por esta
própria linha.

## Estado final da linha

Os 3 candidatos viáveis da Fase 0 (`critical-slowing-down`,
`wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`) testados com
rigor completo — os 3 resultado NEGATIVO. Nenhum `PREREGISTRATION.md`
escrito em nenhum dos 3. Toda a infraestrutura (3 pipelines validadas, 9
domínios/variantes testados no total) commitada e reaproveitável.

## Próxima decisão (não tomada nesta sessão)

Três rotas honestas, nenhuma decidida: (a) nova busca por candidatos TRI-RG
ainda não considerados; (b) revisitar os 3 candidatos já testados com
domínios/dados diferentes (ex. registros de backup do Apnea-ECG); (c)
considerar a linha suficientemente explorada por ora.
