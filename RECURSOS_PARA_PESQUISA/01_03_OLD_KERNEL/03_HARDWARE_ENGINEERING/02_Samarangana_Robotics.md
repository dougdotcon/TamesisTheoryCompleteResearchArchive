![Source](https://img.shields.io/badge/Fonte-Samarangana_Sutradhara-green)
![Concept](https://img.shields.io/badge/Conceito-Yantra_/_Control_System-orange)
![Status](https://img.shields.io/badge/Status-Simulacao_FSM-success)

# Decodificação Tamesis: A Engenharia de Bhoja

> *"Enquanto o Vimanika Shastra é vago, o Rei Bhoja (c. 1000 d.C.) escreve como um engenheiro. Ele descreve polias, válvulas e lógica de controle."*

---

## 1. Definição Técnico-Científica de Yantra

Bhoja define uma máquina (*Yantra*) não como mágica, mas como um sistema de controle de energia.

* **Texto Original:** "Yantra é aquilo que controla e dirige os elementos (Bhutas) de acordo com a vontade."
* **Tradução Tamesis:** **Sistemas de Controle de Feedback (Control Loop).**

Um Yantra reduz a entropia local organizando o fluxo de energia caótica (*Rajas*) em trabalho útil (*Karma*).

### Os Elementos Constitutivos

| Termo Sânscrito | Tradução Tamesis | Função de Engenharia |
| :--- | :--- | :--- |
| **Bija (Semente)** | **Power Supply / Input** | A fonte de força (gravidade, água, fogo). |
| **Kila (Pino)** | **Logic Gate / Key** | O mecanismo de travamento ou decisão lógica. |
| **Sutra (Fio)** | **Data Bus / Transmission** | Correias e cordas que transmitem informação mecânica. |

---

## 2. Iniciação à Cibernética: Os Autômatos (*Putrika*)

O Capítulo 31 descreve "soldados robôs" e "porteiros mecânicos".
A engenharia não é elétrica, é **Lógica Fluídica e Mecânica**.

* **Hardware:** Hidráulica e Pneumática.
* **Software:** Máquinas de Estados Finitos (FSM).
* **Exemplo:** O Porteiro de Bhoja usa sensores de pressão (peso no degrau) para acionar válvulas hidráulicas (AND/OR gates) que abrem a porta ou disparam armas.

---

## 3. A Confirmação do Motor de Mercúrio

Bhoja fornece a descrição mais sóbria e técnica do motor, validando nossa hipótese MHD.

**Versos 95-100:**

* *"No centro, coloque uma caldeira de ferro contendo mercúrio."* (Confinamento Magnético).
* *"Abaixo, coloque o fogo."* (Transição de Fase Líquido-Vapor/Plasma).
* *"Pelo poder latente no mercúrio aquecido..."*
  * **Latente (*Rasa*):** Energia Interna. Não é combustão química, é liberação de energia de estado.

> **O "Bug" Intencional:** Bhoja admite: "Eu não dou os detalhes completos para manter o segredo, pois isso é tecnologia de uso dual (civil e militar)."

---

## 4. Validação Computacional: Lógica de Autômatos

Simulamos a lógica descrita por Bhoja em ![Log FSM](../assets/robotics_fsm_log.png) `ancient_robotics.py` para provar que componentes mecânicos simples podem executar algoritmos complexos.

**Cenário: O Porteiro Mecânico (Gatekeeper FSM)**

* **Inputs:** Peso, Chave Secreta.
* **Lógica:**
  * `IF (Peso > 50kg) AND (Tem_Chave) -> OPEN_DOOR`
  * `IF (Peso > 50kg) AND (!Tem_Chave) -> ATTACK`

**Resultado da Simulação:**

```text
[Teste 1] Invasor se aproxima...
[Guarda Mecânico] CONDIÇÃO ATIVADA! Executando ação...
>> Ação Mecânica: Mola Comprimida Liberada. Lança Disparada!
[STATUS ALERTA]: INTRUSO DETECTADO
```

> **Conclusão:** Os "robôs" de Bhoja eram funcionalmente equivalentes aos autômatos de Jacquet-Droz do séc. XVIII. Eles possuíam lógica programável via hardware.

---

## 5. Veredito Final

O *Samarangana Sutradhara* é o **Manual de Mecatrônica** dos Vimanas.
Ele prova que a infraestrutura para construir essas máquinas (robótica, metalurgia, hidráulica) já era compreendida e formalizada como ciência (*Vastu Shastra*).
