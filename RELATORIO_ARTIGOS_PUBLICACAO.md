# Relatório de inventário e publicação

Data da consolidação: 29 de julho de 2026.

## Escopo

O inventário exclui somente artefatos gerados em `04_FORMAL_RESEARCH_LAB/**` e dependências internas em `.lake/**`. Os documentos formais foram preservados em seu estado original, conforme as instruções do laboratório.

Para evitar contar README, roadmap, status, logs e relatórios como artigos, um Markdown foi tratado como manuscrito quando o nome contém `paper`, `article`, `treatise`, `thesis`, `preprint`, `manuscript` ou `essay`, ou quando está em uma pasta explicitamente editorial (`PAPERS`, `TREATISES`, `ARTICLES` ou `PREPRINTS`).

## Contagem

| Categoria | Quantidade |
|---|---:|
| Arquivos Markdown no repositório (fora `.lake`) | 898 |
| Markdown protegidos no laboratório formal | 111 |
| Markdown identificados como manuscritos | 41 |
| Markdown convertidos para HTML | 41 |
| HTML existentes antes da conversão | 251 |
| HTML após a conversão | 292 |
| HTML identificados como artigos/artefatos de artigo | 280 |
| Títulos HTML únicos (indicativo, antes de revisão editorial) | 248 |
| Artigos canônicos correspondentes ao Zenodo | 7 |
| Artigos locais ainda na fila de publicação | 273 |

A contagem principal é por arquivo editorial. O arquivo também contém versões históricas e duplicatas; por isso, 280 arquivos correspondem a 248 títulos HTML distintos.

## Registros Zenodo fornecidos

| Registro informado | Correspondência local | Situação |
|---|---|---|
| *The Computational Architecture of Reality: A Unified Theory of Emergent Physics* — DOI `10.5281/zenodo.18407409` | Arquitetura computacional Tamesis | Publicado/localizado |
| *Global Regularity of 3D Navier-Stokes via the Alignment Gap Mechanism* | Paper Navier–Stokes | Publicado/localizado |
| *The Physical Resolution of the Riemann Hypothesis via Spectral Entropy and Thermodynamic Stability* | Paper Riemann | Publicado/localizado |
| *The Resolution of the P vs NP Problem: Algorithmic Entropy and Thermodynamic Censorship* | Paper P vs NP | Publicado/localizado |
| *Structural Realizability of Algebraic Cycles: The Resolution of the Hodge Conjecture* | Paper Hodge | Publicado/localizado |
| *A Proof of the Birch and Swinnerton-Dyer Conjecture for all Elliptic Curves over the Field of Rational Numbers* | Paper BSD/Iwasawa | Publicado/localizado |
| *A Formal Proof of the Yang-Mills Mass Gap: Synthesizing Balaban's UV Stability with Infrared Spectral Coercivity* | Paper Yang–Mills | Publicado/localizado |
| *The Ontological Censor: Why Physical Reality Rejects Mathematical Pathologies* | Nenhuma correspondência local inequívoca | Manuscrito local ausente |
| *The Sator Square as a Zero-Entropy Symbolic Structure* | Nenhuma correspondência local inequívoca | Manuscrito local ausente |
| *Orbit-Induced Redundancy in Finite Symbolic Systems* | Nenhuma correspondência local inequívoca | Manuscrito local ausente |

## Pastas de saída

- [`publicados/`](/D:/TamesisTheoryCompleteResearchArchive/publicados): sete arquivos canônicos associados aos registros Zenodo localizados, mantendo sua hierarquia original.
- [`publicar/`](/D:/TamesisTheoryCompleteResearchArchive/publicar): 273 arquivos de artigo ainda não associados a um registro Zenodo confirmado.
- Cada pasta contém uma cópia de [`paper-layout.css`](/D:/TamesisTheoryCompleteResearchArchive/paper-layout.css), portanto os links de estilo continuam funcionando dentro das cópias.

Os arquivos-fonte Markdown permanecem no local original; as versões HTML convertidas foram criadas ao lado deles e incluídas na fila editorial.
