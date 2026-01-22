"""
Constantes físicas fundamentais com capacidade de variação temporal
Baseado na hipótese de leis físicas dinâmicas durante eventos supercosmicos
"""

import numpy as np
from typing import Dict, Callable, Optional
import matplotlib.pyplot as plt

class DynamicPhysicsConstants:
    """
    Classe para modelar constantes físicas que podem variar no tempo
    durante eventos supercosmicos
    """
    
    def __init__(self):
        # Constantes padrão (valores atuais observados)
        self.standard_constants = {
            'c': 299792458,  # velocidade da luz (m/s)
            'h': 6.62607015e-34,  # constante de Planck (J⋅s)
            'G': 6.67430e-11,  # constante gravitacional (m³⋅kg⁻¹⋅s⁻²)
            'k_B': 1.380649e-23,  # constante de Boltzmann (J/K)
            'alpha': 7.2973525693e-3,  # constante de estrutura fina
        }
        
        # Funções de variação temporal para cada constante
        self.variation_functions: Dict[str, Callable] = {}
        
        # Eventos supercosmicos que podem alterar as leis
        self.supercosmic_events = []
        
    def add_supercosmic_event(self, time: float, event_type: str, 
                             affected_constants: list, intensity: float):
        """
        Adiciona um evento supercosmico que pode alterar constantes físicas
        
        Args:
            time: Tempo do evento (em unidades de tempo de Planck)
            event_type: Tipo do evento ('big_bang', 'phase_transition', etc.)
            affected_constants: Lista de constantes afetadas
            intensity: Intensidade do evento (0-1)
        """
        event = {
            'time': time,
            'type': event_type,
            'constants': affected_constants,
            'intensity': intensity
        }
        self.supercosmic_events.append(event)
        
    def set_variation_function(self, constant: str, func: Callable):
        """
        Define uma função de variação temporal para uma constante
        
        Args:
            constant: Nome da constante
            func: Função que recebe tempo e retorna fator de variação
        """
        self.variation_functions[constant] = func
        
    def get_constant(self, constant: str, time: float) -> float:
        """
        Obtém o valor de uma constante em um tempo específico
        
        Args:
            constant: Nome da constante
            time: Tempo (em unidades de Planck)
            
        Returns:
            Valor da constante no tempo especificado
        """
        base_value = self.standard_constants[constant]
        
        if constant in self.variation_functions:
            variation_factor = self.variation_functions[constant](time)
            return base_value * variation_factor
        
        # Aplicar efeitos de eventos supercosmicos
        total_effect = 1.0
        for event in self.supercosmic_events:
            if constant in event['constants']:
                # Efeito decresce com distância temporal do evento
                time_distance = abs(time - event['time'])
                effect_strength = event['intensity'] * np.exp(-time_distance / 1e10)
                total_effect *= (1 + effect_strength * 0.1)  # Variação máxima de 10%
                
        return base_value * total_effect
    
    def planck_epoch_variations(self, time: float) -> Dict[str, float]:
        """
        Calcula variações específicas para a época de Planck
        
        Args:
            time: Tempo desde o Big Bang (unidades de Planck)
            
        Returns:
            Dicionário com todas as constantes no tempo especificado
        """
        constants_at_time = {}
        
        for const_name in self.standard_constants:
            constants_at_time[const_name] = self.get_constant(const_name, time)
            
        return constants_at_time

# Funções de variação específicas para diferentes cenários
def big_bang_variation(time: float) -> float:
    """Variação durante o Big Bang - constantes podem ser muito diferentes"""
    if time < 1e-43:  # Primeira unidade de tempo de Planck
        return 1 + 0.5 * np.exp(-time * 1e43)  # Variação extrema inicial
    elif time < 1e-36:  # Durante época inflacionária
        return 1 + 0.1 * np.sin(time * 1e36)  # Oscilações durante inflação
    return 1.0

def inflation_variation(time: float) -> float:
    """Variação durante inflação cósmica"""
    if 1e-36 < time < 1e-32:  # Época inflacionária
        return 1 + 0.2 * np.sin(time * 1e35)  # Oscilações durante inflação
    return 1.0

def phase_transition_variation(time: float) -> float:
    """Variação durante transições de fase do universo"""
    # Múltiplas transições de fase
    transitions = [1e-12, 1e-6, 1e3]  # Tempos das transições
    total_variation = 1.0
    
    for t_transition in transitions:
        if abs(time - t_transition) < t_transition * 0.1:
            variation = 0.05 * np.exp(-abs(time - t_transition) / (t_transition * 0.01))
            total_variation += variation
            
    return total_variation

if __name__ == "__main__":
    # Exemplo de uso
    physics = DynamicPhysicsConstants()
    
    # Adicionar eventos supercosmicos
    physics.add_supercosmic_event(0, 'big_bang', ['c', 'G', 'h'], 1.0)
    physics.add_supercosmic_event(1e-32, 'inflation_end', ['h', 'alpha'], 0.8)
    physics.add_supercosmic_event(1e-6, 'electroweak_transition', ['alpha'], 0.6)
    
    # Definir funções de variação
    physics.set_variation_function('c', big_bang_variation)
    physics.set_variation_function('G', inflation_variation)
    
    # Testar variações ao longo do tempo
    times = np.logspace(-50, 10, 1000)  # De tempo de Planck até hoje
    c_values = [physics.get_constant('c', t) for t in times]
    
    plt.figure(figsize=(12, 8))
    plt.loglog(times, c_values)
    plt.xlabel('Tempo (unidades de Planck)')
    plt.ylabel('Velocidade da luz (m/s)')
    plt.title('Variação da Velocidade da Luz Durante Eventos Supercosmicos')
    plt.grid(True)
    plt.show()
