#!/usr/bin/env python3
"""
Script de limpeza para o projeto de Física Teórica
Remove arquivos temporários e reorganiza resultados
"""

import os
import shutil
import glob
from pathlib import Path

def clean_project():
    """Limpa arquivos temporários e reorganiza projeto"""
    
    print("🧹 Limpando projeto de Física Teórica...")
    
    # Remover __pycache__
    pycache_dirs = glob.glob("**/__pycache__", recursive=True)
    for pycache in pycache_dirs:
        if os.path.exists(pycache):
            shutil.rmtree(pycache)
            print(f"   ✅ Removido: {pycache}")
    
    # Remover arquivos .pyc
    pyc_files = glob.glob("**/*.pyc", recursive=True)
    for pyc in pyc_files:
        if os.path.exists(pyc):
            os.remove(pyc)
            print(f"   ✅ Removido: {pyc}")
    
    # Remover arquivos temporários
    temp_patterns = ["*.tmp", "*.log", "*.bak", "*~"]
    for pattern in temp_patterns:
        temp_files = glob.glob(f"**/{pattern}", recursive=True)
        for temp in temp_files:
            if os.path.exists(temp):
                os.remove(temp)
                print(f"   ✅ Removido: {temp}")
    
    # Organizar resultados antigos (manter apenas os mais recentes)
    results_dir = Path("resultados")
    if results_dir.exists():
        # Manter apenas os 3 resultados mais recentes de cada tipo
        json_files = sorted(results_dir.glob("physics_test_v2_results_*.json"))
        png_files = sorted(results_dir.glob("physics_test_v2_visualization_*.png"))
        
        # Remover arquivos antigos (manter 3 mais recentes)
        for file_list in [json_files, png_files]:
            if len(file_list) > 3:
                for old_file in file_list[:-3]:
                    old_file.unlink()
                    print(f"   🗂️ Arquivo antigo removido: {old_file.name}")
    
    # Verificar integridade da estrutura
    required_dirs = ["src", "tests", "resultados", "archive", "docs"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir()
            print(f"   📁 Criado diretório: {dir_name}")
    
    # Verificar arquivos essenciais
    essential_files = ["main.py", "README.md", "requirements.txt", "src/__init__.py"]
    missing_files = []
    for file_name in essential_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"   ⚠️ Arquivos essenciais faltando: {missing_files}")
    else:
        print("   ✅ Todos os arquivos essenciais presentes")
    
    print("\n🎉 Limpeza concluída!")
    print("\n📊 Estrutura atual:")
    
    # Mostrar estrutura limpa
    def show_tree(directory, prefix="", max_depth=2, current_depth=0):
        if current_depth >= max_depth:
            return
            
        items = sorted(Path(directory).iterdir())
        dirs = [item for item in items if item.is_dir()]
        files = [item for item in items if item.is_file()]
        
        for i, item in enumerate(dirs + files):
            is_last = i == len(dirs + files) - 1
            current_prefix = "└── " if is_last else "├── "
            print(f"{prefix}{current_prefix}{item.name}")
            
            if item.is_dir() and current_depth < max_depth - 1:
                extension = "    " if is_last else "│   "
                show_tree(item, prefix + extension, max_depth, current_depth + 1)
    
    show_tree(".", max_depth=3)

if __name__ == "__main__":
    clean_project()
