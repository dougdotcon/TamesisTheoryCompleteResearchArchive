# Auditoria — Spectral Geometry / Riemann Hypothesis

**Data:** 2026-07-30  
**Classificação:** hipótese matemática-física; ilustração estatística, não demonstração.

## Veredito

O texto combina a conjectura de Berry–Keating, a correspondência heurística entre zeros e espectros e uma leitura holográfica do vácuo. A estatística GUE dos espaçamentos normalizados é compatível com observações conhecidas, mas não implica que todos os zeros estejam na linha crítica, muito menos que exista o operador auto-adjunto proposto. A página deve substituir “proof/deriving” por “spectral ansatz” e separar dado calculado, hipótese e consequência condicional.

## Lacunas verificáveis

- definir domínio, medida, domínio auto-adjunto e espectro do operador `H`;
- demonstrar que o espectro coincide com **todos** os zeros, com multiplicidades e controle de erros;
- especificar a janela de zeros, o unfolding, a semente e o código da simulação;
- comparar GUE, Poisson e modelos alternativos fora da amostra usada;
- não usar holografia ou unitariedade como argumento para fixar `Re(s)=1/2` sem um teorema que conecte esses axiomas à zeta.

## Próximo teste / falsificação

Publicar dados e código cegos, repetir em várias janelas de altura e registrar o poder estatístico. A proposta falha se o operador não for auto-adjunto, se perder zeros conhecidos ou se a estatística não superar um modelo nulo pré-especificado.

## Fontes primárias

- [Clay Mathematics Institute — Riemann Hypothesis](https://www.claymath.org/millennium/riemann-hypothesis/)
- [NIST Digital Library of Mathematical Functions — zeta function](https://dlmf.nist.gov/25)
- [Odlyzko — tables of zeros and spacings](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/)
