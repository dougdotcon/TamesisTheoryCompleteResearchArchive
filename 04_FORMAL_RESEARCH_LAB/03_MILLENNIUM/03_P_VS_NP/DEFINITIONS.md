# Definições — `P_phys` / `NP_phys`

Auditoria `PVSNP-PHYS-001`, onda `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`.
Substitui o placeholder `NOT_FORMALIZED`.

## 0. Enunciado clássico ao lado (obrigatório por AGENTS.md)

Ver `OFFICIAL_STATEMENT.md`: "Determinar se toda linguagem aceita em tempo
polinomial por uma máquina de Turing não determinística também é aceita em
tempo polinomial por uma máquina determinística." As definições abaixo **não
substituem** este enunciado; elas definem uma família paralela de objetos
que só faz contato com ele se, e somente se, um teorema de ponte explícito
for provado (Seção 3, e ver `PNP-GAP-001`).

## 1. Por que `P_phys` não é uma classe única

Ao contrário de `P`/`NP` clássicos — fixados pela definição de máquina de
Turing — "complexidade física" depende de três escolhas livres que a
literatura não unifica:

```text
(E) esquema de codificação   : instância combinatória -> configuração física
(M) modelo físico             : que tipo de sistema físico/analógico realiza o cálculo
(R) medida de recurso         : que grandeza física conta como "tempo" (passos, energia, precisão)
```

Sem fixar as três, "`P_phys` = `NP_phys`?" não é uma pergunta — é uma
família de perguntas, uma por tripla `(E, M, R)`. Isso já é a raiz de
`PNP-GAP-002` ("Dependência de codificação e recursos precisa ser
formalizada").

## 2. Esquema geral de definição

Dado um modelo físico `M` com espaço de instâncias `Inst_E` (instâncias
combinatórias sob a codificação `E`) e uma função de custo físico
`cost_{M,R} : Inst_E -> ℝ≥0 ∪ {∞}` (tempo físico, energia dissipada, ou bits
de precisão exigidos, conforme `R`):

```text
P_phys(E,M,R)  := { L : existe um procedimento físico em M que decide L,
                     com cost_{M,R}(x) limitado por um polinômio em
                     |E(x)| (tamanho da instância codificada) }

NP_phys(E,M,R) := { L : existe um procedimento físico de VERIFICAÇÃO em M
                     e um "certificado físico" c(x) tais que
                     cost_{M,R}(x, c(x)) é polinomial em |E(x)|,
                     e x ∈ L sse existe tal certificado }
```

Esta é a mesma forma lógica da definição clássica de `P`/`NP`, com a
máquina de Turing substituída por `M` e o passo de computação substituído
por `cost_{M,R}`. **Isto é uma generalização de forma, não um novo
resultado matemático** — cada instanciação concreta de `(E,M,R)` é uma
definição, não um teorema, até que se prove algo sobre ela.

## 3. Ponte de simulação (o objeto que decide se isto toca P vs NP clássico)

```text
Definição (ponte de simulação). Uma tripla (E,M,R) ADMITE uma ponte
polinomial para máquinas de Turing se existem polinômios p, q tais que:
  (i)  toda decisão em M com custo cost_{M,R}(x) ≤ T pode ser simulada por
       uma máquina de Turing determinística em tempo ≤ p(T, |E(x)|);
  (ii) toda computação de uma máquina de Turing em tempo T sobre a mesma
       linguagem pode ser realizada em M com cost_{M,R}(x) ≤ q(T, |E(x)|).
```

Se `(E,M,R)` admite uma ponte de simulação, então `P_phys(E,M,R) = P` e
`NP_phys(E,M,R) = NP` — mas isso **não decide** `P` vs `NP`, apenas
transporta a pergunta sem alterá-la. Se `(E,M,R)` **não** admite ponte de
simulação polinomial (caso dos modelos analógicos idealizados com precisão
infinita, Seção 4), `P_phys(E,M,R)` e `P` podem divergir sem que isso diga
qualquer coisa sobre `P` vs `NP` clássico — a divergência estaria inteira
no lado físico/de codificação, não no lado da máquina de Turing.

**Esta auditoria não constrói nem afirma a existência de uma ponte de
simulação universal.** Isso é exatamente `PNP-GAP-001` ("Ponte universal
para máquinas de Turing ausente"), e permanece `OPEN` — ver `PROOF_SKETCH.md`,
seção "Condição de parada".

## 4. Instanciações concretas encontradas na literatura (ver `KNOWN_RESULTS_MATRIX.md` para status verificado/aproximado)

| `(E,M,R)` | Fonte | Nota |
|---|---|---|
| máquina BSS sobre `ℝ` (ou `ℂ`), custo = nº de operações aritméticas unitárias | Blum–Shub–Smale, *Complexity and Real Computation*, Springer 1998 | Define `P_ℝ`, `NP_ℝ` (e análogos sobre `ℂ`); aritmética real como primitiva, não bits |
| rede neural recorrente analógica (ARNN), custo = passos discretos, pesos reais de precisão arbitrária | Siegelmann & Sontag 1994; Siegelmann 1999 | Poder "super-Turing" **sob precisão infinita idealizada** |
| computação analógica de tempo discreto com ruído físico limitado | Maass & Orponen, *Neural Computation* 10(5):1071–1095, 1998 | Ruído analógico arbitrariamente pequeno colapsa o poder do modelo ao de autômatos finitos |
| têmpera simulada / recozimento físico sobre vidros de spin (custo = tempo até equilíbrio) | Talagrand, *Ann. of Math.* 163 (2006), 221–263 (fórmula de Parisi, modelo SK) | Resultado sobre energia livre de um modelo físico específico, **não** sobre uma classe de complexidade `P_phys`/`NP_phys` — ver ressalva em `KNOWN_RESULTS_MATRIX.md` |

Estas quatro triplas `(E,M,R)` **não são equivalentes entre si**: cada uma
tem sua própria noção de "polinomial" e nenhum teorema encontrado nesta
sessão as unifica sem hipótese adicional (ex.: a relação entre o modelo BSS
sobre `ℂ` e classes clássicas depende da Hipótese Generalizada de Riemann —
Bürgisser & Cucker 2006, ver `KNOWN_RESULTS_MATRIX.md`).

## 5. O que este documento explicitamente não faz

```text
não afirma P_phys = NP_phys para nenhuma tripla concreta
não afirma P_phys != NP_phys para nenhuma tripla concreta
não afirma que qualquer resultado acima decide P vs NP classico
não escolhe uma tripla (E,M,R) "canonica" -- a escolha permanece em aberto
```
