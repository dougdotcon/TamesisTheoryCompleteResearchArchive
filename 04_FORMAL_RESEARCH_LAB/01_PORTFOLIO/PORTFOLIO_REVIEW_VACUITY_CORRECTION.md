---
document_id: PORTFOLIO-REVIEW-VACUITY-CORRECTION
reviewed_at: 2026-08-04
selected_work_item: LAB-CORR-MONOVARIANT-VACUITY-001
alternatives_compared: 3
defect_severity: CRITICAL
---

# Revisão de portfólio — um defeito crítico na frente recém-encerrada

## O defeito

`FOUND-MONOVARIANT-DESCENT-001` foi encerrada em `a8929d7` com uma
definição **vácua**.

```lean
def Monovariant (measure : C → Nat) (stepC : C → C) : Prop :=
  ∀ c : C, measure (stepC c) < measure c
```

Se `C` é habitado, a imagem de `measure` em `Nat` tem mínimo
`m₀ = measure c₀`. Mas a hipótese dá `measure (stepC c₀) < m₀`, e esse
valor também está na imagem. Contradição.

```text
Monovariant measure stepC  ->  IsEmpty C
```

Provado, **sem depender de axioma nenhum**.

## O que isso significa, sem atenuação

```text
todos os teoremas daquela frente sao VERDADEIROS
nenhum deles e APLICAVEL a sistema algum habitado
a claim foi promovida sobre hipotese que nada satisfaz
```

`Monovariant.no_periodic_point` e `monovariant_not_orbitSeparating` são
vacuamente verdadeiros. As duas negações registradas —
`downStep_not_monovariant` e `strictDown_not_monovariant` — são
verdadeiras, mas **tudo** falha em ser monovariante, então elas não
distinguiam nada. O gate de especificação e o de resultado passaram sem
pegar isso: ambos conferiram contagem, pegada e tokens, e **nenhum
verificou satisfazibilidade**.

## Por que não foi pego

Os cinco gates verificaram forma, não conteúdo:

```text
contagem derivada     conferida
pegada axiomatica     medida
tokens proibidos      varridos
typeclasses           contadas
SATISFAZIBILIDADE     NAO VERIFICADA
```

A instância `strictDown` estava lá, e **falhou** em ser monovariante — o
que foi registrado como "limite honesto da ferramenta" quando era, na
verdade, o sintoma. Nenhuma instância positiva foi exigida.

## A correção

O argumento clássico de monovariante nunca exigiu decrescimento em todo
estado: exigiu decrescimento **enquanto o sistema não parou**.

```lean
def DescendsOn (measure : C → Nat) (stepC : C → C) (P : C → Prop) : Prop :=
  ∀ c : C, P c → measure (stepC c) < measure c

theorem DescendsOn.exits (h : DescendsOn measure stepC P) :
    ∀ c : C, ∃ k : Nat, ¬ P ((stepC^[k]) c)
```

Não é vácua, e tem instância que funciona: subtração truncada decresce
enquanto o estado é positivo, e o sistema chega a zero.

## As três alternativas

| | Candidato | Veredito |
|---|---|---|
| A | **Corrigir a vacuidade** | **SELECIONADO** |
| B | Combinar invariante e monovariante, `MON-GAP-005` | bloqueado por A |
| C | Transporte de certificados por semiconjugação | adiado |

**B estava selecionado mentalmente e foi abandonado**: combinar uma peça
vácua com outra produziria duas peças vácuas.

## O que a correção NÃO faz

```text
NAO apaga a frente encerrada
NAO reescreve o changelog
NAO remove a claim do ledger
NAO modifica arquivo Lean de frente encerrada
```

A vacuidade passa a ser **teorema no repositório**, não errata em prosa.
A claim recebe bloco de correção, com o wording anterior preservado.

## Nova regra permanente

```text
Toda frente que introduz uma hipotese deve exibir uma INSTANCIA
POSITIVA que a satisfaca, num tipo habitado, ou declarar
explicitamente que a hipotese e vacua.
```

## Próxima ação

```text
LAB_CORR_MONOVARIANT_VACUITY_CORRECTION_AUTHORIZED
```
