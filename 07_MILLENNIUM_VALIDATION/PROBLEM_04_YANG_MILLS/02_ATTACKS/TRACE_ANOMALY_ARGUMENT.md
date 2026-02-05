# ⚛️ ANOMALIA DE TRAÇO E INSTABILIDADE DO VÁCUO

**Data:** 3 de fevereiro de 2026  
**Status:** 🟠 ARGUMENTO EM CONSTRUÇÃO  
**Dependência:** WILSON_ITO_DEVELOPMENT.md

---

## 1. O TEOREMA DA ANOMALIA DE TRAÇO

### 1.1 Statement Clássico

Para Yang-Mills puro em $d=4$ dimensões, o tensor energia-momento é classicamente sem traço:

$$T^\mu_{\ \mu}|_{\text{clássico}} = 0$$

Isso reflete a invariância conforme clássica da teoria.

### 1.2 Statement Quântico

Após quantização, a anomalia de traço emerge:

$$\boxed{T^\mu_{\ \mu} = \frac{\beta(g)}{2g^3} F^{\mu\nu}F_{\mu\nu}}$$

onde a função $\beta$ para $SU(N)$ é:

$$\beta(g) = -\frac{11 N}{48\pi^2} g^3 + O(g^5)$$

**Referências:**
- Collins, Duncan, Joglekar (1977)
- Nielsen (1977)
- Adler, Collins, Duncan (1977)

---

## 2. INTERPRETAÇÃO FÍSICA

### 2.1 Quebra de Invariância de Escala

A anomalia significa que sob dilatação $x \to \lambda x$:

$$\frac{d}{d\log\lambda} \langle O \rangle \neq 0$$

para observáveis $O$ que seriam invariantes classicamente.

### 2.2 Geração Dinâmica de Escala

O fato de $\beta(g) < 0$ (liberdade assintótica) implica:

$$g^2(\mu) = \frac{g^2(\mu_0)}{1 + \frac{11N}{24\pi^2} g^2(\mu_0) \log(\mu/\mu_0)}$$

Logo existe escala intrínseca $\Lambda_{QCD}$ onde $g^2 \to \infty$:

$$\Lambda_{QCD} = \mu_0 \exp\left(-\frac{24\pi^2}{11 N g^2(\mu_0)}\right)$$

---

## 3. CONEXÃO COM WILSON-ITÔ

### 3.1 O Vácuo Gapless

Se a teoria fosse gapless, o vácuo teria:
- Invariância de escala exata
- $\langle F^2 \rangle = 0$ (sem condensado)
- Correlações power-law

### 3.2 O que a Anomalia Implica

A anomalia de traço força:

$$\langle T^\mu_{\ \mu} \rangle = \frac{\beta(g)}{2g^3} \langle F^2 \rangle$$

**Argumento:**

1. Se $\langle F^2 \rangle = 0$, então $\langle T^\mu_{\ \mu} \rangle = 0$
2. Mas a teoria tem running: $\beta(g) \neq 0$
3. O running implica que há contribuições de loop
4. Contribuições de loop geram $\langle F^2 \rangle \neq 0$
5. Logo o vácuo "verdadeiro" tem $\langle F^2 \rangle \neq 0$

### 3.3 Tradução para Wilson-Itô

Na linguagem de Wilson-Itô, a força efetiva tem forma:

$$f_a(\varphi) = -d^*_\varphi F(\varphi) + \text{(termos quânticos)}$$

Os "termos quânticos" incluem a correção de $\beta$-função:

$$f_a^{\text{quântico}} \sim \frac{\beta(g)}{g} \varphi$$

Este termo *empurra* o campo para longe de $\varphi = 0$.

---

## 4. O ARGUMENTO DE INSTABILIDADE

### 4.1 Linearização em torno do Vácuo

Considere perturbação $\varphi = 0 + \delta\varphi$ com $|\delta\varphi| \ll 1$.

A equação Wilson-Itô linearizada:

$$d(\delta\varphi_a) = \dot{C}_a \left( -\Delta(\delta\varphi_a) + m^2_{\text{eff}}(a) \delta\varphi_a \right) da + \dot{C}^{1/2}_a dW_a$$

onde a massa efetiva dependente de escala é:

$$m^2_{\text{eff}}(a) \sim \frac{\beta(g(a))}{g(a)} \sim -\frac{11N}{48\pi^2} g^2(a)$$

### 4.2 O Sinal Crucial

Para $\beta < 0$ (liberdade assintótica):

$$m^2_{\text{eff}} < 0 \quad \text{(em escalas IR)}$$

Isso é uma **instabilidade taquiônica!**

### 4.3 Conclusão

O vácuo $\varphi = 0$ é instável sob evolução de escala Wilson-Itô:

$$\frac{d}{da} \mathbb{E}[\|\delta\varphi_a\|^2] > 0$$

A perturbação *cresce* exponencialmente em escalas IR.

---

## 5. O QUE ESTABILIZA A TEORIA?

### 5.1 Formação de Condensado

A instabilidade do vácuo perturbativo leva à formação de condensado:

$$\langle F^{\mu\nu} F_{\mu\nu} \rangle \neq 0$$

Este é o **condensado de glúons**, com valor:

$$\langle \frac{\alpha_s}{\pi} G^a_{\mu\nu} G^{a\mu\nu} \rangle \approx (0.35 \pm 0.05) \text{ GeV}^4$$

(Valor fenomenológico de SVZ sum rules)

### 5.2 O Ponto Fixo Não-Trivial

A evolução Wilson-Itô converge para configuração não-trivial $\varphi^*$:

$$\lim_{a \to \infty} \varphi_a = \varphi^* \neq 0$$

com $\varphi^*$ satisfazendo:

$$f_\infty(\varphi^*) = 0$$

### 5.3 O Gap

A massa dos glúeballs emerge da curvatura do potencial efetivo em $\varphi^*$:

$$m^2_{\text{gap}} = \frac{\partial^2 V_{\text{eff}}}{\partial\varphi^2}\bigg|_{\varphi^*} > 0$$

---

## 6. ESTRUTURA DO TEOREMA

### 6.1 Afirmação Precisa

**Teorema (Conjecturado):** Seja $(A_a)_{a \geq 0}$ a difusão Wilson-Itô para Yang-Mills 4D com grupo $SU(N)$, $N \geq 2$. Então:

**(i)** O vácuo perturbativo $A = 0$ é ponto de sela instável do funcional de estabilidade $\mathcal{W}$.

**(ii)** Existe ponto fixo estável $A^*$ com $\langle F(A^*)^2 \rangle = c \cdot \Lambda^4_{QCD}$ para constante $c > 0$.

**(iii)** O espectro de flutuações em torno de $A^*$ tem gap: $\text{spec}(H) \subset \{0\} \cup [m, \infty)$ com $m > 0$.

### 6.2 Esboço da Prova

```
1. Definir Wilson-Itô para YM 4D (precisa extensão de CCHS)
   ↓
2. Mostrar bem-posedness do sistema FBSDE
   ↓
3. Computar massa efetiva m²_eff(a) via β-função
   ↓
4. Provar m²_eff < 0 em IR (liberdade assintótica)
   ↓
5. Concluir instabilidade de A = 0
   ↓
6. Usar monotonicidade de W para encontrar mínimo A*
   ↓
7. Caracterizar espectro de flutuações em A*
   ↓
8. Concluir gap de massa
```

---

## 7. GAPS NO ARGUMENTO

### 7.1 O que Falta Provar

| Item | Status | Dificuldade |
|------|--------|-------------|
| Wilson-Itô em 4D | ❌ | Alta |
| Well-posedness FBSDE | ❌ | Alta |
| Cálculo de $m^2_{\text{eff}}$ | 🟡 | Média |
| Instabilidade | 🟡 | Média (dado os anteriores) |
| Existência de $A^*$ | ❌ | Alta |
| Espectro de flutuações | ❌ | Alta |

### 7.2 Obstáculos Técnicos

1. **Regularidade:** Wilson-Itô produz campos distribucionais. A curvatura $F$ envolve derivadas.

2. **Gauge fixing:** Precisa gauge consistente com dinâmica Wilson-Itô.

3. **Renormalização:** Termos divergentes em 4D requerem tratamento cuidadoso.

4. **Não-perturbativo:** O argumento de condensado é inerentemente não-perturbativo.

---

## 8. CONEXÃO COM LATTICE QCD

### 8.1 Evidência Numérica

Simulações de lattice QCD confirmam:
- Confinamento de quarks
- Gap de massa $\sim 1$ GeV para glúeballs
- Condensado de glúons não-nulo

### 8.2 Limite do Contínuo

O desafio é conectar:

$$\text{Lattice (UV regularizado)} \xrightarrow{a \to 0} \text{Contínuo (Wilson-Itô)}$$

A dinâmica Wilson-Itô pode ser vista como versão do contínuo do "block spin RG" do lattice.

---

## 9. PRÓXIMOS PASSOS

### 9.1 Verificação Imediata

1. Calcular explicitamente $m^2_{\text{eff}}(a)$ para força YM
2. Verificar sinal negativo em IR
3. Estimar taxa de crescimento da instabilidade

### 9.2 Desenvolvimento Teórico

1. Estudar modelos simplificados (YM 2D, Abeliano)
2. Verificar se argumento funciona em casos conhecidos
3. Gradualmente aumentar complexidade

### 9.3 Validação

1. Comparar predições com lattice
2. Checar consistência com fenomenologia
3. Verificar limites assintóticos

---

**Última atualização:** 3 de fevereiro de 2026  
**Classificação:** 🟠 ARGUMENTO EM CONSTRUÇÃO — Gaps significativos permanecem

