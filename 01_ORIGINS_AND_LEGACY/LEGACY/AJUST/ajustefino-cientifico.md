# PROTOCOLO DE AJUSTE FINO E RIGOR CIENTÍFICO
>
> **Objetivo:** Blindagem Acadêmica. "A vulnerabilidade nasce na ambiguidade."

Este documento deve ser consultado antes de finalizar qualquer artefato (Paper, Roadmap, Teorema). Se um documento houver falhas nestes critérios, ele é considerado **Vulnerável** e deve ser reescrito.

---

## 1. 🛡️ O Filtro de Separação (The Separation Filter)

A maior vulnerabilidade é misturar categorias ontológicas.

- [ ] **Identidade Clara:** O documento é explicitamente MATEMÁTICO, FÍSICO ou COMPUTACIONAL?
- [ ] **Higiene Matemática:** Se é um documento matemático (Paper A), existe alguma menção a "tempo", "universo", "Big Bounce" ou "energia" no corpo dos teoremas?
  - *Regra:* Teoremas matemáticos operam sobre conjuntos e operadores, não sobre o mundo real.
- [ ] **Higiene Física:** Se é um documento físico (Paper B), existe alguma pretensão de prova matemática absoluta (ZFC)?
  - *Regra:* A física argumenta sobre *plausibilidade, estabilidade e custo*, não sobre verdade lógica eterna.

## 2. 🏛️ O Teste de Definição (The Definition Test)

Vulnerabilidade: Usar termos carregados sem lastro formal.

- [ ] **Definição Explícita:** Toda entidade nomeada (ex: "Critical Instant", "Classe $C_{crit}$", "PRC") possui uma definição formal numerada (Def 1.1, Axioma 3)?
- [ ] **Autocontenção:** As definições dependem de metáforas ("como um fluido") ou são autocontidas ("conjunto de operadores autoadjuntos")?
- [ ] **Axiomas Expostos:** As premissas estão escondidas no texto ou listadas como "Axiomas"? (Esconder premissas é erro fatal).

## 3. ⚔️ O Escudo de Condicionalidade (The Conditional Shield)

Vulnerabilidade: Afirmar mais do que se provou.

- [ ] **Estrutura "Se-Então":** Teoremas fortes ("P != NP", "RH é verdade") foram substituídos por Teoremas Condicionais ou de Censura?
  - *Ex:* "Se a Classe C for respeitada, então RH..."
- [ ] **Explicitação da Hipótese:** O texto deixa explícito que a conclusão depende das premissas físicas (Axiomas de Realizabilidade)?
- [ ] **Barreira vs Impossibilidade:** Em complexidade, usamos "Censura Termodinâmica" (Barreira Física) em vez de "Impossibilidade Lógica"?

## 4. 🧪 Precisão Linguística (Vocabulary Hygiene)

Vulnerabilidade: Linguagem grandiloquente ou imprecisa.

| ❌ Proibido / Vulnerável | ✅ Seguro / Acadêmico |
| :--- | :--- |
| "Provamos que..." | "Demonstramos que, sob a classe C..." |
| "O universo computa..." | "Um sistema físico realizável computa..." |
| "Impossível" | "Termodinamicamente inviável (Censurado)" |
| "A verdade sobre os primos" | "A estabilidade espectral dos primos" |
| "O operador é..." | "Definimos o operador como..." |

## 5. 🚩 Auditoria de Red Flags

- [ ] **Hand-waving:** Pular a matemática difícil apelando para "intuição física" no meio de uma prova.
- [ ] **Confusão de Escala:** Misturar resultados de simulação (N=400) com asserções assintóticas ($N \to \infty$) sem a devida extrapolação formal (Finite Size Scaling).
- [ ] **Antropomorfização:** O sistema "quer", "sabe", "escolhe". (Substituir por: "O sistema evolui para", "O estado minimiza").

---

## Status de Revisão Atual

- [ ] **Track A (P vs NP):** Verificar Papers A, B, C contra este protocolo.
- [ ] **Track B (Riemann):** Verificar Papers A, B, C contra este protocolo.
- [ ] **Track C (Structural Solvability):** Aplicar desde o design.

> **Regra de Ouro:** "Uma prova matemática com um buraco físico é lixo. Um argumento físico com um buraco matemático é uma teoria. Saiba qual você está escrevendo."
