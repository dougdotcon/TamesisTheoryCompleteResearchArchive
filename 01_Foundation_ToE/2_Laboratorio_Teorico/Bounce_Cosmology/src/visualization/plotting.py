#!/usr/bin/env python3
"""
Módulo de Visualização Científica para Física Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Plotagem de resultados cosmológicos
- Visualização de campos escalares
- Gráficos de convergência
- Análise visual de dados
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from matplotlib.colors import LogNorm, LinearSegmentedColormap
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from typing import Dict, List, Tuple, Optional, Union, Callable
import warnings
from dataclasses import dataclass
import os


@dataclass
class ConfiguracaoPlot:
    """
    Configuração para plots científicos
    """
    figsize: Tuple[int, int] = (12, 8)
    dpi: int = 300
    estilo: str = 'seaborn-v0_8'
    fonte: str = 'DejaVu Sans'
    tamanho_fonte: int = 12
    formato_saida: str = 'png'
    salvar_plots: bool = True
    diretorio_saida: str = 'resultados'

    def __post_init__(self):
        if not os.path.exists(self.diretorio_saida):
            os.makedirs(self.diretorio_saida)


class VisualizadorCosmologico:
    """
    Classe para visualização de resultados cosmológicos
    """

    def __init__(self, config: ConfiguracaoPlot = None):
        if config is None:
            config = ConfiguracaoPlot()

        self.config = config
        plt.style.use(config.estilo)
        plt.rcParams.update({
            'font.family': config.fonte,
            'font.size': config.tamanho_fonte,
            'axes.labelsize': config.tamanho_fonte,
            'axes.titlesize': config.tamanho_fonte + 2,
            'xtick.labelsize': config.tamanho_fonte - 1,
            'ytick.labelsize': config.tamanho_fonte - 1,
            'legend.fontsize': config.tamanho_fonte - 1,
            'figure.dpi': config.dpi
        })

    def plot_evolucao_cosmologica_completa(self, sol, titulo: str = "Evolução Cosmológica Completa",
                                          salvar: bool = True) -> plt.Figure:
        """
        Plot completo da evolução cosmológica com bounce

        Parameters:
        -----------
        sol : Bunch
            Solução da integração numérica
        titulo : str
            Título do plot
        salvar : bool
            Salvar plot em arquivo

        Returns:
        --------
        matplotlib.figure.Figure: Figura criada
        """
        # Preparar dados
        t_plot = np.linspace(sol.t[0], sol.t[-1], 1000)
        y_plot = sol.sol(t_plot)
        a, rho_m, phi, pi_phi = y_plot

        # Cálculos derivados
        phi_dot = pi_phi / a**3
        rho_phi = 0.5 * phi_dot**2 + 0.5 * phi**2  # Assumindo m=1
        rho_total = rho_m + rho_phi
        H = np.gradient(np.log(a), t_plot)

        # Detectar bounce
        idx_bounce = np.argmin(a)
        t_bounce = t_plot[idx_bounce]

        # Criar figura com subplots
        fig = plt.figure(figsize=self.config.figsize)
        gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

        # Plot 1: Fator de escala
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.plot(t_plot, np.log(a), 'b-', linewidth=2, label='ln a(t)')
        ax1.axvline(t_bounce, color='r', linestyle='--', alpha=0.7, label='Bounce')
        ax1.set_ylabel('ln a(t)')
        ax1.set_title('Fator de Escala', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Densidades de energia
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.semilogy(t_plot, rho_m, 'g-', linewidth=2, label='ρ_m (matéria)')
        ax2.semilogy(t_plot, rho_phi, 'orange', linewidth=2, label='ρ_φ (campo)')
        ax2.semilogy(t_plot, rho_total, 'k--', linewidth=1.5, label='ρ_total')
        ax2.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax2.set_ylabel('Densidade de Energia')
        ax2.set_title('Densidades de Energia', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Plot 3: Campo escalar
        ax3 = fig.add_subplot(gs[0, 2])
        ax3.plot(t_plot, phi, 'purple', linewidth=2, label='φ(t)')
        ax3.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax3.set_ylabel('φ(t)')
        ax3.set_title('Campo Escalar', fontweight='bold')
        ax3.grid(True, alpha=0.3)

        # Plot 4: Parâmetro de Hubble
        ax4 = fig.add_subplot(gs[1, 0])
        ax4.plot(t_plot, H, 'cyan', linewidth=2, label='H(t)')
        ax4.axhline(0, color='k', linestyle='-', alpha=0.5, linewidth=0.5)
        ax4.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax4.set_ylabel('H(t)')
        ax4.set_title('Parâmetro de Hubble', fontweight='bold')
        ax4.grid(True, alpha=0.3)

        # Plot 5: Equação de estado efetiva
        ax5 = fig.add_subplot(gs[1, 1])
        P_phi = 0.5 * phi_dot**2 - 0.5 * phi**2  # Assumindo m=1
        w_eff = P_phi / rho_phi
        ax5.plot(t_plot, w_eff, 'red', linewidth=2, label='w_φ')
        ax5.axhline(-1/3, color='orange', linestyle=':', alpha=0.7, label='w=-1/3')
        ax5.axhline(1/3, color='green', linestyle=':', alpha=0.7, label='w=1/3')
        ax5.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax5.set_ylabel('w_φ')
        ax5.set_title('Equação de Estado Efetiva', fontweight='bold')
        ax5.set_ylim([-2, 2])
        ax5.grid(True, alpha=0.3)
        ax5.legend()

        # Plot 6: Trajetória de fase (a vs φ)
        ax6 = fig.add_subplot(gs[1, 2])
        scatter = ax6.scatter(phi, np.log(a), c=t_plot, cmap='viridis', alpha=0.6, s=1)
        ax6.plot(phi[idx_bounce], np.log(a[idx_bounce]), 'ro', markersize=8, label='Bounce')
        ax6.set_xlabel('φ')
        ax6.set_ylabel('ln a')
        ax6.set_title('Trajetória de Fase', fontweight='bold')
        plt.colorbar(scatter, ax=ax6, label='Tempo')
        ax6.grid(True, alpha=0.3)
        ax6.legend()

        # Plot 7: Energia cinética vs potencial
        ax7 = fig.add_subplot(gs[2, 0])
        energia_cinetica = 0.5 * phi_dot**2
        energia_potencial = 0.5 * phi**2
        ax7.plot(t_plot, energia_cinetica, 'blue', linewidth=2, label='K = ½φ̇²')
        ax7.plot(t_plot, energia_potencial, 'red', linewidth=2, label='V = ½φ²')
        ax7.plot(t_plot, energia_cinetica + energia_potencial, 'k--', linewidth=1.5, label='E_total')
        ax7.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax7.set_xlabel('Tempo')
        ax7.set_ylabel('Energia')
        ax7.set_title('Energia do Campo Escalar', fontweight='bold')
        ax7.grid(True, alpha=0.3)
        ax7.legend()

        # Plot 8: Espectro de potência (placeholder)
        ax8 = fig.add_subplot(gs[2, 1])
        k_vals = np.logspace(-4, 0, 100)
        P_k = 2.1e-9 * (k_vals / 0.05)**(-0.04)  # Placeholder
        ax8.loglog(k_vals, P_k, 'purple', linewidth=2)
        ax8.set_xlabel('k [Mpc⁻¹]')
        ax8.set_ylabel('P(k)')
        ax8.set_title('Espectro de Potência', fontweight='bold')
        ax8.grid(True, alpha=0.3)

        # Plot 9: Momento do campo
        ax9 = fig.add_subplot(gs[2, 2])
        ax9.plot(t_plot, pi_phi, 'brown', linewidth=2, label='π_φ')
        ax9.axvline(t_bounce, color='r', linestyle='--', alpha=0.7)
        ax9.set_xlabel('Tempo')
        ax9.set_ylabel('π_φ')
        ax9.set_title('Momento do Campo', fontweight='bold')
        ax9.grid(True, alpha=0.3)

        # Título geral
        fig.suptitle(titulo, fontsize=16, fontweight='bold', y=0.98)

        # Ajustar layout
        plt.tight_layout()

        # Salvar se solicitado
        if salvar and self.config.salvar_plots:
            nome_arquivo = titulo.lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a')
            nome_arquivo = ''.join(c for c in nome_arquivo if c.isalnum() or c in ('_', '-'))
            caminho_arquivo = os.path.join(self.config.diretorio_saida, f"{nome_arquivo}.{self.config.formato_saida}")
            fig.savefig(caminho_arquivo, dpi=self.config.dpi, bbox_inches='tight')
            print(f"✅ Plot salvo em: {caminho_arquivo}")

        return fig

    def plot_comparacao_hipoteses(self, resultados: Dict[str, Dict],
                                 titulo: str = "Comparação de Hipóteses",
                                 salvar: bool = True) -> plt.Figure:
        """
        Plot comparativo de diferentes hipóteses/modelos
        """
        fig, axes = plt.subplots(2, 2, figsize=self.config.figsize)
        fig.suptitle(titulo, fontsize=16, fontweight='bold')

        # Cores para diferentes hipóteses
        cores = ['blue', 'red', 'green', 'orange', 'purple']

        # Plot 1: Fator de escala
        ax1 = axes[0, 0]
        for i, (nome, resultado) in enumerate(resultados.items()):
            if 'sol' in resultado:
                t_plot = np.linspace(resultado['sol'].t[0], resultado['sol'].t[-1], 500)
                a_plot = resultado['sol'].sol(t_plot)[0]
                ax1.plot(t_plot, np.log(a_plot), color=cores[i % len(cores)],
                        linewidth=2, label=nome)

        ax1.set_xlabel('Tempo')
        ax1.set_ylabel('ln a(t)')
        ax1.set_title('Evolução do Fator de Escala')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot 2: Campo escalar
        ax2 = axes[0, 1]
        for i, (nome, resultado) in enumerate(resultados.items()):
            if 'sol' in resultado:
                t_plot = np.linspace(resultado['sol'].t[0], resultado['sol'].t[-1], 500)
                phi_plot = resultado['sol'].sol(t_plot)[2]
                ax2.plot(t_plot, phi_plot, color=cores[i % len(cores)],
                        linewidth=2, label=nome)

        ax2.set_xlabel('Tempo')
        ax2.set_ylabel('φ(t)')
        ax2.set_title('Campo Escalar')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Plot 3: Propriedades do bounce
        ax3 = axes[1, 0]
        nomes = list(resultados.keys())
        t_bounces = [resultados[nome].get('bounce_properties', {}).get('t_bounce', 0)
                    for nome in nomes]
        a_mins = [resultados[nome].get('bounce_properties', {}).get('a_bounce', 1)
                 for nome in nomes]

        x = np.arange(len(nomes))
        ax3.bar(x - 0.2, t_bounces, 0.4, label='t_bounce', alpha=0.7)
        ax3.bar(x + 0.2, np.log(a_mins), 0.4, label='ln a_min', alpha=0.7)
        ax3.set_xlabel('Hipótese')
        ax3.set_ylabel('Valor')
        ax3.set_title('Propriedades do Bounce')
        ax3.set_xticks(x)
        ax3.set_xticklabels(nomes, rotation=45)
        ax3.grid(True, alpha=0.3)
        ax3.legend()

        # Plot 4: G_eff no bounce
        ax4 = axes[1, 1]
        G_effs = [resultados[nome].get('bounce_properties', {}).get('G_eff_bounce', 1)
                 for nome in nomes]

        bars = ax4.bar(nomes, G_effs, alpha=0.7, color=cores[:len(nomes)])
        ax4.set_ylabel('G_eff / G')
        ax4.set_title('Constante Gravitacional Efetiva no Bounce')
        ax4.set_xticklabels(nomes, rotation=45)
        ax4.grid(True, alpha=0.3)

        # Adicionar valores nas barras
        for bar, valor in zip(bars, G_effs):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    '.3f', ha='center', va='bottom')

        plt.tight_layout()

        # Salvar se solicitado
        if salvar and self.config.salvar_plots:
            nome_arquivo = titulo.lower().replace(' ', '_')
            nome_arquivo = ''.join(c for c in nome_arquivo if c.isalnum() or c in ('_', '-'))
            caminho_arquivo = os.path.join(self.config.diretorio_saida, f"{nome_arquivo}.{self.config.formato_saida}")
            fig.savefig(caminho_arquivo, dpi=self.config.dpi, bbox_inches='tight')
            print(f"✅ Plot salvo em: {caminho_arquivo}")

        return fig

    def plot_convergencia_otimizacao(self, historia_otimizacao: List[Dict],
                                    titulo: str = "Convergência da Otimização",
                                    salvar: bool = True) -> plt.Figure:
        """
        Plot da convergência de algoritmos de otimização
        """
        fig, axes = plt.subplots(2, 2, figsize=self.config.figsize)
        fig.suptitle(titulo, fontsize=16, fontweight='bold')

        if not historia_otimizacao:
            print("⚠️  História de otimização vazia")
            return fig

        # Preparar dados
        iteracoes = [h['iteracao'] for h in historia_otimizacao]
        valores = [h['valor'] for h in historia_otimizacao]

        # Plot 1: Valor da função objetivo vs iteração
        ax1 = axes[0, 0]
        ax1.plot(iteracoes, valores, 'b-', linewidth=2, marker='o', markersize=3)
        ax1.set_xlabel('Iteração')
        ax1.set_ylabel('Valor da Função Objetivo')
        ax1.set_title('Convergência da Função Objetivo')
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')

        # Plot 2: Evolução dos parâmetros (se disponível)
        ax2 = axes[0, 1]
        if 'parametros' in historia_otimizacao[0]:
            n_params = len(historia_otimizacao[0]['parametros'])
            for i in range(min(n_params, 5)):  # Máximo 5 parâmetros
                param_vals = [h['parametros'][i] for h in historia_otimizacao]
                ax2.plot(iteracoes, param_vals, linewidth=2,
                        label=f'Parâmetro {i+1}', marker='o', markersize=2)

            ax2.set_xlabel('Iteração')
            ax2.set_ylabel('Valor do Parâmetro')
            ax2.set_title('Evolução dos Parâmetros')
            ax2.grid(True, alpha=0.3)
            ax2.legend()

        # Plot 3: Gradiente da convergência
        ax3 = axes[1, 0]
        if len(valores) > 1:
            gradiente = np.gradient(valores, iteracoes)
            ax3.plot(iteracoes[:-1], np.abs(gradiente), 'r-', linewidth=2)
            ax3.set_xlabel('Iteração')
            ax3.set_ylabel('|dValor/dIteração|')
            ax3.set_title('Taxa de Convergência')
            ax3.grid(True, alpha=0.3)
            ax3.set_yscale('log')

        # Plot 4: Melhor valor vs iteração
        ax4 = axes[1, 1]
        melhores_valores = []
        melhor_atual = float('inf')

        for h in historia_otimizacao:
            if h['valor'] < melhor_atual:
                melhor_atual = h['valor']
            melhores_valores.append(melhor_atual)

        ax4.plot(iteracoes, melhores_valores, 'g-', linewidth=2, marker='s', markersize=3)
        ax4.set_xlabel('Iteração')
        ax4.set_ylabel('Melhor Valor')
        ax4.set_title('Evolução do Melhor Valor')
        ax4.grid(True, alpha=0.3)
        ax4.set_yscale('log')

        plt.tight_layout()

        # Salvar se solicitado
        if salvar and self.config.salvar_plots:
            nome_arquivo = titulo.lower().replace(' ', '_')
            nome_arquivo = ''.join(c for c in nome_arquivo if c.isalnum() or c in ('_', '-'))
            caminho_arquivo = os.path.join(self.config.diretorio_saida, f"{nome_arquivo}.{self.config.formato_saida}")
            fig.savefig(caminho_arquivo, dpi=self.config.dpi, bbox_inches='tight')
            print(f"✅ Plot salvo em: {caminho_arquivo}")

        return fig


# Funções utilitárias para uso direto
def plot_cosmo_basico(sol, titulo: str = "Evolução Cosmológica") -> plt.Figure:
    """
    Função simples para plot básico da evolução cosmológica
    """
    visualizador = VisualizadorCosmologico()
    return visualizador.plot_evolucao_cosmologica_completa(sol, titulo)


def criar_animacao_bounce(sol, nome_arquivo: str = "bounce_animacao.gif",
                         fps: int = 10) -> str:
    """
    Criar animação da evolução do bounce
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Preparar dados
    t_plot = np.linspace(sol.t[0], sol.t[-1], 200)
    y_plot = sol.sol(t_plot)
    a, rho_m, phi, pi_phi = y_plot

    # Configurar plots
    line1, = ax1.plot([], [], 'b-', linewidth=2)
    ax1.set_xlim(t_plot[0], t_plot[-1])
    ax1.set_ylim(np.min(np.log(a)), np.max(np.log(a)) * 1.1)
    ax1.set_xlabel('Tempo')
    ax1.set_ylabel('ln a(t)')
    ax1.set_title('Fator de Escala')
    ax1.grid(True, alpha=0.3)

    line2, = ax2.plot([], [], 'purple', linewidth=2)
    ax2.set_xlim(t_plot[0], t_plot[-1])
    ax2.set_ylim(np.min(phi), np.max(phi) * 1.1)
    ax2.set_xlabel('Tempo')
    ax2.set_ylabel('φ(t)')
    ax2.set_title('Campo Escalar')
    ax2.grid(True, alpha=0.3)

    def animate(frame):
        # Atualizar linha 1 (fator de escala)
        line1.set_data(t_plot[:frame], np.log(a[:frame]))

        # Atualizar linha 2 (campo escalar)
        line2.set_data(t_plot[:frame], phi[:frame])

        return [line1, line2]

    # Criar animação
    anim = animation.FuncAnimation(
        fig, animate, frames=len(t_plot), interval=50, blit=True
    )

    # Salvar animação
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    caminho_completo = os.path.join('resultados', nome_arquivo)
    anim.save(caminho_completo, writer='pillow', fps=fps)

    plt.close(fig)
    print(f"✅ Animação salva em: {caminho_completo}")

    return caminho_completo


# Exemplo de uso
if __name__ == "__main__":
    print("Módulo de Visualização Científica")
    print("=" * 50)
    print("Este módulo fornece ferramentas avançadas para visualização")
    print("de resultados de física computacional e cosmologia.")
    print()
    print("Funcionalidades principais:")
    print("- Plotagem completa de evolução cosmológica")
    print("- Comparação de diferentes hipóteses")
    print("- Visualização de convergência de otimização")
    print("- Criação de animações")
    print()
    print("Para usar, importe o módulo:")
    print("from src.visualization.plotting import VisualizadorCosmologico")
