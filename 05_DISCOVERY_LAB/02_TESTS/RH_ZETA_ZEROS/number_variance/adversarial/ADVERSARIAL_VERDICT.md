# Veredito adversarial — DISC-RH-NUMBER-VARIANCE-001

**Papel:** reprodução adversarial independente, escopo travado pelo
orquestrador: atacar a exclusão GUE (Modelo A) nos dois pontos decisivos
primários e verificar se o veredito ternário formal (`INCONCLUSIVE` /
`PARTIAL_DISAGREEMENT`) se reproduz.

**Disciplina seguida:** estimador, Modelo A e Modelo B implementados do zero
(`estimator_adv.py`), validados contra ground truth sintético (rede regular,
processo de Poisson, força bruta, checagem analítica do Modelo A) **antes**
de qualquer dado real ser tocado, e só então comparados ao `estimator.py` /
`run_primary.py` / `primary_result.json` do agente primário. `zeros4.txt`
não foi tocado. Nenhuma alegação sobre RH em nenhuma hipótese.

## 1. Resultado principal: um terceiro bug real, encontrado nesta reprodução

A regra de decisão exige reprodução adversarial exatamente porque o próprio
agente primário já havia encontrado e corrigido DOIS bugs reais antes de
tocar dado real (normalização GUE 2×; convenção de fronteira no estimador
exato). **Esta reprodução encontrou um TERCEIRO bug real, não detectado nas
validações pré-lock do primário**, no mesmo módulo (`estimator.py`) que já
havia sido corrigido duas vezes.

### 1.1 Descrição do bug

Em `estimator.py::block_number_variance`, cada bloco `[a,b]` calcula
`y_lo = a + L/2` e passa `y_lo` (não `a`) para
`_exact_window_integral(x_slice, y_lo, y_hi, L)`. Dentro dessa função, o
valor inicial `n0` da integral em escada é recomputado fazendo
`y_lo - L/2` — ou seja, o código tenta recuperar `a` fazendo
**`(a + L/2) - L/2`**. Em ponto flutuante IEEE754 isso **não devolve `a`
exatamente** em geral (erro de arredondamento de ~1 ULP, tipicamente
`1e-13` a `1e-15` em valor absoluto, podendo cair para qualquer um dos dois
lados de `a`).

Isso importa porque **o bloco 0 de todo dataset tem `a = x_min` — o menor
dado do dataset, exatamente** (`block_edges = np.linspace(x_min, x_max,
B+1)` sempre faz `edges[0] = x_min` bit a bit). Quando o erro de
arredondamento faz `(y_lo - L/2)` cair **ligeiramente abaixo** do `a` real,
o ponto `x_min` — que deveria "sair" da janela exatamente em `y = y_lo` e
portanto não contar mais para `y > y_lo` — fica erroneamente incluído em
`n0`, e nenhum evento `-1` compensador aparece na lista de eventos do
resto do algoritmo (a saída desse ponto específico acontece exatamente em
`y_lo`, fora do domínio de integração aberto `(y_lo, y_hi)`). O resultado:
`n(L;y)` fica inflado em `+1` **permanentemente através de todo o bloco**,
inflando a variância daquele bloco especificamente (e, com poucos blocos —
exatamente o regime dos pontos decisivos, `B=11` — inflando `SE` de forma
desproporcional).

A direção do erro de arredondamento depende dos bits específicos de `a` e
`L` (efetivamente imprevisível a priori sem calcular), então o bug aparece
em **alguns** pontos da grade e não em outros — não é um bug que grita "todo
resultado está errado", o que provavelmente contribuiu para não ter sido
pego nas validações pré-lock do primário (nenhuma delas usa `B` pequeno com
um dado real cujo `x_min` é *exatamente* um zero real coincidindo bit a bit
com a borda do bloco 0 na mesma combinação `(a,L)` da análise real).

### 1.2 Confirmação (3 métodos independentes concordam, só o do primário diverge)

Reproduzido de forma mínima e autocontida em `bug_report_block0_fp.py`
(dataset sintético, sem depender de dado real): `V` pelo método do
primário = `1.244320`; `V` corrigido (evitando o round-trip, usando `a`
diretamente) = `0.245910`; `V` por força bruta numa grade ultrafina
independente = `0.245910` — os dois métodos independentes concordam
exatamente, só o método com o round-trip diverge.

No dado REAL (bloco 0 de `zeros3`, `L=210.50`, o ponto decisivo primário):
meu método exato (`estimator_adv.py`, construído do zero) dá `V_bloco0 =
0.4122`; uma verificação por força bruta totalmente independente (contagem
literal em janela fechada, grade ultrafina de 2M pontos) dá `0.4103`
(diferença 0,5%, ruído numérico esperado); o código do primário
(`estimator.py`, rodado literalmente, mesmo dado) dá `V_bloco0 = 1.4128` —
mais de 3× o valor correto, o único discrepante dos três.

### 1.3 Alcance do bug na grade completa

Comparando meu grid completo (bug-free, validado) contra
`primary_result.json` ponto a ponto (`compare_and_diagnose.py`/`.log`):

**15 dos 23 pontos usáveis da grade combinada (65%) têm bloco 0 afetado**
pelo bug — em todos os 15, `SE` e `V̂` do primário saem inflados
(às vezes moderadamente, às vezes por >10×) frente ao valor correto. Nos
outros 8 pontos, o arredondamento por coincidência caiu do lado seguro e os
números batem exatamente entre os dois códigos.

**Dos dois pontos DECISIVOS primários (Seção 4 do pré-registro):**
- `zeros1` (`L=2155,04`, `B=11`): arredondamento caiu do lado seguro —
  `V̂`, `SE`, `z_A`, `z_B` do primário **batem exatamente** com os meus.
- `zeros3` (`L=210,50`, `B=11`): arredondamento caiu do lado ruim —
  **os números do primário para o ponto decisivo mais citado do teste
  estão errados**, com `SE` inflado ~31× (`0,0895` reportado vs `0,00287`
  correto).

## 2. Meus números (independentes, validados) vs primário

| Dataset | `L` | Fonte | `V̂` | `SE` | Modelo A | `z_A` | Modelo B | `z_B` |
|---|---|---|---|---|---|---|---|---|
| `zeros1` | 2155,04 | primário | 0,3600 | 0,0038 | 1,1237 | **−203,25** | 0,3049 | +14,66 |
| `zeros1` | 2155,04 | **adversarial** | 0,3600 | 0,0038 | 1,1237 | **−203,25** | 0,3049 | +14,66 |
| `zeros3` | 210,50 | primário (⚠ bug) | 0,5182 | 0,0895 | 0,8880 | **−4,13** | [0,4797;0,6092] | 0,00 |
| `zeros3` | 210,50 | **adversarial (correto)** | 0,4272 | 0,0029 | 0,8880 | **−160,76** | [0,4797;0,6092] | **−18,29** |

`zeros1` reproduz EXATAMENTE (não afetado pelo bug). `zeros3` NÃO reproduz o
número relatado — o valor correto de `z_A(zeros3)` é `−160,76`, não `−4,13`.
(Fórmulas de Modelo A/B verificadas independentemente por fetch direto de
`arxiv.org/pdf/2211.14918`, Seção 1.4, antes de qualquer cômputo — batem
exatamente com a transcrição do pré-registro.)

Validações sintéticas próprias, todas `PASS` antes de tocar dado real:
rede regular (bate com fórmula fechada exata `f(1-f)`, `f`=parte
fracionária de `L`, diferença `<1e-8` em todos os `L` testados, incluindo
os 2 primários reais); processo de Poisson (recupera `V(L)=L`, 99,5% dos
184 testes com `|z|<3`, na MESMA grade `(L,B)` real de ambos os datasets,
incluindo `B=11`); força bruta vs integral exata (`<0,4%` de diferença
relativa em 8 `L`'s incluindo os 2 primários); checagem analítica do
Modelo A (cancelamento exato do termo `π²L` contra `−2πL·Si(2πL)` no limite
`L→∞`, `V_A(0)=0`, não-negatividade); identidade algébrica do Modelo B
verificada numericamente (diferença relativa `1,4e-15` contra soma "crua"
com `Λ(n)` explícito).

## 3. Veredito sobre o componente GUE-EXCLUSION (escopo travado desta reprodução)

**CONFIRMADO — e mais forte do que relatado, não mais fraco.**

O Modelo A (GUE ingênuo estendido) é excluído por margem enorme em AMBOS os
regimes de altura independentes:
- `zeros1`: `z_A = −203,25` (idêntico ao primário, não afetado pelo bug).
- `zeros3`: `z_A = −160,76` (**não** `−4,13` como relatado — o número
  relatado estava artificialmente atenuado pelo bug de `SE`; corrigido, a
  exclusão de GUE em `zeros3` é quase tão extrema quanto em `zeros1`, na
  MESMA ordem de grandeza, não um fator ~40× mais fraco como o relatório
  original sugeria).

A rejeição do Modelo A não depende de nenhum ponto isolado: nos 23/23
pontos da grade combinada (16 `zeros1` + 7 `zeros3`) que computei
independentemente, `z_A` é negativo e `|z_A|≥3` em todos — GUE rejeitado em
toda a grade acessível, nos dois datasets, consistente com o que o
pré-registro já reportava para essa parte específica (não afetada pelo
bug na direção qualitativa, já que o bug infla `SE` mas não muda o sinal
de `V̂−modelo_A`, que é sempre fortemente negativo).

## 4. O veredito ternário formal se reproduz?

**O veredito de TOPO (`INCONCLUSIVE`) se reproduz.** Nem `BERRY_FAVORED` nem
`GUE_FAVORED` são satisfeitos com os números corrigidos — a mesma conclusão
do primário.

**O SUBCASO não se reproduz como relatado.** O primário relatou
`PARTIAL_DISAGREEMENT` (leitura: os dois datasets "discordam de direção" —
`zeros3` favoreceria o padrão Berry (`|z_B|<2`), `zeros1` não). Isso era um
artefato direto do bug: com `z_B(zeros3)` corrigido para `−18,29` (não
`0,00`), `zeros3` **também** rejeita formalmente o Modelo B pelo limiar de
3σ — exatamente o mesmo padrão que já acontecia em `zeros1`
(`|z_A|≥3` e `|z_B|≥3` nos dois datasets). Aplicando a regra travada da
Seção 7 do pré-registro aos números corrigidos:

- `zeros1`: `|z_A|=203,25≥3` **e** `|z_B|=14,66≥3` → ambos rejeitados.
- `zeros3`: `|z_A|=160,76≥3` **e** `|z_B|=18,29≥3` → ambos rejeitados.

→ subcaso correto = **`NEITHER_MODEL`**, não `PARTIAL_DISAGREEMENT`.

Isso não muda o veredito formal de topo (`INCONCLUSIVE` continua sendo
`INCONCLUSIVE`), mas muda a HISTÓRIA sobre *por que* é inconclusivo: não é
que os dois datasets apontem em direções diferentes — é que os dois
datasets, de forma CONSISTENTE, rejeitam os dois modelos pelo limiar formal
de 2-3σ pré-declarado, mesmo com o dado estando visivelmente mais perto do
Modelo B em distância absoluta nos dois casos (`zeros1`: `|V̂−B|=0,055` vs
`|V̂−A|=0,764`; `zeros3` corrigido: `|V̂−B|=0,0525` vs `|V̂−A|=0,461`, ainda
~9× mais perto de Berry). A "leitura honesta" que o próprio pré-registro já
fazia para `zeros1` (poder alto, `SE` pequeno o bastante para que uma
diferença absoluta pequena cruze o limiar de 2σ) se aplica igualmente a
`zeros3` depois da correção — não é mais uma peculiaridade de um único
dataset, é o padrão geral do teste nos dois pontos decisivos.

A checagem de sanidade S1 (mesmo sinal de `z_A` primário/secundário) segue
`PASS` nos dois datasets com os números corrigidos.

## 5. Recomendação para o orquestrador

- **Não abrir o holdout `zeros4`** com base neste resultado — o veredito
  formal continua `INCONCLUSIVE`, e a condição de parada da Seção 8 do
  pré-registro é sobre achados que favorecem um modelo, não é o caso aqui.
- **O componente GUE-EXCLUSION (`z_A` extremo nos dois regimes) fica
  CONFIRMADO por esta reprodução adversarial** — pode ser reportado como
  achado real (não mais "candidato"), com os valores corrigidos
  (`z_A(zeros1)=−203,25`, `z_A(zeros3)=−160,76`, não `−4,13`).
- **`estimator.py` do primário precisa da correção do round-trip** (usar
  `a` diretamente em `block_number_variance` ao computar `n0`, em vez de
  repassar `y_lo` e recompor `y_lo − L/2` dentro de
  `_exact_window_integral`) antes de qualquer reanálise futura que reuse
  esse código — o bug afeta 65% da grade descritiva e um dos dois pontos
  decisivos. Ver `bug_report_block0_fp.py` para a correção mínima e prova
  de conceito.
- `PREREGISTRATION.md` (Seção "Resultado", campos `V̂`, `SE`, `z_A`, `z_B`
  de `zeros3` primário, e a tabela/curva descritiva da grade completa) e
  `primary_result.json` precisam de correção antes de serem citados como
  registro definitivo — o subcaso `PARTIAL_DISAGREEMENT` relatado não é o
  resultado correto da regra travada; é `NEITHER_MODEL`.

## 6. O que NÃO está sendo alegado

Nenhuma alegação sobre RH em nenhuma hipótese. O teste discrimina duas
hipóteses estatísticas sobre a variância local do número de zeros de zeta
em altura finita — não avalia se os zeros estão na linha crítica. O
holdout `zeros4.txt` permanece selado; nenhuma linha de dado numérico desse
arquivo foi lida nesta reprodução.

---

**Arquivos desta pasta:** `ADVERSARIAL_NOTE.md` (plano, escrito antes de
rodar qualquer coisa), `estimator_adv.py` (estimador + Modelo A/B, do
zero), `load_data_adv.py`, `validate_lattice.py` / `.json` / `.log`,
`validate_poisson.py` / `.json` / `.log`, `validate_bruteforce.py` / `.json`
/ `.log`, `validate_model_a_asymptotic.py` / `.json` / `.log`,
`validate_model_b.py` / `.json` / `.log`, `run_adv_primary.py` (análise
primária adversarial completa) / `adv_primary_result.json` /
`adv_primary_run.log`, `compare_and_diagnose.py` / `.log` (comparação
célula a célula + diagnóstico do bug), `bug_report_block0_fp.py` / `.json`
/ `.log` (reprodução mínima do bug), este arquivo.
