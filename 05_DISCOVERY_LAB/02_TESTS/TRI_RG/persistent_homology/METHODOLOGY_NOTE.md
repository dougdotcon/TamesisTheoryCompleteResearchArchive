# Nota de metodologia — fechamento dos gaps de `homologia-persistente` (TDA via filtração de Vietoris-Rips sobre embedding de Takens)

**Status:** decisões metodológicas fixadas ANTES de qualquer cálculo
real nos 2 domínios (deformação de onda gravitacional LIGO GW150914;
S&P500 ao redor da falência do Lehman Brothers). Mesmo espírito de
disciplina já usado para os 10 candidatos anteriores desta linha —
**último candidato formalizado (`viable=true`) da Fase 0.6, fecha a
rodada de busca completa se concluído.**

Ver `05_DISCOVERY_LAB/02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`
(candidato 3) para o levantamento que identificou este candidato como
`viable=true`, ranqueado #3 — matemática mais distinta de todas as já
testadas (topologia algébrica), domínio inédito genuinamente novo
(LIGO), mas com um risco de identificabilidade JÁ DEMONSTRADO
EMPIRICAMENTE (não só teórico) contra o RQA, e uma restrição
computacional real e MEDIDA (não hipotética).

## Contexto: o que já foi verificado na busca, o que falta

Já verificado (Fase 0.6): 2 domínios reais com dado baixado/inspecionado
— (a) deformação de tensão do LIGO, evento GW150914, dado real
decodificado (131.072 amostras reais, 4096Hz, sha256 registrado); (b)
S&P500 ao redor da falência do Lehman Brothers (15/09/2008), dado real
via Yahoo Finance. **Checagem de identificabilidade própria já rodada
na Fase 0.6:** instalação de `ripser`/`gudhi` e teste com senoide
ruidosa em 9 níveis de ruído, correlacionando persistência máxima de H1
com um análogo de `%DET`(RQA) — **correlação de Pearson r≈0,92** no
regime de degradação de estrutura mais relevante para detectar
transição. **Custo computacional medido diretamente** (não estimado):
crescimento pior que O(N²) na prática (3.240 pontos = 16,4s por
diagrama, single-core) — janelas grandes são inviáveis sem
subamostragem. Faltam: (a) regra de embedding — DELIBERADAMENTE
DIFERENTE da regra de FNN do RQA, por um motivo concreto explicado
abaixo; (b) definição de `I(X)` e canal companheiro, com um desenho de
sub-janelas que mantenha o custo computacional tratável; (c) declaração
de identificabilidade contra o achado de `r≈0,92` já medido; (d) PRE/POST,
incluindo um desenho específico para o LIGO (transição transiente, não
deriva gradual — estrutura diferente de todos os domínios anteriores
desta linha); (e) protocolo de significância.

## Gap (a): embedding de Takens — regra DIFERENTE da do RQA, por motivo concreto

**Por que não reaproveitar a regra de FNN do RQA:** a validação
sintética de `rqa` (`02_TESTS/TRI_RG/rqa/VALIDATION_NOTE.md`) já
demonstrou que Falsos Vizinhos Mais Próximos (Kennel et al. 1992) NUNCA
resolve `m<=10` para ruído branco/processos fracamente correlacionados —
achado estrutural, não um acaso daquele candidato específico, que
fecharia ESTE candidato exatamente da mesma forma se reaproveitasse a
mesma regra. **Mas homologia persistente não precisa da mesma condição:**
ao contrário de uma estatística baseada em limiar de recorrência (que
precisa "desdobrar" completamente o atrator para evitar vizinhos
falsos), a detecção topológica de laços (característica H1) é
comparativamente robusta a uma dimensão de embedding pequena e FIXA —
o próprio arcabouço teórico da literatura de persistência em janela
deslizante (Perea & Harer 2015, *Found. Comput. Math.* 15:799) usa
dimensões baixas fixas na maioria de suas aplicações (o teorema de
Takens só exige `m > 2*d_caixa` do atrator subjacente; para um laço
simples, `d_caixa=1`, então `m=3` já é suficiente com folga).

**Regra fixada:** `m=3` FIXO a priori (não reestimado, não FNN) —
escolha padrão e mínima segura da literatura de persistência em janela
deslizante para a característica H1. `tau` via mínimo local da
informação mútua (Fraser & Swinney 1986) — mesma regra JÁ auditada e
funcional em `rqa/analysis/rqa_common.py` (essa parte do RQA nunca
falhou; só o passo de FNN falhou) — reaproveitada aqui sem modificação,
com o mesmo fallback de cruzamento por zero da autocorrelação já
documentado.

## Gap (b): `I(X)`, canal companheiro, e desenho de sub-janelas para custo tratável

**Desenho de sub-janelas (controla o custo O(N²) já medido):**
`N_WINDOW=200` pontos embedded por diagrama de persistência (extremo
inferior da faixa 50-250 já usada na literatura, Gidea & Katz 2018;
Perea & Harer 2015 — escolha DIRETAMENTE motivada pelo custo medido na
Fase 0.6, declarada honestamente como restrição computacional, não
escolha arbitrária). Dentro de cada segmento (PRE ou POST), até
`K_SUBWINDOWS_MAX=10` janelas NÃO-sobrepostas de `N_WINDOW` pontos
embedded, escolhidas igualmente espaçadas cobrindo todo o segmento
disponível (não só o início) se houver mais que 10 janelas possíveis.
**Se um segmento tiver menos que `N_WINDOW` pontos embedded disponíveis
(nem uma janela completa), o segmento é REJEITADO por amostra
insuficiente** — declarado honestamente, não forçado, mesmo padrão já
usado em VG/RQA/EVT-Hill.

**Complexo de Vietoris-Rips:** `ripser` (`maxdim=1`, só precisamos de
H0/H1) sobre cada sub-janela de `N_WINDOW=200` pontos — tratável no
orçamento medido (custo bem abaixo do observado para 440+ pontos).

**`I(X)` primário:** mediana (sobre as até 10 sub-janelas) da
persistência MÁXIMA de H1 (maior intervalo nascimento-morte entre as
características H1 daquele diagrama — 0 se nenhuma característica H1
existir, um valor bem-definido, não indefinido).

**`I(X)` companheiro:** mediana da persistência TOTAL de H1 (soma de
todos os intervalos nascimento-morte de H1 naquele diagrama) — captura
complexidade topológica geral, distinta da persistência máxima isolada.

## Gap (c): declaração de identificabilidade — risco JÁ MEDIDO contra RQA (não hipotético)

**Risco central, já demonstrado empiricamente na Fase 0.6, não apenas
argumentado teoricamente:** a checagem própria do agente de pesquisa
(senoide ruidosa, 9 níveis de ruído, `ripser` instalado e rodado)
encontrou persistência máxima de H1 correlacionada com um análogo de
`%DET`(RQA) em `r≈0,92` no regime de degradação de estrutura mais
relevante para detectar transição. **Nota importante sobre o peso deste
achado:** o RQA, mesmo quando `%DET` FOI computável (controle positivo
de Rössler, após correção de desenho), NÃO mostrou poder real contra
IAAFT (`p=1,0` em ambos os canais) — então uma correlação com `%DET`
não implica automaticamente que a homologia persistente também careça
de poder; é um sinal de alerta concreto a testar, não uma sentença.

**Discriminador:** substituto IAAFT como teste PRIMÁRIO — mesma lógica
já usada em toda a linha (ao contrário de `evt-hill`, aqui o IAAFT É
apropriado: a característica H1 depende da ORDEM temporal via o
embedding de Takens, não só dos valores/marginal, então não sofre da
degenerescência já identificada e evitada em `evt-hill`). **Validação
obrigatória de PODER, ANTES de qualquer dado real:** controle positivo
sintético — PRE = ruído branco Gaussiano; POST = mapa logístico caótico
(`r=4`) com marginal e espectro casados por remapeamento de posto
(mesma técnica já usada com sucesso em MSE/VG/RQA/entropia-de-permutação)
— verificar que a persistência máxima/total de H1 real cai fora da
distribuição nula IAAFT. **Se a validação mostrar baixo poder** (mesmo
padrão de DFA-alpha): bootstrap por blocos móveis pré-autorizado
(Kunsch 1989), mesma correção já aplicada 2x nesta linha. **Se a
validação mostrar poder real:** isso já seria evidência direta de que a
persistência captura algo além do que o `%DET`(RQA) — que nunca
demonstrou poder — mede, apesar da correlação de `r≈0,92` em ruído
puro.

## Gap (d): definição de PRE/POST — inclui um desenho específico para o LIGO (transição transiente)

Regra domain-agnostic REAPROVEITADA para S&P500 (mesma convenção já
usada 10x nesta linha): PRE (primária) = todo o registro disponível
anterior à transição documentada; PRE (robustez) = os 50% mais recentes
desse PRE. POST (primária) = todo o registro disponível posterior à
transição, até o próximo evento documentado; POST (robustez) = os 50%
mais próximos da transição desse POST.

- **S&P500 (falência do Lehman):** transição = 15/09/2008 (documentado
  externamente). PRE = fechamentos diários antes de 15/09/2008 (mesmo
  histórico já verificado acessível). POST = fechamentos diários de
  15/09/2008 até o próximo evento macro claramente documentado (ex.
  aprovação do TARP, 03/10/2008, ou anúncio do QE1, 25/11/2008 — usar o
  que vier primeiro e for mais claramente documentado). **Nota honesta
  de risco, declarada a priori:** com `N_WINDOW=200` e resolução diária,
  o POST pode não ter 200 pregões disponíveis antes do próximo evento —
  se isso acontecer, o domínio é reportado honestamente como amostra
  insuficiente (Gap b), não contornado afrouxando `N_WINDOW` depois de
  ver o problema.

- **LIGO GW150914 (estrutura DIFERENTE — transição transiente, não
  deriva gradual):** ao contrário de todos os domínios anteriores desta
  linha, aqui a "transição" é um evento transiente de fusão
  (chirp+merger+ringdown, ~0,2-0,5s de varredura de frequência) dentro
  de um segmento contínuo de 32s a 4096Hz — exatamente o caso de uso
  clássico da literatura de persistência em janela deslizante
  (detecção de periodicidade/quase-periodicidade, Perea & Harer 2015).
  **Reaproveitando a MESMA regra PRE/POST sem modificação estrutural,
  só aplicada ao horário exato de fusão já documentado (GPS
  1126259462,4, API GWOSC, externo ao cálculo):** PRE (primária) = toda
  a deformação disponível antes do horário de fusão dentro do segmento
  de 32s. PRE (robustez) = os 50% mais recentes desse PRE. POST
  (primária) = toda a deformação disponível depois do horário de fusão
  até o final do segmento de 32s (inclui o ringdown E o ruído quieto
  subsequente — diluição esperada e reportada honestamente, não
  removida por engenharia reversa). POST (robustez) = os 50% mais
  próximos da fusão — captura preferencialmente o ringdown, que é
  exatamente onde a variante de robustez deveria ter mais poder por
  construção, uma coincidência favorável da convenção já padrão desta
  linha com a física deste domínio específico.

## Gap (e): protocolo de significância — IAAFT

Mesmo protocolo padrão desta linha: `N_SURROGATES=200`,
`N_IAAFT_ITER=50`, substitutos de PRE e POST gerados
INDEPENDENTEMENTE, `seed=12345`, teste BICAUDAL. Cada substituto passa
pela MESMA pipeline completa (embedding com `m=3`/`tau` recalculado por
substituto a partir de sua própria série — `tau` é barato de
recalcular, ao contrário do FNN do RQA que motivou fixar do PRE lá;
aqui não há esse mesmo motivo de custo, então recalcular por substituto
é mais fiel e não introduz o mesmo risco de viés). `p = fração de
substitutos com |Delta_mediana_persistencia_maxima_substituto| >=
|Delta_real|` (e igualmente para persistência total).

**Nota de custo computacional, orçamento estimado a priori:** ≈200
substitutos × 2 (PRE/POST) × até 10 sub-janelas × custo por diagrama
(medido, «0,5s para `N_WINDOW=200`) ≈ dezenas de minutos — mesma ordem
de grandeza dos candidatos anteriores mais caros desta linha (VG, RQA).

## O que este passo NÃO é

Continua Fase 0/exploratório — `DISC-TRI-RG-001` segue
`CANDIDATE_FORMULATING` em `TEST_QUEUE.yaml`, nenhum `PREREGISTRATION.md`
foi travado (mesmo padrão já usado nos 10 candidatos anteriores). A
metodologia acima foi fixada ANTES de qualquer cálculo, incluindo a
decisão deliberada de NÃO reaproveitar a regra de embedding do RQA (por
um motivo concreto, documentado, não um capricho) e de tratar o risco de
identificabilidade já medido (`r≈0,92` contra `%DET`) como uma hipótese
a testar via IAAFT, não como veredito antecipado.
