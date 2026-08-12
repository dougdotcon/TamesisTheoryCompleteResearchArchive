# Sessão 2026-08-12 — Pivô SPARC-002: qual derivação interna de a₀ sobrevive ao dado real

## Contexto

Continuação da sessão que criou `05_DISCOVERY_LAB` e adotou a arquitetura
de três motores (`DISC-DEC-003`). Usuário pediu para priorizar, entre as
três linhas candidatas registradas, aquela com "mais riqueza de
ferramentas... e onde podemos fazer descobertas em curto/médio prazo".
Escolhida `DISC-COSMOLOGY-MOND-SPARC-002` (dado SPARC já baixado e
verificado, modelo concorrente com fórmula pública — ver detalhamento
abaixo).

## O que aconteceu

1. **Busca obrigatória pelo `next_action` original** (extrair de
   `01_TAMESIS_CORE` uma previsão Tamesis quantitativa distinta de MOND
   genérico, com fonte exata arquivo:linha) — resultado **negativo**:
   nenhuma previsão dessas existe. Todo lugar do repositório que toca
   dinâmica galáctica cita `a₀=1,2×10⁻¹⁰` de McGaugh et al. (2016)
   diretamente, e usa a função de interpolação "simple" padrão (Famaey &
   Binney 2005) — as próprias notas de auditoria internas já admitem
   isso (`02_MOND_Emergence/AUDITORIA.md:3`,
   `02_Holographic_Uniqueness/AUDITORIA.md:3`).
2. **Achado adicional, verificado por recálculo direto**: o corpo teórico
   contém duas derivações internas conflitantes de `a₀`, nunca testadas
   uma contra a outra: (A) `a₀=cH₀/(2π)` (Ponte Holográfica,
   `mond_derivation_proof.py:28`) ≈ 1,08×10⁻¹⁰; (B) `a₀=cH₀` (MOND
   Emergence, `index.html:282`) — cuja própria alegação numérica
   "≈1,2×10⁻¹⁰" é aritmeticamente incorreta por fator ~5,7 (o valor real
   de `cH₀` com H₀=70 km/s/Mpc é ~6,8×10⁻¹⁰), independente de qualquer
   comparação com dado externo.
3. **Pivô** (`DISC-DEC-004`): teste redesenhado para perguntar qual das
   duas derivações sobrevive ao contato com dado real, em vez de forçar
   um pré-registro sobre uma previsão inexistente.
4. **Pré-registro travado** (`PREREGISTRATION.md`) ANTES de qualquer
   cálculo: H_A vs. H_B, estatística de teste (ajuste não-linear de
   `g†` + IC bootstrap 95% por galáxia), critério de falsificação, split
   discovery(120)/holdout selado(55) gerado com seed determinístico e
   commitado.
5. **Fórmula do modelo concorrente verificada por fetch direto**:
   McGaugh, Lelli & Schombert (2016, PRL 117, 201101) — `Υ_disk=0,50`,
   `Υ_bul=0,7` M☉/L☉, quadratura com preservação de sinal.
6. **Análise rodada** sobre a amostra de descoberta (120 galáxias, 2327
   pontos). **Bug numérico real encontrado e corrigido durante a própria
   execução**: `scipy.optimize.curve_fit` sem reescala "convergia"
   silenciosamente para o próprio palpite inicial (underflow do
   Jacobiano numérico em escala absoluta ~10⁻¹⁰) — verificado testando
   múltiplos `p0` e vendo cada um "convergir" para perto de si mesmo.
   Corrigido reescalando para unidades de 10⁻¹⁰ antes do ajuste.
7. **Resultado**: `g†` ajustado = 1,1977×10⁻¹⁰ m/s² (0,2% do valor
   publicado — checagem de sanidade passa). IC bootstrap 95% =
   [6,76×10⁻¹¹, 2,78×10⁻¹⁰]. `a₀_A` dentro do IC (H_A sobrevive); `a₀_B`
   fora por fator ~2,5× (H_B falsificada).
8. **Reexecução adversarial independente** (agente separado, código
   próprio, escrito antes de ler o script primário): reproduziu N de
   pontos, N excluídos, e `g†` (0,004% de diferença) — e redescobriu o
   mesmo bug numérico de forma independente antes de corrigi-lo.
   Verificou robustez: ajuste em espaço log dá `g†` mais baixo mas H_B
   continua falsificada por margem grande (~7×); excluir o pior outlier
   não muda o veredito. **Veredito: CONFIRMED.**

## Resultado final desta sessão

`DISC-CLAIM-002` registrado: `preregistered_falsified` (para H_B),
`adversarial_review_verdict: CONFIRMED`, `replication_status:
NOT_SUBMITTED` (holdout selado, Gate de Replicação ainda não acionado).

Ao contrário do piloto anterior (`DISC-CLAIM-001`, p=0,049, zona frágil),
este é um resultado **decisivo e robusto**: a falsificação de H_B não
depende de escolhas de implementação (linear vs. log, com/sem outlier).

## Prohibited claims explícitos para este resultado

- Não é "Tamesis vs. ΛCDM" — ambas H_A e H_B são internas a Tamesis.
- Não confirma a derivação "Ponte Holográfica" como correta — apenas que
  não foi falsificada por este teste.
- A derivação "MOND Emergence" (`a₀=cH₀`) deveria ser corrigida ou
  retirada em `01_TAMESIS_CORE` — este achado é acionável para o corpo
  teórico principal, não apenas uma nota isolada nesta trilha.
- Holdout (55 galáxias) permanece selado — este NÃO é ainda um resultado
  `REPLICATION_PASSED`.

## Próxima decisão (não tomada nesta sessão)

O resultado é forte o suficiente para justificar o Gate de Replicação
completo (abrir o holdout com um terceiro agente independente + adversário
de nulo dedicado). Reportado ao usuário antes de acionar, já que abrir o
holdout é um recurso de uso único — não pode ser "reselado" para um teste
cego de verdade depois.
