# Estado da Trilha de Descoberta Computacional

**Última atualização:** 2026-08-12
**Trilha paralela a:** `04_FORMAL_RESEARCH_LAB` (ciclo de ondas Lean, não afetado por esta trilha)

## Status atual

| Campo | Valor |
|---|---|
| Teste ativo | `DISC-COSMOLOGY-MOND-SPARC-001` |
| Fase | Pré-registro travado (LOCKED); análise ainda não executada |
| Próxima ação obrigatória | Rodar a análise pré-registrada sobre `data/Rotmod_LTG/*.dat` (ver `02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` seção 4), depois reexecução adversarial |
| Decisões de governança | `DISC-DEC-001` (criação da trilha) |
| Claims fechados | 0 |
| Claims em andamento | 0 (o teste ainda não produziu resultado) |

## O que já foi feito nesta trilha

1. Governança criada: `00_GOVERNANCE/{AGENTS.md,DECISION_LEDGER.yaml,CLAIM_LEDGER.yaml,PREREGISTRATION_TEMPLATE.md}`.
2. Piloto escolhido (autorização explícita do usuário): auditar e refazer o
   teste EFE/SPARC de `01_TAMESIS_CORE/02_Experimental_Validation/MOND_EFE`.
3. Auditoria do código legado completa:
   `02_TESTS/COSMOLOGY_MOND_SPARC/AUDIT_LEGACY_MOND_EFE_SPARC.md` — 8
   achados citados por arquivo:linha, incluindo o achado central de que as
   8 galáxias "reais" de Virgem da manchete "EFE CONFIRMED" não existem no
   catálogo SPARC público real.
4. Dado real baixado e verificado (URL correta, HTTPS com TLS padrão, sem
   fallback embutido): `02_TESTS/COSMOLOGY_MOND_SPARC/data/PROVENANCE.md`.
5. Pré-registro travado ANTES de qualquer cálculo sobre o dado real:
   `02_TESTS/COSMOLOGY_MOND_SPARC/PREREGISTRATION.md` — hipótese, modelo
   nulo, estatística de teste, critério de falsificação e escopo do que não
   está sendo testado, todos travados. Desenho do teste teve que ser
   adaptado (Virgem → aglomerado de Ursa Maior, usando o campo `f_D=4` já
   nativo do catálogo) precisamente por causa do Achado 5 da auditoria —
   documentado na Seção 0 do pré-registro.

## O que ainda não foi feito

- Executar a análise (calcular as inclinações reais, o teste t, o p-valor).
- Reexecução adversarial por um agente independente.
- Registrar o resultado (qualquer que seja) em `TEST_QUEUE.yaml` e
  `CLAIM_LEDGER.yaml`.
- Relatório de sessão em `09_SESSIONS/2026/`.
- Primeiro commit de toda a árvore `05_DISCOVERY_LAB/` neste repositório.

## Como continuar (para o próximo agente/sessão)

Seguir `00_GOVERNANCE/AGENTS.md` a partir do passo 6 ("Rodar a análise
pré-registrada"). Não alterar `PREREGISTRATION.md` — qualquer mudança de
critério agora é uma violação a ser reportada, não uma correção silenciosa.
