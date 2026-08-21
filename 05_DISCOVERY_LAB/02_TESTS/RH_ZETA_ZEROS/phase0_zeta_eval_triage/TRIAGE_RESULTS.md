# RH-REAL — Fase 0 (continuação): triagem dos itens 5, 6, 10 — RESULTADOS

**Status:** `evidence_level: exploratory_only`. NÃO é um teste
pré-registrado; nada aqui é descoberta, alegação sobre RH, ou resultado
"travado". Continuação da triagem de `PHASE0_TRIAGE_SUMMARY.md`
(2026-08-12) autorizada por `DISC-DEC-013`; a `stop_condition` de
`DISC-RH-REAL-001` proíbe tratar qualquer linha desta tabela como
resultado pré-registrado. Método e critérios foram fixados **antes** da
computação em `TRIAGE_NOTE.md` (com um único adendo datado,
pré-computação). Data: 2026-08-21.

**Definições dos itens:** reconstruídas (o levantamento original de
2026-08-12 não foi persistido verbatim no repositório) — ver
`TRIAGE_NOTE.md` §0–1, com as 4 citações verificadas por fetch direto no
arXiv em 2026-08-21 (arXiv:math/0206018 CFKRS; arXiv:1509.06827
Radziwiłł–Soundararajan; arXiv:1202.4713 Fyodorov–Hiary–Keating;
arXiv:1612.08575 Arguin–Belius–Bourgade–Radziwiłł–Soundararajan).

**Validação do motor de ζ (pré-requisito, PASSOU):** Riemann–Siegel
Z(t) vetorizado (numpy, fases em longdouble), validado contra mpmath e
contra os zeros reais de Odlyzko — ζ(2)=π²/6 exato; ζ(1/2) confere com
−1,46035450880…; `zetazero(1)`=14,134725142 confere com a 1ª linha de
`data/zeros1.txt`; 42 pontos vs `mp.siegelz` em t∈[2×10³,10¹¹] dentro
das tolerâncias por faixa (máx 8,2×10⁻⁵ / 6,3×10⁻⁶ / 1,1×10⁻⁴); Z troca
de sinal em 20/20 zeros amostrados de Odlyzko e conta exatamente 100
mudanças de sinal sobre os 100 primeiros zeros. Um bug real (constante
2π em float64 na redução de fase, erro ~2,5×10⁻⁴ em t~10¹¹) foi
detectado e corrigido PELA validação antes de qualquer uso —
`validation_zeta_eval.{log,json}` e `..._run1_FAILED.log`.

---

## Tabela de triagem (mesmo espírito da tabela de 2026-08-12)

| Item | O que foi computado | Resultado | Admite pergunta pré-registrável falsificável (com modelo concorrente NOMEADO)? | Recomendação |
|---|---|---|---|---|
| **5. Momentos de ζ na linha crítica** (Hardy–Littlewood 1918 k=1; Ingham 1926 k=2; Keating–Snaith 2000 / CFKRS arXiv:math/0206018 k≥3) | Momentos janelados `(1/(T−T₀))∫_{T₀}^{T}\|ζ(1/2+it)\|^{2k}dt`, k=1,2,3, grade de 560.001 pontos em t∈[2000, 30000] (passo 0,05; 17 s); fator aritmético a₂ (auto-checagem vs 6/π², dif. rel. 3×10⁻⁸) e a₃=0,049322 por produto de Euler | k=1: razão emp/teorema = 0,9985–1,0001 (pipeline de momentos valida contra teorema). k=2: 1,117–1,121× o termo líder de Ingham (log⁴T) — termos de ordem inferior ~12% e caindo devagar. k=3 (conjectural): **13,4–17,7×** o termo líder KS `42·a₃/9!·log⁹T` — em T acessível os termos de ordem inferior DOMINAM o momento | **Parcial.** Concorrente nomeável existe (polinômio completo CFKRS vs "só termo líder com constante livre"), mas: (a) k=1,2 são teoremas — não falsificáveis; (b) para k=3 o termo líder sozinho é inobservável em T acessível (fator ~15), então o teste teria de usar o polinômio CFKRS completo de grau 9 — cuja verificação numérica **já foi publicada pelos próprios CFKRS** no paper citado. Seria replicação, não descoberta | **Não priorizar.** Viável e barato, mas pergunta genuína = replicar numérica já publicada. Só reconsiderar se um observável derivado (ex.: flutuação do resto) for formulado com concorrente real |
| **6. TCL de Selberg para log\|ζ\|** (Selberg 1946; prova: Radziwiłł–Soundararajan arXiv:1509.06827) | Em T∈{10⁴,10⁶,10⁸,10¹⁰}: N=4000 pontos t~U[T,2T] (seed 20260821), X=log\|Z(t)\|; média, variância±EP, assimetria, curtose, KS vs N(0,σ²) para **modelo A (Selberg): σ²=(1/2)loglogT** vs **modelo B (lognormal ingênuo, nomeado): σ²=loglogT** (54 s total) | Média ≈ 0 em todas as alturas (−0,013…+0,012 ✓). Variância empírica 1,614→2,347 fica **entre** A e B em TODAS as alturas (~11σ de distância de ambos); crescimento com loglogT tem inclinação ~0,80 (entre 1/2 e 1). Assimetria −0,75 a −0,81 e curtose +1,2 a +1,9 persistentes: em altura acessível a distribuição ainda está longe de Gaussiana (KS p<10⁻⁸ contra A em todas as alturas) — convergência lentíssima do TCL, consistente com o conhecido na literatura | **Fraco.** O enunciado central é **teorema provado** — não é falsificável; o que restaria é a taxa de convergência/correções de altura finita, e a triagem mostra que em T≤10¹⁰ NENHUM dos dois modelos assintóticos descreve os dados (ambos rejeitados a ~11σ) — qualquer pré-registro exigiria um modelo de correção finita explícito, que a literatura ainda dá só parcialmente | **Não priorizar como teste de modelo assintótico** (ambos os concorrentes já "falham" trivialmente em altura finita — resultado não informativo). Possível reuso: os números servem de baseline de calibração para o item 10 |
| **10. Máximo de \|ζ\| em intervalos curtos — FHK** (arXiv:1202.4713; ordem líder provada arXiv:1612.08575) | Em T∈{10⁵,10⁷,10⁹}: M=300 intervalos de comprimento 2π, inícios U[T,2T] (seed 20260821), grade 256 pts/intervalo (viés de grade medido vs 1024 pts: +0,0003…+0,0021); M*=max log\|Z\|; regressão ponderada de mean(M*)−loglogT sobre logloglogT. Extensão a 10¹¹ PULADA por regra de custo pré-declarada (piloto: 7,7 s/intervalo → projeção 771 s > teto 300 s; registrado no log). 5m48s total | mean(M*) = 2,088→2,599 crescendo com loglogT ✓; sd(M*) ≈ 0,44–0,56 (O(1) como previsto). **Inclinação = −0,408 ± 0,184** vs **FHK: −0,75** (z=+1,9) vs **REM/iid: −0,25** (z=−0,9) — **compatível com ambos os modelos**: potência insuficiente nesta configuração, exatamente como antecipado na nota (amplitude de logloglogT é só 0,216 entre 10⁵ e 10⁹) | **Sim — o melhor dos três.** Dois modelos concorrentes NOMEADOS com coeficientes numéricos distintos (−3/4 vs −1/4), questão viva (só a ordem líder está provada), observável discriminante bem definido (inclinação em logloglogT), e nenhuma verificação numérica desta discriminação específica conhecida por nós. A triagem entrega a conta de potência com números reais: com M≈2000/altura e alturas {10⁵,10⁷,10⁹,10¹¹}, EP projetado da inclinação ≈ 0,06 → separação ~8σ entre os modelos; custo dominado por 10¹¹ (~7,7 s/intervalo ⇒ ~4–5 h) — pesado mas viável | **Priorizar.** Único dos três com pergunta genuinamente falsificável e não-replicativa. Um pré-registro real precisaria: grade de alturas e M fixados a priori pela conta de potência acima, viés de grade tratado (grade ≥1024 pts ou correção pré-declarada), holdout de altura (ex.: 10¹¹ selado) e decisão trinária (FHK / REM / nenhum) com limiares declarados |

---

## Observações de disciplina

- Nenhum arquivo pré-existente de `RH_ZETA_ZEROS/` foi modificado; tudo
  desta frente vive em `phase0_zeta_eval_triage/`.
- Nenhuma computação em segundo plano foi deixada rodando; todos os
  scripts rodaram em primeiro plano dentro dos tetos declarados (maior:
  item 10, 5m48s).
- Subamostragens/desvios do plano e suas razões: (i) integrais janeladas
  T₀=2000 no item 5 e tolerâncias por faixa na validação — adendo datado
  da `TRIAGE_NOTE.md`, decididos ANTES dos itens; (ii) extensão 10¹¹ do
  item 10 pulada por regra de custo pré-declarada — registrada no
  próprio log do item.
- **Nada aqui reivindica progresso sobre RH** nem sobre qualquer das
  conjecturas; os números de itens 5 e 6 são consistências com teoria
  conhecida, e o item 10 produziu deliberadamente um intervalo que
  contém ambos os modelos (triagem de potência, não teste).
- Recomendações são apenas recomendações: **nenhum pré-registro foi
  desenhado nem travado nesta fase.** A escolha de seguir (ou não) com o
  item 10 é decisão de governança futura, fora desta frente.

## Arquivos desta frente

`TRIAGE_NOTE.md` (nota pré-computação + adendo único datado),
`rs_zeta.py` (motor RS), `validate_zeta_eval.py` +
`validation_zeta_eval.{log,json}` + `validation_zeta_eval_run1_FAILED.log`
(validação, com histórico da falha corrigida), `item5_moments.py` +
`.log/.json`, `item6_selberg_clt.py` + `.log/.json`, `item10_fhk_max.py`
+ `.log/.json`, este `TRIAGE_RESULTS.md`.
