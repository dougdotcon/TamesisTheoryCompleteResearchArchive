# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-25 (`DISC-DEC-073`: integração da
onda 17 frente (b) — `SHARP-RATE-REASSEMBLY-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND WITH NAMED ISSUES**, "ACCEPT for catalogue"). **O item
"trivial-mas-não-executado" do Estágio 19 está EXECUTADO e FECHADO —
Teorema R: `|φ(n,c)−φ_∞(c)| ≤ [a*√c + κ_B]/n` para `n≥4`, `0≤c≤n`,
ESTRITO em `(0,n]`**, com a constante aditiva `κ_B≈0,2805` INALTERADA
(por independência estrutural: ela vive inteiramente na metade `B_n`,
que nunca referencia (U′) nem `a`) e agora, pela primeira vez,
CERTIFICADA em aritmética racional pura: `κ_B∈(0,28048, 0,2805)`
(branch-and-bound de 1.525 folhas — eleva o apontamento F-9 da onda
11). O bound é assintoticamente justo na linha `c=n` (razão→1), logo
`a*` é a melhor constante multiplicativa possível nesta forma;
melhoria de fator 6,14 no coeficiente de `√c`. Frente: 2.594 células
certificadas, 0 violações; sessão: 404 células independentes na linha
de contorno, 0 violações; referee: engine próprio validado por força
bruta, `κ_B` re-certificada (mesma contagem de folhas, mesma folga
mínima), 1.060 células com 0 violações, contorno empurrado a
`n=50.000`, e a álgebra `K=n` do Estágio 19 re-derivada do zero. Duas
questões nomeadas, nenhuma tocando teoremas: R-1 (estatística "pior
razão 0,970" corrigida para ≈0,9904, erro na direção segura) e O-1
(nit de domínio de citação herdado do Estágio 12); 2 adendos datados.
Integrado como "Estágio 22" em `THEOREM.md`, pointers datados nos
Estágios 12, 19 e 21. Onda 17: 1/5 integradas; (a) K-geral e (e) lei γ
com referees em andamento; (c) e (d) em pesquisa. Anterior:
`DISC-DEC-072`: autorização e
despacho da onda 17 — 5 frentes matemáticas puras paralelas, uma para
cada item aberto nomeado no fechamento da onda 16, sob a política
permanente DISC-DEC-023 e a diretiva do usuário de nunca parar: (a)
`CONJECTURE-1-K5-GENERAL-ATTEMPT` (K=5, e K geral se a identidade de
florestas ponderadas do Estágio 20 render argumento uniforme; risco
incerto); (b) `SHARP-RATE-REASSEMBLY-ATTEMPT` (taxa nítida em `c` com
`a*` — o item "mecânico mas não executado" do Estágio 19; risco baixo);
(c) `JOINT-TWO-POINT-EXPLORATION-ATTEMPT` (a obstrução localizada pelo
Estágio 18, chave comum das Conjecturas 1 geral-K e 2; risco alto); (d)
`PLATEAU-RESUMMATION-ATTEMPT` (identificar a constante do platô
`0,0377616` de DISC-DEC-071; linha M-CLUST, Árvore B; risco
moderado-alto); (e) `GAMMA-SCALING-LAW-ATTEMPT` (provar
`√(2/(2−γ))` em γ∈(0,1) — primeiro ataque dedicado a este aberto).
Seeds 20260860000–20260869999 reservados, grep-confirmados livres.
Anterior: `DISC-DEC-071`: integração da
onda 16 frente (d) — `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND WITH NAMED ISSUES**, "ACCEPT for catalogue" com correções
obrigatórias N1/N2 + N3 menor). **FECHAMENTO PARCIAL FORTALECIDO do
sistema acoplado `(Φ,Ψ)` do piso H2 em `b=1`** — o caso mais claro da
linhagem de correção adversarial em *underselling*: todas as alegações
positivas da frente replicaram do zero (MC 1M, solver PDE independente
de outra família de discretização, série exata a ordem 500), e as duas
alegações NEGATIVAS centrais foram REFUTADAS na direção que fortalece o
registro — N1: todo coeficiente da série small-`t0` está na família
fechada `{P(s)+Q(s)·erfcx(s√(c/2))}` (indução construtiva do referee,
sem camada de quadratura; `b₂`, `b₃`, `a₃(0)`, `a₄(0)` exatos); N2: o
"raio de convergência `c·t0~0,5–0,7`" era erro de truncamento a 3
termos — a série com coeficientes exatos converge no platô inteiro e dá
a caracterização mais nítida da linhagem: `Φ(0,t0)=0,0377616` para todo
`t0≥0,02`. Sessão verificou os resultados novos do referee antes de
catalogar (regra verificar-antes-de-catalogar: sympy resíduos
exatamente 0; implementação independente da família `(P,Q)` até ordem
200, todos os valores reproduzidos). Restam: ressomação fechada
(constante do platô não identificada) e o gap abstrato-vs-real ~30%.
`φ_REDB` INALTERADA; nó `FLOORH2` na Árvore B do mapa de dependências —
linha M-CLUST(b), não um Estágio de THEOREM.md. 6 adendos datados.
**ONDA 16 FECHADA — 5/5 frentes integradas** (DISC-DEC-066 a 071).
Anterior: `DISC-DEC-070`: integração da
onda 16 frente (c) — `GENERAL-P-DSTAR-EXTENSION-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND**, "ACCEPT for catalogue"). `D^{*(p)}_r(b)` montado e
verificado para `p=11,…,20`, todo `b≥0`, via a máquina `H_k` já
provada correta para todo `k` (onda 15); verificação uniforme do
referee em `r≤200`, `b≤30` — 75.899 checagens, zero discrepâncias
(self-check determinístico da frente 36/36). **Bônus analítico do
referee:** o limite de grau `deg_r H_{2k−1}=k−1`, antes apenas
observado, foi PROVADO (coeficiente líder `4^{k−1}(k−1)!`). `p>20`
permanece aberto apenas por não executado — nenhuma barreira
conceitual. 1 adendo datado. Integrado como "Estágio 21" em
`THEOREM.md`, com pointers datados nos Estágios 16–17. Anterior:
`DISC-DEC-069`: integração da onda 16 frente (a) —
`CONJECTURE-1-K4-ATTEMPT` CONCLUÍDA e INTEGRADA, após verificação
adversarial hostil dedicada (veredito **SOUND**, "ACCEPT for
catalogue", dois achados cosméticos, nenhum substantivo).
**FECHAMENTO COMPLETO E INESPERADO — segunda surpresa consecutiva:
`f_{M_4}(x)=8x(1−x²)³` PROVADO em K=4**, módulo a mesma citação
clássica das etapas anteriores. Mecanismo: os Bell(4)=15 padrões de
coincidência colapsam em 5 formas via o produto `∏(b_j−1)!`, cuja
soma ponderada dá `K!=24` pela bijeção partição↔permutação; a
expansão de 625 termos reduz-se a 12 tipos de forma (`Σp(s)`);
`W_C(Q)=1−Q` verificado até `n_off=4` via a identidade de florestas
ponderadas `E(E+Q)^{n−1}=E` — nomeada como rota candidata para
`K≥5`, explicitamente não tentado. A Conjectura 1 fica provada em
`K=1,2,3,4`. Spot-check independente da sessão (enumeração exata em
`Fraction`) antes do despacho do referee, zero discrepâncias; 2
adendos datados. Integrado como "Estágio 20" em `THEOREM.md`.
Anterior: `DISC-DEC-068`: integração da
onda 16 frente (b) — `SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT`
CONCLUÍDA e INTEGRADA, após verificação adversarial hostil dedicada
(veredito **SOUND WITH NAMED ISSUES**, "ACCEPT for catalogue").
**FECHAMENTO COMPLETO, na terceira tentativa, do gap mais difícil da
linha: `sup_K M_K/√K = a*` EXATAMENTE** — `M_K < a*√K` estritamente
para todo `K≥1`, via Robbins 1955 + FGKP95 Teorema 7 (confirmado pelo
referee **contra o PDF primário do artigo**) + a identidade clássica
`Q(n)=n!e^n/(2n^n)−θ(n)`; o `z_K`-bound do Lema 4.1, sem modificação,
bastou do outro lado. A hipótese (U') fica com a constante nítida
`a*` em **todos** os casos `0≤K≤n` — o caso de contorno `K=n`,
não-tentado pela frente, foi fechado pelo próprio referee (§8) e
re-verificado independentemente pela sessão (0 violações,
racional-certificado, n=1..300). A taxa explícita nítida em `c` NÃO é
afirmada (a re-montagem do Estágio 12 com `a*` permanece não
executada, nomeada como próximo passo). Dois erratas obrigatórios do
referee (E-1: exibição de Robbins sem `(n/e)^n`; E-2: dois
intermediários impressos do Lema 1 falsos — o mesmo defeito que o
spot-check da sessão encontrara independentemente antes do despacho)
+ 3 notas, todos corrigidos via 5 adendos datados. Integrado como
"Estágio 19" em `THEOREM.md`, com pointers datados nos Estágios
12–13. Anterior: `DISC-DEC-067`: integração da
onda 16 frente (e) — `CONJECTURE-2-DIRECT-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND WITH NAMED ISSUES**, quatro achados menores, "ACCEPT for
catalogue" no tier reivindicado). **NÃO-FECHAMENTO HONESTO** da rota
direta da Conjectura 2 — o desfecho pré-declarado aceitável para a
frente de maior risco da onda — com progresso parcial estrutural
provado: a arquitetura do método dos momentos
(correta-se-completada); os alvos novos `E[M(c)²]=(1−e^{−c})/c` e
`E[M_K²]=1/(K+1)` (alvos sobre a lei conjecturada; âncoras
incondicionais em `K≤3` via as densidades já provadas); a redução por
blocos do caso `p=2` (cruzada por enumeração exata, estendida a `n=8`
pelo referee, que a fortaleceu para "toda célula = `(n−2)!`"); o
certificado de bloco intacto; e a **refutação rigorosa** da rota
Poissonization-em-`c` (contraexemplo exato `n=6`: um reroute
adicional AUMENTA a contagem cíclica de 3 para 5; o scan exaustivo do
referee — 9 subidas/7 descidas de uma mesma configuração — fecha
também a versão direção-determinística-em-`M`). A obstrução genuína
(exploração conjunta de 2 pontos) está localizada com precisão e
aberta. Quatro adendos datados aplicados (Issues 1–4 do referee, dois
deles com os reparos fornecidos pelo próprio referee). Integrado como
"Estágio 18" em `THEOREM.md`, com extensão datada no bloco da
Conjectura 2 do §8 — e correção de uma omissão da integração
anterior (o bloco da Conjectura 1 no §8 não mencionava K=3 provado).
Conjectura 2 permanece CONJECTURA; nenhum status muda. Frentes
(a)–(d) da onda 16: pesquisa concluída, referees retornados ou em
andamento, integrações a seguir. Anterior: `DISC-DEC-066`: autorização e
despacho da onda 16 — 5 frentes matemáticas puras independentes, a
pedido explícito do usuário ("bater de frente em todos os caminhos
abertos"), uma para cada item da lista-mestra de abertos do "veredito
honesto atualizado" do Estágio 17: (a) `CONJECTURE-1-K4-ATTEMPT`
(risco incerto, K=4 é pergunta genuinamente nova); (b)
`SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT` (terceira tentativa de
`sup_K M_K/√K=a*`, duas rotas já falharam, risco alto); (c)
`GENERAL-P-DSTAR-EXTENSION-ATTEMPT` (estende `D^{*(p)}_r(b)` para
`p≥11`, risco baixo — barreira puramente de execução, não matemática,
já que a máquina `H_k` foi provada correta para todo `k` na onda 15);
(d) `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT` (piso `H2` em `b=1`, sistema
2-var acoplado não-local, mesma classe de dificuldade que Conjectura 1
geral-`K`, risco alto); (e) `CONJECTURE-2-DIRECT-ATTEMPT` (rota direta
para a lei distribucional incondicional completa, não caso-a-caso via
Conjectura 1, risco mais alto — natureza exploratória). Não-fechamento
honesto declarado explicitamente aceitável em todas as 5. Seeds:
20260850000+ a 20260859000+ (uma faixa de 1000 por frente + referee).
Anterior: `DISC-DEC-065`: integração da
onda 15 frente (b) — `CONJECTURE-1-K3-ATTEMPT` CONCLUÍDA e INTEGRADA,
após verificação adversarial hostil dedicada com brief reforçado
(veredito **SOUND**, "ACCEPT for catalogue"). A frente atacou §8
Conjectura 1 (`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`) em `K=3`, despachada com
a expectativa EXPLÍCITA — compartilhada por duas frentes anteriores
desta linhagem — de que a explosão combinatória do número de
configurações de destino impediria o fechamento; um não-fechamento
honesto era o resultado esperado e plenamente aceitável.
**RESULTADO: fechamento completo e inesperado.**
`f_{M_3}(x)=6x(1-x^2)^2`, PROVADO módulo a mesma citação clássica de
`PD(1)` já usada em `K=1,2`, aplicada recursivamente. Lema 1
generalizado via split em 5 padrões por co-blocos; `64` configurações
brutas de destino colapsam, via "fora-do-ciclo contribui massa
cíclica nova exatamente zero," em apenas `7` formas mutuamente
exclusivas cuja soma simbólica é `6x(1-x^2)^2`. Novos momentos
`E[M_3]=16/35=φ_3`, `E[M_3^2]=1/4`, `E[M_3^3]=16/105`. O referee,
briefado explicitamente para caçar a falha que explicaria a surpresa,
re-derivou tudo do zero — incluindo as sete formas de destino (não
apenas as duas pré-checadas pela sessão orquestradora) — e não
encontrou nenhum erro matemático. `K≥4` permanece explicitamente não
tentado, sem alegação de tratabilidade contínua. Integrado como
"Estágio 17" em `THEOREM.md`, com pointers datados em Estágio 15.
**ONDA 15 FECHADA — 2/2 frentes integradas.** Anterior:
`DISC-DEC-064`: integração da
onda 15 frente (a) — `GENERAL-P-DSTAR-CLOSURE-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND**, "ACCEPT for catalogue"). A frente atacou o item 11 do
scorecard de `general_b_dstar_attempt/ATTEMPT.md` — forma fechada
geral-`p` de `D^{*(p)}_r(b)` para `p≥5` — cuja obstrução nomeada o
referee da onda 14 já havia mostrado ser mecanicamente removível
(Estágio 14), sem executar a montagem completa. **Montagem executada
para `p=1,...,10`** (o dobro do mínimo `p=5,6` do mandato): `Q_p(u)`
via identidades de Newton, momentos centrais via função geradora de
cumulantes, ambos algoritmos gerais em `p`, não ajustados caso a
caso — `26.710` checagens exatas, `0` divergências, reduzindo
caractere-por-caractere a todas as seis fórmulas já provadas em
`b∈{0,1}` e re-derivando de forma independente as cinco instâncias
`b≥2` que o documento-pai só verificara numericamente. Referee
re-verificou com métodos deliberadamente diferentes (interpolação de
Lagrange em vez de identidades de Newton/função geradora de
cumulantes) — `18.653` checagens independentes, `0` divergências,
incluindo extensão de escala para `p=5,6` até `r=200,b=30`. **O
referee foi além do exigido: construiu uma prova indutiva de que a
máquina `H_k(r,b)` é correta para TODO `k`**, não apenas os valores
testados — fechando analiticamente, não apenas numericamente, a
lacuna que o próprio documento nomeou como maior risco. `p>10`
permanece aberto apenas por não ter sido executado, não por incerteza
matemática. Integrado como "Estágio 16" em `THEOREM.md`, com pointer
datado em Estágio 14; correção datada em
`general_b_dstar_attempt/ATTEMPT.md`. Anterior:
`DISC-DEC-063`: autorização da
onda 15 — 2 frentes matemáticas puras independentes, escolhidas a
partir dos itens genuinamente abertos e nomeados com precisão que
emergiram da integração completa da onda 14 (`DISC-DEC-058` a `062`),
por `DISC-DEC-023`. **Frente (a)** `GENERAL-P-DSTAR-CLOSURE-ATTEMPT`:
ataca o item 11 do scorecard de `general_b_dstar_attempt/ATTEMPT.md` —
fechamento geral-`p` das constantes agudas `D^{*(p)}_r(b)` para
`p≥5` — usando a identidade de paridade binomial já provada pelo
referee da onda 14 frente (d) como ingrediente citável; risco baixo,
mandato mecânico e bem diagnosticado. **Frente (b)**
`CONJECTURE-1-K3-ATTEMPT`: ataca `THEOREM.md` §8 Conjectura 1 em
`K=3`, estendendo o método whole-space provado em `K=2` (onda 14
frente c) a três fontes de reroteamento; risco mais alto — duas
frentes anteriores desta linhagem já diagnosticaram explosão
combinatória como razão estrutural provável para o método não
generalizar trivialmente além de `K=2`, mas um não-fechamento honesto
é um resultado aceitável e valioso aqui, exatamente como em toda
tentativa anterior desta sessão. Ambas as frentes despachadas com
`DERIVATION_PREREG.md` obrigatório antes de qualquer script, sementes
reservadas (`20260841000+`/referee `20260842000+`; `20260843000+`/
referee `20260844000+`), e verificação adversarial hostil obrigatória
antes de qualquer integração. Anterior:
`DISC-DEC-062`: integração da
onda 14 frente (b) — `FLOOR-CLOSED-FORM-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND WITH NAMED ISSUES**, "ACCEPT for catalogue") — **FECHANDO A
ONDA 14 (5/5 frentes integradas)**. A frente atacou por que o "piso"
H2 (mistura identificada por `DISC-DEC-056`) existe mesmo em `b=1`
(M-U puro), item deixado formalmente aberto pela frente que descobriu
a mistura H1/H2. **Fechamento parcial honesto**: uma redução exata é
**PROVADA** sem simulação (apenas dois fatos clássicos — comprimento
de ciclo exatamente uniforme; independência entre comprimento de ciclo
e status de seed) mostrando que o desvio `φ_far−φ_U(c)` é um efeito de
**seleção** — ambas são médias diferentes, ponderadas diferentemente,
da mesma função não-constante `φ(ℓ)`, não uma falha na derivação de
`φ_U(c)`. O candidato mais natural para `φ(ℓ)` (substituição pontual
na fórmula-mestra) é refutado decisivamente (`z` de `+397` a `+1176`).
Um mecanismo de "reentrada de lacuna" recursivo é **PROVADO**
exatamente (fato combinatório determinístico sobre estrutura de ciclo
finito-`n`) e validado por simulação direta de sua forma exata — mas
**a forma fechada completa NÃO é derivada**: o sistema exato é um
problema acoplado, não-local, de duas variáveis, da mesma ordem de
dificuldade que a Conjectura 1 geral-`K` ainda aberta (Estágio 15). A
própria frente capturou e **retirou**, dentro do próprio documento,
uma alegação mais fina que não sobreviveu a uma réplica robusta a
cluster — autocorreção honesta, não deixada para o referee capturar.
A sessão orquestradora verificou independentemente, via enumeração
exata (`Fraction`, sem simulação) em `n=5,6`, a identidade de redução
central e os dois Fatos clássicos que a sustentam — todos EXATOS.
Referee re-verificou as três alegações empíricas designadas a `5×+` a
potência estatística da própria frente, sementes frescas — todas
confirmadas; único achado uma imprecisão de redação em §7 ("7 de 9"
células), corrigida. Nenhuma fórmula nova substitui `φ_REDB`. Uma
correção datada em `floor_closed_form_attempt/ATTEMPT.md`;
`PROOF_DEPENDENCY_MAP.md` Árvore B ganhou o nó `FLOORCF` + um adendo
datado. Anterior:
`DISC-DEC-061`: integração da
onda 14 frente (c) — `CONJECTURE-1-K2-ATTEMPT` CONCLUÍDA e INTEGRADA,
após verificação adversarial hostil dedicada (veredito **SOUND WITH
NAMED ISSUES** — um, menor, não-substantivo — "ACCEPT for
catalogue"). A frente atacou `THEOREM.md` §8 Conjectura 1
(`f_{M_K}(x)=2Kx(1-x^2)^{K-1}`), provada apenas em `K=1` desde a
criação do documento (§5.3) — o item 5 da lista de gaps do §9.
**`K=2` agora PROVADO exatamente**: `f_{M_2}(x)=4x(1-x^2)`, módulo uma
citação clássica (propriedade residual/size-biased de `PD(1)`) que é a
**mesma** já usada pela Proposição 2.4 do próprio documento sem
re-derivação — não um novo link mais fraco. Método: generaliza a
computação whole-space de §5.3 a `K=2` via duas massas de região
`(m_1,m_2)` com lei conjunta exatamente uniforme numa triângulo (Lema
1), colapsando as 9 combinações de destino em 4 grupos cuja soma
simbólica de densidades é exatamente `4x(1-x^2)`; subprodutos
`E[M_2]=8/15` (já conhecido) e **novo** `E[M_2^2]=1/3`. A sessão
orquestradora re-derivou do zero toda a cadeia simbólica/algébrica
antes de despachar o referee, que re-derivou o restante do zero: Lema
1 via um modelo gerativo genuinamente diferente (simulação de
permutação discreta, 3 escalas, tendência de convergência limpa
conforme `n→∞`); a tabela de mecanismo de 9 células (260.000 testes
exatos, 100% de acerto, incluindo casos-limite); e reconfirmou a
densidade agregada a `n=20.000` (2× a escala da própria frente). Único
achado: uma rotulagem de citação imprecisa dentro da prova do Lema 1,
sem efeito sobre a validade — corrigida via correção datada. `K≥3`
permanece exatamente tão aberto quanto antes, nenhuma tentativa feita.
Integrado como "Estágio 15" em `THEOREM.md`, com pointers datados em
§8 e §9. Anterior:
`DISC-DEC-060`: integração da
onda 14 frente (e) — `CELL-VARIATION-ATTEMPT` CONCLUÍDA e INTEGRADA,
após verificação adversarial hostil dedicada (veredito **SOUND WITH
NAMED ISSUES**). A frente investigou o que explica a variação
célula-a-célula do H2-share medido pela linhagem
`long_cycle_deficit_attempt`, via uma grade pré-registrada de 13
células — `ρ`, `c`, ou `b`. A regra PRIMÁRIA mecânica dá **PARTIAL/
MIXED**, mas três checagens secundárias convergem: `ρ` é a única
covariável com correlação pooled significativa (`r=−0,623,p=0,031`);
`b` é estatisticamente indistinguível de zero (`r=0,08,p=0,81`).
Referee hostil re-simulou 9 das 13 células do zero (68.000 instâncias
frescas), re-derivou toda a maquinaria estatística sem ler nenhum
script da própria frente: T0 e toda aritmética/fórmula confere
exatamente. Nomeou duas complicações reais: a correlação de `ρ` **não
sobrevive** Bonferroni nem Spearman nos dados originais; a célula
`G1b` (excluída por ambiguidade), resolvida por triangulação
(`N=12.000, z=−7,69`), revela não-monotonicidade real em `ρ` dentro de
`G1`. **Mas** na tabela triangulada do próprio referee a correlação
`ρ` **fortalece e sobrevive** Bonferroni (`r=−0,680,p=0,011`); `b`
continua robustamente descartado. Nenhum erro aritmético encontrado;
enquadramento de honestidade do documento julgado preciso, se algo
conservador demais. Resultado **correlacional**, não uma nova fórmula
fechada — `φ_REDB` permanece a fórmula de registro de M-CLUST(b). Um
adendo datado em `cell_variation_attempt/ATTEMPT.md`;
`PROOF_DEPENDENCY_MAP.md` Árvore B ganhou o nó `CVCOV` + um adendo
datado. Anterior:
`DISC-DEC-059`: integração da
onda 14 frente (d) — `GENERAL-B-DSTAR-ATTEMPT` CONCLUÍDA e INTEGRADA,
após verificação adversarial hostil dedicada (veredito **SOUND**,
"ACCEPT" — 165.888 checagens exatas independentes, 0 divergências,
nenhum erro encontrado em lugar algum). A frente atacou o item
nomeadamente deixado aberto pelo Estágio 9 — a forma fechada geral-`b`
das constantes agudas `D^{*(p)}_r(b)` para `b≥2`, tomando o Corolário
A3 já provado como insumo fixo. **Fechado para `p=1,2,3,4`, todo
`b≥0`**: Teorema D1 (`p=1`) mais três fórmulas irmãs, via a rota de
colapso de prefator no estilo Teorema 3′ estendida a `p` simbólico. O
caso `p=2` re-deriva independentemente o já provado Teorema 3′
(confere exatamente); `p=3,4` são formas novas. Referee hostil
re-derivou a rota inteira do zero (própria tabela de Stirling, própria
soma de Abel, própria extração de momentos) sem ler nenhum script da
própria frente, em escala superior à da frente em todos os quatro
valores de `p` (`24` valores distintos de `b≥2` testados para `p=3,4`,
não apenas o único ponto `b=2` que a sessão orquestradora já havia
sinalizado como fino). O referee foi além do exigido: mostrou que a
obstrução nomeada para `p≥5` (item 11 do scorecard, classificado
`OPEN`) é **mecanicamente removível** — o cancelamento de `I5,I7`
segue de uma linha só de um fato binomial de paridade, válido para
todo expoente par, verificado simbolicamente até `n=40` — mas **não**
executou a montagem completa para `p≥5`, que **permanece
honestamente aberta**. Integrado como "Estágio 14" em `THEOREM.md`;
duas correções datadas em `general_b_dstar_attempt/ATTEMPT.md`;
`PROOF_DEPENDENCY_MAP.md` Árvore A ganhou um adendo datado. Frentes
(b), (c), (e) da onda 14 ainda em andamento ou aguardando referee
hostil. Anterior:
`DISC-DEC-058`: integração da
onda 14 frente (a) — `SHARP-CONSTANT-U-PRIME-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND**, "ACCEPT for catalogue" — verificado independentemente até
`n,K=10^6`, zero violações, nenhum erro encontrado). A frente atacou os
dois ingredientes exatos deixados abertos por Estágio 12 para a
constante **nítida** da hipótese (U'): um limitante inferior para a
função `Q` de Ramanujan, e monotonicidade de `M_K/√K` em `K`
(equivalente a `sup_K=lim_K`). **Peça 1 fechada**: provado
`Q(n)≥√(πn/2)-6` para todo `n≥1`, via a rota elementar já nomeada
(`-ln(1-x)≤x/(1-x)`), com uma comparação termo-a-termo sem truncamento.
Combinado com Teorema 3 e o Lema 4.1 já provados de Estágio 12, isto dá
`lim_{K→∞} M_K/√K = a* = 0,3670872…` **exatamente** — a primeira
confirmação rigorosa de que a constante numericamente conjecturada é
genuinamente o valor assintótico correto, não apenas um limitante
superior sobre ele. **Peça 2 não fechada**: monotonicidade de `M_K/√K`
tentada por duas rotas (uma recursão exata para `Q(n)`, refutada por
contraexemplo explícito `Q(3)=17/9`; um limitante pontual direto, que
exigiria precisão `O(1/√K)` para todo `K` finito, mais delicado que a
ferramenta elementar disponível) — relatada honestamente como não
fechada. **A constante efetivamente provada na hipótese (U')
permanece `a=1+√(π/2)≈2,2533`, NÃO `a*`** — `a*` é agora o limite
exato, mas ainda não o supremo uniforme-em-`K` necessário para a
hipótese (U') propriamente dita. Referee re-derivou cada passo
algébrico do zero (incluindo os dois passos sinalizados como não
verificados à mão pela sessão orquestradora), sem encontrar nenhum
erro, e foi além do exigido: derivou independentemente `Err(n)→3/2`
quando `n→∞` (não presente no documento-alvo). Integrado como "Estágio
13" em `THEOREM.md`; duas correções datadas em
`u_prime_hypothesis_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md`
Árvore A ganhou um adendo datado. Frentes (b), (c), (d), (e) da onda 14
ainda em andamento ou aguardando referee hostil. Anterior:
`DISC-DEC-056`: integração da
onda 13 frente (b) — `LONG-CYCLE-DEFICIT-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND WITH NAMED ISSUES**). Investigou o item 1/§9 aberto por
`short_cycle_dynamics_attempt` (DISC-DEC-053): o platô negativo
persistente (`~−10%` a `−15%`) na população de ciclos longos (`L>b`)
do M-CLUST(b) — H1 (viés específico da estrutura de blocos
correlacionados) vs H2 (artefato genérico de `n` finito, também
presente em M-U puro sem correlação de bloco, `b=1`). **T1** (primário,
decisivo): favorece H2 — o déficit reproduz-se em `b=1` a `77–80%` da
magnitude original em duas das três células (`z=−10,21`, `z=−8,04`); o
referee, com o dobro da amostra (`N=5000`), resolve a terceira célula
ambígua também a favor de H2 (`z=−3,39`, cruzando a barra
pré-registrada — um achado positivo que fortalece, não enfraquece, a
conclusão da frente). **T2** (secundário): MISTO por regra própria —
uma amplificação real e reproduzível dependente de `b` (`~1,8`–`2,6×`
entre execuções independentes) fica abaixo do limiar de `3×`
pré-registrado para H1 "limpo". **T3** (exploratório): refuta o
mecanismo causal específico proposto (déficit crescendo com `L/n`).
**Veredito honesto: MISTURA** — um piso independente de `b` (H2,
dominante) mais uma amplificação secundária real dependente de `b`
(H1, sub-limiar), sem forma fechada proposta. Referee hostil replicou
T0/T1/T2 do zero, com sementes frescas e código de medição
inteiramente próprio (nenhum `.py` novo desta frente foi lido),
confirmando todas as conclusões centrais; encontrou dois problemas
nomeados — uma cifra de referência mal-atribuída na pré-registração
(célula e grandeza erradas, coincidentemente próxima do valor correto,
sem efeito em nenhuma classificação) e um problema de precisão
estatística nos pontos intermediários de T2 (`b=20,50`, sem mudar o
veredito MISTO). Correções datadas aplicadas em `ATTEMPT.md` e
`DERIVATION_PREREG.md`. Resíduo M-CLUST(b) permanece **PARCIALMENTE
FECHADO**, sem mudança de status. `PROOF_DEPENDENCY_MAP.md` Árvore B
ganhou um nó novo (`LCDMECH`, verde) e um adendo datado. Onda 13
completa em ambas as frentes. Anterior: `DISC-DEC-055`: integração da
onda 13 frente (a) — `U-PRIME-HYPOTHESIS-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial hostil dedicada (veredito
**SOUND**, "ACCEPT for catalogue" — nenhum erro matemático, lacuna, uso
indevido de citação ou alegação excessiva encontrado em lugar algum do
documento-alvo). A **hipótese (U')** —
`|φ_n^{(K)}-φ_K| ≤ a√K/n` uniforme em `0≤K≤n` — a **última obstrução
central nomeada** entre Teorema A/C (já provados, incondicionais) e uma
taxa de convergência explícita para a linha `uniform_in_c_attempt`,
está agora **PROVADA**, com constante explícita não-nítida
`a = 1+√(π/2) = 2,253314…`. A prova combina a forma fechada
todas-as-ordens de Estágio 9 (Corolário A1) com uma fórmula-companheira
para `ψ_n^{(K),R}` derivada pela primeira vez do Teorema B de Estágio 9
(avaliado no "domain caveat" já sinalizado pela própria fonte
primária), via o Lema A de redução — provando, para **todo** `K` (não
apenas numericamente até `K=16384`), que o supremo sobre `n` é sempre
atingido em `n=K+1`, onde a quantidade colapsa, via a identidade exata
`φ_n^{(n-1)}=Q(n)/n` já estabelecida em Estágio 10, à forma fechada
`M_K=Q(K+1)-(K+1)φ_K` (função `Q` de Ramanujan). Isto dá imediatamente
uma **taxa explícita, incondicional**, para Teorema A/C:
`|Δ_n(c)|≤[(1+√(π/2))√c+0,2805]/n`. A constante **nítida**
`a*=√π(1/√2-1/2)=0,3670872…` **não** é estabelecida — este resultado
prova limitação com uma testemunha explícita, não nitidez — e
permanece aberta, com o ingrediente exato nomeado com precisão (um
limitante inferior correspondente para `Q(n)`). Referee hostil
re-derivou cada teorema/lema do zero a partir das fontes primárias
citadas (nenhum arquivo `.py` da frente-alvo foi lido em momento
algum), construindo um motor Markov `(a,b,r)` inteiramente independente
para checar cada passo algébrico; checou a desigualdade final montada
com **zero violações** em quatro escalas independentes até `K=10^5` e
`n` interior até `100K` — muito além da própria frente e da sessão
orquestradora (que também fez verificação independente própria antes
de despachar o referee, encontrando e corrigindo um erro de
transcrição próprio, não do documento-alvo, no processo). Integrado
como "Estágio 12" em `THEOREM.md`; quatro correções datadas em
`uniform_in_c_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore A
ganhou um adendo datado; `README.md` atualizado (item da linha D: taxa
explícita agora incondicional, não mais "condicional a uma hipótese não
provada"). Onda 13 frente (b) (`LONG-CYCLE-DEFICIT-ATTEMPT`) ainda
aguarda referee hostil. Anterior: `DISC-DEC-053`: integração da
onda 12 frente (b) — `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial (veredito **SOUND WITH NAMED
ISSUES**). **NÃO-FECHAMENTO HONESTO** do alvo mandatado (fechar o
resíduo extremo que `φ_REDB` deixou aberto), mas com um avanço genuíno
de mecanismo: confirmou, à precisão de máquina e além do exigido, que
todo ciclo-π intocado — qualquer comprimento `L`, não só `L≤b` — é
deterministicamente um ciclo de `f`. O diagnóstico que expôs isso
revelou que **o pequeno resíduo agregado (1–3%) que esta linha
persegue desde a onda 7 é, na verdade, o quase-cancelamento de dois
efeitos bem maiores e opostos**: um excesso positivo grande para
ciclos de comprimento pouco acima de `b` (o referee mediu, com duas
sementes frescas independentes, `+796%` a `+874%` na célula-alvo —
corrigindo os `+267,7%` originalmente relatados, rastreado a um efeito
de seleção por condicionamento em `x₀∈R^c` que o modelo original
subestimava) e um platô negativo persistente (`~−10%` a `−15%`) para
ciclos longos — nenhum dos dois modelado por nenhuma fórmula desta
linhagem. **A candidata `φ_REDC` foi REFUTADA** — piora 5 das 6
células testadas, incluindo a própria célula-alvo, confirmado
independentemente pelo referee (`χ²` degrada `4,45×`–`4,81×`). O
referee re-derivou o mecanismo a escala 2,2× maior (2.653.644 pontos,
zero violações), confirmou a forma qualitativa da estrutura
`L`-dependente de forma ainda mais forte no pico perto de `L=b`, e
confirmou a refutação de `φ_REDC` de forma independente. `φ_REDB`
permanece a fórmula de registro; o resíduo M-CLUST(b) permanece
**PARCIALMENTE FECHADO**, sem mudança de status, mas com o mecanismo
genuinamente mais bem compreendido. Três correções datadas aplicadas
em `short_cycle_dynamics_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md`
Árvore B ganhou dois nós novos (`SCMECH`, verde; `REDC`, rosa). Com
isto, a onda 12 (`DISC-DEC-051`) está completa em ambas as frentes.
Anterior: `DISC-DEC-052`: integração da
onda 12 frente (a) — `MK-QUALITATIVE-GEOMETRICITY-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial (veredito **SOUND**, "ACCEPT
for catalogue"). Fechou a única obstrução nomeada restante para
**Teorema E** (Estágio 10) ser incondicional: provou que
`M_K := sup_{n≥K+1}|n(φ_n^{(K)}-φ_K)| ≤ φ_K(K{+}1)e^{K/2}+K =
O(K(\sqrt e)^K)` — crescimento geométrico qualitativo, exatamente o
que a convergência dominada de Teorema E precisa. Não seguiu a rota
originalmente esboçada pelo referee de Estágio 10 (desenrolar a
Proposição 6 de Estágio 8, que exigiria um limitante geral-`b` para
`A_r(b),B_r(b)` não estabelecido em lugar nenhum do arquivo — essa
rota permanece **OPEN**, não forçada); em vez disso usou a forma
fechada todas-as-ordens do Estágio 9 (Corolário A1) mais o Lema A de
redução, ambos já provados, numa rota de três passos elementares.
Referee hostil re-derivou os cinco passos do zero (nenhum arquivo
`.py` da frente-alvo lido) e testou o passo mais crítico
(monotonicidade) exaustivamente muito além da faixa da própria frente
— 0 violações. **Teorema E PERDE o rótulo PROVED-MODULO e torna-se
PROVADO, incondicional, em ambas as versões** (pontual e uniforme).
**Isto NÃO fecha a hipótese (U') nem "uma taxa explícita para Teorema
A/C"** — obstrução distinta e mais forte (exige limitante *uniforme*
em `K`, não apenas crescimento geométrico), permanece aberta sem
mudança; cuidado explícito foi tomado para não confundir os dois itens
nomeados separadamente desde o Estágio 10. Cinco correções datadas
aplicadas em `uniform_in_c_attempt/ATTEMPT.md`; "Estágio 11" anexado a
`THEOREM.md`. Onda 12 frente (b)
(`MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT`) ainda pendente. Anterior:
`DISC-DEC-050`: integração da
onda 10 frente (a) — `MCLUST-ELEVATION-LEVEL-ATTEMPT` CONCLUÍDA e
INTEGRADA, após verificação adversarial completa em duas etapas (um
relatório inicial quase completo mas com dois placeholders de template
vazios e 2 de 6 células do teste de redução inacabadas; um segundo
agente terminou exatamente o cômputo pré-registrado que faltava).
**VEREDITO CINDIDO.** O mecanismo da elevação de fechamento — não é a
constante `P_lead=1/(1-ρ)` que toda fórmula anterior desta linha
assumia, e sim uma função `λ(t)` da massa percorrida — foi
**identificado e confirmado independentemente** (referee: simulador
próprio, `χ²=1925/67` bins contra elevação constante, hazard=1/pool
confirmado a ≈0,2%, zero falhas de auditoria em `5,91×10⁸` passos).
Mas a redução `M-CLUST(b)|x₀∉R ≡ M-U(c(1-ρ),(1-ρ)n)`, usada para
construir a candidata original `φ_RED`, foi **refutada** a 7,5× a
precisão (`χ²` pooled = 334,6/6 células completas). A correção do
próprio referee (`φ_REDB`, argumento `c''=c(1-c/n)^(b-1)`) melhora
substancialmente (`χ²` 334,6→101,4, 5/6 células a `|z|≤1,5`) — **mas
não fecha o resíduo por completo**: a sexta célula, a mais extrema já
testada nesta linha (`b=100,c=1000,ρ=0,785`), sozinha fornece ~96% do
`χ²` restante (`z≈-10`), um resíduo real e ainda não modelado. `φ_REDB`
é adotada como nova fórmula de registro de M-CLUST(b), substituindo
`φ_EPSR` — mas o resíduo sistemático de M-CLUST(b) **permanece
PARCIALMENTE FECHADO**, não `CLOSED`. Seis correções datadas aplicadas
em `ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` (Árvore B) ganhou dois nós
novos. Anterior: `DISC-DEC-049`: integração da
onda 11 frente (a) — `UNIFORM-IN-C-TEOREMA-3-ATTEMPT` CONCLUÍDA e
INTEGRADA. **O item (iv) da lista de itens abertos desde o Estágio 6 —
versão uniforme-em-`c` do Teorema 3 — está FECHADO**, e de forma mais
forte do que pedido: a convergência `φ(n,c)→φ_∞(c)` é uniforme não só
em compactos `[0,C]` (Teorema A) mas globalmente em todo `[0,∞)`
(Teorema C), ambos **incondicionais**, via dois lemas elementares
novos (acoplamento equi-Lipschitz constante 1; limitante de cauda
uniforme-em-`n`) que dispensam inteiramente a maquinaria
`F_r/G_r/H_r`. Perfil de erro exato `e(c)` derivado, incondicional
coeficiente-a-coeficiente (Teorema D). Referee hostil auditou os dois
insumos novos e os dois teoremas incondicionais com peso máximo —
zero erros encontrados. Achado substantivo: o documento nomeava a
lacuna errada para a condicionalidade de Teorema E (versão uniforme do
perfil de erro) — corrigido (a Proposição 6 do Estágio 8 prova o
limitante, não a geometricidade qualitativa dos `M_K`, que é a lacuna
real). Referee também registrou um fortalecimento não solicitado: a
identidade que explica `a^*` é exata, não aproximada. Sessão
orquestradora verificou independentemente antes de despachar o
referee. "Estágio 10" anexado a `THEOREM.md`. Com isso, dos cinco itens
abertos originais desde o Estágio 6, restam apenas a forma fechada das
constantes agudas em `b≥2` e as Conjecturas 1–2. Anterior: `DISC-DEC-048`: integração da
onda 11 frente (b) — `ALL-ORDERS-CLOSED-FORM-ATTEMPT` CONCLUÍDA e
INTEGRADA, com correção adversarial. **O item (i) da lista de itens
abertos desde o Estágio 6 — forma fechada exata, todas-as-ordens,
geral-`K`, para a recursão discreta — está FECHADO.** Estendendo o
`ε`-matching a um índice de ordem simbólico `p`, os multiplicadores
lidos em `p=0,\dots,8` revelam-se exatamente os números de Stirling de
primeira espécie sem sinal, `c(k+p+1,k+1)` — do que segue, por
identidade clássica de fatorial ascendente, a re-soma exata e finita
da série inteira inteira (Teorema A/B: forma fechada geral-`K`,
geral-`b`, geral-`m`, `n` finito), com prova elementar independente
que não usa a maquinaria `ε`. Os Teoremas 1–4 dos Estágios 6–8 tornam-se
corolários diretos — nenhum enfraquecido. Referee hostil re-derivou o
núcleo inteiro do zero contra um simulador próprio das regras
originais (`215.070` checagens exatas, zero divergências), mas
encontrou um erro real negativo: a alegação de que a forma geral-`b`
falha para `b≥1` estava errada — falha apenas para `b≥2`; em `b=1` a
mesma base é exata (e o caso `p=2` já era **provado** pelo Teorema 3′
da onda 10, especializado em `b=1`) — corrigido, com quatro novas
formas fechadas em `b=1`. Referee também promoveu duas alegações
conservadoras a PROVADAS. Sessão orquestradora verificou
independentemente antes de despachar o referee. "Estágio 9" anexado a
`THEOREM.md`. Anterior: `DISC-DEC-047`: autorização da
onda 11, em paralelo ao referee ainda pendente da onda 10 frente (a) —
2 frentes matemáticas puras na linha U₁/₂, ambas reaberturas
nomeadas como legítimas por decisões anteriores: (a)
`UNIFORM-IN-C-TEOREMA-3-ATTEMPT`, tentando estabelecer se a
convergência do Teorema 3 é uniforme em `c` sobre compactos; (b)
`ALL-ORDERS-CLOSED-FORM-ATTEMPT`, buscando um quarto ponto de dados na
sequência de multiplicadores da escada `F_r/G_r/H_r` para testar se há
um padrão fechado geral-ordem. Ambas em andamento. Anterior:
`DISC-DEC-046`: integração da onda
10 frente (b) — `K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT` CONCLUÍDA e
INTEGRADA, com correção pós-adversarial. Estendendo o `ε`-matching que
produziu `F_r`/`G_r` mais uma ordem, forma fechada exata de `H_r(t,b)`
obtida (Teorema 1); em `b=0`, `D*_r(0)=r(3r+1)/32·φ_r−r/12` exatamente
(Teorema 3). Limitante já publicado é FATORIAL; folga decomposta em
dois mecanismos, um corrigido rigorosamente (Proposição 6, geométrico).
Referee hostil dedicado reconfirmou o núcleo inteiro **sem ressalva**
(milhares de checagens exatas, zero divergências) mas encontrou DOIS
ERROS REAIS nos termos subordinados do Teorema 4 publicado — sinal e
magnitude do termo `r^{1/2}` em `b=0` (`+√π/128` publicado, correto
`−√π/512`) e o termo linear tratado como `b`-independente quando é
`−(3b+2)r/24` — ambos corrigidos, com forma fechada geral-`b` derivada
pelo próprio referee (Teorema 3′) provando a `b`-independência da
constante líder `3√π/64` INCONDICIONALMENTE. Sessão orquestradora
verificou as duas correções por conta própria antes de aceitar.
Correções datadas aplicadas em `ATTEMPT.md`; "Estágio 8" anexado a
`THEOREM.md`, fechando o item (ii) da lista de itens abertos do
Estágio 6/7. `DISC-DEC-045` (onda 10, autorização) permanece com a
frente (a) — `MCLUST-ELEVATION-LEVEL-ATTEMPT` — em andamento: resultado
POSITIVO recebido (candidato `φ_RED`, redução `M-CLUST(b)|x₀∉R ≡ M-U`
reescalado, `χ²` agrupado `1149,8→183,3` em 132 células), referee
hostil dedicado despachado, AINDA PENDENTE; `φ_EPSR` permanece a
fórmula de registro até integração. Anterior: `DISC-DEC-044`: referee hostil
dedicado a `φ_EPS` (achado secundário de `DISC-DEC-043`) CONCLUÍDO —
**VEREDITO CINDIDO**. `eps=P(cíclico|x₀∈R)≠0`: SOUND, confirmado ainda
mais fortemente (18 células, método que não simula nenhum passeio —
grafo funcional completo + conjunto cíclico exato, `190–260σ` por
célula). Significância corrigida para `≈8–14σ` (não `12,5–21,7σ` — as
barras do alvo estavam sub-dispersas `~1,8×`). Mecanismo correto:
subpopulação *run-start* de `R` (fração `~1/b`), não o interior
sombreado. `φ_EPS` melhora `φ_CAND`: SOUND WITH NAMED ISSUES — a
melhoria de `χ²` é real e reprodutiva, mas a derivação original tinha
dois erros sistemáticos que se cancelavam parcialmente (canal
run-start alto demais, canal sorteio-f baixo demais, ambos
demonstrados livres-de-modelo a até `−48,7σ`). Formula corrigida
`φ_EPSR` (ingredientes medidos, não ajustados, a `32` células) é
numericamente `≥ φ_EPS` em todas as 6 grades testadas. Teste decisivo:
substituir `eps` modelado pelo exatamente medido move `χ²` de `335,6`
para `183,2` — **o canal `eps` está EXAURIDO**, nenhuma frente futura
deve investir nele. **`φ_EPSR` é adotada como a NOVA FÓRMULA DE
REGISTRO de M-CLUST(b), substituindo `φ_CAND`** (primeira mudança de
fórmula de registro desde `DISC-DEC-034`) — não fecha o resíduo
(`χ²≈183` contra `~18` esperado por ruído), mas o resíduo remanescente
está agora localizado por duas vias independentes inteiramente em
`φ(cíclico|x₀∉R)` (o nível de elevação), o alvo mais preciso que esta
linha já teve. M-CLUST(b) em `U_{1/2}` permanece completamente
intocado. Anterior: `DISC-DEC-043`: onda 9 frente (a) —
tentativa de fechar a hipótese de assimetria x₀-vs-outros-arc-starts
(`DISC-DEC-039`) CONCLUÍDA por **REFUTAÇÃO HONESTA**, com o resíduo
relocalizado com precisão inédita. Hipótese formalizada como modelo de
duas elevações, assimetria necessária calculada ANTES de medir (+2,5%
a +4,0% em `ρ≥0,37`), medida por Horvitz–Thompson separado por
identidade do alvo (1,46M passeios + 0,76M de replicação
independente). Nenhuma célula mostra a assimetria positiva necessária
— razão agrupada `0,983±0,007`, sinal OPOSTO; a única célula com
`−3,7σ` **não replicou** com semente independente (disciplina de
replicação obrigatória em ação). Decisivo: uma vez medido o nível
comum da elevação, `φ` exige simetria a `±1,6%`. Três achados
secundários ESTABELECIDOS: (i) `eps=P(cíclico|x₀∈R)` NÃO é zero
(contradiz `φ_CAND`/`CAND5`/`GLOBAL`), `0,36%–2,19%` de `φ`,
`12,5–21,7σ`; (ii) com a elevação comum E `eps` MEDIDOS (não
ajustados), a fórmula-mestre reproduz `φ_mc` nas 6 células de
estresse com `χ²=4,28/6` — a estrutura está correta, o resíduo inteiro
vive no VALOR de uma constante que excede `1/(1−ρ)` por `+0,9%` a
`+5,6%`, sem forma fechada encontrada (deliberadamente não ajustada);
(iii) um controle dedicado em M-U (`b=1`) mostra que o erro finito-`n`
da própria fórmula-mestre é `O(1/n)`, `≈0,02%` em `n=65536` — duas
ordens abaixo do resíduo, refutando que o resíduo seja artefato da
fórmula-mestre. Um quarto achado é POSITIVO e explicitamente **não
integrado**: `φ_EPS`, uma fórmula candidata sem parâmetro livre, reduz
`χ²` de `121,7` para `72,0` numa validação fresca de 18 células, mas
não fecha o resíduo e exige verificação adversarial obrigatória antes
de qualquer catalogação — a própria frente se recusa a declará-la
integrada; um referee dedicado foi despachado separadamente. `φ_CAND`
permanece a fórmula de registro. M-CLUST(b) em `U_{1/2}` permanece
intocado. Anterior: `DISC-DEC-042`: onda 9 frente (b) —
tentativa de fechar o item (iii) aberto de `THEOREM.md` Estágio 6
CONCLUÍDA por **FECHAMENTO COMPLETO**: PROVADO que o coeficiente exato
de `1/n` de `φ_n^{(K)}-φ_K`, `c_K:=K[φ_K/4+F_{K-1}(1,1)-φ_K]`, é
estritamente positivo para TODO `K≥2` (não apenas a faixa `2≤K≤12` já
verificada). Descoberta central: `c_K` colapsa via um novo Lema 1
(`F_{K-1}(1,1)=[(2K+1)φ_K-1]/(2K)`, fato autônomo) para
`c_K=[(K+2)φ_K-2]/4` — a positividade é exatamente `(K+2)φ_K>2`, com
IGUALDADE EXATA em `K=1` (explicando estruturalmente por que `c_1=0`).
Fechado por um único argumento de razão monótona ancorado em `v_1=2`,
telescopando para uma soma de termos manifestamente positivos. Referee
hostil dedicado rederivou tudo do zero antes de ler o documento-alvo —
indução literal em código `K=1..1500`, todas as 85 células da tabela
recomputadas (0 erradas), varredura exaustiva `K=0,...,3000`
confirmando que o conjunto-solução da igualdade exata é `{0,1}`, e
TRÊS predições próprias (`K=10,11,12`) confirmadas antes de serem
computadas. **Veredito: SOUND** — zero discrepâncias, zero
contraexemplos, o primeiro documento desta linha sem nenhuma correção
exigida. **Consequência:** `φ_n^{(K)}-φ_K=Θ(1/n)` exatamente para todo
`K` fixo `≥2` (não apenas `O(1/n)`), com `Θ(1/n²)` em `K=1` — a taxa de
`φ_n^{(K)}→φ_K` está agora completamente determinada em ordem líder
para todo `K≥1`. Integrado como "Estágio 7" em `THEOREM.md`. `Teorema
3` (Estágio 6) permanece inteiramente inafetado — nunca dependeu desta
frente. `README.md` e traduções não alterados — nenhum deles alegava
algo sobre esta questão específica. Onda 9 frente (a) (`MCLUST-X0-
ASYMMETRY-ATTEMPT`) permanece em andamento. Anterior: `DISC-DEC-041`
(autorização da onda 9: `MCLUST-X0-ASYMMETRY-ATTEMPT` +
`RATE-COEFFICIENT-POSITIVITY-ATTEMPT`, 2 frentes matemáticas puras
independentes, 2026-08-22). Anterior: `DISC-DEC-040`: onda 8 frente (b) —
tentativa de fechar a ressalva de regularidade de `k6_attempt/ATTEMPT.md`
§4 CONCLUÍDA por **FECHAMENTO COMPLETO**. A existência da expansão
assintótica de dois termos foi provada, para TODO `r≥0` (não só os 11
valores `K=0,...,10` já verificados), por indução em `r` cujo passo
indutivo é um limitante de Gronwall discreto EXATO (Taylor livre de
resto, não uma estimativa assintótica) sobre a recursão discreta já
provada — o caso-base é automaticamente subsumido porque o coeficiente
de contração da recursão do resíduo é exatamente zero ali, um fato
algébrico real sobre a recursão já provada, não uma suposição nova.
Referee hostil dedicado (modelo de maior capacidade de raciocínio)
rederivou os seis passos centrais do zero — simulador próprio, formas
fechadas próprias — antes de ler o documento: milhares de verificações
exatas (`Fraction`/`sympy`), incluindo duas predições próprias do
referee (`R_1≡0`, `R_2(m,0,n)=1/(15n²)` para todo `m`) confirmadas
exatamente. **Veredito: SOUND — WITH NAMED ISSUES**, 4 questões
nomeadas, nenhuma fatal, 2 corrigidas via adendo datado (uma delas
crítica: o documento pai carregava a mesma ressalva sobre uma afirmação
`Θ(1/n)` que é FALSA em `K=1` — corrigida com a fórmula mais forte que
o Teorema agora licencia, um coeficiente exato de `1/n`, zero em `K=1`,
reproduzindo `1/30`, `1/14`, `1093/6006` já conhecidos de ondas
anteriores por vias independentes). **Consequência principal:** o Lema
Aberto geral-`K` de `THEOREM.md` §7.4 está agora PROVADO
INCONDICIONALMENTE PARA TODO `K≥0`; a conjectura de taxa geral-`K` é
incondicional para todo `K≥0`; e a Proposição Condicional 5 (§7.5) foi
promovida a **Teorema 3**: para todo `c≥0` fixo,
`φ(n,c)→∫₀¹e^{-ct²}dt` quando `n→∞`, incondicionalmente, sem nenhuma
hipótese não provada — a linha de pesquisa principal do Lema Aberto de
U₁/₂ está fechada por completo. Integrado como "Estágio 6" em
`THEOREM.md`; `PROOF_DEPENDENCY_MAP.md` Árvore A atualizada (todos os
nós agora verdes/incondicionais). Permanece aberto, sem mudança: forma
fechada exata todas-as-ordens geral-`K`; taxa de crescimento em `r` das
constantes de erro; positividade do coeficiente de taxa para `K≥13`;
versão uniforme-em-`c` do Teorema 3; Conjecturas 1–2 (lei distribucional
completa). Anterior: `DISC-DEC-039`: tentativa de fechar a hipótese de exclusão global de escala `tn` [nomeada em `aggregation_closure_attempt/ATTEMPT.md` §7.2] concluída — NÃO-FECHAMENTO HONESTO. Releitura formal de `DERIVATIONS.md` §0–1 mostra que essa exclusão já está presente desde a onda 2 no fator `(1-t)` herdado — não é correção nova. A única interação genuína remanescente (janela local ordem `b` vs. história global) é uma correção de tamanho de pool de ordem `(b-1)/n`, formalizada (elevação `P` é propriedade pura de condicionamento-em-marcas, independente de profundidade de arco) e testada como `φ_GLOBAL`: apenas ±0,1–0,4% de efeito nas 4 células de estresse, ordens de magnitude menor que o resíduo de 2–4%. Medição DIRETA walk-level (simulador próprio do zero, `K(t)` e profundidade de arco explícitos, estimador Horvitz–Thompson, escala de produção `n=65536`, cruzado contra `φ_mc` já confirmado a <2,1σ) não revela lei de profundidade universal. Teste decisivo: 2 das 4 células de estresse (maior `ρ=0,60`, maior `b`) permanecem com lacuna de 10,6–11,4% que nenhuma reponderação por profundidade pode fechar — ativamente descartada, não apenas "não fechada". Validação de 18 células: `χ²(φ_CAND)=79,95 < χ²(φ_GLOBAL)=87,65 < χ²(φ_CAND5)=98,16` — `φ_CAND` continua a fórmula de registro. Suspeita realocada para `q_CLUST` em `ρ` alto, assimetria `x₀`-vs-outros-arc-starts, e a aproximação de Poissonização da fórmula-mestre. Frente irmã da onda 8 (`K-GENERAL-EXISTENCE-ATTEMPT`) permanece sob referee adversarial hostil dedicado, independente deste desfecho. Anterior: `DISC-DEC-037`: tentativa de fechar o passo de agregação nomeado em `residual_attempt/ATTEMPT.md` §5 concluída — PROGRESSO PARCIAL, honestamente caracterizado como tal. A obstrução específica ("como agregar a probabilidade condicional por-alvo sobre o conjunto aleatório de alvos vivos") foi FECHADA — derivada do zero por exposição sequencial de permutação uniforme (técnica diferente da janela deslizante do predecessor), validada por simulação isolada independente (sementes novas, escala de produção `n=65536`): `χ²=1,93` para 4 células (nível de ruído). Também resolveu analiticamente o paradoxo "a soma ingênua dá 1" do predecessor. MAS substituir essa fórmula validada na integral da fórmula-mestre NÃO melhora o ajuste — piora ligeiramente, confirmado em duas validações independentes com sementes frescas (`χ²` 18 células: 81,5→98,2 reuso; 73,6→89,9 fresco). `φ_CAND` (já integrado via `DISC-DEC-034`) continua sendo a melhor fórmula disponível — este documento não a supera, mas caracteriza precisamente onde a dificuldade remanescente mora (hipótese nomeada, não testada: exclusão de imagens já consumidas em escala global `tn`, não só a janela local de `x`). Anterior: `DISC-DEC-036`: casos `K=6,...,10` do Lema Aberto de U₁/₂ agora PROVADOS incondicionalmente (mesma técnica de matriz de transferência da onda 6), estendendo a taxa `Kφ_K/4` confirmada incondicionalmente para `K=0,...,10` (11 valores consecutivos). Além disso, PROVADA a conjectura de taxa geral-`K` (`lim n(ψ_n^{(K)}-φ_K)=Kφ_K/4` para todo `K`), mas EXPLICITAMENTE CONDICIONAL a uma ressalva de regularidade precisamente nomeada (existência da expansão assintótica assumida, para `r` além dos 11 valores verificados) — via argumento de limite de escala contínuo (EDO em `t=m/n`). Referee adversarial hostil rederivou tudo do zero (K=6,7 por substituição na recursão exata + força bruta própria bit a bit; ambas EDOs e formas fechadas `F_r`/`G_r` à mão) — zero erros — e emitiu julgamento explícito, adotado integralmente: **a ressalva está corretamente dimensionada**, nem otimista nem conservadora demais, reforçado por 45 pontos de teste empírico novos (`t≠1`) com zero discrepâncias. Achados e corrigidos via adendos datados (texto original preservado): 2 erros aritméticos cosméticos e 1 erro real-mas-contido (coeficiente de `1/n` de `φ_n^{(6)}`, `1093/6006` não `512/1001`) — nenhum afeta alegação PROVADA. Integrado como "Estágio 5" em `THEOREM.md`. Para `K≥11`: pela primeira vez existe rota de prova completa e verificada, mas o Lema Aberto para `K` geral permanece condicional, não fechado incondicionalmente. Anterior: `DISC-DEC-034`: residuo sistemático de `M-CLUST(b)` (correção finito-`n`, gap nomeado na onda 6) PARCIALMENTE FECHADO — fonte localizada por medição direta (simulador de caminhada próprio, do zero): não está em `q_CLUST(s)=s/(1-ρ)` (fórmula central da onda 4, reconfirmada correta), e sim no termo de risco de fechamento/lotação `(1-t)/(1-s)` herdado sem modificação do mecanismo M-U, combinado com efeito de amostragem não contado (`x₀` uniforme tem probabilidade `ρ` de começar dentro da região sombreada `R`). Fórmula candidata `φ_CAND=(1-ρ)·φ_V4` reduz `χ²` agregado em ~19,5× (532→39 na grade original; 1593→82 incluindo 3 células de estresse novas), com seeds nunca reusadas — mas NÃO é fechamento completo: resta resíduo real pequeno (~3-4σ nos extremos), um passo analítico não fechado (agregação do hazard elevado sobre alvos vivos, nomeado precisamente pelo próprio autor), e uma assimetria não explicada. Classificado honestamente como "PARCIALMENTE FECHADO", não fechamento total. Segunda frente da onda 7 (`DISC-DEC-033`) — tentativa `K≥6`/conjectura de taxa geral-`K` — ainda em revisão adversarial, não integrada. Anterior: `DISC-DEC-032`: `SPARC-FMULTI-STAGE2` fechado `CLOSED_INCONCLUSIVE`. Análise primária real produziu `BOTH_FALSIFIED` mecânico (`a0_fit=6,125×10⁻¹¹` m/s², IC95% `[4,1196×10⁻¹¹;8,5808×10⁻¹¹]`, ambos `a₀^A`/`a₀^B` fora do IC), confirmado bit a bit por reprodução adversarial independente. Debunker obrigatório encontrou confundidor real e estatisticamente robusto: dividir a amostra por RUWE mostra que o subgrupo RUWE-alto (19% da amostra) permanece com excesso de `+0,171` dex (IC95% `[0,126;0,212]`, inteiramente acima de zero) mesmo no bin-âncora após a correção — o modelo de `f_multi` escalar único está mal especificado para a heterogeneidade real. Veredito `BOTH_FALSIFIED` não aceito. `DISC-CLAIM-008`. Holdout selado (12.944 sistemas) nunca tocado. Anterior: `DISC-DEC-031`: casos `K=3,4,5` do Lema Aberto de U₁/₂ agora PROVADOS incondicionalmente — técnica genuinamente diferente da onda 5 (matriz de transferência/cadeia de Markov uniforme em `K`, em vez de análise de casos manual): `ψ_n^{(3)}=16/35+12/(35n)+5/(28n²)+3/(70n³)`, taxa completa `φ_n^{(3)}=16/35+1/(14n)+11/(10n²)+23/(35n³)+6/(35n⁴)`, ambas provadas do zero; `K=4,5` provados como bônus pelo mesmo procedimento mecânico. Verificado por referee adversarial hostil separado (re-derivação completa por técnica diferente, força bruta própria, reexecução dos scripts originais) — veredito SOUND, zero erros. Padrão de taxa geral-`K` catalogado honestamente como CONJECTURA (verificado `K=1..5`, não provado). `K≥6` permanece aberto, obstrução precisa nomeada. Anterior: `DISC-DEC-030`: primeiro resultado real de `DISC-COGNITIVE-EEG-SPECTRAL-001` — braço depressão fechado `CLOSED_REFUTED`. `H_Tamesis` (entropia espectral MENOR em MDD) refutada na direção OPOSTA (`Ī(X)_MDD=0,7613>Ī(X)_HC=0,6558`, `t=5,268`, `p=3,97×10⁻⁶`, `d=1,447`), confirmado por reprodução adversarial independente do zero (todos os números de decisão batem a <10⁻⁹, mesmas 2 exclusões, mesmos 6 arquivos indisponíveis, mesmos 2 pares duplicados descobertos independentemente) — `DISC-CLAIM-007`. Braço ansiedade permanece bloqueado por acesso. Anterior: `DISC-DEC-026`: onda paralela de `DISC-DEC-023` integrada — (a) `SPARC-FMULTI-STAGE1`: pipeline de auto-calibração completa de `f_multi` de Chae (2023) implementado e validado 100% sobre dado sintético [7/7 critérios pré-declarados, 5 cenários], verificado adversarialmente por 2 agentes independentes [1 problema de disciplina documental + 1 lacuna de robustez em `fit_a0` encontrados e corrigidos, nenhum número já reportado alterado] — pronto para Estágio 2 [dado real de descoberta, ainda NÃO o holdout selado], que exige pré-registro e autorização próprios; (b) `DISC-COGNITIVE-EEG-SPECTRAL-001`: etapa de operacionalização concluída [`I(X)`=entropia espectral de Shannon normalizada, modelos concorrentes nomeados, regra de decisão a priori, poder estatístico calculado, acesso real VERIFICADO por download para Mumtaz/depressão, NÃO verificado para DASPS/ansiedade por bloqueio de login IEEE] — braço depressão pronto para um futuro `PREREGISTRATION.md`, 2 lacunas nomeadas pendentes de decisão. Anterior: `DISC-DEC-024`/`DISC-DEC-025`: onda 5 integrada — caso `K=2` do Lema Aberto de U₁/₂ agora PROVADO incondicionalmente [`φ_n^{(2)}=8/15+1/(30n)+7/(10n²)+1/(5n³)`, verificado por referee adversarial em 4 camadas, 0 erros, Lema Aberto restante estritamente `K≥3`]; mecanismo `M-WEIB(β)` de expoente intermediário `α∈(1/2,1)` encontrado e confirmado, com correção de enquadramento via adendo datado [membro da família `M-q` para `β<1`, não escape dela]; pacote `tamesis-cycle-survival/` atualizado e recompilado com o novo resultado. Levantamento arquivo-inteiro de candidatos (Fase 0, 19 candidatos/7 áreas, não restrito a TRI-RG) fechado `CLOSED_NULL` [18/19 rejeitados com razão concreta]; único lead imaturo [EEG cognitivo, depressão vs. ansiedade] promovido a nova linha candidata `DISC-COGNITIVE-EEG-SPECTRAL-001`, `CANDIDATE_FORMULATING`, autorizada apenas etapa de operacionalização. Anterior: `DISC-DEC-021` — `DISC-RH-NUMBER-VARIANCE-001` [item 12] fechado `CLOSED_INCONCLUSIVE`/`NEITHER_MODEL` — reprodução adversarial encontrou um TERCEIRO bug real no estimador primário [corrigido via adendo datado, texto original preservado], mudando o subcaso de `PARTIAL_DISAGREEMENT` para `NEITHER_MODEL`; componente de exclusão de GUE CONFIRMADO como achado real, mais forte do que reportado originalmente [z_A de -203 e -161, não -203 e -4]. Todos os 12 itens do levantamento original de `DISC-RH-REAL-001` agora têm disposição final)
**Arquitetura:** motor 1 de 3 — ver `00_GOVERNANCE/RESEARCH_PIPELINE.md`
(`05_DISCOVERY_LAB` → `03_REPLICATION_GATE` → `04_FORMAL_RESEARCH_LAB`,
adotada em `DISC-DEC-003`). `04_FORMAL_RESEARCH_LAB` não é mais um
laboratório paralelo desacoplado — é o destino de formalização para claims
que sobrevivem ao Gate de Replicação (ver `DEC-107` de lá, que reclassifica
as Ondas 1-7 como arquivo de calibração de capacidade formal, não pesquisa
sobre nenhum Problema do Millennium).

## Status atual

| Campo | Valor |
|---|---|
| Teste ativo | Nenhum. `DISC-COSMOLOGY-MOND-SPARC-004` encerrado (`CLOSED_INCONCLUSIVE`, 2026-08-18, ver seção própria abaixo — redesenho de SPARC-003 com desprojeção Monte Carlo completa; confundidor de multiplicidade oculta plausivelmente suficiente para explicar todo o sinal residual). `DISC-COSMOLOGY-MOND-SPARC-003` encerrado (`CLOSED_INCONCLUSIVE` — estatística pré-registrada estruturalmente incapaz de produzir veredito válido, não erro nem falta de dado). `DISC-RH-ZERO-GAP-RUNS-001` encerrado (`REPLICATION_PASSED`). `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` encerrado (`REPLICATION_FAILED` — inconclusivo por falta de poder no dataset reservado, achado primário NÃO contradito). `DISC-COSMOLOGY-MOND-SPARC-002` encerrado (`REPLICATION_FAILED`). `DISC-COSMOLOGY-MOND-SPARC-001` encerrado (`CLOSED_INCONCLUSIVE`). `DISC-TRI-RG-001` retomada em 2026-08-18 a pedido do usuário, completou os 11/11 candidatos identificados (Fase 0.6 incluída), foi PAUSADA (`DISC-DEC-008`, 2026-08-20), reaberta na prática no mesmo dia por nova busca (Fase 0.7), completou os 3/3 candidatos novos (`complexidade-de-lempel-ziv` NEGATIVO após reexecução adversarial; `largest_lyapunov_exponent` fechado na validação; `dmd_koopman` NEGATIVO — 1 domínio `NOT_COMPUTABLE`, achado do outro refutado por 4 checagens adversariais), foi PAUSADA novamente (`DISC-DEC-009`, 2026-08-20), reaberta na prática no mesmo dia por nova busca (Fase 0.8), completou os 2/2 candidatos novos (`transfer_entropy` NEGATIVO após reprodução adversarial descobrir um artefato instrumental de baixa frequência; `epsilon-machine-complexity` fechado na etapa de validação), foi ENCERRADA FORMALMENTE (`DISC-DEC-010`, 2026-08-21, `status: CLOSED_NULL`) — os 16 candidatos identificados em 5 rodadas de busca têm resultado completo, nenhum produziu invariante cross-domain sobrevivente — foi REABERTA (`DISC-DEC-011`, mesmo dia) com escopo estritamente delimitado (revisitar `epsilon-machine-complexity` com CSSR incremental completo), e ENCERRADA NOVAMENTE (`DISC-DEC-012`, mesmo dia) após a revisão concluir: a implementação corrigida foi verificada como correta (recupera exatamente um processo de ordem finita com solução teórica exata) e AINDA ASSIM não mostrou poder discriminativo para `C_mu` — a ambiguidade original está resolvida a favor de fragilidade genuína do estimador, não limitação de implementação. Dado real (Old Faithful, La Palma 2021) nunca tocado. Ver `02_TESTS/TRI_RG/CLOSURE_SUMMARY.md` (síntese original) e `02_TESTS/TRI_RG/epsilon_machine_complexity/RESULTS_SUMMARY_V2.md` (revisão) |
| Fase | RH-REAL: dois sub-testes concluídos, ambos com Gate de Replicação completo acionado. (1) `DISC-RH-ZERO-GAP-RUNS-001`: `INVERSE_SIGNAL` `REPLICATION_PASSED` — gaps grandes consecutivos são menos comuns que sob reordenação aleatória, confirmado em 3 regimes de altura (~75.000, ~10¹², ~10²¹). (2) `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`: gap mínimo escala como `N^(-1/3)` (GUE), exclui `N^(-1)` (Poisson) e `N^(-1/2)` (GOE) — `β̂=-0,3395` vs. previsão `-0,3333`, `evidence_level: preregistered_confirmed` sobre o dataset primário; Gate no terceiro dataset reservado (`zeros5.txt`, #10²²) resultou `REPLICATION_FAILED` por amostra pequena demais para a grade travada (0 blocos possíveis em N=10.000) — inconclusivo, não contraditório. TRI-RG: os 3 candidatos viáveis da Fase 0 agora testados com rigor completo, os 3 NEGATIVO para invariante cross-domain — `critical-slowing-down` (GISP2/SDDB/NASDAQ), `wavelet-multiresolution-scaling` (Tohoku/CHB-MIT), `dfa-multiscale-entropy` (Apneia-ECG/GISP2, achado forte de 1 domínio explicado por mecanismo fisiológico já conhecido — CVHR — e não replicado no segundo domínio); mais 3 candidatos novos fechados NEGATIVO (`soc-avalanches`, `mse-multiscale-entropy`, `grafo-de-visibilidade` — este último com achado adicional decisivo: `d_B`, o canal originalmente primário, é estruturalmente não computável para séries estocásticas, small-world por construção; `C`, promovido a canal único ANTES de dado real, validado com poder real mas sem sinal em nenhum dos 2 domínios); e o 7º e último candidato, `RQA`, fechado na própria etapa de validação (identificabilidade nunca estabelecida, mesmo após uma correção de desenho pré-autorizada — dado real nunca tocado). Linha `DISC-TRI-RG-001` agora completa, 7/7 candidatos com resultado final. SPARC-003: pré-registro travado como réplica independente do veredito de SPARC-002 via binárias largas Gaia reais (43.147 sistemas pós-corte); modelo MOND pré-registrado tem imagem `(1,+∞)` mas as 5 medianas empíricas reais são todas `<1` — ajuste estruturalmente impossível (diluição por projeção). `CLOSED_INCONCLUSIVE`. SPARC-004: redesenho de SPARC-003 com desprojeção 3D via Monte Carlo (método primário de Chae 2023, estatística `δ_obs-newt`); `a0_fit=1,657×10⁻¹⁰` (IC95% `[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`) após correção de um bug de assimetria de ruído astrométrico encontrado pela descoberta adversarial de nulos; veredito bruto `BOTH_FALSIFIED`, mas a checagem adversarial de multiplicidade oculta (gatilho pré-declarado) mostrou que companheiras não resolvidas, em magnitude plausível pela literatura, são sozinhas suficientes para explicar todo o sinal — `CLOSED_INCONCLUSIVE`, nenhum veredito H_A/H_B aceito |
| Próxima ação obrigatória | Nenhuma obrigatória. `DISC-CORE-NUMERICS-001`, linha U₁/₂: **onda 8 (`DISC-DEC-040`) fechou o Lema Aberto geral-`K` incondicionalmente para todo `K≥0`**, promovendo a Proposição Condicional 5 de `THEOREM.md` §7.5 a **Teorema 3** — `φ(n,c)→∫₀¹e^{-ct²}dt` para todo `c≥0` fixo, sem nenhuma hipótese não provada (substitui integralmente o estado de "onda 5" abaixo, mantido apenas como registro histórico da consolidação anterior). Reaberturas futuras legítimas na linha U₁/₂: forma fechada exata todas-as-ordens geral-`K`; positividade do coeficiente de taxa `φ_n^{(K)}` para `K≥13`; versão localmente-uniforme-em-`c` do Teorema 3; Conjecturas 1–2 (lei distribucional completa, `K≥2`). M-CLUST(b) (objeto separado) permanece `PARCIALMENTE FECHADO` (`DISC-DEC-039`); só depois de uma reabertura legítima considerar testar U_α em sistemas empíricos reais (explicitamente adiado pelo usuário). [Registro histórico, estado ao fim da onda 5:] Teorema 1 provado e verificado por referee adversarial sem erros; ponte `n→∞` provada de forma exata para `K=0,1,2` (fórmula completa `φ_n^{(2)}=8/15+1/(30n)+7/(10n²)+1/(5n³)`); generalização U_α derivada e confirmada (`α∈[1/2,1]` para toda a classe), mecanismo `M-WEIB(β)` de expoente intermediário confirmado; pacote `tamesis-cycle-survival/` (recompilado com o resultado K=2) e `FAILED_HYPOTHESES.md` publicados. `SPARC-FMULTI-STAGE1` concluído e verificado adversarialmente (auto-calibração de `f_multi`, validação sintética apenas, pronto para Estágio 2, holdout selado intocado, Estágio 2 exige pré-registro/autorização próprios). `DISC-COGNITIVE-EEG-SPECTRAL-001` (`CANDIDATE_FORMULATING`) tem etapa de operacionalização concluída — braço depressão (Mumtaz) pronto para um futuro `PREREGISTRATION.md`; braço ansiedade (DASPS) bloqueado por acesso (exige signup IEEE humano); nenhum dado real ainda computado. `DISC-TRI-RG-001` permanece `CLOSED_NULL` (`DISC-DEC-012`). A revisão delimitada de `epsilon-machine-complexity` (CSSR incremental completo) concluiu com veredito mais decisivo que o original — fragilidade genuína do estimador `C_mu` confirmada, não limitação de implementação (verificado via um diagnóstico de ordem finita recuperado exatamente, e via uma prova analítica original sobre a estrutura período-2 do Processo Even). 16/16 candidatos permanecem com resultado final. Uma reabertura futura exigiria nova justificativa explícita; uma revisita legítima a `epsilon-machine-complexity` exigiria uma medida de complexidade fundamentalmente diferente de `C_mu` (nova candidatura), não mais uma correção de implementação. Ver `02_TESTS/TRI_RG/epsilon_machine_complexity/RESULTS_SUMMARY_V2.md` |
| Decisões de governança | `DISC-DEC-001` (criação da trilha), `DISC-DEC-002` (fechamento do piloto), `DISC-DEC-003` (arquitetura de três motores + seis extensões), `DISC-DEC-004` (pivô de SPARC-002 + pré-registro do teste de derivação de a₀), `DISC-DEC-005` (1ª pausa de `DISC-TRI-RG-001`, revertida em 2026-08-14), `DISC-DEC-006` (2ª pausa, revertida em 2026-08-15), `DISC-DEC-007` (3ª pausa, revertida em 2026-08-18), `DISC-DEC-008` (4ª pausa, revertida no mesmo dia por nova busca — Fase 0.7), `DISC-DEC-009` (5ª pausa, revertida no mesmo dia por nova busca — Fase 0.8), `DISC-DEC-010` (ENCERRAMENTO FORMAL de `DISC-TRI-RG-001`, 2026-08-21, `status: CANDIDATE_FORMULATING -> CLOSED_NULL`, após os 16/16 candidatos resultarem sem invariante cross-domain sobrevivente), `DISC-DEC-011` (REABERTURA delimitada, mesmo dia, `status: CLOSED_NULL -> CANDIDATE_FORMULATING`, escopo restrito a revisitar `epsilon-machine-complexity` com CSSR incremental completo), `DISC-DEC-012` (ENCERRAMENTO FORMAL novamente, mesmo dia, `status: CANDIDATE_FORMULATING -> CLOSED_NULL`, após a revisão delimitada confirmar de forma mais decisiva a ausência de invariante), `DISC-DEC-013` (criação de `DISC-CORE-NUMERICS-001`, 4 frentes de adjudicação numérica interna + triagem RH itens 5/6/10, 5 agentes paralelos, 2026-08-21), `DISC-DEC-014` (integração da onda 1 + autorização da onda 2: caracterização da função-limite U₁/₂ + pré-registro FHK item 10; diretriz permanente de README atualizado a cada onda, 2026-08-21), `DISC-DEC-015` (autorização da onda 3: prioridade de literatura, teorema rigoroso, generalização U_α, pacote standalone, 2026-08-22), `DISC-DEC-016` (fechamento de `DISC-RH-FHK-SHORT-INTERVAL-MAX-001`, `CLOSED_INCONCLUSIVE`, confirmado adversarialmente, 2026-08-22), `DISC-DEC-017` (integração completa da onda 3: teorema + referee + generalização U_α + adversarial + pacote standalone, 2026-08-22), `DISC-DEC-018` (autorização da onda 4: itens RH-REAL não-tentados + rigor M-CLUST, 2026-08-22), `DISC-DEC-019` (integração da revisão RH-REAL + autorização do pré-registro do item 12, 2026-08-22), `DISC-DEC-020` (integração da correção de rigor M-CLUST, PARCIALMENTE CORRIGIDO, 2026-08-22), `DISC-DEC-021` (fechamento de `DISC-RH-NUMBER-VARIANCE-001` com correção pós-adversarial de um bug real, `NEITHER_MODEL`, 2026-08-22), `DISC-DEC-022` (autorização da onda 5: tentativa delimitada do Lema Aberto K≥2 + busca de mecanismo de α intermediário, 2 frentes matemáticas puras, 2026-08-22), `DISC-DEC-023` (adoção de paralelismo multi-linha como modo padrão de operação; autorização de 2 frentes paralelas independentes da onda 5 — `SPARC-FMULTI-STAGE1` e `ARCHIVE-WIDE-PHASE0-SURVEY`, 2026-08-22), `DISC-DEC-024` (integração da onda 5: caso K=2 do Lema Aberto PROVADO incondicionalmente com referee adversarial de 4 camadas; mecanismo M-WEIB(β) de α intermediário encontrado e confirmado com correção de enquadramento, 2026-08-22), `DISC-DEC-025` (fechamento de `DISC-ARCHIVE-PHASE0-SURVEY-001` como `CLOSED_NULL`, 18/19 candidatos rejeitados; autorização de `DISC-COGNITIVE-EEG-SPECTRAL-001` como nova linha candidata, etapa de operacionalização apenas, 2026-08-22), `DISC-DEC-026` (integração da onda paralela de `DISC-DEC-023`: `SPARC-FMULTI-STAGE1` concluído e verificado adversarialmente, pronto para Estágio 2; operacionalização de `DISC-COGNITIVE-EEG-SPECTRAL-001` concluída, braço depressão pronto para pré-registro, braço ansiedade bloqueado por acesso, 2026-08-22), `DISC-DEC-027` (autorização de rascunhos NÃO travados para SPARC-004 Estágio 2 e braço depressão EEG, mais nova tentativa K3 do Lema Aberto, 2026-08-22), `DISC-DEC-028` (lock do pré-registro do braço depressão EEG, 2026-08-22), `DISC-DEC-029` (lock do pré-registro de `SPARC-FMULTI-STAGE2`, correção de robustez em `calibrate_f_multi()`, 2026-08-22), `DISC-DEC-030` (fechamento `CLOSED_REFUTED` do braço depressão EEG com reprodução adversarial confirmada, `DISC-CLAIM-007`, 2026-08-22), `DISC-DEC-031` (casos `K=3,4,5` do Lema Aberto provados por matriz de transferência uniforme em `K`, verificado por referee adversarial hostil separado, veredito SOUND, 2026-08-22), `DISC-DEC-032` (fechamento `CLOSED_INCONCLUSIVE` de `SPARC-FMULTI-STAGE2` — confundidor de heterogeneidade RUWE-correlacionada encontrado pelo debunker obrigatório, `DISC-CLAIM-008`, 2026-08-22), `DISC-DEC-033` (autorização da onda 7: tentativa `K≥6`/taxa geral-`K` + tentativa de fechamento do resíduo M-CLUST(b), 2 frentes matemáticas puras, 2026-08-22), `DISC-DEC-034` (integração do resultado PARCIALMENTE FECHADO do resíduo M-CLUST(b) — fonte localizada, `χ²` reduzido ~19,5×, resíduo residual pequeno e um passo analítico permanecem abertos, 2026-08-22), `DISC-DEC-035` (autorização de frente de continuação delimitada: tentativa de fechar o passo de agregação do resíduo M-CLUST(b) nomeado em `residual_attempt/ATTEMPT.md` §5, despachada em paralelo ao referee `K≥6`, 2026-08-22), `DISC-DEC-036` (integração de `K=6,...,10` do Lema Aberto PROVADOS incondicionalmente + conjectura de taxa geral-`K` PROVADA, explicitamente condicional a ressalva de regularidade julgada corretamente dimensionada pelo referee adversarial hostil, "Estágio 5" em `THEOREM.md`, 2026-08-22), `DISC-DEC-037` (integração de MCLUST-AGGREGATION-CLOSURE-ATTEMPT — PROGRESSO PARCIAL: obstrução de agregação de `residual_attempt/ATTEMPT.md` §5 FECHADA por primeiros princípios e validação independente (χ²=1,93/4, nível de ruído), mas não melhora `φ_CAND`, que continua a fórmula de registro, 2026-08-22), `DISC-DEC-038` (autorização da onda 8: `MCLUST-GLOBAL-EXCLUSION-ATTEMPT` + `K-GENERAL-EXISTENCE-ATTEMPT`, 2 frentes matemáticas puras independentes, 2026-08-22), `DISC-DEC-039` (integração de `MCLUST-GLOBAL-EXCLUSION-ATTEMPT` — NÃO-FECHAMENTO HONESTO da hipótese de exclusão global `tn`, `φ_GLOBAL` não supera `φ_CAND`, teste decisivo descarta a hipótese como suficiente nas 2 células de maior `ρ`/`b`, 2026-08-22), `DISC-DEC-040` (integração de `K-GENERAL-EXISTENCE-ATTEMPT` — FECHAMENTO COMPLETO da ressalva de regularidade geral-`r`, referee hostil SOUND — WITH NAMED ISSUES, Lema Aberto geral-`K` e conjectura de taxa geral-`K` agora incondicionais para todo `K≥0`, Proposição Condicional 5 promovida a **Teorema 3** incondicional, 2026-08-22), `DISC-DEC-041` (autorização da onda 9: `MCLUST-X0-ASYMMETRY-ATTEMPT` + `RATE-COEFFICIENT-POSITIVITY-ATTEMPT`, 2 frentes matemáticas puras independentes, 2026-08-22), `DISC-DEC-042` (integração de `RATE-COEFFICIENT-POSITIVITY-ATTEMPT` — PROVADO que o coeficiente de taxa `c_K` é estritamente positivo para todo `K≥2` via colapso a um novo Lema 1 e um argumento de razão monótona; referee hostil SOUND, zero discrepâncias, primeiro documento desta linha sem nenhuma correção exigida; `φ_n^{(K)}-φ_K=Θ(1/n)` exatamente para todo `K` fixo `≥2`, fechando o item (iii) de `THEOREM.md` Estágio 6 como "Estágio 7", 2026-08-22), `DISC-DEC-043` (integração de `MCLUST-X0-ASYMMETRY-ATTEMPT` — REFUTAÇÃO HONESTA da hipótese de assimetria x₀-vs-outros-arc-starts, razão agrupada `0,983±0,007` de sinal oposto, célula de `−3,7σ` não replicada; resíduo relocalizado no nível da elevação comum (`χ²=4,28/6` com elevação e `eps` medidos); `φ_EPS` reportada como achado positivo pendente de revisão adversarial, não integrada, 2026-08-22), `DISC-DEC-044` (integração do referee hostil dedicado a `φ_EPS` — veredito cindido, `eps≠0` SOUND, `φ_EPS` SOUND WITH NAMED ISSUES; `φ_EPSR` corrigida adotada como nova fórmula de registro de M-CLUST(b), substituindo `φ_CAND`; canal `eps` declarado exaurido; resíduo remanescente localizado em `φ(cíclico|x₀∉R)`, 2026-08-22), `DISC-DEC-045` (autorização da onda 10: `MCLUST-ELEVATION-LEVEL-ATTEMPT` + `K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT`, 2 frentes matemáticas puras independentes, 2026-08-22), `DISC-DEC-046` (integração de `K-GENERAL-ERROR-CONSTANT-GROWTH-ATTEMPT` — forma fechada exata de `H_r(t,b)` e `D*_r(0)`, `Θ(r^{3/2})` provado incondicionalmente para todo `b` fixo após referee hostil corrigir dois erros reais nos termos subordinados do Teorema 4 publicado (sinal/magnitude do termo `r^{1/2}`; coeficiente linear geral-`b`), correções verificadas independentemente pela sessão orquestradora antes de aceitar; item (ii) de `THEOREM.md` Estágio 6/7 fechado como "Estágio 8", 2026-08-23), `DISC-DEC-047` (autorização da onda 11: `UNIFORM-IN-C-TEOREMA-3-ATTEMPT` + `ALL-ORDERS-CLOSED-FORM-ATTEMPT`, 2 frentes matemáticas puras independentes, 2026-08-23), `DISC-DEC-048` (integração de `ALL-ORDERS-CLOSED-FORM-ATTEMPT` — forma fechada exata todas-as-ordens, geral-`K`, geral-`b`, geral-`m`, `n` finito, para a recursão discreta inteira (Teorema A/B), via identificação dos multiplicadores `F_r/G_r/H_r` como números de Stirling de primeira espécie sem sinal, com prova elementar independente; Teoremas 1–4 dos Estágios 6–8 tornam-se corolários diretos; referee hostil re-derivou o núcleo do zero (215.070 checagens exatas, zero divergências) e corrigiu um erro negativo real (a forma geral-`b` falha apenas para `b≥2`, não `b≥1` — em `b=1` é exata, incluindo um caso já provado pelo Teorema 3′ da onda 10), mais duas promoções a PROVADO; item (i) de `THEOREM.md` Estágio 6/7/8 fechado como "Estágio 9", 2026-08-23), `DISC-DEC-049` (integração de `UNIFORM-IN-C-TEOREMA-3-ATTEMPT` — convergência de Teorema 3 provada uniforme não só em compactos `[0,C]` mas globalmente em `[0,∞)`, ambos incondicionais (Teorema A/C), via dois lemas elementares novos que dispensam a maquinaria `F_r/G_r/H_r`; perfil de erro exato `e(c)` incondicional coeficiente-a-coeficiente (Teorema D); referee hostil auditou os dois teoremas incondicionais com peso máximo e não encontrou nenhum erro, mas corrigiu a descrição de uma lacuna já rotulada condicional (Teorema E, versão uniforme do perfil de erro — a lacuna real é geometricidade qualitativa de `M_K`, não uma constante explícita) e registrou um fortalecimento não solicitado (`a^*` é exato, não aproximado); item (iv) de `THEOREM.md` Estágio 6/7/8/9 fechado como "Estágio 10", 2026-08-23), `DISC-DEC-050` (integração de `MCLUST-ELEVATION-LEVEL-ATTEMPT` — mecanismo da elevação de fechamento M-CLUST(b) identificado e confirmado independentemente (`λ(t)`, função da massa percorrida, não constante); redução original refutada a alta precisão; correção do referee `φ_REDB` (`c''=c(1-c/n)^(b-1)`) adotada como nova fórmula de registro, substituindo `φ_EPSR`, mas resíduo real permanece não fechado na célula mais extrema testada (`b=100,c=1000`, `z≈-10`); resíduo M-CLUST(b) permanece PARCIALMENTE FECHADO; seis correções datadas em `ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore B ganhou dois nós, 2026-08-23), `DISC-DEC-051` (autorização da onda 12: `MK-QUALITATIVE-GEOMETRICITY-ATTEMPT` + `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT`, 2 frentes matemáticas puras independentes, cada uma com rota construtiva já esboçada — não executada — por um referee independente, 2026-08-23), `DISC-DEC-052` (integração de `MK-QUALITATIVE-GEOMETRICITY-ATTEMPT` — crescimento geométrico qualitativo de `M_K` PROVADO (`M_K≤φ_K(K+1)e^{K/2}+K=O(K(\sqrt e)^K)`) via rota alternativa usando a forma fechada todas-as-ordens do Estágio 9 (não a rota da Proposição 6 originalmente esboçada, que permanece OPEN); fecha a única obstrução nomeada restante para Teorema E (Estágio 10) ser incondicional — Teorema E PERDE o rótulo PROVED-MODULO; referee hostil SOUND, "ACCEPT for catalogue"; NÃO fecha a hipótese (U')/taxa explícita para Teorema A/C, obstrução distinta e mais forte que permanece aberta; cinco correções datadas em `uniform_in_c_attempt/ATTEMPT.md`; "Estágio 11" anexado a `THEOREM.md`, 2026-08-23), `DISC-DEC-053` (integração de `MCLUST-SHORT-CYCLE-DYNAMICS-ATTEMPT` — NÃO-FECHAMENTO HONESTO do resíduo extremo de `φ_REDB`, com avanço genuíno de mecanismo: confirmado que todo ciclo-π intocado (qualquer `L`, não só `L≤b`) é deterministicamente um ciclo de `f`; descoberto que o pequeno resíduo agregado é o quase-cancelamento de dois efeitos bem maiores e opostos (excesso grande perto de `L=b`, referee independente: `+796%` a `+874%`; platô negativo persistente `~−10%` a `−15%` para `L` longo), nenhum modelado; candidata `φ_REDC` REFUTADA (piora 5/6 células); referee hostil SOUND WITH NAMED ISSUES, confirmou o mecanismo a escala 2,2× maior e a refutação de `φ_REDC` de forma independente; `φ_REDB` permanece fórmula de registro, resíduo M-CLUST(b) permanece PARCIALMENTE FECHADO; três correções datadas em `ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore B ganhou dois nós, 2026-08-23), `DISC-DEC-054` (autorização da onda 13: `U-PRIME-HYPOTHESIS-ATTEMPT` + `LONG-CYCLE-DEFICIT-ATTEMPT`, 2 frentes matemáticas puras independentes, cada uma reabertura explicitamente nomeada e ainda aberta pela integração que a descobriu, 2026-08-23), `DISC-DEC-055` (integração de `U-PRIME-HYPOTHESIS-ATTEMPT` — hipótese (U') PROVADA com constante explícita não-nítida `a=1+√(π/2)=2,253314…`, fechando a última obstrução central nomeada entre Teorema A/C (já provados) e uma taxa de convergência explícita para a linha `uniform_in_c_attempt`: `|Δ_n(c)|≤[(1+√(π/2))√c+0,2805]/n`, incondicional; prova via decomposição exata de `T(n,K)` (provando fato (i) de Estágio 10/§6.3 para todo `K`, não só numericamente), colapso a `M_K=Q(K+1)-(K+1)φ_K` (função `Q` de Ramanujan) via a identidade `φ_n^{(n-1)}=Q(n)/n` já estabelecida, e dois limitantes-sanduíche elementares; constante nítida `a*=0,3670872…` permanece aberta, ingrediente exato nomeado (limitante inferior para `Q(n)`); referee hostil re-derivou tudo do zero das fontes primárias (nenhum `.py` da frente-alvo lido), motor Markov `(a,b,r)` independente construído, desigualdade final checada com zero violações até `K=10^5`; veredito SOUND, "ACCEPT for catalogue", nenhum erro encontrado; "Estágio 12" anexado a `THEOREM.md`; quatro correções datadas em `uniform_in_c_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore A ganhou um adendo; `README.md` atualizado, 2026-08-23), `DISC-DEC-056` (integração de `LONG-CYCLE-DEFICIT-ATTEMPT` — investigação H1-vs-H2 do platô negativo persistente de ciclos longos do M-CLUST(b): MISTURA de piso independente de `b` (H2, dominante, `z` até `−13,9` no referee) e amplificação secundária dependente de `b` (H1, real, sub-limiar, `~1,8–2,6×`); referee hostil SOUND WITH NAMED ISSUES, replicou T0/T1/T2 do zero (`N=5000`/`N=2500`, código próprio), confirmou todas as conclusões centrais, resolveu a favor de H2 a ambiguidade da célula A da própria frente (achado positivo); dois problemas nomeados corrigidos via correções datadas (cifra de referência mal-atribuída, precisão de T2) sem mudar nenhuma conclusão; resíduo M-CLUST(b) permanece PARCIALMENTE FECHADO; `PROOF_DEPENDENCY_MAP.md` Árvore B ganhou um nó novo, 2026-08-23), `DISC-DEC-057` (autorização da onda 14: 5 frentes matemáticas puras independentes atacando todo item genuinamente aberto e nomeado com precisão no arquivo, a pedido explícito do usuário — `SHARP-CONSTANT-U-PRIME-ATTEMPT`, `FLOOR-CLOSED-FORM-ATTEMPT`, `CONJECTURE-1-K2-ATTEMPT`, `GENERAL-B-DSTAR-ATTEMPT`, `CELL-VARIATION-ATTEMPT`, 2026-08-23), `DISC-DEC-058` (integração de `SHARP-CONSTANT-U-PRIME-ATTEMPT` — limitante inferior de Ramanujan `Q(n)≥√(πn/2)-6` PROVADO, dando `lim_{K→∞}M_K/√K=a*` exatamente — primeira confirmação rigorosa de que a constante nítida é o valor assintótico correto; monotonicidade de `M_K/√K` (peça 2) NÃO fechada; constante efetivamente provada na hipótese (U') permanece `a=1+√(π/2)`, não `a*`; referee hostil SOUND, "ACCEPT for catalogue", verificado até `n,K=10^6`, zero violações, achado analítico novo (`Err(n)→3/2`) não presente no documento-alvo; "Estágio 13" anexado a `THEOREM.md`, 2026-08-23), `DISC-DEC-059` (integração de `GENERAL-B-DSTAR-ATTEMPT` — forma fechada geral-`b` de `D^{*(p)}_r(b)` PROVADA para `p=1,2,3,4`, todo `b≥0` (Teorema D1 + três fórmulas irmãs), fechando o item nomeado aberto por Estágio 9 nesse escopo; `p=2` re-deriva independentemente o já provado Teorema 3′; referee hostil re-derivou a rota inteira do zero, 165.888 checagens exatas, 0 divergências, escala superior à própria frente; achado extra do referee: obstrução nomeada para `p≥5` (item 11) é mecanicamente REMOVÍVEL (prova geral de paridade binomial), mas `p≥5` continua NÃO fechado; veredito SOUND, "ACCEPT"; "Estágio 14" anexado a `THEOREM.md`; duas correções datadas em `general_b_dstar_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore A ganhou um adendo, 2026-08-23), `DISC-DEC-060` (integração de `CELL-VARIATION-ATTEMPT` — investigação de qual covariável (`ρ`,`c`,`b`) explica a variação célula-a-célula do H2-share; regra PRIMÁRIA mecânica dá PARTIAL/MIXED, três checagens secundárias convergem em `ρ` (`r=−0,623,p=0,031`), `b` estatisticamente indistinguível de zero; referee hostil re-simulou 9/13 células do zero (68.000 instâncias frescas), T0 e toda aritmética/fórmula confere exatamente, nomeou duas complicações reais — correlação de `ρ` NÃO sobrevive Bonferroni/Spearman nos dados originais; célula `G1b` (excluída por ambiguidade), resolvida por triangulação (`N=12.000,z=−7,69`), revela não-monotonicidade real em `ρ` dentro de `G1` — MAS na tabela triangulada do próprio referee a correlação `ρ` FORTALECE e SOBREVIVE Bonferroni (`r=−0,680,p=0,011`), `b` continua robustamente descartado; veredito SOUND WITH NAMED ISSUES; resultado correlacional, `φ_REDB` permanece fórmula de registro; um adendo datado em `cell_variation_attempt/ATTEMPT.md`; `PROOF_DEPENDENCY_MAP.md` Árvore B ganhou o nó `CVCOV` + um adendo, 2026-08-23), `DISC-DEC-061` (integração de `CONJECTURE-1-K2-ATTEMPT` — `THEOREM.md` §8 Conjectura 1 PROVADA em `K=2`: `f_{M_2}(x)=4x(1-x^2)`, módulo a mesma citação clássica já usada pela Proposição 2.4; `K≥3` permanece exatamente tão aberto quanto antes; referee hostil re-derivou o Lema 1 via modelo gerativo diferente (simulação discreta), a tabela de mecanismo de 9 células (260.000 testes exatos, 100% de acerto) e reconfirmou a densidade a `n=20.000`; veredito SOUND WITH NAMED ISSUES (um, menor, não-substantivo), "ACCEPT for catalogue"; "Estágio 15" anexado a `THEOREM.md`, com pointers em §8 e §9; duas correções datadas em `conjecture1_k2_attempt/ATTEMPT.md`, 2026-08-23), `DISC-DEC-062` (integração de `FLOOR-CLOSED-FORM-ATTEMPT` — FECHANDO A ONDA 14 (5/5 frentes); FECHAMENTO PARCIAL HONESTO do piso H2 em `b=1`: redução exata PROVADA (efeito de seleção sobre `φ(ℓ)` não-constante), Candidato 1 refutado decisivamente, mecanismo de "reentrada de lacuna" PROVADO exatamente e validado por simulação da forma exata; forma fechada completa NÃO derivada (sistema acoplado não-local de 2 variáveis); frente retirou, ela mesma, uma alegação mais fina que não sobreviveu a réplica robusta a cluster; referee confirmou as 3 alegações empíricas a `5×+` potência, único achado uma imprecisão de redação corrigida; veredito SOUND WITH NAMED ISSUES, "ACCEPT for catalogue"; `φ_REDB` inalterada; `PROOF_DEPENDENCY_MAP.md` Árvore B ganhou o nó `FLOORCF` + um adendo, 2026-08-23), `DISC-DEC-063` (autorização da onda 15: `GENERAL-P-DSTAR-CLOSURE-ATTEMPT` (p≥5, risco baixo) + `CONJECTURE-1-K3-ATTEMPT` (K=3, risco mais alto, não-fechamento honesto aceitável), 2 frentes matemáticas puras independentes, por `DISC-DEC-023`, 2026-08-23), `DISC-DEC-064` (integração de `GENERAL-P-DSTAR-CLOSURE-ATTEMPT` — item 11 do scorecard de `general_b_dstar_attempt/ATTEMPT.md` FECHADO para `p=1,...,10`, todo `b≥0`: `Q_p` via identidades de Newton, momentos via função geradora de cumulantes, ambos algoritmos gerais em `p`; `26.710` checagens exatas, `0` divergências; referee re-verificou com métodos deliberadamente diferentes (`18.653` checagens, `0` divergências) e construiu uma PROVA INDUTIVA de que a máquina `H_k(r,b)` é correta para TODO `k`, fechando analiticamente a lacuna que o documento nomeou como maior risco; veredito SOUND, "ACCEPT for catalogue"; `p>10` aberto apenas por não executado, não por incerteza matemática; "Estágio 16" anexado a `THEOREM.md`, com pointer em Estágio 14; correção datada em `general_b_dstar_attempt/ATTEMPT.md`, 2026-08-24), `DISC-DEC-065` (integração de `CONJECTURE-1-K3-ATTEMPT` — FECHANDO A ONDA 15 (2/2 frentes); `THEOREM.md` §8 Conjectura 1 PROVADA em `K=3`: `f_{M_3}(x)=6x(1-x^2)^2`, módulo a mesma citação clássica de `K=1,2`, aplicada recursivamente — fechamento COMPLETO e INESPERADO, contrariando a expectativa de dispatch de não-fechamento por explosão combinatória compartilhada por duas frentes anteriores; Lema 1 generalizado a 3 fontes via split em 5 padrões, `64` configurações brutas de destino colapsam em `7` formas via "fora-do-ciclo contribui zero"; `K≥4` explicitamente não tentado; referee hostil, briefado para caçar a falha que explicaria a surpresa, re-derivou tudo do zero incluindo as 7 formas de destino (não só as 2 pré-checadas), `26.000` testes de mecanismo discreto sem divergências, `8.000.000` amostras de Monte Carlo contínuo; veredito SOUND, "ACCEPT for catalogue", nenhum erro matemático encontrado, único achado uma lacuna de exposição menor não-substantiva; "Estágio 17" anexado a `THEOREM.md`, com pointers em Estágio 15, 2026-08-24), `DISC-DEC-066` (autorização e despacho da onda 16, a pedido explícito do usuário — 5 frentes matemáticas puras independentes, uma para cada item da lista-mestra de abertos do "veredito honesto atualizado" do Estágio 17, replicando a estrutura de 5 frentes da onda 14: `CONJECTURE-1-K4-ATTEMPT`, `SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT`, `GENERAL-P-DSTAR-EXTENSION-ATTEMPT`, `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT`, `CONJECTURE-2-DIRECT-ATTEMPT`; não-fechamento honesto declarado aceitável em todas as 5, 2026-08-24), `DISC-DEC-067` (integração de `CONJECTURE-2-DIRECT-ATTEMPT` — NÃO-FECHAMENTO HONESTO da rota direta da Conjectura 2, com progresso parcial provado: arquitetura do método dos momentos correta-se-completada; alvos `E[M(c)²]=(1−e^{−c})/c` e `E[M_K²]=1/(K+1)` (sobre a lei conjecturada, âncoras incondicionais em `K≤3`); redução por blocos do `p=2` provada e fortalecida pelo referee a "toda célula `=(n−2)!`" até `n=8`; certificado de bloco intacto provado; rota Poissonization-em-`c` REFUTADA por contraexemplo exato (`n=6`, contagem cíclica 3→5 ao adicionar um reroute; scan exaustivo do referee fecha a variante direção-em-`M`: 9 subidas/7 descidas de uma configuração); obstrução real (exploração conjunta de 2 pontos) localizada e aberta; referee SOUND WITH NAMED ISSUES (4 menores, 2 reparados pelo próprio referee), ACCEPT no tier reivindicado; 4 adendos datados; "Estágio 18" anexado a `THEOREM.md` com extensões datadas no §8, incluindo correção de omissão K=3 da integração anterior, 2026-08-25), `DISC-DEC-068` (integração de `SHARP-CONSTANT-A-STAR-MONOTONICITY-ATTEMPT` — FECHAMENTO COMPLETO, na terceira tentativa, do gap mais difícil da linha: `sup_K M_K/√K = a*` EXATAMENTE, via `M_K < a*√K` estrito para todo `K≥1` (Robbins 1955 + FGKP95 Teorema 7 — confirmado pelo referee contra o PDF primário — + identidade clássica `Q(n)=n!e^n/(2n^n)−θ(n)`; o `z_K`-bound do Lema 4.1 sem modificação bastou do outro lado); hipótese (U') com constante nítida `a*` em todos os casos `0≤K≤n`, o caso de contorno `K=n` fechado pelo próprio referee (§8) e re-verificado pela sessão (0 violações racional-certificado n=1..300); taxa nítida em `c` NÃO afirmada (re-montagem do Estágio 12 não executada, nomeada como próximo passo); referee SOUND WITH NAMED ISSUES com 2 erratas obrigatórios (E-1 exibição de Robbins sem `(n/e)^n`; E-2 dois intermediários impressos do Lema 1 falsos — mesmo defeito achado independentemente pelo spot-check da sessão) + 3 notas, todos corrigidos via 5 adendos datados; "Estágio 19" anexado a `THEOREM.md`, pointers nos Estágios 12–13, 2026-08-25), `DISC-DEC-069` (integração de `CONJECTURE-1-K4-ATTEMPT` — FECHAMENTO COMPLETO E INESPERADO, segunda surpresa consecutiva: `f_{M_4}(x)=8x(1−x²)³` PROVADO em K=4, módulo a mesma citação clássica; mecanismo: Bell(4)=15 padrões de coincidência colapsam em 5 formas via `∏(b_j−1)!` somando a `K!=24` pela bijeção partição↔permutação, expansão de 625 termos reduzida a 12 tipos de forma (`Σp(s)`), `W_C(Q)=1−Q` até `n_off=4` via identidade de florestas ponderadas `E(E+Q)^{n−1}=E` — nomeada rota candidata para `K≥5`, não tentado; Conjectura 1 provada em `K=1,2,3,4`; spot-check independente da sessão (enumeração exata `Fraction`, zero discrepâncias) antes do despacho; referee SOUND, ACCEPT for catalogue (2 achados cosméticos); 2 adendos datados; "Estágio 20" anexado a `THEOREM.md` com nota datada no §8 Conjectura 1, 2026-08-25), `DISC-DEC-070` (integração de `GENERAL-P-DSTAR-EXTENSION-ATTEMPT` — `D^{*(p)}_r(b)` montado e verificado para `p=11,…,20`, todo `b≥0`, via a máquina `H_k` provada correta para todo `k` na onda 15; verificação uniforme do referee `r≤200`, `b≤30`, 75.899 checagens, zero discrepâncias, self-check determinístico 36/36; bônus analítico do referee: limite de grau `deg_r H_{2k−1}=k−1` PROVADO com coeficiente líder `4^{k−1}(k−1)!`; `p>20` aberto apenas por não executado; referee SOUND, ACCEPT for catalogue; 1 adendo datado; "Estágio 21" anexado a `THEOREM.md`, pointers nos Estágios 16–17, 2026-08-25), `DISC-DEC-071` (integração de `FLOOR-H2-B1-FULL-CLOSURE-ATTEMPT` — FECHAMENTO PARCIAL FORTALECIDO do sistema `(Φ,Ψ)` do piso H2 em `b=1`; frente entregou regime small-`t0` exato + solver corrigido/convergente (Richardson `0,0377`, `|z|<1,7` vs 6 MCs) + achado near-rank-2 + 3 bugs auto-capturados; referee replicou todas as alegações positivas do zero (MC 1M, solver PDE de outra família com razões 0,250, série exata ordem 500) e REFUTOU as duas negativas na direção de underselling — N1: família fechada `{P+Q·erfcx}` para todos os coeficientes (indução, sem quadratura), N2: "raio" era erro de truncamento, série converge no platô inteiro, `Φ(0,t0≥0,02)=0,0377616`; sessão verificou os resultados do referee antes de catalogar (sympy resíduos 0; implementação `(P,Q)` independente ordem 200); restam ressomação fechada e gap abstrato-vs-real ~30%; `φ_REDB` inalterada; nó `FLOORH2` na Árvore B; veredito SOUND WITH NAMED ISSUES, ACCEPT, 6 adendos datados; **ONDA 16 FECHADA — 5/5** , 2026-08-25), `DISC-DEC-072` (autorização e despacho da onda 17 — 5 frentes, uma por aberto nomeado no fechamento da onda 16: (a) Conjectura 1 K=5/geral via florestas ponderadas, (b) taxa nítida em `c` com `a*`, (c) exploração conjunta de 2 pontos, (d) ressomação da constante do platô `0,0377616`, (e) lei de escala `√(2/(2−γ))`; seeds 20260860000–20260869999 reservados, 2026-08-25), `DISC-DEC-073` (integração de `SHARP-RATE-REASSEMBLY-ATTEMPT` — Teorema R: `|φ(n,c)−φ_∞(c)| ≤ [a*√c+κ_B]/n`, `n≥4`, `0≤c≤n`, estrito em `(0,n]`; a constante antiga consumida em exatamente um passo (Jensen); `κ_B` inalterada por independência estrutural da metade `B_n` e certificada em `(0,28048, 0,2805)` por racional puro; bound justo na linha `c=n` (razão→1, `a*` ótima nesta forma, fator 6,14 de melhoria); frente 2.594 células/0 violações, sessão 404 células independentes/0 violações, referee 1.060 células/0 violações com contorno a `n=50.000`; veredito SOUND WITH NAMED ISSUES, ACCEPT (R-1 estatística corrigida ≈0,9904, direção segura; O-1 nit herdado); 2 adendos datados; "Estágio 22" anexado a `THEOREM.md`, pointers nos Estágios 12/19/21, 2026-08-25) |
| Claims fechados/registrados | 7 (`DISC-CLAIM-001`, `preregistered_inconclusive`; `DISC-CLAIM-002`, `preregistered_inconclusive` após Gate, `replication_status: REPLICATION_FAILED`; `DISC-CLAIM-003`, `preregistered_falsified` [direção de H, efeito real na direção oposta], `replication_status: REPLICATION_PASSED`; `DISC-CLAIM-004`, `preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`, `replication_status: REPLICATION_FAILED` [inconclusivo por falta de poder no dataset reservado, não contradição]; `DISC-CLAIM-005`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [estatística estruturalmente incapaz de produzir veredito válido, não erro de implementação]; `DISC-CLAIM-006`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [confundidor de multiplicidade oculta plausivelmente suficiente para explicar o sinal residual, não erro de implementação — o bug de assimetria de ruído foi corrigido antes de catalogar]; `DISC-CLAIM-007`, `preregistered_falsified` [entropia espectral EEG em depressão na direção OPOSTA à prevista, `d=1,447`], `adversarial_review_verdict: CONFIRMED`; `DISC-CLAIM-008`, `preregistered_inconclusive`, `adversarial_review_verdict: METHODOLOGY_FLAW_FOUND` [heterogeneidade RUWE-correlacionada não capturada pelo modelo de f_multi único, não bug de código -- reprodução bit a bit confirmada]) |
| Claims em andamento | 0 |

## Resultado do piloto (DISC-COSMOLOGY-MOND-SPARC-001)

Auditoria do código legado (`AUDIT_LEGACY_MOND_EFE_SPARC.md`) confirmou que
o resultado "EFE CONFIRMED, p<0.000001" de
`01_TAMESIS_CORE/.../MOND_EFE/efe/README.md` vinha de curvas de rotação
digitadas à mão para 8 galáxias de Virgem que **não existem** no catálogo
SPARC público real — não apenas um fallback de emergência, mas o dado por
trás da manchete inteira.

Refeito com dado real (SPARC_Lelli2016c.mrt + Rotmod_LTG/*.dat, 175
galáxias, proveniência em `data/PROVENANCE.md`), pré-registro travado antes
de qualquer cálculo (`PREREGISTRATION.md`, commit `49867fa`), o teste
comparável disponível (aglomerado de Ursa Maior vs. campo, já que Virgem não
está representado na amostra real) deu p=0.049373 — cruza o limiar de 0.05
na direção prevista pelo EFE, mas cai exatamente na zona frágil (0.04–0.06)
que o próprio pré-registro já previa precisar declarar como tal.

Reexecução adversarial independente reproduziu os números exatamente (sem
bugs) e mostrou que excluir 4 galáxias de campo com ajuste de inclinação
baseado em apenas 2 pontos inverte o veredito (p sobe para 0.0635). Veredito
formal: **INCONCLUSIVE**. Registrado em `DISC-CLAIM-001`, sem nenhuma
linguagem "CONFIRMED"/"DETECTED".

Este é o resultado que a trilha foi desenhada para produzir: nem a manchete
inflada do código legado, nem uma negação categórica — um número real,
reproduzido de forma independente, e corretamente rotulado como frágil
demais para sustentar qualquer alegação de detecção.

## Resultado de DISC-COSMOLOGY-MOND-SPARC-002 (pivotado, encerrado)

`next_action` original (extrair de `01_TAMESIS_CORE` uma previsão Tamesis
distinta de MOND genérico) resolvido com achado **negativo**: essa
previsão não existe. Pivotado para testar qual das duas derivações
internas conflitantes de `a₀` sobrevive ao dado real — `a₀=cH₀/(2π)`
("Ponte Holográfica") vs. `a₀=cH₀` ("MOND Emergence", cuja própria
alegação numérica já é aritmeticamente incorreta por fator ~5,7,
independente de qualquer dado).

Na amostra de descoberta (120 galáxias), o resultado pareceu decisivo:
`H_A` sobrevive, `H_B` falsificada por fator ~2,5×, reproduzido de forma
independente com 0,004% de diferença. O Gate de Replicação (holdout de 55
galáxias, nunca antes visto, aberto por um terceiro agente independente)
**não confirmou** esse resultado — `g†` no holdout saiu 3,5× maior,
intervalo de confiança largo o suficiente para conter as duas hipóteses.
Um adversário de nulo dedicado mostrou que o achado sobrevive a
sistemáticas conhecidas do SPARC, mas seu peso evidencial específico para
Tamesis é mais fraco do que parecia (a0_A reproduz uma coincidência já
conhecida na literatura MOND padrão desde antes de Tamesis existir).
Achado lateral acionável: `MOND_Emergence/index.html:282` provavelmente
contém um erro de copy-paste, independente do veredito estatístico.

Veredito final: `DISC-CLAIM-002`, `evidence_level: preregistered_inconclusive`,
`replication_status: REPLICATION_FAILED` (inconclusivo, não contraditório).
Ver `09_SESSIONS/2026/2026-08-12_A0_DERIVATION_PIVOT.md` para o relato
completo em ordem cronológica.

## Fase 0 de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14)

Iniciada a pedido do usuário. Três agentes investigaram em paralelo:
(1) busca exaustiva por nova previsão Tamesis-específica em
`01_TAMESIS_CORE` — **negativa**, toda fórmula adicional encontrada ou
reproduz exatamente MOND padrão (a função de interpolação "derivada"
por unicidade holográfica é numericamente idêntica à "Simple" de
Milgrom/Famaey & Binney; a função "TAMESIS" é a própria curva empírica
de McGaugh et al. 2016 rebatizada), ou já foi auto-refutada dentro do
próprio corpus (correlação M/L-`g_ext`), ou duplicaria SPARC-001 (teste
EFE Ursa Maior), ou não é falsificável como está (lente de aglomerado);
(2) a discrepância de leverage do holdout de SPARC-002 como germe de
teste — **negativa**, Monte Carlo mostrou que é variância de amostragem
comum (percentil ~78, nada extremo), sem nenhuma alegação Tamesis sobre
comportamento em alta aceleração para dar um modelo concorrente nomeado;
(3) dataset independente para replicar o veredito de SPARC-002 —
**positiva**: binárias largas do Gaia (El-Badry, Rix & Heintz 2021,
MNRAS 506, 2269) são reais, públicas, volumosas (≈1,94 GB, 1.817.594
pares), o mesmo catálogo usado por Chae (2023) para testes de gravidade
em regime de aceleração ultra-baixa.

**Achado de integridade grave, descoberto no processo:**
`01_TAMESIS_CORE/.../lab_gravity/analysis/gaia_real_analysis.py` contém
uma lista `REAL_GAIA_BINARIES` rotulada como dado real de El-Badry/Chae,
mas com `source_id` sequenciais/artificiais e progressão de velocidades
monotônica demais — dado fabricado. O achado "MOND DETECTED"
(`RESEARCH_RESULTS.md:259-261`) descansa sobre esse dado — mesmo padrão
do achado original que motivou a criação desta trilha (curvas de
Virgem fabricadas, SPARC-001).

**Rota recomendada:** tratar SPARC-003 como réplica independente do
veredito ainda inconclusivo de SPARC-002 (`H_A: a0=cH0/2π` vs.
`H_B: a0=cH0`), substituindo o dataset fabricado pelo catálogo real
El-Badry et al. (2021). Nenhuma nova alegação — mesmas duas hipóteses já
travadas em SPARC-002, observável discriminador adaptado ao novo
sistema físico (binário Kepleriano, não disco rotativo). Antes de
qualquer pré-registro: verificar por fetch direto a fórmula exata do
estimador de Chae (2023), declarar corte de qualidade e split
discovery/holdout próprios. Detalhes completos em
`02_TESTS/COSMOLOGY_WIDE_BINARIES/phase0/PHASE0_SEARCH.md`.

## Pré-registro travado de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14)

A pedido do usuário, pré-registro escrito e travado
(`02_TESTS/COSMOLOGY_WIDE_BINARIES/PREREGISTRATION.md`). Metodologia de
Chae verificada por fetch direto de **dois** artigos primários (uma
confusão de arXiv ID entre o título/ApJ citado e o número arXiv
originalmente fornecido foi descoberta e corrigida: são dois artigos
reais e distintos do mesmo autor, "Artigo A" ApJ 952,128/arXiv:2305.04613
e "Artigo B" arXiv:2309.10404, artigo de acompanhamento). O método
primário de Chae (desprojeção 3D via Monte Carlo orbital, dependente de
excentricidades de Hwang et al. 2022 não verificadas nesta sessão) foi
declarado tratável demais para reproduzir diretamente — adotado em vez
disso o método de perfil de velocidade projetada do Artigo B (simplicação
honesta e declarada, ainda real/publicada, validada pelo próprio Chae
como correlacionada ao método completo).

Catálogo real El-Badry, Rix & Heintz (2021) baixado por completo
(1.937.351.290 bytes = 100% do esperado, sha256 verificado duas vezes,
1.817.594 pares, contagem exata batendo com o paper). Cortes de
qualidade REAIS de Chae aplicados (`R<0,01` — não `R<0,1` como suposto
inicialmente —, `200<sepAU<30.000`, `BinType==MSMS`, distância`<200pc`,
`4<M_G<14`): **43.147 sistemas** sobrevivem. Massa estelar derivada via
relação massa-luminosidade de Pecaut & Mamajek (2013), tabela de Mamajek
baixada diretamente (catálogo não traz massa). Split
discovery(**30.203**)/holdout(**12.944** selado) gerado com seed
determinístico. Bordas de 5 bins de `log(g_N)` calculadas somente de
massa+separação — `a0_A` e `a0_B` ambos caem dentro da faixa de dado
disponível, dando poder genuíno ao teste. H_A/H_B idênticas às já
travadas em SPARC-002, não reformuladas. Nenhuma razão de velocidade
observada foi calculada antes deste lock.

Status: `CANDIDATE_LOCKED`. Próximo passo: rodar a análise
pré-registrada, depois reexecução adversarial independente.

## Resultado final de `DISC-COSMOLOGY-MOND-SPARC-003` (2026-08-14) — `CLOSED_INCONCLUSIVE`

Análise pré-registrada rodada sobre os 30.203 sistemas de descoberta,
seguida de reexecução adversarial independente (segundo agente,
implementação do zero, sem ler o código/resultado primário antes de ter
o próprio pronto). **Concordância bit a bit** em toda a parte
determinística entre os dois agentes — nenhum bug de fórmula, unidade,
constante ou binagem em nenhum dos dois scripts.

**As 5 medianas empíricas de `v_p_obs/v_p_N` por bin** (0,6932; 0,6409;
0,6243; 0,6150; 0,5941) **são todas abaixo de 1** — mas o modelo MOND
pré-registrado, `(1-e^{-√(g_N/a0)})^{-1/2}`, tem imagem estritamente em
`(1,+∞)` para qualquer `a0>0` finito. **Não existe `a0` que alcance o
alvo.** Checagem de convergência e checagem de sanidade (Seção 3 do
pré-registro) — ambas já declaradas como salvaguardas — falharam:
ajustes de `x0=1` e `x0=5` divergem ~16%; `a0` ajustado sai ~2,4 ordens
de grandeza abaixo do valor de referência McGaugh.

**Causa raiz confirmada independentemente, não é bug:** o agente
adversarial rodou uma simulação Monte Carlo própria (N=200.000) de
binárias Keplerianas puramente Newtonianas (zero física MOND) e obteve
mediana(v_proj/v_circ)≈0,55 — mesma ordem de grandeza do observado no
dado real. É diluição por projeção, efeito conhecido na literatura
(Pittordis & Sutherland 2018; Banik & Zhao 2018), já antecipada no
preâmbulo da Seção 4 do pré-registro como limitação da estatística
simplificada adotada.

Por instrução explícita da própria Seção 3 ("o teste para até isso ser
resolvido, antes de aceitar qualquer veredito H_A/H_B"): **nenhum
veredito H_A/H_B é aceito.** Registrado como `DISC-CLAIM-005`,
`evidence_level: preregistered_inconclusive`,
`adversarial_review_verdict: METHODOLOGY_FLAW_FOUND`. Gate de
Replicação nunca acionado (teste já falhou sua própria checagem de
sanidade). Holdout (12.944 sistemas) permanece selado, disponível para
um teste futuro genuinamente redesenhado com desprojeção completa.
Lição de governança registrada em `METHODOLOGY_EXTENSIONS.md` Seção 1.
Detalhes completos: `09_SESSIONS/2026/2026-08-14_SPARC003_WIDE_BINARIES.md`.

## Resultado final de `DISC-COSMOLOGY-MOND-SPARC-004` (2026-08-18) — `CLOSED_INCONCLUSIVE`

Usuário pediu para redesenhar SPARC-003 com desprojeção Monte Carlo
completa (método primário de Chae 2023: desprojeção 3D orbital, não a
simplificação de velocidade projetada que matou SPARC-003 por restrição
de imagem). Pré-registro travado após validação sintética pré-lock
corrigir a estatística discriminadora para `δ_obs-newt` (real menos mock
Newtoniano casado por sistema), reaproveitando H_A/H_B, catálogo, cortes
e split de SPARC-002/003 sem modificação.

**Análise primária v1:** `δ_obs-newt=[+0,2274;+0,1723;+0,1313;+0,1027;
+0,0467]`, `a0_fit=3,634×10⁻¹⁰` (IC95% `[2,944×10⁻¹⁰;4,494×10⁻¹⁰]`),
`BOTH_FALSIFIED` bruto. A descoberta adversarial de nulos obrigatória
(`AGENTS.md` passo 7) achou um **bug de implementação real** (não
reformulação): o ramo mock não carregava ruído astrométrico Gaia,
enquanto o ramo real carrega — viés de Rice/Rayleigh não cancelado pela
subtração real-mock, provado decisivamente via teste 100% sintético.
Corrigido, revalidado, análise real re-executada.

**Análise primária v2 (corrigida):** `δ_obs-newt=[+0,1486;+0,1482;
+0,1150;+0,0949;+0,0430]` (~5× menor), `a0_fit=1,657×10⁻¹⁰` (IC95%
`[1,232×10⁻¹⁰;2,181×10⁻¹⁰]`) — `a0_A` cai logo abaixo do IC (margem
~0,057 dex), `a0_B` claramente fora. Reexecução adversarial confirmou v2
bit a bit.

**Achado decisivo:** o gatilho pré-declarado (`g/g_N` real bruto>1 no
bin 0) ativou a checagem adversarial obrigatória de multiplicidade
oculta (`f_multi`, Chae Eqs. 11-13, declarada NÃO implementada). Com o
sinal v2 corrigido, companheiras não resolvidas — sozinhas, em magnitude
inteiramente plausível pela literatura (`f_multi=0,25-0,47`) — cobrem de
23% a 146% do sinal por bin, a diferença RUWE-alto/baixo excede o sinal
real total em vários bins, e mesmo `f_multi=0,25` produz sinal sintético
(zero MOND) maior que o sinal real inteiro nos 5 bins.

Por instrução explícita da própria Seção 4 do pré-registro ("checagem
adversarial de multiplicidade oculta obrigatória se `g/g_N>1`, ANTES de
aceitar qualquer veredito"): **nenhum veredito H_A/H_B é aceito.**
Registrado como `DISC-CLAIM-006`, `evidence_level:
preregistered_inconclusive`, `adversarial_review_verdict:
METHODOLOGY_FLAW_FOUND`. Gate de Replicação não acionado. Holdout
(12.944 sistemas) permanece selado, disponível para uma tentativa futura
que implemente a auto-calibração completa de `f_multi`. Detalhes
completos: `02_TESTS/COSMOLOGY_WIDE_BINARIES_MC_DEPROJECTION/PREREGISTRATION.md`
Seção 7; `09_SESSIONS/2026/2026-08-18_SPARC004_MC_DEPROJECTION.md`.

## Resultado da linha RH-REAL (dois sub-testes, ambos com Gate acionado)

Motivada pela pesquisa de zeros de zeta da Anthropic, a linha `DISC-RH-REAL-001`
converteu duas afirmações de literatura não-testáveis com dado finito
(`liminf`/"infinitos") em perguntas proxy falsificáveis com modelo
concorrente nomeado, satisfazendo a exigência de discriminating observable.

**Sub-teste 1 — `DISC-RH-ZERO-GAP-RUNS-001`** (item 9, correlação sequencial
de gaps). Hipótese direcional original **errada** — previu mais runs de
gaps grandes consecutivos, achado real foi o oposto (`INVERSE_SIGNAL`,
reportado honestamente como tal, sem spin). Gate de Replicação com
`zeros4.txt` (regime #10²¹): `REPLICATION_PASSED`. Adversário de nulo
mostrou que o efeito é genérico a qualquer sequência com autocorrelação
serial negativa (confirmado via simulação sintética AR(1)) — isso não
enfraquece o achado, já que a alegação substantiva sempre foi "gaps de
zeta têm correlação serial negativa", não um mecanismo exclusivo de zeta.
Ver `09_SESSIONS/2026/` para o relato completo desta sessão.

**Sub-teste 2 — `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`** (item 7,
constante de gaps pequenos de Inoue 2026, arXiv:2604.05733). Pergunta
proxy via teoria de valores extremos: gap normalizado mínimo entre `N`
zeros escala como `N^(-1/3)` (GUE) ou `N^(-1)` (Poisson)? Resultado sobre
`zeros1.txt` (100k zeros): `β̂=-0,3395`, quase exatamente `-1/3=-0,3333`,
IC 95% bootstrap `[-0,3872;-0,2868]` — contém GUE folgadamente, exclui
Poisson e GOE (`-1/2`) com folga grande. `evidence_level:
preregistered_confirmed`, `adversarial_review_verdict: CONFIRMED`
(reprodução bit a bit por agente independente, três métodos de ajuste
concordantes). Gate de Replicação completo acionado sobre `zeros5.txt`
(regime #10²², nunca antes baixado): **`REPLICATION_FAILED` por falta de
poder estatístico**, não por contradição — o dataset reservado só tem
9.999 gaps, insuficiente para a grade travada (0 blocos possíveis em
N=10.000; só N=500/N=1.000 atingem a barra de ≥8 blocos declarada no
pré-registro, e restritos a esses dois pontos o IC vira
não-informativo). O achado primário sobre `zeros1.txt` permanece de pé,
apenas não pôde ser confirmado de forma independente numa terceira altura
com esta fonte específica. `promoted_to_formal_lab: false` — confirmação
numérica de universalidade GUE já conhecida na literatura, não descoberta
matemática nova. Lição de governança documentada em
`03_REPLICATION_GATE/PROTOCOL.md`: verificar A PRIORI que uma fonte
reservada tem amostra suficiente para a grade já travada, não apenas que
existe em regime diferente. Ver
`09_SESSIONS/2026/2026-08-12_RH_GAP_EXTREME_VALUE_SCALING.md` para o
relato completo.

Não há mais fonte adicional de Odlyzko disponível no regime #10²² para
resolver a falta de poder do sub-teste 2 sem consumir dado já usado.

## Resultado da Fase 0 de `DISC-TRI-RG-001` (2026-08-14)

5 candidatos de par `(R_lambda, I(X))` avaliados em paralelo por agentes
de pesquisa independentes, cada um obrigado a verificar dado real (baixar/
inspecionar, não só citar) antes de declarar um domínio utilizável. Relato
completo em `02_TESTS/TRI_RG/phase0/PHASE0_SURVEY.md`.

**3/5 `viable: true`**, ranqueados por uma síntese adversarial que aplicou
a mesma régua a todos: (1) **critical-slowing-down** — variância/
autocorrelação lag-1 crescentes perto de bifurcação (Scheffer 2009, Dakos
2008/2012, Lenton 2012); 3 domínios com transição REAL dentro do mesmo
sistema no tempo, dado verificado (GISP2/Younger Dryas, PhysioNet SDDB/
onset de fibrilação ventricular, NASDAQ/crash pontocom); modelo
concorrente nomeado real (B-tipping vs. R/N-tipping, Ashwin 2012); ainda
faltam regra de `lambda` cross-domain, protocolo de nulo substituto, e o
cálculo real de `Delta I` (só o acesso ao dado foi verificado). (2)
**wavelet-multiresolution-scaling** — `R_lambda` mais rigoroso
matematicamente dos 5 (`R_2λ=R_λ'∘R_λ` por construção via subespaços
aninhados), mas só 1 domínio robusto (sismologia, mainshock de Tohoku
2011, rótulo USGS/GCMT externo). (3) **dfa-multiscale-entropy** —
execução empírica mais sólida (DFA implementado do zero, validado contra
nulos teóricos, rodado sobre dado PhysioNet real decodificado E sobre os
gaps de zeta já usados em `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`), mas
os 2 domínios usados são comparações ESTÁTICAS de classe (saudável vs.
insuficiência cardíaca; continental vs. oceânico), não transições
temporais — mesmo defeito que corretamente derrubou o candidato (4)
abaixo, só detectado na síntese cross-candidato.

**2/5 `viable: false`**, corretamente rejeitados pelos próprios agentes:
(4) **box-covering-network-renorm** (Song-Havlin-Makse) — `R_lambda` mais
literal de todos, dado real de 4 redes verificado (SNAP/CAIDA), mas toda
"transição" fractal↔não-fractal na literatura vem de modelos sintéticos
com parâmetro artificial; dado real só mostra classificação estática, e
essa classificação está sob disputa ativa em 2025. (5)
**spacing-statistics-rmt-non-zeta** — dado real e computação real
executados (níveis nucleares RIPL-3, autovalores de rede SNAP), mas falha
em identificabilidade (previsão idêntica ao consenso BGS/RMT de 40 anos)
e em RG/EFT (nenhum `R_lambda` genuíno implementado).

**Nenhum candidato foi travado.** Decisão de qual (ou quais) perseguir
fica com o usuário.

## Fechamento dos 3 gaps de `critical-slowing-down` (2026-08-14) — resultado NEGATIVO

A pedido do usuário, os 3 gaps concretos do candidato `critical-slowing-
down` (rank 1 na Fase 0) foram fechados: (a) regra de `lambda`
cross-domain — todos os parâmetros de escala expressos como frações fixas
do comprimento do segmento (convenção Dakos et al. 2012), a mesma em
todo domínio; (b) protocolo de teste contra nulo substituto — AR(1) de
parâmetro constante, 1000 substitutos, teste unicaudal (Dakos et al. 2008
*PNAS*); (c) `Delta I` calculado de fato nos 3 domínios já verificados
(GISP2, PhysioNet SDDB, NASDAQ). Metodologia fixada e commitada (commit
`b43fde0`) ANTES de qualquer cálculo real; pipeline única
(`csd_common.py`) validada contra dado sintético primeiro (caso nulo:
sem tendência; caso com CSD injetado: `τ=1,000`, detectado), depois
chamada sem modificação por 3 agentes independentes.

**Resultado: NEGATIVO.** Das 12 combinações testadas (3 domínios × 2
variantes de janela × 2 canais — AC1 e variância), apenas 1 cruzou
`p<0,05` (GISP2, variante de 50% mais recente, canal AC1: `τ=0,848`,
`p=0,032`) — estatisticamente consistente com ruído puro sob 12
comparações múltiplas sem correção (esperado ~0,6 falsos positivos ao
acaso). Mais grave: em 2 dos 3 domínios (PhysioNet SDDB, NASDAQ variante
primária), o canal de AC1 mostrou tendência FORTEMENTE NEGATIVA
(`τ=-0,82`, `τ=-0,95`, `τ=-0,37`) — direção OPOSTA à prevista por CSD,
não apenas ausência de sinal. `critical-slowing-down`, formulado com uma
regra de `lambda` genuinamente cega ao domínio (exigência central de
`DISC-TRI-RG-001`), não produz um invariante cross-domain confiável
nestes 3 domínios/transições. Achado negativo honesto, catalogado com o
mesmo peso que um resultado positivo teria — não invalida CSD como
fenômeno geral na literatura (que usa janelas informadas por
conhecimento específico de cada sistema, não uma regra cega), apenas
mostra que esta instanciação específica cross-domain não sobrevive.
Nenhum `PREREGISTRATION.md` foi escrito — o próprio passo de fechamento
de gaps evitou travar um pré-registro fadado ao fracasso. Detalhes
completos em `02_TESTS/TRI_RG/critical_slowing_down/RESULTS_SUMMARY.md`.

## Busca de segundo domínio para `wavelet-multiresolution-scaling` (2026-08-14)

Com `critical-slowing-down` descartado, usuário pediu para buscar um
segundo domínio robusto para `wavelet-multiresolution-scaling` (que
tinha só sismologia/Tohoku 2011 na Fase 0). Três agentes investigaram em
paralelo três candidatos — relato completo em
`02_TESTS/TRI_RG/wavelet_multiresolution/SECOND_DOMAIN_SEARCH.md`.

**Recomendado: EEG de crise epiléptica (CHB-MIT, PhysioNet).** Banco
aberto (sem login), registro real de 42,4 MB baixado e parseado byte a
byte com parser EDF escrito do zero, rótulo de transição clínico
(onset/offset de crise em segundos, dentro do mesmo registro contínuo do
paciente) — mesma estrutura de rótulo já validada em sismologia e no
domínio cardíaco de `critical-slowing-down`. Ressalvas: só 1 crise/1
paciente verificada (182 crises/22 pacientes disponíveis para
replicação futura); EEG de escalpo é mais suscetível a artefato que
ECG/sismômetro.

**Domínio de apoio válido: turbulência de plasma no vento solar** (NASA
OMNI + catálogo independente CfA de choques interplanetários) —
transição real confirmada numericamente (velocidade do vento solar
400→729 km/s, `|B|` 7,7→30,5 nT no choque de 2024-10-10), mas domínio
FISICAMENTE DIFERENTE do WTMM hidrodinâmico histórico (que continua sem
fonte livremente acessível encontrada — lacuna honesta reconfirmada).

**Descartado: MAWI/MAWILab** — dado real verificado, rótulo genuíno para
fluxos isolados, mas falha estrutural (só captura amostras diárias de 15
min, nunca contínuas — eventos pequenos ficam invisíveis no agregado,
eventos grandes preenchem a janela toda sem baseline); também
descontinuado pelos mantenedores em dezembro/2024.

## Fechamento dos gaps de `wavelet-multiresolution-scaling` (2026-08-14) — resultado NEGATIVO

A pedido do usuário, os gaps restantes (regra de janela, cálculo real do
método, protocolo de substitutos) foram fechados nos 2 domínios acima.
Metodologia fixada e commitada (commit `6da7112`) ANTES de qualquer
cálculo real: `WTMM`/wavelet-leader completo substituído honestamente
por log-cumulantes de coeficientes wavelet (WCM — Castaing/Gagne/
Hopfinger 1990, Delbeke/Abry 2000, Wendt/Abry/Jaffard 2007), por
tratabilidade computacional; `R_lambda` continua a mesma projeção
multirresolução wavelet. Pipeline validada contra controle sintético
multifractal (ruído gaussiano modulado por cascata log-normal) antes de
tocar dado real.

**EEG (CHB-MIT, chb01_03):** variante primária com significância nominal
(`p=0,040` ΔC2; `p=0,015` ΔC1) desaparece por completo quando o PRE é
truncado ao mesmo tamanho do POST (`p=0,290`; `p=0,900`, ΔC1 chega a
inverter de sinal) — frágil, dependente do desenho do teste.

**Sismologia (Tohoku 2011, IU.ANMO/BHZ):** achado inicial muito
significativo (`ΔC2=+0,356 p=0,005`; `ΔC1=+0,942 p=0,000`) acionou
checagem adversarial completa. Hipótese de saturação/clipping do
sismômetro REJEITADA (pico usa só 31,3% da escala de 24 bits, sem
assinatura de clipping, sem relatos documentados para ANMO/GSN durante
Tohoku 2011). Mas o achado NÃO sobrevive a um truncamento genuíno
(`N=16.384`: `ΔC2` dispara para 2,30 mas é diagnosticado como artefato
de estimador de amostra pequena; `ΔC1` perde significância,
`p=0,595`) nem a aparar apenas 1% das amostras mais extremas do POST
(`ΔC2` inverte de sinal e perde toda significância, `p=0,990`) —
consistente com a limitação do próprio IAAFT sob marginais de cauda
pesada já documentada na validação sintética desta metodologia.

**Veredito: NEGATIVO nos 2 domínios.** Nenhuma variante tem `ΔC2` E
`ΔC1` simultaneamente significativos e estáveis.
`wavelet-multiresolution-scaling`, como `critical-slowing-down` antes
dele, não produz um invariante cross-domain confiável testado com
protocolo genuinamente cego ao domínio e checagem adversarial completa.
Nenhum `PREREGISTRATION.md` foi escrito. Detalhes completos em
`02_TESTS/TRI_RG/wavelet_multiresolution/RESULTS_SUMMARY.md`.

## Retomada de `DISC-TRI-RG-001` e fechamento dos gaps de `dfa-multiscale-entropy` (2026-08-14) — resultado NEGATIVO

Usuário pediu explicitamente para retomar a linha após a pausa
(`DISC-DEC-005`). Um agente de busca dedicado encontrou um domínio
fisiológico com transição temporal GENUÍNA (corrigindo o defeito da Fase
0, que usava comparações estáticas de classe): PhysioNet Apnea-ECG
Database, registro `a04` (AHI=77,4, apneia severa), 35 min de sono normal
seguidos imediatamente por 140 min contínuos de apneia dentro do mesmo
paciente/registro, rótulo clínico externo (Thomas Penzel). Segundo
domínio cross-domain: paleoclima GISP2, reaproveitado de
`critical-slowing-down` (mesma transição Younger Dryas→Preboreal).

Pipeline DFA-1 nova (`dfa_common.py`) validada contra dado sintético
ANTES de qualquer dado real — a validação revelou que o teste IAAFT
bicaudal originalmente especificado na metodologia tem baixo poder para
`alpha` (substitutos preservam o espectro linear, que é essencialmente o
que `alpha` mede: o controle positivo sintético, H=0,5→H=0,9, não atingiu
`p<0,05`). Corrigido ANTES de tocar dado real: adicionado um teste
complementar de bootstrap por blocos móveis (Künsch 1989), que passou a
ser o teste PRIMÁRIO de significância — mesma disciplina de
`METHODOLOGY_EXTENSIONS.md` Seção 1 (verificar comportamento da
estatística contra nulo/sintético antes de gastar tempo em dado real).

**Resultado: NEGATIVO cross-domain.** Apneia-ECG mostrou sinal forte nos
6 testes de bootstrap (`p<0,05`, maioria `p<0,001`), que sobreviveu à
reexecução adversarial cega (extração independente de RR bate ~byte a
byte) e à winsorização (não é artefato de outlier) — mas a descoberta
adversarial de nulos identificou um mecanismo fisiológico já conhecido há
40 anos (CVHR — Cyclical Variation of Heart Rate, Guilleminault et al.
1984) que explica o efeito por completo, batendo exatamente com o AHI
documentado do paciente. GISP2 não replicou o sinal (5 dos 6 testes de
bootstrap não significativos). `dfa-multiscale-entropy`, como os outros 2
candidatos antes dele, não produz um invariante cross-domain confiável.
Detalhes completos em
`02_TESTS/TRI_RG/dfa_multiscale_entropy/RESULTS_SUMMARY.md`.

**Estado final da linha:** os 3 candidatos viáveis da Fase 0
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`) testados com rigor completo — metodologia
pré-commitada, pipeline validada contra dado sintético, checagem
adversarial completa onde o efeito justificou — os 3 resultado NEGATIVO
para invariante cross-domain. Nenhum `PREREGISTRATION.md` foi escrito em
nenhum dos 3. Toda a infraestrutura (3 pipelines validadas, 9
domínios/variantes testados no total) fica commitada e reaproveitável.

## Revisita com registros de backup do Apnea-ECG (2026-08-15)

Usuário pediu para revisitar os candidatos com os registros de backup do
Apnea-ECG mapeados na busca de `dfa-multiscale-entropy` (`a18`, `a14`,
`a01`). Questionado sobre escopo, optou por tratar o banco como um
domínio fisiológico NOVO para os 3 candidatos (não só replicação de DFA).
3 agentes independentes baixaram os 3 registros e rodaram as 3 pipelines
já validadas sem modificação. Detalhes completos em
`02_TESTS/TRI_RG/APNEA_BACKUP_RECORDS_REVISIT.md`.

**Não resolve a exigência cross-domain** (os 3 registros são do MESMO
domínio já testado em `a04`). CSD: sem sinal em nenhum registro (mesmo
padrão de ausência já visto em todos os outros domínios). Wavelet
(primeira aplicação a apneia-ECG): `ΔC1` mostra padrão direcionalmente
consistente, mas é exatamente o canal que a própria linha já suspeitava
refletir amplitude, não estrutura multifractal genuína; `ΔC2` instável.
DFA: a direção de `Δalpha`/`Δalpha2` (queda) **replica nos 4 registros de
apneia** (`a18` é o mais fraco); `Δalpha1` (o canal mais dramático em
`a04`) é o menos replicável. Fortalece a leitura já registrada — efeito
fisiológico real que generaliza parcialmente entre pacientes, mas
continua sendo a mesma explicação mundana já identificada (CVHR). Checagem
adversarial adicional não foi acionada para os registros de backup
(efeitos mais modestos que o achado original, custo alto vs. valor
marginal baixo, declarado explicitamente).

## Nova rodada de busca de candidatos para `DISC-TRI-RG-001` (2026-08-15)

Após `DISC-DEC-006` (segunda pausa), usuário pediu a única rota de
retomada ainda não exercida: nova busca por candidatos ainda não
considerados. 5 agentes independentes em paralelo investigaram 6
candidatos genuinamente novos (não variações dos 5 originais). Detalhes
completos em `02_TESTS/TRI_RG/phase0/PHASE0_5_SURVEY_NEW_CANDIDATES.md`.

**4 `viable=true`:** (1) **Entropia Multiescala (MSE)** — fundamentação
formal de `R_lambda` mais rigorosa já considerada nesta linha (conexão
direta com o Teorema Central do Limite via Jona-Lasinio 2001), 2 domínios
novos verificados (tempestade geomagnética 1989, rolamento FEMTO/PRONOSTIA
até falha), mas risco real de redundância com a família Hurst já testada
(DFA/wavelet). (2) **Expoentes de criticalidade auto-organizada (SOC)** —
matemática genuinamente distinta dos 3 já testados, 2 domínios novos
(sismicidade Ridgecrest 2019, flares solares GOES/NOAA), sem risco de
redundância identificado, mecanismos mundanos já mapeados e corrigíveis.
(3) **Grafo de visibilidade + box-covering** — reaproveita box-covering já
verificado (nunca implementado em código na Fase 0 original), 2 domínios
novos (geomagnetismo 2015, furacão Harvey), mas risco de redundância com
Hurst documentado DIRETAMENTE na literatura (Xie & Zhou 2011). (4) **RQA
(Recurrence Quantification Analysis)** — único candidato com regras de
parâmetro NÃO-arbitrárias publicadas, mas sondagem exploratória própria já
mostrou o MESMO padrão de inconsistência cross-domain que derrubou
`critical-slowing-down`.

**2 `viable=false`, corretamente rejeitados com justificativa concreta:**
percolação sob ataque a hubs (nenhum evento real tem simultaneamente
fragmentação genuína E reconstrução publicada de `S(f)`); escala de
Anderson (nenhuma generalização real se liberta de transporte de onda
quântico).

**Ranking honesto, não travado:** SOC > MSE > grafo de visibilidade > RQA.
Nenhum candidato foi travado — decisão de qual perseguir (se algum) fica
com o usuário.

## Fechamento de gaps de `soc-avalanches` (2026-08-15) — resultado NEGATIVO

Candidato ranqueado #1 na nova rodada de busca. Metodologia (binagem por
intervalo médio entre eventos, `I(X)`=`tau` via MLE + `sigma`, substituto
Poisson + bootstrap pareado após validação sintética revelar perda de
poder do Poisson sob desequilíbrio de taxa) fixada e pipeline validada
ANTES de qualquer dado real. Detalhes completos em
`02_TESTS/TRI_RG/soc_avalanches/RESULTS_SUMMARY.md`.

**Ridgecrest 2019 (sismicidade):** achado inicial na variante de robustez
(`p_bootstrap_tau=0,0`) acionou a escalada condicional já pré-declarada
(nulo ETAS subcrítico) — resultado `p_ETAS_tau=0,273`, NÃO significativo.
Descoberta adversarial de nulos reproduziu o mesmo "efeito" dividindo
apenas a janela POST (sem nenhuma transição envolvida) — decaimento
clássico de Omori-Utsu, não SOC/invariante novo. **Flares solares GOES:**
sem sinal em nenhuma variante, direção instável.

**Estado da linha:** 4 candidatos agora testados com rigor completo
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`, `soc-avalanches`) — os 4 NEGATIVO. Restam 3
candidatos da nova busca não fechados (MSE, grafo de visibilidade, RQA).

## Fechamento de gaps de `mse-multiscale-entropy` (2026-08-15) — resultado NEGATIVO

Candidato ranqueado #2 na nova rodada de busca. Validação sintética
confirmou o discriminador de identificabilidade central desta linha: ao
contrário de `alpha`/DFA, o IAAFT TEM poder real para `CI`/`beta`
(controle positivo com `p=0,0`), o que já resolve substancialmente o
risco de redundância com Hurst identificado na Fase 0.5. Detalhes
completos em `02_TESTS/TRI_RG/mse_multiscale_entropy/RESULTS_SUMMARY.md`.

**Resultado real:** sem sinal em nenhuma das 8 combinações testadas (2
domínios × 2 variantes × 2 canais) — geomagnetismo (SYM-H, tempestade de
março/1989) e rolamento (FEMTO/PRONOSTIA `Bearing1_1`, run-to-failure)
ambos completamente negativos. Nenhuma reexecução adversarial completa
foi acionada (proporcional — sem achado significativo a explicar, ao
contrário de DFA/apneia-ECG e SOC/Ridgecrest). Desvio metodológico
honesto no domínio de rolamento: PRE decimado por stride (fator 200) por
inviabilidade computacional, risco de ter atenuado sinal fino não
descartado.

**Estado da linha:** 5 candidatos agora testados com rigor completo
(`critical-slowing-down`, `wavelet-multiresolution-scaling`,
`dfa-multiscale-entropy`, `soc-avalanches`, `mse-multiscale-entropy`) —
os 5 NEGATIVO. Resta 1 candidato da nova busca não fechado (grafo de
visibilidade; RQA também não fechado).

## Fechamento de gaps de `grafo-de-visibilidade` (2026-08-18) — resultado NEGATIVO

Usuário pediu para retomar `DISC-TRI-RG-001`; escolhido o candidato
ranqueado #3 na busca de 2026-08-15 (grafo de visibilidade natural,
Lacasa et al. 2008, + box-covering, Song-Havlin-Makse 2005). Metodologia
fixada em `02_TESTS/TRI_RG/visibility_graph/METHODOLOGY_NOTE.md` ANTES
de qualquer cálculo real.

**Achado decisivo da validação sintética obrigatória:** `d_B` (dimensão
fractal de box-covering, canal primário originalmente declarado) é
ESTRUTURALMENTE NÃO COMPUTÁVEL para séries temporais estocásticas —
grafos de visibilidade são "small-world" (diâmetro cresce só como
`~log(N)`, medido entre 9 e 19 para `N` de 1.000 a 15.000), nunca
atingindo o piso de 20 exigido pela própria grade a priori, mesmo no
teto de 5.000 amostras já declarado. Não é bug (diagnóstico com série
determinística confirma o código correto) nem falta de poder estatístico
(bootstrap por blocos móveis testado e não resolve — 25/25 reamostras
continuam insuficientes). Decisão, fixada ANTES de dado real, honrando a
própria regra de rejeição já pré-declarada em vez de afrouxá-la: `d_B`
retirado do critério; `C` (clustering, canal companheiro) promovido a
`I(X)` único — validado com poder real forte (~14,55 desvios-padrão no
controle positivo sintético).

**Resultado real** (geomagnetismo — SYM-H, tempestade 17/03/2015, NASA
OMNI; hidrologia — régua, furacão Harvey, USGS 08074500, pico real
confirmado 44,31 pés): NEGATIVO limpo nas 4 combinações
(2 domínios × 2 variantes), `p_C` entre 0,595 e 0,995, sem consistência
direcional entre domínios. `d_B` não-computável nos 4 casos reais,
confirmando a previsão da validação. Reexecução adversarial NÃO
acionada por proporcionalidade (nada significativo a explicar, mesmo
princípio já usado em MSE). Detalhes completos:
`02_TESTS/TRI_RG/visibility_graph/RESULTS_SUMMARY.md`.

**Estado da linha:** 6 dos 7 candidatos identificados (3 da Fase 0
original + 4 da nova busca) agora têm resultado completo — os 6
NEGATIVO. Resta apenas 1 candidato formalizado não fechado: RQA (rank #4
— sondagem exploratória já mostrou o mesmo padrão de inconsistência
cross-domain que derrubou `critical-slowing-down`).

## Fechamento de gaps de `RQA` (2026-08-18) — fechado NA VALIDAÇÃO, dado real nunca tocado

Usuário pediu para fechar também o RQA — último candidato identificado
nesta linha (7 de 7 no total). Metodologia fixada em
`02_TESTS/TRI_RG/rqa/METHODOLOGY_NOTE.md` ANTES de qualquer cálculo real:
regras de parâmetro não-arbitrárias e publicadas (FNN para `m`,
informação mútua para `tau`, taxa de recorrência fixa para `epsilon`),
embedding compartilhado PRE/POST, `I(X)=%DET+ENTR`, IAAFT primário.

**Validação sintética, tentativa 1** (PRE=ruído branco, conforme
especificado): achado estrutural mais severo que o de
`grafo-de-visibilidade` — FNN nunca resolve `m<=10` para ruído branco
(nem AR(1) até `phi=0,9`, só a partir de `phi=0,95` ou `H(fGn)>=0,3`),
bloqueando `%DET` E `ENTR` simultaneamente (compartilham o mesmo passo de
embedding). Não é bug (diagnóstico determinístico confirma código
correto) nem falta de poder (bootstrap testado, 0/25 resolve).

**Correção de desenho, fixada ANTES de dado real, com protocolo de
decisão mecânico pré-declarado (nenhuma terceira tentativa autorizada):**
trocar a fonte caótica de POST do mapa logístico (espectro banda-larga,
causa de um descasamento espectral que confundiu uma tentativa informal
anterior) para o sistema de Rössler (espectro colorido, compatível com o
PRE `fGn H=0,7` já validado).

**Validação, tentativa 2 (Rössler):** embedding resolveu (`m=4, tau=40`),
bom casamento espectral — mas `p_DET=1,0`, `p_ENTR=1,0`, sem poder real
em nenhum canal. Aplicando o protocolo pré-fixado mecanicamente:
candidato **fechado na própria etapa de validação** — o dado real
(rolamento IMS/Rexnord, vulcão Kīlauea 2018) nunca foi tocado. Resultado
honesto e completo, distinto de "negativo no dado real" mas igualmente
definitivo para os propósitos desta linha. Detalhes completos:
`02_TESTS/TRI_RG/rqa/RESULTS_SUMMARY.md`.

## Estado final da linha `DISC-TRI-RG-001` — 7 de 7 candidatos identificados com resultado completo

| Candidato | Domínios testados | Resultado |
|---|---|---|
| `critical-slowing-down` | GISP2, PhysioNet SDDB, NASDAQ | NEGATIVO |
| `wavelet-multiresolution-scaling` | Sismologia/Tohoku, EEG/CHB-MIT | NEGATIVO |
| `dfa-multiscale-entropy` | Apneia-ECG (4 registros), GISP2 | NEGATIVO (achado de 1 domínio explicado por mecanismo mundano) |
| `soc-avalanches` | Ridgecrest, flares solares GOES | NEGATIVO (achado de 1 domínio refutado por nulo ETAS) |
| `mse-multiscale-entropy` | Geomagnetismo (1989), rolamento FEMTO | NEGATIVO (sem achado em nenhum domínio) |
| `grafo-de-visibilidade` | Geomagnetismo (2015), hidrologia/Harvey | NEGATIVO (sem achado em nenhum domínio) |
| `RQA` | — (fechado na validação) | FECHADO NA VALIDAÇÃO (identificabilidade não estabelecida; dado real nunca tocado) |

Nenhum candidato produziu um invariante cross-domain confiável. Isso é um
prior forte e honesto contra a hipótese central desta linha tal como
formulada até aqui (um par `R_lambda`/`I(X)` genuinamente cego ao
domínio, aplicado sem reformulação, prevendo transições em domínios
físicos diferentes) — não uma prova de impossibilidade. Toda a
infraestrutura (7 `METHODOLOGY_NOTE.md`, 6 pipelines validadas e
aplicadas a dado real, domínios reais de 14+ fontes testadas no total)
fica commitada e reaproveitável.

## Fase 0.6 — nova busca de candidatos (2026-08-18)

Usuário pediu nova rodada de busca. 5 agentes independentes em paralelo
investigaram 5 candidatos genuinamente novos (nenhuma reformulação leve
dos 7 já testados), cada um com instrução de verificar dado real e
avaliar risco de identificabilidade contra todos os 7 candidatos já
fechados. **Resultado: 4 `viable=true`, 1 `viable=false`.**

1. **Entropia de permutação + plano complexidade-entropia** (Bandt-Pompe/
   Rosso) — melhores regras de parâmetro não-arbitrárias desta rodada
   (`m∈{3..7}`, `N>=5·m!`, `tau` via informação mútua), 2 domínios novos
   fortes (VitalDB indução de anestesia, PhysioNet European ST-T
   isquemia). `H_S` sozinho tem risco documentado de redundância com
   Hurst (Zunino et al. 2008); `C_JS` (complexidade de Jensen-Shannon) é
   o discriminador proposto, nunca testado na literatura contra IAAFT.
2. **Kramers-Moyal / Friedrich-Peinke** (reconstrução de Fokker-Planck)
   — regra de seleção de `lambda` mais principiada de toda a linha até
   agora (teste de Markov-Einstein/Chapman-Kolmogorov orientado a dado,
   não janela escolhida), 2 domínios novos (choque do SNB EUR/CHF
   tick-a-tick; `vfdb` com ~10 transições N→VFL→N dentro do mesmo
   registro). Risco de redundância com `critical_slowing_down`
   confirmado analiticamente (Ritchie & Sieber 2016), mas canal de
   escape real e citado (forma global do potencial, Livina & Lenton
   2007/2010).
3. **Homologia persistente / TDA** — matemática mais distinta de todas
   (topologia algébrica), domínio inédito genuinamente novo (deformação
   de onda gravitacional LIGO GW150914). Único candidato com checagem
   EMPÍRICA própria de redundância já rodada nesta sessão: correlação
   r≈0,92 entre persistência máxima de H1 e o `%DET` do RQA (que nem
   chegou a tocar dado real) no regime mais relevante para detectar
   transição. Custo computacional real força janelas pequenas.
4. **Índice de cauda EVT/Hill estimator** — bem fundamentado (seleção de
   limiar automatizada, Danielsson et al. 2001; Bader, Yan & Zhang
   2018), 2 domínios novos (onda de calor 2021 Pacífico Noroeste;
   furacão Florence/Rio Cape Fear, gauge diferente do Harvey). Risco de
   redundância com SOC via princípio do "grande salto único" — real,
   parcialmente mitigado, barato de checar cedo.
5. **RG de block-spin literal sobre série binarizada** — `viable: false`,
   fechado por identificabilidade ANALÍTICA (a decimação de Ising 1D
   força fluxo trivial para qualquer processo de correlação de curto
   alcance; quando tem poder discriminativo, colapsa numa versão mais
   ruidosa do Hurst já testado 2x negativo) — sem tocar dado real, mesmo
   espírito de `spacing-statistics-rmt-non-zeta` na Fase 0 original.

Nenhum candidato foi travado. Ranking honesto (não travado): permutação+
CECP > Kramers-Moyal > TDA > EVT/Hill. Detalhes completos:
`02_TESTS/TRI_RG/phase0/PHASE0_6_SURVEY_NEW_CANDIDATES.md`.

## Fechamento de gaps de `entropia-de-permutacao` (2026-08-18) — resultado NEGATIVO

Usuário pediu para fechar o candidato ranqueado #1 na Fase 0.6.
Metodologia (coarse-graining reaproveitado de MSE + embedding ordinal
Bandt-Pompe, `m=4` fixo; `I(X)=H_S`/`PCI`+`C_JS`/`MCI`) fixada em
`02_TESTS/TRI_RG/permutation_entropy/METHODOLOGY_NOTE.md` ANTES de
qualquer cálculo real.

**Validação sintética — o resultado mais limpo desta linha até agora:**
ao contrário da hipótese a priori (`C_JS` teria poder, `H_S` talvez não,
como `alpha` do DFA), **os DOIS canais mostraram poder real completo**
contra o controle positivo IAAFT (mapa logístico: `p_PCI=0,0`,
`p_MCI=0,0`, ambos com separação de ~10-12 desvios-padrão da nula). Um
controle adicional de Hurst diferencial (`H=0,3` vs. `H=0,9`, sem
conteúdo não-linear, pedido pela sessão orquestradora para testar
diretamente o risco de identificabilidade já nomeado — Zunino et al.
2008) confirmou que nenhum canal mostra significância espúria por mero
desvio linear de Hurst (`p=1,0` em ambos) — o risco foi resolvido ANTES
de tocar dado real, não descoberto depois.

**Resultado real** (VitalDB, indução de anestesia via EEG; PhysioNet
European ST-T, episódio isquêmico transitório): **sem sinal
significativo nas 8 combinações** (2 domínios × 2 variantes × 2 canais).
A variante primária do domínio isquêmico teve os `p` mais baixos da
linha inteira (`p_PCI=0,275`, `p_MCI=0,325`, direção qualitativamente
intuitiva para isquemia) mas não cruzou `p<0,05` e não se reproduziu na
variante de robustez — reportado honestamente como tendência sub-limiar,
não achado. Durante a etapa de dado real, um bug de desempenho real foi
encontrado e corrigido (subamostragem do Gap (d) não aplicada antes da
geração de substitutos IAAFT), com revalidação sintética confirmada
bit-idêntica após a correção. Reexecução adversarial completa não
acionada por proporcionalidade (nada significativo a explicar).

**Veredito honesto:** negativo, mas não por falta de poder do teste — é
o único candidato desta linha cuja validação sintética confirmou poder
completo em AMBOS os canais declarados, tornando este o resultado
negativo mais confiável (menos ambíguo) já obtido nesta linha. Detalhes
completos: `02_TESTS/TRI_RG/permutation_entropy/RESULTS_SUMMARY.md`.

**Estado da linha:** 8 dos 8 candidatos fechados até agora (7 da linha
original + este) sem invariante cross-domain sobrevivente. Restam 3
candidatos formalizados da Fase 0.6 ainda não fechados: Kramers-Moyal/
Friedrich-Peinke (rank #2), homologia persistente/TDA (rank #3), índice
de cauda EVT/Hill (rank #4).

## Fechamento de gaps de `kramers-moyal` (2026-08-19) — sem veredito computável, dois motivos estruturais honestos

Usuário pediu para fechar o candidato ranqueado #2 na Fase 0.6.
Metodologia (teste de Markov-Einstein/Chapman-Kolmogorov para `tau_ME`;
`I(X)=PKS`, curtose de forma do potencial reconstruído) fixada em
`02_TESTS/TRI_RG/kramers_moyal/METHODOLOGY_NOTE.md` ANTES de qualquer
cálculo real — incluindo uma decisão a priori incomum: `kappa`
(taxa de decaimento local) foi demovido a diagnóstico-apenas DESDE O
INÍCIO, com base numa prova algébrica publicada (Ritchie & Sieber 2016,
não uma correlação empírica) de que é identidade exata com a mesma
grandeza que `critical_slowing_down` já testou e refutou.

**Validação sintética:** `PKS` (canal primário) confirmado com poder
real e limpo (`p=0,005` no controle positivo de SDE biestável, `p=0,23`
no negativo). `beta_D2` (companheiro) não mostrou poder detectável em
nenhuma das duas variantes pré-autorizadas nem sob o fallback de
bootstrap — demovido também a diagnóstico por decisão da sessão
orquestradora (adendo, commit `9d35eeb`), ANTES de qualquer dado real.

**Resultado real, dois motivos estruturais distintos, nenhum deles
problema de poder do IAAFT:**
- **PhysioNet `vfdb`** (arritmia ventricular maligna, registro 418):
  propriedade de Markov NUNCA estabelecida — o teste de CK rejeita
  fortemente em quase todos os lags curtos testados, resultado
  teoricamente esperado para amplitude bruta de ECG sem informação de
  fase cardíaca. `tau_ME` não encontrado, `PKS` não computado.
- **EUR/CHF** (choque do SNB, 15/01/2015, confirmado empiricamente:
  preço caiu de 1,200975 para 1,020855 em 5min): `tau_ME` estabelecido
  normalmente no PRE, mas `PKS` fica ESTRUTURALMENTE INDEFINIDO no
  POST — o choque (~15% num dia) é grande demais para os 10 bins de
  quantil fixados do PRE resolverem o POST (~50% de todo o POST cai
  num único bin), consequência honesta da própria regra "bins fixados
  do PRE" (travada precisamente para evitar reestimação ad hoc)
  colidindo com um choque de magnitude extrema.

Reexecução adversarial não acionada (nenhum achado positivo computável
a explicar). Uma nota metodológica para tentativas futuras (bins sobre
a união PRE+POST, ou normalização por log-retorno) foi registrada, não
implementada. Detalhes completos:
`02_TESTS/TRI_RG/kramers_moyal/RESULTS_SUMMARY.md`.

**Estado da linha:** 9 dos 9 candidatos fechados até agora sem
invariante cross-domain sobrevivente. Restam 2 candidatos formalizados
da Fase 0.6 ainda não fechados: homologia persistente/TDA (rank #3),
índice de cauda EVT/Hill (rank #4).

## Fechamento de gaps de `evt-hill` (2026-08-19) — negativo/não testável

Usuário pediu para fechar o último candidato formalizado da Fase 0.6.
Metodologia fixada em `02_TESTS/TRI_RG/evt_hill/METHODOLOGY_NOTE.md`
ANTES de qualquer cálculo real, com um desvio deliberado da convenção
padrão desta linha: o protocolo de significância NÃO usa IAAFT (que
preserva a marginal exata por construção, tornando a nula degenerada
para um estimador puramente baseado em estatísticas de ordem como
Hill) — usa em vez disso um teste de randomização do ponto de corte.
`I(X)=xi_Hill` (primário, limiar REESTIMADO por segmento, não fixado do
PRE) + `xi_MLE` (companheiro, GPD/MLE).

**Validação sintética:** `xi_Hill` correto contra distribuições de
cauda conhecida; poder real do teste de randomização confirmado para
PRE/POST desbalanceado (o caso realista). Checagem obrigatória de
redundância com SOC (reaproveitando dado já commitado) ficou
inconclusiva por poder estatístico (`n=3`), levemente contra
redundância simples.

**Resultado real:** PDX (onda de calor 2021, NOAA GHCN-Daily)
ESTRUTURALMENTE NÃO TESTÁVEL — piso de amostra não atingido (POST=37
dias, resolução diária vs. janela de "semanas" exigida para evitar
circularidade). Cape Fear (furacão Florence 2018, USGS 02105769):
canal primário `xi_Hill` sem significância em nenhuma variante
(`p=0,185`/`0,22`); canal companheiro `xi_MLE` significativo só na
variante de robustez (`p=0,025`), investigado a fundo e explicado por
um platô de crista de cheia físico real e limitado (suporte GPD
finito, não cauda mais pesada), não um achado cross-domain genuíno.
Checagem de confundidor de comporta (Lock 1, gatilho pré-declarado)
acionada — evidência circunstancial pesa contra o confundidor
(estrutura submersa no pico). Detalhes completos:
`02_TESTS/TRI_RG/evt_hill/RESULTS_SUMMARY.md`.

**Estado da linha:** 10 dos 11 candidatos identificados fechados sem
invariante cross-domain sobrevivente. Resta apenas 1 candidato
formalizado não fechado: homologia persistente/TDA (rank #3).

## Fechamento de gaps de `homologia-persistente` (2026-08-20) — fechado NA VALIDAÇÃO, Fase 0.6 completa

Usuário pediu para fechar o último candidato formalizado da Fase 0.6
(rank #3, TDA via filtração de Vietoris-Rips sobre embedding de
Takens). Metodologia fixada em
`02_TESTS/TRI_RG/persistent_homology/METHODOLOGY_NOTE.md` ANTES de
qualquer cálculo real: embedding `m=3` FIXO (deliberadamente diferente
da regra de FNN do RQA, que já falhara estruturalmente para ruído
branco), desenho de sub-janelas (`N_WINDOW=200`, até 10 por segmento)
diretamente motivado pelo custo computacional já MEDIDO na Fase 0.6.

**Validação sintética — achado decisivo, respondendo diretamente ao
risco já medido na Fase 0.6** (correlação `r≈0,92` entre persistência
máxima de H1 e um análogo do `%DET`(RQA) num teste informal): os DOIS
canais (`I(X)`=persistência máxima e total de H1) mostraram
`IAAFT_LOW_POWER` contra o controle positivo não-linear (`p=0,355` e
`p=0,320`), e o fallback de bootstrap por blocos móveis pré-autorizado,
acionado automaticamente, TAMBÉM não mostrou poder (`p=0,454`/`0,368`).
Controle negativo corretamente não-significativo em ambos os testes.
Diagnóstico de correção de código passou limpo (onda senoidal traça um
laço inequívoco em espaço de fase).

**Mecanismo diferente de como o RQA falhou, resultado final igual:** o
embedding com `m=3` fixo resolveu perfeitamente em ~1.200 séries (zero
falhas de `tau`) — o problema não é resolução de embedding, é que a
própria estatística de persistência não separa sinal caótico genuíno de
ruído colorido de espectro casado, sob este desenho. Fechado NA ETAPA DE
VALIDAÇÃO, sem terceira tentativa de redesenho (mesma disciplina já
usada no RQA) — o dado real (LIGO GW150914, S&P500/Lehman) nunca foi
tocado. Detalhes completos:
`02_TESTS/TRI_RG/persistent_homology/RESULTS_SUMMARY.md`.

**Estado da linha:** Fase 0.6 completa — 4 de 4 candidatos formalizados
fechados, nenhum produziu invariante cross-domain sobrevivente. **11 de
11 candidatos identificados nesta linha, desde sua criação, têm
resultado final** (2 fechados na etapa de validação — RQA e
homologia-persistente —, 9 testados até dado real, todos negativos ou
estruturalmente não-testáveis). Nenhum invariante cross-domain
confiável foi encontrado por esta linha até agora.

## O que já foi feito nesta trilha

1. Governança criada: `00_GOVERNANCE/{AGENTS.md,DECISION_LEDGER.yaml,CLAIM_LEDGER.yaml,PREREGISTRATION_TEMPLATE.md}`.
2. Piloto escolhido (autorização explícita do usuário): auditar e refazer o
   teste EFE/SPARC de `01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE`.
3. Auditoria do código legado completa (`AUDIT_LEGACY_MOND_EFE_SPARC.md`,
   8 achados citados por arquivo:linha).
4. Dado real baixado e verificado (`data/PROVENANCE.md`).
5. Pré-registro travado (`PREREGISTRATION.md`, commit `49867fa`).
6. Análise pré-registrada executada sobre dado real
   (`analysis/run_preregistered_analysis.py`, `result_primary.json`).
7. Reexecução adversarial por agente independente
   (`analysis/adversarial_reproduction.py`, `result_adversarial.json`) —
   veredito INCONCLUSIVE.
8. Resultado registrado em `TEST_QUEUE.yaml` (status `CLOSED_INCONCLUSIVE`)
   e `CLAIM_LEDGER.yaml` (`DISC-CLAIM-001`).
9. Decisão de fechamento registrada (`DISC-DEC-002`).

## Arquitetura adotada em 2026-08-12 (`DISC-DEC-003`)

Revisão estratégica externa do usuário identificou que o laboratório
formal (Ondas 1-7, `04_FORMAL_RESEARCH_LAB`) provavelmente otimizava
probabilidade de fechamento (13/13 em três ondas seguidas) em vez de valor
científico esperado. Resposta: arquitetura de três motores
(`00_GOVERNANCE/RESEARCH_PIPELINE.md`) — descoberta de risco alto aqui,
Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`) de risco baixo no
meio, formalização Lean de risco baixíssimo só para quem sobrevive os dois.
Seis extensões técnicas de metodologia adotadas junto
(`00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md`): identificabilidade
(discriminating observable obrigatório), RG/EFT para TRI/TDTR, MDL/
complexidade algorítmica (`ΔJ`), descoberta automática de invariantes
antes de narrativa LLM, descoberta adversarial de nulos (debunker
convencional dedicado), holdout selado obrigatório para buscas amplas.

Três linhas candidatas registradas (`01_PORTFOLIO/TEST_QUEUE.yaml`,
status `CANDIDATE_FORMULATING`, nenhuma pré-registrada):
- `DISC-COSMOLOGY-MOND-SPARC-002` — SPARC como comparação preditiva de
  modelos nomeados, não confirmação/refutação de EFE isolada.
- `DISC-RH-REAL-001` — pesquisa real sobre `riemannZeta`, distinta do
  operador de brinquedo `Tp` (agora reclassificado em
  `04_FORMAL_RESEARCH_LAB` como teste unitário de maquinário, não
  caminho até RH — ver `DEC-107` de lá).
- `DISC-TRI-RG-001` — busca de invariante cross-domain via lente de
  renormalização/coarse-graining para a Theory of Regime Interfaces.

## O que ainda não foi feito

- Decisão do usuário sobre qual candidato de `DISC-TRI-RG-001` perseguir
  (ver seção própria acima) e fechamento dos gaps concretos do candidato
  escolhido antes de qualquer `PREREGISTRATION.md`.
- Fora do escopo desta trilha, mas acionável: reportar/corrigir o
  provável erro de copy-paste em
  `01_TAMESIS_CORE/03_Axiomatic_Closure/Universe_Equation/02_MOND_Emergence/index.html:282`.

## Como continuar (para o próximo agente/sessão)

Ler `00_GOVERNANCE/RESEARCH_PIPELINE.md` e `METHODOLOGY_EXTENSIONS.md`
primeiro. Para `DISC-TRI-RG-001` ou uma nova linha, seguir
`00_GOVERNANCE/AGENTS.md` desde o passo 1 — mas o passo 3 exige declarar
o discriminating observable (e holdout selado, se aplicável) no
`PREREGISTRATION.md` antes do commit de lock, e ao reservar uma fonte de
dado adicional para o Gate, verificar A PRIORI que ela tem amostra
suficiente para a grade/estatística que será travada (lição de
`03_REPLICATION_GATE/PROTOCOL.md`, 2026-08-13). Não reabrir nem editar
`02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` (piloto 001),
`02_TESTS/COSMOLOGY_A0_DERIVATION/PREREGISTRATION.md` (teste 002),
`02_TESTS/RH_ZETA_ZEROS/PREREGISTRATION.md` (RH-REAL sub-teste 1) nem
`02_TESTS/RH_GAP_EXTREME_VALUE_SCALING/PREREGISTRATION.md` (RH-REAL
sub-teste 2) — todos fechados e travados, holdouts/fontes reservadas já
consumidos. Uma extensão de qualquer uma dessas linhas de investigação é
um novo teste com seu próprio pré-registro, não uma reabertura.
