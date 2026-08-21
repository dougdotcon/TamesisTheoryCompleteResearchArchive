# Resultados — `constant_fits` (adjudicação de ajustes de constantes do núcleo)

**Linha:** DISC-CORE-NUMERICS-001 · **Frente:** constant-fit-adjudication (DISC-DEC-013)
**Data:** 2026-08-21 · **Critérios:** fixados a priori em `METHODOLOGY_NOTE.md` ·
**Referências:** `PROVENANCE.md` (todas por fetch direto; nenhuma de memória) ·
**Cálculos:** `adjudicate_constants.py` → `adjudication_results.json`, `adjudication.log`;
segunda rota em `second_route_check.log` (aritmética racional/Decimal exata, independente).

## Tabela de vereditos

| Sub-alegação (fonte no núcleo) | Referência externa (proveniência) | Discrepância medida | Consistência como formulado | Identificabilidade |
|:---|:---|:---|:---|:---|
| (a) sin²θ_W = 3/13 = 0,23077, "✅ CONFIRMED, 0,19% error" (`RESEARCH_RESULTS.md:321-328`) | PDG 2025: MS-bar 0,23122(6); on-shell 0,22342(9); efetivo 0,23154(6) | **7,5σ** no esquema MAIS caridoso (MS-bar, exato 293/39); 12,8σ efetivo; 81,7σ on-shell | **INCONSISTENTE como formulado** — o rótulo "0,19%" é aritmeticamente correto (0,195%) mas corresponde a 7,5σ; "CONFIRMED" não sobrevive nem à leitura mais caridosa | **NÃO-IDENTIFICÁVEL (tuning)** — o próprio README declara a varredura contra o alvo: "scanned … to match the observed CODATA value" (`electroweak/README.md:25`; `torsion_angle.py:15` `target_s2w=0.23122`); esquema de comparação também é escolha a posteriori |
| (b) α⁻¹ = Ω^β, Ω=117,038, β=1,033, "137,04, 0,003% error" (`RESEARCH_RESULTS.md:30,61-62`) | CODATA 2022 (NIST): α⁻¹ = 137,035 999 177(21) | Expoente exato x\* = ln α⁻¹/ln Ω = **1,033122317** (existe para QUALQUER alvo positivo → 0 g.l. de teste). Sensibilidade dα⁻¹/dβ ≈ 653: reproduzir α⁻¹ na incerteza CODATA exige β com 11 casas | **Aritmética interna do núcleo NÃO fecha:** Ω^1,033 = **136,956** (erro 0,058%), não 137,04/0,003% — o rótulo "0,003%" pressupõe β=x\* com ≥6 casas, i.e., o expoente É o alvo reescrito | **NÃO-IDENTIFICÁVEL (tuning)** — 1 parâmetro contínuo livre ajustado a 1 dado; ajuste exato por construção, não falsificável; a própria `paper_fine_structure/AUDITORIA.md:4` já diz "coincidência numérica, não derivação" (E0/H1). Adjudicação quantitativa e final |
| (c) bounce: ξ=100 → N=61,7, n_s=0,967 "Planck compatible / Critical Discovery" (`RESEARCH_RESULTS.md:160-167`) | Planck 2018 (arXiv:1807.06209, abstract): n_s = 0,965 ± 0,004 | **0,50σ** (0,65σ usando o valor algébrico 0,9676; conclusão inalterada) | Numericamente consistente (≤2σ) — mas trivialmente: n_s = 1−2/N dá ≈0,967 para QUALQUER modelo classe Starobinsky com N≈60; o número não discrimina o mecanismo de bounce | **NÃO-IDENTIFICÁVEL (tuning)** — ξ varrido em {1, 10, 100, 1000, 3000, 5000, 10000} (`scan_xi.py:46`) e 100 selecionado por dar N>60; alvos codificados: `N_target=60.0`, `ns_target=0.965` (`optimize_inflation.py:97-99`); o código declara: "se conseguirmos N=60, teremos n_s correto automaticamente" (linha 95). **n_s é consequência da seleção de ξ contra o alvo, não predição** |
| (d) ρ_Λ ~ 1/L_H², "✅ CONFIRMED", 8,5×10⁻²⁷ vs 5,8×10⁻²⁷ (×1,46) (`RESEARCH_RESULTS.md:360-371`) | Planck 2018 + CODATA G: ρ_Λ_obs = 5,84×10⁻²⁷ ± 0,11×10⁻²⁷ kg/m³ (±1,8%) | **25σ** (o "observed 5,8e-27" do núcleo bate com Planck a 0,4σ; o "holographic 8,5e-27" não) | **INCONSISTENTE como formulado** — única tolerância pré-declarada no arquivo é "0,1 < ratio < 10 → SUCCESS within 1 order of magnitude" (`holographic_lambda.py:91-92`); nenhuma tolerância sob a qual 46% = "CONFIRMED" existe. Máximo defensável: "ordem de grandeza", como a `lambda/AUDITORIA.md` interna já diz | **NÃO-IDENTIFICÁVEL como predição** — identidade estrutural: a construção ρ_holo = (Lc²/2G)/(4πL³/3) com L=c/H₀ é IDENTICAMENTE ρ_crit, logo ratio ≡ 1/Ω_Λ = 1,460 (o "×1,46" do núcleo é exatamente isso); qualquer fator O(1) de cutoff o absorveria |

## Achados quantitativos centrais

1. **(a)** A discrepância real de 3/13 é **7,5σ** sob a leitura mais caridosa (MS-bar,
   o próprio esquema que o núcleo cita como alvo) — não os "~11σ" estimados na
   entrada do ledger (que usava incerteza menor), mas ainda refutação inequívoca.
   Curiosidade diagnóstica: no esquema on-shell tree-level (1−m_W²/m_Z² = 0,22321
   das massas PDG 2025), 3/13 está a ~82σ — o esquema escolhido para comparação já
   era o único que chegava perto.
2. **(b)** Adjudicação final da identificabilidade: x\* = 1,033122317 existe para
   qualquer alvo (0 graus de liberdade de teste). Adicionalmente, a aritmética
   interna nem fecha: Ω^1,033 = 136,956 (0,058% do CODATA), de modo que o rótulo
   "137,04 / 0,003%" só se obtém usando o expoente-alvo com ≥6 casas. É um ajuste
   de 1 parâmetro a 1 dado, exatamente como a AUDITORIA interna já classificara.
3. **(c)** O único eixo que sobrevive em todo o conjunto: n_s=0,967 está a 0,50σ do
   Planck 2018. Mas o arquivo documenta, no próprio código, que N≈60 era o alvo da
   varredura de ξ e que n_s segue algebricamente de N (1−2/N). Portanto:
   **consistente numericamente, não-identificável como predição**.
4. **(d)** A "predição holográfica" é identicamente ρ_crit; o desvio de 46% é
   1/Ω_Λ por construção. "CONFIRMED" não é sustentado por nenhuma tolerância
   pré-declarada no arquivo (a única existente é 1 ordem de magnitude, que
   sustentaria apenas "ordem de grandeza correta").

## Flags para o orquestrador

- **Reprodução adversarial requerida** apenas para a parte sobrevivente de (c):
  a afirmação estreita "n_s(ξ=100)=0,967 concorda com Planck 2018 a <1σ" (já
  recomputada aqui por segunda rota exata: 0,50σ com o claim arredondado, 0,65σ com
  o valor algébrico 0,9676). O veredito de identificabilidade (tuning) NÃO depende
  dessa reprodução — está documentado no próprio código do arquivo.
- Nenhum outro sub-alegação sobreviveu; (a), (b) e (d) fecham como
  refutadas/não-identificáveis sem necessidade de reprodução adicional.
- Observação para a governança (sem edição aqui): o valor de tabela 4-casas do
  Planck (0,9649±0,0042) não foi fetchado (abstract dá 0,965±0,004); análise de
  sensibilidade no script mostra conclusão idêntica nas duas formas.

*Nenhuma alegação física mais ampla é feita. Vereditos restritos ao vocabulário
autorizado: consistente/inconsistente como formulado; identificável/não-identificável.*
