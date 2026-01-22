#!/usr/bin/env python3
"""
Hipóteses Alternativas: Exploração de Variações do Modelo de Bounce Gravitacional
Implementa diferentes abordagens teóricas para o bounce gravitacional
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from simulacao_campo_escalar_bounce import CampoEscalarBounce
import json
from datetime import datetime

class HipoteseBounceModificado(CampoEscalarBounce):
    """
    Extensão da hipótese original com termos adicionais
    """

    def __init__(self, xi=1e6, alpha=-1e-4, beta=1e-6, gamma=0.1, **kwargs):
        """
        Parâmetros adicionais:
        beta: termo de acoplamento φ³
        gamma: constante cosmológica dinâmica
        """
        super().__init__(xi=xi, alpha=alpha, **kwargs)
        self.beta = beta
        self.gamma = gamma

    def f_phi(self, phi):
        """Função de acoplamento modificada f(φ) = 1 + ξφ² + βφ³ + α(φ⁴/M_Pl²)"""
        return 1.0 + self.xi * phi**2 + self.beta * phi**3 + self.alpha * (phi**4 / self.M_Pl**2)

    def V_phi(self, phi):
        """Potencial com termo de quinta potência para inflação híbrida"""
        m_phi = 1e-6
        lambda_phi = 1e-14  # Acoplamento para inflação
        return 0.5 * m_phi**2 * phi**2 + lambda_phi * phi**4 + self.gamma * phi**5 / self.M_Pl

class HipoteseBounceHolografico(CampoEscalarBounce):
    """
    Bounce baseado em princípios holográficos
    """

    def __init__(self, xi=1e6, alpha=-1e-4, entropia_max=1e100, **kwargs):
        super().__init__(xi=xi, alpha=alpha, **kwargs)
        self.entropia_max = entropia_max

    def sistema_dinamico(self, t, y):
        """
        Sistema com limite holográfico na entropia
        """
        a, rho_m, phi, pi_phi = y

        if a <= 1e-10:
            return [0, 0, 0, 0]

        # Função de acoplamento
        f_val = self.f_phi(phi)
        G_eff = 1.0 / f_val

        # Campo escalar
        phi_dot = pi_phi / a**3
        rho_phi = 0.5 * phi_dot**2 + self.V_phi(phi)

        # Entropia holográfica (estimativa)
        volume = (4/3) * np.pi * a**3
        entropia_atual = rho_m * volume**(2/3)

        # Fator de supressão holográfica
        if entropia_atual > self.entropia_max:
            supressao = self.entropia_max / entropia_atual
            rho_m *= supressao

        # Equações modificadas
        rho_total = rho_m + rho_phi
        H_squared = max(0, (8*np.pi*G_eff/3) * rho_total - self.k_curv/a**2)
        H = np.sqrt(H_squared)

        R = 6 * H_squared

        a_dot = a * H
        rho_m_dot = -3 * H * rho_m
        phi_dot_calc = pi_phi / a**3
        pi_phi_dot = -3 * H * pi_phi - a**3 * (self.dV_dphi(phi) + 0.5 * R * self.df_dphi(phi))

        return [a_dot, rho_m_dot, phi_dot_calc, pi_phi_dot]

class HipoteseBounceQuantico(CampoEscalarBounce):
    """
    Bounce com correções quânticas semiclassicas
    """

    def __init__(self, xi=1e6, alpha=-1e-4, hbar_eff=1e-2, **kwargs):
        super().__init__(xi=xi, alpha=alpha, **kwargs)
        self.hbar_eff = hbar_eff

    def sistema_dinamico(self, t, y):
        """
        Sistema com correções quânticas
        """
        a, rho_m, phi, pi_phi = y

        if a <= 1e-10:
            return [0, 0, 0, 0]

        f_val = self.f_phi(phi)
        G_eff = 1.0 / f_val

        phi_dot = pi_phi / a**3

        # Correção quântica para densidade de energia
        rho_quantum = self.hbar_eff / a**4  # Energia do vácuo quântico
        rho_phi = 0.5 * phi_dot**2 + self.V_phi(phi) + rho_quantum

        rho_total = rho_m + rho_phi
        H_squared = max(0, (8*np.pi*G_eff/3) * rho_total - self.k_curv/a**2)
        H = np.sqrt(H_squared)

        # Correção quântica para equação de Friedmann
        H_squared += self.hbar_eff * (1/a**2) * (1/a**2)  # Correção Wheeler-DeWitt

        R = 6 * H_squared

        a_dot = a * H
        rho_m_dot = -3 * H * rho_m
        phi_dot_calc = pi_phi / a**3
        pi_phi_dot = -3 * H * pi_phi - a**3 * (self.dV_dphi(phi) + 0.5 * R * self.df_dphi(phi))

        return [a_dot, rho_m_dot, phi_dot_calc, pi_phi_dot]

class ExploradorHipoteses:
    """
    Classe para comparar diferentes hipóteses de bounce
    """

    def __init__(self):
        self.hipoteses = {}
        self.resultados = {}

    def adicionar_hipotese(self, nome, modelo):
        """Adiciona uma hipótese para teste"""
        self.hipoteses[nome] = modelo

    def executar_comparacao(self, t_span=(-100, 100)):
        """
        Executa todas as hipóteses e compara resultados
        """
        print("Executando comparacao de hipoteses...")

        for nome, modelo in self.hipoteses.items():
            print(f"\nTestando hipotese: {nome}")
            try:
                modelo.simular(t_span=t_span)
                modelo.imprimir_resultados()

                # Salvar resultados
                self.resultados[nome] = {
                    'parametros': {
                        'xi': modelo.xi,
                        'alpha': modelo.alpha,
                        'M_Pl': modelo.M_Pl,
                        'k_curv': modelo.k_curv
                    },
                    'bounce_properties': modelo.bounce_properties,
                    'sucesso': True
                }

            except Exception as e:
                print(f"ERRO na hipotese {nome}: {e}")
                self.resultados[nome] = {
                    'erro': str(e),
                    'sucesso': False
                }

        return self.resultados

    def plotar_comparacao(self):
        """
        Cria gráficos comparativos das diferentes hipóteses
        """
        if not self.resultados:
            print("Execute comparação primeiro")
            return

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        for nome, modelo in self.hipoteses.items():
            if hasattr(modelo, 'sol') and modelo.sol is not None:
                t_plot = np.linspace(modelo.sol.t[0], modelo.sol.t[-1], 1000)
                y_plot = modelo.sol.sol(t_plot)
                a, rho_m, phi, pi_phi = y_plot

                # Plot do fator de escala
                axes[0,0].plot(t_plot, np.log(a), label=nome, linewidth=2)

                # Plot das densidades
                rho_phi = 0.5*(pi_phi/a**3)**2 + modelo.V_phi(phi)
                axes[0,1].semilogy(t_plot, rho_m, label=f'{nome} (ρ_m)', alpha=0.7)
                axes[0,1].semilogy(t_plot, rho_phi, label=f'{nome} (ρ_φ)', alpha=0.7)

                # Plot do campo escalar
                axes[1,0].plot(t_plot, phi, label=nome, linewidth=2)

                # Plot de G_eff
                f_vals = modelo.f_phi(phi)
                G_eff = 1.0 / f_vals
                axes[1,1].plot(t_plot, G_eff, label=nome, linewidth=2)

        # Configurar gráficos
        axes[0,0].set_ylabel('ln a(t)')
        axes[0,0].set_title('Fator de Escala - Comparação')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)

        axes[0,1].set_ylabel('Densidade de Energia')
        axes[0,1].set_title('Densidades de Energia')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)

        axes[1,0].set_xlabel('Tempo')
        axes[1,0].set_ylabel('φ(t)')
        axes[1,0].set_title('Campo Escalar')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)

        axes[1,1].set_xlabel('Tempo')
        axes[1,1].set_ylabel('G_eff/G')
        axes[1,1].set_title('Constante Gravitacional Efetiva')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

        plt.tight_layout()

        # Salvar comparação
        plt.savefig('resultados/comparacao_hipoteses.png', dpi=300, bbox_inches='tight')
        print("SUCESSO: Comparacao salva como 'resultados/comparacao_hipoteses.png'")

        return fig

    def salvar_resultados_comparacao(self):
        """
        Salva resultados da comparação em JSON
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados/comparacao_hipoteses_{timestamp}.json"

        dados = {
            'hipoteses': list(self.hipoteses.keys()),
            'resultados': self.resultados,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'tipo': 'comparacao_hipoteses'
            }
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print(f"SUCESSO: Resultados da comparacao salvos em {filename}")
        return filename

def main():
    """
    Função principal para testar hipóteses alternativas
    """
    print("Explorador de Hipoteses Alternativas de Bounce Gravitacional")
    print("=" * 70)

    # Criar explorador
    explorador = ExploradorHipoteses()

    # Hipótese Original
    modelo_original = CampoEscalarBounce(xi=1e6, alpha=-1e-4)
    explorador.adicionar_hipotese("Original (Campo Escalar)", modelo_original)

    # Hipótese Modificada
    modelo_modificado = HipoteseBounceModificado(xi=5e5, alpha=-5e-5, beta=1e-7, gamma=0.05)
    explorador.adicionar_hipotese("Modificada (φ³ + φ⁵)", modelo_modificado)

    # Hipótese Holográfica
    modelo_holografico = HipoteseBounceHolografico(xi=2e6, alpha=-2e-4, entropia_max=1e80)
    explorador.adicionar_hipotese("Holográfica", modelo_holografico)

    # Hipótese Quântica
    modelo_quantico = HipoteseBounceQuantico(xi=8e5, alpha=-8e-5, hbar_eff=1e-3)
    explorador.adicionar_hipotese("Quântica Semiclássica", modelo_quantico)

    # Executar comparação
    resultados = explorador.executar_comparacao(t_span=(-80, 80))

    # Salvar resultados
    explorador.salvar_resultados_comparacao()

    # Criar gráficos comparativos
    print("\nGerando graficos comparativos...")
    fig = explorador.plotar_comparacao()
    plt.show()

    # Análise dos resultados
    print("\nAnalise Comparativa:")
    print("-" * 50)

    hipoteses_sucesso = [nome for nome, res in resultados.items() if res.get('sucesso', False)]

    if hipoteses_sucesso:
        print(f"SUCESSO: Hipoteses bem-sucedidas: {len(hipoteses_sucesso)}/{len(resultados)}")

        # Comparar previsões de Ωk
        print("\nPrevisoes de Ωk:")
        for nome in hipoteses_sucesso:
            res = resultados[nome]
            if 'bounce_properties' in res:
                xi = res['parametros']['xi']
                alpha = res['parametros']['alpha']
                omega_k = -alpha * (xi / 1.0**2)  # M_Pl = 1
                print(f"  {nome}: Ωk = {omega_k:.6f}")

    else:
        print("ERRO: Nenhuma hipotese teve sucesso")

    print("\nConclusoes:")
    print("   - A hipotese modificada pode oferecer maior estabilidade")
    print("   - A abordagem holografica impõe limites naturais")
    print("   - Correções quanticas podem ser importantes para altas densidades")
    print("   - Cada abordagem oferece vantagens especificas para diferentes regimes")

if __name__ == "__main__":
    main()
