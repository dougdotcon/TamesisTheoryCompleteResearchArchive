---
document_id: RT-NOVELTY-BOUNDARY
mathematical_novelty: NONE
algorithmic_novelty: NONE
---

# Fronteira de novidade

## Registro literal

```text
Representar uma maquina de estados por uma tabela finita, validar seus
destinos e construir uma funcao sobre Fin n eh engenharia formal padrao.

O resultado pretendido nao eh um novo algoritmo.

O valor esta em:

- receber dados dinamicos;
- rejeitar dados invalidos sem correcao silenciosa;
- construir internamente um dominio finito tipado;
- reutilizar um detector ja formalmente verificado;
- devolver certificados interpretaveis sobre a tabela original;
- preparar uma futura interface nativa.
```

## Classificação

```yaml
mathematical_novelty: NONE
algorithmic_novelty: NONE
research_role: FORMAL_SOFTWARE_BRIDGE
```

## Proibido afirmar

```text
novo algoritmo;
nova teoria de automatos;
nova maquina de estados;
descoberta matematica;
resultado fisico;
TRI; TDTR; TOE; problema Clay.
```

## O que é, honestamente

Uma tabela de transições é a representação mais antiga e mais banal de um
autômato determinístico. Validar que cada destino está no domínio é uma
verificação de limites. Construir `Fin n → Fin n` a partir dela é uma
aplicação de tipos dependentes que qualquer texto de Lean cobre.

Nada disso é novo. O que a frente acrescenta é **conectar** essas três
banalidades a um detector cuja correção e completude já são teoremas, e
provar que a conexão preserva a dinâmica.

## A distinção que importa

```text
FOUND-CYCLE-DETECTION-001    o programa esta correto
ENG-FINITE-STATE-RUNTIME-001 o programa aceita o SEU dado, e continua correto
```

A segunda não é matemática nova. É a diferença entre um teorema e uma
ferramenta.

## A ressalva que a frente não pode apagar

```text
converter um sistema real para uma tabela finita eh uma ABSTRACAO;
a correcao dessa abstracao NAO eh fornecida por esta frente.
```

O adaptador garante que **a tabela dada** é analisada corretamente. Que a
tabela **represente** o sistema real é responsabilidade de quem a
produziu. `RT-GAP-017` permanece aberto, e provavelmente permanecerá:
provar essa correspondência exigiria um modelo formal do sistema real, o
que está fora de qualquer escopo previsível deste laboratório.

## Reutilização em software

Pela quinta vez neste laboratório, e continua verdadeiro:

```text
A reutilizacao em software NAO transforma o resultado matematico padrao
em descoberta cientifica.
```
