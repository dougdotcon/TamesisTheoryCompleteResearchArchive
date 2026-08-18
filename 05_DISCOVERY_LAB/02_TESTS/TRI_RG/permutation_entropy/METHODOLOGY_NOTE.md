# Nota de metodologia — fechamento dos gaps de `entropia-de-permutacao` (Entropia de Permutação Multiescala + Plano Complexidade-Entropia)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo real
nos 2 domínios (indução de anestesia via EEG, VitalDB; episódio
isquêmico transitório, PhysioNet European ST-T Database). Mesmo
espírito de disciplina já usado para os 7 candidatos anteriores desta
linha.

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`
(candidato 1) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #1 entre os 4 novos candidatos da Fase 0.6 —
melhores regras de parâmetro não-arbitrárias desta rodada, dois
domínios novos fortes já verificados por download real, e um risco de
identificabilidade já nomeado e citado na literatura (não hipotético).

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.6): 2 domínios reais com dado baixado/inspecionado
— (a) VitalDB (Seoul National University, EEG bruto de indução de
anestesia, 128Hz, rótulo externo `anestart` do sistema clínico); (b)
PhysioNet European ST-T Database, onset de episódio isquêmico transitório
dentro do mesmo registro contínuo, anotado por cardiologista (Taddei et
al. 1992). Nenhum `Delta I` calculado ainda. Faltam: (a) regra de
composição entre o coarse-graining multiescala (reaproveitado de MSE) e
o embedding ordinal de Bandt-Pompe, sem ambiguidade de notação; (b)
definição exata de `I(X)` e declaração de identificabilidade; (c)
definição de segmento PRE/POST; (d) protocolo de significância.

## Gap (a): composição de escalas — coarse-graining (reaproveitado de MSE) + embedding ordinal (Bandt-Pompe)

**Nota de notação, para evitar a ambiguidade que a literatura de
entropia de permutação multiescala às vezes carrega:** este pré-registro
usa `s` para o fator de escala do coarse-graining (o `tau` de Costa,
renomeado aqui só para não colidir com o `tau` do embedding de
Bandt-Pompe) e `tau_BP` para o atraso do embedding ordinal.

**Coarse-graining:** IDÊNTICO, reaproveitado sem modificação, ao
`R_lambda` já auditado de `mse_multiscale_entropy` — blocos NÃO
sobrepostos de tamanho `s`:
`x_j^(s) = (1/s) * sum_{i=(j-1)*s+1}^{j*s} x_i` (Costa, Goldberger & Peng
2002/2005).

**Embedding ordinal, aplicado a CADA série coarse-grained `x^(s)`:**
Bandt & Pompe (2002, *PRL* 88:174102), atraso `tau_BP=1` FIXO — convenção
padrão da literatura de Entropia de Permutação Multiescala (Aziz & Arif
2005; Morabito et al. 2012, *Entropy* 14), onde o próprio fator de
coarse-graining `s` já desempenha o papel de separação temporal
multiescala, evitando um parâmetro livre adicional que teria que ser
escolhido por escala.

**Ordem de embedding `m` — regra não-arbitrária, fixada a priori:** `m=4`,
o valor mais usado na literatura clínica/aplicada de entropia de
permutação (convenção amplamente citada desde Bandt & Pompe 2002, faixa
recomendada `m∈{3,...,7}`) — fixado UMA VEZ e mantido igual em todas as
escalas (mesma disciplina de "parâmetro fixo do canal, não reajustado
por escala" já usada para `r` em MSE). Piso de amostra mínimo por escala,
Riedl, Müller & Wessel 2013 (*Eur. Phys. J. Special Topics* 222:249):
`N_min_por_escala = 5*m! = 5*24 = 120`.

**Grade de escala domain-agnostic (fixada a priori, mesma lógica já
usada em CSD/DFA/MSE/VG — ligada ao que é de fato estimável, não a um
valor de tempo absoluto):**
- `s_min=1`.
- `s_max=floor(N/120)` (piso de 120 amostras por escala, Gap acima).
- `N_SCALES=min(15,s_max)` valores de `s`, log-espaçados entre `s_min` e
  `s_max`, arredondados para inteiros únicos.

## Gap (b): `I(X)` e declaração de identificabilidade

**`I(X)` primário:** `H_S(s)` — entropia de Shannon normalizada da
distribuição de padrões ordinais em cada escala `s`:
`H_S(s) = -sum_pi p(pi)*log(p(pi)) / log(m!)`. `PCI` (Índice de
Complexidade de Permutação) = soma de `H_S(s)` sobre a grade de escalas
— mesma estrutura de agregação já usada para `CI` em MSE.

**`I(X)` companheiro:** `C_JS(s)` — complexidade estatística de
Jensen-Shannon (Rosso, Larrondo, Martín, Plastino & Fuentes 2007, *PRL*
99:154102; construção MPR, Martín, Plastino & Rosso 2006):
`C_JS(s) = Q_0 * J[P(s),P_e] * H_S(s)`, onde `J[P,P_e]` é a divergência
de Jensen-Shannon entre a distribuição ordinal observada e a uniforme, e
`Q_0` a constante de normalização padrão. `MCI` (Índice de Complexidade
Multiescala) = soma de `C_JS(s)` sobre a mesma grade.

**Nota honesta de não-ortogonalidade, declarada a priori (não descoberta
depois):** `C_JS` inclui `H_S` como fator multiplicativo na própria
fórmula — os dois canais não são estatisticamente independentes por
construção (mesmo grau de não-ortogonalidade já aceito para `CI`/`beta`
em MSE ou `tau`/`sigma` em SOC). Isso não invalida usá-los como canais
primário+companheiro, só precisa ser dito claramente.

**Declaração de identificabilidade — risco CENTRAL, já documentado na
literatura, não hipotético (achado da Fase 0.6):** Zunino, Pérez,
Martín, Garavaglia, Plastino & Rosso 2008 (*Phys. Lett. A* 372:4768)
deriva, das fórmulas teóricas de probabilidade de padrão ordinal de
Bandt & Shiha, uma relação quase monótona entre `H_S` normalizado e o
expoente de Hurst `H` para fGn/fBm — `H_S` sozinho corre risco real de
ser reparametrização de `alpha`(DFA)/`h(2)`(wavelet), ambos já fechados
NEGATIVOS nesta linha. **Modelo concorrente nomeado e real:** processo
gaussiano autossimilar de `H` único (fGn/fBm), mesmo concorrente já
usado por `wavelet-multiresolution-scaling`, `dfa-multiscale-entropy`,
`mse-multiscale-entropy` e `grafo-de-visibilidade`.

**Discriminador:** substituto IAAFT como teste PRIMÁRIO de
significância para AMBOS os canais (`H_S`/`PCI` e `C_JS`/`MCI`) — mesma
lógica já validada com sucesso em MSE e parcialmente em VG. A previsão
honesta, baseada na literatura (não assumida como certa, testada como
hipótese): `C_JS`/`MCI` foi desenhado especificamente (Rosso et al.
2007) para separar ruído estocástico linear de dinâmica
caótica/determinística — deve, por construção teórica, comportar-se como
`CI`/`beta` de MSE (poder real contra IAAFT) em vez de como `alpha` de
DFA (sem poder, IAAFT reproduz quase exatamente). `H_S`/`PCI`, pelo
risco de Zunino et al. 2008, pode repetir o padrão de baixo poder já
visto em DFA-alpha. **Nenhum artigo publicado testou IAAFT contra
`C_JS` especificamente** (verificado por busca dedicada na Fase 0.6) —
esta seria uma checagem genuinamente nova desta linha, não replicação de
resultado já conhecido.

**Diferença estrutural favorável em relação ao RQA, já identificável a
priori:** ao contrário do embedding de Takens+FNN do RQA (que pode falhar
em RESOLVER para ruído branco/processos fracamente correlacionados,
achado decisivo que fechou RQA na validação), o embedding ordinal de
Bandt-Pompe é uma estatística combinatória direta sobre vetores de atraso
— sempre computável para qualquer `N>=m`, independente de estrutura de
correlação. Não há risco estrutural equivalente de "não-computabilidade"
aqui — mas isso é uma expectativa a priori, não uma garantia, e será
verificado empiricamente na validação sintética como qualquer outra
declaração desta nota.

**Se a validação repetir o padrão de baixo poder já visto em DFA-alpha
para QUALQUER canal:** adicionar teste complementar de bootstrap por
blocos móveis (Kunsch 1989) como PRIMÁRIO para esse canal, mesma
correção já aplicada 2x nesta linha (DFA, SOC), ANTES de tocar dado
real. **Se a validação mostrar que `H_S`/`PCI` genuinamente não tem
poder discriminativo além do já testado pela família Hurst:** esse canal
pode ser retirado do critério de decisão (mantido como diagnóstico),
mesma disciplina já aplicada a `d_B` em `grafo-de-visibilidade` — decisão
de governança tomada pela sessão orquestradora após ver o resultado da
validação, não pelo agente que a executa.

## Gap (c): definição de segmento PRE/POST

Regra domain-agnostic REAPROVEITADA sem modificação (mesma convenção já
usada 6x nesta linha — CSD, DFA, SOC, MSE, VG, RQA): PRE (primária) =
todo o registro contínuo disponível anterior à transição documentada;
PRE (robustez) = os 50% mais recentes (por CONTAGEM de amostras) desse
PRE. POST (primária) = todo o registro contínuo disponível posterior à
transição, até o próximo evento/confundidor documentado; POST
(robustez) = os 50% mais próximos da transição desse POST.

- **VitalDB (indução de anestesia):** transição = `anestart`, timestamp
  registrado pelo sistema de informação clínico do hospital (externo,
  não derivado do sinal). PRE = EEG antes da indução. POST = EEG após a
  indução, até o final do caso (`aneend`) ou até a próxima intervenção
  farmacológica documentada, o que vier primeiro.
- **PhysioNet European ST-T Database:** transição = onset do episódio
  isquêmico anotado por cardiologista (Taddei et al. 1992), externo ao
  cálculo de entropia. PRE = ECG antes do onset. POST = ECG durante o
  episódio, até o offset anotado ou o final do registro disponível.

## Gap (d): regra de subamostragem (custo computacional, mais barato que VG/RQA)

Ao contrário do grafo de visibilidade (O(N²)) e do RQA (matriz de
recorrência O(N²)), a contagem de padrões ordinais é O(N) por escala —
custo muito menor. Mesmo assim, uma regra de teto é fixada a priori
(consistência de orçamento computacional com o protocolo IAAFT de 200
substitutos × até 15 escalas): `MAX_N_PER_SEGMENT=20000` amostras,
decimação por *stride* uniforme se excedido, aplicada IGUALMENTE aos 2
domínios desta rodada.

## Gap (e): protocolo de significância — IAAFT como teste PRIMÁRIO

Mesmo protocolo já usado com sucesso em MSE/VG/RQA: `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, substitutos de PRE e POST gerados INDEPENDENTEMENTE
cada um da sua própria série real, `seed=12345`. Teste BICAUDAL. `p =
fração de substitutos com |Delta_H_S_substituto| >= |Delta_H_S_real|`
(e igualmente para `Delta_C_JS`), aplicado independentemente a `PCI` e
`MCI` agregados sobre a grade de escalas.

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado (mesmo padrão já usado nos 7 candidatos anteriores desta
linha de fechamento exploratório de gaps). A metodologia acima foi
fixada ANTES de qualquer cálculo, precisamente para que o risco de
redundância com Hurst já nomeado na Fase 0.6 — e a expectativa de que
`C_JS` (não `H_S`) seja o canal genuinamente discriminador — sejam
testados honestamente, não assumidos.
