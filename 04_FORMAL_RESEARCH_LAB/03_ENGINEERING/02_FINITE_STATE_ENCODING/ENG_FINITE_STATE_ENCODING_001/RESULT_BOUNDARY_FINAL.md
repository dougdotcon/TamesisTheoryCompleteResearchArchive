---
document_id: ENC-RESULT-BOUNDARY-FINAL
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
---

# Fronteira final do resultado

```text
Foi formalizado:

- codificacao finita certificada fornecida;
- encode e decode com duas leis inversas;
- injetividade de encode;
- passo codificado;
- construcao computavel de uma unica tabela validada;
- validade estrutural por construcao;
- tamanho da tabela;
- dois pontos controlados de transporte;
- preservacao do valor natural do indice;
- semiconjugacao;
- comutacao de um passo;
- comutacao de iteradas;
- correspondencia com run?;
- API dinamica tipada;
- soundness terminando em igualdade sobre S;
- completeness sem pre-condicoes;
- exclusao universal de erros;
- testes, computabilidade e axiomas.

Nao foi formalizado:

- toEquiv;
- consequencias opcionais de bijetividade;
- invariancia do witness concreto sob recodificacao;
- minimalidade ou unicidade;
- modelo de custo;
- benchmark;
- extracao;
- CLI;
- parser;
- JSON;
- rede;
- integracao;
- correcao de um sistema externo especifico;
- novidade matematica ou algoritmica.
```

## A fronteira semântica, literal

```text
Um CycleWitness produzido para uma tabela correta eh um certificado
correto sobre essa tabela.

Uma codificacao incorreta nao torna falso o certificado sobre a
tabela; ela impede apenas que ele sustente uma conclusao sobre o
sistema que se pretendia representar.

ENG-FINITE-STATE-ENCODING-001 prova correspondencia somente para
sistemas formais tipados acompanhados de encode, decode e leis de
inversao verificadas.

A frente nao prova que um programa, servico, workflow, agente,
processo fisico ou sistema externo foi corretamente modelado.
```

```yaml
relationship_to_RT_GAP_017:
  status: ADDRESSED_FOR_CERTIFIED_TYPED_SYSTEMS_ONLY
  runtime_item_modified: false
  general_external_system_case: OPEN
```

`RT-GAP-017` não foi alterado, e nenhum arquivo da frente anterior foi
tocado.

## O que o laboratório passou a ter

```text
uma cadeia que comeca em um objeto Lean TIPADO e termina em um
certificado interpretado NESSE objeto, passando por um Array Nat que
ela mesma constroi e prova correto.
```

A frente anterior provava algo sobre a tabela. Esta prova algo sobre a
**relação** entre a tabela e o sistema. A diferença está no enunciado
final: `stepS^[b + p] start = stepS^[b] start`, em `S`.

E o que continua faltando, dito sem rodeio: **de onde vem o objeto
tipado**. Essa pergunta pertence a quem modela o sistema, e nenhuma
frente formal a responde por ele.

## Valor registrado

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

Codificar um tipo finito como `Fin n` é rotina desde os anos 1950.
Nenhum algoritmo novo, nenhum resultado novo de teoria de autômatos,
nenhum modelo universal, nenhuma correção automática de sistemas
externos, nenhuma afirmação sobre segurança de workflows, nenhum
problema matemático aberto, nenhuma evidência física.
