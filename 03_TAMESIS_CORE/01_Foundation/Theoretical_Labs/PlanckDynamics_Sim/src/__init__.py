"""
Sistema Avançado de Física Teórica V3.0
Época de Planck com Leis Dinâmicas e Universo TAMESIS

Este módulo contém as implementações avançadas para testar:
1. Hipótese de Leis Físicas Dinâmicas (com métodos numéricos avançados)
2. Hipótese do Universo TAMESIS (com compressão quântica)
3. Integração com bibliotecas especializadas (QuTiP, Astropy, PySCF)

Características V3.0:
- Múltiplos métodos numéricos (Runge-Kutta, diferenças finitas, Monte Carlo)
- Validação rigorosa com benchmarking
- Integração com bibliotecas especializadas
- Estrutura modular e bem documentada

Versão: 3.0.0 (Avançada com Integração Especializada)
"""

__version__ = "3.0.0"
__author__ = "Sistema Avançado de Física Teórica"

# Importações principais - V3.0
from .constants_physics import DynamicPhysicsConstants
from .tardis_universe_model import TARDISUniverse
from .main_physics_test_v2 import PhysicsTestSystemV3

# Módulos especializados (opcionais)
try:
    from .physics_specialized_modules import (
        SpecializedPhysicsModules,
        QuantumMechanicsSpecialized,
        AstrophysicsSpecialized,
        QuantumChemistrySpecialized
    )
    _specialized_available = True
except ImportError:
    _specialized_available = False
    # Classes placeholder para quando bibliotecas não estão disponíveis
    class SpecializedPhysicsModules:
        def __init__(self):
            print("⚠️ Módulos especializados não disponíveis. Instale: pip install qutip astropy pyscf")

    class QuantumMechanicsSpecialized:
        pass

    class AstrophysicsSpecialized:
        pass

    class QuantumChemistrySpecialized:
        pass

# Atualizar __all__ baseado na disponibilidade
__all__ = [
    'DynamicPhysicsConstants',
    'TARDISUniverse',
    'PhysicsTestSystemV3'
]

if _specialized_available:
    __all__.extend([
        'SpecializedPhysicsModules',
        'QuantumMechanicsSpecialized',
        'AstrophysicsSpecialized',
        'QuantumChemistrySpecialized'
    ])

def get_system_info():
    """Retorna informações sobre o sistema V3.0"""
    info = {
        'version': __version__,
        'author': __author__,
        'specialized_modules': _specialized_available,
        'description': 'Sistema avançado de física teórica com métodos numéricos modernos'
    }

    if _specialized_available:
        # Verificar quais bibliotecas especializadas estão disponíveis
        try:
            specialized = SpecializedPhysicsModules()
            info['available_modules'] = specialized.get_available_modules()
        except:
            info['available_modules'] = 'Erro ao verificar módulos'

    return info
