# Esboço — YM-LIMIT-001

Status anterior: `NO_EXECUTION`. Esta rodada executa o primeiro resultado
permitido pelo escopo: um teorema de insuficiência com dois contraexemplos
abstratos. **Não** executa a construção Clay (não é o objetivo desta
frente — ver `AGENTS.md` e `PORTFOLIO_REVIEW_AFTER_SOBOLEV_CHAIN.md`).

## Teorema de insuficiência (nível abstrato)

**Enunciado informal.** Sejam \((X, d)\) um espaço métrico e
\(\{a_n\}_{n\in\mathbb N}\) uma família de "gaps de volume finito"
\(a_n \in \mathbb R_{>0}\), ou uma família \(\{\mu_n\}\) de objetos
associados (medidas, operadores). As duas hipóteses

```text
(H_tight)  {a_n} (ou {μ_n}) é limitada / tight
(H_gap)    a_n > 0 para todo n   (gap de volume finito positivo)
```

**não implicam**, sem hipótese adicional:

```text
(C1)  existe um único limite (todas as subsequências convergem
      para o mesmo ponto)
(C2)  o limite, quando existe, tem gap ≥ c > 0 para algum c
      independente de n
```

**Prova (por contraexemplo, dois construídos independentemente):**

### Contraexemplo 1 — falha de (C1) apesar de gap uniforme

Define-se \(a_n = 2\) se \(n\) par, \(a_n = 3\) se \(n\) ímpar (formalizado
como `toyGap` em `FORMAL/InsufficiencyToyModel.lean`). Então:

- \(\forall n,\ a_n \ge 2\) — gap uniforme, hipótese (H_gap) satisfeita na
  forma mais forte possível (uniforme, não apenas pontual).
- \(\{a_n\}\) é limitada, logo tight/relativamente compacta (análogo
  elementar de Prokhorov via Bolzano–Weierstrass).
- A subsequência dos pares converge para 2; a subsequência dos ímpares
  converge para 3. Como \(2 \ne 3\), a sequência completa **não converge**
  — não existe teoria limite única.

Isto é exatamente a instância abstrata do erro identificado no
`stop_condition` desta frente: confundir "existe subsequência
convergente" (verdadeiro, por Bolzano–Weierstrass/Prokhorov) com "existe
uma única teoria limite" (falso, em geral).

Lean: `toyGap_uniform_lower_bound`, `toyGap_even_subseq`,
`toyGap_odd_subseq`, `toyGap_no_unique_continuum_limit`.

### Contraexemplo 2 — falha de (C2): gap positivo em cada n, mas não uniforme

Define-se \(a_n = \dfrac{1}{n+1}\) (formalizado como
`toyFiniteVolumeGap`). Então:

- \(\forall n,\ a_n > 0\) — hipótese (H_gap) satisfeita pontualmente.
- \(a_n \to 0\); não existe \(c>0\) com \(a_n \ge c\) para todo \(n\) —
  a hipótese de gap **não é uniforme**.

Isto formaliza o "GAP 2" do documento legado
(`ANALISE_CRITICA_YM.md`, seção 4): "gap finito-volume não implica gap
uniforme no limite" (= `YM-GAP-002` em `GAP_REGISTER.yaml`).

Lean: `toyFiniteVolumeGap_pos`,
`finite_volume_gap_does_not_survive_without_uniform_bound`.

### Elo espectral (não formalizado em Lean nesta rodada)

Mesmo assumindo (H_gap) na forma uniforme e uma noção de convergência tão
forte quanto convergência forte de resolvente (mais forte que convergência
fraca de medidas), a literatura de análise espectral estabelece que o
espectro do limite não pode *expandir*, mas pode *contrair repentinamente*
(ver `REVIEWS/AUDIT_REPORT.md`, seção Verificado). Um contraexemplo
concreto — operador de multiplicação \(H_n = 0 \oplus M_{f_n}\) com
\(f_n(x) = \max(x, 1/n)\) em \(L^2([0,1])\), espectro
\(\{0\}\cup[1/n,1]\), gap \(1/n \to 0\), convergindo em norma para
\(H = 0 \oplus M_{\mathrm{id}}\) com espectro \([0,1]\) (gap nulo) — está
descrito em `COUNTEREXAMPLES/ABSTRACT_COUNTEREXAMPLES.md#contraexemplo-3`.
**Este terceiro contraexemplo não foi formalizado em Lean nesta rodada**
(exigiria infraestrutura de operadores em espaço de Hilbert e cálculo de
espectro não disponível/não construída neste ciclo) — registrado como não
tentado, motivo: escopo de tempo de uma frente paralela de auditoria, não
limite estrutural do Mathlib.

## Onde esta rodada para (`stop_condition`)

O `stop_condition` desta frente é: **não confundir uma subsequência
convergente com a existência de uma única teoria limite**. Esta auditoria
não tenta ir além disso na direção da construção completa — não afirma
(nem tenta provar) que a medida de Yang–Mills real tem ou não tem limite
único; apenas que a cadeia de hipóteses citada na literatura secundária
não basta para concluir isso, com dois contraexemplos formais que tornam
essa insuficiência precisa e verificável. Ver `stop_condition_triggered`
no retorno estruturado desta sessão — o gatilho foi **respeitado
proativamente**: o teorema de insuficiência é construído exatamente para
não cometer esse erro, não porque a execução foi interrompida por tê-lo
cometido.
