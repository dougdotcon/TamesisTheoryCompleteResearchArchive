# ATTACK: Transferência de Energia por Escala — Análise Littlewood-Paley

**Data:** 2025-01-29
**Status:** 🔵 DESENVOLVIMENTO TÉCNICO
**Objetivo:** Quantificar taxa de transferência não-linear

---

## 1. SETUP: DECOMPOSIÇÃO LITTLEWOOD-PALEY

### 1.1 Definição

Seja $\{\Delta_j\}_{j \in \mathbb{Z}}$ a decomposição de Littlewood-Paley:

$$u = \sum_{j=-\infty}^{\infty} \Delta_j u$$

onde $\widehat{\Delta_j u}(\xi) = \phi(2^{-j}|\xi|) \hat{u}(\xi)$ com $\phi$ suportado em anel.

### 1.2 Propriedades

- $\text{supp}(\widehat{\Delta_j u}) \subset \{2^{j-1} \leq |\xi| \leq 2^{j+1}\}$
- $\sum_j \Delta_j = I$ (identidade)
- **Bernstein:** $\|\nabla \Delta_j u\|_{L^p} \sim 2^j \|\Delta_j u\|_{L^p}$

### 1.3 Energia por Escala

$$E_j(t) = \frac{1}{2}\|\Delta_j u(t)\|_{L^2}^2$$

$$E(t) = \sum_j E_j(t)$$

---

## 2. EQUAÇÃO POR ESCALA

### 2.1 Projeção da Equação NS

Aplicando $\Delta_j$ a NS:

$$\partial_t \Delta_j u + \Delta_j[(u \cdot \nabla)u] = -\nabla \Delta_j p + \nu \Delta \Delta_j u$$

### 2.2 Evolução de $E_j$

Multiplicando por $\Delta_j u$ e integrando:

$$\frac{dE_j}{dt} = -\int \Delta_j u \cdot \Delta_j[(u \cdot \nabla)u] dx - \nu \|\nabla \Delta_j u\|_{L^2}^2$$

### 2.3 Decomposição do Termo Não-Linear

$$\Delta_j[(u \cdot \nabla)u] = \sum_{k,\ell} \Delta_j[(\Delta_k u \cdot \nabla)\Delta_\ell u]$$

Os termos significativos satisfazem $|k - \ell| \lesssim 1$ ou $|j - \max(k,\ell)| \lesssim 1$.

---

## 3. FLUXO DE ENERGIA

### 3.1 Definição do Fluxo

O fluxo de energia através da escala $j$ é:

$$\Pi_j = -\sum_{k \leq j} \int \Delta_k u \cdot \Delta_k[(u \cdot \nabla)u] dx$$

### 3.2 Propriedade de Conservação

$$\sum_j \frac{dE_j}{dt} = \frac{dE}{dt} = -\epsilon$$

O fluxo total é zero (energia apenas redistribuída), mas há fluxo líquido para escalas menores.

### 3.3 K41 em Termos de Fluxo

K41 afirma que na faixa inercial:

$$\Pi_j \approx \epsilon_0 = \text{const}$$

independente de $j$.

---

## 4. ESTIMATIVA DO FLUXO

### 4.1 Decomposição Paraproduct

$$(\Delta_k u \cdot \nabla)\Delta_\ell u = T_{u} \nabla \Delta_\ell u + T_{\nabla \Delta_\ell u} u + R(u, \nabla \Delta_\ell u)$$

onde:
- $T$ é o operador paraproduct
- $R$ é o termo de resto (interação de frequências comparáveis)

### 4.2 Estimativa do Paraproduct

$$\|T_u \nabla v\|_{L^2} \lesssim \|u\|_{L^\infty} \|\nabla v\|_{L^2}$$

**Problema:** Requer $\|u\|_{L^\infty}$, que pode ser infinito no blow-up.

### 4.3 Estimativa do Resto

$$\|R(u, \nabla v)\|_{L^2} \lesssim \|\nabla u\|_{L^2} \|v\|_{L^\infty}$$

Também requer controle de $L^\infty$.

---

## 5. ABORDAGEM ALTERNATIVA: ESTIMATIVAS DE BESOV

### 5.1 Espaços de Besov

$$\|u\|_{\dot{B}^s_{p,q}} = \left(\sum_j 2^{jsq} \|\Delta_j u\|_{L^p}^q\right)^{1/q}$$

### 5.2 Embedding Crítico

NS é crítico em $\dot{B}^{-1}_{\infty,\infty}$ e $\dot{H}^{1/2}$.

**Resultado (Koch-Tataru):** Se $\|u_0\|_{\dot{B}^{-1}_{\infty,\infty}}$ é pequeno, solução global existe.

### 5.3 Limitação

Dados grandes não satisfazem a condição de pequenez.

---

## 6. BOUND NA TRANSFERÊNCIA: TENTATIVA RIGOROSA

### 6.1 Setup

Defina a taxa de transferência para escala $j$:

$$T_j = \int \Delta_j u \cdot \Delta_j[(u \cdot \nabla)u] dx$$

### 6.2 Estimativa via Hölder

$$|T_j| \leq \|\Delta_j u\|_{L^2} \|\Delta_j[(u \cdot \nabla)u]\|_{L^2}$$

### 6.3 Estimativa do Termo Projetado

Usando que a projeção é limitada:

$$\|\Delta_j[(u \cdot \nabla)u]\|_{L^2} \lesssim \sum_{|k-j| \leq 2} \|(\Delta_k u \cdot \nabla)u\|_{L^2}$$

Usando Hölder:

$$\|(\Delta_k u \cdot \nabla)u\|_{L^2} \leq \|\Delta_k u\|_{L^6} \|\nabla u\|_{L^3}$$

### 6.4 Aplicando Sobolev

$$\|\Delta_k u\|_{L^6} \lesssim \|\nabla \Delta_k u\|_{L^2} \lesssim 2^k \|\Delta_k u\|_{L^2} = 2^k \sqrt{2E_k}$$

E interpolando:

$$\|\nabla u\|_{L^3} \lesssim \|\nabla u\|_{L^2}^{1/2} \|\Delta u\|_{L^2}^{1/2}$$

### 6.5 Resultado

$$|T_j| \lesssim 2^j \sqrt{E_j} \cdot \sqrt{\epsilon/\nu} \cdot \|\Delta u\|_{L^2}^{1/2}$$

**Problema:** Ainda depende de $\|\Delta u\|_{L^2}$ (enstrofia).

---

## 7. ANÁLISE DIMENSIONAL

### 7.1 Scaling de NS

Sob $u \mapsto \lambda u$, $x \mapsto x/\lambda$, $t \mapsto t/\lambda^2$:

- $E \mapsto \lambda^2 E$
- $\epsilon \mapsto \lambda^4 \epsilon$
- $\Omega \mapsto \lambda^4 \Omega$

### 7.2 Consequência

Não há combinação adimensional de $E$ e $\epsilon$ que dê bound em $\Omega$.

**Este é o problema de scaling crítico.**

### 7.3 A Única Esperança

Usar a **estrutura específica** de NS que não é capturada por scaling.

Candidatos:
- Incompressibilidade $\nabla \cdot u = 0$
- Geometria do termo $\omega \cdot S \cdot \omega$
- Cancelamentos do paraproduct

---

## 8. INSIGHT TAMESIS APLICADO

### 8.1 Reinterpretação do Limite

O Tamesis diz que existe "bit-rate limit" — máximo de processamento.

**Em termos de Littlewood-Paley:**

$$\sum_j |T_j| \leq T_{max}$$

A soma das taxas de transferência é bounded.

### 8.2 Por Que Seria Verdade?

**Argumento Heurístico:**

Cada $T_j$ envolve interação de três campos:
$$T_j \sim \int \Delta_j u \cdot \Delta_k u \cdot \nabla \Delta_\ell u$$

A integral é bounded por:
$$|T_j| \lesssim \|\Delta_j u\|_{L^2} \|\Delta_k u\|_{L^4} \|\nabla \Delta_\ell u\|_{L^4}$$

Somando sobre $j, k, \ell$:
$$\sum_{j,k,\ell} |T_{jk\ell}| \lesssim \|u\|_{L^2} \|u\|_{L^4}^2 \|\nabla u\|_{L^4}^2$$

**Problema:** $\|u\|_{L^4}$ e $\|\nabla u\|_{L^4}$ não são controlados por energia.

---

## 9. DIREÇÃO: MÉDIA TEMPORAL

### 9.1 Observação

Mesmo que $T_j(t)$ seja grande instantaneamente, a média temporal pode ser bounded:

$$\langle T_j \rangle = \frac{1}{t} \int_0^t T_j(s) ds \leq ?$$

### 9.2 Argumento de Energia

A energia total dissipada é:
$$\int_0^\infty \epsilon(t) dt \leq E_0$$

Se a transferência está correlacionada com dissipação:
$$\int_0^\infty |T_j(t)| dt \lesssim f(E_0, \nu)$$

### 9.3 Problema

A correlação entre $T_j$ e $\epsilon$ não é clara.

Poderia haver transferência rápida seguida de dissipação rápida, com pico de vorticidade no meio.

---

## 10. CONCLUSÃO PARCIAL

### 10.1 O Que Conseguimos

1. Formulação precisa do fluxo de energia por escala
2. Identificação das estimativas necessárias
3. Localização do gap: controle de $\|\Delta u\|_{L^2}$ ou $\|u\|_{L^\infty}$

### 10.2 O Que Falta

1. Bound na taxa de transferência sem usar $\Omega$
2. Explorar cancelamentos específicos do paraproduct
3. Média temporal do fluxo

### 10.3 Próximo Passo

Investigar se a **incompressibilidade** fornece cancelamentos adicionais no fluxo.

$$\nabla \cdot u = 0 \Rightarrow ?$$

---

## 11. HIPÓTESE DE TRABALHO

### 11.1 Conjectura (Weak)

Para soluções de Leray:

$$\limsup_{t \to \infty} \frac{1}{t} \int_0^t \sum_j |T_j(s)| ds < \infty$$

### 11.2 Conjectura (Strong)

Para soluções clássicas:

$$\sup_{t} \sum_j |T_j(t)| < \infty$$

### 11.3 Implicação

Se qualquer conjectura for verdadeira, combinada com dissipação, implica regularidade.

**Status:** 🟠 CONJECTURAS ABERTAS — PRECISAM PROVA
