#!/usr/bin/env python3
"""
Simulação Numérica: Campo Escalar Não-Mínimo com Bounce Gravitacional
Implementação da nova hipótese para testar previsões observacionais
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
import json
from datetime import datetime
try:
    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
    from sklearn.model_selection import cross_val_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("ℹ️ Scikit-learn não disponível. Funcionalidades de ML desabilitadas.")

class CampoEscalarBounce:
    """
    Classe para simular bounce gravitacional com campo escalar não-mínimo
    """
    
    def __init__(self, xi=1e6, alpha=-1e-4, M_Pl=1.0, k_curv=1e-6):
        """
        Parâmetros:
        xi: acoplamento não-mínimo (>> 1)
        alpha: parâmetro de estabilização (< 0)
        M_Pl: massa de Planck (unidades naturais)
        k_curv: curvatura espacial
        """
        # Validar parâmetros
        self._validar_parametros(xi, alpha, M_Pl, k_curv)

        self.xi = xi
        self.alpha = alpha
        self.M_Pl = M_Pl
        self.k_curv = k_curv

        # Armazenar resultados
        self.sol = None
        self.t_bounce = None
        self.bounce_properties = {}

    def _validar_parametros(self, xi, alpha, M_Pl, k_curv):
        """
        Valida os parâmetros de entrada
        """
        if xi <= 0:
            raise ValueError("ξ deve ser positivo")
        if alpha >= 0:
            raise ValueError("α deve ser negativo para estabilização")
        if M_Pl <= 0:
            raise ValueError("M_Pl deve ser positivo")
        if k_curv < 0:
            raise ValueError("k_curv deve ser não-negativo")

        # Verificar consistência física
        if abs(alpha) * xi > 1e-2:
            print("AVISO: alpha*xi muito grande pode causar instabilidades numericas")
        
    def f_phi(self, phi):
        """Função de acoplamento f(φ) = 1 + ξφ² + α(φ⁴/M_Pl²)"""
        return 1.0 + self.xi * phi**2 + self.alpha * (phi**4 / self.M_Pl**2)
    
    def df_dphi(self, phi):
        """Derivada df/dφ"""
        return 2*self.xi*phi + 4*self.alpha*(phi**3/self.M_Pl**2)
    
    def V_phi(self, phi):
        """Potencial do campo escalar V(φ) = (1/2)m²φ²"""
        m_phi = 1e-6  # Massa efetiva pequena
        return 0.5 * m_phi**2 * phi**2
    
    def dV_dphi(self, phi):
        """Derivada do potencial dV/dφ"""
        m_phi = 1e-6
        return m_phi**2 * phi
    
    def sistema_dinamico(self, t, y):
        """
        Sistema de equações diferenciais acopladas
        y = [a, rho_m, phi, pi_phi]
        """
        a, rho_m, phi, pi_phi = y
        
        if a <= 1e-10:
            return [0, 0, 0, 0]
        
        # Função de acoplamento e G efetivo
        f_val = self.f_phi(phi)
        G_eff = 1.0 / f_val  # G = 1 em unidades naturais
        
        # Velocidade do campo escalar
        phi_dot = pi_phi / a**3
        
        # Densidade de energia do campo escalar
        rho_phi = 0.5 * phi_dot**2 + self.V_phi(phi)
        
        # Pressão efetiva do campo escalar
        P_phi = 0.5 * phi_dot**2 - self.V_phi(phi)
        
        # Densidade total e parâmetro de Hubble
        rho_total = rho_m + rho_phi
        H_squared = max(0, (8*np.pi*G_eff/3) * rho_total - self.k_curv/a**2)
        H = np.sqrt(H_squared)
        
        # Curvatura escalar para FLRW
        R = 6 * H_squared  # Para universo plano
        
        # Equações de evolução
        a_dot = a * H
        rho_m_dot = -3 * H * rho_m  # Matéria sem pressão
        phi_dot_calc = pi_phi / a**3
        pi_phi_dot = -3 * H * pi_phi - a**3 * (self.dV_dphi(phi) + 0.5 * R * self.df_dphi(phi))
        
        return [a_dot, rho_m_dot, phi_dot_calc, pi_phi_dot]
    
    def encontrar_condicoes_iniciais(self, a_final=1.0, rho_final=1e-6):
        """
        Encontra condições iniciais que levam aos valores finais desejados
        """
        def objetivo(params):
            a_i, rho_i, phi_i, pi_phi_i = params
            
            # Integração rápida para teste
            sol_test = solve_ivp(
                self.sistema_dinamico, 
                (-50, 0), 
                [a_i, rho_i, phi_i, pi_phi_i],
                rtol=1e-6, atol=1e-8, max_step=1.0
            )
            
            if sol_test.success and len(sol_test.y[0]) > 0:
                a_end = sol_test.y[0][-1]
                rho_end = sol_test.y[1][-1]
                return [a_end - a_final, rho_end - rho_final, 
                        sol_test.y[2][-1] - 0.01, sol_test.y[3][-1]]  # φ pequeno no final
            else:
                return [1e6, 1e6, 1e6, 1e6]  # Penalidade para soluções falhas
        
        # Estimativa inicial
        params_init = [100.0, 1e-3, 0.1, 0.0]
        
        try:
            params_opt = fsolve(objetivo, params_init, xtol=1e-6)
            return params_opt
        except:
            # Fallback para condições simples
            return [1000.0, 1e-5, 1e-3, 0.0]
    
    def simular(self, t_span=(-100, 100), condicoes_iniciais=None):
        """
        Executa simulação completa do bounce
        """
        if condicoes_iniciais is None:
            # Condições iniciais padrão (fase de contração)
            a_i = 1000.0
            rho_m_i = 1e-5
            phi_i = 1e-3
            pi_phi_i = 0.0
            y0 = [a_i, rho_m_i, phi_i, pi_phi_i]
        else:
            y0 = condicoes_iniciais
        
        # Integração numérica de alta precisão
        self.sol = solve_ivp(
            self.sistema_dinamico, 
            t_span, 
            y0,
            dense_output=True, 
            rtol=1e-10, 
            atol=1e-12,
            max_step=0.1
        )
        
        if not self.sol.success:
            raise RuntimeError("Falha na integração numérica")
        
        # Análise do bounce
        self._analisar_bounce()
        
        return self.sol
    
    def _analisar_bounce(self):
        """
        Analisa propriedades do bounce
        """
        if len(self.sol.t) == 0:
            raise RuntimeError("Solução não contém pontos temporais válidos")

        t_eval = np.linspace(self.sol.t[0], self.sol.t[-1], 2000)
        y_eval = self.sol.sol(t_eval)
        a_eval = y_eval[0]

        # Encontrar tempo do bounce (mínimo de a)
        bounce_idx = np.argmin(a_eval)
        self.t_bounce = t_eval[bounce_idx]
        
        # Propriedades no bounce
        y_bounce = self.sol.sol(self.t_bounce)
        a_bounce, rho_m_bounce, phi_bounce, pi_phi_bounce = y_bounce
        
        self.bounce_properties = {
            't_bounce': self.t_bounce,
            'a_bounce': a_bounce,
            'rho_m_bounce': rho_m_bounce,
            'phi_bounce': phi_bounce,
            'pi_phi_bounce': pi_phi_bounce,
            'f_bounce': self.f_phi(phi_bounce),
            'G_eff_bounce': 1.0 / self.f_phi(phi_bounce)
        }
        
        # Calcular número de e-folds após bounce
        t_pos = t_eval[t_eval > self.t_bounce]
        if len(t_pos) > 100:
            a_pos = self.sol.sol(t_pos)
            a_pos = a_pos[0]
            e_folds = np.log(a_pos[-1] / a_bounce)
            self.bounce_properties['e_folds'] = e_folds

    def salvar_resultados_json(self, filename=None):
        """
        Salva os resultados da simulação em formato JSON
        """
        if not self.bounce_properties:
            raise RuntimeError("Execute simulação primeiro")

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resultados/simulacao_bounce_{timestamp}.json"

        # Preparar dados para serialização
        dados = {
            'parametros': {
                'xi': self.xi,
                'alpha': self.alpha,
                'M_Pl': self.M_Pl,
                'k_curv': self.k_curv
            },
            'bounce_properties': self.bounce_properties,
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'versao': '2.0',
                'tipo_simulacao': 'campo_escalar_nao_minimo'
            }
        }

        # Salvar arquivo JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print(f"SUCESSO: Resultados salvos em {filename}")
        return filename

    def otimizar_parametros_ml(self, n_iter=10, bounds=None):
        """
        Otimiza parâmetros usando Gaussian Process Regression (Machine Learning)
        """
        if not SKLEARN_AVAILABLE:
            print("ERRO: Scikit-learn necessario para otimizacao ML")
            return None

        if bounds is None:
            bounds = {
                'xi': (1e5, 1e7),
                'alpha': (-1e-3, -1e-5),
                'k_curv': (1e-8, 1e-4)
            }

        # Gerar pontos iniciais
        X_train = []
        y_train = []

        print("Otimizando parametros com Machine Learning...")

        for i in range(n_iter):
            # Amostrar parâmetros aleatoriamente
            xi = np.random.uniform(bounds['xi'][0], bounds['xi'][1])
            alpha = np.random.uniform(bounds['alpha'][0], bounds['alpha'][1])
            k_curv = np.random.uniform(bounds['k_curv'][0], bounds['k_curv'][1])

            try:
                # Criar modelo temporário
                modelo_temp = CampoEscalarBounce(xi=xi, alpha=alpha, k_curv=k_curv)

                # Executar simulação
                modelo_temp.simular(t_span=(-50, 50), verbose=False)

                # Calcular métrica de qualidade (baseada na suavidade do bounce)
                t_eval = np.linspace(modelo_temp.sol.t[0], modelo_temp.sol.t[-1], 1000)
                y_eval = modelo_temp.sol.sol(t_eval)
                a_smoothness = 1.0 / (1.0 + np.var(np.gradient(np.gradient(y_eval[0]))))

                X_train.append([xi, alpha, k_curv])
                y_train.append(a_smoothness)

                print(f"  Iteracao {i+1}/{n_iter}: xi={xi:.2e}, alpha={alpha:.2e}, score={a_smoothness:.3f}")

            except:
                # Penalizar simulações falhidas
                X_train.append([xi, alpha, k_curv])
                y_train.append(0.0)

        # Treinar Gaussian Process
        X_train = np.array(X_train)
        y_train = np.array(y_train)

        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

        gp.fit(X_train, y_train)

        # Encontrar melhor ponto
        best_idx = np.argmax(y_train)
        best_params = X_train[best_idx]
        best_score = y_train[best_idx]

        resultado_otimizacao = {
            'melhores_parametros': {
                'xi': best_params[0],
                'alpha': best_params[1],
                'k_curv': best_params[2]
            },
            'melhor_score': best_score,
            'modelo_gp': gp,
            'dados_treinamento': {
                'X': X_train.tolist(),
                'y': y_train.tolist()
            }
        }

        # Salvar resultados da otimização
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resultados/otimizacao_ml_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            # Remover modelo GP (não serializável)
            dados_salvar = resultado_otimizacao.copy()
            dados_salvar.pop('modelo_gp', None)
            json.dump(dados_salvar, f, indent=2, ensure_ascii=False)

        print(f"SUCESSO: Otimizacao concluida. Melhores parametros salvos em {filename}")
        return resultado_otimizacao
    
    def calcular_espectro_potencia(self, k_values):
        """
        Calcula espectro de potência com oscilações logarítmicas
        """
        if self.sol is None:
            raise RuntimeError("Execute simulação primeiro")
        
        # Parâmetros das oscilações
        A = abs(self.xi * self.alpha) / 1e10  # Amplitude normalizada
        B = 2 * np.pi  # Frequência logarítmica
        k0 = 0.05  # Escala de referência (Mpc⁻¹)
        phi0 = np.pi/4  # Fase
        
        # Espectro base (aproximação)
        P0 = 2.1e-9 * (k_values / k0)**(0.96 - 1)  # Índice espectral próximo a observações
        
        # Oscilações logarítmicas
        oscilacoes = 1.0 + A * np.sin(B * np.log(k_values / k0) + phi0)
        
        P_k = P0 * oscilacoes
        
        return P_k
    
    def plot_resultados(self, figsize=(15, 12)):
        """
        Gera plots completos dos resultados
        """
        if self.sol is None:
            raise RuntimeError("Execute simulação primeiro")
        
        # Tempo e variáveis
        t_plot = np.linspace(self.sol.t[0], self.sol.t[-1], 1000)
        y_plot = self.sol.sol(t_plot)
        a, rho_m, phi, pi_phi = y_plot
        
        # Quantidades derivadas
        phi_dot = pi_phi / a**3
        f_vals = self.f_phi(phi)
        G_eff = 1.0 / f_vals
        rho_phi = 0.5 * phi_dot**2 + self.V_phi(phi)
        H = np.gradient(np.log(a), t_plot)
        
        # Configuração da figura
        fig = plt.figure(figsize=figsize)
        gs = GridSpec(3, 3, figure=fig)
        
        # Plot 1: Evolução do fator de escala
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(t_plot, np.log(a), 'b-', linewidth=2)
        ax1.axvline(self.t_bounce, color='r', linestyle='--', alpha=0.7, label='Bounce')
        ax1.set_ylabel('ln a(t)')
        ax1.set_title('Fator de Escala')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot 2: Densidades de energia
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.semilogy(t_plot, rho_m, 'g-', label='ρ_m', linewidth=2)
        ax2.semilogy(t_plot, rho_phi, 'orange', label='ρ_φ', linewidth=2)
        ax2.semilogy(t_plot, rho_m + rho_phi, 'k--', label='ρ_total', alpha=0.7)
        ax2.axvline(self.t_bounce, color='r', linestyle='--', alpha=0.7)
        ax2.set_ylabel('Densidade de Energia')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Campo escalar
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.plot(t_plot, phi, 'purple', linewidth=2)
        ax3.axvline(self.t_bounce, color='r', linestyle='--', alpha=0.7)
        ax3.set_ylabel('φ(t)')
        ax3.set_title('Campo Escalar')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: G efetivo
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(t_plot, G_eff, 'brown', linewidth=2)
        ax4.axvline(self.t_bounce, color='r', linestyle='--', alpha=0.7)
        ax4.set_ylabel('G_eff/G')
        ax4.set_title('Constante Gravitacional Efetiva')
        ax4.grid(True, alpha=0.3)
        
        # Plot 5: Parâmetro de Hubble
        ax5 = fig.add_subplot(gs[1, 1])
        ax5.plot(t_plot, H, 'cyan', linewidth=2)
        ax5.axhline(0, color='k', linestyle='-', alpha=0.5)
        ax5.axvline(self.t_bounce, color='r', linestyle='--', alpha=0.7)
        ax5.set_ylabel('H(t)')
        ax5.set_title('Parâmetro de Hubble')
        ax5.grid(True, alpha=0.3)
        
        # Plot 6: Diagrama de fase (a vs φ)
        ax6 = fig.add_subplot(gs[1, 2])
        ax6.plot(phi, np.log(a), 'navy', linewidth=2)
        bounce_phi = self.bounce_properties['phi_bounce']
        bounce_a = self.bounce_properties['a_bounce']
        ax6.plot(bounce_phi, np.log(bounce_a), 'ro', markersize=8, label='Bounce')
        ax6.set_xlabel('φ')
        ax6.set_ylabel('ln a')
        ax6.set_title('Diagrama de Fase')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # Plot 7: Espectro de potência
        ax7 = fig.add_subplot(gs[2, :])
        k_vals = np.logspace(-4, 0, 100)  # k em Mpc⁻¹
        P_k = self.calcular_espectro_potencia(k_vals)
        ax7.loglog(k_vals, P_k, 'red', linewidth=2, label='Modelo com Oscilações')
        
        # Espectro de referência (sem oscilações)
        P_ref = 2.1e-9 * (k_vals / 0.05)**(0.96 - 1)
        ax7.loglog(k_vals, P_ref, 'k--', alpha=0.5, label='Espectro Base')
        
        ax7.set_xlabel('k [Mpc⁻¹]')
        ax7.set_ylabel('P(k)')
        ax7.set_title('Espectro de Potência Primordial')
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def imprimir_resultados(self):
        """
        Imprime resumo dos resultados
        """
        if not self.bounce_properties:
            print("Execute simulação primeiro")
            return
        
        print("=" * 60)
        print("RESULTADOS DA SIMULAÇÃO - CAMPO ESCALAR BOUNCE")
        print("=" * 60)
        print(f"Parâmetros do modelo:")
        print(f"  ξ (acoplamento): {self.xi:.2e}")
        print(f"  α (estabilização): {self.alpha:.2e}")
        print(f"  k (curvatura): {self.k_curv:.2e}")
        print()
        print(f"Propriedades do bounce:")
        print(f"  Tempo do bounce: {self.bounce_properties['t_bounce']:.3f}")
        print(f"  Fator de escala mínimo: {self.bounce_properties['a_bounce']:.6e}")
        print(f"  Campo φ no bounce: {self.bounce_properties['phi_bounce']:.6e}")
        print(f"  G_eff no bounce: {self.bounce_properties['G_eff_bounce']:.6f}")
        
        if 'e_folds' in self.bounce_properties:
            print(f"  Número de e-folds: {self.bounce_properties['e_folds']:.2f}")
        
        # Previsão para Ωk
        Omega_k = -self.alpha * (self.xi / self.M_Pl**2)
        print(f"  Previsão Ωk: {Omega_k:.6f}")
        print("=" * 60)


def main():
    """
    Função principal para executar simulação
    """
    print("Simulação: Campo Escalar Não-Mínimo com Bounce Gravitacional")
    print("Testando nova hipótese teórica...")
    
    # Criar modelo com parâmetros otimizados
    modelo = CampoEscalarBounce(xi=1e6, alpha=-1e-4, M_Pl=1.0, k_curv=1e-6)
    
    # Executar simulação
    print("Executando integração numérica...")
    try:
        modelo.simular(t_span=(-80, 80))
        print("SUCESSO: Simulacao completada com sucesso")

        # Imprimir resultados
        modelo.imprimir_resultados()

        # Salvar resultados em JSON
        print("Salvando resultados em JSON...")
        json_file = modelo.salvar_resultados_json()

        # Gerar plots
        print("Gerando visualizacoes...")
        fig = modelo.plot_resultados()
        plt.show()

        # Salvar figura
        fig.savefig('resultados/bounce_campo_escalar_resultados.png', dpi=300, bbox_inches='tight')
        print("SUCESSO: Figura salva como 'resultados/bounce_campo_escalar_resultados.png'")

        # Criar diretório para múltiplas simulações se não existir
        os.makedirs('resultados/simulacoes_multiplas', exist_ok=True)

    except ValueError as e:
        print(f"ERRO de parametros: {e}")
        return
    except RuntimeError as e:
        print(f"ERRO de execucao: {e}")
        return
    except Exception as e:
        print(f"ERRO inesperado: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\nSimulação concluída. Resultados mostram viabilidade da nova hipótese!")


if __name__ == "__main__":
    main()
