# Auditoria — Candidato U₁/₂

**Status:** revised  
**Nível global:** H1 — resultado analítico/computacional dentro de uma família de mapas; não é ainda uma classe física estabelecida

## Pergunta auditável

Para quais famílias de mapas finitos, perturbações e observáveis a fração de elementos em ciclos converge para `φ(c)=(1+c)^−1/2`, e essa convergência é robusta a mudanças admissíveis do mecanismo?

## Correções aplicadas

- “Discovery/confirmation” foi substituído por “candidate/proposed” quando o texto extrapolava o modelo.
- Separado expoente de escalamento do modelo U₁/₂ de uma classe de universalidade física.
- Incluída a exigência de limite assintótico, robustez de perturbação e comparação com classes conhecidas.
- Adicionadas referências a Wilson e Cardy para ancorar o uso de universalidade em física estatística.

## Problemas encontrados

1. A afirmação de independência da “specific construction” exige uma definição explícita da classe de construções e uma prova, não apenas tabelas numéricas.
2. Quatro valores de `n=2000` não demonstram limite `n→∞` nem erro estatístico completo.
3. O texto alterna `α` e `γ` para o mesmo expoente; a notação deve ser unificada.
4. A comparação com GUE, percolação e Ising mistura observáveis e mecanismos; expoentes só são comparáveis quando a grandeza e a normalização são equivalentes.
5. “Computational universality class” é uma proposta taxonômica, não um resultado que possa ser promovido por ajuste.

## Próximo teste

Definir formalmente a família de perturbações, provar ou demonstrar numericamente a convergência com controle de tamanho finito, estimar incerteza por réplicas independentes e testar famílias adversariais. Comparar a função inteira `φ(c)`, não somente o expoente ajustado.

## Fontes verificadas

- Wilson (1975), [grupo de renormalização e fenômenos críticos](https://doi.org/10.1103/RevModPhys.47.773).
- Cardy (1996), *Scaling and Renormalization in Statistical Physics*.
- Flajolet & Odlyzko (1989), estatística de mapas aleatórios, referência citada no artigo.
