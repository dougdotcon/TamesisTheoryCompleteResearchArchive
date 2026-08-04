---
document_id: ATTACK-READINESS-2026-08-04
reviewed_at: 2026-08-04
selected_work_item: FOUND-COMPUTABILITY-BRIDGE-001
open_problems_assessed: 6
capability_probe_exit: 1
capability_probe_note: "exit 1 vem de UMA identificacao ausente; as 17 demais elaboraram"
---

# Prontidão de ataque — o que falta descobrir

## Como isto foi medido

Não por leitura de documentos. Por **elaboração**: um probe descartável
que tenta `#check` nos objetos de que cada problema precisa. Se o objeto
não elabora, não há o que atacar.

## O que o toolchain TEM

```text
riemannZeta : C -> C                 ELABORA
riemannZeta_one_sub                  ELABORA   equacao funcional
completedRiemannZeta                 ELABORA
Complex.log, Complex.exp             ELABORA
inner, InnerProductSpace             ELABORA
MeasureTheory.Measure, MeasureSpace  ELABORA
fderiv, HasFDerivAt                  ELABORA
Turing.TM2.Stmt                      ELABORA
Nat.Partrec                          ELABORA
Nat.Partrec.Code                     ELABORA
ComputablePred                       ELABORA
EllipticDivisibilitySequence         NAO ENCONTRADO
```

Uma correção de método, registrada: `Mathlib.MeasureTheory.Integral.Bochner`
**não tem `.olean`** — o módulo foi dividido em versões recentes. Isso não
é ausência de teoria, é nome obsoleto, e só se descobre elaborando.

## O que o LABORATORIO tem

Doze frentes encerradas, e **todas** sobre sistemas discretos
determinísticos finitos:

```text
monoides finitos, grafos funcionais, deteccao de ciclo executavel,
adaptador de tabela, codificacao certificada S <-> Fin n,
abstracao por semiconjugacao e a fronteira observacao/reflexao,
colapso de bissimulacao, invariantes e inalcancabilidade,
descida (corrigida apos vacuidade)
```

Em árvore própria: **zero análise, zero medida, zero EDP, zero teoria
espectral, zero geometria algébrica.**

## O veredito por problema

| Item | Primeiro passo honesto | Alcançável |
|---|---|---|
| `PVSNP-PHYS-001` | estrutural sobre computabilidade | **SIM** |
| `RH-NOGO-001` | lei global de Weyl, cálculo pseudodiferencial | NÃO |
| `NS-PRESSURE-001` | EDP e análise de fluidos | NÃO |
| `YM-LIMIT-001` | QFT construtiva | NÃO |
| `HODGE-CDK-001` | geometria algébrica | NÃO |
| `BSD-HYP-MATRIX-001` | aritmética de curvas, Iwasawa | NÃO |

Para os cinco de baixo, o primeiro passo seria **bibliográfico**, não
formal: auditar literatura que o laboratório não leu, com custo declarado
`very_high` em toda revisão de portfólio desde 2026-07-31. Nada mudou
nisso, e fingir o contrário seria teatro.

`RH-NOGO-001` merece nota: `riemannZeta` e a equação funcional
**elaboram**. Mas a lacuna congelada não é zeta — é
`GLOBAL-WEYL-BRIDGE-SCALAR`, `SPECIFIED_NOT_PROVED`, que exige cálculo
pseudodiferencial e lei de contagem global. Ter o objeto não é ter a
teoria.

## O que foi descoberto, e é a resposta pedida

**As duas metades nunca se tocaram.**

```text
o laboratorio prova coisas sobre sistemas finitos EXECUTAVEIS e
CERTIFICADOS -- analyzeEncodedSystem, CertifiedFiniteEncoding,
CycleWitness, detectores com soundness e completeness

o Mathlib tem ComputablePred, Nat.Partrec, Nat.Partrec.Code,
maquinas de Turing

e nao ha UMA declaracao ligando os dois
```

Isso é uma lacuna **verificável**, não uma opinião: nenhum arquivo sob
`TamesisLab/` menciona `Computable`, `Partrec` ou `Turing`.

`PVSNP-PHYS-001` pede definir `P_phys` e `NP_phys` **sem** alegar
`P ≠ NP`. Definir classes de complexidade exige uma noção de computação
formalizada. O laboratório tem execução certificada mas **não sabe dizer
que ela é computável** no sentido de Mathlib. Sem essa ponte, qualquer
definição de classe seria uma definição sobre nada.

## As perguntas que faltam responder, e são checáveis

```text
1. analyzeEncodedSystem e ComputablePred-compativel? Isto e, existe
   Computable para a funcao que ele calcula?
2. CertifiedFiniteEncoding S n induz Primcodable S?
3. O detector, sendo busca limitada, e Primrec e nao so Computable?
4. A cota baseIndex + period <= n da um limite de RECURSOS, e nao so de
   terminacao?
5. Existe alguma nocao de custo formalizavel sem modelo de maquina, ou
   custo exige comprometer-se com um modelo?
```

Nenhuma dessas é programa de pesquisa. Todas têm resposta verificável em
Lean, e **nenhuma foi respondida**.

## A seleção

```text
FOUND-COMPUTABILITY-BRIDGE-001
```

Ligar a máquina executável certificada do laboratório à hierarquia de
computabilidade do Mathlib. É o **único** caminho em que as doze frentes
encerradas transferem para um problema em aberto, e é pré-requisito de
qualquer coisa honesta em `PVSNP-PHYS-001`.

## O que esta seleção NÃO afirma

```text
que P vs NP sera atacado
que classes de complexidade serao definidas nesta frente
que o laboratorio esta perto de resultado em complexidade
que custo ou complexidade assintotica serao afirmados
```

O laboratório **não está** pronto para atacar nenhum dos seis. O caminho
mais curto até o único alcançável passa por, no mínimo, esta ponte e uma
frente de recursos depois dela. Duas frentes de preparação, e então uma
reavaliação — não um ataque.
