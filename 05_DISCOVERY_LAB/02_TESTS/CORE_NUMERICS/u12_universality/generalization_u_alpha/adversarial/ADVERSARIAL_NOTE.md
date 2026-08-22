# Nota adversarial (plano + sementes) — frente `generalization_u_alpha` (onda 3, DISC-DEC-015)

**Gravado ANTES de qualquer execução numérica desta verificação.**
**Data/hora (UTC):** 2026-08-22T10:05Z.

**Disciplina:** li `METHODOLOGY_NOTE.md`, `RESULTS_SUMMARY.md` e
`DERIVATIONS.md` da frente-alvo (definições, programa e a tabela de
classes alegada). **NÃO li** `predictions.py`, `ualpha_sim.py` nem
`posthoc_finiten.py` (implementações) — simuladores abaixo escritos do
zero. Parâmetros (c, p, b, n, sementes) escolhidos para serem
DIFERENTES da grade pré-registrada deles (c ∈ {0.5,2,10,40,160},
n=32768, b=8, p=0.5).

## Alvo

Tabela de classes de `RESULTS_SUMMARY.md`/`DERIVATIONS.md`: fórmula-mestre
φ_q(c)=∫₀¹e^{-cH_q(t)}dt, H_q(t)=t-(1-t)∫₀ᵗ(1-q(s))/(1-s)ds; lei de
expoente α=1/(1+min(β,1)); piso/teto α∈[1/2,1] em toda a classe M-q;
mecanismos M-U, M-CLUST(b), M-MIX(p), M-SELF, M-PREV (fecham em U_{1/2}
ou U_1) e M-INTRA (K=1 exato 3/4 DERIVADO; cauda √π·c^{-1/2}
HEURÍSTICA, critério de expoente pré-registrado FALHOU nas mãos deles:
α̂=0.4226±0.0034).

## (1) Re-derivação própria (rota independente, feita à mão antes de rodar)

**1a. Termo de crowding via expansão direta (não via Watson/Laplace citado por eles) —
verificação elementar de H_{q≡0}.** Com q≡0: H(t) = t + (1-t)ln(1-t).
Expansão de Taylor de ln(1-t) = -t - t²/2 - t³/3 - O(t⁴) dá
H(t) = t + (1-t)(-t - t²/2 - O(t³))
     = t + [-t - t²/2 - O(t³) + t² + t³/2 + O(t⁴)]
     = t²/2 + O(t³).
Confirma por CONTA DIRETA (sem invocar o mesmo maquinário deles) que MESMO
o mecanismo que nunca mata paga t²/2 — o termo de crowding não é um
artefato da rota deles. Isto é o coração do "piso 1/2": não depende de
q, só da geometria dos inícios de arco.

**1b. Rota alternativa para o termo de crowding (combinatória, não
analítica):** cada evento de reroute sobrevivente (não-morto) cria um
NOVO início de arco em massa fresca; x₀ fecha quando um clock de
fechamento (taxa 1/(1-r) por início de arco ativo) dispara sobre o
início de arco de x₀ especificamente. Com k inícios de arco ativos
(x₀ + k concorrentes, todos criados por sobreviventes até massa t), a
taxa TOTAL de fechamento de QUALQUER início é (k+1)/(1-t) mas x₀ só
"vence" com probabilidade 1/(k+1) condicional a um fechamento — ou,
via superposição de Poisson (rota exponencial-de-corrida usada por
eles), o hazard de "x₀ especificamente fecha" a mass t é exatamente
1/(1-t), INDEPENDENTE de quantos concorrentes existem (propriedade de
"thinning" do processo de Poisson: cada concorrente é apenas mais um
alvo aleatório, e o clock de x₀ é exponencial de taxa 1/(1-t) por
construção do próprio π restrito à massa não visitada — ver nota (0)
herdada). O número de concorrentes SÓ entra multiplicando a taxa de
MORTE por evento (mais concorrentes ⇒ mais chance de um evento cair em
massa já visitada) — que é justamente o q(s) endógeno q(s)=s de M-U.
Ou seja: reobtive H(t) = t²/2 + ... por um argumento de "corrida de
exponenciais" ligeiramente diferente do deles (que soma sobre s uma
integral de F(s); aqui penso em termos de contagem de concorrentes) —
mesma resposta, checagem cruzada de lógica.

**1c. Lei do expoente por substituição direta (não citando "Watson"):**
para H(t) ~ K·t^{γ} (γ = 1+min(β,1), K>0) quando t→0⁺, substituo
u = t·(cK)^{1/γ}: c·H(t) ≈ u^γ, dt = du/(cK)^{1/γ}, logo
φ_q(c) ~ (cK)^{-1/γ}∫₀^∞ e^{-u^γ}du = (cK)^{-1/γ}·Γ(1+1/γ)/1
(usando ∫₀^∞e^{-u^γ}du = Γ(1+1/γ)). Confirma α=1/γ=1/(1+min(β,1)) e a
forma do coeficiente — reproduz (2.2) deles por substituição elementar
em vez de "Laplace/Watson" citado por nome.

**1d. Piso/teto:** H_q monótona em q (mais morte ⇒ H maior ⇒ φ menor)
é imediata de (1.1): o integrando (1-q(s))/(1-s) é decrescente em
q(s) pontualmente, logo H_q(t) cresce com q(s) para cada s. Extremos
q≡0 e q≡1 dão os dois lados do sanduíche — confirmo o argumento deles
sem achar furo.

**Veredito da rederivação analítica: NENHUM ERRO ENCONTRADO nas partes
DERIVADAS (fórmula-mestre, lei de expoente, piso/teto, lema de
intercambiabilidade — este último é trivial: uma lei invariante sob TODO
o grupo simétrico de [n] só pode ser a uniforme, por simetria elementar).
A tentativa de quebra concentra-se então em (i) checar numericamente com
parâmetros/sementes/n independentes, (ii) EXTRAPOLAR M-INTRA para c bem
maior que o alcance testado por eles (onde o critério pré-registrado
FALHOU), e (iii) procurar mecanismo DENTRO ou na FRONTEIRA da família que
quebre a classificação.

## (2) Tentativa de quebra — candidatos considerados

- **M-CLUST(b) com b grande** (b=50, 6× o deles): o argumento de
  "sombreamento" deles assume b FIXO com correção O(bc/n); testar b
  maior e c maior estressa essa correção mais diretamente.
- **M-SHARED (destino único compartilhado X, mesmo p/ todos os
  redirecionados):** mecanismo que eles PRÓPRIOS mencionam de passagem
  em `DERIVATIONS.md` §3.1 ("shared randomness... e.g. all reroutes
  jumping to one common uniform point X") mas **não simulam nem
  derivam** — apenas conjecturam "α=1-type". Nota: D_i = X para TODO
  i∈R viola a hipótese de independência dos destinos EXIGIDA na
  definição da família (§1 de `METHODOLOGY_NOTE.md`: "destinos D_i...
  independentes entre si dado (π,R)") — logo M-SHARED está FORA da
  família estrita deles; testá-lo não pode refutar nenhuma alegação
  DERIVADA (que é sobre a família com destinos independentes), mas
  testa a CONJECTURA lateral deles e ilustra o limite de validade da
  família. Rotulado EXPLORATÓRIO.
  Raciocínio prévio (não simulação): X é quase certamente cíclico (seu
  próprio ciclo-π, encurtado no primeiro reroute que o próprio X
  alcança, sempre fecha de volta em X); MAS um ponto x₀ que apenas
  ATINGE X não se torna cíclico só por isso — cíclico exige f^t(x₀)=x₀,
  não f^t(x₀)=X. Logo a intuição "todo mundo funde no ciclo de X" está
  ERRADA (verificado à mão num exemplo n=3 abaixo) — a massa cíclica
  extra vem apenas do PRÓPRIO ciclo de X (que tem massa size-biased,
  tipicamente O(1), não O(1/n)), somada à massa-base de ciclos
  inteiramente intocados por R. Sem fórmula fechada derivada aqui
  (deixado para a simulação decidir); registro ANTES de rodar que
  espero φ_SHARED(c) descer MAIS DEVAGAR que M-U (possivelmente sem
  decair para 0) — previsão qualitativa, não numérica, declarada antes
  da execução.
  Exemplo à mão (n=3, π=(1→2→3→1), R={2}, X=1): f(1)=π(1)=2 (1∉R),
  f(2)=1 (2∈R,X=1), f(3)=π(3)=1 (3∉R). Ciclo: {1,2} (f(1)=2,f(2)=1).
  Ponto 3: f(3)=1, f²(3)=2, f³(3)=1,... nunca retorna a 3 ⇒ NÃO
  cíclico. φ=2/3 neste exemplo particular (não é uma previsão de
  limite, só ilustra o mecanismo de tail feeding vs ciclo).
- **Intercambiabilidade não-uniforme:** mostrado impossível por
  simetria (§1d) — não há candidato a testar (qualquer lei
  label-invariant sob TODO Sym([n]) é a uniforme); não simulado.
- **Expoente intermediário natural (β∈(0,1)):** nenhum candidato novo
  encontrado no tempo disponível; permanece aberto como no arquivo
  deles — não reivindicado.

## (3) Plano numérico pré-declarado (sementes fixadas ANTES de rodar)

Método de detecção de ciclo: g = f^{2^K} por dobramento vetorizado
(g₁=f; g_{2i}=g_i[g_i]), K tal que 2^K ≥ n (margem ≥2×); pontos
cíclicos = imagem distinta de g (mesmo método validado pelo adversário
da onda 2). Método 100% próprio, sem ler `ualpha_sim.py`.

- **Bateria 1 — controle/mecanismos (independência dos destinos):**
  n=65536=2¹⁶, K=17 (2¹⁷=131072≥2n). Mecanismos: M-U, M-MIX(p=0.3),
  M-PREV, M-CLUST(b=13). c_grid=[0.3, 3, 18, 70, 220] (todos INÉDITOS
  vs. grade deles). N=3000/célula. Semente: `SeedSequence(31415926)`,
  spawn de 20 filhos na ordem (mecanismo)×(c crescente), mecanismos na
  ordem [M-U, M-MIX0.3, M-PREV, M-CLUST13].
- **Bateria 2 — estresse M-CLUST(b) grande:** n=65536, K=17, b=50
  (6.25× o deles), c_grid=[10, 50, 150, 400] (até quase 2×sombreamento
  cŌ crítico). N=2000/célula. Semente: `SeedSequence(27182818)`, 4
  filhos.
- **Bateria 3 — M-INTRA estendido (prioridade; critério deles
  FALHOU):** n=131072=2¹⁷ (2× deles, empurra o viés finito-n ~√n para
  mais longe), K=18. c_grid=[20, 80, 320, 1000] (até 6.25× o c máximo
  deles). N=1200/célula (ver nota de orçamento abaixo). Semente:
  `SeedSequence(16180339)`, 4 filhos. K=1 próprio (N=4000, 1 ponto
  redirecionado, posição uniforme; destino conforme regra do
  mecanismo — M-U/M-MIX0.3/M-PREV/M-INTRA em n=65536, K=17): semente
  `SeedSequence(271828)`.
- **Bateria 4 — M-SHARED (exploratório, fora da família estrita):**
  n=65536, K=17, c_grid=[3, 18, 70]. N=2000/célula. Semente:
  `SeedSequence(14142135)`, 3 filhos.
- **Orçamento de tempo (ajuste ANTES da execução travada, com base em
  smoke test de sementes descartáveis 999/555/12345, sem uso em
  validação):** benchmark por-replicata mediu ~0.005-0.006s
  (M-U/MIX/PREV/CLUST/SHARED, n=65536) e ~0.05s (M-INTRA, ligado a
  `connected_components` para achar ciclos de π, n=131072). Isso
  projeta ~14 min para o plano acima com N=3000/2000/1200/2000/4000
  por bateria — dentro do orçamento de ≤15 min; os N acima já
  refletem esse ajuste (reduzidos de um plano inicial N=2000/8000 para
  M-INTRA/K=1, declarado aqui ANTES da execução travada, mesmo
  espírito da regra "estourar ⇒ reduzir N, declarando").
- **Runtime alvo:** ≤ 15 min foreground total. Execução ÚNICA por
  bateria; bug ⇒ correção + reexecução COMPLETA da bateria afetada com
  sementes declaradas de novo (nunca parcial).
- **Critérios de aceite (pré-declarados):**
  - C1 (curvas, mecanismos com forma fechada — M-U, M-MIX0.3, M-PREV,
    M-CLUST13, M-CLUST50): |z|<4 por célula, alvo = quadratura própria
    (script separado, rodado e travado em JSON ANTES da simulação;
    fórmulas re-derivadas em (1), avaliadas nos MEUS c/p/b — não
    copiadas de `predictions.json` deles). Banda sistemática conhecida
    para M-MIX/M-PREV (termo +pc/n ou +2c/n, já identificado por eles
    E por mim em (1) via geometria finito-n) declarada e aplicada
    apenas OBSERVACIONALMENTE (reportada, não usada para "salvar" um
    z ruim sem full disclosure). M-CLUST: banda 2bc/n.
  - C2 (declive de cauda, α̂ = ln(φ̂(c₁)/φ̂(c₂))/ln(c₂/c₁) no maior
    intervalo disponível de cada bateria): reporta-se α̂±σ para TODOS
    os mecanismos, incluindo M-INTRA — sem janela de aceite artificial
    além de comparar com o α alegado (0.5 p/ M-U/CLUST/INTRA; →1 para
    MIX/PREV) e notar tendência (crescente/decrescente com c).
  - C3 (M-SHARED): sem alvo numérico pré-declarado (mecanismo fora da
    família); reporta-se φ̂(c) vs baseline (1-e^{-c})/c e vs φ_U(c)
    (ambas quadraturas independentes) — INCONCLUSIVO por design,
    interpretação qualitativa apenas.
- Nenhum ajuste de parâmetro após ver resultados; falha ⇒ relatada
  como tal.

## (4) Re-derivação própria do alvo finito-n de M-CLUST(b)

Um ponto p∈R é "início de bloco alcançável pelo passeio-π" (run start)
sse π^{-1}(p)∉R (senão p é sombreado — chega-se a ele só por
redirecionamento de dentro do próprio bloco, não pelo passeio). Para p
ser início de bloco, p mesmo precisa ser semente OU ser um dos b-1
sucessores de uma semente com todos os predecessores no bloco também
semeados — mas a densidade de "primeiro ponto alcançável de um bloco"
ao longo do passeio-π é mais simples de contar via runs: cada corrida
maximal de pontos consecutivos-em-π todos marcados como sementes tem
comprimento geométrico; o argumento deles (run-start density
ρ=(c/n)(1-c/n)^b) é o caso b=block-length fixo — refiz o argumento via
runs de Bernoulli(c/n) ao longo da sequência π-ordenada e cheguei à
MESMA densidade efetiva (é a probabilidade de "início de run" padrão
para uma sequência i.i.d., ajustada pelo alcance de sombreamento b);
uso como alvo próprio c_eff=c(1-c/n)^b, com banda declarada 2bc/n,
igual à deles (concordância de rota, não cópia de número).



