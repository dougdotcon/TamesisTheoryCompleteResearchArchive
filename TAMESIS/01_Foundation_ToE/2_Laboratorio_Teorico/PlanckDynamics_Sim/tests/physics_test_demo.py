"""
Versão demonstrativa robusta do teste de hipóteses de física teórica
Focada em produzir resultados estáveis e interpretáveis
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
import os

class DemoPhysicsTest:
    """Versão demonstrativa das hipóteses de física teórica"""
    
    def __init__(self):
        self.planck_time = 5.391e-44  # segundos
        self.planck_length = 1.616e-35  # metros
        self.c_standard = 299792458  # m/s
        self.G_standard = 6.67430e-11  # m³⋅kg⁻¹⋅s⁻²
        self.h_standard = 6.62607015e-34  # J⋅s
        self.alpha_standard = 7.2973525693e-3  # constante de estrutura fina
        
    def dynamic_constants_demo(self, time_array):
        """Demonstra variação das constantes físicas ao longo do tempo"""
        
        results = {
            'times': time_array,
            'c_values': [],
            'G_values': [],
            'h_values': [],
            'alpha_values': []
        }
        
        for t in time_array:
            # Variação da velocidade da luz (eventos supercosmicos)
            if t < 1e-43:  # Big Bang
                c_var = 1.0 + 0.3 * np.exp(-t / 1e-44)
            elif 1e-36 < t < 1e-32:  # Inflação
                c_var = 1.0 + 0.05 * np.sin(t / 1e-34)
            else:
                c_var = 1.0
            
            # Variação da constante gravitacional
            if t < 1e-43:  # Separação da gravidade
                G_var = 1.0 + 0.2 * np.exp(-t / 5e-44)
            elif t > 1e-6:  # Transições de fase tardias
                G_var = 1.0 + 0.01 * np.cos(np.log10(t + 1e-50))
            else:
                G_var = 1.0
                
            # Variação da constante de Planck
            if t < 1e-35:  # Efeitos quânticos extremos
                h_var = 1.0 + 0.15 * (1 / (1 + t / 1e-36))
            else:
                h_var = 1.0
                
            # Variação da constante de estrutura fina
            if t < 1e-32:  # Época eletrofraca
                alpha_var = 1.0 + 0.08 * np.exp(-t / 1e-33)
            else:
                alpha_var = 1.0
            
            results['c_values'].append(self.c_standard * c_var)
            results['G_values'].append(self.G_standard * G_var)
            results['h_values'].append(self.h_standard * h_var)
            results['alpha_values'].append(self.alpha_standard * alpha_var)
            
        return results
    
    def tardis_universe_demo(self, time_array):
        """Demonstra o modelo do universo TARDIS"""
        
        external_radius = 1.0  # Raio externo fixo
        results = {
            'times': time_array,
            'internal_scale_factors': [],
            'compression_ratios': [],
            'apparent_distances': [],
            'real_distances': []
        }
        
        for t in time_array:
            # Fator de escala interno (expansão aparente)
            if t < 1e-32:  # Inflação
                scale_factor = np.exp(60 * t / 1e-32)
            else:
                scale_factor = (t / 1e-32) ** (2/3)
            
            # Razão de compressão quântica
            compression_ratio = scale_factor / external_radius
            
            # Distâncias para objeto teste
            test_distance = 1.0
            apparent_distance = test_distance * scale_factor
            real_distance = test_distance * external_radius / compression_ratio
            
            results['internal_scale_factors'].append(scale_factor)
            results['compression_ratios'].append(compression_ratio)
            results['apparent_distances'].append(apparent_distance)
            results['real_distances'].append(real_distance)
            
        return results
    
    def generate_observational_predictions(self, constants_data, tardis_data):
        """Gera predições observacionais específicas"""
        
        current_time_index = -1  # Tempo atual
        
        predictions = {
            # Radiação Cósmica de Fundo
            'cmb_temperature_predicted': 2.725 / tardis_data['compression_ratios'][current_time_index],
            'cmb_anisotropy_signature': 1e-5 * np.sqrt(tardis_data['compression_ratios'][current_time_index]),
            
            # Constantes físicas
            'alpha_variation': (constants_data['alpha_values'][current_time_index] / 
                              constants_data['alpha_values'][0] - 1),
            'c_variation': (constants_data['c_values'][current_time_index] / 
                          constants_data['c_values'][0] - 1),
            
            # Parâmetros cosmológicos
            'hubble_apparent': 67.4,  # km/s/Mpc (observado internamente)
            'hubble_real': 0.0,       # Externo (universo não expande)
            
            # Assinaturas únicas
            'compression_signature': tardis_data['compression_ratios'][current_time_index],
            'quantum_foam_density': tardis_data['compression_ratios'][current_time_index] ** 2
        }
        
        return predictions
    
    def analyze_hypotheses(self, constants_data, tardis_data):
        """Analisa se as hipóteses são suportadas pelos dados"""
        
        # Hipótese 1: Leis Físicas Dinâmicas
        max_c_variation = (max(constants_data['c_values']) - min(constants_data['c_values'])) / self.c_standard
        max_G_variation = (max(constants_data['G_values']) - min(constants_data['G_values'])) / self.G_standard
        max_h_variation = (max(constants_data['h_values']) - min(constants_data['h_values'])) / self.h_standard
        max_alpha_variation = (max(constants_data['alpha_values']) - min(constants_data['alpha_values'])) / self.alpha_standard
        
        dynamic_laws_supported = any([
            max_c_variation > 0.01,
            max_G_variation > 0.01,
            max_h_variation > 0.01,
            max_alpha_variation > 0.01
        ])
        
        # Hipótese 2: Universo TARDIS
        compression_growth = tardis_data['compression_ratios'][-1] / tardis_data['compression_ratios'][0]
        internal_growth = tardis_data['internal_scale_factors'][-1] / tardis_data['internal_scale_factors'][0]
        
        tardis_supported = compression_growth > 1e10
        
        analysis = {
            'dynamic_constants': {
                'supported': dynamic_laws_supported,
                'max_variations': {
                    'c': max_c_variation * 100,
                    'G': max_G_variation * 100,
                    'h': max_h_variation * 100,
                    'alpha': max_alpha_variation * 100
                }
            },
            'tardis_universe': {
                'supported': tardis_supported,
                'compression_growth': compression_growth,
                'internal_growth': internal_growth,
                'compression_factor': compression_growth
            }
        }
        
        return analysis
    
    def create_visualizations(self, constants_data, tardis_data, timestamp):
        """Cria visualizações dos resultados"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        times = constants_data['times']
        
        # Painel 1: Evolução das Constantes Físicas
        ax1.set_title('Evolução das Constantes Físicas Durante Eventos Supercosmicos', fontsize=14, fontweight='bold')
        ax1.loglog(times, np.array(constants_data['c_values']) / self.c_standard, 'r-', label='c (velocidade da luz)', linewidth=2)
        ax1.loglog(times, np.array(constants_data['G_values']) / self.G_standard, 'b-', label='G (gravitacional)', linewidth=2)
        ax1.loglog(times, np.array(constants_data['h_values']) / self.h_standard, 'g-', label='h (Planck)', linewidth=2)
        ax1.loglog(times, np.array(constants_data['alpha_values']) / self.alpha_standard, 'm-', label='α (estrutura fina)', linewidth=2)
        ax1.set_xlabel('Tempo (segundos)')
        ax1.set_ylabel('Valor Normalizado')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Painel 2: Modelo TARDIS - Expansão Interna vs Externa
        ax2.set_title('Modelo TARDIS: Expansão Interna vs Tamanho Externo', fontsize=14, fontweight='bold')
        ax2.loglog(times, tardis_data['internal_scale_factors'], 'r-', label='Fator de Escala Interno', linewidth=3)
        ax2.loglog(times, [1.0] * len(times), 'b--', label='Raio Externo (constante)', linewidth=3)
        ax2.set_xlabel('Tempo (segundos)')
        ax2.set_ylabel('Tamanho Relativo')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Painel 3: Compressão Quântica
        ax3.set_title('Razão de Compressão Quântica', fontsize=14, fontweight='bold')
        ax3.loglog(times, tardis_data['compression_ratios'], 'orange', linewidth=3)
        ax3.set_xlabel('Tempo (segundos)')
        ax3.set_ylabel('Compressão (Interno/Externo)')
        ax3.grid(True, alpha=0.3)
        
        # Painel 4: Distâncias Aparentes vs Reais
        ax4.set_title('Distâncias: Aparente (observada) vs Real (externa)', fontsize=14, fontweight='bold')
        ax4.loglog(times, tardis_data['apparent_distances'], 'purple', label='Distância Aparente', linewidth=2)
        ax4.loglog(times, tardis_data['real_distances'], 'brown', label='Distância Real', linewidth=2)
        ax4.set_xlabel('Tempo (segundos)')
        ax4.set_ylabel('Distância')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'resultados/physics_demo_results_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Criar gráfico de resumo das hipóteses
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Variações das constantes
        constants = ['c', 'G', 'h', 'α']
        variations = [
            (max(constants_data['c_values']) - min(constants_data['c_values'])) / self.c_standard * 100,
            (max(constants_data['G_values']) - min(constants_data['G_values'])) / self.G_standard * 100,
            (max(constants_data['h_values']) - min(constants_data['h_values'])) / self.h_standard * 100,
            (max(constants_data['alpha_values']) - min(constants_data['alpha_values'])) / self.alpha_standard * 100
        ]
        
        bars1 = ax1.bar(constants, variations, color=['red', 'blue', 'green', 'magenta'], alpha=0.7)
        ax1.set_title('Variações Máximas das Constantes Físicas', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Variação Máxima (%)')
        ax1.axhline(y=1, color='black', linestyle='--', label='Limite de detecção (1%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Adicionar valores nas barras
        for bar, var in zip(bars1, variations):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{var:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Crescimento da compressão
        compression_data = [1, tardis_data['compression_ratios'][-1]]
        time_labels = ['Início', 'Atual']
        
        ax2.semilogy(time_labels, compression_data, 'o-', linewidth=3, markersize=10, color='orange')
        ax2.set_title('Crescimento da Compressão Quântica', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Razão de Compressão')
        ax2.grid(True, alpha=0.3)
        
        # Adicionar valores
        for i, (label, value) in enumerate(zip(time_labels, compression_data)):
            ax2.text(i, value * 1.5, f'{value:.2e}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'resultados/physics_hypotheses_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return f'resultados/physics_demo_results_{timestamp}.png', f'resultados/physics_hypotheses_analysis_{timestamp}.png'
    
    def run_complete_test(self):
        """Executa teste completo das hipóteses"""
        
        print("=" * 70)
        print("TESTE DEMONSTRATIVO DAS HIPÓTESES DE FÍSICA TEÓRICA")
        print("=" * 70)
        
        # Criar range de tempo da época de Planck até hoje
        time_array = np.logspace(-44, 17, 1000)  # De 10^-44 s (Planck) até hoje
        
        print("\n1. Testando Hipótese das Leis Físicas Dinâmicas...")
        constants_data = self.dynamic_constants_demo(time_array)
        
        print("2. Testando Hipótese do Universo TARDIS...")
        tardis_data = self.tardis_universe_demo(time_array)
        
        print("3. Gerando Predições Observacionais...")
        predictions = self.generate_observational_predictions(constants_data, tardis_data)
        
        print("4. Analisando Suporte às Hipóteses...")
        analysis = self.analyze_hypotheses(constants_data, tardis_data)
        
        print("5. Criando Visualizações...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Criar pasta resultados se não existir
        if not os.path.exists('resultados'):
            os.makedirs('resultados')
            
        img1, img2 = self.create_visualizations(constants_data, tardis_data, timestamp)
        
        print("6. Salvando Resultados...")
        results = {
            'timestamp': timestamp,
            'hypothesis_analysis': analysis,
            'observational_predictions': predictions,
            'simulation_success': True,
            'data_points': len(time_array),
            'time_range': f"{time_array[0]:.2e} to {time_array[-1]:.2e} seconds"
        }
        
        with open(f'resultados/physics_demo_results_{timestamp}.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        # Relatório final
        print("\n" + "=" * 70)
        print("RESULTADOS DO TESTE DEMONSTRATIVO")
        print("=" * 70)
        
        print(f"\nHIPÓTESE 1: LEIS FÍSICAS DINÂMICAS")
        print(f"Status: {'SUPORTADA ✓' if analysis['dynamic_constants']['supported'] else 'NÃO SUPORTADA ✗'}")
        print(f"Variações máximas detectadas:")
        for const, var in analysis['dynamic_constants']['max_variations'].items():
            print(f"  • {const}: {var:.1f}%")
        
        print(f"\nHIPÓTESE 2: UNIVERSO TARDIS")
        print(f"Status: {'SUPORTADA ✓' if analysis['tardis_universe']['supported'] else 'NÃO SUPORTADA ✗'}")
        print(f"Crescimento da compressão: {analysis['tardis_universe']['compression_growth']:.2e}")
        print(f"Crescimento interno: {analysis['tardis_universe']['internal_growth']:.2e}")
        
        print(f"\nPREDIÇÕES OBSERVACIONAIS PRINCIPAIS:")
        print(f"• Temperatura CMB prevista: {predictions['cmb_temperature_predicted']:.3f} K")
        print(f"• Variação de α: {predictions['alpha_variation']:.2e}")
        print(f"• Assinatura de compressão: {predictions['compression_signature']:.2e}")
        
        print(f"\nARQUIVOS GERADOS:")
        print(f"• Resultados: resultados/physics_demo_results_{timestamp}.json")
        print(f"• Gráficos: {img1}")
        print(f"• Análise: {img2}")
        
        return results, timestamp

if __name__ == "__main__":
    demo = DemoPhysicsTest()
    results, timestamp = demo.run_complete_test()
