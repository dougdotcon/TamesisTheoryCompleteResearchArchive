# Referee note — plano de verificação adversarial (K2-OPEN-LEMMA)

Escrito ANTES de rodar qualquer força bruta própria ou ler os scripts do front
(`psi_bruteforce.py`, `psi_k2_case_formula.py`, `derive_closed_forms.py`,
`psi_k3_exploration.py`), conforme a disciplina de árbitro hostil.

## O que já foi lido

- `THEOREM.md` completo (0–1325 linhas): definições (Definição 1 `M_n(c)`,
  Definição 3 `L(c)` explícito, Definição 4 `φ_n^{(K)}`), Teorema 1, Lema 2
  (`φ_K = 4^K(K!)^2/(2K+1)!`), Proposição 3 (redução Binomial→Poisson, PROVADA),
  Proposição 4 (`φ_n^{(1)} = 2/3+1/(3n^2)`, PROVADA com prova completa lida),
  §7.4 (Lema Aberto K≥2, tabela exata de `φ_n^{(2)}` para n=2..8 dada no
  próprio THEOREM.md — vou reusar esses 7 valores como um terceiro ponto de
  verificação independente, já que vieram de um script diferente do front).
- `ATTEMPT.md` completo (640 linhas): Lema A (redução), execução K=1 (§3),
  Lema B (co-cycle, P=1/2, §4.1), análise de casos K=2 (a)/(b)/(c) (§4.3),
  forma fechada `ψ_n^{(2)}` (§4.4), "teorema" K=2 fechado (§5), taxa bônus via
  interpolação racional fitada para `ψ_n^{(2),R}` (§6), discussão K≥3 (§7),
  scorecard (§8).

## Rederivação analítica já feita à mão (antes de programar)

Antes de escrever qualquer script, re-derivei manualmente, a partir da
definição (não copiando do ATTEMPT.md), as fórmulas de caso:

- Contagem de casos (a)/(b)/(c) via hipergeométrica (probabilidade de 0, 1 ou 2
  fontes estarem no ciclo `C_0` de comprimento `ℓ`, entre as `n-1` outras
  posições) — confere exatamente com os pesos `(n-ℓ)(n-ℓ-1)/[(n-1)(n-2)]`,
  `2(ℓ-1)(n-ℓ)/[(n-1)(n-2)]`, `(ℓ-1)(ℓ-2)/[(n-1)(n-2)]` do ATTEMPT.md, e a
  soma dá exatamente `(n-1)(n-2)` (identidade `a(a-1)+2ab+b(b-1)=(a+b)(a+b-1)`
  com `a=n-ℓ,b=ℓ-1`).
- Lema B (co-cycle): `P(mesmo ciclo) = (E[L]-1)/(m-1) = 1/2` — confirmado
  algebricamente (`E[L]=(m+1)/2` de `L~Unif{1..m}`) e à mão para `m=2,3`.
- Caso (b): rederivei `P_b(ℓ,d)` do zero (ramificando em `U_A = x*`, `∈{c_1..
  c_{d-1}}`, `∈{c_{d+1}..c_{ℓ-1}}`, `=B`, `∈` território fresco `\{B\}`, usando
  o Lema B para a chance de a excursão fresca encontrar `B`, e o "target-set
  principle" — que também rederivei, mostrando que qualquer pouso em território
  nunca-visitado sem fontes restantes é necessariamente morto, e que pousar na
  cauda de `C_0` após a última posição usada leva deterministicamente a `x*`).
  Resultado: `(ℓ-d)(3n-ℓ+1)/(2n^2)` — bate exatamente com o ATTEMPT.md.
- Caso (c): rederivei `P_c(ℓ,p,q)` do zero de forma análoga (sem território
  fresco relevante, já que ambas as fontes já estão em `C_0`). Resultado:
  `(ℓ-q)(n+q-p)/n^2` — bate exatamente com o ATTEMPT.md.

Isso já é uma verificação forte da lógica de casos citada no item (3)/(6) do
scorecard — mas ainda preciso confirmar que a SOMA final sobre `ℓ,d,p,q` dá
`8/15+4/(15n)+1/(15n^2)`, e principalmente preciso de uma verificação numérica
100% independente (função-alvo calculada diretamente da definição, sem passar
pelas fórmulas de caso) para não estar simplesmente confirmando minha própria
álgebra com a álgebra deles.

## Plano de força bruta própria (a executar agora)

Script próprio (`ref_bruteforce.py`), escrito do zero, SEM olhar
`psi_bruteforce.py` nem os outros scripts do front:

1. Para cada `n`, enumerar EXAUSTIVAMENTE todas as permutações `π` de
   `{0,...,n-1}` (`itertools.permutations`) e todos os alvos de reroteamento
   `U_1,...,U_K ∈ {0,...,n-1}^K` (produto cartesiano completo, não amostrado).
   Fontes fixas = `{0,...,K-1}` (0-indexado). Construir `f` e determinar, via
   detecção de ciclo em grafo funcional (O(n) por instância, sem hipóteses),
   quais pontos são cíclicos.
2. Calcular, com frações exatas (`fractions.Fraction`), para cada `n`:
   - `ψ_n^{(K)}` = P(ponto genérico `K` é cíclico) [ponto de índice `K`,
     0-indexado, i.e., o primeiro ponto fora das fontes]
   - `ψ_n^{(K),R}` = P(ponto `0`, uma fonte, é cíclico)
   - `φ_n^{(K)}` = média sobre TODOS os `n` pontos (contagem total cíclica / n)
3. Rodar para `K=1`: `n=2..10` (rápido). Comparar com
   `ψ_n^{(1)}=2/3+1/(6n)`, `ψ_n^{(1),R}=1/2+1/(2n)`,
   `φ_n^{(1)}=2/3+1/(3n^2)` (Proposição 4 do THEOREM.md).
4. Rodar para `K=2`: `n=3..9` (talvez 9 dependendo do tempo). Comparar com
   `ψ_n^{(2)}=8/15+4/(15n)+1/(15n^2)`,
   `ψ_n^{(2),R}=(5n+2)(n+1)/(12n^2)` (item fitado, checar mesmo assim),
   `φ_n^{(2)}=8/15+1/(30n)+7/(10n^2)+1/(5n^3)`, e cruzar `φ_n^{(2)}` com a
   tabela EXATA já publicada em `THEOREM.md` §7.4 (n=2..8) — terceira fonte
   independente (script `k2_exact_exploration.py`, que também não li).
5. Verificar a identidade do Lema A exatamente, ponto a ponto em `n`, a partir
   dos MEUS PRÓPRIOS `ψ_n^{(K)}, ψ_n^{(K),R}, φ_n^{(K)}` (não das fórmulas
   fechadas) — isso testa a Lema A como identidade estrutural, não apenas via
   seu enunciado assintótico.
6. `K=3`, apenas como checagem de sanidade de baixa prioridade, para `n` tão
   grande quanto o orçamento permitir (provavelmente `n=4..7`), comparando com
   a tabela do §7.3 do ATTEMPT.md.
7. Rodar um teste de "unicidade do ansatz" para `ψ_n^{(2),R}`: ajustar (a)
   a família `(An^2+Bn+C)/(12n^2)` usada pelo front e (b) pelo menos uma
   família alternativa com estrutura diferente (por ex. grau extra `1/n^3`,
   ou denominador diferente) aos MESMOS pontos de brute force, e ver se ambas
   batem igualmente bem nos pontos held-out — para avaliar se o ansatz do
   front é "quase forçado" pela estrutura ou genuinamente arbitrário.
8. Tentativa (esforço limitado, prioridade baixa) de derivar `ψ_n^{(2),R)}`
   pelo mesmo método de passeio/target-set (fonte 1 como ponto de partida),
   para tentar promover o item de "fitado" para "derivado".

## Critério de veredito

- Cada fórmula fechada citada no ATTEMPT.md será classificada SOUND se meus
  números de força bruta batem exatamente (frações idênticas) em TODO o
  intervalo testado, e a lógica do passo correspondente resistir à minha
  rederivação independente.
- GAP FOUND / ERROR exige um `n` ou configuração concreta onde a força bruta
  diverge da fórmula, ou um passo lógico específico citado (número de linha/
  seção do ATTEMPT.md) que não se sustenta.
- Só depois de fixar esses números é que vou ler os scripts do front, para
  comparar metodologia (não para copiar números).
