"""
Modelo do Universo TAMESIS - Hipótese de dimensão externa constante
com expansão interna aparente

Baseado na ideia de que o universo mantém tamanho constante quando observado
de fora, mas expande internamente (efeito quântico dimensional)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Dict
from scipy.integrate import odeint
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TARDISUniverse:
    """
    Modelo do universo com dimensão externa fixa e expansão interna
    """
    
    def __init__(self, external_radius: float = 1.0):
        """
        Args:
            external_radius: Raio externo fixo do universo (unidades arbitrárias)
        """
        self.external_radius = external_radius
        self.planck_length = 1.616e-35  # metros
        self.planck_time = 5.391e-44    # segundos
        
        # Parâmetros do modelo TAMESIS
        self.quantum_compression_factor = 1.0
        self.internal_metric_tensor = np.eye(4)  # Métrica interna 4D
        
    def internal_scale_factor(self, time: float) -> float:
        """
        Fator de escala interno - como o espaço se expande internamente
        
        Args:
            time: Tempo cosmológico (em unidades de Planck)
            
        Returns:
            Fator de escala interno
        """
        if time <= 0:
            return 1e-50  # Tamanho inicial minúsculo
            
        # Expansão inflacionária seguida de expansão mais lenta
        if time < 1e-32:  # Época inflacionária
            return np.exp(60 * time / 1e-32)  # Inflação exponencial
        else:
            # Expansão tipo lei de potência após inflação
            return (time / 1e-32) ** (2/3)  # Expansão dominada por radiação/matéria
    
    def quantum_compression_ratio(self, time: float) -> float:
        """
        Razão de compressão quântica - como mais espaço é "empacotado"
        dentro do mesmo volume externo
        
        Args:
            time: Tempo cosmológico
            
        Returns:
            Razão de compressão (espaço interno / espaço externo)
        """
        internal_scale = self.internal_scale_factor(time)
        
        # O universo "aprende" a comprimir mais espaço no mesmo volume
        compression = internal_scale / self.external_radius
        
        return compression
    
    def apparent_vs_real_distance(self, time: float, 
                                 comoving_distance: float) -> Tuple[float, float]:
        """
        Calcula distância aparente (observada internamente) vs real (externa)
        
        Args:
            time: Tempo cosmológico
            comoving_distance: Distância comóvel
            
        Returns:
            (distância_aparente, distância_real)
        """
        scale_factor = self.internal_scale_factor(time)
        compression = self.quantum_compression_ratio(time)
        
        # Distância aparente (o que medimos de dentro)
        apparent_distance = comoving_distance * scale_factor
        
        # Distância real (se pudéssemos ver de fora)
        real_distance = comoving_distance * self.external_radius / compression
        
        return apparent_distance, real_distance
    
    def hubble_parameter_internal(self, time: float) -> float:
        """
        Parâmetro de Hubble aparente (medido internamente)
        
        Args:
            time: Tempo cosmológico
            
        Returns:
            H(t) interno
        """
        dt = time * 1e-10  # Pequeno incremento
        scale_now = self.internal_scale_factor(time)
        scale_future = self.internal_scale_factor(time + dt)
        
        # H = (da/dt) / a
        hubble = (scale_future - scale_now) / (dt * scale_now)
        
        return hubble
    
    def hubble_parameter_external(self, time: float) -> float:
        """
        Parâmetro de Hubble real (se observado externamente)
        
        Args:
            time: Tempo cosmológico
            
        Returns:
            H(t) externo (deveria ser ~0 se o universo não expande externamente)
        """
        # Se o universo não expande externamente, H_externo ≈ 0
        return 0.0
    
    def cosmic_microwave_background_prediction(self, time: float) -> Dict:
        """
        Predições para a radiação cósmica de fundo no modelo TAMESIS
        
        Args:
            time: Tempo atual
            
        Returns:
            Dicionário com predições da CMB
        """
        scale_factor = self.internal_scale_factor(time)
        compression = self.quantum_compression_ratio(time)
        
        # Temperatura da CMB
        # No modelo padrão: T ∝ 1/a
        # No modelo TAMESIS: T ∝ 1/(a_interno)
        T_cmb = 2.7 / scale_factor  # Kelvin
        
        # Anisotropias podem ser diferentes devido à compressão quântica
        anisotropy_amplitude = 1e-5 * np.sqrt(compression)
        
        return {
            'temperature': T_cmb,
            'anisotropy_amplitude': anisotropy_amplitude,
            'compression_signature': compression
        }
    
    def observational_signatures(self, time_range: np.ndarray) -> Dict:
        """
        Calcula assinaturas observacionais que distinguem o modelo TAMESIS
        do modelo padrão
        
        Args:
            time_range: Array de tempos para análise
            
        Returns:
            Dicionário com assinaturas observacionais
        """
        signatures = {
            'times': time_range,
            'internal_hubble': [],
            'external_hubble': [],
            'compression_ratio': [],
            'apparent_distances': [],
            'real_distances': []
        }
        
        test_distance = 1.0  # Distância de teste
        
        for t in time_range:
            signatures['internal_hubble'].append(self.hubble_parameter_internal(t))
            signatures['external_hubble'].append(self.hubble_parameter_external(t))
            signatures['compression_ratio'].append(self.quantum_compression_ratio(t))
            
            app_dist, real_dist = self.apparent_vs_real_distance(t, test_distance)
            signatures['apparent_distances'].append(app_dist)
            signatures['real_distances'].append(real_dist)
        
        return signatures
    
    def plot_tardis_evolution(self, time_range: np.ndarray):
        """
        Visualiza a evolução do universo TAMESIS
        
        Args:
            time_range: Range de tempo para plotar
        """
        signatures = self.observational_signatures(time_range)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Parâmetro de Hubble (Interno vs Externo)',
                'Razão de Compressão Quântica',
                'Distâncias: Aparente vs Real',
                'Fator de Escala vs Raio Externo'
            )
        )
        
        # Parâmetro de Hubble
        fig.add_trace(
            go.Scatter(x=time_range, y=signatures['internal_hubble'],
                      name='H interno', line=dict(color='red')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_range, y=signatures['external_hubble'],
                      name='H externo', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Razão de compressão
        fig.add_trace(
            go.Scatter(x=time_range, y=signatures['compression_ratio'],
                      name='Compressão', line=dict(color='green')),
            row=1, col=2
        )
        
        # Distâncias
        fig.add_trace(
            go.Scatter(x=time_range, y=signatures['apparent_distances'],
                      name='Distância Aparente', line=dict(color='orange')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=time_range, y=signatures['real_distances'],
                      name='Distância Real', line=dict(color='purple')),
            row=2, col=1
        )
        
        # Fator de escala
        scale_factors = [self.internal_scale_factor(t) for t in time_range]
        external_radii = [self.external_radius] * len(time_range)
        
        fig.add_trace(
            go.Scatter(x=time_range, y=scale_factors,
                      name='Fator Escala Interno', line=dict(color='red')),
            row=2, col=2
        )
        fig.add_trace(
            go.Scatter(x=time_range, y=external_radii,
                      name='Raio Externo', line=dict(color='blue')),
            row=2, col=2
        )
        
        fig.update_xaxes(type="log", title_text="Tempo (unidades de Planck)")
        fig.update_layout(
            title_text="Modelo do Universo TAMESIS - Evolução Temporal",
            height=800
        )
        
        fig.show()

if __name__ == "__main__":
    # Teste do modelo TAMESIS
    TAMESIS = TARDISUniverse(external_radius=1.0)
    
    # Range de tempo da época de Planck até hoje
    time_range = np.logspace(-50, 18, 1000)  # 10^-50 a 10^18 unidades de Planck
    
    # Plotar evolução
    TAMESIS.plot_tardis_evolution(time_range)
    
    # Calcular algumas predições específicas
    current_time = 4.35e17  # Idade atual do universo em unidades de Planck
    cmb_prediction = TAMESIS.cosmic_microwave_background_prediction(current_time)
    
    print("Predições do Modelo TAMESIS para hoje:")
    print(f"Temperatura CMB: {cmb_prediction['temperature']:.2f} K")
    print(f"Amplitude de anisotropia: {cmb_prediction['anisotropy_amplitude']:.2e}")
    print(f"Assinatura de compressão: {cmb_prediction['compression_signature']:.2e}")
    
    # Comparar com observações reais
    print("\nComparação com observações:")
    print(f"CMB observada: 2.725 K")
    print(f"Anisotropia observada: ~1e-5")
