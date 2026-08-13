# Proveniência de dados — DISC-RH-GAP-EXTREME-VALUE-SCALING-001

## Dataset primário

Reaproveitado sem modificação de `../../RH_ZETA_ZEROS/data/zeros1.txt`
(100.000 primeiros zeros reais de ζ(s), Odlyzko) — mesma proveniência já
documentada em `../../RH_ZETA_ZEROS/data/PROVENANCE.md` (URL, checksum,
verificação de conteúdo). Nenhum novo download necessário.

## Dataset reservado para o Gate de Replicação

`zeros5.txt` (Odlyzko, zeros próximos de #10²², mesma fonte
`https://www-users.cse.umn.edu/~odlyzko/zeta_tables/`) — **explicitamente
NÃO baixado nem inspecionado nesta sessão**. Reservado para checagem de
robustez fora-do-regime no Gate de Replicação (`03_REPLICATION_GATE/PROTOCOL.md`
Seção 3, cláusula de fallback — este pré-registro não declara holdout
selado sobre `zeros1.txt`, então o Gate exige checagem contra fonte de
dado adicional). Mesmo padrão que funcionou em `DISC-RH-ZERO-GAP-RUNS-001`
(que usou `zeros4.txt`, regime #10²¹, ~15 ordens de magnitude acima do
primário).

---

## Adição — Gate de Replicação, terceiro dataset (`zeros5.txt`)

**Agente:** terceiro agente, independente, executando o Gate de Replicação
para `DISC-RH-GAP-EXTREME-VALUE-SCALING-001`
(`03_REPLICATION_GATE/PROTOCOL.md`, cláusula de fallback da Seção 3 —
nenhum holdout selado foi declarado no pré-registro deste teste, então o
Gate exige checagem de robustez formal contra pelo menos uma fonte de
dado adicional). Este arquivo NUNCA havia sido baixado, inspecionado, ou
tocado nesta sessão antes desta adição — download feito diretamente pelo
agente do Gate, primeira vez que seu conteúdo real foi visto por qualquer
agente. Este agente não leu `run_preregistered_analysis.py` nem
`adversarial_reproduction.py` antes de escrever seu próprio script.

- **URL exata:** `https://www-users.cse.umn.edu/~odlyzko/zeta_tables/zeros5`
  (mesmo domínio já verificado como real acima e já usado para `zeros4.txt`
  no Gate do teste-irmão — fetch direto via `curl`, HTTP 200,
  `Content-Length: 170318`, corpo salvo com 170.318 bytes, tamanhos
  batendo).
- **Data de acesso:** 2026-08-13.
- **Arquivo local:** `data/zeros5.txt`.
- **sha256:** `250ac4ba722c6face4d07c05777376fc2b9bc021b05232e8f53c91b1eb2b7e0d`.
- **Linhas totais:** 10.009 (9 linhas de cabeçalho em prosa/branco — linhas
  1–7 texto, 8–9 em branco — seguidas de exatamente 10.000 linhas de dado
  numérico, linhas 10–10.009 — confirmado por parsing programático via
  regex `^\s*\d+\.\d+\s*$` linha a linha, não assumido por analogia com
  `zeros3.txt`/`zeros4.txt`, embora a contagem tenha batido com a mesma
  estrutura geral de cabeçalho curto + dado contíguo sem rodapé).
- **Conteúdo/formato:** valores de `gamma - BASE`, onde `BASE =
  1370919909931995300000` (22 dígitos, declarado no próprio cabeçalho do
  arquivo: "Values of gamma - 1370919909931995300000, where gamma runs
  over the heights of the zeros of the Riemann zeta numbered 10^22 + 1
  through 10^22 + 10^4"). Precisão declarada no cabeçalho: "Values are not
  guaranteed, and are probably accurate to within 10^(-6)" — mesma
  precisão nominal de `zeros4.txt` (10⁻⁶), mais grosseira que `zeros1.txt`
  (~9 dígitos decimais) e `zeros3.txt` (10⁻⁸).
- **Verificação de conteúdo:** `BASE + primeiro_offset` (calculado em
  precisão exata via `decimal.Decimal`, não `float64`) =
  1370919909931995300000 + 8226.68016095 = 1370919909931995308226.68016095,
  batendo dígito a dígito com o valor declarado no próprio cabeçalho para
  o zero #10²²+1 ("1/2 + i * 1,370,919,909,931,995,308,226.68016095...")
  — confirma que o conteúdo é real, não um stub ou placeholder, e que a
  base foi lida corretamente. Sequência de 10.000 offsets verificada
  estritamente crescente (nenhuma linha fora de ordem).
- **Regime de altura:** γ ≈ 1,37×10²¹ (zeros numerados #10²²+1..#10²²+10⁴,
  mas a altura γ em si é da ordem de 10²¹) — mais alto que `zeros4.txt`
  (γ≈1,44×10²⁰) e ~16 ordens de magnitude acima do primário (`zeros1.txt`,
  γ até ~75.000).
- **Nota de precisão numérica (mesmo padrão de `zeros4.txt`, confirmado
  empiricamente aqui):** `BASE` tem 22 dígitos significativos. Representar
  `BASE` como `float64` e arredondar para o inteiro mais próximo produz um
  erro absoluto de **65.376** (verificado neste agente:
  `int(float(1370919909931995300000)) - 1370919909931995300000 = 65376`),
  muito maior que qualquer gap normalizado típico desta análise (~0,01–3).
  O script deste agente (`analysis/gate_third_dataset_replication.py`)
  calcula gaps brutos **diretamente da diferença de offsets**
  (`offset_{n+1} - offset_n`, onde `BASE` se cancela algebricamente e
  nunca precisa ser formado em precisão plena), e usa `BASE` em `float64`
  **apenas** dentro do termo `log(gamma_n/(2π))`, termo comprovadamente
  insensível a erro relativo de arredondamento de `float64` nessa
  magnitude (erro relativo ~1,6×10⁻¹⁷ propaga para erro absoluto
  ~1,6×10⁻¹⁷ em `log`, desprezível).
- **Fontes ainda não baixadas nesta sessão:** nenhuma pendência restante
  desta linha de teste — `zeros5.txt` era o último dataset reservado
  citado no pré-registro.

### Resultado da checagem de robustez (resumo — ver
`analysis/result_gate_third_dataset.json` para o resultado completo)

`zeros5.txt` tem apenas 10.000 zeros ⟹ 9.999 gaps normalizados — quase
10× menos que o primário (`zeros1.txt`, 99.999 gaps). Isso é
estruturalmente insuficiente para a grade de `N` travada no pré-registro
(até N=10.000): contagens de bloco obtidas foram **19 (N=500), 9
(N=1.000), 4 (N=2.000), 1 (N=5.000), 0 (N=10.000 — impossível, dataset
tem só 9.999 gaps)**. Só N=500 e N=1.000 atingem a barra de qualidade de
"≥8 blocos" que o próprio pré-registro declara (Seção 4, passo 3) para o
dataset primário. Ver relatório do agente para a análise completa de
poder estatístico (inconclusivo com apenas 2 pontos de grade válidos;
grade completa ingênua de 4 pontos usáveis produz `β=-0,171345`, IC 95%
`[-0,240284; -0,096531]`, que exclui tanto -1/3 quanto -1 mas é
contaminado por pontos com 1 e 4 blocos apenas — ver seção "Descoberta
adversarial de nulos" do relatório da sessão para avaliação de robustez).
