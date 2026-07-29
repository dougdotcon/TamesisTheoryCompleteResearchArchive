# Auditoria rigorosa — The Cusp Contribution

Data: 2026-07-29  
Status: análise candidata da contribuição contínua.

## Achados

O fator de espalhamento para a superfície modular é explícito, mas a atribuição do crescimento $T\log T$ exige a fórmula de traço completa, incluindo espectro discreto, termo identidade e contribuição contínua. Devem ser fixados normalização, ramo de $\arg$, singularidades e resto uniforme.

## Teste reproduzível

Derivar a contagem espectral a partir da fórmula de Selberg para funções-teste admissíveis; fornecer notebook que compare cada termo e reproduza a constante líder em uma faixa de $T$. Separar erro numérico de erro analítico.

## Fontes

- Iwaniec, *Spectral Methods of Automorphic Forms*, referência de traço e espalhamento.
- NIST DLMF, [Gamma asymptotics](https://dlmf.nist.gov/5.11) e [zeta function](https://dlmf.nist.gov/25).
