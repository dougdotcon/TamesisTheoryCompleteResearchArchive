#!/usr/bin/env python3
"""
Aplica os padrões do PADROES_ESTILO_ARTIGO.md aos 12 treatises em 13_CANON
"""

import re
from pathlib import Path

CANON_DIR = Path(r"d:\TamesisTheoryCompleteResearchArchive\13_CANON")

# Padrões CSS a serem aplicados conforme PADROES_ESTILO_ARTIGO.md
CSS_STANDARDS = """
        /* === ACADEMIC JOURNAL STYLING - TAMESIS STANDARDS === */
        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
            line-height: 1.15;
            color: #000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 1.5cm;
            background-color: #fff;
        }

        /* === HEADER === */
        header {
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #000;
        }

        h1 {
            font-family: 'Times New Roman', Times, serif;
            font-size: 16pt;
            font-weight: bold;
            margin-bottom: 0.75rem;
            line-height: 1.2;
            color: #000;
        }

        .authors {
            font-size: 11pt;
            font-style: normal;
            font-weight: normal;
            color: #000;
            margin-bottom: 0.25rem;
        }

        .affiliations {
            font-size: 10pt;
            font-style: italic;
            color: #333;
            margin-bottom: 0.5rem;
        }

        .date {
            font-size: 9pt;
            color: #333;
        }

        /* === ABSTRACT === */
        .abstract {
            margin: 1.5rem 0;
            font-size: 9pt;
            text-align: justify;
            padding: 1rem 0;
            border-top: 1px solid #000;
            border-bottom: 1px solid #000;
        }

        .abstract-title {
            font-weight: bold;
            font-style: italic;
            font-size: 9pt;
            margin-bottom: 0.5rem;
            display: block;
            text-align: center;
        }

        /* === TYPOGRAPHY === */
        h2 {
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            font-weight: bold;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            color: #000;
            border-bottom: 1px solid #000;
            padding-bottom: 0.3rem;
            text-transform: uppercase;
        }

        h3 {
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
            font-weight: bold;
            font-style: normal;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
            color: #000;
        }

        h4 {
            font-family: 'Times New Roman', Times, serif;
            font-size: 10pt;
            font-weight: normal;
            font-style: italic;
            margin-top: 0.8rem;
            margin-bottom: 0.3rem;
            color: #000;
        }

        p {
            margin-bottom: 0.8rem;
            text-indent: 1em;
            text-align: justify;
        }

        p.no-indent {
            text-indent: 0;
        }

        /* === BOXES === */
        .definition-box,
        .theorem-box {
            background: #fafafa;
            padding: 0.8rem;
            margin: 0.8rem 0;
            border: 2px solid #000;
            break-inside: avoid;
        }

        .derivation-box {
            background: #fff;
            padding: 0.8rem;
            margin: 0.8rem 0;
            border: 1px solid #000;
            break-inside: avoid;
        }

        /* === EQUATIONS === */
        .equation,
        .equation-box {
            background: #fff;
            padding: 0.8rem;
            margin: 0.8rem 0;
            border: 2px solid #000;
            text-align: center;
            break-inside: avoid;
        }

        .master-equation {
            background: #fafafa;
            padding: 0.8rem;
            margin: 0.8rem 0;
            border: 2px solid #000;
            text-align: center;
            break-inside: avoid;
        }

        /* === TABLES === */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
            font-size: 8pt;
            break-inside: avoid;
        }

        th, td {
            border-top: 1px solid #000;
            border-bottom: 1px solid #000;
            border-left: none;
            border-right: none;
            padding: 3px 4px;
            text-align: center;
        }

        th {
            background: #f0f0f0;
            color: #000;
            font-weight: bold;
            font-size: 8pt;
            border-bottom: 2px solid #000;
        }

        tr:last-child td {
            border-bottom: 2px solid #000;
        }

        /* === FIGURES === */
        figure {
            margin: 1rem 0;
            break-inside: avoid;
            text-align: center;
        }

        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }

        figcaption {
            font-size: 9pt;
            color: #000;
            margin-top: 0.5rem;
            text-align: justify;
            text-indent: 0;
            line-height: 1.3;
        }

        figcaption strong {
            font-weight: bold;
        }

        /* === REFERENCES === */
        .references {
            margin-top: 1.5rem;
            padding-top: 0.75rem;
            border-top: 1px solid #000;
        }

        .references h2 {
            font-size: 11pt;
            margin-bottom: 0.5rem;
        }

        .references ol {
            font-size: 9pt;
            padding-left: 1.5rem;
            color: #000;
            line-height: 1.2;
        }

        .references li {
            margin-bottom: 0.3rem;
        }

        /* === CODE === */
        code {
            font-family: 'Courier New', Courier, monospace;
            font-size: 8pt;
            background: #f5f5f5;
            padding: 1px 3px;
            border-radius: 2px;
        }

        /* === LISTS === */
        ul, ol {
            margin: 0.5rem 0;
            padding-left: 1.2rem;
        }

        li {
            margin-bottom: 0.3rem;
        }

        /* === LINKS === */
        a {
            color: #000;
            text-decoration: underline;
        }

        /* === DOI BADGE === */
        .doi-badge {
            font-family: 'Lato', sans-serif;
            font-size: 9px;
            color: #666;
            position: absolute;
            top: 10px;
            right: 20px;
            background: #fdfdfd;
            padding: 2px 5px;
            border: 1px solid #eee;
            border-radius: 3px;
            z-index: 1000;
        }

        /* === PRINT === */
        @media print {
            body {
                padding: 0;
                margin: 0;
                font-size: 10pt;
            }

            @page {
                size: A4;
                margin: 2cm;
            }

            a {
                color: #000;
                text-decoration: none;
            }

            .doi-badge {
                display: none;
            }
        }
"""

def update_treatise_styles(filepath):
    """Atualiza os estilos de um treatise para seguir os padrões"""
    print(f"Processando: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar e substituir a seção <style>
    style_pattern = r'<style>.*?</style>'
    new_style = f'<style>{CSS_STANDARDS}    </style>'
    
    content_updated = re.sub(style_pattern, new_style, content, flags=re.DOTALL)
    
    # Atualizar classes do abstract
    content_updated = content_updated.replace('class="abstract"', 'class="abstract"><span class="abstract-title">Abstract</span>')
    
    # Remover .content-wrapper se existir (layout de duas colunas)
    content_updated = content_updated.replace('<div class="content-wrapper">', '')
    content_updated = content_updated.replace('</div>\n</body>', '</body>')
    
    # Salvar
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_updated)
    
    print(f"  ✓ Atualizado: {filepath.name}")
    return True

def main():
    print("=" * 80)
    print("APLICANDO PADRÕES TAMESIS AOS 12 TREATISES CANÔNICOS")
    print("=" * 80)
    print()
    
    treatises = sorted(CANON_DIR.glob("Treatise_*.html"))
    
    if not treatises:
        print("❌ Nenhum treatise encontrado!")
        return
    
    print(f"Encontrados {len(treatises)} treatises:")
    for t in treatises:
        print(f"  - {t.name}")
    print()
    
    print("Aplicando padrões...")
    print()
    
    success_count = 0
    for treatise in treatises:
        try:
            if update_treatise_styles(treatise):
                success_count += 1
        except Exception as e:
            print(f"  ❌ Erro em {treatise.name}: {e}")
    
    print()
    print("=" * 80)
    print(f"CONCLUÍDO: {success_count}/{len(treatises)} treatises atualizados")
    print("=" * 80)
    print()
    print("Padrões aplicados:")
    print("  ✓ Fonte: Times New Roman 10pt")
    print("  ✓ Line-height: 1.15")
    print("  ✓ Margens: 1.5cm")
    print("  ✓ H1: 16pt negrito")
    print("  ✓ H2: 11pt maiúsculo com borda")
    print("  ✓ H3: 10pt negrito")
    print("  ✓ H4: 10pt itálico")
    print("  ✓ Abstract: 9pt com bordas")
    print("  ✓ Tabelas: 8pt com headers #f0f0f0")
    print("  ✓ Equações: Bordas 2px")
    print("  ✓ Referências: 9pt line-height 1.2")
    print("  ✓ Layout: Coluna única (removido duas colunas)")

if __name__ == "__main__":
    main()
