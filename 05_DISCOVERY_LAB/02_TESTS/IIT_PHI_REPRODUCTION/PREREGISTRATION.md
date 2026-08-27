# Pré-registro: Reprodução via PyPhi do Φ publicado para a rede ABC de Oizumi, Albantakis & Tononi (2014)

**Status:** LOCKED
**Data de criação:** 2026-08-27 (Fase 0, `DISC-DEC-101`)
**Data de travamento:** 2026-08-27 (`DISC-DEC-102`)
**Autor (agente/sessão):** Tamesis Discovery Lab, sessão 2026-08-27 — Fase 0
conduzida por agente de pesquisa dedicado (mandato `DISC-DEC-101`); redigido
e travado pela sessão orquestradora após revisão explícita da
especificação da rede e da citação do valor-alvo.
**Origem:** `PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §2.2;
`DISC-IIT-PHI-REPRO-001` em `01_PORTFOLIO/TEST_QUEUE.yaml`.

> Preenchido e commitado ANTES de rodar `PyPhi`. Depois deste commit de
> lock, nenhum campo abaixo pode ser alterado sem abrir um novo
> pré-registro.

## 1. Hipótese exata

O pacote `PyPhi` (autoria do próprio grupo de Tononi — Mayner et al. 2018,
*PLoS Comput Biol* 14(7):e1006343), aplicado à rede booleana de 3 nós ABC
definida na Figura 4 de Oizumi, Albantakis & Tononi (2014, *PLoS Comput
Biol* 10(5):e1003588) — `A = OR(B,C)`, `B = AND(A,C)`, `C = XOR(A,B)`, no
estado atual `(1,0,0)` — reproduz o valor de Φ do sistema completo `{A,B,C}`
publicado na literatura primária desta linhagem: **`Φ = 1.916665`**
(citado como `1.92` em Mayner et al. 2018, seção de demonstração: "we can
verify that the Φ value of the example system in [Oizumi et al. 2014] is
1.92 and the minimal partition is that which removes the causal
connections from AB to C").

**Especificação exata da rede (TPM e matriz de conectividade), a partir
da qual a rede será reconstruída em `PyPhi`:**
- `TPM = [[0,0,0],[0,0,1],[1,0,1],[1,0,0],[1,0,0],[1,1,1],[1,0,1],[1,1,0]]`
- `CM = [[0,1,1],[1,0,1],[1,1,0]]`
- Estado analisado: `(1,0,0)`
- Subsistema: `{A,B,C}` completo

## 2. Fonte de dado

- **Especificação da rede:** Oizumi M, Albantakis L, Tononi G (2014).
  "From the Phenomenology to the Mechanisms of Consciousness: Integrated
  Information Theory 3.0." *PLoS Comput Biol* 10(5):e1003588. DOI:
  `10.1371/journal.pcbi.1003588`. Figura 4 (definição da rede ABC, estado
  100); Figuras 6, 8, 9, 10 (estrutura causa-efeito); Figuras 12–13
  (Φ de sistema).
- **Valor-alvo numérico (citação verificada por fetch direto):** Mayner
  WGP, Marshall W, Albantakis L, Findlay G, Marchman R, Tononi G (2018).
  "PyPhi: A toolbox for integrated information theory." *PLoS Comput
  Biol* 14(7):e1006343. DOI: `10.1371/journal.pcbi.1006343` — seção de
  demonstração, declaração em prosa explícita citada acima.
- **Confirmação adicional (documentação oficial do pacote, mesmo grupo):**
  https://pyphi.readthedocs.io/en/latest/examples/2014paper.html (seção
  da Figura 12: `sia.phi` → `1.916665`); especificação de TPM/CM em
  https://github.com/wmayner/pyphi/blob/develop/pyphi/examples.py
  (`fig4_network`).
- **Nota de proveniência importante:** o texto/legendas do paper de 2014
  em si, conforme lido por fetch direto nesta Fase 0 (PLOS + mirror PMC),
  NÃO contém o dígito `1.92`/`1.916665` impresso em prosa — o número
  aparece apenas graficamente na Figura 13 (não inspecionada visualmente
  nesta Fase 0; a URL da imagem no PMC retornou um desafio CAPTCHA). O
  valor-alvo travado aqui repousa na declaração em prosa do paper
  companheiro de 2018 (mesmo grupo, revisado por pares, citando
  explicitamente o exemplo de 2014) — considerada citação primária
  suficiente para este pré-registro, mas o fato é registrado aqui para
  transparência total.

## 3. Modelo nulo / hipótese concorrente

Se a implementação de `PyPhi` não reproduzir o valor publicado — por erro
na especificação da rede acima, por mudança de comportamento padrão entre
versões do pacote (a documentação oficial nota mudanças de convenção de
"background condition"/poda de nós entre versões), ou por erro genuíno no
valor originalmente publicado — o Φ computado divergirá do valor-alvo além
da tolerância da Seção 5, e/ou a partição de informação mínima (MIP)
encontrada não coincidirá com a reportada.

## 4. Estatística de teste

Construir a rede em `PyPhi` exatamente com a TPM/CM da Seção 1. Fixar e
registrar a versão exata do pacote `PyPhi` instalada (`pip show pyphi`)
antes de rodar, junto com quaisquer parâmetros não-default alterados (se
nenhum for alterado, declarar explicitamente "todos os defaults IIT 3.0
do PyPhi usados, EMD como distância causa-efeito"). Computar
`pyphi.compute.sia(subsystem).phi` para o subsistema completo `{A,B,C}`
no estado `(1,0,0)`, e registrar também a partição (MIP) encontrada.

## 5. Critério de falsificação

- **CONFIRMA reprodução:** `Φ` computado igual a `1.916665` dentro de
  tolerância `1e-4` (equivalentemente, arredonda para `1.92`), E a MIP
  encontrada coincide com a reportada (corte das conexões causais de
  `{A,B}` para `C`).
- **FALSIFICA/não reproduz:** `Φ` computado difere além da tolerância
  acima, OU uma MIP diferente é encontrada. Neste caso, antes de concluir
  que o valor publicado está incorreto, checar explicitamente se a
  divergência é rastreável a uma mudança de versão/default do `PyPhi`
  documentada (ex. poda de "minor complex", mudança de background
  condition) — se for, registrar como `REPLICATION_FAILED` por mudança de
  ferramenta, não como refutação do valor original de 2014.

## 6. Correção para comparações múltiplas

Um único alvo numérico, uma única rede, um único estado — não há família
de comparações múltiplas nesta análise primária. Um segundo ponto de
dado independente (rede FG do sistema maior da Figura 16, `Φ≈0.069445`,
mesma fonte) está disponível como checagem secundária opcional, mas NÃO é
parte do critério de falsificação travado acima — se usado, será
reportado separadamente como corroboração adicional, não substituindo o
alvo primário.

## 7. O que NÃO está sendo testado

- A questão metafísica de fundo — se `Φ>0` implica "consciência" em
  qualquer sentido, para qualquer sistema (biológico, de rede, ou
  sintético). Isto é uma checagem de reprodutibilidade computacional de
  uma métrica matematicamente definida, não um teste da tese
  panpsiquista (`PROGRAMA_CONSCIENCIA_LOGICA_E_REALIDADE.md` §2.2, §6).
- Nenhuma alegação sobre sistemas biológicos reais (cérebros, neurônios)
  — a rede testada é um sistema booleano abstrato de 3 nós, escolhido
  puramente por ser o exemplo canônico e verificável da literatura
  primária de IIT.
- Nenhuma alegação teórica específica do arcabouço Tamesis.

---

## [Preenchido depois da análise] Resultado

## [Preenchido depois da reexecução adversarial] Veredito adversarial
