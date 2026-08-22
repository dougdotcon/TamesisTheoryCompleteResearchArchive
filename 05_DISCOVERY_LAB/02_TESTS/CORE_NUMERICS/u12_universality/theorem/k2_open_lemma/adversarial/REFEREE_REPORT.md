# REFEREE_REPORT — verificação adversarial hostil de ATTEMPT.md (K2-OPEN-LEMMA)

> Árbitro adversarial, wave 5, DISC-DEC-022 frente (a). Alvo:
> `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/ATTEMPT.md`,
> que afirma provar incondicionalmente o caso `K=2` do Lema Aberto de
> `THEOREM.md` §7.4. Disciplina seguida: (1) li apenas `THEOREM.md` antes de
> `ATTEMPT.md`; (2) tranquei meus próprios números de força bruta ANTES de
> ler qualquer script do front; (3) só depois disso li
> `psi_bruteforce.py`, `psi_k2_case_formula.py`, `derive_closed_forms.py`,
> `psi_k3_exploration.py`. Plano registrado em `REFEREE_NOTE.md` (mesma
> pasta), escrito antes de rodar qualquer código.

## Resumo do veredito (leia isto primeiro)

**Não encontrei nenhum erro, lacuna lógica ou passo mal justificado na
prova do caso `K=2`.** Toda fórmula fechada citada no ATTEMPT.md para
`K=1,2` foi reproduzida por força bruta exaustiva **escrita do zero**
(sem olhar os scripts do front antes), e a análise de casos (a)/(b)/(c) do
§4.3 — incluindo o Lema B (co-cycle, `P=1/2`) e o "target-set principle" —
foi **rederivada independentemente à mão e depois confirmada
simbolicamente com `sympy`** a partir dos pesos de caso, não copiando as
fórmulas do front. Além disso, um item que o próprio ATTEMPT.md rotula
honestamente como **"CONFIRMED BY EXACT FIT, not derived"** (`ψ_n^{(2),R}`,
item 8 do placar) — a única peça não totalmente derivada do documento —
**eu consegui derivar aqui do zero, por primeiros princípios**, usando o
mesmo método de passeio/target-set do §4 aplicado ao passeio que começa
NA própria fonte (não em um ponto genérico); a derivação bate
simbolicamente, termo a termo, com a fórmula que o front só tinha ajustado
por interpolação. Isso fecha a única lacuna metodológica que o próprio
front havia sinalizado.

**Veredito geral: o caso `K=2` do Lema Aberto (`φ_n^{(2)} → φ_2 = 8/15`)
pode ser honestamente rotulado PROVADO**, não PROPOSIÇÃO CONDICIONAL — a
prova do ATTEMPT.md resiste integralmente ao ataque adversarial, e a
"taxa bônus" (`φ_n^{(2)} = 8/15+1/(30n)+7/(10n²)+1/(5n³)`) pode agora ser
rotulada PROVADA sem ressalva (não mais "modulo #8"), graças à derivação
adicional que produzi. O caso geral `K≥3` continua corretamente aberto —
o ATTEMPT.md não superestima nada ali.

---

## 1. Lema A (Lema de Redução, geral em `K`) — **SOUND**

**Afirmação (ATTEMPT.md §2):** `φ_n^{(K)} = (K/n)ψ_n^{(K),R} + (1-K/n)ψ_n^{(K)}`,
exatamente, para todo `n>K`, todo `K≥1` fixo.

**Verificação.** A prova é um argumento de simetria/exchangeabilidade
elementar (conjugação por transposições dentro de cada bloco de índices).
Reconferi a prova linha por linha — não há restrição escondida a `K=1,2`;
o argumento usa apenas que uma transposição dentro de um bloco não mistura
os dois blocos, o que vale para qualquer `K` e qualquer `n>K`.

Além da leitura, testei a identidade como **identidade exata em `n` finito**
(não apenas no limite) a partir dos MEUS PRÓPRIOS `ψ_n^{(K)}`, `ψ_n^{(K),R)}`,
`φ_n^{(K)}` calculados por enumeração exaustiva independente
(`ref_bruteforce.py`, escrito do zero — ver §5), para `K=1` (`n=2..10`),
`K=2` (`n=3..9`) e `K=3` (`n=4..8`) — **em TODOS os 24 pontos testados a
identidade bateu exatamente** (frações idênticas), incluindo o caso
degenerado `n=K+1` (só um ponto genérico, `K=3,n=4`). Ver
`ref_bruteforce_K*.json` e a linha "LemmaA predicts phi = ... == computed
phi ? True" em cada execução.

**Veredito: SOUND.** Genuinamente geral em `K`, sem citação, sem gap.

---

## 2. `K=1` rederivado via a rota do passeio (ATTEMPT.md §3) — **SOUND**

**Afirmações:** `ψ_n^{(1)} = 2/3+1/(6n)`, `ψ_n^{(1),R} = 1/2+1/(2n)`,
recombinando via Lema A para reproduzir exatamente a Proposição 4 de
`THEOREM.md` (`φ_n^{(1)} = 2/3+1/(3n²)`).

**Verificação.** Minha própria força bruta (`ref_bruteforce.py`, K=1,
`n=2..10`) reproduz `ψ_n^{(1)}`, `ψ_n^{(1),R}` e `φ_n^{(1)}` exatamente
iguais às três fórmulas fechadas, em cada um dos 9 valores de `n`
(`verify_formulas.log`, seção K=1: 27/27 checagens exatas passaram). Os
valores de `φ_n^{(1)}` (n=3: 19/27; n=4: 11/16; n=5: 17/25; n=6: 73/108;
n=7: 33/49) também batem exatamente com a verificação independente já
registrada em `THEOREM.md` §7.3 ("Independent verification... exact
enumeration") — uma **terceira** fonte concordando (THEOREM.md's próprio
`k1_exact_check.py`, ATTEMPT.md's `psi_bruteforce.py`, e meu
`ref_bruteforce.py`, três implementações independentes, mesmo resultado).

O "cancelamento exato" que o front destaca (§3, coeficientes `1/n` de
`ψ^R` e `ψ` se cancelando para dar a taxa `O(1/n²)` de Prop. 4) confere:
recombinando `(1/n)(1/2+1/(2n)) + (1-1/n)(2/3+1/(6n))` simbolicamente dá
exatamente `2/3+1/(3n²)`, sem termo `1/n` residual — confirmado à mão e
numericamente.

**Veredito: SOUND.**

---

## 3. Lema B (co-cycle lemma, `P=1/2` exatamente) — **SOUND, estresse-testado**

**Afirmação:** para uma permutação uniforme de um conjunto finito de
tamanho `m≥2`, dois elementos fixos distintos estão no mesmo ciclo com
probabilidade exatamente `1/2`, independente de `m`.

**Rederivação independente (antes de rodar qualquer código):** com
`L~Unif{1,...,m}` o comprimento do ciclo de um dos dois elementos,
`P(mesmo ciclo) = E[(L-1)/(m-1)] = (E[L]-1)/(m-1) = ((m+1)/2-1)/(m-1) =
1/2`, usando apenas `E[L]=(m+1)/2` — álgebra elementar, sem hipótese
escondida sobre `m`.

**Força bruta independente** (`check_lemma_B.py`, escrito do zero,
NENHUM reroteamento envolvido — só permutações puras): `m=2,...,8`, `P`
calculada exatamente por enumeração de todas as `m!` permutações —
**`P=1/2` exato em todos os 7 casos**, incluindo o caso extremo `m=2`
(`check_lemma_B.log`).

**Tentativa de contra-exemplo:** procurei deliberadamente por uma
configuração degenerada onde `P≠1/2` — `m` pequeno (2,3), estrutura de
ciclo degenerada (permutação identidade incluída na enumeração completa,
não excluída) — nenhuma encontrada. O lema é, de fato, um fato clássico
correto e bem conhecido sobre permutações uniformes (não é um resultado
novo arriscado); a "surpresa" alegada pelo ATTEMPT.md ("apparently not
stated as such in THEOREM.md") é apenas que `THEOREM.md` não precisou
dele, não que o fato seja incomum.

**Veredito: SOUND**, nenhum contra-exemplo encontrado, prova elementar
correta.

---

## 4. Análise de casos `K=2` (a)/(b)/(c), §4.3, e a fórmula fechada `ψ_n^{(2)}` — **SOUND**

Esta é a parte mais delicada e onde um erro de contagem seria mais
provável de se esconder. Ataque em três camadas:

### 4.1 Rederivação independente dos pesos de caso e das fórmulas `P_b`, `P_c`

Antes de escrever qualquer código, rederivei à mão, via um argumento
hipergeométrico direto (qual dos `n-1` outros pontos cai nas `ℓ-1` vagas
de `C_0`), os três pesos de caso — batem exatamente com os do
ATTEMPT.md, e a soma `(n-ℓ)(n-ℓ-1)+2(ℓ-1)(n-ℓ)+(ℓ-1)(ℓ-2)=(n-1)(n-2)`
confere via a identidade `a(a-1)+2ab+b(b-1)=(a+b)(a+b-1)`.

Rederivei também `P_b(ℓ,d)` e `P_c(ℓ,p,q)` do zero, ramificando
explicitamente cada valor possível do alvo de reroteamento (`U_A`),
usando o Lema B para a probabilidade de a excursão fresca encontrar a
outra fonte, e justificando por que qualquer pouso em território nunca
visitado, sem fontes restantes, é necessariamente um beco sem saída
("target-set principle", que também rederivei, não apenas aceitei). O
resultado bate **exatamente**, termo a termo, com as fórmulas do
ATTEMPT.md:

- `P_b(ℓ,d) = (ℓ-d)(3n-ℓ+1)/(2n²)` — confirmado.
- `P_c(ℓ,p,q) = (ℓ-q)(n+q-p)/n²` — confirmado.

### 4.2 Checagem no nível de CASO (não só o resultado agregado)

Escrevi `check_case_formulas.py` do zero: para cada `n`, classifica cada
uma das `n!` permutações por `(caso, ℓ, extra)` a partir da definição
crua (não das fórmulas de caso), calcula a probabilidade de sucesso
condicional empírica exata por enumeração de todos os `n²` pares de alvo,
e compara com `P_b`/`P_c` avaliados nesse `(ℓ,d)`/`(ℓ,p,q)` específico —
um teste estritamente mais fino que checar só a fórmula fechada final,
porque testa a análise de casos em si.

**Resultado: 0 incompatibilidades em 120 configurações distintas
`(caso,ℓ,extra)` testadas, `n=3,...,7`** (`check_case_formulas.log`).

### 4.3 Rederivação simbólica independente da forma fechada

Somei os pesos de caso × `P_b`/`P_c` (que eu mesmo rederivei, não copiei)
com `sympy`, do zero, sem olhar `derive_closed_forms.py` antes
(`independent_symbolic_derivation.py`). Resultado **simbólico**, não
apenas numérico:

```
ψ_n^{(2)} = (8n²+4n+1)/(15n²) = 8/15 + 4/(15n) + 1/(15n²)     [identidade exata em n, sympy confirma diff==0]
```

Confere com a fórmula do ATTEMPT.md termo a termo e simbolicamente
(`independent_symbolic_derivation.log`).

### 4.4 Força bruta pura, da definição, `n=3..9`

`ref_bruteforce.py` (força bruta exaustiva independente, `n! × n²`
instâncias, detecção de ciclo verificada por testes unitários — ver
§5) dá, comparado à fórmula `8/15+4/(15n)+1/(15n²)`:

| n | meu `ψ_n^{(2)}` (força bruta) | fórmula | igual? |
|---|---|---|---|
| 3 | 17/27 | 17/27 | sim |
| 4 | 29/48 | 29/48 | sim |
| 5 | 221/375 | 221/375 | sim |
| 6 | 313/540 | 313/540 | sim |
| 7 | 421/735 | 421/735 | sim |
| 8 | 109/192 | 109/192 | sim |
| 9 | 137/243 | 137/243 | sim |

(`n=9` é um ponto NOVO, além do range `n=3..8` originalmente testado no
ATTEMPT.md — bate também.) `verify_formulas.log`.

**Veredito: SOUND, em quatro camadas independentes** (rederivação à mão,
checagem por caso, rederivação simbólica, força bruta pura) — não
encontrei nenhuma configuração `n`, `ℓ`, `d` ou `(p,q)` onde a lógica
falha.

---

## 5. Metodologia da minha própria força bruta — validação

`ref_bruteforce.py` foi escrito do zero, ANTES de ler qualquer script do
front, implementando a definição diretamente (Definição 1/4 de
`THEOREM.md`): enumera TODAS as `n!` permutações × TODOS os `n^K` alvos
de reroteamento, detecta pontos cíclicos via o algoritmo padrão de
coloração de grafo funcional (`O(n)` por instância). A função
`cyclic_flags` foi verificada com 8 testes unitários manuais cobrindo
identidade, ciclos, pontos fixos, auto-loops e um caso composto
(`n=4`, `f=[3,0,0,1]`) — todos passaram (ver transcript acima na sessão;
não regravado em arquivo separado, mas reproduzível rodando o snippet
citado no fim deste relatório).

Meus números batem em TRÊS pontos de triangulação diferentes:
1. Com `THEOREM.md` §7.3's próprio `k1_exact_check.py` (K=1, φ_n^{(1)}).
2. Com `THEOREM.md` §7.4's própria tabela (`k2_exact_exploration.py`,
   K=2, φ_n^{(2)}, `n=2..8` — os 7 valores da tabela publicada em
   `THEOREM.md` batem exatamente com o que minha força bruta produziu
   independentemente).
3. Com as fórmulas fechadas do ATTEMPT.md (K=1, K=2).

Três implementações independentes (a minha, a de `THEOREM.md`, a do
ATTEMPT.md) concordando bit-a-bit em frações exatas é a evidência mais
forte disponível de que não há erro de definição ou de implementação em
nenhuma das três.

---

## 6. O item fitado (`ψ_n^{(2),R}`) — de "CONFIRMED BY EXACT FIT" para **DERIVADO**

Isto é a principal contribuição nova deste relatório, além de confirmar
o que já estava lá.

**O que o ATTEMPT.md fez (§6, honestamente rotulado):** ajustou
`ψ_n^{(2),R} = (An²+Bn+C)/(15n²)` a 3 pontos de força bruta (`n=6,7,8`),
checou contra 3 pontos held-out (`n=3,4,5`) — 6/6 batem — mas
explicitamente NÃO derivou essa fórmula dos primeiros princípios, e
sinaliza isso como um item de acompanhamento não realizado.

**O que eu fiz:** apliquei o MESMO método de passeio/target-set do §4,
mas com o passeio começando NA própria fonte (`y_0=0`, `f(0)=U_0`
imediatamente, sem percorrer `π` antes). A derivação (registrada em
`derive_psiR_from_scratch.py`/`.log`) mostra que:

- Seja `D` o próprio ciclo-`π` da fonte `0` (independente do
  reroteamento), comprimento `m~Unif{1,...,n}` (mesmo fato clássico).
  Como a fonte `0` nunca percorre `D` antes do primeiro reroteamento
  (seu primeiro passo já é `U_0`, não um passo de `π`), `D` fica
  **inteiramente intocado** até algo pousar nele — ao contrário do caso
  do ponto genérico, onde `C_0` é parcialmente "consumido" andando até
  a primeira fonte.
- Isso faz os dois sub-casos (fonte-1 fora de `D` / fonte-1 em `D` na
  posição `k`) coincidirem EXATAMENTE com `P_b(ℓ,d)` e `P_c(ℓ,p,q)` do
  §4.3 avaliados em `d=0` e `p=0` respectivamente — "a própria fonte
  conta como se estivesse na posição 0 do seu próprio ciclo".
- Somando com `sympy` (independente de `derive_closed_forms.py`, que só
  li depois), o resultado é **simbolicamente idêntico** à fórmula que o
  front só tinha ajustado por interpolação:

```
ψ_n^{(2),R} = (n+1)(5n+2)/(12n²)      [derivado; diff simbólico com a fórmula "fitada" = 0]
```

**Checagem no nível de caso** (`check_case_formulas_R.py`, análoga à
§4.2 acima): classifica cada permutação por `(m,k)` = (comprimento do
ciclo próprio de `0`, posição da fonte 1 nesse ciclo), compara a
probabilidade de sucesso empírica com `P_b(m,0)`/`P_c(m,0,k)` —
**0 incompatibilidades em 75 configurações, `n=3..7`**
(`check_case_formulas_R.log`).

**Teste de unicidade do ansatz (item 5 da tarefa):** ajustei a MESMA
família de 3 parâmetros usando um split INDEPENDENTE dos meus próprios
dados (`n=3,4,5` em vez de `n=6,7,8` do front) — reproduz exatamente
`A=25/4,B=35/4,C=5/2`, e prediz corretamente `n=6,7,8,9` (holdout,
incluindo um ponto — `n=9` — que nem o front nem eu tínhamos usado no
ajuste original). Também ajustei uma família ESTRITAMENTE MAIOR (4
parâmetros, denominador `n³`) a 4 pontos: o parâmetro extra sai
EXATAMENTE zero, colapsando de volta à família de 3 parâmetros, e ainda
assim prediz corretamente os 2 pontos held-out restantes
(`check_ansatz.log`). Isso mostra que o ajuste não é uma coincidência de
poucos pontos — é sobre-determinado por um fator de 2 (6 pontos exatos
para 3 parâmetros) e resiste a uma família estritamente mais flexível.
Agora, com a derivação analítica do parágrafo anterior, a questão de
unicidade do ansatz fica de qualquer forma **superada**: não é mais um
ajuste, é uma fórmula derivada.

**Recombinação final:** usando as DUAS peças agora totalmente derivadas
(`ψ_n^{(2)}` do §4 e `ψ_n^{(2),R}` derivado aqui), a identidade do Lema
A reproduz, simbolicamente e sem ressalva,

```
φ_n^{(2)} = 8/15 + 1/(30n) + 7/(10n²) + 1/(5n³)
```

(`recombine_check.py`/`.log`, diff simbólico = 0).

**Veredito: o item 8 do placar do ATTEMPT.md ("CONFIRMED BY EXACT FIT,
not derived") pode ser promovido para PROVADO**, e por consequência o
item 9 ("PROVED modulo #8's status") pode ser promovido para **PROVADO
sem ressalva**. Isto é uma correção estritamente a favor do front — o
ATTEMPT.md tinha subestimado o próprio rigor do que havia estabelecido
(a fórmula estava correta, só faltava a derivação, que eu forneço aqui).

---

## 7. `K≥3` (ATTEMPT.md §7) — honestidade confirmada, nenhuma superestimação

Reproduzi a tabela de `ψ_n^{(3)}` do §7.3 por força bruta independente
(`ref_bruteforce.py`, K=3, `n=4..8`) — bate exatamente em todos os 5
valores, incluindo `n=8` (`18023/35840`, um cálculo de ~58s,
independente do dos ~36s do front) — `verify_formulas.log`. O ATTEMPT.md
rotula esses números corretamente como "NUMERICALLY SUPPORTED ONLY... not
even a rate estimate", e o Lema A confere exatamente também em `K=3`
(`n=4..8`, todos os 5 pontos). Não encontrei nenhuma alegação
inflada sobre `K≥3` — o documento é preciso ao dizer que nada além de
evidência numérica qualitativa existe ali, e que a Lema B′ conjectural
do §7.2 é o item que faltaria.

---

## 8. Checagem de disciplina de governança

- Nenhum arquivo em `THEOREM.md` foi tocado (apenas lido).
- Nenhum commit/push feito nesta sessão.
- Nenhuma edição em `05_DISCOVERY_LAB/00_GOVERNANCE/`.
- Todos os artefatos deste relatório estão em
  `.../k2_open_lemma/adversarial/`, conforme instruído.
- Nenhum nome de modelo de IA aparece em nenhum arquivo criado.

---

## Placar consolidado (minha revisão do placar §8 do ATTEMPT.md)

| # | Alvo | Veredito do front | Meu veredito adversarial |
|---|---|---|---|
| 1 | Lema A, geral em K | PROVADO | **SOUND** — confirmado (§1 acima) |
| 2 | `ψ_n^{(1)}=2/3+1/(6n)` | PROVADO | **SOUND** (§2) |
| 3 | `ψ_n^{(1),R}=1/2+1/(2n)` | PROVADO | **SOUND** (§2) |
| 4 | `K=1` Open Lemma via Lema A | PROVADO | **SOUND** (§2) |
| 5 | Lema B (`P=1/2`) | PROVADO | **SOUND**, testado até tentar quebrar (§3) |
| 6 | `ψ_n^{(2)}=8/15+4/(15n)+1/(15n²)` | PROVADO | **SOUND**, 4 camadas independentes (§4) |
| 7 | **`K=2` Open Lemma**: `φ_n^{(2)}→φ_2` | PROVADO | **SOUND — confirmo PROVADO** |
| 8 | `ψ_n^{(2),R}=(5n+2)(n+1)/(12n²)` | CONFIRMED BY FIT (não derivado) | **PROMOVIDO A PROVADO** — derivei do zero (§6) |
| 9 | `φ_n^{(2)}` taxa bônus | PROVED modulo #8 | **PROMOVIDO A PROVADO sem ressalva** (§6) |
| 10 | Taxa verdadeira `Θ(1/n)`, não `Θ(1/n²)` | RESOLVED para K=2 | **CONFIRMADO** |
| 11-14 | Discussão `K≥3`, Lema B′ | ARGUED/STATED/OPEN | **Honestidade confirmada**, nenhuma superestimação (§7) |

**Nenhum item foi rebaixado.** Dois itens (8, 9) foram **promovidos**
de "confirmado por ajuste" para "provado por primeiros princípios",
graças a uma derivação adicional produzida durante esta verificação
adversarial e verificada em três camadas (rederivação simbólica,
checagem por caso, força bruta).

---

## Veredito final sobre a pergunta da tarefa

> "K=2 case of the Open Lemma is proved" — **pode ser honestamente
> afirmado como PROVADO**, não PROPOSIÇÃO CONDICIONAL nem com lacuna
> identificada. A cadeia completa — Lema A (geral, `K`) + Lema B
> (co-cycle, `P=1/2` exato) + análise de casos (a)/(b)/(c) explícita +
> soma simbólica exata — resistiu a uma tentativa hostil de quebra em
> múltiplas camadas independentes (rederivação analítica própria,
> checagem no nível de caso, força bruta pura escrita do zero, e
> re-derivação simbólica independente), sem que nenhuma delas
> encontrasse uma discrepância. A única peça que o próprio front não
> tinha derivado (`ψ_n^{(2),R}`) foi derivada aqui, fechando também essa
> ressalva.
>
> O caso geral `K≥3` **permanece corretamente aberto** — nada neste
> relatório o resolve, e o ATTEMPT.md não alega o contrário.

---

## Arquivos produzidos nesta verificação

Todos em `05_DISCOVERY_LAB/02_TESTS/CORE_NUMERICS/u12_universality/theorem/k2_open_lemma/adversarial/`:

- `REFEREE_NOTE.md` — plano escrito antes de rodar qualquer força bruta.
- `ref_bruteforce.py` + `ref_bruteforce_K{1,2,3}_n*.json` — força bruta
  exaustiva independente (definição crua), `K=1` (n=2..10), `K=2`
  (n=3..9), `K=3` (n=4..8).
- `verify_formulas.py` + `.log` — checa todas as fórmulas fechadas do
  ATTEMPT.md contra meus próprios números de força bruta.
- `check_lemma_B.py` + `.log` — força bruta independente do Lema B
  (m=2..8), sem reroteamento.
- `check_case_formulas.py` + `.log` — checagem no nível de caso
  `(caso,ℓ,extra)` para `ψ_n^{(2)}`, `n=3..7`, 120 configurações, 0
  incompatibilidades.
- `check_case_formulas_R.py` + `.log` — idem para `ψ_n^{(2),R}`
  (`(m,k)`), `n=3..7`, 75 configurações, 0 incompatibilidades.
- `independent_symbolic_derivation.py` + `.log` — resoma simbólica
  independente (sympy) dos pesos de caso rederivados à mão, reproduz
  `ψ_n^{(2)}` exatamente.
- `derive_psiR_from_scratch.py` + `.log` — derivação por primeiros
  princípios de `ψ_n^{(2),R}` (novo, não estava no ATTEMPT.md).
- `check_ansatz.py` + `.log` — teste de unicidade do ansatz de
  interpolação (split independente + família maior).
- `recombine_check.py` + `.log` — recombinação final via Lema A das duas
  peças agora derivadas, confirma a taxa bônus sem ressalva.
