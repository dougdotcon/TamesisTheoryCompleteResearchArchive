# Padrões e Estilo do Artigo Acadêmico - Teoria Tamesis

Este documento documenta os padrões estruturais, estilísticos e de formatação identificados no artigo "The Computational Architecture of Reality: Complete Theory of Everything" (Treatise_07_Computational_Architecture_v3_COMPLETE.html), para padronização de papers de nível Nobel.

## 1. Estrutura Geral do Documento

### 1.1 Layout e Formatação Básica
- **Fonte principal**: Times New Roman, 10pt, justificado.
- **Espaçamento**: Line-height 1.15, margem 1.5cm nas laterais.
- **Layout**: Coluna única (duas colunas comentadas no CSS, mas não ativadas).
- **Cabeçalho**: Centralizado, com título em negrito 16pt, autores 11pt, afiliações 10pt itálico, data 9pt.
- **Abstract**: Centralizado, 9pt, com título em negrito itálico, bordas superior e inferior.
- **Corpo**: Texto justificado, parágrafos indentados em 1em (exceto primeiro de seção).

### 1.2 Hierarquia de Seções
- **H1**: Título principal (16pt, negrito, centralizado).
- **H2**: Seções principais (11pt, negrito maiúsculo, com borda inferior).
- **H3**: Subseções (10pt, negrito).
- **H4**: Sub-subseções (10pt, itálico).
- **Introdução**: Sempre sem indentação no primeiro parágrafo.

### 1.3 Elementos Especiais
- **Caixas de Definição**: Bordas 2px pretas, padding 0.8rem, fundo #fafafa, para definições e teoremas.
- **Caixas de Derivação**: Bordas 1px pretas, padding 0.8rem, para derivações matemáticas.
- **Caixas de Equação**: Bordas 2px pretas, padding 0.8rem, fundo branco, para equações destacadas.
- **Teoremas**: Caixas com título em negrito, conteúdo justificado.

## 2. Formatação de Texto

### 2.1 Ênfase e Destaque
- **Negrito**: Para termos-chave, constantes fundamentais, títulos de caixas.
- **Itálico**: Para afiliações, nomes de constantes (ex: α, Ω_Λ), ênfase sutil.
- **Código**: Fonte Courier New 8pt, fundo #f5f5f5, padding 1px 3px, para nomes de arquivos/scripts.

### 2.2 Parágrafos
- Primeiro parágrafo de seção: Sem indentação.
- Parágrafos subsequentes: Indentação 1em.
- Margem inferior: 0.8rem.

### 2.3 Listas
- **Ordenadas (ol)**: Para passos de derivação, argumentos.
- **Não ordenadas (ul)**: Para listas de pontos, interpretações físicas.
- Margem: 0.5rem superior/inferior, padding-left 1.2rem.
- Itens: Margem inferior 0.3rem.

## 3. Matemática e Equações

### 3.1 Renderização
- **Biblioteca**: KaTeX para renderização de LaTeX.
- **Delimitadores**: $$ para display mode, $ para inline.
- **Fonte**: Mesmo que texto, tamanho 10pt para display.

### 3.2 Formatação de Equações
- **Display**: Centralizadas, margem 1rem superior/inferior.
- **Inline**: Integradas no texto.
- **Caixas de Equação**: Para equações destacadas, com bordas.
- **Numeração**: Implícita, não explícita (equações não numeradas).

### 3.3 Símbolos e Notação
- Constantes: α, Ω_Λ, m_e, etc.
- Subscritos/Superscritos: Usados extensivamente.
- Vetores: Negrito para vetores (ex: σ_i).
- Unidades: Sempre especificadas (MeV, GeV, etc.).

## 4. Figuras e Tabelas

### 4.1 Figuras
- **Posicionamento**: Centralizadas, margem 1rem.
- **Imagem**: Max-width 100%, borda 1px #999.
- **Legenda**: 9pt, justificada, margem superior 0.5rem.
- **Numeração**: FIG. 1, FIG. 2, etc.
- **Alt-text**: Descrição técnica para acessibilidade.

### 4.2 Tabelas
- **Largura**: 100%, collapse borders.
- **Fonte**: 8pt para corpo, headers negrito.
- **Bordas**: 1px pretas.
- **Headers**: Fundo #f0f0f0.
- **Padding**: 3px 4px, centralizado.
- **Quebra de página**: Evitada (break-inside: avoid).

## 5. Referências e Citações

### 5.1 Citações no Texto
- **Formato**: [1], [2,3], numérico sequencial.
- **Posicionamento**: Após menção, antes de pontuação.

### 5.2 Seção de Referências
- **Título**: H2 "References".
- **Formato**: Lista ordenada, 9pt, line-height 1.2.
- **Estrutura**: [Número] Autor. (Ano). "Título". *Journal*, volume(issue), páginas. DOI.
- **Links**: DOIs como hyperlinks.
- **Nota final**: Créditos e link para repositório.

## 6. Apêndices e Elementos Adicionais

### 6.1 Apêndices
- **Títulos**: H2 "Appendix A", etc.
- **Conteúdo**: Scripts Python listados em ul, com nomes de arquivos em code.

### 6.2 Figuras de Página Inteira
- Classe "full-width", quebra de página antes.
- Imagem 100% width, legenda detalhada.

## 7. Linguagem e Tom

### 7.1 Estilo Acadêmico
- **Formal**: Linguagem precisa, técnica, sem colloquialismos.
- **Objetivo**: Foco em fatos, derivações, comparações.
- **Crítico**: Auto-avaliação honesta, distinção entre derivado e fenomenológico.

### 7.2 Estrutura de Argumentação
- **Introdução**: Contextualização histórica, motivação.
- **Corpo**: Derivações passo-a-passo, resultados numéricos, erros.
- **Conclusão**: Síntese, predições testáveis, impacto.

### 7.3 Ênfase em Precisão
- **Erros**: Sempre reportados em %, com "EXACT", "EXCELLENT", "GOOD".
- **Limitações**: Admitidas explicitamente (ex: k fenomenológico).
- **Reprodutibilidade**: Scripts Python fornecidos.

## 8. Metadados e Publicação

### 8.1 Cabeçalho
- **Título completo**: Descritivo, abrangente.
- **Autor**: Nome completo, afiliação institucional.
- **Data**: Completa, com versão.
- **DOI**: Link para Zenodo ou similar.

### 8.2 CSS para Impressão
- **Quebra de página**: Evitada em elementos importantes.
- **Margens**: Adequadas para papel A4/Letter.
- **Cores**: Preto/branco, tons de cinza para headers.

## 9. Padrões Específicos para Teoria de Tudo

### 9.1 Derivações
- **Estrutura**: Título H4, base física, fórmula, resultado, observado, erro, status.
- **Status**: ✓ EXACT, ⚠ STRUCTURAL, ❌ PHENOMENOLOGICAL.

### 9.2 Comparação com Modelo Padrão
- **Parâmetros**: Redução de 19+ para 7-10 (~50-60%).
- **Realizações**: Destaque para resolução de Λ (10^120 → 2.7%).

### 9.3 Predições Testáveis
- **Falsificabilidade**: Critérios explícitos para refutação.
- **Experimentos**: Levitated nanoparticles, MAQRO, etc.

Este padrão garante consistência, rigor matemático e apresentação profissional adequada para publicações de alto impacto.