# RH-REAL — Fase 0: triagem numérica exploratória

**Status:** exploratório (`evidence_level: exploratory_only`), NÃO um teste
pré-registrado. Segue `00_GOVERNANCE/AGENTS.md` passo 2 (formular hipótese
+ localizar dado real) e o `next_action` de `DISC-RH-REAL-001` em
`01_PORTFOLIO/TEST_QUEUE.yaml`.

## O que foi feito

1. **Dado real localizado e baixado** (`data/PROVENANCE.md`): tabelas de
   Odlyzko, 100.000 primeiros zeros reais de ζ(s) (`zeros1.txt`) +
   amostra de 10.000 zeros próximos ao zero #10¹² (`zeros3.txt`).
   Verificado por fetch direto — primeiro valor bate com o zero didático
   conhecido (14,134725142).
2. **Levantamento de literatura**: 12 conjecturas/resultados concretos e
   numericamente testáveis sobre zeros de zeta (não a Hipótese de Riemann
   em si), cada um com citação verificada — ver relatório completo do
   agente de pesquisa nesta sessão. Itens 5, 6, 10 exigem avaliação de
   ζ(s) (não só localização de zeros) — deferidos.
3. **Triagem numérica** (`analysis/phase0_triage.py`,
   `analysis/phase0_triage_result.json`) rodada sobre os 100.000 zeros
   reais para 6 dos 12 itens (os que só precisam de localização de
   zeros).

## Resultados da triagem

| Item | Achado | Interpretação |
|---|---|---|
| 2. Espaçamento GUE (Wigner surmise) | média=1,0000, RMSE=0,0306 vs. Wigner surmise | Pipeline funciona — reproduz estatística GUE conhecida com precisão razoável |
| 3. N(T) (Riemann–von Mangoldt) | resíduo 0,3–0,6 em 5 pontos de T | Consistente com a fórmula clássica (termo S(T) pequeno esperado) |
| 7. Gap mínimo (Inoue 2026, limiar 0,50895, condicional a RH) | mínimo observado: 0,02186 | Não testa o liminf (não testável com dado finito) — apenas confirma que gaps pequenos já aparecem nesta faixa, sem contradição |
| 8. Gap máximo (Bui & Milinovich, limiar 3,18) | máximo observado: 2,8052, não excede | Esperado — o resultado é sobre existência em alturas maiores, não detectável nesta faixa |
| 9. Runs de gaps moderados consecutivos (questão aberta, arXiv:2412.15481) | r=2: 80.953 runs; r=3: 72.334 runs (c=0,5) | **c=0,5 é permissivo demais para ser informativo** — a maioria dos gaps já excede metade do espaçamento médio, então isso não é uma checagem afiada da questão em aberto. Um `c` menor precisaria ser escolhido para um teste real |
| 1. Correlação de pares (Montgomery) | densidade perto de u<0,3: 0,0111 vs. fundo uniforme 0,1111 (supressão ~10×); densidade para u>1,0: 0,1165 (≈ fundo uniforme) | Repulsão de nível clara e forte perto de u=0, sem correlação de longo alcance — qualitativamente exatamente o que GUE prevê |

**Nota de correção durante a própria execução**: a primeira versão do
script tinha um comentário de impressão enganoso (dizia que a densidade
de fundo "deveria ser ~1", quando na verdade — dado que
`np.histogram(density=True)` normaliza sobre todo o domínio de 9 unidades
— o fundo uniforme esperado é ~1/9≈0,111, não 1). Corrigido antes de
aceitar o resultado como válido; o número calculado (0,1165) sempre
esteve correto, só o comentário estava errado.

## Avaliação: o que isso estabelece

- **Validação de ferramental**: itens 1, 2 e 3 confirmam que nosso
  próprio código de carregamento/análise de zeros reais produz
  estatísticas consistentes com resultados bem estabelecidos — condição
  necessária antes de tentar qualquer coisa mais ambiciosa.
- **Nenhum resultado aqui é uma descoberta** — são checagens de
  consistência com literatura já estabelecida (itens 1-3, 8) ou
  observações não-decisivas sobre limites finitos de resultados
  assintóticos (item 7).
- **Item 9 precisa de redesenho** antes de virar candidato a
  pré-registro — o `c=0,5` sugerido pelo levantamento inicial não é
  afiado o suficiente.

## Candidatos mais promissores para um pré-registro real (não decidido ainda)

Por ordem de "novidade genuína" (menos verificado antes = mais
interessante testar com disciplina):

1. **Item 9 (runs de gaps moderados consecutivos)** — questão
   explicitamente aberta na literatura (arXiv:2412.15481, dez/2024),
   nenhum estudo numérico citado. Precisa de escolha cuidadosa de `c` e
   `r` (não `c=0,5`) antes de qualquer pré-registro.
2. **Item 7 (constante de gaps pequenos, Inoue 2026)** — resultado muito
   recente (abr/2026), condicional a RH, sem verificação numérica
   independente citada. Um pré-registro real precisaria de uma pergunta
   testável mais específica que "o mínimo observado é menor que X" (que
   não é falsificável da forma como está).
3. **Item 12 (variância do número / rigidez GUE)** — sinalizado pelo
   agente de pesquisa como "STATUS_UNCERTAIN", precisa de checagem de
   fonte primária antes de qualquer uso.

## Próxima ação

Nenhuma decidida nesta sessão. Escolher um destes (ou outro) para
desenhar um pré-registro real exigiria: (a) uma pergunta genuinamente
falsificável (não "o mínimo observado é X", que não falsifica nada); (b)
um critério de decisão declarado a priori; (c) provavelmente holdout
selado se envolver busca sobre múltiplos parâmetros (`c`, `r`, janelas de
altura). Ver `00_GOVERNANCE/METHODOLOGY_EXTENSIONS.md` §1 e §6.
