# Nota técnica — `P_phys` / `NP_phys`: definições e teoremas de simulação/limite

`PVSNP-PHYS-001` · onda `PORTFOLIO-REVIEW-AFTER-SOBOLEV-CHAIN-2026-08-09`
Data: 2026-08-09. Documento integrador — reúne `DEFINITIONS.md`,
`ASSUMPTIONS.md`, `KNOWN_RESULTS_MATRIX.md` e `PROOF_SKETCH.md` num único
produto legível. As fontes primárias com status verificado/aproximado estão
em `REVIEWS/AUDIT_REPORT.md`.

## Enunciado clássico (não substituído — AGENTS.md)

> Determinar se toda linguagem aceita em tempo polinomial por uma máquina
> de Turing não determinística também é aceita em tempo polinomial por uma
> máquina determinística.

Nada neste documento decide, aproxima ou torna essa pergunta alcançável.

## 1. Objetivo desta nota

Definir `P_phys` e `NP_phys` — noções de complexidade computacional
ancoradas em modelos físicos/analógicos em vez de máquinas de Turing — de
forma formal o suficiente para ter propriedades internas prováveis, **sem**
alegar que isso decide `P` vs `NP` clássico.

## 2. Por que não existe um único `P_phys`

`P`/`NP` clássicos são definidos sobre um objeto fixo (máquina de Turing,
alfabeto binário). "Complexidade física" não tem esse objeto fixo — depende
de três escolhas livres:

- **`E`** — esquema de codificação de instância combinatória em
  configuração física;
- **`M`** — modelo físico (analógico contínuo, BSS sobre `ℝ`/`ℂ`, rede
  neural recorrente analógica, sistema termodinâmico ruidoso, etc.);
- **`R`** — medida de recurso física que faz o papel de "tempo" (passos,
  energia, bits de precisão).

Dado `(E,M,R)`, com custo `cost_{M,R} : Inst_E → ℝ≥0`:

```text
P_phys(E,M,R)  = { L : existe procedimento fisico em M decidindo L com
                   cost_{M,R} polinomial no tamanho de E(x) }
NP_phys(E,M,R) = { L : existe procedimento fisico de verificacao e
                   certificado fisico c(x) com cost_{M,R}(x,c(x))
                   polinomial, x em L sse tal certificado existe }
```

Mesma forma lógica de `P`/`NP`, `M` no lugar da máquina de Turing. Isto é
uma generalização de forma, não um resultado — ver `DEFINITIONS.md` para o
detalhamento completo, inclusive a noção de **ponte de simulação**: `(E,M,R)`
admite ponte se existem polinômios `p,q` traduzindo custo em `M` para tempo
de Turing e vice-versa; se sim, `P_phys(E,M,R)=P` e `NP_phys(E,M,R)=NP` —
mas isso apenas transporta a pergunta, não a decide.

## 3. Instanciações concretas na literatura (status detalhado em `KNOWN_RESULTS_MATRIX.md`)

| Modelo | Fonte (verificada bibliograficamente) | Comportamento |
|---|---|---|
| BSS sobre `ℝ`/`ℂ` | Blum–Shub–Smale, *Complexity and Real Computation*, 1998 | `P_ℝ`/`NP_ℝ` bem definidas; relação com clássico via Bürgisser–Cucker 2006, **condicional a GRH** |
| Rede neural recorrente analógica, pesos reais idealizados | Siegelmann & Sontag 1994; Siegelmann 1999 | poder "super-Turing" **sob precisão infinita** |
| Computação analógica com ruído físico | Maass & Orponen, *Neural Computation* 10(5), 1998 | ruído arbitrariamente pequeno colapsa o poder a autômatos finitos |
| Vidro de spin (modelo SK) | Talagrand, *Ann. of Math.* 163, 2006 | fórmula de Parisi rigorosa para energia livre — resultado de física estatística, **não** uma classe de complexidade computacional |

Estas triplas não são equivalentes entre si sem hipótese adicional
(ver `DEFINITIONS.md` §4-5). Isso **é** a formalização de `PNP-GAP-002`.

## 4. Teoremas de simulação/limite (o que existe, e nada além disso)

Dois padrões emergem na literatura pesquisada, ambos condicionais:

1. **Colapso sob ruído/precisão finita** (Maass–Orponen 1998): um modelo
   analógico idealizado com poder super-Turing, quando forçado a operar
   sob ruído físico realista arbitrariamente pequeno, perde esse poder —
   colapsa ao de autômatos finitos. Isto sugere (não prova em geral) que
   computação física *realista* não escapa de `P`/classes clássicas.
2. **Relação condicional a GRH** (Bürgisser–Cucker 2006): partes da
   estrutura de complexidade do modelo BSS sobre `ℂ` se relacionam com
   classes clássicas apenas assumindo a Hipótese Generalizada de Riemann —
   uma hipótese matemática independente do problema físico em si.

Nenhum dos dois padrões estabelece uma **ponte de simulação universal**
(seção 2) capaz de transportar uma eventual separação `P_phys ≠ NP_phys`
para uma separação superpolinomial clássica de máquinas de Turing. Essa
ausência é `PNP-GAP-001`.

Um teorema condicional interno, na forma abstrata desses dois padrões, é
enunciado em `PROOF_SKETCH.md` §2.2: se o custo físico de um par `(E,M,R)`
é "polinomialmente equivalente" (nos dois sentidos) ao custo de uma máquina
de Turing de referência, e este último é polinomial, então o custo físico
também é. **Este teorema não foi formalizado em Lean nesta sessão** (razão
técnica documentada em `PROOF_SKETCH.md` §2.1); as definições subjacentes e
duas propriedades estruturais triviais (reflexividade, simetria) *foram*
formalizadas, sem `sorry`, em `FORMAL/PvsNPPhys.lean`.

## 5. Condição de parada — atingida, reportada, não forçada

```text
(i)  indefinicao de codificacao: 4 triplas (E,M,R) da literatura, nao
     equivalentes sem hipotese extra -- PNP-GAP-002
(ii) ausencia de ponte para separacao superpolinomial de Turing:
     nenhuma fonte encontrada estabelece essa ponte de forma universal --
     os resultados existentes ou colapsam o modelo fisico a poder classico
     (Maass-Orponen), ou dependem de GRH (Burgisser-Cucker), ou resolvem
     um problema fisico distinto sem reducao de complexidade (Talagrand)
     -- PNP-GAP-001
```

Ambas as condições da tarefa foram atingidas simultaneamente. Por
instrução explícita ("pare e reporte, não force"), esta auditoria não tenta
construir a ponte nem escolher uma tripla `(E,M,R)` canônica. Ver
`GAP_REGISTER.yaml` para os quatro gaps registrados (`PNP-GAP-001` a
`PNP-GAP-004`, todos `OPEN`) e `REVIEWS/AUDIT_REPORT.md` para a separação
completa entre afirmações verificadas e aproximadas nesta sessão.

## 6. O que esta nota não afirma

```text
nao afirma P_phys = NP_phys para nenhum modelo concreto
nao afirma P_phys != NP_phys para nenhum modelo concreto
nao afirma que qualquer resultado aqui decide, aproxima ou torna
   alcancavel P versus NP classico
nao endossa o "Physical Computation Axiom" do documento legado -- ver
   ASSUMPTIONS.md secao 3 e GAP_REGISTER.yaml PNP-GAP-003
```
