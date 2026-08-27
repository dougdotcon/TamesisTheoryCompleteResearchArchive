# Resultado primário — Reprodução via PyPhi do Φ publicado para a rede ABC (Oizumi, Albantakis & Tononi 2014)

**Test ID:** `DISC-IIT-PHI-REPRO-001`
**Pré-registro (LOCKED):** `PREREGISTRATION.md` (`DISC-DEC-102`, travado
2026-08-27). Este documento reporta o resultado exatamente como saiu da
execução da análise pré-registrada — nenhuma reformulação de hipótese,
rede, estado, estatística de teste, ou critério de falsificação foi feita
depois de ver o resultado.
**Data de execução:** 2026-08-27.
**Código:** `analysis/reproduce_phi.py` (reexecutável, determinístico —
nenhuma aleatoriedade em nenhuma etapa; a única entrada externa é a
instalação do pacote `PyPhi` via `pip install pyphi`).
**Resultado numérico bruto completo:** `analysis/phi_results.json`.

> **Este é o resultado da análise primária (não-adversarial), executado por
> um único agente.** Por `00_GOVERNANCE/AGENTS.md` passo 7, ele **não pode**
> ser catalogado como fechado (`01_PORTFOLIO/TEST_QUEUE.yaml`,
> `00_GOVERNANCE/CLAIM_LEDGER.yaml`) até que um segundo agente, instruído a
> tentar refutá-lo, reexecute a análise de forma independente — essa
> reexecução **não** foi feita por este agente/sessão (deliberadamente, por
> instrução explícita da tarefa).

---

## Veredito

```
VEREDITO: CONFIRMED (reprodução bem-sucedida, dentro da tolerância travada)
```

`Φ` computado = **`1.916666`**, alvo pré-registrado = `1.916665`,
`|diferença| = 0.000001`, dentro da tolerância travada `1e-4` (e arredonda
para `1.92`, idêntico ao valor citado em prosa por Mayner et al. 2018). A
MIP (partição de informação mínima) encontrada corta exatamente as conexões
causais de `{A,B}` para `{C}` — `Cut [A, B] ━━/ /━━➤ [C]` — idêntica à
reportada ("the minimal partition is that which removes the causal
connections from AB to C"). **Ambas as condições da Seção 5 do
pré-registro são satisfeitas: reprodução CONFIRMADA.**

---

## 1. Ambiente e versão do pacote (Seção 4 do pré-registro)

```
$ pip install pyphi
Successfully installed ... pyphi-1.2.0 ...

$ pip show pyphi
Name: pyphi
Version: 1.2.0
Summary: Python library for computing integrated information.
Home-page: http://github.com/wmayner/pyphi
Author: William GP Mayner
License: GNU General Public License v3.0
Requires: decorator, joblib, numpy, psutil, pyemd, pymongo, pyyaml, redis,
          scipy, tblib, tqdm
```

`pyphi.__version__ == "1.2.0"` — a versão mais recente disponível no PyPI
neste momento (`pip index versions pyphi` lista `1.2.0` como `LATEST`,
lançada em 2020; não há versão mais nova). Python usado: `3.11.15 (main,
GCC 13.3.0)`.

### 1.1 Incompatibilidade de ambiente encontrada e corrigida (documentada, não é mudança de default de IIT/PyPhi)

`import pyphi` falha nesta versão instalada, neste Python, com:

```
ImportError: cannot import name 'Iterable' from 'collections'
```

**Causa:** `PyPhi` 1.2.0 foi escrito para Python ≤3.9 e importa
`collections.Iterable`/`collections.Mapping` diretamente do módulo
`collections` de nível superior (`pyphi/db.py:10`,
`pyphi/models/cmp.py:10`, `pyphi/registry.py:12`). Esses aliases foram
movidos para `collections.abc` desde Python 3.3 (descontinuados desde
então) e **removidos** de `collections` no Python 3.10. Este ambiente roda
Python 3.11, então o import falha sem correção — testado também que a
mesma falha ocorre em Python 3.10, 3.12 e 3.13 (todos disponíveis nesta
imagem); não há Python ≤3.9 disponível para evitar o problema por outra
via.

**Correção aplicada, no início do próprio script (`reproduce_phi.py`,
antes de `import pyphi`):**

```python
import collections, collections.abc
for _name in ("Iterable", "Mapping", "Callable", "Sequence", "MutableMapping"):
    if not hasattr(collections, _name) and hasattr(collections.abc, _name):
        setattr(collections, _name, getattr(collections.abc, _name))
```

Isto **não** altera nenhum default de configuração do PyPhi, nenhum
parâmetro do cálculo de IIT, nenhuma lógica numérica — apenas restaura, no
módulo padrão `collections`, um nome que o próprio código-fonte do PyPhi
espera encontrar lá (e que existia lá até Python 3.9). O patch é aplicado
de forma idêntica independente da rede/estado analisados, então não pode
introduzir viés no resultado. Isto é exatamente o tipo de risco que a
Seção 3 do pré-registro antecipava ("mudança de comportamento padrão entre
versões... a documentação oficial nota mudanças de convenção") — mas
**não é esse tipo de risco**: é uma incompatibilidade Python-vs-stdlib,
não uma mudança de convenção de "background condition" ou poda de nó do
PyPhi. Nenhum parâmetro de `pyphi.config` foi alterado do default (ver
§2 abaixo — todos os defaults de fábrica do PyPhi 1.2.0 foram usados).

> **[Correção datada, 2026-08-27 — revisão adversarial, `DISC-DEC-103`,
> Issue 1, severidade BAIXA.]** O parágrafo acima nomeia apenas 3 arquivos
> (`db.py`, `models/cmp.py`, `registry.py`) e enquadra o problema como
> essencialmente sobre plumbing de cache/registro — isto subestima o
> alcance real. O mesmo tipo de alias descontinuado
> (`collections.Sequence`) também é requerido por `pyphi/models/
> subsystem.py` (`CauseEffectStructure`, a estrutura causa-efeito central
> ao cálculo de Φ) e `pyphi/models/cuts.py` (`KPartition`, o próprio
> objeto de partição/MIP) — confirmado pelo referee removendo `"Sequence"`
> do loop de patch e observando `import pyphi` falhar em
> `models/actual_causation.py:219` como consequência. O código de patch
> efetivamente executado (mostrado acima) **já incluía** `"Sequence"` —
> a lacuna era apenas na descrição em prosa de onde ele se aplica, não no
> comportamento real. Isto não altera nenhuma conclusão: os nomes
> restaurados eram aliases literais (mesmo objeto de classe) para
> `collections.abc.*` antes de Python 3.10, então o alcance mais amplo do
> patch não introduz nenhum risco adicional de alteração de comportamento
> — confirmado empiricamente pela reprodução bit-idêntica do referee
> (mesmos 16 dígitos significativos, ambiente e instalação totalmente
> independentes).

---

## 2. Metodologia exata (Seção 4 do pré-registro)

1. **Rede construída exatamente com a TPM/CM da Seção 1 do pré-registro**
   (não a partir de nenhum exemplo pré-empacotado do PyPhi):

   ```python
   tpm = np.array([
       [0, 0, 0], [0, 0, 1], [1, 0, 1], [1, 0, 0],
       [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 0],
   ])
   cm = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])
   network = pyphi.Network(tpm, cm=cm, node_labels=("A", "B", "C"))
   subsystem = pyphi.Subsystem(network, (1, 0, 0), network.node_indices)
   ```

2. **Checagem cruzada (adicional, não substitui a construção manual
   acima):** o próprio `pyphi.examples.fig4()` desta versão instalada
   contém, verificado por leitura direta do código-fonte
   (`/usr/local/lib/python3.11/dist-packages/pyphi/examples.py:823-838`),
   a **mesma** TPM e CM literais. Construídos os dois objetos `Network`
   (o manual, acima, e `pyphi.examples.fig4()`), seus atributos internos
   `.tpm` e `.cm` (forma canônica multidimensional que o PyPhi usa
   internamente) são **idênticos elemento a elemento**
   (`fig4_bundled_example_matches_preregistered_network: true` em
   `phi_results.json`) — confirmação independente de que a rede
   pré-registrada foi construída corretamente.

3. **API usada, exatamente como especificado na Seção 4:**
   `pyphi.compute.sia(subsystem).phi`. Esta função **existe** na versão
   1.2.0 instalada (`pyphi.compute.sia`, assinatura
   `sia(cache_key, subsystem)` via decorator de memoização — chamada
   normalmente como `pyphi.compute.sia(subsystem)`), então não foi
   necessário substituir por nenhuma API equivalente de versão mais nova.

4. **Nenhum parâmetro não-default alterado.** Configuração completa do
   PyPhi em vigor durante a execução (todos os defaults de fábrica do
   pacote 1.2.0, nenhum `pyphi_config.yml` presente, nenhuma variável de
   ambiente `PYPHI_*` além de `PYPHI_WELCOME_OFF=yes`, que só suprime a
   mensagem de boas-vindas impressa no `stdout` e não afeta o cálculo):

   | Parâmetro | Valor |
   |---|---|
   | `MEASURE` | `EMD` |
   | `PARTITION_TYPE` | `BI` |
   | `SYSTEM_CUTS` | `3.0_STYLE` |
   | `CUT_ONE_APPROXIMATION` | `False` |
   | `PICK_SMALLEST_PURVIEW` | `False` |
   | `ASSUME_CUTS_CANNOT_CREATE_NEW_CONCEPTS` | `False` |
   | `USE_SMALL_PHI_DIFFERENCE_FOR_CES_DISTANCE` | `False` |
   | `SINGLE_MICRO_NODES_WITH_SELFLOOPS_HAVE_PHI` | `False` |
   | `PRECISION` | `6` |
   | `VALIDATE_CONDITIONAL_INDEPENDENCE` | `True` |
   | `VALIDATE_SUBSYSTEM_STATES` | `True` |
   | `PARALLEL_CUT_EVALUATION` | `True` |
   | `PARALLEL_COMPLEX_EVALUATION` / `PARALLEL_CONCEPT_EVALUATION` | `False` |
   | `CACHE_SIAS` | `False` |

   Isto satisfaz literalmente a instrução da Seção 4: "se nenhum
   [parâmetro] for alterado, declarar explicitamente 'todos os defaults
   IIT 3.0 do PyPhi usados, EMD como distância causa-efeito'" — **é
   exatamente o caso aqui**: `MEASURE = EMD`, todo o resto em default de
   fábrica.

---

## 3. Resultado numérico completo

| Quantidade | Valor |
|---|---|
| `Φ` computado | `1.916666` |
| `Φ` alvo (pré-registrado, Seção 1) | `1.916665` |
| `\|diferença\|` | `0.000001` (`9.999999999177334e-07`) |
| Tolerância travada (Seção 5) | `1e-4` |
| Dentro da tolerância? | **Sim** |
| `Φ` arredondado (2 c.d.) | `1.92` (idêntico ao citado em prosa por Mayner et al. 2018) |
| Tempo de computação da SIA (`sia.time`) | `0.166944` s |
| Tempo de computação da CES (`sia.small_phi_time`) | `0.076696` s |
| Estrutura causa-efeito (CES) não-particionada | 6 conceitos |

A diferença de `0.000001` (um ponto na sexta casa decimal, exatamente a
`PRECISION=6` configurada) é consistente com ruído numérico de baixa ordem
do solver de EMD (`pyemd`) entre implementações/versões, não uma
divergência substantiva — muitas ordens de grandeza abaixo da tolerância
travada `1e-4`.

### 3.1 MIP (partição de informação mínima) encontrada

```
Cut [A, B] ━━/ /━━➤ [C]
```

Estruturado: `cut.from_nodes = (0, 1)` → rótulos `('A', 'B')`;
`cut.to_nodes = (2,)` → rótulo `('C',)`. Isto é, a partição severa as
conexões causais direcionadas de `{A,B}` para `{C}`, mantendo as demais
conexões intactas — **idêntico**, palavra por palavra, ao critério da
Seção 1/5 do pré-registro ("the minimal partition is that which removes
the causal connections from AB to C"; "corte das conexões causais de
`{A,B}` para `C`"). `mip_matches_preregistered_ab_to_c: true`.

---

## 4. Aplicação do critério de falsificação (Seção 5 do pré-registro)

> "CONFIRMA reprodução: `Φ` computado igual a `1.916665` dentro de
> tolerância `1e-4`... E a MIP encontrada coincide com a reportada (corte
> das conexões causais de `{A,B}` para `C`)."

Ambas as condições são satisfeitas simultaneamente:

1. `|1.916666 − 1.916665| = 0.000001 < 1e-4` → **satisfeita**.
2. MIP encontrada = corte `{A,B} → {C}` = MIP reportada → **satisfeita**.

**Resultado: CONFIRMED.** Como o resultado confirma (não diverge), a
Seção 5's ramo "FALSIFICA" (checar se a divergência é rastreável a uma
mudança de versão/default do PyPhi) **não se aplica** — não há divergência
numérica ou de MIP a explicar. A única discrepância de ambiente encontrada
(§1.1 acima, incompatibilidade `collections.Iterable` do Python 3.10+) foi
corrigida de forma transparente e documentada **antes** do cálculo, sem
alterar nenhum default de comportamento do PyPhi, e não é a causa de
nenhuma divergência de resultado (não houve divergência).

---

## 5. Corroboração secundária opcional (Seção 6 do pré-registro) — NÃO parte do critério travado

A Seção 6 declara explicitamente: "Um segundo ponto de dado independente
(rede FG do sistema maior da Figura 16, `Φ≈0.069445`, mesma fonte) está
disponível como checagem secundária opcional, mas NÃO é parte do critério
de falsificação travado... se usado, será reportado separadamente como
corroboração adicional, não substituindo o alvo primário."

**Rede completa (Figura 16, 7 nós A–G):** obtida via
`pyphi.examples.fig16()` (esta versão instalada não expõe um alias
`fig16_network()`, mas a TPM/CM/rótulos são idênticos aos documentados —
rótulos `('A','B','C','D','E','F','G')`, TPM de forma `(2,2,2,2,2,2,2,7)`).

**Estado analisado:** esta versão do PyPhi **não** expõe uma função
`fig16_state()` no módulo `examples` — para não inventar um valor (proibido
por `AGENTS.md`), o estado foi obtido por **fetch direto** da mesma URL já
citada no pré-registro Seção 2 como "confirmação adicional"
(`https://pyphi.readthedocs.io/en/latest/examples/2014paper.html`), que
documenta explicitamente, para a análise da Figura 16: rede via
`pyphi.examples.fig16_network()`, `state = (1, 0, 0, 1, 1, 1, 0)` (7 nós
A–G, nós H–L omitidos do sistema completo de 12 nós), complexo menor FG
com `Φ ≈ 0.069445`.

**Subsistema FG:** construído diretamente com os índices dos nós rotulados
`F` (índice 5) e `G` (índice 6) no estado completo `(1,0,0,1,1,1,0)`,
sem passar pelo pipeline `pyphi.compute.condensed()` mencionado na
documentação (que localiza automaticamente os complexos do sistema
maior) — construção direta do subsistema `{F,G}`, análoga à construção do
subsistema completo `{A,B,C}` da análise primária.

| Quantidade | Valor |
|---|---|
| `Φ` computado (subsistema FG) | `0.069445` |
| `Φ` alvo (Seção 6) | `0.069445` |
| `\|diferença\|` | `0.0` (exato, na precisão `PRECISION=6`) |
| MIP (cut) | `Cut [G] ━━/ /━━➤ [F]` |

**Corroboração secundária: reprodução exata.** Isto reforça
independentemente que o estado `(1,0,0,1,1,1,0)` obtido por fetch é o
estado canônico correto para a Figura 16 (a própria concordância exata
com o valor-alvo pré-registrado é evidência disso), mas — seguindo
explicitamente a Seção 6 — **este resultado secundário não substitui, nem
é necessário para, o veredito primário acima**, que já foi decidido apenas
com base na rede ABC/Figura 4.

> **[Correção datada, 2026-08-27 — revisão adversarial, `DISC-DEC-103`,
> Issue 2, severidade BAIXA.]** A direção do corte MIP relatada acima
> (`Cut [G] ━━/ /━━➤ [F]`) **não é uma propriedade determinística** deste
> cálculo. O referee, rodando o mesmo subsistema FG com entrada idêntica
> 5 vezes, obteve a mesma direção 3× e a direção oposta (`Cut [F] ━━/
> /━━➤ [G]`) 2× — as duas direções são um empate genuíno em Φ (ambas dão
> `0,069445`), e qual delas é reportada depende da ordem de conclusão de
> workers sob `PARALLEL_CUT_EVALUATION=True` (default de fábrica), não de
> nenhuma propriedade da rede. **O valor de Φ em si permanece perfeitamente
> estável e reproduzido exatamente** — apenas a direção do corte específica
> varia. Isto não afeta o veredito travado (Seção 5): o referee confirmou
> separadamente que o corte da rede ABC primária (o que de fato importa
> para o critério travado) é unicamente determinado, sem empate, em 8/8
> reexecuções independentes. A afirmação de determinismo total no
> cabeçalho/§7 deste documento ("nenhuma aleatoriedade em nenhuma etapa")
> deve ser lida como válida para o Φ computado em todos os casos, mas não
> para a direção de corte específica reportada nesta corroboração
> secundária opcional em caso de empate.

---

## 6. O que este resultado NÃO estabelece (Seção 7 do pré-registro)

- **Isto é uma checagem de reprodutibilidade computacional de uma métrica
  matematicamente definida — nada mais.** Não é um teste da questão
  metafísica de fundo (se `Φ>0` implica "consciência" em qualquer sentido,
  para qualquer sistema — biológico, de rede, ou sintético), nem da tese
  panpsiquista referenciada em
  `PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §2.2/§6.
- **Nenhuma alegação sobre sistemas biológicos reais** (cérebros, neurônios)
  é feita ou pode ser inferida daqui — a rede testada é um sistema
  booleano abstrato de 3 nós (e, secundariamente, 7 nós), escolhido
  puramente por ser o exemplo canônico e verificável da literatura
  primária de IIT.
- **Nenhuma alegação teórica específica do arcabouço Tamesis** é feita por
  este teste.
- Confirmar que o PyPhi reproduz seu próprio valor publicado **não** é
  evidência sobre a validade da IIT como teoria da consciência — é apenas
  evidência de que a implementação de referência do próprio grupo autor é
  internamente consistente com o que publicaram, o que era exatamente a
  pergunta pré-registrada.

---

## 7. Inventário de arquivos desta etapa

- `analysis/reproduce_phi.py` — código completo, reexecutável,
  determinístico (patch de compatibilidade `collections.abc` documentado
  inline, construção manual da rede a partir da TPM/CM da Seção 1,
  checagem cruzada contra `pyphi.examples.fig4()`, cálculo primário via
  `pyphi.compute.sia`, checagem secundária opcional FG com estado obtido
  por fetch direto e citado).
- `analysis/phi_results.json` — saída numérica bruta completa (config
  snapshot, rede, `Φ`, MIP/cut estruturado, representação textual completa
  da SIA e da CES, resultado secundário opcional).
- `RESULTS_PRIMARY.md` — este documento.

**Nenhum dado externo além do próprio pacote `PyPhi` (via `pip install`) e
uma página de documentação oficial do mesmo grupo (fetch direto, citada) foi
usado.** Nenhum valor numérico foi inventado ou assumido de memória —
sempre que um valor não estava disponível diretamente no pacote instalado
(o estado canônico da Figura 16), ele foi obtido por fetch direto de uma
fonte já citada no pré-registro, ou a checagem correspondente foi reportada
como não-completável em vez de adivinhada (ver histórico de execução do
script — a primeira tentativa, sem o fetch, reportou corretamente
"cannot construct... without inventing a value" em vez de uma resposta
fabricada).
