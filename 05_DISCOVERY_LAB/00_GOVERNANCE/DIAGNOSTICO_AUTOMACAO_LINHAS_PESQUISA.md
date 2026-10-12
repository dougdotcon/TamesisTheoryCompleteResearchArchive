# Diagnóstico e Roteiro de Automação das 16 Linhas de Pesquisa Tamesis

**Data do Registro:** 2026-10-12  
**Finalidade:** Lembrete técnico e roteiro acionável para guiar o trabalho futuro de estruturação, pré-registro e automação das linhas de pesquisa que ainda não estão prontas para o daemon 24/7.  
**Fontes de Auditoria:** `PROJECT_STATE.json`, `FAILED_HYPOTHESES.md`, `05_DISCOVERY_LAB/01_PORTFOLIO/TEST_QUEUE.yaml`, `RELATORIO_VISAO_FINAL_LABORATORIO_TAMESIS.md`.

---

## 1. O Critério Inegociável de Automação

Para que uma linha de pesquisa possa ser incorporada com segurança ao daemon contínuo na RTX 5090 (sem alucinar resultados ou gerar falsos positivos), ela precisa satisfazer a tríade do Discovery Lab:
1. **Representação Matemática Executável:** Uma fórmula fechada, equações diferenciais numéricas, grafo combinatorial ou código verificável em SymPy/Lean 4 (não metáforas qualitativas).
2. **Avaliador Imutável (*Harness*):** Um conjunto de testes estáticos, banco de dados observacional real com *checksum* ou lema de controle (a régua que o agente não pode modificar).
3. **Critério Falsificável Pré-Registrado:** Limiares objetivos de aceitação/rejeição ($p$-valor com correção, $\chi^2$, margem espectral ou resíduo assintótico).

---

## 2. Mapa Geral de Prontidão das 16 Linhas (A a P)

```mermaid
flowchart TD
    subgraph AUTO [1. Totalmente Automatizadas e Ativas (4 Linhas)]
        LD["Linha D: Universalidade U(1/2) e Permutações (Ativa no Daemon)"]
        LE["Linha E: Espectral, Berry–Keating e Zeros de Riemann (Ativa no Daemon)"]
        LN["Linha N: Problemas do Milênio / Auditoria OAI (Ativa no Daemon)"]
        LP["Linha P: Infraestrutura e Discovery Engine (Ativa no Daemon)"]
    end

    subgraph PRE_REG [2. Pronta para Automação — Falta Pré-Registro (1 Linha)]
        LG["Linha G: Cosmologia SPARC & Binárias Gaia DR3 (Exige PREREGISTRATION.md)"]
    end

    subgraph BLOCKED_DATA [3. Bloqueadas por Dependência Física/Clínica (3 Linhas)]
        LJ["Linha J: Colapso Quântico e Massa Crítica M_c (Exige Metrologia Real)"]
        LK["Linha K: Ecossistemas Cognitivos & EEG (Bloqueio de Login Médico)"]
        LL["Linha L: Topologia Cognitiva & C_bio (Falta Sensor Fisiológico)"]
    end

    subgraph NO_EQUATIONS [4. Bloqueadas por Falta de Equações Fechadas (5 Linhas)]
        LA["Linha A: Arquitetura da Realidade (Falta Ação Variacional)"]
        LB["Linha B: Axiomas e Pontes de Unificação (Conceitos Verbais)"]
        LH["Linha H: Buracos Negros e Bounce Entrópico (Falta Tensor T_uv)"]
        LO["Linha O: Engenharia Métrica e Universos-Pais (Soluções Instáveis)"]
        LM["Linha M: Estabilidade de Operadores e Leue Horizon (Domínio Aberto)"]
    end

    subgraph REFUTED [5. Fechadas / Refutadas — Exigem Nova Teoria (3 Linhas)]
        LC["Linha C: Invariantes TRI-RG (16/16 Candidatos Fecharam NULL)"]
        LI["Linha I: Física de Partículas e Nós (Fórmulas Refutadas a 7.5 sigma)"]
        LF["Linha F: Grafos e Primos (Heurística sem Teorema de Correspondência)"]
    end
```

---

## 3. Detalhamento e O Que Fazer para Desbloquear Cada Linha

### Bloco A — Pronta para Automação Imediata (Falta apenas Governança)

#### Linha G — Cosmologia Observacional e Astrofísica (SPARC / MOND / Gaia DR3)
* **Diagnóstico Atual:** Os testes anteriores (`SPARC-001` a `SPARC-004`) fecharam como `INCONCLUSIVE` devido à contaminação de multiplicidade estelar em estrelas com alto RUWE no Gaia DR3.
* **Por que não rodar agora:** As regras do laboratório proíbem baixar gigabytes de catálogos astronômicos e rodar ajustes empíricos sem travar o modelo nulo e os cortes a priori.
* **O que fazer para desbloquear:**
  1. Redigir `05_DISCOVERY_LAB/02_TESTS/COSMOLOGY_GAIA_MCMC/PREREGISTRATION.md`.
  2. Fixar o modelo de mistura para binárias não resolvidas e o corte de RUWE $< 1.4$.
  3. Criar o script de amostragem hierárquica MCMC em CUDA usando **NumPyro / JAX** na RTX 5090.
  4. Adicionar à fila do daemon.

---

### Bloco B — Bloqueadas por Dependência de Hardware Físico ou Dados Clínicos

#### Linha J — Limite Quântico-Clássico e Massa Crítica $M_c$
* **Diagnóstico Atual (`PROJECT_STATE.json`):** Congelada formalmente com estado `PAUSED_PENDING_HARDWARE_AND_METROLOGY`. O parâmetro $M_c = 5.292674 \times 10^{-16}\text{ kg}$ é uma hipótese matemática sem calibração física.
* **Bloqueio:** Qualquer inferência sem dado experimental real é categoricamente proibida pelo protocolo de integridade do laboratório.
* **O que fazer para desbloquear:** Obter parcerias com laboratórios de interferometria de matéria macroscópica (ex.: optomecânica de levitação óptica) e importar dados brutos de séries temporais de decoerência calibrados.

#### Linha K & L — Ecossistemas Cognitivos, EEG e Cibernética Híbrida
* **Diagnóstico Atual:** O teste pré-registrado de depressão (`DISC-COGNITIVE-EEG-001`) foi refutado (a entropia espectral foi maior, contradizendo a teoria). O braço de ansiedade depende de repositórios médicos com autenticação institucional que um daemon não pode acessar automaticamente.
* **Bloqueio:** Falta acesso automatizado a dados clínicos brutos (.EDF) abertos e falta definição operacional estrita para o parâmetro $C_{bio}$.
* **O que fazer para desbloquear:** Mapear bases abertas no Zenodo/PhysioNet sem restrição de credencial e formular um pré-registro focando exclusivamente em bandas de potência com teste de hipótese bicaudal.

---

### Bloco C — Bloqueadas por Ausência de Sistema de Equações Diferenciais Fechado

#### Linhas A & B — Fundamentos, Geometria da Informação e Axiomas
* **Diagnóstico Atual:** O arquivo possui tratados extensos e vocabulário conceitual ("rede informacional", "espaço de estados $S_i$", "evolução $P_i$"), mas **não possui uma ação variacional covariante mínima** ($S = \int d^4x \sqrt{-g} \mathcal{L}$).
* **Bloqueio:** Sem um funcional de ação ou equação de movimento fechada, o computador não tem o que integrar numericamente ou provar analiticamente.
* **O que fazer para desbloquear:** Reduzir o texto conceitual a um modelo discreto de rede (ex.: matrizes de adjacência com dinâmica de dissipação formulada como cadeia de Markov ou equação de Lindblad unidimensional) e testar a emergência de métrica efetiva.

#### Linhas H & O — Buracos Negros, Bounces Entrópicos e Engenharia Métrica
* **Diagnóstico Atual:** Propõe que a saturação holográfica (limite de Bekenstein) gera uma repulsão que substitui a singularidade por um "Bounce" cósmico.
* **Bloqueio:** Falta um tensor de energia-momento $T_{\mu\nu}$ que satisfaça as identidades de Bianchi ($\nabla_\mu T^{\mu\nu} = 0$) e evite instabilidades fantasma (*ghost instabilities*).
* **O que fazer para desbloquear:** Formular um modelo gravitacional $f(R)$ ou escalartensor com acoplamento não-mínimo concreto onde o bounce ocorra de forma estável, permitindo a integração de equações de Friedmann modificadas.

#### Linha M — Estabilidade de Operadores e Leue Horizon (ROC/LMC/ROA)
* **Diagnóstico Atual:** Proposta de estimadores de margem espectral para prevenir divergências em dinâmica de fluidos e sistemas dinâmicos.
* **Bloqueio:** Não há definição explícita do espaço de Hilbert/Sobolev onde o operador atua, nem demonstração de coercividade.
* **O que fazer para desbloquear:** Delimitar o problema para uma equação diferencial comum (EDO) não-linear simples de dimensão 2 ou 3 (ex.: atrator de Lorenz ou equação de Duffing) e provar a função de Lyapunov via SOS (*Sum of Squares*) em SymPy.

---

### Bloco D — Fechadas / Refutadas que Exigem Nova Teoria do Zero

#### Linha C — Teoria da Incompatibilidade (TRI) e TDTR
* **Diagnóstico Atual:** Fechada como `CLOSED_NULL` em `FAILED_HYPOTHESES.md`. Testou 16 candidatos matemáticos em 5 fases cruzando dados geofísicos, médicos e financeiros. Todos os 16 caíram sob replicação adversarial.
* **Bloqueio:** Não restou nenhum candidato a invariante cross-domain com sustentação empírica.
* **O que fazer para desbloquear:** Abandonar a busca de invariantes universais empíricos em séries temporais arbitrárias e restringir a teoria a sistemas termodinâmicos estritamente hamiltonianos com acoplamento a banho térmico.

#### Linha I — Física de Partículas e Modelos de Nós
* **Diagnóstico Atual:** A relação numérica $\sin^2\theta_W = 3/13$ errou os dados do PDG por mais de $7.5\sigma$, e a fórmula de massa de quarks via invariantes de nós falhou no teste de validação cruzada.
* **Bloqueio:** As fórmulas originais eram ajustes numéricos pós-hoc sem simetria de gauge preservada.
* **O que fazer para desbloquear:** Somente se for formulada uma teoria quântica de campos de gauge com representação geométrica que reproduza os diagramas de Feynman e a quebra de simetria eletrofraca padrão.

---

## 4. Ordem Recomendada de Ataque para o Usuário

Quando você decidir trabalhar manualmente para desbloquear as próximas frentes, siga esta ordem de maior viabilidade para menor:

1. **Passo 1 (Mais fácil — 1 a 2 dias):** Pré-registrar a **Linha G (Cosmologia MCMC)**. Criar o `PREREGISTRATION.md` com modelo de multiplicidade para binárias do Gaia DR3 e plugar o script no daemon da 5090.
2. **Passo 2 (Intermediário — 1 semana):** Formalizar um modelo restrito da **Linha M (Estabilidade)**. Escolher um oscilador não-linear simples e usar o SymPy para buscar funções de Lyapunov polinomiais certificadas.
3. **Passo 3 (Teórico profundo — médio prazo):** Desenvolver um modelo de brinquedo (*toy model*) de Lindblad para a **Linha C/A**, testando relaxação de semigrupos irreversíveis em redes finitas de 10 a 50 nós.
