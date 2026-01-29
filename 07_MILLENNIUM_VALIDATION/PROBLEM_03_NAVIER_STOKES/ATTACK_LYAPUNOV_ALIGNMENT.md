# ATTACK: Análise de Lyapunov para o Gap de Alinhamento

**Data:** 2025-01-29
**Status:** 🔴 ATAQUE CRÍTICO — TENTATIVA DE FECHAMENTO
**Objetivo:** Provar rigorosamente que $\int\int |\omega|^2[\lambda_1 - \hat{\omega}^T S \hat{\omega}] \geq \delta > 0$

---

## 1. FORMULAÇÃO PRECISA

### 1.1 Definições

Seja $u: \mathbb{R}^3 \times [0,T] \to \mathbb{R}^3$ solução suave de NS.

**Tensor de strain:**
$$S_{ij} = \frac{1}{2}(\partial_i u_j + \partial_j u_i)$$

**Autovalores:** $\lambda_1(x,t) \geq \lambda_2(x,t) \geq \lambda_3(x,t)$ com $\sum_i \lambda_i = 0$.

**Autovetores ortonormais:** $\{e_1(x,t), e_2(x,t), e_3(x,t)\}$.

**Vorticidade:** $\omega = \nabla \times u$, direção $\hat{\omega} = \omega/|\omega|$.

**Coseno quadrado:**
$$\alpha_i = \cos^2(\omega, e_i) = (\hat{\omega} \cdot e_i)^2, \quad i = 1,2,3$$

Note: $\alpha_1 + \alpha_2 + \alpha_3 = 1$.

### 1.2 Stretching Efetivo

$$\sigma := \hat{\omega}^T S \hat{\omega} = \sum_{i=1}^3 \alpha_i \lambda_i$$

O stretching máximo seria $\lambda_1$ (quando $\alpha_1 = 1$).

### 1.3 Gap de Alinhamento

Definimos:
$$\mathcal{G}(x,t) := \lambda_1 - \sigma = \lambda_1 - \sum_i \alpha_i \lambda_i = \sum_{i=2}^3 \alpha_i (\lambda_1 - \lambda_i)$$

Note que $\mathcal{G} \geq 0$ sempre, com igualdade sse $\alpha_1 = 1$.

### 1.4 Objetivo

Provar que existe $\delta > 0$ tal que:
$$\int_0^T \int_{\mathbb{R}^3} |\omega|^2 \mathcal{G}(x,t) \, dx \, dt \geq \delta \int_0^T \Omega(t) \, dt$$

onde $\Omega(t) = \frac{1}{2}\|\omega\|_{L^2}^2$ é a enstrofia.

---

## 2. EQUAÇÕES DE EVOLUÇÃO

### 2.1 Sistema Acoplado

O sistema $(|\omega|, \hat{\omega}, S)$ satisfaz:

**Magnitude:**
$$\frac{D|\omega|}{Dt} = \sigma |\omega| - \nu \frac{|\nabla\omega|^2 - |\omega|\Delta|\omega|}{|\omega|}$$

**Direção:**
$$\frac{D\hat{\omega}}{Dt} = P_\perp S \hat{\omega} + \nu \cdot (\text{termos difusivos})$$

onde $P_\perp = I - \hat{\omega}\hat{\omega}^T$ é a projeção perpendicular.

**Tensor S:**
$$\frac{DS_{ij}}{Dt} = -S_{ik}S_{kj} - \frac{1}{4}(\omega_i\omega_j - |\omega|^2\delta_{ij}/3) - \partial_i\partial_j p + \nu\Delta S_{ij}$$

### 2.2 Evolução do Coseno

Para $\alpha_1 = (\hat{\omega} \cdot e_1)^2$:

$$\frac{D\alpha_1}{Dt} = 2(\hat{\omega} \cdot e_1)\left(\frac{D\hat{\omega}}{Dt} \cdot e_1 + \hat{\omega} \cdot \frac{De_1}{Dt}\right)$$

### 2.3 Evolução dos Autovetores

Se $\lambda_1$ é simples (não degenerado):
$$\frac{De_1}{Dt} = \sum_{j \neq 1} \frac{e_j^T \dot{S} e_1}{\lambda_1 - \lambda_j} e_j + \Omega \cdot e_1$$

onde $\dot{S} = DS/Dt$ e $\Omega$ é o tensor antissimétrico do gradiente de velocidade.

---

## 3. FUNCIONAL DE LYAPUNOV

### 3.1 Candidato Natural

Considere o funcional:
$$\mathcal{L}(t) = \int_{\mathbb{R}^3} |\omega|^2 \alpha_1 \, dx$$

que mede a "quantidade de alinhamento pesada pela enstrofia".

### 3.2 Evolução de $\mathcal{L}$

$$\frac{d\mathcal{L}}{dt} = \int \frac{D}{Dt}(|\omega|^2 \alpha_1) \, dx = \int \left[2|\omega|\frac{D|\omega|}{Dt}\alpha_1 + |\omega|^2 \frac{D\alpha_1}{Dt}\right] dx$$

### 3.3 Contribuição do Crescimento de $|\omega|$

$$2|\omega|\frac{D|\omega|}{Dt}\alpha_1 = 2\sigma |\omega|^2 \alpha_1 - \nu \cdot (\text{difusão})$$

### 3.4 Contribuição da Rotação de $\hat{\omega}$

A evolução de $\alpha_1$ vem de:
1. $P_\perp S \hat{\omega}$ tende a **aumentar** $\alpha_1$ se $\lambda_1 > \sigma$
2. Rotação de $e_1$ pode aumentar ou diminuir $\alpha_1$
3. Difusão tende a **isotrpizar** → diminui $\alpha_1$

---

## 4. ANÁLISE DO TERMO DE STRAIN

### 4.1 Efeito de $P_\perp S \hat{\omega}$ em $\alpha_1$

$$\frac{d\alpha_1}{dt}\bigg|_{\text{strain}} = 2(\hat{\omega} \cdot e_1)(P_\perp S \hat{\omega} \cdot e_1)$$

Calculando $P_\perp S \hat{\omega}$:
$$P_\perp S \hat{\omega} = S\hat{\omega} - (\hat{\omega}^T S \hat{\omega})\hat{\omega} = S\hat{\omega} - \sigma\hat{\omega}$$

Projetando em $e_1$:
$$(S\hat{\omega} - \sigma\hat{\omega}) \cdot e_1 = \lambda_1(\hat{\omega}\cdot e_1) - \sigma(\hat{\omega}\cdot e_1) = (\lambda_1 - \sigma)(\hat{\omega}\cdot e_1)$$

### 4.2 Resultado Chave

$$\frac{d\alpha_1}{dt}\bigg|_{\text{strain}} = 2(\hat{\omega}\cdot e_1)^2(\lambda_1 - \sigma) = 2\alpha_1(\lambda_1 - \sigma) = 2\alpha_1 \mathcal{G}$$

**O termo de strain AUMENTA $\alpha_1$ quando $\mathcal{G} > 0$!**

### 4.3 Interpretação

Isso parece contradizer nossa tese. O strain naturalmente empurra $\omega$ para $e_1$.

MAS: outros efeitos competem...

---

## 5. O EFEITO DA ROTAÇÃO DE $e_1$

### 5.1 Contribuição da Evolução de $e_1$

$$\frac{d\alpha_1}{dt}\bigg|_{e_1} = 2(\hat{\omega}\cdot e_1)\left(\hat{\omega} \cdot \frac{De_1}{Dt}\right)$$

### 5.2 Usando a Fórmula de Evolução

$$\hat{\omega} \cdot \frac{De_1}{Dt} = \sum_{j=2,3} \frac{e_j^T \dot{S} e_1}{\lambda_1 - \lambda_j}(\hat{\omega} \cdot e_j)$$

### 5.3 Análise de Sinais

O termo $e_j^T \dot{S} e_1$ depende de:
- $-S^2$ (contribuição quadrática)
- $-\omega\otimes\omega/4$ (contribuição da vorticidade)
- Pressão e difusão

**A contribuição $-\omega\otimes\omega$ é crucial!**

### 5.4 Efeito da Vorticidade em $\dot{S}$

$$e_j^T(-\omega\otimes\omega/4)e_1 = -\frac{1}{4}(\omega\cdot e_j)(\omega\cdot e_1) = -\frac{|\omega|^2}{4}\sqrt{\alpha_j\alpha_1}$$

Para $j = 2,3$, isso é **negativo** quando há alinhamento parcial.

### 5.5 Contribuição Total

$$\hat{\omega} \cdot \frac{De_1}{Dt}\bigg|_{\omega\otimes\omega} = -\frac{|\omega|^2}{4}\sum_{j=2,3}\frac{\alpha_j^{1/2}\alpha_1^{1/2}}{\lambda_1 - \lambda_j} \cdot \alpha_j^{1/2}$$

$$= -\frac{|\omega|^2}{4}\sum_{j=2,3}\frac{\alpha_j \alpha_1^{1/2}}{\lambda_1 - \lambda_j}$$

---

## 6. BALANÇO COMPLETO

### 6.1 Equação de Evolução para $\alpha_1$

Combinando:
$$\frac{D\alpha_1}{Dt} = 2\alpha_1\mathcal{G} - \frac{|\omega|^2}{2}\sum_{j=2,3}\frac{\alpha_1\alpha_j}{\lambda_1-\lambda_j} + \text{rotação de corpo rígido} + \nu(\text{difusão})$$

### 6.2 O Termo de Retroalimentação

O termo $-|\omega|^2\alpha_1\alpha_j/(\lambda_1-\lambda_j)$ é **negativo** (pois $\lambda_1 > \lambda_j$).

**Este termo DIMINUI $\alpha_1$ proporcionalmente a $|\omega|^2$!**

### 6.3 Interpretação Física

Quando $|\omega|$ é grande:
- A vorticidade deforma o tensor $S$
- Essa deformação **gira os autovetores de $S$**
- Especificamente, $e_1$ gira **para longe de $\omega$**

É uma **auto-regulação**: vorticidade intensa cria um campo de strain que evita alinhamento.

---

## 7. ESTIMATIVA QUANTITATIVA

### 7.1 Simplificação

Ignorando viscosidade temporariamente e assumindo $\lambda_1 - \lambda_2 \sim \lambda_1$:

$$\frac{D\alpha_1}{Dt} \lesssim 2\alpha_1\mathcal{G} - C\frac{|\omega|^2\alpha_1(1-\alpha_1)}{\lambda_1}$$

### 7.2 Ponto de Equilíbrio

No equilíbrio:
$$2\alpha_1\mathcal{G} \approx C\frac{|\omega|^2\alpha_1(1-\alpha_1)}{\lambda_1}$$

Usando $\mathcal{G} = (1-\alpha_1)(\lambda_1 - \bar{\lambda})$ onde $\bar{\lambda}$ é média dos outros:
$$2(1-\alpha_1)(\lambda_1 - \bar{\lambda}) \approx C\frac{|\omega|^2(1-\alpha_1)}{\lambda_1}$$

$$\lambda_1 - \bar{\lambda} \approx C\frac{|\omega|^2}{2\lambda_1}$$

### 7.3 Relação com Intensidade

Se $\lambda_1 \sim |\omega|/2$ (regime típico):
$$|\omega|/2 - \bar{\lambda} \approx C\frac{|\omega|^2}{|\omega|} = C|\omega|$$

Isso sugere $\alpha_1 < 1$ por uma quantidade **não infinitesimal**.

---

## 8. O PAPEL CRUCIAL DA DIFUSÃO

### 8.1 Termo Difusivo em $\alpha_1$

$$\frac{D\alpha_1}{Dt}\bigg|_{\text{diff}} = \nu \cdot (\text{derivadas de } \hat{\omega} \text{ e } e_1)$$

### 8.2 Efeito Qualitativo

A difusão **isotropiza** o campo de vorticidade.

Isotropização significa: $\alpha_1 \to 1/3$, $\alpha_2 \to 1/3$, $\alpha_3 \to 1/3$.

**A difusão impede alinhamento perfeito!**

### 8.3 Estimativa Heurística

Em regiões de alta vorticidade com escala $\ell$:
$$\nu \Delta \alpha_1 \sim \nu \frac{\alpha_1 - 1/3}{\ell^2}$$

Na escala de Kolmogorov $\ell \sim \eta$:
$$\nu/\eta^2 \sim \epsilon^{1/2}/\nu^{1/2} \sim \lambda_1$$

**A difusão compete com o alinhamento na escala de Kolmogorov!**

---

## 9. TEOREMA PRINCIPAL (CONJECTURAL)

### 9.1 Enunciado

**Teorema (Gap de Alinhamento):** Seja $u$ solução suave de NS com energia inicial $E_0$ e viscosidade $\nu > 0$. Então existe $\delta = \delta(E_0, \nu) > 0$ tal que:

$$\fint_0^T \left\langle \mathcal{G} \right\rangle_\Omega(t) \, dt \geq \delta$$

onde $\langle \cdot \rangle_\Omega$ é a média pesada por $|\omega|^2$.

### 9.2 Sketch de Prova

1. **Setup:** Defina $\mathcal{A}(t) = \langle \alpha_1 \rangle_\Omega(t)$ (alinhamento médio).

2. **Evolução:** 
   $$\frac{d\mathcal{A}}{dt} \lesssim C_1 \mathcal{A}\langle\mathcal{G}\rangle_\Omega - C_2 \langle|\omega|^2\rangle_\Omega \mathcal{A}(1-\mathcal{A}) + \nu(\text{dissipativo})$$

3. **Bound superior:** O termo $-C_2\langle|\omega|^2\rangle_\Omega$ limita $\mathcal{A}$ quando vorticidade é alta.

4. **Bound inferior em $\mathcal{G}$:** Se $\mathcal{A} \leq 1 - \delta_0$, então $\langle\mathcal{G}\rangle \geq \delta_0 \langle\lambda_1 - \lambda_2\rangle > 0$.

5. **Fechamento:** A combinação implica $\langle\mathcal{G}\rangle_\Omega$ é bounded away de zero em média.

### 9.3 Dificuldade Técnica

O passo 4 requer controle sobre $\langle\lambda_1 - \lambda_2\rangle$, que depende da estrutura local do strain.

---

## 10. CONEXÃO COM BKM

### 10.1 Da Gap de Alinhamento para Enstrofia

Se $\mathcal{G} \geq \delta$ em média, então o stretching efetivo é:
$$\sigma = \lambda_1 - \mathcal{G} \leq \lambda_1 - \delta$$

### 10.2 Equação de Enstrofia Refinada

$$\frac{d\Omega}{dt} = \int |\omega|^2 \sigma \, dx - \nu\|\nabla\omega\|_{L^2}^2$$

$$\leq \int |\omega|^2 (\lambda_1 - \delta) \, dx - \nu\|\nabla\omega\|_{L^2}^2$$

### 10.3 Bound de $\lambda_1$

Pelo Biot-Savart: $\|S\|_{L^\infty} \lesssim \|\omega\|_{L^\infty}$.

Portanto $\lambda_1(x) \lesssim \|\omega\|_{L^\infty}$.

### 10.4 Estimativa Final

$$\frac{d\Omega}{dt} \leq C\|\omega\|_{L^\infty}\Omega - \delta \Omega - \nu\|\nabla\omega\|_{L^2}^2$$

$$\leq (C\|\omega\|_{L^\infty} - \delta)\Omega$$

Se conseguirmos que $\|\omega\|_{L^\infty} \leq C(\Omega)$ (controle via enstrofia), fecha!

---

## 11. A PEÇA FALTANTE

### 11.1 O Que Precisamos

Relação $\|\omega\|_{L^\infty} \leq C \Omega^a$ para algum $a < 1$.

### 11.2 O Que Temos

Pelo Sobolev: $\|\omega\|_{L^\infty} \lesssim \|\omega\|_{H^{3/2+\epsilon}}$.

Mas $\|\omega\|_{H^{3/2+\epsilon}}$ não é controlado por $\Omega = \|\omega\|_{L^2}^2/2$.

### 11.3 Possível Saída

**Hipótese de Gap:** Se o gap de alinhamento é suficientemente forte:
$$\mathcal{G} \geq \delta |\omega|^\beta \text{ para algum } \beta > 0$$

Então o stretching fica **mais fraco** onde $|\omega|$ é máximo.

### 11.4 Consequência

Com stretching suprimido nos picos de vorticidade:
- $\|\omega\|_{L^\infty}$ cresce mais lentamente
- Pode haver bound uniforme

---

## 12. SÍNTESE

### 12.1 Mecanismos Identificados

| Mecanismo | Efeito em $\alpha_1$ | Sinal |
|-----------|---------------------|-------|
| Strain $S\hat{\omega}$ | Alinha com $e_1$ | + |
| Rotação de $e_1$ por $\omega\otimes\omega$ | Desalinha | − |
| Difusão | Isotropiza | − |
| Pressão | Depende | ± |

### 12.2 Conclusão Qualitativa

Os mecanismos de desalinhamento são proporcionais a $|\omega|^2$.

Os mecanismos de alinhamento são proporcionais a $\lambda_1 \sim |\omega|$.

**Para $|\omega|$ grande, desalinhamento domina!**

### 12.3 Status da Prova

| Componente | Status |
|------------|--------|
| Identificação dos termos | ✅ Completo |
| Estrutura qualitativa | ✅ Clara |
| Bound do gap | 🟠 Precisa formalizar |
| Conexão com BKM | 🟠 Precisa fechar |
| Prova rigorosa | ❌ Em andamento |

---

## 13. PRÓXIMOS PASSOS

### 13.1 Técnico

1. Formalizar o bound no termo de rotação de $e_1$
2. Provar que difusão impede $\alpha_1 \to 1$
3. Combinar em estimativa fechada

### 13.2 Conceitual

Explorar se a estrutura probabilística de turbulência garante gap uniforme.

### 13.3 Alternativo

Verificar se há contra-exemplo: solução com $\alpha_1 \to 1$ em blow-up.

---

## 14. CONCLUSÃO

**O gap de alinhamento emerge naturalmente da dinâmica de NS.**

A vorticidade intensa cria um campo de strain que **evita seu próprio alinhamento máximo**.

É um mecanismo de **auto-regulação intrínseco** às equações.

Se formalizado, fecha o problema.

**Status:** 🟠 ESTRUTURA COMPLETA — FALTA RIGOR TÉCNICO.
