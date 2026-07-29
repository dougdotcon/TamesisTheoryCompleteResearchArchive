# Protocolo de auditoria rigorosa dos artigos

## Objetivo

Transformar cada artigo do repositório em uma investigação legível, rastreável e testável. A auditoria não deve confirmar a tese por retórica; deve identificar a pergunta, separar dados de interpretação, adicionar fontes primárias e indicar claramente o que ainda não foi demonstrado.

## Ordem obrigatória por artigo

1. **Identificação:** título, versão, idioma, caminho, estado editorial e relação com outros artigos.
2. **Pergunta:** converter o tema em uma pergunta falsificável.
3. **Afirmações:** listar cada afirmação como observação, definição, derivação, hipótese, previsão ou conclusão.
4. **Evidência:** localizar dados, código, equações, controles, amostra, incertezas e replicações.
5. **Fontes:** priorizar artigo original, dataset, documentação oficial ou revisão sistemática; verificar DOI, data, autores e se a fonte realmente sustenta a frase.
6. **Método:** conferir unidades, dimensionalidade, condições de contorno, estatística, comparação com alternativas e possibilidade de reprodução.
7. **Linguagem:** substituir absolutismos por níveis de evidência; explicar termos técnicos na primeira ocorrência; distinguir analogia, modelo e resultado.
8. **Resposta:** terminar com o que o artigo responde, o que não responde e qual experimento pode decidir a questão.
9. **Controle:** verificar links, fórmulas, referências, HTML válido, acessibilidade, consistência entre versões Markdown/HTML e ausência de afirmações extraordinárias sem qualificação.

## Rótulos epistemológicos

- **E0 — menção:** aparece como termo, analogia ou ideia sem análise.
- **E1 — artefato computacional/legado:** simulação, cálculo ou relatório existente, sem validação independente suficiente.
- **H1 — hipótese/modelo:** formulação explícita com previsões, ainda não confirmada.
- **H2 — suporte empírico:** dados reproduzíveis, controles, incerteza e comparação com alternativas.
- **T — resultado formal verificado:** prova ou teorema com escopo preciso; não confundir com evidência física.
- **Q — quarentena:** afirmação especulativa, contradita, mal definida ou que exigiria autoridade além do acervo atual.

## Matriz de afirmações

Cada artigo deve conter uma tabela como esta, no relatório de auditoria:

| ID | Afirmação | Tipo | Evidência local | Fonte externa | Teste/falsificação | Rótulo |
|---|---|---|---|---|---|---|
| A1 | frase curta e verificável | dado/definição/modelo/previsão | arquivo, seção ou linha | DOI/URL | resultado que a refutaria | E0–Q |

## Regras de fontes

Uma fonte só pode sustentar uma frase que ela realmente contém ou demonstra. Para resultados técnicos, preferir artigo original e versão aberta/preprint; para fatos de consenso, revisão de alta qualidade; para dados, repositório e documentação do instrumento. Não usar uma fonte secundária para dar aparência de confirmação a uma hipótese própria. Registrar data de acesso quando o fato puder mudar.

## Linguagem científica e palatável

O texto final deve usar a sequência: **problema → hipótese → método → resultado → limite → próximo teste**. Evitar “prova que”, “resolve”, “universal” e “consciência é” quando o estudo apenas sugere associação. Preferir “é compatível com”, “o modelo prevê”, “o conjunto de dados não permite distinguir” e “esta afirmação permanece em aberto”. Cada artigo deve ter um resumo de 100–150 palavras para leitor não especialista e um bloco técnico para reprodução.

## Novas abordagens obrigatórias

- **Comparação adversarial:** formular antecipadamente o resultado que favorece e o que desafia a tese, incluindo pelo menos uma teoria alternativa.
- **Análise de sensibilidade:** repetir a conclusão com diferentes janelas, parâmetros, escalas e critérios de inclusão.
- **Reprodutibilidade:** guardar dados, código, ambiente, sementes aleatórias e versão do manuscrito.
- **Inferência causal:** separar correlação, mecanismo proposto e intervenção que poderia alterar o sistema.
- **Escalonamento:** só declarar lei de potência, universalidade ou fractalidade após estimar faixa de escala, expoente e incerteza e comparar distribuições alternativas.
- **Síntese por sistema:** comparar artigos pelo mesmo observável e mecanismo; não agrupar sistemas apenas por palavras semelhantes.

## Registro de execução

O progresso deve ser mantido em um registro separado, com uma linha por artigo:

```text
article_id | source_path | format | language | research_line | status |
evidence_level | source_gaps | language_revision | method_revision |
html_checked | reviewer_notes | last_audited
```

Estados editoriais recomendados: `not_started`, `auditing`, `revised`, `needs_data`, `ready_for_review`, `published`, `quarantined`.

## Critério de conclusão global

O programa só estará concluído quando todos os artigos tiverem uma linha no registro, cada afirmação central tiver rótulo epistemológico, cada fonte estiver validada, cada versão HTML/Markdown estiver sincronizada e o relatório global listar respostas encontradas, perguntas abertas e artigos que precisam de novos dados.
