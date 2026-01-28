# PESQUISAS.MD: Análise Tática para o Roadmap Navier-Stokes

## 🧭 Visão Geral: O Que Estamos Buscando

Nosso objetivo no `ROADMAP_NAVIER_STOKES.md` é estabelecer a **Censura Termodinâmica do Blow-up**. Diferente da abordagem matemática pura, que busca contra-exemplos exóticos, nossa tese é física: a viscosidade atua como um mecanismo de "apagamento de informação" que censura a formação de singularidades (concentração infinita de informação) em tempo finito.

Filtragem estratégica da literatura:

1. **Cemitério (Tentativas Falhas):** A busca por regularidade via estimativas de Sobolev (Leray) e a busca por blow-up em Euler (Hou-Luo).
2. **Espelhos (Abordagens Adjacentes):** A "Integração Convexa" que constrói soluções "selvagens" (matematicamente válidas, fisicamente falsas).
3. **Arsenal (Ferramentas Locais):** O defeito de Duchon-Robert e a Intermitência como provas da censura viscosa.

---

## 💀 TIPO 1: Tentativas Sérias que Falharam (E Onde Exatamente Quebraram)

*Por que a análise clássica travou no "Gap de Regularidade".*

### 1.1 O Programa de Leray (1934) e Sobolev

* **A Tentativa:** Provar regularidade global controlando a norma de energia ($L^2$) e enstrofia ($H^1$).
* **Onde Quebrou:**
  * **Subcrítico vs Supercrítico:** Em 3D, a equação é supercrítica. A transferência de energia para escalas pequenas ($k \to \infty$) acontece mais rápido do que a viscosidade consegue dissipar *nas estimativas de pior caso*.
  * **Falha de Controle:** Leray provou a existência de "Soluções Fracas", mas não conseguiu garantir que elas não explodem (perda de unicidade/regularidade).
* **Lição para o Roadmap:**
  * ❌ **Não tentar:** Melhorar as desigualdades de Sobolev "hard" (BKM, Prodi-Serrin). Isso é um muro analítico.
  * ✅ **Fazer:** Focar na **Termodinâmica**. O "pior caso" de Sobolev ignora a direção do tempo. A viscosidade proíbe o reagrupamento de energia necessário para o blow-up.

### 1.2 O Blow-up de Euler (Hou-Luo, Elgindi)

* **A Tentativa:** Mostrar que fluídos invíscidos (Euler) explodem em tempo finito.
* **Onde (Quase) Funcionou:**
  * Hou e Luo (e provas de Elgindi) mostraram que, sem viscosidade, a vorticidade pode ir para o infinito em pontos de estagnação hiperbólicos (fronteira).
* **Por que falha para Navier-Stokes (Nossa Tese):**
  * Em Euler, o mecanismo de estiramento de vórtices ganha da advecção.
  * Em Navier-Stokes, ao se aproximar da escala de singularidade ($\ell \to 0$), o termo viscoso $\nu \Delta u$ ($ \sim 1/\ell^2$) domina o termo não-linear advectivo ($ \sim 1/\ell$).
* **Lição para o Roadmap:**
  * O blow-up de Euler é o "fantasma" que queremos exorcizar. Ele mostra o que o sistema *quer* fazer, mas a viscosidade é o agente censor que impede a conclusão do processo.

---

## 🌌 TIPO 2: Abordagens Estruturais Adjacentes (O Mesmo Espírito)

*Modelos que mostram o perigo de ignorar a física.*

### 2.1 Conjectura de Onsager e Integração Convexa (De Lellis, Székelyhidi, Buckmaster)

* **Conceito:** Construção de soluções "selvagens" (wild solutions) que dissipam energia mesmo sem viscosidade (Euler dissipativo) ou que violam a unicidade em Navier-Stokes.
* **Conexão com o Roadmap:**
  * Essas soluções são construídas iterativamente adicionando oscilações (Mikado flows). Elas são matematicamente corretas, mas fisicamente suspeitas (podem "criar" energia do nada se não restritas).
  * Elas provam que a formulação fraca padrão é **muito permissiva**.
  * Nossa estratégia é fechar essa porta: impor a **Desigualdade de Entropia** (Duchon-Robert) como lei fundamental para excluir essas singularidades artificiais.

### 2.2 Regularidade Parcial (Caffarelli-Kohn-Nirenberg - CKN)

* **Conceito:** O conjunto de pontos singulares no espaço-tempo tem dimensão unidimensional nula ($\mathcal{P}^1(S) = 0$).
* **Conexão com o Roadmap:**
  * Isso já é quase a prova. Diz que singularidades, se existirem, são eventos extremamente raros e esparsos ("pó" no espaço-tempo).
  * Nós vamos além: afirmamos que a medida é zero não por sorte matemática, mas porque manter uma singularidade custa entropia infinita.

---

## 🛠️ TIPO 3: Ferramentas Técnicas Locais (O Arsenal)

*Componentes para o `PAPER_B_STRUCTURAL_NO_GO`.*

### 3.1 O Defeito de Duchon-Robert

* **Origem:** Análise (2000).
* **Uso Tático:**
  * A equação de balanço de energia local: $\partial_t E + \nabla \cdot J = -D(u) - \nu |\nabla u|^2$.
  * $D(u)$ é o "defeito", a anomalia dissipativa.
  * Se houver blow-up (singularidade de Onsager), $D(u) > 0$.
  * Nossa tese: Para Navier-Stokes com $\nu > 0$, o termo viscoso $\nu |\nabla u|^2$ satura a produção de entropia, forçando $D(u) = 0$. A viscosidade "rouba" a energia necessária para alimentar o defeito.

### 3.2 Intermitência e Multifractais

* **Origem:** Frisch, Parisi (Turbulência K41/K62).
* **Uso Tático:**
  * A dissipação não é uniforme, é concentrada em fractais.
  * Isso explica por que as estimativas médias (Sobolev) falham: elas não veem a concentração extrema.
  * Porém, a intermitência física tem limites. A dimensão dos vórtices não pode descer abaixo de um certo limiar crítico sem violar a conservação de massa/momento.

### 3.3 Propriedade de Semigrupo (Irreversibilidade)

* **Origem:** Dinâmica de Sistemas.
* **Uso Tático:**
  * Navier-Stokes é um semi-grupo difusivo ($e^{t\Delta}$).
  * Operadores difusivos regularizam (suavizam) em tempo infinitesimal ($t > 0$).
  * Um blow-up em tempo finito exige que o sistema "desfaça" a difusão para concentrar massa em um ponto. Isso viola a seta do tempo termodinâmica do operador.

---

## 📉 Síntese para o Roadmap

O `GUN-NS` reestruturado clarifica a batalha:

1. **Não lutar contra a Matemática Pura:** Aceitamos que soluções fracas "selvagens" (Tipo 2.1) existem no papel.
2. **Impor a Física:** Usamos a **Desigualdade de Duchon-Robert (Tipo 3.1)** e a **Irreversibilidade (Tipo 3.3)** para selecionar as soluções físicas.
3. **O Veredito:** O Blow-up é uma tentativa do fluido de acessar o regime de Euler (Tipo 1.2), mas é censurado pela viscosidade, que dissipa a energia do "gatilho" antes que a singularidade se forme.

**Próxima Ação:** Detalhar no `PAPER_B` como a viscosidade atua como um "Cutoff Dinâmico" que se move mais rápido que a formação da singularidade.

---

### Referências Selecionadas

* **Leray (1934):** *Sur le mouvement d'un liquide visqueux.* (A Base)
* **Caffarelli, Kohn, Nirenberg (1982):** *Partial Regularity.* (O Limite Atual)
* **Duchon, Robert (2000):** *Inertial Energy Dissipation.* (A Ferramenta de Entropia)
* **Hou, Luo (2014):** *Potentially Singular Solutions to Euler.* (O Inimigo)
* **De Lellis, Székelyhidi (2010+):** *Convex Integration / h-principle.* (As Soluções Selvagens)
* **Buckmaster, Vicol (2019):** *Non-uniqueness of Navier-Stokes.* (A Fronteira "Wild")
