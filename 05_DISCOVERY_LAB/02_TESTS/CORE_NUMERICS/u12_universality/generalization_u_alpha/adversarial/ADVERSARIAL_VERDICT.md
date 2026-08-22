# Veredito adversarial — frente `u12-generalization-u-alpha` (onda 3, DISC-DEC-015)

**Agente:** verificação ADVERSARIAL independente (frente C, mandato do
orquestrador). **Data:** 2026-08-22.
**Disciplina cumprida:** plano + sementes pré-registrados em
`ADVERSARIAL_NOTE.md` (10:05Z), re-derivação analítica própria feita
ANTES de qualquer execução numérica (10:05-10:10Z), alvos de quadratura
próprios travados em `adv_predictions.json` (10:10Z) e simulador
(`adv_sim.py`) travado no mesmo instante — todos ANTES da execução
única (ordem verificável por timestamps de arquivo). Definições e a
tabela de classes lidas em `METHODOLOGY_NOTE.md`/`RESULTS_SUMMARY.md`/
`DERIVATIONS.md`; `predictions.py`/`ualpha_sim.py`/`posthoc_finiten.py`
(implementações da frente-alvo) NÃO foram lidos.

## Alegação atacada

Fórmula-mestre φ_q(c)=∫₀¹e^{-cH_q(t)}dt (com H_q dado); lei de
expoente α=1/(1+min(β,1)); piso/teto α∈[1/2,1] em toda a classe M-q;
mecanismos M-U/M-CLUST(b)/M-INTRA ∈ U_{1/2} (M-INTRA CONJECTURADO,
cauda heurística); M-MIX(p>0)/M-SELF/M-PREV ∈ U_1.

## VEREDITO GLOBAL

> **CONFIRMADO no essencial, com uma ressalva substantiva e localizada.**
> Rederivação analítica própria (rota independente, seção 1 de
> `ADVERSARIAL_NOTE.md`) não encontrou erro na fórmula-mestre, na lei de
> expoente, no piso/teto α∈[1/2,1], nem no lema de intercambiabilidade.
> Verificação numérica com n, c, p, b e sementes 100% independentes
> confirma M-U, M-MIX(p), M-PREV, M-CLUST(b) e a bateria K=1 exata
> (5 mecanismos, todos os alvos racionais e assintóticos batem, incluindo
> os DOIS termos de correção finito-n +pc/n e +2c/n que a frente-alvo
> identificou pós-hoc — reproduzidos aqui de forma independente e a
> priori, não copiados). A extensão de M-INTRA a c até 1000 (6.25× o
> alcance deles) e n=131072 **fortalece** a conjectura α=1/2 sem prová-la
> (declive local sobe 0.41→0.45→0.48, razão MC/heurística sobe
> 0.83→0.89→0.93→0.94, continuando exatamente a tendência que eles já
> haviam relatado) — status permanece CONJECTURADO, como deve. **Achado
> adversarial genuíno:** o teste de estresse M-CLUST(b=50) revela que a
> correção finito-n de primeira ordem c_eff=c(1−c/n)^b, sozinha, é
> **insuficiente** para b grande — resíduo sistemático crescente com c
> (+0.7%→−3.5%→−11.3%→−27.1%), de magnitude comparável a bc/n, sugerindo
> que o termo de "chain-kill" que eles rotulam "parcialmente cancelado"
> não cancela para b=50. Isto NÃO refuta a classificação M-CLUST(b)∈U_{1/2}
> (∀ b fixo) no limite n→∞ — não encontrei evidência de que o limite
> mude — mas expõe uma lacuna real na contabilidade de rigor-de-rascunho
> declarada por eles para b grande, que deveria ser corrigida ou
> explicitamente restrita a b pequeno/moderado. Nenhum mecanismo
> encontrado quebra a classificação DENTRO da família estrita
> (destinos independentes); o candidato de fronteira M-SHARED (fora da
> família, destinos correlacionados) tem comportamento qualitativamente
> consistente com a conjectura lateral deles ("α=1-type"), não com a
> hipótese mais extrema que eu havia registrado como possível antes de
> rodar.

## (0) Disciplina e proveniência

Todos os arquivos desta pasta foram gravados na ordem: `ADVERSARIAL_NOTE.md`
(10:05–10:10Z, plano+sementes+rederivação), `adv_predictions.py`/`.json`
+ `adv_sim.py` (10:10Z, travados), execução única (10:10–10:25Z,
`adv_sim.log`/`adv_sim_results.json`), `adv_posthoc_check.py`/`.json`
(10:29Z, declarado pós-hoc, motivado por um outlier — ver §5). Ordem
verificável por timestamps. `predictions.py`, `ualpha_sim.py` e
`posthoc_finiten.py` da frente-alvo NÃO foram lidos em momento algum.

## (1) Rederivação analítica — resultado

Ver `ADVERSARIAL_NOTE.md` §1 (feita antes de qualquer execução). Três
rotas independentes das deles: expansão de Taylor direta do termo de
crowding (não Watson), argumento de "corrida de exponenciais com k
concorrentes" (não soma sobre F(s)), substituição elementar u=t(cK)^{1/γ}
(não citação de Watson). Todas reproduzem H_q(t)=t²/2+at^{β+1}/(β+1)+…,
α=1/(1+min(β,1)) e o piso/teto α∈[1/2,1]. Lema de intercambiabilidade:
trivial por simetria do grupo completo. **Nenhum erro de lógica
encontrado.** Bônus: re-derivei φ₁(M-INTRA)=3/4 por um argumento
geométrico próprio (arco w=0 fixo, destino v uniforme no ciclo,
x=d/L~U(0,1) no limite ⇒ E[(1−ℓ)+xℓ]=1−1/2+1/4=3/4), confirmando o
valor deles por uma rota ligeiramente diferente.

## (2) Bateria 1 — controle/mecanismos (n=65536, c∈{0.3,3,18,70,220}, N=3000)

| Mecanismo | χ²₅ (bruto) | p | χ²₅ (c/ termo finito-n conhecido) | p corrigido | Declives locais (c crescente) |
|---|---|---|---|---|---|
| M-U | 1.13 | 0.95 | — (sem termo) | — | 0.254, 0.492, 0.502, 0.500 |
| M-CLUST(b=13) | 15.78 | 0.0075 | — (ver §3) | — | 0.258, 0.494, 0.492, 0.509 |
| M-MIX(p=0.3) | 25.34 | 1.2e-4 | 7.51 (alvo+pc/n) | 0.185 | 0.315, 0.711, 0.805, 0.851 |
| M-PREV | 6167 | ~0 | 2.37 (alvo+2c/n) | 0.795 | 0.432, 0.975, 0.909, 0.314 |

**M-U:** todos os \|z\|<1 (max 0.95); PASS limpo — confirma
∫₀¹e^{−ct²}dt em n, c e sementes totalmente inéditos. Declives locais
convergem para 0.49-0.50 assim que c sai do regime pré-assintótico
(c≥18), igual ao 0.5021±0.0048 deles em outra grade — **CONFIRMED**.

**M-MIX(0.3):** falha bruta concentrada em c=220 (z=+4.30) — **exatamente
explicada** pelo termo +p·c/n (0.3·220/65536=0.00101, contra excesso
observado 0.00107): a MESMA correção finito-n que a frente-alvo
identificou pós-hoc para p=0.5, aqui reproduzida a priori (eu já a
tinha antecipado em `ADVERSARIAL_NOTE.md` §(4) do plano) para p=0.3.
Após correção, χ²₅=7.51 (p=0.19) — PASS. Único resíduo: c=18 com z=−2.51
antes e depois da correção (a correção é despezível nesse c) — tratado
como outlier candidato, ver §6 (checagem pós-hoc: NÃO reproduz,
provavelmente flutuação estatística em 20 comparações). Declives locais
sobem 0.32→0.71→0.81→0.85, consistentes com bend para α=1 (previsto:
"sobrevive para c≪(1−p)/p²=7.8"). **CONFIRMED** (com a mesma disciplina
de transparência da frente-alvo: correção declarada, não usada para
esconder o z ruim).

**M-PREV:** falha bruta catastrófica em c≥70 (z=7.3 e 78.2) —
**exatamente explicada** pelo termo +2c/n (2·220/65536=0.0067, versus
alvo líder 0.004545 — a correção é 1.5× o próprio alvo em c=220,
exatamente o regime "cauda mascarada" que eles descrevem para c≳√n
[aqui √65536=256, e o colapso já é visível em c=220]). Corrigido,
χ²₅=2.37 (p=0.80) — PASS limpo. Declive local 3→18 chega a 0.975 (quase
o α=1 alegado) antes do colapso finito-n em 70→220 (0.314, artefato,
não física do limite). **CONFIRMED**, e reproduz de forma independente
o MECANISMO EXATO da reconciliação pós-hoc deles (não só o número).

## (3) M-CLUST(b): b=13 (controle) e b=50 (estresse, achado principal)

**M-CLUST(b=13), n=65536, c∈{0.3,3,18,70,220}, N=3000, alvo próprio
φ_U(c_eff), c_eff=c(1−c/n)^13:** \|z\|<4 em TODAS as 5 células (max 3.54
em c=220); χ²₅=15.78 (p=0.0075, abaixo do limiar p≥0.01 que a
frente-alvo usa — porém critério C1 que EU pré-declarei foi só \|z\|<4,
que passa). Declives locais 0.258/0.494/0.492/0.509 — convergência
LIMPA para 0.5 assim que c sai do regime pré-assintótico, **igual** ao
resultado deles em b=8 (0.4992±0.0048) mas agora em b=13, n, c e
sementes diferentes. **CONFIRMED** (independência de b confirmada de
novo, com p-valor marginal — reportado, não escondido).

**M-CLUST(b=50), estresse, n=65536, c∈{10,50,150,400}, N=2000, mesmo
alvo:** χ²₄=1135.6 (formalmente catastrófico), mas TODAS as 4 células
passam pela regra OU pré-declarada (\|z\|<4 OU desvio relativo<2bc/n) —
a banda em c=400 é 61% (b=50 grande a torna quase vazia de conteúdo,
como eu já havia antecipado no plano). **O achado real não é PASS/FAIL
mas um padrão:** desvio relativo cresce MONOTONICAMENTE e SEMPRE no
mesmo sentido (φ observado < alvo) com c:

| c | desvio relativo | bc/n |
|---|---|---|
| 10 | +0.7% | 0.76% |
| 50 | −3.5% | 3.8% |
| 150 | −11.3% | 11.4% |
| 400 | −27.1% | 30.5% |

O desvio acompanha bc/n em ORDEM DE GRANDEZA em todas as células — ou
seja, o termo de "chain-kill amplification O(bc/n) com cancelamento
parcial de sinal" que `DERIVATIONS.md` §3.5 cita mas não quantifica
**não está sendo cancelado** para b=50 (pelo menos não além de ~10%).
Para b=13 (bateria de controle), bc/n máximo é 13·220/65536=4.4%,
pequeno o bastante para não aparecer no χ²/declives — consistente com
"o argumento funciona bem para b pequeno-moderado, degrada para b
grande" em vez de "funciona para todo b fixo" tratado uniformemente.
**Isto NÃO é uma refutação da classificação M-CLUST(b)∈U_{1/2} no limite
n→∞** (não testei n→∞ com b fixo — apenas n=65536 fixo com b crescendo
até 50; os declives locais de CLUST50, 0.517–0.602, ainda são
claramente sub-1 e da ordem de 0.5, não sugerem um α diferente) — **é
uma lacuna real na contabilidade de rigor-de-rascunho declarada, que
deveria citar b explicitamente ou fornecer o termo de próxima ordem**.
Classificado **PLAUSIBLE** (não CONFIRMED nem REFUTED): o argumento de
sombreamento provavelmente ainda vale no limite, mas a correção
finito-n publicada é incompleta para b grande.

## (4) M-INTRA — extensão da cauda (prioridade; critério deles FALHOU)

n=131072 (2× o deles), c∈{20,80,320,1000} (até 6.25× o c máximo deles),
N=1200, K=1 próprio N=4000 em n=65536.

**K=1:** φ̂₁=0.7492±0.0035 vs alvo exato 3/4 (z=−0.24) — **CONFIRMED**,
reproduz o valor deles E minha rederivação geométrica independente (§1).

**Cauda:** sem alvo numérico rígido pré-declarado (deliberado — ver
`ADVERSARIAL_NOTE.md` §(3), C2 "sem janela de aceite artificial", dado
que eles próprios já haviam achado convergência lenta). Resultado:

| c | φ̂ ± SEM | φ heurística (√π c^{-1/2} integrado) | razão MC/heur | declive local |
|---|---|---|---|---|
| 20 | 0.2964±0.0033 | 0.3571 | 0.830 | — |
| 80 | 0.1680±0.0017 | 0.1883 | 0.892 | 0.410 (20→80) |
| 320 | 0.0899±0.0009 | 0.0966 | 0.930 | 0.451 (80→320) |
| 1000 | 0.0518±0.0005 | 0.0553 | 0.937 | 0.484 (320→1000) |

Declive local SOBE monotonicamente 0.41→0.45→0.48, e razão MC/heurística
sobe 0.83→0.89→0.93→0.94 — **continua exatamente a mesma tendência que
eles relataram** (declive 0.406→0.439 em c∈[10,160]; razão 0.815→0.900
em c=10/40/160), agora estendida 6× além do alcance deles, e chegando
MAIS PERTO de α=0.5 e razão=1 do que eles conseguiram. **Isto não prova
α=1/2** (ainda não há platô visível nem em c=1000), mas é evidência
NOVA e consistente na direção da conjectura, e nenhuma evidência de uma
assíntota diferente (o declive não estagna nem inverte). Reporto como
**PLAUSIBLE, reforçado** — status honesto continua CONJECTURADO (a
frente-alvo não deve promovê-lo a DERIVADO com base nisto), mas a
tentativa de quebra especificamente FALHOU em produzir evidência
contrária.

## (5) M-SHARED (exploratório, fora da família estrita — ver §2 da nota)

n=65536, c∈{3,18,70}, N=2000. φ̂(3)=0.4584±0.0060, φ̂(18)=0.1036±0.0016,
φ̂(70)=0.0288±0.0005 — estritamente entre a baseline (1−e^{−c})/c
(ciclos intocados: 0.317/0.056/0.014) e φ_U(c) (0.504/0.209/0.106),
mais perto de φ_U em c baixo e caindo relativamente mais rápido que
φ_U em c alto. Declives locais: 0.83 (3→18), 0.94 (18→70) — SOBEM em
direção a 1, **consistentes com a conjectura lateral deles** ("α=1-type"
por átomo efetivo de destino compartilhado) e **inconsistentes** com a
hipótese mais extrema que eu havia registrado como possível antes de
rodar (φ→const>0, "não decai"). Confirma o exemplo à mão de n=3: atingir
X não torna um ponto cíclico por si só. **Rotulado INCONCLUSIVO por
desenho** (sem alvo, 3 pontos, fora da família) mas **direção qualitativa
alinhada com a conjectura deles** — não é um contra-exemplo à teoria.

## (6) Nota pós-hoc: outlier M-MIX(0.3), c=18

Na bateria travada, M-MIX0.3 em c=18 deu z=−2.51 (único resíduo não
explicado pelo termo +pc/n, que ali é despezível). Antes de escrever
este veredito, rodei uma checagem CONFIRMATÓRIA declarada como pós-hoc
(`adv_posthoc_check.py/.json`): mesmo mecanismo/c/n, semente NOVA
(555000111), N=6000 (2× a bateria original). Resultado: mean=0.126302,
sem=0.001285, z=+0.55 contra o mesmo alvo — **não reproduz**. Concluo
que o z=−2.51 original foi flutuação estatística (não implausível: 1
outlier a ~2.5σ em 20 células comparadas não é incomum), não um bug ou
efeito real. Reportado por transparência; não usado para alterar
nenhum outro número da bateria travada.

## (7) Bateria K=1 (própria, N=4000, n=65536)

| Mecanismo | φ̂₁ ± SEM | alvo exato | z |
|---|---|---|---|
| M-U | 0.6660±0.0037 | 2/3 | −0.19 |
| M-MIX(0.3) | 0.6155±0.0042 | 1−p/2−(1−p)/3 = 0.61667 | −0.28 |
| M-PREV | 0.5001±0.0045 | 1/2 | +0.03 |
| M-INTRA | 0.7492±0.0035 | 3/4 | −0.24 |

Todos os 4 alvos racionais exatos **CONFIRMED** (\|z\|<0.3 em todos).

## (8) Veredito por mecanismo (resumo) e recomendações

| Mecanismo | Alegação | Veredito adversarial |
|---|---|---|
| Fórmula-mestre + lei de expoente + piso/teto | DERIVADO | **CONFIRMED** (rederivação própria, 3 rotas) |
| Lema de intercambiabilidade | DERIVADO (trivial) | **CONFIRMED** |
| M-U ∈ U_{1/2} | DERIVADO+verificado | **CONFIRMED** (n,c,seed independentes) |
| M-CLUST(b) ∈ U_{1/2}, ∀b fixo | DERIVADO (draft) | **CONFIRMED** para b=13; **PLAUSIBLE com ressalva** — correção finito-n publicada (c_eff só) é incompleta para b grande (b=50), resíduo ~O(bc/n) não cancelado |
| M-MIX(p) ∈ U_1 | DERIVADO | **CONFIRMED** (após aplicar o termo +pc/n, identificado independentemente) |
| M-PREV ∈ U_1 | DERIVADO | **CONFIRMED** (após aplicar o termo +2c/n, identificado independentemente) |
| K=1 exato (4 mecanismos) | DERIVADO | **CONFIRMED**, incl. M-INTRA=3/4 rederivado por rota própria |
| M-INTRA ∈ U_{1/2} (cauda) | CONJECTURADO/HEURÍSTICO | **CONJECTURADO permanece** — evidência estendida (c até 1000, n=131072) é consistente e reforça, não prova; tentativa de quebra falhou em produzir contra-evidência |
| M-SHARED (fora da família) | conjectura lateral não simulada por eles | **EXPLORATÓRIO, direção qualitativa consistente** ("α=1-type"); não decidido, fora de escopo das alegações DERIVADAS |

**Recomendações à frente-alvo:** (i) quantificar ou restringir
explicitamente o alcance de validade em b da correção finito-n de
M-CLUST(b) (achado de §3 — a fórmula c_eff sozinha falha
sistematicamente para b grande, na direção e ordem de grandeza de um
termo bc/n não cancelado); (ii) se buscarem promover M-INTRA além de
CONJECTURADO, os dados desta verificação (c até 1000, n=131072) são
reaproveitáveis como evidência adicional, mas não substituem uma prova.

## Arquivos (todos nesta pasta)

`ADVERSARIAL_NOTE.md` (plano+sementes+rederivação, pré-execução),
`adv_predictions.py`/`.json` (alvos próprios, travados antes de rodar),
`adv_sim.py` (simuladores próprios), `adv_sim.log`/`adv_sim_results.json`
(execução única), `adv_analyze.py` (z-scores/χ²/declives),
`adv_posthoc_check.py`/`.json` (checagem pós-hoc declarada, §6).
