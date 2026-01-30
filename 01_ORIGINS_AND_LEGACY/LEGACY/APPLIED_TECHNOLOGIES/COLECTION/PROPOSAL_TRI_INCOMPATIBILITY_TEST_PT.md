# PROPOSTA DE EXPERIMENTO DE LIMITE: O Teste de Incompatibilidade (TRI)

**Objetivo:** Testar se a **Teoria da Incompatibilidade de Regimes (TRI)** é uma lei física real ou apenas filosofia. Isso validará (ou matará) a base da Topologia Cognitiva.

## 1. O Risco (O que está em jogo)

Você está preocupado que a **Topologia Cognitiva** (Diagnósticos como "Armadilha Entrópica") seja um salto especulativo.
Essa parte da teoria depende de uma premissa: **O cérebro obedece às mesmas restrições de fase que a matéria.**
Se TRI for falsa (se regimes incompatíveis puderem se misturar livremente), então toda a classificação de doenças mentais da Tamesis desmorona.

## 2. A Hipótese de TRI (O "No-Go Theorem")

TRI afirma que **Lógica Rígida (Classe A)** e **Criatividade Caótica/Busca (Classe B)** são matematicamente ortogonais.

* **Previsão Tamesis:** Uma única rede neural monolítica (conectividade densa, homogênea) **NÃO CONSEGUE** aprender tarefas Classe A e Classe B simultaneamente com alta performance.
* **Consequência:** Para resolver ambas, a rede deve sofrer **Quebra Espontânea de Simetria** e se dividir em dois módulos (Topologia Modular). Se ela não se dividir, ela falha (Catastrophic Forgetting ou Performance Medíocre).

## 3. O Experimento: "A Tortura da Rede" (Python)

Construímos uma Rede Neural simples, mas a forçamos a servir dois mestres incompatíveis:

1. **Tarefa A (O Bibliotecário - Classe A):** Memorizar uma tabela de hash exata (Entrada X -> Saída Y arbitrária). Exige *overfitting*, memorização rígida, ruído zero.
2. **Tarefa B (O Poeta - Classe B):** Generalizar funções contínuas suaves ou prever séries temporais caóticas. Exige *suavização*, tolerância a ruído, regularização.

**O Teste:**
Treinamos a rede com uma função de perda combinada: $L = \alpha L_A + \beta L_B$.

### Critério de Falsificação (Como provar que Tamesis está ERRADA)

* **Se** a rede densa padrão resolver A e B perfeitamente sem mudar sua topologia interna...
* **ENTÃO** TRI é falsa. Regimes podem coexistir. A base física da sua teoria mental cai.

### Critério de Validação (Como provar que Tamesis está CERTA)

* **Se** a rede falhar consistentemente OU...
* **Se** observarmos (visualizando os pesos) que a rede espontaneamente "desliga" conexões transversais, criando duas sub-redes isoladas (um "Hemisfério Esquerdo" e "Direito")...
* **ENTÃO** TRI é uma restrição real. A modularidade não é uma escolha de design, é uma necessidade termodinâmica.

## 4. Por que isso valida a Topologia Cognitiva?

Se provarmos que redes *precisam* se dividir para lidar com a complexidade do mundo (A vs B), então "Doenças Mentais" passam a ser vistas como falhas nessa divisão:

* **Depressão:** A rede ficou muito rígida (Excesso de Classe A, matou B).
* **Mania:** A rede ficou muito fluida (Excesso de Classe B, matou A).
* **Esquizofrenia:** A divisão (Barreira de Regimes) quebrou, e A e B estão vazando um no outro (alucinação lógica).

**Conclusão:** Este código testa se a "Esquizofrenia Artificial" ocorre quando violamos TRI. É o teste definitivo de limite.
