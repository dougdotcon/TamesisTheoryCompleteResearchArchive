# Esboço — auditoria da hipótese pressão–alinhamento

status: `AUDIT_COMPLETE_STOP_CONDITION_TRIGGERED`. Este documento NÃO é
um esboço de prova de regularidade global; é o registro de uma
auditoria que encontrou uma correção necessária e, ao tentar
fortalecê-la para uma forma que ainda pudesse funcionar, chegou ao
critério de parada definido para esta frente. Ver `STOP CONDITION`
abaixo.

## A cadeia sob auditoria (linguagem do documento legado)

```
Passo 1: Pressure Dominance    |R_press|/|R_vort| ≥ C₀·L/a
Passo 2: Alignment Gap         ⟨α₁⟩_Ω ≤ 1 - δ₀
Passo 3: Stretching Reduction  ⟨σ⟩ ≤ (1-δ₀/2)⟨λ_max⟩
Passo 4: Enstrophy Bound       Ω_max finito
Passo 5: L∞ Bound              ‖ω‖_∞ limitado
Passo 6: BKM                   regularidade global
```

Passo 6 é um teorema clássico correto (Beale–Kato–Majda 1984, ver
`KNOWN_RESULTS_MATRIX.md`). Passos 4–5 são Gronwall/Sobolev padrão
**se** o Passo 3 já estiver estabelecido — nenhuma novidade aí. Todo o
conteúdo não-trivial da hipótese está nos Passos 1–3.

## O que esta sessão fez

1. Separou Passo 2 ("Alignment Gap") do Passo 3 ("Stretching
   Reduction") e testou Passo 2 isoladamente, em um sistema onde ele
   pode ser verificado por computação: a equação de Euler restrita
   (Vieillefosse 1982), que é exatamente o truncamento de Navier–Stokes
   que zera a parte anisotrópica e não-local do Hessiano de pressão —
   o objeto central de Passo 1/H4.
2. Resultado (verificado por computação nesta sessão, não por
   citação): em todas as 6 condições iniciais aleatórias testadas, o
   sistema explode em tempo finito **enquanto** `α₁ → 0` (desalinhamento
   quase perfeito com `e₁`) — ver
   `COUNTEREXAMPLES/restricted_euler_alignment_gap.md`.
3. Conclusão: Passo 2, tomado isoladamente (sem a componente de TAXA do
   Passo 1/Lemma 3.1), não carrega nenhum conteúdo regularizador. Isto
   é uma **correção** à arquitetura do argumento legado — não uma
   refutação de Navier–Stokes (o sistema testado descarta por
   construção o termo ao qual a hipótese atribui o efeito
   regularizador; ver ressalva na seção "O que isto NÃO mostra" do
   arquivo de contraexemplo).
4. Consequência: toda a força do argumento tem que estar inteiramente
   no Passo 1/Lemma 3.1 — a afirmação quantitativa sobre o SINAL e a
   TAXA da parte anisotrópica do Hessiano de pressão. Esta sessão
   tentou avaliar se essa afirmação está ao alcance de uma prova ou
   correção nesta rodada.

## Por que o Passo 1/Lemma 3.1 não foi, e não deveria ser, forçado nesta
   rodada

A parte anisotrópica do Hessiano de pressão não tem fórmula local
fechada: é dada por uma integral singular (tipo Biot–Savart/Riesz) do
campo de deformação sobre todo o domínio (consequência da equação de
Poisson `-Δ(H_p)_{ij} = \dots` — não uma função pontual de `A(x), ω(x)`
apenas). Provar seu sinal médio exigiria, no mínimo, um controle
quantitativo dessa integral não-local até um tempo de blow-up
hipotético — ou seja, uma hipótese sobre o comportamento da própria
solução no limiar da singularidade, não sobre o dado inicial.

Isto coloca a hipótese na mesma classe estrutural dos critérios de
regularidade condicional já publicados e nunca verificados a priori
para uma solução geral: Constantin–Fefferman (1993, direção da
vorticidade Lipschitz), critérios tipo Prodi–Serrin, e — mais perto do
espírito exato desta hipótese — o critério de Evan Miller (2020, ARMA)
via autovalor intermediário da deformação, que contorna a interação
não-local vorticidade–deformação de outra forma e ainda assim não
resolve o problema geral. Nenhum destes, desde sua publicação, foi
estabelecido a priori para soluções gerais de Navier–Stokes 3D — é
precisamente esse o motivo de nenhum deles ter fechado o problema do
Milênio.

## STOP CONDITION

Critério de parada definido para esta frente:
> "hipótese equivalente a regularidade global ou contraexemplo
> explícito"

**Contraexemplo explícito**: obtido para a forma nua do Passo 2 (ver
acima e `COUNTEREXAMPLES/`). Isto por si só já satisfaz o critério de
parada — a frente para aqui quanto a essa forma da hipótese.

**Equivalência estrutural à regularidade global**: para a forma
fortalecida (Passo 1/Lemma 3.1 com a componente de taxa, a única que
sobreviveria ao contraexemplo), esta sessão não encontrou nem uma prova
nem uma redução formal a "isto é literalmente o mesmo enunciado que
regularidade global" (não é uma equivalência lógica bicondicional
provada). O que esta sessão encontrou é uma observação estrutural, não
uma prova: a hipótese fortalecida exige um controle a priori sobre a
solução até o tempo de blow-up hipotético, exatamente a mesma
dificuldade central de todo critério de regularidade condicional
conhecido publicado desde 1984 (BKM) — nenhum dos quais jamais foi
verificado a priori. Continuar tentando fechar o Lemma 3.1 nesta
auditoria seria reproduzir, sem ferramentas novas, um problema aberto
documentado desde pelo menos Constantin–Fefferman (1993).

**Ação tomada**: PARAR aqui. Não forçar uma prova do Lemma 3.1/Passo 1.
Registrar o estado exato em `GAP_REGISTER.yaml` e reportar como
`REFUTED_HYPOTHESIS` (para a forma nua, Passo 2 isolado) com
`stop_condition_triggered = true` (para a forma fortalecida, Passo
1/Lemma 3.1).

## O que um próximo ciclo precisaria para avançar de fato

1. Uma estimativa **quantitativa e local** (não apenas de sinal) para a
   parte anisotrópica do Hessiano de pressão em termos de `A`, `ω` e
   escala local — isto é matemática nova, não uma auditoria de
   literatura.
2. Ou: aceitar a hipótese como estritamente condicional (teorema
   `Lemma 3.1 ⟹ regularidade`, nunca `regularidade` sozinha) e restringir
   o escopo a uma classe de soluções onde `Lemma 3.1` seja verificável
   por outros meios (ex.: soluções autossimilares — já excluídas por
   Nečas–Růžička–Šverák 1996 — ou classes com simetria adicional).
3. Nenhuma das duas rotas está ao alcance de uma sessão de auditoria de
   literatura; ambas exigem pesquisa matemática original.
