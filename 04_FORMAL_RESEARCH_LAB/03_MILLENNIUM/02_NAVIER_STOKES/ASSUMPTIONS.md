# Hipóteses

status: `AUDITED_NOT_ESTABLISHED` (as hipóteses foram identificadas e
separadas por força de prova nesta rodada; nenhuma delas foi provada
para Navier–Stokes 3D geral).

Para que qualquer versão condicional do argumento pressão–alinhamento
funcione, as seguintes hipóteses precisariam valer simultaneamente. Cada
uma é marcada com seu status de verificação nesta sessão.

## H1 — Existência local de solução forte

Dado `u₀ ∈ H^s`, `s > 5/2`, existe `T* > 0` e solução forte suave em
`[0,T*)`. **Status: clássico, verificado por citação** (existência local
padrão via ponto fixo/energia; parte do arsenal usado por BKM 1984 — ver
`REVIEWS/AUDIT_REPORT.md`).

## H2 — Critério BKM aplicável

Se a solução deixa de ser suave em `T*`, então
`∫₀^{T*} ‖ω(·,t)‖_∞ dt = ∞`. **Status: teorema clássico, verificado por
citação** (Beale–Kato–Majda 1984).

## H3 — "Alignment Gap" quantitativo e uniforme no tempo

`⟨α₁(t)⟩_Ω ≤ 1 - δ₀` para `δ₀ > 0` fixo, para todo `t ∈ [0,T*)`, ONDE
`T*` é o tempo de blow-up hipotético (ou seja, a hipótese precisa valer
justamente na janela de tempo em que a solução ainda não se sabe se é
regular — não é uma hipótese sobre o dado inicial, é uma hipótese sobre
o comportamento da própria solução até o momento em que ela poderia
falhar). **Status: `NOT_AUDITED` / não provada.** Consistente com dados
de DNS citados no documento legado (`⟨α₁⟩ ≈ 0.15`, ver
`ANALISE_CRITICA_NS.md`), mas DNS não é prova — é evidência numérica em
regime finito-Reynolds, finito-tempo, finita-resolução; não estabelece
um limite uniforme válido para toda solução de Leray–Hopf hipotética
perto de um blow-up.

**Achado desta sessão (verificado por computação, não por citação):**
`H3` isolada — sem uma hipótese adicional de TAXA (ver H4) — é
**insuficiente** mesmo dentro da classe de sistemas mais favorável a
ela: no sistema de Euler restrita (Vieillefosse 1982), `α₁ → 0` ao longo
de toda trajetória que explode em tempo finito (ver
`COUNTEREXAMPLES/restricted_euler_alignment_gap.md`). `H3`, sozinha,
não impede blow-up nem no modelo mais favorável possível a ela.

## H4 — "Rotation/Pressure Dominance" (Lemma 3.1 do documento legado)

O termo de pressão no crescimento de `α₁` domina o termo de vorticidade
e tem o sinal que reduz `α₁`, com uma TAXA quantitativa suficiente para
compensar o "stretching":
`⟨σ⟩ ≤ (1 - δ₀/2)⟨λ_max⟩` (Passo 3 do esboço legado). **Status:
`NOT_AUDITED` / explicitamente marcada como `🔴 NÃO PROVADO` no próprio
documento legado** (`ANALISE_CRITICA_NS.md`, seção 4, GAP 1), que
também registra que "o termo de vorticidade pode ser positivo". Esta
sessão não encontrou nem produziu uma prova de H4; não é uma afirmação
de álgebra linear finita (ver `FORMAL/PressureHessianAlgebra.lean`,
comentário final) — depende do comportamento não-local (tipo
Biot–Savart) da parte anisotrópica do Hessiano de pressão, que não tem
fórmula fechada local.

## Observação sobre a estrutura lógica

`H3 ⟹ regularidade` só é válida junto com `H4` (Passos 3–6 do esboço).
`H3` sozinha (a "afirmação de alinhamento" propriamente dita, sem a
componente de taxa) não é a barreira contra blow-up — o contraexemplo
computacional desta sessão mostra isso diretamente. Toda a força
regularizadora precisa estar em `H4`, cuja prova é, pela avaliação desta
sessão, estruturalmente da mesma dificuldade que a própria regularidade
global: é uma condição a priori sobre a solução até um tempo de blow-up
hipotético (não uma condição sobre o dado inicial), na mesma família dos
critérios de Constantin–Fefferman (1993) e Prodi–Serrin, que desde sua
publicação nunca foram verificados a priori para uma solução de
Navier–Stokes 3D genérica. Isto é o motivo do `stop_condition` desta
frente ter sido acionado — ver `REVIEWS/AUDIT_REPORT.md`.

## DNS / K41

Dados numéricos (DNS) e heurísticas de Kolmogorov (K41) **não são
hipóteses de uma prova**. Servem como evidência de plausibilidade para
H3, nunca como substituto de H4.
