"""
Configurações do projeto de Física Teórica
"""

import os
from pathlib import Path

# Diretórios
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
RESULTS_DIR = PROJECT_ROOT / "resultados"
ARCHIVE_DIR = PROJECT_ROOT / "archive"
DOCS_DIR = PROJECT_ROOT / "docs"

# Configurações de simulação
SIMULATION_CONFIG = {
    "default_time_span": (0.0, 1e7),
    "default_tolerance": 1e-8,
    "max_variation_percent": 30.0,
    "planck_units": True,
}

# Configurações de visualização
PLOT_CONFIG = {
    "figsize": (16, 12),
    "dpi": 300,
    "style": "seaborn-v0_8",
    "save_format": "png"
}

# Configurações de saída
OUTPUT_CONFIG = {
    "save_json": True,
    "save_numpy": True,
    "save_plots": True,
    "timestamp_format": "%Y%m%d_%H%M%S"
}

# Constantes físicas padrão (valores atuais)
PHYSICS_CONSTANTS = {
    'c': 299792458,           # m/s
    'G': 6.67430e-11,         # m³⋅kg⁻¹⋅s⁻²
    'h': 6.62607015e-34,      # J⋅s
    'k_B': 1.380649e-23,      # J/K
    'alpha': 7.2973525693e-3, # adimensional
}

# Criar diretórios se não existirem
for directory in [RESULTS_DIR, ARCHIVE_DIR, DOCS_DIR]:
    directory.mkdir(exist_ok=True)
