# Instruções para agentes do laboratório formal

## Ordem obrigatória

1. Ler `LAB_STATE.md`.
2. Rodar `python 10_TOOLS/labctl.py status`.
3. Verificar a autorização do `active_work_item`.
4. Ler o `STATUS.yaml` da frente ativa.
5. Executar somente `next_single_action`.
6. Rodar os testes e validadores pertinentes.
7. Criar um relatório de sessão em `09_SESSIONS/YYYY/`.
8. Atualizar `LAB_STATE.md`.
9. Atualizar `CHANGELOG.md` somente se houver mudança de estado,
   arquitetura, evidência ou decisão.
10. Parar.

## Proibições

Um agente não pode:

- iniciar a fase seguinte automaticamente;
- alterar status para `VERIFIED` sem gate;
- modificar arquivos fora de `04_FORMAL_RESEARCH_LAB/`;
- inventar referências;
- substituir o enunciado clássico por linguagem Tamesis;
- usar simulação como prova;
- ocultar falha ou preencher gap com `sorry`, `admit` ou axioma local;
- continuar após um stop condition;
- declarar qualquer Problema do Milênio resolvido.

## Separação de ferramentas

Lean contém definições, lemas e teoremas verificados. Python procura
contraexemplos, testa casos finitos, verifica álgebra simbólica e valida
artefatos. Python nunca promove uma afirmação universal a `T`.

## Legado

O legado é somente leitura. Qualquer alteração fora de
`04_FORMAL_RESEARCH_LAB/` interrompe a sessão e deve ser reportada como
`LAB0_LEGACY_MODIFICATION_DETECTED`.

