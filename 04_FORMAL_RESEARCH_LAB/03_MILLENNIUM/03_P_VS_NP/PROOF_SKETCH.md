# Esboço

Auditoria `PVSNP-PHYS-001`. Substitui o placeholder `NO_EXECUTION`.
**O produto permitido continua sendo uma nota técnica de complexidade
física (`RESULTS/TECHNICAL_NOTE.md`), não uma tentativa de prova de `P` vs
`NP`.**

## 1. O que existe para provar aqui

Dado `DEFINITIONS.md`, os únicos alvos internos legítimos são:

```text
(a) propriedades estruturais das definicoes de P_phys/NP_phys em si
    (fechamento, reflexividade/simetria da nocao de "equivalencia de
    simulacao", etc.) -- nao dizem nada sobre P vs NP classico
(b) teoremas de simulacao/limite JA EXISTENTES na literatura, relatados
    com exatidao e com suas hipoteses (KNOWN_RESULTS_MATRIX.md #3, #4)
(c) uma ponte universal de (a) ou (b) para uma separacao superpolinomial
    de maquinas de Turing -- NAO TENTADA aqui, ver Secao 3
```

## 2. (a) e (b): o que foi formalizado nesta sessão

### 2.1 Lean (definições + propriedades internas triviais)

`FORMAL/PvsNPPhys.lean` (rascunho, não integrado — ver seção 4) formaliza:

- `AffineBounded f`: uma aproximação simplificada de "`f` cresce
  polinomialmente" usando limitante afim `c·n+c` em vez de grau geral
  `c·n^k+c`. **Simplificação deliberada e documentada no próprio arquivo**:
  evita depender da API de `Nat.pow`/`Polynomial` do Mathlib para manter o
  rascunho pequeno e verificável à mão; uma generalização para grau `k`
  arbitrário fica para a integração serial futura.
- `SimEquivalent f g`: forma abstrata de "`f` e `g` são polinomialmente
  comparáveis nas duas direções" — a forma lógica de uma hipótese de
  simulação como a de Maass–Orponen 1998 ou da tese de Church–Turing
  estendida, mas como **definição parametrizada**, não como afirmação sobre
  um modelo físico concreto.
- Dois lemas provados sem `sorry`/`admit`/axioma: `simEquivalent_refl` e
  `simEquivalent_symm` — reflexividade e simetria de `SimEquivalent`. São
  triviais por construção; documentam que a relação tem a forma certa para
  ser usada como hipótese em um teorema condicional futuro.

Um terceiro resultado — "se `physTime` é `SimEquivalent` a um
`turingTime` que é `AffineBounded`, então `physTime` também é
`AffineBounded`" — foi **redigido em prosa** (ver 2.2 abaixo) mas **não
formalizado em Lean nesta sessão**: a prova exigiria lemas de monotonicidade
de multiplicação do Mathlib (`Nat.mul_le_mul` ou `mul_le_mul_left'`) cujo
nome/assinatura exatos não puderam ser confirmados sem rodar `lake build` —
proibido nesta etapa paralela (ver instruções da tarefa). Formalizá-lo
sem essa confirmação arriscaria um erro de compilação silencioso ou, pior,
a tentação de tampar com `sorry`, que é proibido por `AGENTS.md`. Registrado
aqui como item aberto para a integração serial, não como resultado.

### 2.2 Teorema condicional (prosa, não formalizado em Lean)

```text
Proposição (não formalizada em Lean nesta sessão).
Se cost_{M,R} de um par (E,M,R) é polinomialmente equivalente (nos dois
sentidos, Definicao SimEquivalent) ao custo de uma maquina de Turing de
referencia, e o custo da maquina de Turing e polinomial, entao
cost_{M,R} tambem e polinomial -- i.e. P_phys(E,M,R) = P para aquele par.
```

Isto é a forma abstrata do que Maass–Orponen 1998 mostra concretamente para
um modelo de ruído analógico específico (colapso a autômatos finitos, um
limite ainda mais forte que "polinomial") e do que a tese de Church–Turing
física de Deutsch 1985 afirma informalmente em geral. **Nenhuma das duas
fontes, nem esta proposição, estabelece o inverso** — isto é, nenhuma
mostra que exista um `(E,M,R)` capaz de simular eficientemente um problema
NP-difícil sem essa equivalência já estar presuposta.

## 3. Condição de parada — ATINGIDA

Por instrução da tarefa: *"pare e reporte, não force"* ao encontrar
`ponte para maquina de Turing superpolinomial, ou indefinicao de
codificacao`. **Ambas as condições foram encontradas nesta sessão**:

```text
(i)  indefinicao de codificacao (PNP-GAP-002):
     DEFINITIONS.md Secao 4 mostra 4 triplas (E,M,R) da literatura que NAO
     sao equivalentes entre si sem hipotese extra -- a relacao entre o
     modelo BSS sobre C e classes classicas (item 3 da matriz) so vale
     SOB GRH (Burgisser-Cucker 2006). Nao ha uma codificacao/modelo
     canonico de "complexidade fisica" na literatura pesquisada.

(ii) ausencia de ponte universal para separacao superpolinomial de Turing
     (PNP-GAP-001):
     nenhuma fonte encontrada (itens 1-8 de KNOWN_RESULTS_MATRIX.md)
     estabelece uma ponte de simulacao (DEFINITIONS.md Sec. 3) que
     transporte uma separacao P_phys != NP_phys para uma separacao
     P != NP classica -- os resultados existentes ou (a) colapsam o
     modelo fisico DE VOLTA a poder classico sob ruido/precisao finita
     (Maass-Orponen), o que faz P_phys = P e nada mais, ou (b) exigem
     hipoteses matematicas independentes nao relacionadas ao problema
     (GRH, Burgisser-Cucker), ou (c) resolvem um problema fisico distinto
     (energia livre do modelo SK, Talagrand) sem estabelecer a reducao de
     complexidade computacional que o documento legado presumia.
```

**Esta auditoria para aqui**, conforme instruído. Não é tentada nenhuma
construção de ponte nova, nenhuma escolha de `(E,M,R)` "canônica", e nenhuma
extensão do teorema condicional da Seção 2.2 além do que já está nas fontes
citadas. `GAP_REGISTER.yaml` mantém `PNP-GAP-001` e `PNP-GAP-002` como
`OPEN`.

## 4. Sobre a formalização Lean

`lean_sketch_written = true`, `lean_sketch_path =
04_FORMAL_RESEARCH_LAB/03_MILLENNIUM/03_P_VS_NP/FORMAL/PvsNPPhys.lean`.
Arquivo autocontido, **não** registrado em `TamesisLab.lean`, **não**
compilado nesta sessão (regra da onda paralela: nenhuma frente roda
`lake build`). A integração e o build real ficam para a etapa serial
posterior, fora desta auditoria.
