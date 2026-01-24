#!/usr/bin/env python3
"""
SCRIPT DE INSTALAÇÃO DAS BIBLIOTECAS ESPECIALIZADAS
Para o Sistema de Física Teórica V3.0

Este script ajuda a instalar as bibliotecas especializadas necessárias
para funcionalidades avançadas do sistema.
"""

import subprocess
import sys
import os
from typing import List, Dict, Tuple

class SpecializedLibrariesInstaller:
    """Instalador de bibliotecas especializadas para física"""

    def __init__(self):
        self.libraries = {
            'qutip': {
                'name': 'QuTiP (Quantum Toolbox in Python)',
                'description': 'Computação quântica e informação quântica',
                'install_cmd': 'pip install qutip',
                'importance': 'Alta',
                'size': '~50MB'
            },
            'astropy': {
                'name': 'Astropy',
                'description': 'Astronomia e astrofísica',
                'install_cmd': 'pip install astropy',
                'importance': 'Alta',
                'size': '~100MB'
            },
            'pyscf': {
                'name': 'PySCF',
                'description': 'Química quântica computacional',
                'install_cmd': 'pip install pyscf',
                'importance': 'Média-Alta',
                'size': '~200MB'
            },
            'fenics': {
                'name': 'FEniCS',
                'description': 'Métodos de elementos finitos',
                'install_cmd': 'pip install fenics-ffc',
                'importance': 'Média',
                'size': '~500MB'
            },
            'gwpy': {
                'name': 'GWpy',
                'description': 'Ondas gravitacionais',
                'install_cmd': 'pip install gwpy',
                'importance': 'Média',
                'size': '~100MB'
            },
            'cupy': {
                'name': 'CuPy',
                'description': 'GPU computing com CUDA',
                'install_cmd': 'pip install cupy-cuda11x',
                'importance': 'Opcional',
                'size': '~1GB'
            },
            'tensorflow': {
                'name': 'TensorFlow',
                'description': 'Machine learning para física',
                'install_cmd': 'pip install tensorflow',
                'importance': 'Opcional',
                'size': '~500MB'
            },
            'pytorch': {
                'name': 'PyTorch',
                'description': 'Deep learning alternativo',
                'install_cmd': 'pip install torch torchvision',
                'importance': 'Opcional',
                'size': '~2GB'
            }
        }

    def check_library_availability(self, library_name: str) -> bool:
        """Verificar se uma biblioteca está disponível"""
        try:
            if library_name == 'qutip':
                import qutip
            elif library_name == 'astropy':
                import astropy
            elif library_name == 'pyscf':
                import pyscf
            elif library_name == 'fenics':
                import fenics
            elif library_name == 'gwpy':
                import gwpy
            elif library_name == 'cupy':
                import cupy
            elif library_name == 'tensorflow':
                import tensorflow
            elif library_name == 'pytorch':
                import torch
            return True
        except ImportError:
            return False

    def install_library(self, library_name: str) -> Tuple[bool, str]:
        """Instalar uma biblioteca específica"""
        if library_name not in self.libraries:
            return False, f"Biblioteca '{library_name}' não encontrada"

        library_info = self.libraries[library_name]

        print(f"\n📦 Instalando {library_info['name']}...")
        print(f"   Descrição: {library_info['description']}")
        print(f"   Tamanho aproximado: {library_info['size']}")
        print(f"   Comando: {library_info['install_cmd']}")

        try:
            # Executar comando de instalação
            result = subprocess.run(
                library_info['install_cmd'].split(),
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos timeout
            )

            if result.returncode == 0:
                # Verificar se a instalação foi bem-sucedida
                if self.check_library_availability(library_name):
                    return True, "Instalação bem-sucedida!"
                else:
                    return False, "Instalação falhou - biblioteca não encontrada após instalação"
            else:
                return False, f"Erro na instalação: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Timeout na instalação"
        except Exception as e:
            return False, f"Erro inesperado: {str(e)}"

    def install_all_essential(self) -> Dict[str, Tuple[bool, str]]:
        """Instalar todas as bibliotecas essenciais"""
        essential_libs = ['qutip', 'astropy', 'pyscf']
        results = {}

        print("🚀 INSTALANDO BIBLIOTECAS ESSENCIAIS")
        print("=" * 50)

        for lib in essential_libs:
            success, message = self.install_library(lib)
            results[lib] = (success, message)

            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {lib}: {message}")

        return results

    def show_status(self) -> None:
        """Mostrar status de todas as bibliotecas"""
        print("\n📊 STATUS DAS BIBLIOTECAS ESPECIALIZADAS")
        print("=" * 60)

        for lib_name, lib_info in self.libraries.items():
            available = self.check_library_availability(lib_name)
            status_icon = "✅" if available else "❌"
            importance_icon = "🔥" if lib_info['importance'] == 'Alta' else "⚡" if lib_info['importance'] == 'Média-Alta' else "🔄"

            print(f"{status_icon} {importance_icon} {lib_info['name']}")
            print(f"   Status: {'Instalada' if available else 'Não instalada'}")
            print(f"   Importância: {lib_info['importance']}")
            print(f"   Descrição: {lib_info['description']}")
            print()

    def create_installation_script(self, filename: str = "install_specialized_libs.sh") -> None:
        """Criar script de instalação para sistemas Linux/Mac"""
        script_content = """#!/bin/bash
# Script de instalação das bibliotecas especializadas
# para o Sistema de Física Teórica V3.0

echo "🚀 Instalando bibliotecas especializadas para física..."
echo "=================================================="

# Atualizar pip
pip install --upgrade pip

# Instalar bibliotecas essenciais
echo "📦 Instalando bibliotecas essenciais..."

# QuTiP - Quantum computing
echo "🔬 Instalando QuTiP (Quantum Toolbox)..."
pip install qutip

# Astropy - Astronomy
echo "🌌 Instalando Astropy..."
pip install astropy

# PySCF - Quantum chemistry
echo "🧪 Instalando PySCF..."
pip install pyscf

# Bibliotecas opcionais
echo "🔄 Instalando bibliotecas opcionais..."

# FEniCS - Finite elements (pode ser complexo de instalar)
echo "🔧 Instalando FEniCS (pode falhar em alguns sistemas)..."
pip install fenics-ffc || echo "FEniCS não pôde ser instalado automaticamente"

# GWpy - Gravitational waves
echo "🌊 Instalando GWpy..."
pip install gwpy || echo "GWpy não pôde ser instalado"

# GPU support (opcional)
echo "💻 Instalando suporte a GPU (opcional)..."
pip install cupy-cuda11x || echo "CuPy não pôde ser instalado (GPU não disponível?)"

echo ""
echo "✅ Instalação concluída!"
echo "🔍 Execute 'python -c \"from src.physics_specialized_modules import SpecializedPhysicsModules; print(SpecializedPhysicsModules().get_available_modules())\"' para verificar."
"""

        with open(filename, 'w') as f:
            f.write(script_content)

        # Tornar executável no Linux/Mac
        if os.name != 'nt':  # Não Windows
            os.chmod(filename, 0o755)

        print(f"📝 Script de instalação criado: {filename}")


def main():
    """Função principal do instalador"""
    print("🛠️ INSTALADOR DE BIBLIOTECAS ESPECIALIZADAS")
    print("Sistema de Física Teórica V3.0")
    print("=" * 50)

    installer = SpecializedLibrariesInstaller()

    while True:
        print("\nOpções:")
        print("1. Mostrar status atual")
        print("2. Instalar biblioteca específica")
        print("3. Instalar bibliotecas essenciais")
        print("4. Criar script de instalação")
        print("5. Sair")

        try:
            choice = input("\nEscolha uma opção (1-5): ").strip()

            if choice == '1':
                installer.show_status()

            elif choice == '2':
                print("\nBibliotecas disponíveis:")
                for i, (lib_name, lib_info) in enumerate(installer.libraries.items(), 1):
                    print(f"{i}. {lib_info['name']} - {lib_info['description']}")

                try:
                    lib_choice = input("\nDigite o nome da biblioteca: ").strip().lower()
                    if lib_choice in installer.libraries:
                        success, message = installer.install_library(lib_choice)
                        print(f"\nResultado: {'✅' if success else '❌'} {message}")
                    else:
                        print("❌ Biblioteca não encontrada")
                except KeyboardInterrupt:
                    continue

            elif choice == '3':
                results = installer.install_all_essential()
                successful = sum(1 for success, _ in results.values() if success)
                total = len(results)
                print(f"\n📊 Resultado: {successful}/{total} bibliotecas instaladas com sucesso")

            elif choice == '4':
                script_name = input("Nome do script (padrão: install_specialized_libs.sh): ").strip()
                if not script_name:
                    script_name = "install_specialized_libs.sh"
                installer.create_installation_script(script_name)

            elif choice == '5':
                print("\n👋 Até logo!")
                break

            else:
                print("❌ Opção inválida")

        except KeyboardInterrupt:
            print("\n\n👋 Instalação interrompida pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
