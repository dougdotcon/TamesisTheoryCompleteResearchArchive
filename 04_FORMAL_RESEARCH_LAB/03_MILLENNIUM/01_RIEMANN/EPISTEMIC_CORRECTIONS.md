# RH-NOGO-001 — Correções epistemológicas

Registro das correções aplicadas no gate `ASYM-NOGO-001` (2026-07-31) sobre
artefatos produzidos no gate de especificação anterior. O relatório de
sessão daquele gate **não foi reescrito**: ele permanece como registro
histórico do que foi afirmado na época, e esta página é a errata.

## Correção 1 — exaustividade indevida sobre a literatura

O texto anterior afirmava, em `DEFINITIONS.md` (questão 14) e em
`EXCLUSIONS.md` (consequência epistemológica), que *"todas as rotas
espectrais vivas / atualmente estudadas na literatura"* ficam fora da
Classe W.

Um catálogo de oito registros não sustenta uma afirmação exaustiva sobre a
literatura inteira. A formulação passou a ser:

```text
todas as propostas espectrais incluídas na amostra bibliográfica
catalogada nesta sessão
```

O conteúdo do resultado não muda: o no-go continua sem refutar
Hilbert–Pólya. O que muda é a extensão da afirmação sobre o campo.

## Correção 2 — "fontes auditadas" versus "registros classificados"

O texto anterior falava em *"oito fontes auditadas"*. Nenhuma das oito
obras teve seu texto integral obtido e lido nesta ou na sessão anterior.
A formulação correta é:

```text
oito registros bibliográficos classificados
```

A chave `sources_audited` de `rh-nogo-001-specification-result.json` foi
renomeada para `bibliographic_records_classified`, com nota de correção
embutida no próprio arquivo.

## Dois eixos independentes

A confusão vinha de colapsar dois eixos que devem ser declarados
separadamente. Um resultado pode estar **estabelecido na literatura**
enquanto a **fonte primária específica** ainda não foi lida.

```yaml
source_retrieval_status:
  CONTENT_AUDITED: []        # texto integral obtido e lido — nenhum registro
  LISTING_CONFIRMED:
    - HEDENMALM-2026         # existência confirmada em listagem pública
  KNOWN_RECORD:
    - RIEMANN-1859
    - VONMANGOLDT-1905
    - BOMBIERI-CLAY
    - HORMANDER-1968
    - BERRYKEATING-1999
    - CONNES-1999
    - BBM-2017
  TO_FETCH:
    - RIEMANN-1859
    - VONMANGOLDT-1905
    - HORMANDER-1968
    - BERRYKEATING-1999
    - HEDENMALM-2026

mathematical_claim_status:
  ESTABLISHED:
    - "contagem de Riemann–von Mangoldt (incondicional)"
    - "lei de Weyl na classe elíptica compacta"
    - "comparações assintóticas log vs potência"
    - "RH permanece sem solução aceita"
  CONDITIONAL:
    - "extensão do no-go a bordo, a pseudodiferenciais clássicos e a operadores limitados inferiormente"
  PROPOSED:
    - "RH-NOGO-001 (exclusão da Classe W)"
    - "ASYM-NOGO-001 (antes deste gate; agora VERIFIED em Lean)"
  REJECTED:
    - "preprints de suposta prova da RH como autoridade"
    - "claims históricas Tamesis sobre Riemann"
```

Leitura obrigatória: `CONTENT_AUDITED` está **vazio**. Nenhum enunciado
deste programa pode ser apresentado como apoiado em leitura integral de
fonte primária até que o gate `RH_NOGO_PRIMARY_SOURCE_AUDIT_AUTHORIZED`
seja executado.

## Efeito sobre o núcleo formalizado

Nenhum. `ASYM-NOGO-001` é um lema de análise real que não depende de
nenhuma das oito referências: sua prova usa apenas a Mathlib. A ponte entre
o lema e Riemann–von Mangoldt / lei de Weyl continua **não construída** e
depende da leitura primária (GAP-RH-002, GAP-RH-003).
