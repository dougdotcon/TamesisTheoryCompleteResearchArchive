#!/usr/bin/env python3
"""
Script para analisar papers .html no repositório Tamesis Theory
- Identifica todos os arquivos .html
- Detecta duplicatas baseado no conteúdo
- Lista arquivos .md sem versão .html
- Gera relatório completo
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict
import re

# Diretório raiz
ROOT_DIR = Path(r"d:\TamesisTheoryCompleteResearchArchive")

# Pastas a ignorar
IGNORE_FOLDERS = {'__pycache__', 'node_modules', '.git', 'venv', 'env'}

def get_file_hash(filepath):
    """Calcula hash MD5 do conteúdo do arquivo"""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            # Remove whitespace para comparação
            content_normalized = re.sub(rb'\s+', b' ', content)
            return hashlib.md5(content_normalized).hexdigest()
    except Exception as e:
        print(f"Erro ao ler {filepath}: {e}")
        return None

def get_title_from_html(filepath):
    """Extrai o título do arquivo HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(10000)  # Primeiros 10KB
            # Busca por título
            title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if title_match:
                return title_match.group(1).strip()
            # Busca por h1
            h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            if h1_match:
                return re.sub(r'<[^>]+>', '', h1_match.group(1)).strip()
    except Exception as e:
        pass
    return "Sem título"

def find_html_files():
    """Encontra todos os arquivos .html"""
    html_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Remove pastas ignoradas
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        
        for file in files:
            if file.endswith('.html'):
                filepath = Path(root) / file
                rel_path = filepath.relative_to(ROOT_DIR)
                html_files.append({
                    'path': filepath,
                    'relative': str(rel_path),
                    'name': file,
                    'dir': Path(root).relative_to(ROOT_DIR)
                })
    return html_files

def find_md_papers():
    """Encontra arquivos .md que parecem ser papers"""
    md_files = []
    paper_keywords = ['paper', 'treatise', 'theory', 'proof', 'validation']
    
    for root, dirs, files in os.walk(ROOT_DIR):
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]
        
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                rel_path = filepath.relative_to(ROOT_DIR)
                
                # Verifica se é um paper baseado no nome ou localização
                is_paper = any(kw in file.lower() for kw in paper_keywords)
                is_paper = is_paper or 'paper' in str(rel_path).lower()
                
                if is_paper:
                    md_files.append({
                        'path': filepath,
                        'relative': str(rel_path),
                        'name': file
                    })
    return md_files

def analyze_duplicates(html_files):
    """Identifica arquivos HTML duplicados por conteúdo"""
    hash_map = defaultdict(list)
    
    print("Calculando hashes dos arquivos HTML...")
    for idx, file_info in enumerate(html_files):
        if idx % 20 == 0:
            print(f"Processando {idx}/{len(html_files)}...")
        
        file_hash = get_file_hash(file_info['path'])
        if file_hash:
            title = get_title_from_html(file_info['path'])
            file_info['hash'] = file_hash
            file_info['title'] = title
            hash_map[file_hash].append(file_info)
    
    # Filtra apenas duplicatas
    duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
    
    return duplicates, hash_map

def check_md_without_html(md_files, html_files):
    """Verifica quais .md não têm versão .html correspondente"""
    html_names = {f['name'].replace('.html', '') for f in html_files}
    html_dirs = {str(f['dir']) for f in html_files}
    
    missing_html = []
    for md in md_files:
        md_name = md['name'].replace('.md', '')
        md_dir = str(md['path'].parent.relative_to(ROOT_DIR))
        
        # Verifica se existe HTML com mesmo nome ou na mesma pasta
        has_html = md_name in html_names or md_dir in html_dirs
        
        if not has_html:
            missing_html.append(md)
    
    return missing_html

def generate_report(html_files, duplicates, missing_html, hash_map):
    """Gera relatório completo"""
    report = []
    
    report.append("=" * 80)
    report.append("RELATÓRIO DE ANÁLISE DE PAPERS - TAMESIS THEORY")
    report.append("=" * 80)
    report.append("")
    
    # Estatísticas gerais
    report.append("## ESTATÍSTICAS GERAIS")
    report.append(f"Total de arquivos .html encontrados: {len(html_files)}")
    report.append(f"Arquivos únicos (por conteúdo): {len(hash_map)}")
    report.append(f"Grupos de duplicatas: {len(duplicates)}")
    report.append(f"Papers .md sem versão .html: {len(missing_html)}")
    report.append("")
    
    # Duplicatas
    if duplicates:
        report.append("=" * 80)
        report.append("## ARQUIVOS DUPLICADOS (MESMO CONTEÚDO)")
        report.append("=" * 80)
        report.append("")
        
        for idx, (file_hash, files) in enumerate(duplicates.items(), 1):
            report.append(f"\n### Grupo {idx} - {len(files)} cópias idênticas")
            report.append(f"Título: {files[0]['title']}")
            report.append(f"Hash: {file_hash}")
            report.append("Arquivos:")
            for f in files:
                report.append(f"  - {f['relative']}")
            report.append("")
    
    # Papers .md sem HTML
    if missing_html:
        report.append("=" * 80)
        report.append("## PAPERS .MD SEM VERSÃO .HTML")
        report.append("=" * 80)
        report.append("")
        for md in missing_html:
            report.append(f"  - {md['relative']}")
        report.append("")
    
    # Lista completa por pasta
    report.append("=" * 80)
    report.append("## LISTA COMPLETA DE PAPERS .HTML POR PASTA")
    report.append("=" * 80)
    report.append("")
    
    by_folder = defaultdict(list)
    for f in html_files:
        by_folder[str(f['dir'])].append(f)
    
    for folder in sorted(by_folder.keys()):
        report.append(f"\n### {folder}")
        for f in sorted(by_folder[folder], key=lambda x: x['name']):
            report.append(f"  - {f['name']}")
    
    return "\n".join(report)

def main():
    print("Iniciando análise do repositório Tamesis Theory...")
    print(f"Diretório raiz: {ROOT_DIR}")
    print()
    
    # Encontrar arquivos
    print("1. Buscando arquivos .html...")
    html_files = find_html_files()
    print(f"   Encontrados: {len(html_files)} arquivos")
    
    print("2. Buscando papers .md...")
    md_files = find_md_papers()
    print(f"   Encontrados: {len(md_files)} arquivos")
    
    # Analisar duplicatas
    print("3. Analisando duplicatas...")
    duplicates, hash_map = analyze_duplicates(html_files)
    print(f"   Encontrados: {len(duplicates)} grupos de duplicatas")
    
    # Verificar .md sem .html
    print("4. Verificando papers .md sem versão .html...")
    missing_html = check_md_without_html(md_files, html_files)
    print(f"   Encontrados: {len(missing_html)} arquivos")
    
    # Gerar relatório
    print("5. Gerando relatório...")
    report = generate_report(html_files, duplicates, missing_html, hash_map)
    
    # Salvar relatório
    report_file = ROOT_DIR / "PAPER_ANALYSIS_REPORT.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n✓ Relatório salvo em: {report_file}")
    print("\nRESUMO:")
    print(f"  - Total de .html: {len(html_files)}")
    print(f"  - Arquivos únicos: {len(hash_map)}")
    print(f"  - Grupos de duplicatas: {len(duplicates)}")
    print(f"  - Papers .md sem .html: {len(missing_html)}")
    
    return report_file

if __name__ == "__main__":
    main()
