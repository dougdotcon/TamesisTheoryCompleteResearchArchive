# Pré-registro: escala do gap mínimo entre zeros reais de ζ(s) — GUE vs. Poisson

**Status:** LOCKED
**Data de criação:** 2026-08-12
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-12 (Claude Code)
**Test ID:** `DISC-RH-GAP-EXTREME-VALUE-SCALING-001` (sub-teste de `DISC-RH-REAL-001`)
**Commit em que foi travado:** ver histórico git do commit que introduz este arquivo.

## 0. Motivação e o que este teste NÃO é

O item 7 do levantamento de literatura (`../RH_ZETA_ZEROS/PHASE0_TRIAGE_SUMMARY.md`)
é o resultado de Inoue (2026, arXiv:2604.05733, condicional a RH):
liminf dos gaps normalizados `< 0,50895`. Uma afirmação de `liminf` **não é
testável nem falsificável** com dado finito — nenhum teste aqui confirma
ou refuta essa constante. `PHASE0_TRIAGE_SUMMARY.md` já registrou isso
explicitamente: "o mínimo observado é X" não é um critério falsificável.

Este pré-registro testa uma **pergunta proxy genuinamente falsificável**,
motivada pelo mesmo fenômeno (estatística de gaps pequenos), mas
formulada como teoria de valores extremos, não como uma constante
específica: **a forma como o gap mínimo encolhe conforme se observam mais
zeros seguirá a lei de escala prevista pela repulsão de nível GUE, ou a
lei de escala de um processo sem correlação (Poisson)?**

Isso conecta diretamente com achados já estabelecidos nesta sessão: a
correlação de pares GUE (Fase 0, item 1) e a correlação serial negativa
entre gaps consecutivos (`DISC-CLAIM-003`, `REPLICATION_PASSED`) já
mostraram que zeros de zeta têm repulsão de nível de curto alcance. Este
teste pergunta se esse mesmo efeito é forte o suficiente para determinar
a lei de escala do valor extremo (o gap mínimo), que é uma propriedade
estatística diferente (cauda da distribuição, não correlação serial).

## 1. Hipótese exata

Sob teoria de valores extremos padrão: se a densidade de probabilidade
do gap normalizado perto de zero se comporta como `p(s) ~ C·s^β` quando
`s→0`, então o mínimo de `N` gaps escala como `min ~ N^{-1/(β+1)}`.

- **H_GUE:** `β=2` (repulsão de nível GUE/Wigner surmise, já usada na
  Fase 0 e consistente com a densidade suprimida perto de u=0 encontrada
  na correlação de pares) ⟹ **expoente de escala previsto: `-1/3`**.
- **H_Poisson:** `β=0` (sem repulsão de nível — processo sem correlação)
  ⟹ **expoente de escala previsto: `-1`**.
- **Discriminating observable** (Methodology Extensions §1): o expoente
  de escala empírico do gap mínimo vs. tamanho de amostra `N`, testado
  contra os dois valores concorrentes nomeados acima (`-1/3` GUE vs. `-1`
  Poisson) — os dois são modelos estatísticos padrão para processos
  pontuais, bem definidos e mutuamente distinguíveis pela mesma
  estatística.

## 2. Fonte de dado

- Dataset primário: `../RH_ZETA_ZEROS/data/zeros1.txt` (100.000 primeiros
  zeros reais de ζ(s), Odlyzko) — mesma proveniência já documentada em
  `../RH_ZETA_ZEROS/data/PROVENANCE.md`, reaproveitada sem modificação.
- Dataset reservado para o Gate de Replicação (NÃO baixado nem
  inspecionado nesta sessão): `zeros5.txt` da mesma fonte Odlyzko
  (zeros próximos de #10²², regime de altura ainda maior que o `zeros4.txt`
  já usado no Gate de `DISC-RH-ZERO-GAP-RUNS-001`). Reservado
  explicitamente como checagem de robustez fora-do-regime, a ser aberto
  só no Gate (mesmo padrão que funcionou bem no teste anterior desta
  linha).

## 3. Modelo nulo / hipótese concorrente

`H_Poisson` (expoente `-1`) É o modelo concorrente nomeado — não há
necessidade de um nulo separado, já que as duas hipóteses (GUE vs.
Poisson) são mutuamente exclusivas quanto ao valor do expoente e ambas
testadas contra o mesmo intervalo de confiança empírico.

## 4. Estatística de teste

1. Calcular os gaps normalizados dos 99.999 pares consecutivos de
   `zeros1.txt` (mesma fórmula de `../RH_ZETA_ZEROS/PREREGISTRATION.md`
   Seção 1).
2. Grade pré-declarada de tamanhos de bloco: `N ∈ {500; 1.000; 2.000;
   5.000; 10.000}`.
3. Para cada `N`: particionar a sequência de gaps em blocos
   **não-sobrepostos** e **contíguos** de tamanho `N` (99, 99, 49, 19, 9
   blocos respectivamente — números diferentes de blocos por `N` são
   esperados e não são um problema, contanto que ≥8 blocos por `N`, o
   que vale para todos os 5 pontos da grade). Calcular o gap mínimo
   dentro de cada bloco. Tomar a **mediana** dos mínimos de bloco como a
   estimativa pontual de "gap mínimo típico na escala N".
4. Ajustar `log(mediana_min_N) = α + β·log(N)` por mínimos quadrados
   ordinários sobre os 5 pontos da grade.
5. **Intervalo de confiança de 95% em β**: bootstrap (10.000 réplicas,
   seed 20260812) — para cada réplica, para cada `N` da grade,
   reamostrar com reposição os mínimos de bloco daquele `N` (mesma
   contagem de blocos que o original), recalcular a mediana, reajustar o
   mesmo OLS, registrar `β` da réplica.

## 5. Critério de falsificação

- **H_GUE falsificada** se `-1/3` cair fora do IC de 95% de `β`.
- **H_Poisson falsificada** se `-1` cair fora do IC de 95% de `β`.
- **Ambas sobrevivem**: IC largo demais para distinguir — reportado como
  INCONCLUSIVO quanto à escolha entre GUE e Poisson, não como suporte a
  ambas.
- **Nenhuma sobrevive**: `β` empírico está fora dos dois valores
  previstos — resultado informativo por si só (reportar o valor exato de
  `β̂` e seu IC), não forçado a se encaixar em nenhuma das duas hipóteses.
- Nenhuma reformulação da grade de `N`, do método de bloco, ou do
  critério após ver o resultado.

## 6. Correção para comparações múltiplas

Um único ajuste de `β` (não uma busca sobre múltiplos modelos ou
subconjuntos) testado contra dois valores candidatos pré-declarados
(`-1/3`, `-1`) via o mesmo IC — não uma família de testes independentes
no sentido do item 6 do teste anterior desta linha. Nenhuma correção de
Bonferroni aplicável além de checar os dois valores contra o mesmo IC
único.

## 7. O que NÃO está sendo testado

- Isto NÃO testa nem confirma/refuta a constante `0,50895` de Inoue
  (2026) nem qualquer afirmação de `liminf` — essas não são testáveis
  com dado finito.
- Isto NÃO testa, confirma, ou refuta a Hipótese de Riemann.
- Isto NÃO tem conteúdo Tamesis-específico — pesquisa matemática pura
  sobre `riemannZeta` real.
- Um resultado `H_GUE sobrevive` não é uma descoberta matemática nova —
  a repulsão de nível GUE em zeros de zeta já é bem estabelecida na
  literatura (Montgomery, Odlyzko); este teste verifica se ela é forte o
  suficiente para determinar a lei de escala do valor extremo nesta
  amostra específica, com este método específico.
- Nenhum resultado é promovido a `04_FORMAL_RESEARCH_LAB` sem sobreviver
  ao Gate de Replicação, e mesmo assim a promoção não é automática (ver
  `RESEARCH_PIPELINE.md`) — um achado empírico sobre estatística de
  valores extremos de dado finito não é, por si só, um teorema
  demonstrável em Lean.

---

## [Preenchido depois da análise] Resultado

## [Preenchido depois da reexecução adversarial] Veredito adversarial
