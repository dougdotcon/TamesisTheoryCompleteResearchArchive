# CRITÉRIO BKM REFINADO — Análise do Beale-Kato-Majda

**Data:** 2025-01-13
**Status:** 🟡 ANÁLISE DE CRITÉRIO
**Objetivo:** Explorar refinamentos do critério de blow-up

---

## 1. O TEOREMA BEALE-KATO-MAJDA

### 1.1 Enunciado Original (1984)

**Teorema (BKM):** Seja $u$ solução suave de NS em $[0, T^*)$ com $T^* < \infty$ tempo maximal. Então:

$$
\int_0^{T^*} \|\omega(\cdot, t)\|_{L^\infty} dt = \infty
$$

### 1.2 Contraposição

Se para todo $T > 0$:
$$
\int_0^T \|\omega(\cdot, t)\|_{L^\infty} dt < \infty
$$

então solução global suave existe.

### 1.3 Significado Físico

Blow-up requer que vorticidade máxima cresça tão rapidamente que sua integral temporal diverge.

---

## 2. REFINAMENTOS CONHECIDOS

### 2.1 Critério de Kozono-Taniuchi (2000)

Blow-up implica:
$$
\int_0^{T^*} \|\omega\|_{BMO}^2 dt = \infty
$$

onde $BMO$ é o espaço de oscilação média limitada.

**Vantagem:** $\|\cdot\|_{BMO}$ é mais fraco que $\|\cdot\|_{L^\infty}$.

### 2.2 Critério de Escauriaza-Seregin-Šverák (2003)

Se $u$ satisfaz:
$$
u \in L^\infty(0, T; L^3(\mathbb{R}^3))
$$

então $u$ é regular.

**Significado:** Controlando apenas $L^3$, obtemos regularidade.

### 2.3 Critério de Seregin (2012)

Type I blow-up não ocorre:
$$
\limsup_{t \to T^*} (T^* - t)^{1/2} \|u(\cdot, t)\|_{L^\infty} = \infty
$$

é necessário para blow-up.

---

## 3. ANÁLISE DO CRITÉRIO BKM

### 3.1 Dedução do Critério

Partindo da equação de enstrofia:
$$
\frac{d\Omega}{dt} = \int \omega \cdot S \cdot \omega \, dx - \nu \|\nabla\omega\|_{L^2}^2
$$

Usando $\|S\|_{L^\infty} \lesssim \|\omega\|_{L^\infty}$:
$$
\frac{d\Omega}{dt} \leq C \|\omega\|_{L^\infty} \Omega
$$

Por Gronwall:
$$
\Omega(t) \leq \Omega(0) \exp\left(C \int_0^t \|\omega\|_{L^\infty} ds\right)
$$

Se a integral diverge quando $t \to T^*$, $\Omega$ pode explodir.

### 3.2 Por Que Não Fecha?

O bound de Gronwall só diz que $\Omega$ PODE crescer, não que DEVE.

**Precisamos:** Mostrar que $\int \|\omega\|_{L^\infty} dt$ é finito para soluções de NS.

---

## 4. TENTATIVAS DE BOUND EM $\|\omega\|_{L^\infty}$

### 4.1 Via Biot-Savart

$$
u(x) = \frac{1}{4\pi} \int \frac{\omega(y) \times (x-y)}{|x-y|^3} dy
$$

**Bound:**
$$
\|u\|_{L^\infty} \lesssim \|\omega\|_{L^1}^{1/3} \|\omega\|_{L^\infty}^{2/3}
$$

### 4.2 Via Equação de Vorticidade

$$
\partial_t \omega + (u \cdot \nabla)\omega = (\omega \cdot \nabla)u + \nu \Delta \omega
$$

O termo $(\omega \cdot \nabla)u$ é o stretching.

**Estimativa pontual:**
$$
\frac{D|\omega|}{Dt} \leq |S| |\omega| + \nu \Delta |\omega|
$$

Isso não fecha porque $|S| \sim |\omega|$.

### 4.3 Via Funções de Lyapunov

**Tentativa:** Encontrar $\Phi(\omega)$ tal que $\frac{d\Phi}{dt} \leq 0$.

**Problema:** Não se conhece tal funcional para NS 3D.

---

## 5. CONEXÃO COM K41

### 5.1 Escala de Kolmogorov

Se $\epsilon \leq \epsilon_0$ (K41), então:
$$
\eta = \left(\frac{\nu^3}{\epsilon}\right)^{1/4} \geq \eta_{min} = \left(\frac{\nu^3}{\epsilon_0}\right)^{1/4}
$$

### 5.2 Vorticidade na Escala Viscosa

$$
|\omega| \sim \frac{u_\eta}{\eta} = \frac{(\epsilon\nu)^{1/4}}{\eta} = \left(\frac{\epsilon}{\nu}\right)^{1/2}
$$

### 5.3 Bound Resultante

$$
\|\omega\|_{L^\infty} \lesssim \left(\frac{\epsilon_0}{\nu}\right)^{1/2}
$$

**Então:**
$$
\int_0^T \|\omega\|_{L^\infty} dt \lesssim T \left(\frac{\epsilon_0}{\nu}\right)^{1/2} < \infty
$$

**Conclusão:** K41 ⟹ BKM satisfeito ⟹ Regularidade.

---

## 6. ANÁLISE REVERSA: BKM ⟹ K41?

### 6.1 Pergunta

Se BKM é satisfeito, isso implica K41?

### 6.2 Resposta

**Não diretamente.** BKM é uma condição sobre $\omega$, K41 é sobre $\epsilon$.

**Mas:** Se $\|\omega\|_{L^\infty}$ é limitada, então:
$$
\epsilon = \nu \|\nabla u\|_{L^2}^2 \lesssim \nu \|\omega\|_{L^2}^2 \lesssim \nu \|\omega\|_{L^\infty}^2 V
$$

onde $V$ é o volume onde $\omega \neq 0$.

**Problema:** $V$ pode crescer.

---

## 7. CRITÉRIOS ALTERNATIVOS

### 7.1 Critério de Pressão

**Chae-Lee (2001):**
$$
\int_0^{T^*} \|\nabla p\|_{L^{3/2}} dt = \infty
$$

implica blow-up.

### 7.2 Critério de Velocidade

**Prodi-Serrin:**

Se $u \in L^q(0,T; L^p)$ com $\frac{2}{q} + \frac{3}{p} \leq 1$, $p > 3$, então regularidade.

**Caso limite:** $p = \infty$, $q = 2$:
$$
\int_0^T \|u\|_{L^\infty}^2 dt < \infty \Rightarrow \text{regularidade}
$$

### 7.3 Critério Direcional

**Chemin-Zhang (2016):**

Se uma componente de $u$ está em $L^q(L^p)$ com condição Prodi-Serrin, regularidade.

**Significado:** Blow-up requer crescimento em TODAS as direções.

---

## 8. CENÁRIOS DE BLOW-UP

### 8.1 Self-Similar

$$
u(x,t) = \frac{1}{\sqrt{T^* - t}} U\left(\frac{x}{\sqrt{T^* - t}}\right)
$$

**Status:** Excluído por Nečas-Růžička-Šverák (1996) para $U \in L^3$.

### 8.2 Type I

$$
\|u(\cdot, t)\|_{L^\infty} \lesssim (T^* - t)^{-1/2}
$$

**Status:** Excluído por Seregin-Šverák.

### 8.3 Type II (Único Restante)

Crescimento mais rápido que self-similar:
$$
\|u(\cdot, t)\|_{L^\infty} \gg (T^* - t)^{-1/2}
$$

**Status:** NÃO EXCLUÍDO.

---

## 9. HIPÓTESE DE TRABALHO

### 9.1 Conjectura

**Type II blow-up não ocorre para NS.**

### 9.2 Motivação

1. Type II requer configuração muito especial
2. Dissipação viscosa aumenta para altas frequências
3. Nenhuma evidência numérica de Type II

### 9.3 Dificuldade de Prova

Type II é definido negativamente (não é Type I).

Precisaríamos excluir TODOS os cenários de blow-up rápido.

---

## 10. SÍNTESE

### 10.1 Estado dos Critérios

| Critério | Status |
|----------|--------|
| BKM | Necessário e suficiente para blow-up |
| Kozono-Taniuchi | Refinamento em BMO |
| ESŠ | $L^3$ controla |
| Type I | Excluído |
| Type II | Aberto |

### 10.2 A Cadeia Lógica

$$
\text{NS} \xrightarrow{?} K41 \xrightarrow{\checkmark} \text{BKM satisfeito} \xrightarrow{\checkmark} \text{Regularidade}
$$

O gap está em NS ⟹ K41 (ou equivalentemente, excluir Type II).

### 10.3 Conclusão

BKM não resolve o problema diretamente - apenas reformula.

**De "solução é suave" para "integral de vorticidade é finita".**

A dificuldade real está em mostrar que soluções de NS satisfazem esta condição.

---

## 11. PRÓXIMOS PASSOS

1. Investigar estrutura de potenciais Type II blow-ups
2. Buscar novos critérios que excluam Type II
3. Explorar restrições geométricas adicionais

**Status:** 🟡 Compreensão aprofundada, gap persiste.
