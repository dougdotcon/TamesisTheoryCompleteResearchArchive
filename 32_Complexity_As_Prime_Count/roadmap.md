# Roadmap: Primos Computacionais no Espaco de Inputs (Caminho 2)

## Objetivo Final
Redefinir "primos computacionais" como ciclos no espaco de inputs e mostrar que sua contagem determina complexidade.

## Principio Fundamental
**Primos computacionais = ciclos irredutiveis na transformacao de inputs**

Nao sao ciclos no espaco de estados, mas ciclos na relacao entrada -> saida.

---

## FASE 1: Redefinicao de Primos (Stages 34-36)

### Stage 34: Definicao Formal de Primo Computacional
**Objetivo:** Definir matematicamente o que e um "primo" de um algoritmo

**Tarefas:**
1. Dado algoritmo A, definir grafo G_A no espaco de inputs
2. Aresta (x, y) existe se T_A(x) "gera" y em um passo
3. Definir ciclo: sequencia x_1 -> x_2 -> ... -> x_1
4. Definir ciclo primitivo: nao e potencia de ciclo menor

**Entregavel:** `prime_definition.py`

**Formalizacao:**
```
Primo de A = ciclo primitivo em G_A
pi_A(n) = numero de primos de comprimento <= n
```

**Criterio de sucesso:** Definicao precisa e implementavel

### Stage 35: Contagem de Primos para Algoritmos Classicos
**Objetivo:** Calcular pi_A(n) para quicksort, mergesort, Euclides

**Tarefas:**
1. Implementar busca de ciclos em G_quicksort
2. Implementar busca de ciclos em G_mergesort
3. Implementar busca de ciclos em G_euclides (mapa de Gauss)
4. Tabular pi_A(n) para n = 1, 2, ..., 20

**Entregavel:** `prime_counting.py`

**Criterio de sucesso:** Tabelas de pi_A(n) para 3+ algoritmos

### Stage 36: Lei de Crescimento de pi_A(n)
**Objetivo:** Determinar como pi_A(n) cresce com n

**Tarefas:**
1. Ajustar pi_A(n) ~ n^alpha para cada algoritmo
2. Ajustar pi_A(n) ~ n / log(n) (analogo PNT)
3. Comparar expoentes entre algoritmos
4. Formular hipotese: alpha determina complexidade

**Entregavel:** `prime_growth.py`

**Criterio de sucesso:** Expoentes calculados, hipotese formulada

---

## FASE 2: Conexao Primos-Complexidade (Stages 37-39)

### Stage 37: Conjectura Principal
**Objetivo:** Formular e testar: "pi_A(n) ~ f(n) => complexidade O(g(n))"

**Tarefas:**
1. Para algoritmos O(n): medir pi_A(n)
2. Para algoritmos O(n log n): medir pi_A(n)
3. Para algoritmos O(n^2): medir pi_A(n)
4. Identificar relacao f -> g

**Entregavel:** `prime_complexity_conjecture.py`

**Hipotese a testar:**
```
pi_A(n) ~ n^alpha  =>  complexidade ~ O(n^{1/alpha}) ?
```

**Criterio de sucesso:** Correlacao observada ou refutada

### Stage 38: Formula Explicita Computacional
**Objetivo:** Derivar formula tipo Weil para algoritmos

**Tarefas:**
1. Definir "zeros" = autovalores do operador L_A
2. Definir "primos" = ciclos primitivos
3. Escrever: sum_zeros f(gamma) = sum_primos g(p)
4. Verificar numericamente

**Entregavel:** `computational_explicit_formula.py`

**Formula alvo:**
```
sum_gamma h(gamma) = sum_p log(l_p) * h_hat(l_p) + termos suaves
```

**Criterio de sucesso:** Formula verificada para 1+ algoritmo

### Stage 39: Densidade de Primos e Complexidade Media
**Objetivo:** Relacionar densidade de primos com tempo medio

**Tarefas:**
1. Definir densidade: d_A(n) = pi_A(n) / n
2. Calcular para varios algoritmos
3. Comparar com complexidade media empirica
4. Derivar relacao teorica (se possivel)

**Entregavel:** `prime_density_complexity.py`

**Criterio de sucesso:** Relacao quantitativa estabelecida

---

## FASE 3: Teoria dos Numeros Computacional (Stages 40-42)

### Stage 40: Teorema dos Numeros Primos Computacional
**Objetivo:** Provar (ou conjecturar) pi_A(n) ~ n / log(n) para alguma classe

**Tarefas:**
1. Identificar algoritmos onde pi_A(n) ~ n / log(n)
2. Caracterizar essa classe
3. Formular teorema analogo ao PNT
4. Esbocar prova ou evidencia numerica

**Entregavel:** `computational_pnt.py`

**Teorema alvo:**
```
Para algoritmos "genericos": pi_A(n) ~ n / log(n)
```

**Criterio de sucesso:** Teorema enunciado com evidencia

### Stage 41: Hipotese de Riemann Computacional
**Objetivo:** Formular analogo de RH para algoritmos

**Tarefas:**
1. Definir zeta_A(s) = prod_p (1 - p^{-s})^{-1}
2. Identificar zeros de zeta_A
3. Verificar se zeros tem parte real especial
4. Formular "RH computacional"

**Entregavel:** `computational_rh.py`

**Hipotese alvo:**
```
Todos os zeros nao-triviais de zeta_A tem Re(s) = 1/2 ?
```

**Criterio de sucesso:** Hipotese formulada, testada numericamente

### Stage 42: Funcoes L Computacionais
**Objetivo:** Generalizar para "caracteres" de algoritmos

**Tarefas:**
1. Definir caracteres chi: G_A -> C
2. Definir L_A(s, chi) = prod_p (1 - chi(p) p^{-s})^{-1}
3. Estudar propriedades
4. Conectar com invariantes do algoritmo

**Entregavel:** `computational_l_functions.py`

**Criterio de sucesso:** L-functions definidas e calculadas

---

## FASE 4: Aplicacoes (Stages 43-45)

### Stage 43: Otimizacao via Primos
**Objetivo:** Usar contagem de primos para otimizar algoritmos

**Tarefas:**
1. Identificar: menos primos = mais eficiente ?
2. Testar variantes de quicksort
3. Medir correlacao primos <-> tempo
4. Propor criterio de otimizacao

**Entregavel:** `prime_optimization.py`

**Criterio de sucesso:** Criterio util identificado

### Stage 44: Classificacao de Algoritmos
**Objetivo:** Classificar algoritmos pela estrutura de primos

**Tarefas:**
1. Calcular "assinatura de primos" para cada algoritmo
2. Definir distancia entre assinaturas
3. Clusterizar algoritmos
4. Ver se clusters correspondem a complexidade

**Entregavel:** `algorithm_classification.py`

**Criterio de sucesso:** Classificacao coerente

### Stage 45: Paper e Formalizacao
**Objetivo:** Publicar teoria

**Tarefas:**
1. Escrever paper: "Prime Numbers of Algorithms"
2. Definicoes rigorosas
3. Teoremas principais
4. Conjecturas abertas

**Entregavel:** `paper_draft.tex`

**Criterio de sucesso:** Paper submetido

---

## Metricas de Progresso

| Fase | Stages | Tempo Estimado | Criterio |
|------|--------|----------------|----------|
| 1    | 34-36  | 2-3 semanas    | pi_A(n) calculado |
| 2    | 37-39  | 3-4 semanas    | Conexao estabelecida |
| 3    | 40-42  | 4-6 semanas    | Teoria formulada |
| 4    | 43-45  | 4-6 semanas    | Paper pronto |

## Riscos

1. **Definicao de "primo" pode ser arbitraria**
   - Mitigacao: testar varias definicoes

2. **Correlacao primos-complexidade pode ser fraca**
   - Mitigacao: pivotar para outro invariante

3. **Calculos explodem para n grande**
   - Mitigacao: usar amostragem, heuristicas

## Resultado Esperado

- Nova "teoria dos numeros" para algoritmos
- Invariantes novos para classificar algoritmos
- Paper publicavel: "Computational Prime Number Theory"
