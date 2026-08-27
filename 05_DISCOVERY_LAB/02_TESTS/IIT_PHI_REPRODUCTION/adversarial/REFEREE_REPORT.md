# Relatório adversarial — reexecução independente (passo 7, `AGENTS.md`)

**Test ID:** `DISC-IIT-PHI-REPRO-001`
**Papel:** revisor adversarial, agente separado do que produziu
`RESULTS_PRIMARY.md` (`00_GOVERNANCE/AGENTS.md` §"Separação de papéis").
Instruído explicitamente a tentar refutar o achado, não confirmá-lo.
**Data:** 2026-08-27.
**Disciplina seguida:** todo código deste relatório foi escrito do zero a
partir de `PREREGISTRATION.md` — `analysis/reproduce_phi.py` (o script do
agente original) **não foi lido** antes de `referee_reproduce_phi.py` estar
completo e ter produzido resultado. A convenção de indexação LOLI/HOLI do
PyPhi foi verificada por derivação manual, não assumida da alegação do
pré-registro.
**Artefatos deste relatório:**
- `check_tpm_indexing.py` — verificação independente da TPM (tarefa 1).
- `referee_reproduce_phi.py` — reprodução independente completa (tarefa 3).
- `referee_phi_results_py311.json` — saída bruta, Python 3.11.15 (mesmo
  Python do resultado primário).
- `referee_phi_results_py312.json` — saída bruta, Python 3.12.3 (checagem
  cruzada de versão, tarefa 5).

---

## Veredito

```
VEREDITO ADVERSARIAL: SOUND WITH NAMED ISSUES
```

O critério de falsificação travado na Seção 5 do pré-registro **é
satisfeito de forma robusta e independentemente reproduzida**: Φ computado
por mim, do zero, em ambiente próprio (venv novo, `pip install pyphi`
independente), bate com o valor-alvo pré-registrado dentro da tolerância, e
a MIP encontrada é idêntica à reportada, em 8/8 reexecuções. **Não encontrei
nada que refute o resultado primário.** A alegação `CONFIRMED` de
`RESULTS_PRIMARY.md` para o critério travado (Seção 5 do pré-registro)
**se sustenta**.

No entanto, duas questões reais (não fatais, nenhuma delas toca o critério
travado) foram encontradas durante a tentativa de refutação e são
registradas abaixo como "named issues", por instrução explícita de não
suavizar achado real para evitar conflito. Por isso o veredito é
`SOUND WITH NAMED ISSUES`, não um `CONFIRMED` sem ressalvas.

---

## Tarefa 1 — Verificação independente da TPM (convenção LOLI vs. HOLI)

**Método:** sem ler o pré-registro além da especificação da rede, derivei
por mão própria (`check_tpm_indexing.py`) a TPM esperada de
`A=OR(B,C)`, `B=AND(A,C)`, `C=XOR(A,B)` sob as duas convenções possíveis de
indexação estado↔linha:

- **LOLI** ("low-order bits ↔ low-index nodes"): nó A = bit menos
  significativo do índice da linha.
- **HOLI** ("high-order bits ↔ low-index nodes"): nó A = bit mais
  significativo.

**Resultado:** a TPM dada no pré-registro bate **8/8 linhas** sob LOLI e
falha em **4/8 linhas** sob HOLI (linhas 1, 3, 4, 6 divergem sob HOLI). Isto
não é uma coincidência estatisticamente fraca — é uma discriminação limpa
entre as duas convenções, e a TPM dada só é consistente com a rede
booleana declarada sob LOLI.

**Confirmação de que LOLI é de fato a convenção real do PyPhi (não apenas
assumida):** meu script independente `referee_reproduce_phi.py` compara a
`Network` construída manualmente com `pyphi.examples.fig4()` (o exemplo
canônico empacotado pelo próprio PyPhi para esta mesma rede) e obtém
`bundled_fig4_tpm_matches: true`, `bundled_fig4_cm_matches: true` — os
atributos `.tpm`/`.cm` internos são idênticos elemento a elemento. Como
`pyphi.examples.fig4()` é código do próprio grupo autor do PyPhi
(implicitamente sob a convenção real do pacote), esta concordância
independe de qualquer alegação do pré-registro.

**Conclusão da tarefa 1:** a TPM/CM travada no pré-registro é uma
codificação correta da rede booleana declarada, sob a convenção de
indexação que o PyPhi de fato usa. Nenhum problema encontrado.

---

## Tarefa 2 — ImportError `collections.Iterable` e o patch de compatibilidade

**Reprodução do erro (ambiente novo, não o do agente original):**
`python3 -m venv venv_pyphi_referee && pip install pyphi` (fresh, sem
reaproveitar nenhum cache/ambiente do agente original) → `import pyphi`
falha exatamente como descrito:

```
ImportError: cannot import name 'Iterable' from 'collections'
  (.../pyphi/db.py:10, from collections import Iterable)
```

Confirmado **real**, não fabricado. Testado também em Python 3.12.3 (venv
separado) — mesma falha, mesmo traceback (`pyphi/db.py:10`). PyPI
(`pip index versions pyphi`) confirma `1.2.0` como única/última versão
disponível — não há Python ≤3.9 disponível neste ambiente para evitar o
problema por outra via (`python3.10`, `.11`, `.12`, `.13` apenas), o que
também bate com a alegação do resultado primário.

**Auditoria dos locais de uso (não confiando na descrição do resultado
primário — lendo o código-fonte do PyPhi diretamente):**

| Arquivo | Uso de `collections.Iterable`/`Mapping`/`Sequence` | Perto do cálculo de Φ? |
|---|---|---|
| `pyphi/db.py:77` | `isinstance(filtered_args, Iterable)` dentro de `generate_key()`, usado **apenas** se `CACHING_BACKEND == 'db'` (backend MongoDB) | **Não** — default é `CACHING_BACKEND='fs'` (confirmado no config snapshot); este código nem executa no caminho de cálculo padrão. Import é incondicional, mas o uso é inerte aqui. |
| `pyphi/models/cmp.py:100` | `numpy_aware_eq()`, helper de igualdade genérica entre phi-objetos | Tangencial — usado em comparações/ordenação (`__eq__`, `__lt__`), não na aritmética EMD em si. |
| `pyphi/registry.py:12` | `class Registry(collections.Mapping)` — classe-base de `MeasureRegistry` (guarda `measures['EMD']`) e `PartitionRegistry` (guarda `partition_types['BI']`) | **Estruturalmente no caminho** — é a classe que armazena/retorna a função de medida EMD e o tipo de partição BI efetivamente usados no cálculo. Porém `collections.Mapping` aqui só fornece métodos mixin (`get`, `keys`, `__contains__`, etc.) via ABC; a lógica de armazenamento (`self.store[name]`) já está implementada explicitamente na classe e não depende do mixin. |

**Achado adicional, além do que o resultado primário documenta (ver
"Issue 1" abaixo):** o grep por `collections\.` em todo o pacote mostra que
`collections.Sequence` (o mesmo tipo de alias descontinuado) também é usado
em `pyphi/models/subsystem.py:20` (`class CauseEffectStructure(cmp.Orderable,
collections.Sequence)` — a própria estrutura causa-efeito cujo cálculo de
distância EMD produz Φ), `pyphi/models/cuts.py:269` (`class
KPartition(collections.Sequence)` — o objeto de partição/corte, ou seja, a
própria MIP), `pyphi/models/actual_causation.py:219`, e
`pyphi/labels.py:25`. **Testei removendo `"Sequence"` do loop de patch**: o
`import pyphi` então falha em um ponto diferente,
`pyphi/models/actual_causation.py:219` (`class Account(cmp.Orderable,
collections.Sequence)`), confirmando que `Sequence` é **genuinamente
necessário** e que o problema de compatibilidade não está confinado aos 3
arquivos citados no §1.1 de `RESULTS_PRIMARY.md`.

**O patch em si é seguro (verificado, não apenas assumido):** os nomes
`collections.Iterable`/`Mapping`/`Sequence`/`Callable`/`MutableMapping`
eram, antes de removidos em Python 3.10, **aliases literais** (o mesmo
objeto de classe, não uma reimplementação) para
`collections.abc.Iterable`/etc. — documentado no próprio changelog do
CPython. Restaurar `collections.Iterable = collections.abc.Iterable` produz
o objeto idêntico que existia até Python 3.9, então `isinstance(x,
collections.Iterable)` se comporta de forma bit-idêntica antes e depois do
patch, **independente de qual classe o usa** (superficial como
`registry.py` ou central como `CauseEffectStructure`). Isto é corroborado
empiricamente: meu cálculo independente (ambiente, instalação e script
totalmente separados) produz `Φ = 1.916666` com `abs_diff =
9.999999999177334e-07` — **os mesmos 16 dígitos significativos** do
resultado primário arquivado em `phi_results.json`. Se o patch alterasse
qualquer comportamento numérico, essa coincidência bit-a-bit entre duas
execuções independentes seria virtualmente impossível.

**Conclusão da tarefa 2:** o ImportError é real, não fabricado; o patch
aplicado pelo agente original (que inclui `"Sequence"` no loop, verificado
em `RESULTS_PRIMARY.md` §1.1) é correto e comportamentalmente neutro. Mas
a **narrativa em prosa** de `RESULTS_PRIMARY.md` §1.1 subestima o alcance
do problema, nomeando apenas 3 arquivos e enquadrando-os de forma que
sugere "plumbing" periférico — quando na verdade `collections.Sequence`
(que o próprio patch já corrige, só não é discutido em prosa) é requerido
por `CauseEffectStructure` e `KPartition`, estruturas centrais do
pipeline de SIA. Ver "Issue 1" para severidade.

---

## Tarefa 3 — Reprodução independente do zero (`referee_reproduce_phi.py`)

Script próprio, construído apenas a partir da Seção 1 do pré-registro
(TPM/CM/estado/subsistema), **sem ler** `analysis/reproduce_phi.py`.

**Resultado (Python 3.11.15, ambiente `venv_pyphi_referee`,
`referee_phi_results_py311.json`):**

| Quantidade | Meu resultado independente | Alvo pré-registrado | Resultado primário arquivado |
|---|---|---|---|
| Φ computado | **`1.916666`** | `1.916665` | `1.916666` |
| `\|diferença\|` vs. alvo | `9.999999999177334e-07` | — | `9.999999999177334e-07` |
| Dentro da tolerância `1e-4`? | Sim | — | Sim |
| MIP/cut | `Cut [A, B] ━━/ /━━➤ [C]` | corte `{A,B}→{C}` (Mayner et al. 2018) | `Cut [A, B] ━━/ /━━➤ [C]` |
| `mip_matches_ab_to_c` | `true` | — | `true` |
| Conceitos na CES não-particionada | 6 | — | 6 |

**Meu Φ independente e o Φ do resultado primário coincidem em todos os
dígitos reportados (`1.916666`), e a diferença absoluta vs. o alvo
pré-registrado coincide até a 16ª casa decimal
(`9.999999999177334e-07`)** — esta não é apenas "dentro da tolerância", é
uma reprodução bit-idêntica entre duas instalações, dois scripts, e (no
mínimo) duas versões distintas de dependências transitivas (meu
`pip install pyphi` fresco trouxe `numpy==2.4.6`, `scipy==1.17.1`,
`pyemd==1.1.0` — não tenho garantia de que sejam as mesmas versões do
agente original, já que `RESULTS_PRIMARY.md` não fixa essas versões, apenas
lista as dependências sem pin). Isto é evidência forte de que o resultado
não é artefato de uma escolha de ambiente específica.

**Teste de estabilidade (não pedido explicitamente, mas necessário para a
tarefa 6 abaixo):** rodei o cálculo primário **8 vezes** em sequência,
ambiente limpo a cada vez (`rm -rf __pyphi_cache__`). Todas as 8 execuções
produziram `Φ=1.916666` e `Cut [A, B] ━━/ /━━➤ [C]`, sem nenhuma variação.
**O resultado primário é deterministicamente estável.**

**Checagem cruzada de versão do Python (Python 3.12.3,
`referee_phi_results_py312.json`):** `Φ=1.916666`,
`Cut [A, B] ━━/ /━━➤ [C]`, `mip_matches_ab_to_c: true` — idêntico ao
resultado em 3.11.15.

**Conclusão da tarefa 3:** reprodução independente bem-sucedida. Não
consegui refutar o resultado primário apesar de tentar ativamente (ambiente
novo, código novo, duas versões de Python, oito reexecuções).

---

## Tarefa 4 — Configuração do PyPhi em vigor

Meu `pyphi.config` (fresh install, sem `pyphi_config.yml`, sem variáveis
`PYPHI_*` no ambiente — `env_pyphi_vars: {}` confirmado programaticamente)
bate campo a campo com o `config_snapshot` de `phi_results.json` e com o
log (`pyphi.log`) do resultado primário:
`MEASURE=EMD`, `PARTITION_TYPE=BI`, `SYSTEM_CUTS=3.0_STYLE`,
`CUT_ONE_APPROXIMATION=False`, `PICK_SMALLEST_PURVIEW=False`,
`ASSUME_CUTS_CANNOT_CREATE_NEW_CONCEPTS=False`,
`USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE=False`,
`SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI=False`, `PRECISION=6`,
`VALIDATE_CONDITIONAL_INDEPENDENCE=True`, `VALIDATE_SUBSYSTEM_STATES=True`,
`CACHING_BACKEND=fs`, `CACHE_SIAS=False`, `WELCOME_OFF=False`. Nenhum
desvio de default de fábrica. **Conclusão: confirmado, sem ressalvas.**

---

## Tarefa 5 — Mudanças de default entre versões do PyPhi

`pip index versions pyphi` confirma `1.2.0` como única versão `LATEST`
disponível no PyPI (lista completa checada, de `0.1.3` a `1.2.0`) — bate
com a alegação do resultado primário de que não há versão mais nova.

Busquei o changelog do PyPhi (`CHANGELOG.md` no GitHub, `develop` branch) e
a página de releases do GitHub por fetch direto. Mudanças documentadas
relevantes ao tema "background condition"/poda de nó:

- **v0.4.0**: `compute.complexes` passou a podar subsistemas contendo nós
  sem entrada ou saída (Φ=0 necessariamente). **Não aplicável aqui** — a
  CM da rede ABC é totalmente conectada (todo nó tem entrada e saída) e,
  mais importante, o cálculo primário **não** passa por
  `compute.complexes`/busca de complexo — constrói o subsistema completo
  `{A,B,C}` diretamente e chama `sia()` nele.
- **v0.7.5**: introduziu validação de estado de subsistema
  (`VALIDATE_SUBSYSTEM_STATES`, hoje `True` por default) — lança
  `StateUnreachableError` para estados impossíveis, em vez de alterar
  silenciosamente o resultado. Como o cálculo primário completou sem erro,
  isto confirma (não contradiz) que o estado `(1,0,0)` é alcançável.
- Nenhuma mudança de default documentada entre `1.0.0`→`1.1.0`→`1.2.0` (as
  únicas versões instaláveis relevantes) afeta o **valor numérico** do
  cálculo de Φ para uma rede de 3 nós totalmente conectada analisada
  diretamente (sem busca de complexo) — as mudanças dessas versões, por
  fetch direto do GitHub, são renomeações de API (`big_mip`→`sia`,
  `Constellation`→`CauseEffectStructure`, `partition_registry`→
  `partition_types`, etc.), não mudanças de comportamento numérico.

**Conclusão da tarefa 5:** o enquadramento de `RESULTS_PRIMARY.md` de "não
há divergência para explicar" é honesto — não encontrei nenhum risco de
mudança de versão/default documentado que pudesse estar sendo mascarado
pela ausência de divergência.

---

## Tarefa 6 — Corroboração secundária FG (Figura 16) — escrutínio

**Proveniência do estado `(1,0,0,1,1,1,0)`:** busquei por fetch direto,
independentemente, a mesma URL citada
(`https://pyphi.readthedocs.io/en/latest/examples/2014paper.html`) e
confirmei que ela **de fato contém**, verbatim:
```
network = pyphi.examples.fig16_network()
state = (1, 0, 0, 1, 1, 1, 0)
```
e o resultado `(FG.subsystem.nodes, FG.phi) == ((F, G), 0.069445)`. **Não
é um valor inventado ou reconstruído para bater com o alvo** — está
genuinamente na fonte citada, confirmado por mim, não apenas pelo agente
original.

**Também verifiquei, por fetch direto e independente, os dois valores-alvo
numéricos centrais que ancoram todo o pré-registro** (não pedido
explicitamente pela tarefa 6, mas necessário para não aceitar a citação de
segunda mão):
- `pyphi.readthedocs.io/.../2014paper.html`: bloco de código mostra
  `>>> sia.phi` → `1.916665`, e a descrição do corte mínimo
  `"Cut [A,B] ━━/ /━━▶ [C]"` — confirmado presente, verbatim.
- Mayner et al. 2018 (PLOS Comput Biol, fetch direto do artigo publicado):
  confirmado o texto exato citado no pré-registro — "We can verify that
  the Φ value of the example system in [3] is 1.92 and the minimal
  partition is that which removes the causal connections from AB to C" —
  presente na subseção "Irreducible cause-effect structures (system-level
  integration)".

Ambas as citações-âncora do pré-registro são reais, não fabricadas.

**Achado adverso real na corroboração secundária (não fatal, não gating):**
ao rodar o subsistema FG repetidamente com entrada idêntica
(`pyphi.Subsystem(net16, state16, (5, 6))`, sem nenhuma aleatoriedade
declarada no código), o **valor de Φ é estável** (`0.069445` em toda
execução, incluindo minha própria — reprodução exata confirmada), mas a
**direção do corte MIP relatado não é determinística**:

```
5 execuções idênticas, mesmo ambiente, mesmo script:
  execução 1: Cut [F] ━━/ /━━➤ [G]
  execução 2: Cut [F] ━━/ /━━➤ [G]
  execução 3: Cut [F] ━━/ /━━➤ [G]
  execução 4: Cut [G] ━━/ /━━➤ [F]
  execução 5: Cut [G] ━━/ /━━➤ [F]
```

Isto é, as duas direções de corte produzem exatamente o mesmo Φ mínimo
(`0.069445`) — um empate genuíno — e qual delas é reportada depende da
ordem de conclusão dos workers sob `PARALLEL_CUT_EVALUATION=True` (default
de fábrica, não alterado por nenhum dos dois agentes), não de nenhuma
propriedade determinística da rede/estado. `referee_phi_results_py311.json`
capturou `Cut [G]→[F]` (por acaso, igual ao valor arquivado em
`phi_results.json` do resultado primário); `referee_phi_results_py312.json`
capturou `Cut [F]→[G]` (a direção oposta), na mesma sessão de investigação.
**Confirmei que o corte primário `{A,B}→{C}}` (rede ABC) NÃO sofre deste
problema** — 8/8 execuções produziram exatamente o mesmo corte, ou seja, a
MIP da rede primária é unicamente determinada (sem empate), o que blinda o
critério travado (Seção 5 do pré-registro) deste efeito. Ver "Issue 2"
abaixo.

**Conclusão da tarefa 6:** a corroboração secundária não é fabricada —
estado e valor-alvo genuinamente sourced. O valor de Φ reproduz
exatamente. Mas a direção de corte específica relatada em
`RESULTS_PRIMARY.md` §5 (`Cut [G]→[F]`) não é uma propriedade robusta e
reproduzível do cálculo — é um artefato de corrida entre workers paralelos
em um empate de partições, e isso não é mencionado no documento.

---

## Tarefa 7 — Integridade geral, provenance, consistência

- **Consistência `phi_results.json` ↔ `RESULTS_PRIMARY.md`:** conferido
  campo a campo (Φ, alvo, diferença absoluta, tolerância, `cut_repr`,
  `sia_time`, `small_phi_time_seconds`, `config_snapshot` completo, número
  de conceitos da CES). **Nenhuma inconsistência encontrada.**
- **Ordem trava-antes-de-rodar (item 4 do fluxo obrigatório,
  `AGENTS.md`):** `git log` mostra `PREREGISTRATION.md` commitado e
  travado no commit `ec42b65` em `2026-08-27 13:58:19 UTC`.
  `analysis/pyphi.log` mostra a primeira execução da análise às
  `2026-08-27 14:03:12 UTC` — **~5 minutos depois** do commit de trava, na
  ordem correta. `git diff HEAD -- PREREGISTRATION.md` retorna vazio — o
  arquivo travado **não foi alterado** desde o commit (sem adulteração
  pós-hoc do critério). `RESULTS_PRIMARY.md` e `analysis/` estão
  não-commitados (`git status` os lista como `??`), consistente com
  trabalho aguardando integração pela sessão orquestradora, não uma
  tentativa de esconder histórico.
- **Critério não reformulado pós-resultado:** a tolerância `1e-4` e o
  critério de corte `{A,B}→{C}` já estavam no texto travado do
  pré-registro antes da execução (confirmado pelo diff vazio acima); não
  há sinal de que o critério tenha sido ajustado depois de ver o número.
- **Nenhuma citação/URL inventada:** as duas citações numéricas centrais
  (readthedocs `1.916665`/corte `[A,B]→[C]`; Mayner et al. 2018 "1.92") e a
  citação do estado FG (`(1,0,0,1,1,1,0)`) foram todas verificadas por
  fetch direto nesta revisão adversarial, independentemente da alegação do
  pré-registro/resultado primário de já tê-las verificado.
- **Linguagem do veredito:** `RESULTS_PRIMARY.md` usa "CONFIRMED" apenas
  para o teste específico e não extrapola para "IIT está correta" ou
  alegações biológicas — consistente com as proibições de
  `00_GOVERNANCE/AGENTS.md`.

---

## Issues nomeados

### Issue 1 — Narrativa incompleta sobre o alcance do patch `collections.abc` (Severidade: LOW)

`RESULTS_PRIMARY.md` §1.1 nomeia apenas 3 arquivos
(`pyphi/db.py:10`, `pyphi/models/cmp.py:10`, `pyphi/registry.py:12`) como
usuários de `collections.Iterable`/`Mapping`, e enquadra o problema como
essencialmente sobre plumbing de cache/registro. Na prática, o mesmo tipo
de import descontinuado (`collections.Sequence`) é usado por
`pyphi/models/subsystem.py` (`CauseEffectStructure`, a estrutura
causa-efeito central ao cálculo de Φ) e `pyphi/models/cuts.py`
(`KPartition`, o objeto de partição/corte) — verificado nesta revisão
removendo `"Sequence"` do loop de patch e confirmando que `import pyphi`
falha em `models/actual_causation.py:219` como consequência.

**Por que é LOW e não invalida nada:** o código de patch efetivamente
aplicado (mostrado em `RESULTS_PRIMARY.md` §1.1) **já inclui** `"Sequence"`
no loop — a lacuna é apenas na explicação em prosa, não no código
executado. E como os nomes restaurados eram aliases literais (mesmo objeto
de classe) para as versões `collections.abc.*` antes de Python 3.10, o
alcance mais amplo do patch não implica nenhum risco adicional de alteração
de comportamento — confirmado empiricamente pela reprodução bit-idêntica
obtida nesta revisão. **Recomendação:** atualizar §1.1 de
`RESULTS_PRIMARY.md` para nomear também `models/subsystem.py` e
`models/cuts.py`, e para não descrever o problema como confinado a
"cache/registro" — ele toca estruturas centrais do pipeline de SIA, embora
de forma comportamentalmente neutra.

### Issue 2 — Direção do corte MIP na corroboração secundária FG não é determinística (Severidade: LOW)

A direção do corte reportada para o subsistema FG (`Cut [G]→[F]` em
`RESULTS_PRIMARY.md` §5 / `phi_results.json`) é uma de duas direções
empatadas em Φ (`0.069445` para ambas), e qual delas aparece depende da
ordem de conclusão de workers sob `PARALLEL_CUT_EVALUATION=True` (default
de fábrica) — confirmado nesta revisão por 5 reexecuções idênticas que
produziram 3× uma direção e 2× a outra. O valor de Φ em si permanece
perfeitamente estável e reproduzido exatamente.

**Por que é LOW e não invalida o veredito:** (a) a Seção 6 do pré-registro
já declara este teste como corroboração opcional, **não parte do critério
de falsificação travado**; (b) a fonte citada
(readthedocs 2014paper.html) não documenta uma direção de corte específica
para o subsistema FG contra a qual comparar — `RESULTS_PRIMARY.md` não
alega "bate com a direção publicada", apenas reporta o Φ e o corte
observado; (c) **o corte primário da rede ABC (o que de fato importa para
o critério travado) foi verificado nesta revisão como unicamente
determinado, sem empate — 8/8 reexecuções idênticas**, então este efeito
não contamina o resultado que gate o veredito. **Recomendação:** se
`RESULTS_PRIMARY.md` §5 for citado no futuro, qualificar explicitamente que
apenas o valor de Φ da corroboração FG é uma propriedade reproduzível — a
direção do corte relatada não é, e não deveria ser tratada como um "match"
com nada. A afirmação de determinismo total ("nenhuma aleatoriedade em
nenhuma etapa", `RESULTS_PRIMARY.md` cabeçalho/§7) deveria ser qualificada
como válida para o Φ mas não para a direção de corte reportada em casos de
empate como este.

---

## Resumo para `TEST_QUEUE.yaml` / `CLAIM_LEDGER.yaml`

- **Critério travado (Seção 5 do pré-registro): CONFIRMED**, reproduzido
  independentemente do zero, com Φ bit-idêntico ao resultado primário e MIP
  idêntica, estável em 8/8 reexecuções e em 2 versões de Python (3.11,
  3.12).
- **Veredito geral da revisão adversarial: `SOUND WITH NAMED ISSUES`** —
  2 issues LOW registrados acima (narrativa do patch incompleta; corte MIP
  da corroboração secundária opcional não-determinístico), nenhum dos dois
  tocando o critério travado ou o valor de Φ primário.
- Nenhum indício de dado fabricado, citação inventada, critério
  reformulado pós-hoc, ou violação de proveniência foi encontrado.
