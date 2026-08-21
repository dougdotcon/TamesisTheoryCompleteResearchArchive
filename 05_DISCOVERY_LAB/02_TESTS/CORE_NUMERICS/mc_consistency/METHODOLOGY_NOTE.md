# Nota de metodologia — `mc_consistency` (consistência interna do valor congelado de M_c)

**Frente:** `mc-internal-consistency`, linha `DISC-CORE-NUMERICS-001`
(autorizada por `DISC-DEC-013`, 2026-08-21).

**Status: critérios de decisão fixados ANTES de qualquer computação de
comparação.** Mesma disciplina de `METHODOLOGY_NOTE.md` usada em toda a
história da linha TRI-RG (p.ex.
`05_DISCOVERY_LAB/02_TESTS/TRI_RG/transfer_entropy/METHODOLOGY_NOTE.md`):
a nota é finalizada antes do primeiro cálculo contra referência; se uma
correção for necessária depois, no máximo UM adendo datado e limitado —
nunca reescrita silenciosa.

## A alegação sob teste, precisamente

O contrato congelado `tamesis-mc-v1.0`
(`01_TAMESIS_CORE/02_Experimental_Validation/Quantum_Classical_Transition/tamesis_mc_v1/config/tamesis_mc_v1.yaml`,
congelado em 2026-07-26) fixa

```
M_c = m_P * (a0 / a_P)^(1/8) = 5.292674126388712e-16 kg
a0 = c * H0,   H0 = 70 km/s/Mpc (si_value congelado 2.268545502662652e-18 s^-1)
a_P = c^2 / l_P
```

**Alegação:** este valor é internamente consistente com o restante do
núcleo Tamesis. "Internamente" porque isto é uma **adjudicação de mesa**
(auditoria numérica), não um teste experimental — o próprio módulo
registra em `reports/BOHR_LEVEL_GAP.md` que a fronteira experimental
observada está ~1,9 milhão de vezes abaixo de M_c (zero registros
observados perto/acima do limiar), e o próprio `STATUS.md` do módulo
admite: *"O valor não é uma constante medida nem uma derivação
concluída."* Nenhum dado de laboratório pode adjudicar M_c hoje; o que
PODE ser adjudicado é se o núcleo é coerente consigo mesmo.

Fatos motivadores (do levantamento de 2026-08-21, verificados por grep
nesta sessão antes desta nota — inventário exaustivo será tabulado em
`RESULTS_SUMMARY.md`):

1. O contrato usa o ramo `a0 = cH0`. O teste pré-registrado do próprio
   laboratório, `DISC-COSMOLOGY-MOND-SPARC-002`
   (`05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_A0_DERIVATION/`), confrontou os
   DOIS ramos de a0 existentes no núcleo contra dados reais SPARC e
   concluiu `H_A_SURVIVES_H_B_FALSIFIED`: o ramo sobrevivente é
   `a0 = cH0/2π` (Ponte Holográfica, ~1,08e-10 m/s²) e o ramo
   **falsificado** é exatamente `a0 = cH0` (~6,8e-10 m/s²,
   `a0_B_in_ci: false` em `analysis/result_primary.json`).
2. M_c aparece no núcleo em pelo menos 4 formulações/valores mutuamente
   distintos: 5,29e-16 kg (contrato v1.0), 2,2e-14 kg
   (Killer_Prediction / Universe_Equation / paper 08 e rascunho PRL),
   ~1e-14 kg (paper.html do 08, ordem de grandeza), 1,16e-16 kg
   (`01_Foundation/README.md:97`, `M_c ≈ M_P·Ω^-4`, Ω=117,038).
3. O expoente 1/8 é classificado no próprio contrato como
   `modelling_assumption` ("Root-eighth is a v1.0 hypothesis, not a
   derived theorem"), e
   `massa_critica/hipotese_colapso_quantico/calculo_mc.py` documenta que
   o expoente foi encontrado por VARREDURA de frações simples
   {1/2 … 3/4} contra uma janela-alvo 1e-17–1e-14 kg.

## O que esta frente NÃO é

- NÃO é um teste experimental de colapso quântico (não existe dado de
  laboratório na escala de M_c — `BOHR_LEVEL_GAP.md`).
- NÃO produz alegação de física nova nem inferência Tamesis além do
  número específico. Força máxima de veredito:
  **"consistente como formulado" / "inconsistente como formulado"**.
- NÃO altera nenhum arquivo do núcleo nem de governança.

## Constantes e proveniência (buscadas nesta sessão, NUNCA de memória)

Todas obtidas por fetch direto em 2026-08-21:

| Constante | Valor citado | Fonte (URL, acessada 2026-08-21) |
|---|---|---|
| G | "6.674 30(15) x 10⁻¹¹ m³ kg⁻¹ s⁻²" (CODATA 2022) | https://physics.nist.gov/cgi-bin/cuu/Value?bg |
| ħ | "1.054 571 817... x 10⁻³⁴ J s" (exato, CODATA 2022) | https://physics.nist.gov/cgi-bin/cuu/Value?hbar |
| c | "299 792 458 m s⁻¹" (exato) | https://physics.nist.gov/cgi-bin/cuu/Value?c |
| m_P (Planck) | "2.176 434(24) x 10⁻⁸ kg" (CODATA 2022) | https://physics.nist.gov/cgi-bin/cuu/Value?plkm |
| au | 149 597 870 700 m (exato, IAU 2012 Res. B2) | https://observatoiredeparis.psl.eu/the-new-definition-of-the-astronomical-unit.html (via busca; PDF oficial da IAU retornou 403 nesta sessão — reportado, não substituído) |
| pc | 648000/π au (exato, IAU 2015 Res. B2) | mesma busca (resultado citando IAU 2015 B2) |

Derivados exatos a partir das definições acima (calculados no script, não
digitados): `1 Mpc = (648000/π)·au·10⁶ m`; `l_P = sqrt(ħG/c³)`;
`m_P = sqrt(ħc/G)` (será comparado ao valor CODATA tabulado como checagem
de sanidade, tolerância relativa 2e-5, a incerteza relativa do próprio G);
`a_P = c²/l_P`. A aceleração de Planck não é uma constante CODATA
tabulada; usa-se exclusivamente a definição do próprio contrato
(`aP: c^2/l_P`), que coincide com `c/t_P`.

Valores INTERNOS do núcleo (não são referência externa; lidos dos
arquivos, com arquivo:linha registrado na tabela de inventário):
`H0 = 70 km/s/Mpc` e `si_value = 2.268545502662652e-18 s⁻¹` (contrato);
`Ω = 117.038` (`01_Foundation/README.md:17,46`); os quatro valores de
M_c listados acima.

## Plano de computação (fixado a priori, script determinístico, sem RNG)

Script único `analysis/compute_mc_consistency.py`, saída impressa salva
em `analysis/compute_mc_consistency.log` e resultados numéricos em
`analysis/results.json`. Nenhum ajuste, nenhuma iteração: uma execução,
números reportados como saírem.

1. **A1 — verificação aritmética do contrato.** Recomputar
   `M_c = m_P(a0/aP)^(1/8)` usando EXATAMENTE as constantes congeladas do
   próprio YAML (G=6.67430e-11, ħ=1.054571817e-34, c=299792458,
   H0_si=2.268545502662652e-18) e comparar com o valor congelado
   5.292674126388712e-16 kg. Também: reconverter H0=70 km/s/Mpc para SI
   com o Mpc IAU exato e comparar com o `si_value` congelado.
2. **A2 — os dois ramos de a0.** Recomputar M_c sob `a0=cH0` e
   `a0=cH0/2π` com H0=70; fator de deslocamento `(2π)^(1/8)` em valor
   pleno; M_c sob o ramo sobrevivente de SPARC-002.
3. **A3 — sensibilidade a H0.** M_c (ambos os ramos) para H0 ∈
   {67.4, 70, 73} km/s/Mpc; desvios percentuais.
4. **A4 — as outras derivações do núcleo.**
   a) `M_P·Ω^-4` com Ω=117,038 e M_P CODATA — reproduz 1,16e-16 kg?
   b) `(ħ²/(Gc))^(1/4)` (rascunho PRL `08_.../prl_submission.html:239` e
      `paper.html:410`) — análise dimensional explícita (a combinação tem
      dimensão de massa?) e valor numérico da expressão como escrita;
      reproduz a alegação "≈ 2,2×10⁻¹⁴ kg"?
   c) `(ħ·m_atom·c³/(4G))^(1/3)`
      (`03_Axiomatic_Closure/Universe_Equation/01_Mc_Derivation/index.html:255`)
      — análise dimensional; valor numérico com m_atom = 1 u (única
      leitura fisicamente óbvia, o arquivo não define m_atom); e o
      m_atom que SERIA necessário para reproduzir 2,2e-14 kg. Também
      checar a afirmação do mesmo arquivo de que 2,2e-14 kg ≈ "320
      million amu".
5. **A5 — matriz de razões.** Razões par-a-par (e ordens de grandeza)
   entre: valor congelado, valor no ramo sobrevivente, 2,2e-14, ~1e-14,
   1,16e-16.

## Critérios de decisão (fixados AGORA, antes de computar)

- **C1 (aritmética do contrato):** APROVADO se o recálculo A1 reproduzir
  o valor congelado com |Δ|/valor ≤ 1e-9 (tolerância de reprodução em
  dupla precisão; o próprio `mc_model.py` usa gate absoluto 1e-30 kg) E a
  reconversão de H0 bater com o `si_value` congelado com desvio relativo
  ≤ 1e-6. Caso contrário: erro aritmético interno.
- **C2 (coerência com o ramo a0 sobrevivente do próprio núcleo):**
  APROVADO somente se o ramo de a0 usado pelo contrato for o ramo que
  SPARC-002 (teste pré-registrado do próprio laboratório, dados reais)
  deixou sobreviver, OU se a diferença induzida em M_c pela troca de ramo
  for ≤ 1% (irrelevante numericamente). O ramo do contrato é `a0=cH0`
  (YAML linha 81); o veredito de SPARC-002 está em
  `analysis/result_primary.json` (`H_A_SURVIVES_H_B_FALSIFIED`, H_A =
  cH0/2π). REPROVADO caso contrário, com o fator de deslocamento
  quantificado.
- **C3 (coerência entre as formulações de M_c no núcleo):** as
  formulações são mutuamente CONSISTENTES se todos os pares de valores
  concordarem dentro de um fator 2 (tolerância generosa, já que os papers
  08 declaram estimativa de ordem de grandeza); INCONSISTENTES COMO
  FORMULADAS se qualquer par diferir por fator > 10 (uma ordem de
  grandeza). Entre fator 2 e 10: "tensão, não adjudicável" (reportada
  como tal).
- **C4 (aritmética das derivações alternativas):** cada fórmula
  alternativa é "aritmeticamente fiel" se reproduzir o valor que o
  próprio arquivo alega com desvio ≤ 5% (é o arredondamento típico de 2
  algarismos usado nos arquivos); "infiel" caso contrário. Fórmula
  dimensionalmente inconsistente (expoente de kg ≠ 1 na análise
  dimensional) é registrada como "dimensionalmente inconsistente"
  independentemente do número.
- **Veredito global:** "**consistente como formulado**" exige C1, C2 e
  C3 todos aprovados. Qualquer reprovação em C2 ou C3 ⇒ "**inconsistente
  como formulado**" (mesmo que C1 aprove — aritmética corretamente
  executada sobre um ramo internamente desautorizado continua sendo
  inconsistência interna do núcleo). C1 reprovado sozinho ⇒ "erro
  aritmético no contrato" (subcaso de inconsistente). C4 alimenta a
  tabela e o texto, não muda o veredito global sozinho.
- Se o veredito global for "consistente como formulado": recomputar por
  segunda rota independente (constantes CODATA em vez das congeladas;
  logaritmos em precisão estendida via `decimal`) e SINALIZAR no
  relatório que reprodução adversarial em nível de orquestrador é
  obrigatória antes de catalogar. Se "inconsistente": catalogar com o
  mesmo peso, sem promoção.

## Riscos de identificabilidade desta adjudicação (nomeados a priori)

1. **Isto não valida nem refuta M_c fisicamente.** Um núcleo
   internamente consistente ainda poderia estar errado; um inconsistente
   ainda poderia conter um valor correto por acidente. O veredito é
   somente sobre coerência interna.
2. **SPARC-002 é evidência sobre a0 em dinâmica galáctica**, e o uso de
   a0 em M_c é uma transferência de contexto feita pelo próprio núcleo.
   O critério C2 só cobra do núcleo a coerência com a SUA PRÓPRIA
   escolha sobrevivente — não afirma que a0 galáctico deva reger colapso
   quântico.
3. **A escolha do fator 2 / fator 10 em C3** é convenção declarada aqui,
   antes dos números; qualquer resultado na faixa intermediária será
   reportado como não adjudicável, não forçado.
4. **m_atom indefinido na fórmula do 01_Mc_Derivation** obriga uma
   escolha de leitura (1 u); ambas as direções (valor com 1 u; m_atom
   requerido para bater 2,2e-14) são reportadas para não depender da
   escolha.
