# RH-NOGO-001 — Stop conditions

Interromper imediatamente qualquer sessão desta frente se:

1. o próximo passo exigir `RH_NOGO_PROOF_EXECUTION` sem autorização
   literal;
2. alguém tentar construir um operador cujo espectro é definido a partir
   dos próprios zeros (circularidade de construção);
3. GUE, Montgomery–Odlyzko ou estatísticas de zeros entrarem como
   **premissa** de prova;
4. a formalização exigir `sorry`, `admit`, axioma local ou `unsafe`;
5. o enunciado começar a ser apresentado como refutação de Hilbert–Pólya,
   como progresso sobre a verdade da RH ou com percentuais de chance;
6. a classe W for silenciosamente ampliada para cobrir rotas listadas em
   `ESCAPE_ROUTES.md`;
7. um preprint não auditado (incluindo HEDENMALM-2026 e qualquer suposta
   prova da RH) for citado como resultado estabelecido;
8. linguagem Tamesis substituir o enunciado clássico;
9. a fonte primária da lei de Weyl (GAP-RH-002) não puder ser transcrita
   na versão exata exigida — nesse caso o gate de prova do resultado
   completo fica bloqueado (o núcleo abstrato não é afetado);
10. qualquer arquivo fora de `04_FORMAL_RESEARCH_LAB/` for modificado.
