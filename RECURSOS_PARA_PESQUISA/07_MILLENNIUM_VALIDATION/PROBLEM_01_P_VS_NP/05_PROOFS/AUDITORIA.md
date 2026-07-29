# Auditoria — P versus NP

**Status:** needs_data  
**Nível global:** S1/H1 — modelo físico proposto; não resolve P versus NP em ZFC

## Veredicto

O texto confunde uma possível separação em um modelo de computação fisicamente limitado com a questão matemática clássica. Um custo termodinâmico não implica, sem axiomas formais, que nenhum algoritmo polinomial resolva SAT ou outro problema NP-completo.

## Lacunas

- o modelo `P_phys` não está definido como classe de linguagens;
- o passo Talagrand → tempo de leitura → impossibilidade computacional não é demonstrado;
- as barreiras de relativização, natural proofs e algebrização não são removidas por citar um modelo físico;
- simulações não provam uma afirmação assintótica universal.

## Próximo teste

Definir formalmente recursos, ruído, precisão e acesso à entrada; provar um limite inferior para uma classe de máquinas e declarar se a conclusão é sobre `P_phys` ou sobre `P`/`NP`. O Clay mantém P versus NP entre os problemas em aberto ([problemas do milênio](https://www.claymath.org/millennium-problems/), [regras](https://www.claymath.org/millennium-problems/rules/)).
