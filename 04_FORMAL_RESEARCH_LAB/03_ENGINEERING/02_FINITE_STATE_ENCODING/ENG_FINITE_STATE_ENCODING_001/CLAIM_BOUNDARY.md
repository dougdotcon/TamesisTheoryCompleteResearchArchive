---
document_id: ENC-CLAIM-BOUNDARY
claims_promoted: 0
ledger_size: 21
---

# Fronteira de claims

## Nenhuma claim promovida

```text
o ledger permanece com 21 claims.
```

Nada foi formalizado permanentemente neste gate; promover seria promover
uma especificação.

## Candidato futuro, não promovido

```yaml
claim_id: CERTIFIED-FINITE-STATE-ENCODING-FORMAL-001
status: CANDIDATE_NOT_PROMOTED
evidence_level: NONE
depends_on: FINITE-STATE-RUNTIME-ADAPTER-FORMAL-001
```

## Wording futura permitida

```text
codificacao finita certificada FORNECIDA;
tabela construida computavelmente;
correspondencia de passo;
correspondencia de iteracoes;
soundness da analise no sistema tipado.
```

## Wording proibida

```text
correcao de sistema externo;
modelo universal;
extracao;
CLI;
integracao;
eficiencia;
minimalidade;
novo algoritmo;
novidade matematica.
```

## A precisão de linguagem congelada neste gate

```text
Um erro de codificacao NAO torna falso o certificado sobre a tabela.

O certificado continua correto para aquela tabela, mas pode nao
sustentar nenhuma conclusao sobre o sistema que se pretendia
representar.
```

Esta formulação substitui qualquer redação anterior que sugerisse que uma
codificação errada produziria um certificado incorreto. O certificado da
frente anterior é, e continua sendo, correto sobre o seu objeto. O que
faltava — e o que esta frente fornece, no recorte tipado — é a ponte
entre esse objeto e o sistema pretendido.
