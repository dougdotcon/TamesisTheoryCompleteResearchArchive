---
document_id: ENC-RESULT-BOUNDARY
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
---

# Fronteira do resultado

## Será formalizado

```text
CertifiedFiniteEncoding, com duas leis inversas;
encode injetiva;
encodedStep, total por construcao;
buildTransitionTable, por Array.ofFn;
o teorema de tamanho, em orientacao unica;
o lema central de leitura;
tableIndex, ponto unico de transporte;
tableIndex_val, o teorema anti-correcao;
a comutacao de um passo;
a semiconjugacao;
a comutacao de iteradas;
a correspondencia com run?;
analyzeEncodedSystem;
soundness com igualdade em S;
completeness sem pre-condicoes;
a impossibilidade dos erros;
oito testes executaveis.
```

## NÃO será formalizado

```text
minimalidade de baseIndex ou period;
unicidade do witness;
invariancia do witness sob mudanca de codificacao;
independencia da ordem de busca do detector;
totalizacao do detector;
Floyd, Brent, tabela visitada;
modelo de custo ou complexidade;
extracao, CLI, parser, JSON, IO, rede;
correcao da abstracao de sistemas externos no caso geral;
correcao de servico, programa, workflow, agente ou processo fisico;
seguranca ou terminacao de sistemas reais;
qualquer Problema do Milenio;
evidencia fisica;
novidade matematica ou algoritmica.
```

## A fronteira semântica, literal e vinculante

```text
O runtime adapter prova que uma tabela fornecida eh analisada
corretamente.

A nova frente devera provar que uma tabela construida a partir de uma
codificacao certificada corresponde ao sistema formal tipado que
forneceu essa codificacao.

Um certificado pode ser correto sobre uma tabela e, ainda assim, nao
sustentar uma conclusao sobre um sistema externo pretendido caso a
tabela tenha sido produzida por uma codificacao incorreta.

A nova frente elimina esse risco apenas para sistemas formais
acompanhados de codificacao certificada.

Ela nao prova que um servico, programa, workflow, agente, processo
fisico ou sistema externo real foi modelado corretamente.
```

## Relação com `RT-GAP-017`

```yaml
relationship_to_RT_GAP_017:
  status: ADDRESSED_FOR_CERTIFIED_TYPED_SYSTEMS_ONLY
  runtime_item_modified: false
  general_external_system_case: OPEN
```

`RT-GAP-017` **não** é alterado retroativamente. Ele permanece
`OPEN_DEFERRED` no registro da frente anterior, e nenhum arquivo daquela
frente é tocado.

## O que o laboratório passa a ter

```text
uma cadeia que comeca em um objeto Lean tipado e termina em um
certificado interpretado NESSE objeto,
passando por um Array Nat que ela mesma constroi e prova correto.
```

E o que continua faltando, dito sem rodeio: **de onde vem o objeto
tipado**. Essa pergunta pertence a quem modela o sistema, e nenhuma
frente formal a responde por ele.


---

## Revisão — `2066edc`

Fronteira **inalterada**. Acrescentado um limite explícito:

```yaml
encoding_invariance_of_concrete_witness:
  status: OPEN_DEFERRED
  gap: ENC-GAP-020
```

A validade **semântica** do witness no sistema tipado é preservada por
qualquer codificação correta — isso é `analyzeEncodedSystem_sound`. Não
foi provado que duas codificações diferentes produzam o mesmo `Array`, o
mesmo `baseIndex`, o mesmo `period` ou o mesmo primeiro witness segundo a
ordem da busca.
