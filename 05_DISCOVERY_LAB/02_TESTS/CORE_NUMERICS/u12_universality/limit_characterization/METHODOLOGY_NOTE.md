# Pré-registro — frente `u12-limit-characterization` (onda 2)

**Linha:** DISC-CORE-NUMERICS-001. **Governança:** DISC-DEC-014.
**Data/hora de gravação:** 2026-08-21T22:18Z — gravado ANTES de qualquer
execução numérica desta frente (verificável por timestamps).

## Objeto herdado (onda 1, confirmado adversarialmente)

Ensemble: permutação uniforme de `[n]`; cada ponto rerroteado
independentemente com prob. `c/n` para destino uniforme; observável
φ(n,c) = fração esperada de pontos cíclicos. Estabelecido: o limite
φ_∞(c) existe, tem cauda ~c^{-1/2}, e NÃO é `(1+c)^{-1/2}` (refutado a
até 101σ). Objeto-limite (construção adversarial, `adv_continuum.py`):
ciclos ~ Poisson–Dirichlet(1); K ~ Poisson(c) reroteamentos em posições
uniformes com destinos uniformes; massa cíclica = ciclos livres de
reroteamento + segmentos ao longo dos ciclos do mapa de saltos g.

## Declaração de estado inicial (honestidade)

Antes de escrever esta nota, o agente desta frente completou EM PAPEL
(sem nenhuma execução numérica própria) uma derivação probabilística do
limite via processo de exploração da trajetória, que produz uma forma
fechada candidata. Esta nota pré-declara o protocolo numérico e os
critérios de aceitação ANTES de qualquer execução; os únicos números já
vistos são os da onda 1 (públicos no repositório: grade
c ∈ {0.5, 1, 2, 5, 10, 20, 50} de `adv_continuum.json`). Por isso o
protocolo de validação usa (a) valores de c FORA da grade da onda 1,
(b) sementes novas, (c) predições por-K (condicionais no número de
reroteamentos) que a onda 1 nunca mediu — três camadas que a derivação
não pôde ter "ajustado".

## (i) Programa analítico (pré-declarado)

1. **Derivação principal (trajetória):** computar P(ponto típico é
   cíclico) no limite n→∞ pelo processo de exploração: revelar π passo a
   passo ao longo da órbita de f a partir de um ponto típico x₀;
   identificar as taxas de eventos por unidade de massa percorrida t
   (reroteamento: c; fechamento-π num início de arco: m_t/(1−t);
   salto em massa já visitada: terminal), e reduzir P(cíclico) a uma
   expectativa do tipo Feynman–Kac sobre o processo de Poisson de
   reroteamentos, resolvida por PGFL. Toda etapa deve ser justificada
   (quais pontos têm pré-imagem de π revelada; por que cada evento é
   terminal; unicidade do fechamento contendo x₀). Resultado esperado:
   ou uma forma fechada, ou uma representação integral/equação funcional
   bem definida — ambas são desfechos legítimos.
2. **Verificação independente de baixa ordem:** derivar exatamente, por
   argumento probabilístico direto e independente da derivação 1, o
   coeficiente de primeira ordem a₁ em φ_∞(c) = 1 − a₁c + O(c²)
   (cálculo com exatamente 1 reroteamento sobre comprimento de ciclo
   size-biased ~ U(0,1)), e o coeficiente exato φ₁ = E[massa cíclica |
   K=1]. Qualquer forma fechada candidata DEVE reproduzir esses valores
   derivados EXATAMENTE (não numericamente).
3. **Assintótica c→∞:** derivar o coeficiente exato A da cauda
   φ_∞(c) ~ A·c^{-1/2} a partir da representação obtida.
4. **Predições por-K:** se a derivação 1 der forma fechada, extrair as
   predições condicionais φ_K = E[massa cíclica | K reroteamentos]
   (K = 0, 1, 2, …) — são predições paramétricas rígidas, testáveis por
   MC condicional, que nenhum ajuste de curva em c poderia imitar.

## (ii) Programa numérico (pré-declarado ANTES de rodar)

Implementação PRÓPRIA do objeto-limite (estrutura independente de
`adv_continuum.py`: truncamento do stick-breaking em resto < 1e−12,
aritmética modular para o avanço circular, medição SEPARADA de massa
livre e massa de segmentos). Tudo em
`limit_characterization/` (scripts + .json + .log). Sementes e tamanhos
fixados AGORA:

- **T1 — grade de validação held-out (c fora da grade da onda 1):**
  c ∈ {0.05, 0.25, 0.75, 1.5, 3, 7, 15, 30, 70, 100};
  N = 200.000/célula; `SeedSequence(20260821)`, spawn por célula em
  ordem de c crescente.
- **T2 — cross-check na grade da onda 1 com sementes novas:**
  c ∈ {0.5, 1, 2, 5, 10, 20, 50}; N = 200.000/célula;
  `SeedSequence(31337)`.
- **T3 — MC condicional por-K:** K ∈ {1, 2, 3, 4, 5} reroteamentos
  determinísticos (sem Poisson); N = 400.000/célula;
  `SeedSequence(64206)`. Compara com φ_K derivado.
- **T4 — decomposição:** nas células de T2, comparar a massa livre
  medida com o valor exato derivável E[massa livre] = (1−e^{−c})/c
  (size-biasing de PD(1); derivação na DERIVATION.md) — valida o
  simulador em nível de componente.
- **Runtime alvo:** ≤ 30 min total; se estourar, reduzir N
  uniformemente para 100.000 (T1/T2) e 200.000 (T3), DECLARANDO no log.

## (iii) Critérios de aceitação de QUALQUER forma fechada (pré-declarados)

Uma forma fechada candidata só é promovida a "forma derivada aceita" se
TODAS as condições valerem:

1. **Consistência analítica exata:** reproduz exatamente a₁ e φ₁ do
   programa analítico item 2 (derivados por rota independente), e o
   expoente −1/2 da cauda estabelecido pela onda 1.
2. **Validação held-out (T1):** χ² = Σ z² sobre as 10 células held-out,
   com z = (φ_MC − φ_forma)/SEM. Aceita se p(χ²₁₀) ≥ 0.01 E |z| < 4 em
   toda célula. (Nenhum parâmetro é ajustado em T1 — a forma vem da
   derivação, com zero parâmetros livres.)
3. **Cross-check (T2):** mesmo critério (χ²₇, p ≥ 0.01, |z| < 4).
4. **Por-K (T3):** |z| < 4 em cada K ∈ {1..5} e χ²₅ com p ≥ 0.01.
5. **Decomposição (T4):** massa livre MC vs (1−e^{−c})/c com |z| < 4
   por célula (valida o simulador; falha aqui invalida o SIMULADOR, não
   a forma, e exige correção antes de qualquer veredito).

Se qualquer critério falhar: a forma é rebaixada a "aproximação
candidata" e o desfecho reportado é a representação
integral/tabulação + "forma fechada não identificada" (ou o que
sobreviver). Uma forma que apenas ajusta bem numericamente sem passar
pelo item 1 NUNCA é aceita.

**Correção múltipla/olhada única:** os testes T1–T4 serão rodados UMA
vez com as sementes acima; não haverá reexecução seletiva. Bugs
descobertos serão corrigidos com reexecução COMPLETA e novas sementes
(documentado), nunca reexecução parcial.

## (iv) Checagem de literatura (pré-declarada)

Busca honesta (WebSearch) por: modelos de mapeamento aleatório
interpolando permutação↔mapping ("random mapping", "perturbed random
permutation", "cyclic points", "p-mappings", Aldous–Pitman,
Hansen–Jaworski, criptografia de grafos funcionais). Se o limite (ou a
forma fechada) já existir na literatura, IDENTIFICÁ-LO é o achado — será
citado com proveniência e NÃO apresentado como novo.

## Entregáveis

`METHODOLOGY_NOTE.md` (este), `DERIVATION.md` (analítico completo),
`limit_sim.py` + `limit_results.json` + `limit_sim.log` (T1–T4),
`tabulation.json` (tabulação de alta precisão da forma final/quadratura),
`RESULTS_SUMMARY.md` (PT: derivado vs conjecturado vs ajustado +
veredito + flag adversarial).
