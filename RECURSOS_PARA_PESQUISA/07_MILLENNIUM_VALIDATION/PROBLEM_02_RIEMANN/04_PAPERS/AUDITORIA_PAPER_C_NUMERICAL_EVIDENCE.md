# Auditoria — Document C: Numerical Evidence

**Status:** needs_data  
**Classificação:** simulação de ensemble; não é teste dos zeros da zeta (S1/E)

## Veredicto

Gerar matrizes hermitianas GUE e observar a distribuição de Wigner confirma que o código reproduz a propriedade do ensemble escolhido. Isso não fornece evidência independente sobre `ζ`, pois o GUE já impõe repulsão por construção.

## Lacunas decisivas

- não são analisados zeros calculados da zeta;
- não há especificação de unfolding, janela, semente, incerteza ou tamanho efetivo;
- não há comparação com ensembles nulos (Poisson, GOE, matrizes estruturadas);
- não há correção para múltiplas estatísticas ou seleção pós-hoc.

## Próximo teste

Usar tabelas independentes de zeros, pré-registrar a janela e a estatística, comparar vários nulos e disponibilizar código/dados. Reportar intervalos de confiança e análise de robustez a diferentes métodos de unfolding.

## Fontes

- [Odlyzko — tabelas de zeros](https://www-users.cse.umn.edu/~odlyzko/zeta_tables/)
- [NIST DLMF §25](https://dlmf.nist.gov/25)
- [Clay Mathematics Institute — RH permanece problema aberto](https://www.claymath.org/millennium/Riemann-Hypothesis/)
