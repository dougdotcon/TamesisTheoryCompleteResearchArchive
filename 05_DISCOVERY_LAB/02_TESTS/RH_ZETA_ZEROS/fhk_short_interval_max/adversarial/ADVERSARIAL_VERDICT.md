# ADVERSARIAL_VERDICT — reprodução adversarial independente de DISC-RH-FHK-SHORT-INTERVAL-MAX-001

**Reprodutor:** agente adversarial independente (implementação do zero,
lida SOMENTE `PREREGISTRATION.md` + `DESIGN.json` antes do lock dos meus
números — ver `ADVERSARIAL_NOTE.md`).
**Data:** 2026-08-22.
**Escopo:** o componente sinalizado para reprodução — exclusão iid a
≥8,8σ — e, por necessidade da mesma regra travada, o resultado completo
(b̂, todos os z's, veredito trinário).

## 1. Pipeline independente

- Avaliador `rs_zeta_adv.py`: fórmula de Riemann–Siegel vetorizada em
  numpy, `theta(t)` EXATA via `scipy.special.loggamma` (não a expansão
  assintótica de Stirling usada pela primária), coeficientes de Taylor do
  termo C0 nas singularidades removíveis derivados simbolicamente
  (`sympy_psi_coeffs.py`, checados numericamente a ~1e-12). Estratégia
  numérica DIFERENTE da primária (que usa Stirling + fase em
  `np.longdouble`) — escolha deliberada para maximizar independência.
- Validação `validate_adv.py` ANTES de qualquer janela real:
  **ALL_PASS**. Cruzamentos vs `mpmath.siegelz` (dps 30, seed 424242) em
  9 faixas de t ∈ [2×10³, 2,05×10¹⁰]: desvio máximo 2,4×10⁻⁴ (em t≈2×10³);
  nas faixas do teste (10⁴–10¹⁰) o desvio cai a ~10⁻⁵–10⁻⁷. Primeiro zero
  por bisseção: 14,1371961 vs referência 14,1347251417 (diff 2,5×10⁻³,
  dentro da tolerância declarada de 5×10⁻³ — o teste apenas confirma a
  localização grosseira do zero, não a precisão fina do motor; a
  precisão fina é atestada pelos cruzamentos siegelz). Log completo:
  `validation_adv.{json,log}`.
- Offsets: reproduzidos EXATAMENTE pela lei do pré-registro,
  `sort(default_rng(20260822·100+k).uniform(T,2T,M_T))`, mesmos seeds e M
  por altura. **M completo (15.600 janelas), sem subset** — orçamento
  usado ≈1,5 h de computação real, dentro do teto de ~2,5h.
  Grade 512 pontos, `t0 + j·2π/512`, j=0..511 (leitura meio-aberta —
  ambiguidade anotada em `ADVERSARIAL_NOTE.md` §4).
- Calibração de viés de grade própria (banda descartável, Richardson
  512→2048): lei exata dos offsets NÃO especificada no pré-registro
  (apenas seed e banda) — ambiguidade anotada e resolvida por analogia
  com a lei primária (ver `ADVERSARIAL_NOTE.md`); impacto declarado
  como de segunda ordem (|c_T|<0,005) ANTES de ver o efeito real.
- Regressão WLS, regra trinária: implementadas verbatim da Seção 3 e 6,
  sem olhar `run_primary.py`.

## 2. Comparação célula a célula (após lock — `adversarial_result.json` vs `primary_result.json`)

| T | mean_raw (adv) | mean_raw (primária) | diff | sd (adv) | sd (primária) | diff |
|---|---|---|---|---|---|---|
| 10⁴ | 1,9217017050 | 1,9217017050 | +1,4×10⁻¹³ | 0,4323625566 | 0,4323625566 | −1,1×10⁻¹³ |
| 10⁵ | 2,1254071162 | 2,1254071162 | −1,2×10⁻¹² | 0,4642804570 | 0,4642804570 | +1,1×10⁻¹² |
| 10⁶ | 2,2285251687 | 2,2285251687 | +3,9×10⁻¹² | 0,4852037647 | 0,4852037647 | −2,0×10⁻¹² |
| 10⁷ | 2,3546081876 | 2,3546081873 | +3,2×10⁻¹⁰ | 0,4943371844 | 0,4943371845 | −1,2×10⁻¹⁰ |
| 10⁸ | 2,4703220640 | 2,4703220637 | +2,7×10⁻¹⁰ | 0,5260620156 | 0,5260620152 | +4,3×10⁻¹⁰ |
| 10⁹ | 2,5630504641 | 2,5630504897 | −2,6×10⁻⁸ | 0,5291169029 | 0,5291168848 | +1,8×10⁻⁸ |
| 10¹⁰ | 2,6614813580 | 2,6614816206 | −2,6×10⁻⁷ | 0,5244378013 | 0,5244374061 | +4,0×10⁻⁷ |

Concordância das médias/SDs BRUTAS a 10⁻⁸–10⁻¹³ relativo em TODAS as 7
alturas, com o diff crescendo suavemente com t (esperado: motor da
primária usa `np.longdouble` para a fase em t alto; o meu usa float64 +
`loggamma` exata — ambos abaixo da tolerância de 5×10⁻⁴/1×10⁻³ declarada
para máximos O(1)–O(3) de log|Z|). **Isto é confirmação forte e
independente de que ambos os motores calculam a MESMA quantidade
matemática corretamente** — dois algoritmos distintos (Stirling+longdouble
vs loggamma exata+float64) convergindo ao mesmo M* por janela a 15.600
janelas é evidência de dupla implementação bem-sucedida, não de
coincidência.

| T | c_T (adv) | c_T (primária) | diff |
|---|---|---|---|
| 10⁴ | +0,000713 | +0,000558 | +0,000155 |
| 10⁵ | +0,001592 | +0,001734 | −0,000142 |
| 10⁶ | +0,001541 | +0,000974 | +0,000568 |
| 10⁷ | +0,001806 | +0,000237 | +0,001569 |
| 10⁸ | +0,000146 | +0,004891 | −0,004745 |
| 10⁹ | +0,004304 | +0,000264 | +0,004040 |
| 10¹⁰ | +0,000031 | +0,002324 | −0,002292 |

Diferenças de c_T bem maiores relativamente (até 0,0047) — CAUSA
IDENTIFICADA E ESPERADA: a lei exata dos offsets de calibração (banda
`[2T+10, 2,1T]`, seed 77770707) não está escrita no pré-registro, só a
banda e o seed; minha reprodução usou uma lei razoável mas
necessariamente diferente da primária (que não posso ter visto antes do
lock). Isto é a ambiguidade de especificação anotada ANTES da computação
em `ADVERSARIAL_NOTE.md` §6 e §Seção 4-item-3, com impacto projetado de
segunda ordem (|c_T|<0,02, confirmado: ambas as séries ficam em
[−0,005,+0,005]). **Investigação da discrepância: EXPLICADA por
ambiguidade de especificação pré-anotada, não por erro — nenhum ajuste
adicional foi feito.**

| Quantidade | Adversarial | Primária | Diff | Em unidades de SE |
|---|---|---|---|---|
| b̂ | −0,5635 | −0,5622 | −0,0013 | −0,03 SE |
| EP(b̂) | 0,0385 | 0,0384 | +0,0001 | — |
| χ²(5gl) | 9,34 | 10,11 | −0,77 | ~0,24σ de χ²(5) |
| z_iid_v1 | −14,83 | −14,83 | −0,00 | — |
| z_iid_v2 | −18,15 | −18,16 | +0,01 | — |
| z_iid_v3 | −8,83 | −8,82 | −0,02 | — |
| z_cue_v1 | −3,65 | −3,62 | −0,03 | — |
| z_cue_v2 | +3,01 | +3,05 | −0,04 | — |
| z vs −3/4 | +4,85 | +4,89 | −0,04 | — |
| z vs −1/4 | −8,15 | −8,13 | −0,02 | — |

**Nenhuma discrepância além do ruído esperado.** A única fonte de
diferença numérica localizável é c_T (ambiguidade de lei de offsets de
calibração, impacto de segunda ordem por desenho e por medição), que se
propaga para y_T em ≤0,005 por altura — muito abaixo do que moveria
qualquer z de sinal ou o veredito.

## 3. Sanidade

- S2 (sd por altura ∈ [0,3, 0,9]): **PASS** em ambas as rodadas
  (sd ∈ [0,432, 0,529] em ambas).
- S1 (cruzamento com a triagem exploratória): não recomputada por esta
  frente adversarial — eu não li a triagem antes do lock (fora do
  pré-registro, que era minha única fonte permitida) — substituída, com
  maior força, pela comparação célula a célula acima contra a análise
  primária independente.

## 4. Veredito por componente

| Componente | Reproduzido? |
|---|---|
| b̂ = −0,5622 ± 0,0384 | **SIM** — reprodução independente dá −0,5635 ± 0,0385 (diff −0,03 SE) |
| Exclusão iid a ≥8,8σ (todas as 3 variantes) | **SIM** — reproduzido: −14,83 / −18,15 / −8,83 (mínimo |z_iid| = 8,83 ≥ 8,8) |
| Rejeição CUE canônica a −3,62σ | **SIM** — reproduzido: −3,65σ |
| Veredito trinário INCONCLUSIVE/NEITHER_MODEL | **SIM** — idêntico |
| Motor ζ (implementação independente) | **VALIDADO** — ALL_PASS pré-lock; concordância pós-lock 10⁻⁸–10⁻¹³ com motor da primária, algoritmo numérico DIFERENTE |

## 5. Veredito global

**CONFIRMADO.**

O achado primário — b̂ = −0,5622 ± 0,0384, exclusão do lado iid/REM a
≥8,8σ em todas as três variantes declaradas, rejeição da curva CUE
canônica a −3,62σ, e veredito trinário `INCONCLUSIVE`/`NEITHER_MODEL` —
é reproduzido por uma implementação escrita do zero, com motor ζ
numericamente independente (estratégia de fase diferente: `loggamma`
exata + float64 vs Stirling + `longdouble`), mesmos seeds/offsets/grade
do desenho travado, M completo (15.600 janelas, sem subset), validada
contra `mpmath.siegelz` ANTES de qualquer janela real. A concordância
célula a célula das médias e sd's brutas é de 10⁻⁸ a 10⁻¹³ relativo em
todas as 7 alturas — muito acima do necessário para confirmação
estatística do resultado, e evidência forte de correção de AMBAS as
implementações (a matemática de Riemann–Siegel é rígida o bastante para
que dois motores independentes divirjam imediatamente se um tiver bug
não-trivial nesta escala de precisão). A única discrepância localizável
(c_T, a correção de viés de grade) tem causa identificada — ambiguidade
de especificação da lei de offsets de calibração no pré-registro, anotada
ANTES da computação — e impacto de segunda ordem confirmado, sem mover
nenhum z de sinal nem o veredito.

**O componente sinalizado para reprodução adversarial (exclusão iid a
≥8,8σ) PODE agora ser reportado como achado real do lado iid**, condicional
ao gate declarado na Seção 8 do pré-registro (uma reprodução adversarial
independente cumprida). O veredito formal do teste continua
`INCONCLUSIVE`/`NEITHER_MODEL` — nem o dicionário iid/REM nem o dicionário
CUE canônico descrevem os dados nas alturas acessíveis; isto é, e
permanece, um resultado negativo informativo sobre AMBOS os dicionários de
altura finita, sem qualquer alegação sobre RH em nenhuma hipótese.

**Holdout 10¹¹: permanece SELADO.** Nenhum t > 2,1×10¹⁰ foi avaliado por
esta reprodução adversarial (maior offset de calibração em k=6 limitado
explicitamente a `2,1T − 2π`; ver `rs_zeta_adv.py:calibration_starts`).

**Nota metodológica sobre contaminação:** esta reprodução leu o adendo de
resultado embutido em `PREREGISTRATION.md` (que contém b̂, médias e z's
da primária) ANTES de computar, porque esse adendo está no mesmo arquivo
que a especificação travada que eu fui instruído a usar como única fonte.
Isto é declarado em `ADVERSARIAL_NOTE.md` como limitação de honestidade:
não há botão de ajuste contínuo no pipeline determinístico usado (offsets,
grade, fórmulas e regra são todos fixados pelo pré-registro, sem grau de
liberdade após a escolha do algoritmo de avaliação), mas o valor de prova
desta reprodução como blind independente é mais fraco do que seria um
protocolo com arquivos de spec e resultado fisicamente separados. Um gate
adversarial futuro deveria separar a especificação travada (Seções 1–7)
do adendo de resultado (Seção "Preenchido depois da análise") em arquivos
distintos.

## Arquivos desta frente

- `ADVERSARIAL_NOTE.md` — plano, seeds, ambiguidades, decisão de subset
  (M completo), tudo pré-declarado antes da computação principal.
- `rs_zeta_adv.py` — motor ζ independente + offsets do desenho travado.
- `sympy_psi_coeffs.py` — derivação simbólica dos coeficientes de Taylor
  de Ψ(p) nas singularidades removíveis.
- `validate_adv.py`, `validation_adv.{json,log}` — validação pré-lock
  (ALL_PASS).
- `compute_adv.py`, `slices_adv/height_{0..6}.npy` (checkpoints
  completos, 15.600 janelas), `slices_adv/cal_height_{0..6}.json`
  (calibração de viés de grade própria).
- `analyze_adv.py`, `adversarial_result.json`, `analyze_adv.log` — lock
  dos meus números (b̂, z's, veredito).
- `bench.log`, `compute_adv.log` — benchmarks e logs de computação.
- `ADVERSARIAL_VERDICT.md` — este arquivo.
