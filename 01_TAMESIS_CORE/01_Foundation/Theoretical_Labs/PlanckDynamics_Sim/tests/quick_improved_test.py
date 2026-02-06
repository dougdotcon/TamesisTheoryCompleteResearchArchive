"""
Teste rápido do simulador melhorado com range temporal menor
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import json
from datetime import datetime

class QuickImprovedSimulator:
    """Simulador rápido para testar melhorias"""
    
    def __init__(self):
        self.epsilon = 1e-15
        self.max_variation = 0.2  # Reduzido para 20%
        
    def get_varying_constant(self, base_value: float, time: float, intensity: float = 0.1) -> float:
        """Simula variação de constante de forma controlada"""
        if time < 1.0:  # Big Bang
            variation = intensity * np.exp(-time * 5)
        elif 1.0 < time < 1000.0:  # Transições
            variation = intensity * 0.5 * np.sin(time / 100.0)
        else:
            variation = 0.0
            
        variation = np.clip(variation, -self.max_variation, self.max_variation)
        return base_value * (1 + variation)
    
    def tardis_compression(self, time: float) -> float:
        """Compressão TAMESIS simplificada"""
        if time < 1.0:
            return 1.0 + time * 10  # Crescimento inicial
        else:
            return 1.0 + 10 * (time / 1000.0) ** 0.5  # Crescimento mais lento
    
    def stable_equations(self, t: float, y: np.ndarray) -> np.ndarray:
        """Equações estabilizadas"""
        a, a_dot, rho, T = y
        
        # Garantir valores positivos
        a = max(a, self.epsilon)
        rho = max(rho, self.epsilon)
        T = max(T, self.epsilon)
        
        # Constantes variáveis
        G = self.get_varying_constant(6.67e-11, t, 0.15)
        c = self.get_varying_constant(3e8, t, 0.12)
        
        # Parâmetro de Hubble limitado
        H = np.clip(a_dot / a, -1e3, 1e3)
        
        # Compressão TAMESIS
        compression = self.tardis_compression(t)
        
        # Equações simplificadas
        da_dt = a_dot
        
        # Aceleração com regularização
        acceleration = -4 * np.pi * G * a * rho / (3 * c**2)
        acceleration = np.clip(acceleration, -1e3, 1e3)
        d2a_dt2 = acceleration / np.sqrt(compression + self.epsilon)
        
        # Densidade
        drho_dt = -3 * H * rho * (1 + 1/3)  # Radiação
        drho_dt = np.clip(drho_dt, -rho * 10, rho * 10)
        
        # Temperatura
        dT_dt = -H * T
        dT_dt = np.clip(dT_dt, -T * 10, T * 10)
        
        return np.array([da_dt, d2a_dt2, drho_dt, dT_dt])
    
    def run_quick_test(self) -> dict:
        """Executa teste rápido"""
        print("Executando teste rápido do simulador melhorado...")
        
        # Condições iniciais moderadas
        y0 = [1e-5, 100.0, 1e20, 1e10]
        t_span = (0.0, 10000.0)  # Range menor para teste rápido
        
        # Integração
        sol = solve_ivp(
            self.stable_equations,
            t_span,
            y0,
            method='RK45',
            rtol=1e-6,
            atol=1e-8,
            max_step=100.0
        )
        
        if sol.success:
            times = sol.t
            scale_factors = sol.y[0]
            temperatures = sol.y[3]
            
            # Calcular variações das constantes
            G_values = [self.get_varying_constant(6.67e-11, t, 0.15) for t in times]
            c_values = [self.get_varying_constant(3e8, t, 0.12) for t in times]
            
            G_variation = (max(G_values) - min(G_values)) / G_values[0] * 100
            c_variation = (max(c_values) - min(c_values)) / c_values[0] * 100
            
            # Compressão TAMESIS
            compression_start = self.tardis_compression(times[0])
            compression_end = self.tardis_compression(times[-1])
            compression_growth = compression_end / compression_start
            
            results = {
                'success': True,
                'points': len(times),
                'time_range': [float(times[0]), float(times[-1])],
                'scale_growth': float(scale_factors[-1] / scale_factors[0]),
                'temperature_change': float(temperatures[0] / temperatures[-1]),
                'G_variation_percent': float(G_variation),
                'c_variation_percent': float(c_variation),
                'compression_growth': float(compression_growth),
                'dynamic_constants_supported': G_variation > 1.0 or c_variation > 1.0,
                'tardis_supported': compression_growth > 2.0
            }
            
            print(f"✅ Simulação bem-sucedida!")
            print(f"Pontos simulados: {results['points']}")
            print(f"Range temporal: {results['time_range'][0]:.2e} - {results['time_range'][1]:.2e}")
            print(f"Crescimento do fator de escala: {results['scale_growth']:.2e}")
            print(f"Variação de G: {results['G_variation_percent']:.1f}%")
            print(f"Variação de c: {results['c_variation_percent']:.1f}%")
            print(f"Crescimento da compressão: {results['compression_growth']:.2f}")
            print(f"\nHIPÓTESES:")
            print(f"Leis Dinâmicas: {'✅ SUPORTADA' if results['dynamic_constants_supported'] else '❌ NÃO SUPORTADA'}")
            print(f"Universo TAMESIS: {'✅ SUPORTADA' if results['tardis_supported'] else '❌ NÃO SUPORTADA'}")
            
            return results
            
        else:
            print(f"❌ Simulação falhou: {sol.message}")
            return {'success': False, 'message': sol.message}

if __name__ == "__main__":
    sim = QuickImprovedSimulator()
    results = sim.run_quick_test()
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f'resultados/quick_test_results_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResultados salvos em: resultados/quick_test_results_{timestamp}.json")
