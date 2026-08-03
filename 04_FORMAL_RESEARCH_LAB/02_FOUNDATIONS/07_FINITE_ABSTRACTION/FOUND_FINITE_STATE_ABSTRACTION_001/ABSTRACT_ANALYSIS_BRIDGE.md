---
document_id: FOUND-FINITE-STATE-ABSTRACTION-001-ABSTRACT-ANALYSIS-BRIDGE
work_item_id: FOUND-FINITE-STATE-ABSTRACTION-001
---

# Ponte para a análise abstrata

## Assinatura congelada

```lean
def analyzeAbstractSystem
    (abstraction :
      CertifiedFiniteAbstraction C A stepC stepA)
    (encoding : CertifiedFiniteEncoding A n)
    (start : C) :
    Except RuntimeCycleError CycleWitness :=
  analyzeEncodedSystem
    encoding
    stepA
    (abstraction.abstract start)
```

Uma linha de corpo. A única coisa que a ponte faz é **abstrair o estado
inicial** e delegar.

## O que a ponte reutiliza sem alterar

```text
CertifiedFiniteEncoding      tipo da codificacao
analyzeEncodedSystem         a analise ja verificada
RuntimeCycleError            tipo de erro, intocado
CycleWitness                 certificado, intocado
```

Nenhum construtor de erro é criado ou removido. Nenhum witness padrão
existe. O detector não é copiado nem totalizado. Não há segunda
semântica de execução.

## Por que `stepA`, e não `stepC`

`analyzeEncodedSystem` exige um passo sobre o tipo **codificado**. `C`
não tem codificação — e a frente inteira existe porque ele pode nem ser
finito. O que se executa é o sistema abstrato; o concreto é observado.

## Computabilidade

```text
analyzeAbstractSystem   computavel
```

A pegada `[propext, Classical.choice, Quot.sound]` medida na declaração
é herdada de `analyzeEncodedSystem` pelo **tipo**, e vive em
proposições apagadas na execução. Nenhuma escolha clássica produz
`abstract`, `encode`, `decode`, `Array` ou o `CycleWitness` devolvido.

## Erros

A exclusão universal de erro herdada,
`analyzeEncodedSystem_ne_error`, permanece disponível na frente
anterior. Reexportá-la para o nível abstrato é `DEFERRED_OPTIONAL`:
`analyzeAbstractSystem_complete` já entrega o que a cadeia central
precisa.
