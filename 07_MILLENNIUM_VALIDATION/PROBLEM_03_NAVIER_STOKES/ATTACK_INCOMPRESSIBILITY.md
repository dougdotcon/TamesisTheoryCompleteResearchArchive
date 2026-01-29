# ATTACK: Cancelamentos da Incompressibilidade — O Papel de ∇·u = 0

**Data:** 2025-01-29
**Status:** 🔵 EXPLORAÇÃO TÉCNICA
**Objetivo:** Extrair bounds adicionais da condição de divergência zero

---

## 1. A RESTRIÇÃO DE INCOMPRESSIBILIDADE

### 1.1 A Condição

$$\nabla \cdot u = 0 \quad \text{(em todo ponto)}$$

Esta é uma **constraint global** que relaciona as três componentes de $u$.

### 1.2 Em Fourier

$$\hat{u}(k) \cdot k = 0 \quad \forall k$$

O campo de velocidade é **perpendicular** ao vetor de onda em cada modo.

### 1.3 Consequência Geométrica

O espaço de campos incompressíveis é um **subespaço** de $L^2(\mathbb{R}^3; \mathbb{R}^3)$.

Especificamente, é o kernel do operador divergência: $\ker(\nabla \cdot)$.

---

## 2. PROJEÇÃO DE LERAY

### 2.1 Definição

O projetor de Leray $\mathbb{P}$ projeta campos vetoriais no espaço incompressível:

$$\mathbb{P} = I - \nabla \Delta^{-1} \nabla \cdot$$

Em Fourier:
$$\widehat{\mathbb{P} f}(k) = \left(I - \frac{k \otimes k}{|k|^2}\right) \hat{f}(k)$$

### 2.2 Propriedades

- $\mathbb{P}^2 = \mathbb{P}$ (projetor)
- $\mathbb{P} u = u$ se $\nabla \cdot u = 0$
- $\mathbb{P} \nabla \phi = 0$ para qualquer $\phi$

### 2.3 NS em Forma Projetada

$$\partial_t u + \mathbb{P}[(u \cdot \nabla)u] = \nu \Delta u$$

A pressão é eliminada automaticamente!

---

## 3. O TERMO NÃO-LINEAR PROJETADO

### 3.1 Estrutura

$$\mathbb{P}[(u \cdot \nabla)u] = (u \cdot \nabla)u + \nabla p$$

onde $p$ resolve:
$$\Delta p = -\nabla \cdot [(u \cdot \nabla)u] = -\partial_i \partial_j (u_i u_j)$$

### 3.2 Forma Alternativa

Usando incompressibilidade:
$$(u \cdot \nabla)u = \nabla \cdot (u \otimes u)$$

Então:
$$\mathbb{P}[(u \cdot \nabla)u] = \mathbb{P}[\nabla \cdot (u \otimes u)]$$

### 3.3 Em Fourier

$$\widehat{\mathbb{P}[(u \cdot \nabla)u]}(k) = i \sum_j k_j \left(I - \frac{k \otimes k}{|k|^2}\right) \widehat{u_j u}(k)$$

---

## 4. CANCELAMENTOS NO PARAPRODUCT

### 4.1 Decomposição de Bony

Para $f, g$ funções:
$$fg = T_f g + T_g f + R(f,g)$$

onde:
- $T_f g = \sum_j S_{j-2} f \cdot \Delta_j g$ (paraproduct: baixa freq × alta freq)
- $R(f,g) = \sum_{|j-k| \leq 1} \Delta_j f \cdot \Delta_k g$ (resto: freq comparáveis)

### 4.2 Aplicação a $(u \cdot \nabla)u$

$$(u \cdot \nabla)u = T_u \nabla u + T_{\nabla u} u + R(u, \nabla u)$$

### 4.3 O Cancelamento da Incompressibilidade

**Observação chave:** Quando aplicamos $\mathbb{P}$, alguns termos se cancelam.

Para o paraproduct $T_u \nabla u$:
$$\mathbb{P}[T_u \nabla u] = T_u \nabla u - \nabla \Delta^{-1} \nabla \cdot [T_u \nabla u]$$

O termo de correção $\nabla \Delta^{-1} \nabla \cdot [\cdots]$ envolve derivadas adicionais, mas ganha regularidade.

---

## 5. ESTIMATIVAS MELHORADAS

### 5.1 Estimativa Padrão (sem incompressibilidade)

$$\|(u \cdot \nabla)u\|_{H^{-1}} \lesssim \|u\|_{L^4}^2$$

### 5.2 Estimativa com Projeção de Leray

$$\|\mathbb{P}[(u \cdot \nabla)u]\|_{H^{-1}} \lesssim \|u\|_{L^2} \|\nabla u\|_{L^2}$$

**Melhoria:** Usamos $L^2$ (energia) ao invés de $L^4$.

### 5.3 Prova da Melhoria

Pela estrutura:
$$\mathbb{P}[(u \cdot \nabla)u] = \mathbb{P}[\nabla \cdot (u \otimes u)]$$

Em $H^{-1}$:
$$\|\mathbb{P}[\nabla \cdot (u \otimes u)]\|_{H^{-1}} \lesssim \|u \otimes u\|_{L^2} = \|u\|_{L^4}^2$$

Mas usando interpolação $\|u\|_{L^4} \lesssim \|u\|_{L^2}^{1/4} \|\nabla u\|_{L^2}^{3/4}$:

$$\|\mathbb{P}[(u \cdot \nabla)u]\|_{H^{-1}} \lesssim \|u\|_{L^2}^{1/2} \|\nabla u\|_{L^2}^{3/2}$$

---

## 6. CONSEQUÊNCIA PARA TRANSFERÊNCIA DE ENERGIA

### 6.1 Fluxo de Energia Revisitado

$$\frac{dE}{dt} = -\underbrace{\int u \cdot \mathbb{P}[(u \cdot \nabla)u] dx}_{= 0} - \nu \|\nabla u\|_{L^2}^2$$

O primeiro termo é **ZERO** porque:
$$\int u \cdot (u \cdot \nabla)u \, dx = \int u \cdot \nabla\left(\frac{|u|^2}{2}\right) dx = -\int \frac{|u|^2}{2} \nabla \cdot u \, dx = 0$$

### 6.2 Interpretação

A incompressibilidade garante que o termo não-linear **não produz nem consome energia**.

Toda a dinâmica energética é:
$$\frac{dE}{dt} = -\nu \|\nabla u\|_{L^2}^2 \leq 0$$

### 6.3 Mas e a Transferência por Escala?

A energia total é conservada pelo não-linear, mas **redistribuída entre escalas**.

O fluxo $T_j$ mede essa redistribuição:
$$\sum_j T_j = 0 \quad \text{(conservação)}$$

Mas $T_j$ individual pode ser grande.

---

## 7. A ESTRUTURA TENSORIAL DE u ⊗ u

### 7.1 Propriedades do Tensor

O tensor $u \otimes u$ é:
- Simétrico: $(u \otimes u)_{ij} = u_i u_j$
- Não-negativo: $v^T (u \otimes u) v = (u \cdot v)^2 \geq 0$
- Traço: $\text{tr}(u \otimes u) = |u|^2$

### 7.2 Relação com Pressão

A pressão resolve:
$$\Delta p = -\text{tr}(\nabla^2 (u \otimes u)) = -\partial_i \partial_j (u_i u_j)$$

### 7.3 Bound na Pressão

$$\|p\|_{L^{3/2}} \lesssim \|u\|_{L^3}^2$$

E pela equação de NS:
$$\|\nabla p\|_{L^{3/2}} \lesssim \|u\|_{L^3} \|\nabla u\|_{L^2}$$

---

## 8. HELICIDADE E INCOMPRESSIBILIDADE

### 8.1 Helicidade

$$H = \int u \cdot \omega \, dx = \int u \cdot (\nabla \times u) \, dx$$

### 8.2 Evolução

$$\frac{dH}{dt} = -2\nu \int \omega \cdot (\nabla \times \omega) \, dx$$

### 8.3 Significado Geométrico

Helicidade mede o "enrolamento" do campo de velocidade.

Se $H \neq 0$, as linhas de corrente estão topologicamente ligadas.

### 8.4 Restrição

**Observação:** Configurações de blow-up com $H \neq 0$ são mais restritas.

O colapso a um ponto destruiria a topologia do enlace.

---

## 9. NOVA ESTIMATIVA: USANDO INCOMPRESSIBILIDADE NO FLUXO

### 9.1 Fluxo de Energia para Escala j

$$T_j = \int \Delta_j u \cdot \Delta_j[(u \cdot \nabla)u] dx$$

### 9.2 Reescrevendo com Projeção

Como $\Delta_j u$ já é incompressível:
$$T_j = \int \Delta_j u \cdot \mathbb{P}\Delta_j[(u \cdot \nabla)u] dx$$

### 9.3 Usando a Estrutura

$$\mathbb{P}\Delta_j[(u \cdot \nabla)u] = \mathbb{P}\Delta_j[\nabla \cdot (u \otimes u)]$$

Em Fourier, isso envolve a projeção:
$$\widehat{\mathbb{P}\Delta_j[\nabla \cdot (u \otimes u)]}(k) = i|k| \phi_j(k) \left(I - \frac{k \otimes k}{|k|^2}\right) \widehat{u \otimes u}(k) \cdot \frac{k}{|k|}$$

### 9.4 Simplificação

A projeção remove a componente longitudinal:
$$\left(I - \frac{k \otimes k}{|k|^2}\right) A \cdot \frac{k}{|k|} = A \cdot \frac{k}{|k|} - \frac{(A \cdot k)(k \cdot k)}{|k|^3} \cdot \frac{k}{|k|}$$

Hmm, isso não simplifica trivialmente...

---

## 10. ABORDAGEM ALTERNATIVA: VORTICIDADE

### 10.1 Equação de Vorticidade

$$\partial_t \omega + (u \cdot \nabla)\omega = (\omega \cdot \nabla)u + \nu \Delta \omega$$

### 10.2 Vantagem

Não há pressão na equação de vorticidade!

A incompressibilidade está "embutida" em $\omega = \nabla \times u$.

### 10.3 Estimativa do Stretching

$$\left|\int \omega \cdot S \cdot \omega \, dx\right| \leq \|S\|_{L^p} \|\omega\|_{L^{2p/(p-1)}}^2$$

Usando $S = \frac{1}{2}(\nabla u + \nabla u^T)$ e Calderon-Zygmund:
$$\|S\|_{L^p} \lesssim \|\omega\|_{L^p}$$

### 10.4 Fechamento?

$$\left|\int \omega \cdot S \cdot \omega \, dx\right| \lesssim \|\omega\|_{L^3}^3$$

Usando interpolação: $\|\omega\|_{L^3} \lesssim \|\omega\|_{L^2}^{1/2} \|\nabla\omega\|_{L^2}^{1/2}$

$$\left|\int \omega \cdot S \cdot \omega \, dx\right| \lesssim \Omega^{3/4} \|\nabla\omega\|_{L^2}^{3/2}$$

Mas precisamos comparar com a dissipação $\nu \|\nabla\omega\|_{L^2}^2$.

---

## 11. O GAP PERSISTENTE

### 11.1 A Comparação Crítica

Stretching: $\lesssim \Omega^{3/4} \|\nabla\omega\|_{L^2}^{3/2}$

Dissipação: $= \nu \|\nabla\omega\|_{L^2}^2$

### 11.2 Quando Dissipação Domina?

$$\nu \|\nabla\omega\|_{L^2}^2 > C \Omega^{3/4} \|\nabla\omega\|_{L^2}^{3/2}$$

$$\Leftrightarrow \|\nabla\omega\|_{L^2} > \frac{C}{\nu} \Omega^{3/4}$$

### 11.3 O Problema

Se $\Omega$ cresce, precisamos que $\|\nabla\omega\|_{L^2}$ cresça mais rápido.

Mas $\|\nabla\omega\|_{L^2}$ é o que queremos controlar!

**Circularidade não resolvida.**

---

## 12. TENTATIVA: LOG-GRONWALL

### 12.1 Desigualdade Diferencial

$$\frac{d\Omega}{dt} \leq C \Omega^{3/2} - \nu \|\nabla\omega\|_{L^2}^2$$

Usando Poincaré em escala: $\|\nabla\omega\|_{L^2}^2 \geq \lambda_1 \Omega$ para algum $\lambda_1 > 0$ (se domínio é limitado).

### 12.2 Simplificação

$$\frac{d\Omega}{dt} \leq C \Omega^{3/2} - \nu \lambda_1 \Omega$$

### 12.3 Análise

- Para $\Omega$ pequeno: segundo termo domina (estabilidade)
- Para $\Omega$ grande: primeiro termo domina (instabilidade)

Threshold: $\Omega^* = (\nu \lambda_1 / C)^2$

### 12.4 O Problema do Domínio Infinito

Em $\mathbb{R}^3$, não há Poincaré. $\lambda_1 = 0$.

**A estimativa não fecha em espaço inteiro.**

---

## 13. SÍNTESE: O QUE A INCOMPRESSIBILIDADE DÁ

### 13.1 Ganhos

✅ Conservação de energia pelo não-linear  
✅ Eliminação da pressão via projeção de Leray  
✅ Melhoria de algumas estimativas (5.2)  
✅ Estrutura tensorial de $u \otimes u$  
✅ Helicidade como invariante adicional  

### 13.2 O Que Não Resolve

❌ Bound direto no stretching por energia  
❌ Fechamento da desigualdade de enstrofia  
❌ Controle do fluxo de energia por escala  

### 13.3 Conclusão Parcial

A incompressibilidade é **necessária** para a estrutura do problema, mas **não suficiente** para fechar o gap.

---

## 14. DIREÇÃO FINAL: ESTRUTURA ESPECÍFICA DO STRETCHING

### 14.1 Observação

O termo $(\omega \cdot \nabla)u = \omega \cdot S \cdot \hat{\omega} \cdot |\omega|$ onde $\hat{\omega} = \omega/|\omega|$.

### 14.2 Alinhamento

O stretching máximo ocorre quando $\omega$ alinha com autovetor de $S$ de autovalor máximo.

**Mas:** Esse alinhamento é dinamicamente instável!

### 14.3 Conjectura de Alinhamento

Se pudermos provar que o alinhamento máximo é repelido pela dinâmica, então o stretching efetivo é menor que o máximo.

**Status:** 🟠 Hipótese interessante, não provada.

---

## 15. CONCLUSÃO

A incompressibilidade fornece **estrutura rica** mas **não fecha o gap**.

O próximo passo é investigar a **dinâmica do alinhamento** $\omega$-$S$.

Se o alinhamento máximo for provado instável, isso pode dar o bound faltante.

**Status:** 🟡 Progresso estrutural, gap persiste.
