---
document_id: PORTFOLIO-REVIEW-COST-MODEL-2026-08-04
reviewed_at: 2026-08-04
selected_work_item: ENG-RUNTIME-SOUNDNESS-002
cost_model_probe_exit: 0
cost_model_exists_in_toolchain: true
---

# Revisao de portfolio — o modelo de custo, medido

## O que foi medido, e corrige o que eu disse

Antes desta medicao eu afirmei ao operador que **escolher um modelo de
custo e decisao de portfolio, nao descoberta**. A parte "nao e
descoberta" continua certa. A parte que ficou incompleta e que a opcao
concreta nunca tinha sido **procurada no toolchain**.

Procurada agora, por elaboracao, `exit 0`:

```text
Turing.FinTM2                          ELABORA
Turing.TM2OutputsInTime                ELABORA
Turing.TM2ComputableInTime             ELABORA
Turing.TM2ComputableInPolyTime         ELABORA
Turing.idComputableInPolyTime          ELABORA
```

**O Mathlib tem modelo de custo.** `CB-GAP-002` e `UP-GAP-001` dizem que
custo exige comprometer-se com um modelo de maquina — isso continua
verdadeiro, e `TM2ComputableInPolyTime` **e** esse compromisso, ja
formalizado.

Era um quase-Bochner: nao teoria ausente, e sim nome nao procurado. A
proibicao de 2026-08-04 — *nao declarar teoria ausente sem tentar
elaborar* — pegou este caso a tempo.

## E o preco, tambem medido

```text
TM2ComputableInPolyTime   Type 1, nao Prop
                          e ESTRUTURA DE DADOS: carrega uma maquina

idComputableInPolyTime    o unico exemplo trabalhado do Mathlib
                          e a IDENTIDADE, e e noncomputable
```

Usar o modelo **nao** e adotar uma definicao: e **construir um `FinTM2`
para `analyzeTransitionTable`**. O unico precedente no Mathlib e `id`.

```text
Primrec2 analyzeTransitionTable    FEITO, 31 declaracoes, 4 gates
FinTM2 para a mesma funcao         frente inteira, sem precedente proximo
```

## O veredito sobre `PVSNP-PHYS-001`

```text
ponte de computabilidade      FEITA
nivel uniforme                FEITO
modelo de custo               EXISTE no toolchain, caro de instanciar
P_phys / NP_phys              dependem de instancia-lo
ataque a P vs NP              NAO decorre de nada disso
```

Mesmo com as tres primeiras linhas prontas, o produto seria uma
**definicao de classe**, nao um ataque. Registrar isso agora impede a
leitura de que acumular pre-requisitos leva a um resultado.

## A selecao

```text
ENG-RUNTIME-SOUNDNESS-002
```

Nao e a frente mais ambiciosa; e a **unica barata e claramente devida**.

`analyzeTransitionTable_sound` devolve tres clausulas e perde o resto do
contrato `CycleWitness.Valid`. Consequencia medida:

```text
FiniteStateRuntime/DynamicAnalysis.lean   reducao privada, original
Monovariants/WitnessBounds.lean           segunda copia
ComputabilityBridge/WitnessBound.lean     terceira copia
UniformPrimrec/Analysis.lean              quarta copia
```

**Quatro reproducoes da mesma reducao do bloco `do`**, cada uma privada,
cada uma declarada como divida. `CB-GAP-004` e `UP-GAP-002` apontam para
a mesma correcao: alargar a soundness na origem.

Isso toca `ENG-FINITE-STATE-RUNTIME-001`, que esta **ENCERRADA**, e por
isso exige gate proprio — que e o que esta revisao autoriza, e nada mais.

## O que esta selecao NAO afirma

```text
que o modelo de custo sera instanciado
que classe de complexidade sera definida
que algum dos 6 problemas mudou de status
que alargar a soundness aproxima de qualquer problema aberto
```

E divida tecnica, paga porque quatro parcelas ja venceram.

## Estado dos 6, inalterado

```text
NS-PRESSURE-001    EDP e analise de fluidos          NAO
YM-LIMIT-001       QFT construtiva                   NAO
HODGE-CDK-001      geometria algebrica               NAO
BSD-HYP-MATRIX-001 aritmetica de curvas, Iwasawa     NAO
RH-NOGO-001        calculo pseudodiferencial         NAO
PVSNP-PHYS-001     falta instanciar FinTM2           AINDA NAO
```
