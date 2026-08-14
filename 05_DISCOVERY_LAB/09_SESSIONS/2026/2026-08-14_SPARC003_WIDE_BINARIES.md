# Sessão 2026-08-14 (continuação) — DISC-COSMOLOGY-MOND-SPARC-003: pré-registro, análise e fechamento

## Contexto

Após `DISC-TRI-RG-001` ser pausada a pedido do usuário (`DISC-DEC-005`),
usuário pediu para "começar a linha `DISC-COSMOLOGY-MOND-SPARC-003`" —
uma terceira linha de teste cosmológico/MOND, ainda não definida.

## Fase 0: busca de formulação

Três agentes investigaram em paralelo: (1) busca exaustiva por nova
alegação Tamesis-específica em `01_TAMESIS_CORE` — negativa, toda
fórmula adicional reproduz MOND padrão ou já foi auto-refutada; (2) a
discrepância de leverage do holdout de SPARC-002 como germe de teste —
negativa, variância de amostragem comum, sem alegação Tamesis a testar;
(3) dataset independente para replicar o veredito de SPARC-002 —
**positiva**: binárias largas do Gaia (El-Badry, Rix & Heintz 2021),
mesmo catálogo usado por Chae (2023) para testes de gravidade em regime
de aceleração ultra-baixa.

**Achado colateral grave:** `lab_gravity/analysis/gaia_real_analysis.py`
contém uma tabela de binárias largas rotulada como dado real do
El-Badry+2021 mas fabricada (IDs Gaia sequenciais, progressão de
velocidade artificialmente monotônica) — o achado "MOND DETECTED" em
`RESEARCH_RESULTS.md` descansa sobre esse dado. Registrado em
`TEST_QUEUE.yaml` campo `achado_de_integridade`, não corrigido nesta
sessão (fora do escopo do Discovery Lab).

Detalhes completos: `02_TESTS/COSMOLOGY_WIDE_BINARIES/phase0/PHASE0_SEARCH.md`.

## Pré-registro

Usuário pediu para prosseguir. Metodologia de Chae (2023) verificada por
fetch direto — descoberta e corrigida uma confusão de arXiv ID (o
título/ApJ 952,128 citado pertence a arXiv:2305.04613, não ao número
originalmente fornecido, arXiv:2309.10404, que é um artigo de
acompanhamento distinto do mesmo autor). Método primário de Chae
(desprojeção 3D via Monte Carlo orbital, dependente de excentricidades
de Hwang et al. 2022 não verificadas) declarado tratável demais para
reproduzir — adotado em vez disso o método de perfil de velocidade
projetada (Artigo B, simplificação declarada, real e publicada).

Catálogo real El-Badry+2021 baixado por completo (1,94GB, sha256
verificado duas vezes, 1.817.594 pares — contagem exata). Cortes de
qualidade reais de Chae aplicados: 43.147 sistemas sobrevivem. Massa
derivada via Pecaut & Mamajek (2013). Split discovery(30.203)/
holdout(12.944 selado) gerado com seed determinístico. H_A/H_B
idênticas às já travadas em SPARC-002. `PREREGISTRATION.md` travado e
commitado (`652e7e5`) antes de qualquer razão de velocidade calculada.

## Análise pré-registrada + reexecução adversarial

Usuário pediu para rodar a análise. Workflow com 2 fases: análise
primária, depois reexecução adversarial independente (segundo agente,
implementação do zero, sem ler o código/resultado primário até ter o
próprio pronto).

**Concordância bit a bit** em toda a parte determinística entre os dois
agentes — nenhum bug de fórmula, unidade, constante ou binagem em
nenhum dos dois scripts.

**Resultado:** as 5 medianas empíricas de `v_p_obs/v_p_N` por bin
(0,6932; 0,6409; 0,6243; 0,6150; 0,5941) são todas abaixo de 1 — mas o
modelo MOND pré-registrado, `(1-e^{-√(g_N/a0)})^{-1/2}`, tem imagem
estritamente em `(1,+∞)` para qualquer `a0>0` finito. **Não existe `a0`
que alcance o alvo.** Checagem de convergência (Seção 4) e checagem de
sanidade (Seção 3) — ambas já declaradas no pré-registro como
salvaguardas contra exatamente este tipo de problema — falharam:
convergência de `x0=1` e `x0=5` divergem ~16%; `a0` ajustado sai ~2,4
ordens de grandeza abaixo do valor de referência McGaugh.

**Causa raiz confirmada independentemente, não é bug:** o agente
adversarial rodou uma simulação Monte Carlo própria (N=200.000) de
binárias Keplerianas puramente Newtonianas (zero física MOND) e obteve
mediana(v_proj/v_circ)≈0,55 — mesma ordem de grandeza das medianas
observadas no dado real. É o efeito de diluição por projeção já
documentado na literatura (Pittordis & Sutherland 2018; Banik & Zhao
2018), já antecipado no preâmbulo da Seção 4 do pré-registro como
limitação declarada da estatística simplificada.

## Veredito

Por instrução explícita da própria Seção 3 do pré-registro ("o teste
para até isso ser resolvido, antes de aceitar qualquer veredito
H_A/H_B"): **nenhum veredito H_A/H_B é aceito.** O critério literal da
Seção 5, mecanicamente aplicado, produziria "BOTH_FALSIFIED" — mas isso
NÃO é lido como evidência real contra `a0_A` nem `a0_B`. Registrado como
`DISC-CLAIM-005`, `evidence_level: preregistered_inconclusive`,
`adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` (limitação
estrutural do desenho da estatística, não erro de implementação nem
falta de dado). Teste fechado `CLOSED_INCONCLUSIVE` em `TEST_QUEUE.yaml`
— o Gate de Replicação nunca foi acionado, já que o teste falhou sua
própria checagem de sanidade na amostra de descoberta. Holdout (12.944
sistemas) permanece selado, disponível para um teste futuro
genuinamente redesenhado.

**Lição de governança** adicionada a `METHODOLOGY_EXTENSIONS.md` Seção
1: antes de travar um pré-registro cuja estatística discriminadora
tenha uma imagem matematicamente derivável, validar via simulação
sintética/nula rápida que valores reais plausíveis não ficam
estruturalmente fora dessa imagem — evitaria descobrir o problema só
depois de processar 43 mil sistemas reais.

## Estado final

`DISC-COSMOLOGY-MOND-SPARC-001`: `CLOSED_INCONCLUSIVE`.
`DISC-COSMOLOGY-MOND-SPARC-002`: `REPLICATION_FAILED` (inconclusivo,
holdout não confirmou nem refutou).
`DISC-COSMOLOGY-MOND-SPARC-003`: `CLOSED_INCONCLUSIVE` (estatística
estruturalmente incapaz de produzir veredito válido). As três linhas da
trilha SPARC/MOND estão encerradas por ora. `DISC-TRI-RG-001` segue
pausada.

## Próxima decisão (não tomada nesta sessão)

Nenhuma linha ativa no momento. Opções para o usuário: retomar
`DISC-TRI-RG-001`; desenhar uma versão de SPARC-003 com desprojeção
Monte Carlo completa (reaproveitando o holdout selado e o catálogo já
baixado); investigar o achado de integridade de `gaia_real_analysis.py`
fora do Discovery Lab; ou outra linha inteiramente nova.
