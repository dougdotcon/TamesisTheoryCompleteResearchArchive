# Revisita de `DISC-TRI-RG-001` com os registros de backup do Apnea-ECG (2026-08-15)

**Contexto:** usuário pediu explicitamente para "revisitar os candidatos com
os registros de backup do Apnea-ECG" e, questionado sobre o escopo, optou
por tratar o banco Apnea-ECG como um DOMÍNIO FISIOLÓGICO NOVO para os 3
candidatos da linha (não só replicação do achado de DFA). Os 3 registros
mapeados na busca original (`a18`, `a14`, `a01`) foram baixados, decodificados
e processados por 3 agentes independentes (um por registro), cada um rodando
as 3 pipelines já validadas e travadas (`csd_common.py`, `wtmm_common.py`,
`dfa_common.py`) SEM MODIFICAÇÃO — `git diff` confirmado vazio nos 3 módulos
pelos 3 agentes.

**Nota metodológica declarada com transparência:** a regra de segmento
PRE/POST usada para os 3 candidatos nestes 3 registros foi a regra de
`dfa-multiscale-entropy`/`critical-slowing-down` (bloco N/A contínuo
completo; robustez = 50% por CONTAGEM de intervalos RR), não a regra
própria de `wavelet-multiresolution-scaling` (cap de 2h + truncamento ao
menor lado) — instrução explícita da tarefa era reaproveitar a mesma regra
de segmento nos 3 candidatos para manter os 3 comparáveis entre si nesta
revisita. Isso é uma pequena divergência da metodologia formal do wavelet,
documentada em cada JSON (`segment_rule_note`/`segment_rule_deviation_note`),
não escondida.

## Seleção de transição por registro

- **a18:** sequência limpa, transição única e óbvia: N(33min)→A(137min).
- **a14:** sequência com 8 transições N→A candidatas (não um único bloco
  limpo como `a04`/`a18`). Critério de desempate declarado a priori pelo
  agente responsável (produto do comprimento dos dois blocos) escolheu
  N(15min)→A(90min) — não a maior janela A disponível (223min), que tinha
  um PRE muito mais frágil (2min).
- **a01:** 3 transições candidatas; a regra "maior bloco N contínuo seguido
  de bloco A contínuo" (mesma regra de `a04`) escolheu a primeira:
  N(13min)→A(214min).

## Tabela consolidada — DFA (`Δalpha`, teste de bootstrap = primário)

| Registro | Variante | Δalpha (p_boot) | Δalpha1 (p_boot) | Δalpha2 (p_boot) |
|---|---|---|---|---|
| a04 | Primária | −0,134 (**0,000**) | +0,569 (**0,000**) | −0,366 (**0,000**) |
| a04 | Robustez | −0,169 (**0,018**) | +0,334 (**0,024**) | −0,346 (**0,002**) |
| a18 | Primária | −0,051 (0,650) | +0,254 (**0,042**) | −0,067 (0,424) |
| a18 | Robustez | −0,062 (0,552) | +0,231 (0,160) | −0,138 (0,148) |
| a14 | Primária | −0,195 (0,078) | +0,070 (0,884) | −0,323 (**0,040**) |
| a14 | Robustez | −0,478 (**0,000**) | −0,108 (0,032*) | −0,639 (**0,000**) |
| a01 | Primária | −0,243 (**0,000**) | +0,206 (**0,048**) | −0,333 (**0,000**) |
| a01 | Robustez | −0,237 (**0,012**) | +0,142 (0,196) | −0,352 (0,072) |

\* `a14` robustez: `Δalpha1` NEGATIVO (sinal invertido em relação a
`a04`/`a18`/`a01`, que são todos positivos), mas com `p_boot=0,032`
nominalmente significativo — direção oposta ao padrão dos outros 3
registros nesse canal específico.

**Leitura honesta:** a DIREÇÃO de `Δalpha` (queda) e `Δalpha2` (queda) é
**consistente nos 4 registros** — todos negativos, significativos em pelo
menos uma variante em 3 de 4 (`a18` é o mais fraco, nunca atinge `p<0,05`
em nenhum dos dois canais). `Δalpha1` (subida) replica a DIREÇÃO em 3 de 4
registros (`a04`, `a18`, `a01` — todos positivos, com significância
variável), mas `a14` mostra o canal `alpha1` sem sinal consistente
(positivo mas não-significativo na primária, negativo e nominalmente
significativo na robustez) — o único registro que não replica esse canal
específico.

## Tabela consolidada — Wavelet/WCM (`ΔC2`, `ΔC1`)

| Registro | Variante | ΔC2 (p) | ΔC1 (p) |
|---|---|---|---|
| a18 | Primária | −0,623 (**0,015**) | −0,214 (**0,010**) |
| a18 | Robustez | +0,445 (0,120) | −0,420 (**0,000**) |
| a14 | Primária | +0,326 (0,230) | −0,378 (**0,010**) |
| a14 | Robustez | −0,059 (0,920) | −0,431 (0,630) |
| a01 | Primária | −0,722 (**0,015**) | −0,352 (**0,000**) |
| a01 | Robustez | −0,732 (**0,045**) | −0,139 (0,050) |

(`a04` nunca teve o wavelet rodado — esta é a primeira vez que o método é
aplicado a apneia-ECG.) **Leitura honesta:** `ΔC2` é instável — inverte de
sinal entre variantes em `a18`, fraco em `a14`, só consistente e
significativo nos 2 testes de `a01`. `ΔC1` é mais consistente em direção
(negativo em 5 de 6 testes), mas a própria linha já havia identificado
`ΔC1`, no achado original de Tohoku/CHB-MIT, como um canal que
"provavelmente reflete apenas amplitude, não estrutura genuína" — a mesma
ressalva se aplica aqui sem verificação adicional.

## Tabela consolidada — CSD (`τ_AC1`, `τ_var`, só segmento PRE)

| Registro | Variante | τ_AC1 (p) | τ_var (p) |
|---|---|---|---|
| a18 | Primária | −0,053 (0,557) | +0,413 (0,280) |
| a18 | Robustez | −0,680 (0,889) | +0,433 (0,224) |
| a14 | Primária | +0,705 (0,099) | +0,668 (0,119) |
| a14 | Robustez | −0,087 (0,542) | −0,107 (0,547) |
| a01 | Primária | −0,262 (0,629) | +0,852 (**0,019**) |
| a01 | Robustez | +0,355 (0,299) | −0,478 (0,776) |

**Leitura honesta: nenhum sinal consistente.** Apenas 1 de 12 testes cruza
`p<0,05` (`a01`/primária/`τ_var`), inteiramente consistente com ruído sob
múltiplas comparações, e o próprio sinal AC1 nunca é significativo em
nenhum registro/variante — mesmo padrão de ausência de sinal já visto em
GISP2/SDDB/NASDAQ.

## Veredito da revisita

**A revisita NÃO resolve a exigência cross-domain da linha** — os 3
registros de backup são todos do MESMO banco/domínio físico (apneia-ECG)
já testado em `a04`, não um novo domínio físico distinto. O propósito
desta revisita (per decisão do usuário) era dar a `critical-slowing-down`
e `wavelet-multiresolution-scaling` uma chance real neste domínio (nunca
testado antes por eles) e checar se o achado de `dfa-multiscale-entropy`
em `a04` generaliza entre pacientes.

- **CSD:** sem sinal em nenhum dos 3 registros — mesmo veredito que em
  todos os outros domínios já testados por este candidato.
- **Wavelet:** `ΔC1` mostra um padrão direcionalmente consistente, mas essa
  é exatamente a estatística que a própria linha já suspeita refletir
  amplitude e não estrutura multifractal genuína (mesma ressalva do achado
  original de Tohoku/CHB-MIT) — não elevado a um achado positivo sem
  verificação adicional dedicada.
- **DFA:** a direção de `Δalpha`/`Δalpha2` (queda) **replica nos 4
  registros de apneia**, com `a18` sendo notavelmente mais fraco que os
  outros 3. Isto FORTALECE a leitura já registrada em
  `dfa_multiscale_entropy/RESULTS_SUMMARY.md`: o efeito é um fenômeno
  fisiológico real que generaliza (parcialmente) entre pacientes com
  apneia — mas continua sendo a MESMA explicação mundana já identificada
  pela descoberta adversarial de nulos (CVHR, Guilleminault et al. 1984),
  não um ingrediente novo de invariante cross-domain. `alpha1` (o canal
  mais dramático em `a04`) é o menos replicável dos 3 canais entre
  pacientes (inconsistente em `a14`).

**Checagem adversarial adicional NÃO foi acionada para os registros de
backup** — declarado explicitamente, não escondido: os tamanhos de efeito
aqui são bem mais modestos que o 6/6 original de `a04` (a maioria dos
testes individuais não atinge `p<0,05`, com inversões de sinal entre
variantes em vários casos), e o mecanismo mundano (CVHR) já identificado
para `a04` é a explicação mais parcimoniosa também para este padrão mais
fraco e heterogêneo entre pacientes — repetir uma reexecução adversarial
completa (extração cega + debunker dedicado) para cada um dos 3 novos
registros teria custo alto e valor marginal baixo dado que não mudaria o
veredito cross-domain da linha (que já depende do 2º domínio verdadeiro,
GISP2, não replicado).

## Estado final

Os 3 candidatos da linha `DISC-TRI-RG-001` continuam sem produzir um
invariante cross-domain confiável. A revisita com os registros de backup
do Apnea-ECG acrescenta contexto útil (generalização parcial do achado de
DFA entre pacientes; primeira aplicação de CSD e wavelet a este domínio,
ambos sem achado robusto novo) mas não muda o veredito geral da linha.
Toda a infraestrutura desta revisita (9 arquivos de resultado, dados brutos
de 3 registros adicionais) fica commitada e reaproveitável.
