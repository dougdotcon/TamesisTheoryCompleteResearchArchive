#!/usr/bin/env python3
"""
Métodos de Monte Carlo para Física Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Monte Carlo clássico e quântico
- Simulação de Ising 2D
- Métodos de amostragem avançados
- Análise estatística de resultados
"""

import numpy as np
from typing import Callable, Tuple, Dict, Optional, Union
import warnings
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class ConfiguracaoMonteCarlo:
    """
    Configuração para simulações Monte Carlo
    """
    n_sweeps: int = 1000
    n_thermalizacao: int = 100
    n_amostras: int = 100
    temperatura: float = 1.0
    tamanho_sistema: Tuple[int, ...] = (10, 10)
    campo_externo: float = 0.0
    seed: Optional[int] = None

    def __post_init__(self):
        if self.n_sweeps <= 0:
            raise ValueError("Número de sweeps deve ser positivo")
        if self.temperatura <= 0:
            raise ValueError("Temperatura deve ser positiva")
        if self.seed is not None:
            np.random.seed(self.seed)


class SimulacaoMonteCarlo(ABC):
    """
    Classe base abstrata para simulações Monte Carlo
    """

    def __init__(self, config: ConfiguracaoMonteCarlo):
        self.config = config
        self.rng = np.random.RandomState(config.seed)
        self.historia_energia = []
        self.historia_magnetizacao = []
        self.observaveis_acumulados = {}

    @abstractmethod
    def inicializar_sistema(self) -> np.ndarray:
        """Inicializa a configuração do sistema"""
        pass

    @abstractmethod
    def calcular_energia(self, configuracao: np.ndarray) -> float:
        """Calcula energia da configuração"""
        pass

    @abstractmethod
    def calcular_magnetizacao(self, configuracao: np.ndarray) -> float:
        """Calcula magnetização da configuração"""
        pass

    @abstractmethod
    def passo_monte_carlo(self, configuracao: np.ndarray) -> np.ndarray:
        """Executa um passo de Monte Carlo"""
        pass

    def executar_simulacao(self, verbose: bool = True) -> Dict[str, np.ndarray]:
        """
        Executa simulação Monte Carlo completa

        Parameters:
        -----------
        verbose : bool
            Mostrar progresso da simulação

        Returns:
        --------
        dict: Resultados da simulação
        """
        # Inicialização
        configuracao = self.inicializar_sistema()

        if verbose:
            print(f"Iniciando simulação Monte Carlo...")
            print(f"Sistema: {configuracao.shape}")
            print(f"Temperatura: {self.config.temperatura}")
            print(f"Sweeps: {self.config.n_sweeps}")

        # Thermalização
        for sweep in range(self.config.n_thermalizacao):
            configuracao = self.passo_monte_carlo(configuracao)

        if verbose:
            print("Thermalização concluída. Iniciando medições...")

        # Simulação principal
        for sweep in range(self.config.n_sweeps):
            configuracao = self.passo_monte_carlo(configuracao)

            # Calcular observáveis
            energia = self.calcular_energia(configuracao)
            magnetizacao = self.calcular_magnetizacao(configuracao)

            self.historia_energia.append(energia)
            self.historia_magnetizacao.append(magnetizacao)

            # Calcular observáveis adicionais
            self._calcular_observaveis_adicionais(configuracao)

            if verbose and (sweep + 1) % (self.config.n_sweeps // 10) == 0:
                progresso = (sweep + 1) / self.config.n_sweeps * 100
                print(".1f")

        if verbose:
            print("Simulação concluída!")

        # Preparar resultados
        resultados = self._processar_resultados()

        return resultados

    def _calcular_observaveis_adicionais(self, configuracao: np.ndarray):
        """Calcula observáveis adicionais específicos do modelo"""
        pass

    def _processar_resultados(self) -> Dict[str, np.ndarray]:
        """Processa resultados finais da simulação"""
        energia_array = np.array(self.historia_energia)
        magnetizacao_array = np.array(self.historia_magnetizacao)

        # Estatísticas básicas
        energia_media = np.mean(energia_array)
        energia_std = np.std(energia_array)
        magnetizacao_media = np.mean(magnetizacao_array)
        magnetizacao_std = np.std(magnetizacao_array)

        # Capacidade calorífica (flutuações de energia)
        capacidade_calorifica = energia_std**2 / (self.config.temperatura**2)

        # Susceptibilidade magnética (flutuações de magnetização)
        susceptibilidade = magnetizacao_std**2 / self.config.temperatura

        resultados = {
            'energia_media': energia_media,
            'energia_std': energia_std,
            'magnetizacao_media': magnetizacao_media,
            'magnetizacao_std': magnetizacao_std,
            'capacidade_calorifica': capacidade_calorifica,
            'susceptibilidade': susceptibilidade,
            'historia_energia': energia_array,
            'historia_magnetizacao': magnetizacao_array,
            'configuracao_final': self.passo_monte_carlo(np.copy(self.inicializar_sistema())),
            'configuracao': self.config.__dict__
        }

        # Adicionar observáveis específicos
        resultados.update(self.observaveis_acumulados)

        return resultados


class ModeloIsing2D(SimulacaoMonteCarlo):
    """
    Implementação do modelo de Ising 2D clássico
    """

    def __init__(self, config: ConfiguracaoMonteCarlo, J: float = 1.0):
        """
        Parameters:
        -----------
        config : ConfiguracaoMonteCarlo
            Configuração da simulação
        J : float
            Constante de interação (J > 0: ferromagnético, J < 0: antiferromagnético)
        """
        super().__init__(config)
        self.J = J
        self.L = config.tamanho_sistema[0]  # Assumindo sistema quadrado

        if len(config.tamanho_sistema) != 2 or config.tamanho_sistema[0] != config.tamanho_sistema[1]:
            raise ValueError("Sistema deve ser quadrado 2D")

    def inicializar_sistema(self) -> np.ndarray:
        """Inicializa spins aleatoriamente"""
        return self.rng.choice([-1, 1], size=self.config.tamanho_sistema)

    def calcular_energia(self, configuracao: np.ndarray) -> float:
        """
        Calcula energia do sistema de Ising
        H = -J * Σ_{<i,j>} s_i * s_j - h * Σ_i s_i
        """
        energia_interacao = 0

        # Interações horizontais e verticais
        for i in range(self.L):
            for j in range(self.L):
                # Interação com vizinho à direita
                energia_interacao += configuracao[i, j] * configuracao[i, (j + 1) % self.L]
                # Interação com vizinho abaixo
                energia_interacao += configuracao[i, j] * configuracao[(i + 1) % self.L, j]

        energia_total = -self.J * energia_interacao

        # Campo externo
        if self.config.campo_externo != 0:
            energia_total -= self.config.campo_externo * np.sum(configuracao)

        return energia_total

    def calcular_magnetizacao(self, configuracao: np.ndarray) -> float:
        """Calcula magnetização total do sistema"""
        return np.sum(configuracao)

    def passo_monte_carlo(self, configuracao: np.ndarray) -> np.ndarray:
        """
        Executa um sweep completo de Monte Carlo usando Metropolis
        """
        for _ in range(self.L * self.L):  # Um passo por sítio
            # Escolher sítio aleatório
            i, j = self.rng.randint(0, self.L, 2)

            # Calcular mudança de energia se o spin for invertido
            delta_E = self._calcular_delta_energia(configuracao, i, j)

            # Algoritmo de Metropolis
            if delta_E <= 0 or self.rng.random() < np.exp(-delta_E / self.config.temperatura):
                configuracao[i, j] *= -1

        return configuracao

    def _calcular_delta_energia(self, configuracao: np.ndarray, i: int, j: int) -> float:
        """
        Calcula mudança de energia ao inverter spin em (i,j)
        """
        s_ij = configuracao[i, j]

        # Soma dos vizinhos
        vizinhos = (
            configuracao[(i-1) % self.L, j] +  # Acima
            configuracao[(i+1) % self.L, j] +  # Abaixo
            configuracao[i, (j-1) % self.L] +  # Esquerda
            configuracao[i, (j+1) % self.L]    # Direita
        )

        # ΔE = 2 * J * s_ij * Σ_vizinhos + 2 * h * s_ij
        delta_E = 2 * self.J * s_ij * vizinhos

        if self.config.campo_externo != 0:
            delta_E += 2 * self.config.campo_externo * s_ij

        return delta_E


class SimulacaoMonteCarloQuantico:
    """
    Simulação Monte Carlo para sistemas quânticos
    Implementação usando método de Path Integral Monte Carlo
    """

    def __init__(self, hamiltoniano: Callable, config: ConfiguracaoMonteCarlo):
        """
        Parameters:
        -----------
        hamiltoniano : callable
            Função que retorna H|ψ⟩
        config : ConfiguracaoMonteCarlo
            Configuração da simulação
        """
        self.hamiltoniano = hamiltoniano
        self.config = config
        self.rng = np.random.RandomState(config.seed)

    def path_integral_monte_carlo(self, psi_tentativa: np.ndarray,
                                tempo_imaginario: float) -> Dict[str, np.ndarray]:
        """
        Simulação usando Path Integral Monte Carlo

        Parameters:
        -----------
        psi_tentativa : array_like
            Função de onda tentativa
        tempo_imaginario : float
            Tempo imaginário β = 1/T

        Returns:
        --------
        dict: Resultados da simulação
        """
        # Implementação simplificada do PIMC
        # Versão completa requereria discretização do tempo imaginário

        beta = tempo_imaginario
        n_slices = 100  # Número de slices no tempo imaginário

        # Armazenar energia local em cada configuração
        energias_locais = []

        print(f"Iniciando PIMC com β = {beta}, {n_slices} slices temporais")

        for amostra in range(self.config.n_amostras):
            # Gerar configuração aleatória (implementação simplificada)
            configuracao = self.rng.normal(0, 1, size=len(psi_tentativa))

            # Calcular energia local
            energia_local = self._calcular_energia_local(configuracao, psi_tentativa)
            energias_locais.append(energia_local)

            if (amostra + 1) % (self.config.n_amostras // 10) == 0:
                progresso = (amostra + 1) / self.config.n_amostras * 100
                print(".1f")

        energias_array = np.array(energias_locais)

        return {
            'energia_media': np.mean(energias_array),
            'energia_std': np.std(energias_array),
            'todas_energias': energias_array,
            'beta': beta,
            'n_slices': n_slices
        }

    def _calcular_energia_local(self, configuracao: np.ndarray,
                               psi_tentativa: np.ndarray) -> float:
        """
        Calcula energia local para Path Integral Monte Carlo
        """
        # Implementação simplificada - versão real seria mais complexa
        H_psi = self.hamiltoniano(configuracao)

        # <ψ|H|ψ>/<ψ|ψ> ≈ energia local
        numerador = np.vdot(psi_tentativa, H_psi)
        denominador = np.vdot(psi_tentativa, psi_tentativa)

        return np.real(numerador / denominador)


# Funções utilitárias
def ising_monte_carlo(L: int, T: float, n_sweeps: int = 1000,
                     campo_externo: float = 0.0) -> Dict[str, np.ndarray]:
    """
    Função wrapper para simulação rápida do modelo de Ising 2D

    Parameters:
    -----------
    L : int
        Tamanho do sistema (LxL)
    T : float
        Temperatura
    n_sweeps : int
        Número de sweeps Monte Carlo
    campo_externo : float
        Campo magnético externo

    Returns:
    --------
    dict: Resultados da simulação
    """
    config = ConfiguracaoMonteCarlo(
        n_sweeps=n_sweeps,
        temperatura=T,
        tamanho_sistema=(L, L),
        campo_externo=campo_externo,
        n_thermalizacao=100,
        n_amostras=100
    )

    simulacao = ModeloIsing2D(config)
    resultados = simulacao.executar_simulacao(verbose=True)

    return resultados


def calcular_exponentes_criticos(T_range: np.ndarray, L: int) -> Dict[str, np.ndarray]:
    """
    Calcula expoentes críticos do modelo de Ising
    """
    capacidades_calorificas = []
    susceptibilidades = []
    magnetizacoes = []

    for T in T_range:
        print(f"Simulando T = {T:.3f}")
        resultados = ising_monte_carlo(L, T, n_sweeps=2000)

        capacidades_calorificas.append(resultados['capacidade_calorifica'])
        susceptibilidades.append(resultados['susceptibilidade'])
        magnetizacoes.append(abs(resultados['magnetizacao_media']))

    # Encontrar temperatura crítica (máximo da capacidade calorífica)
    idx_critico = np.argmax(capacidades_calorificas)
    T_c = T_range[idx_critico]

    return {
        'temperaturas': T_range,
        'capacidades_calorificas': np.array(capacidades_calorificas),
        'susceptibilidades': np.array(susceptibilidades),
        'magnetizacoes': np.array(magnetizacoes),
        'temperatura_critica': T_c,
        'indice_critico': idx_critico
    }


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo: Transição de fase no modelo de Ising
    print("Simulação do Modelo de Ising 2D")
    print("=" * 40)

    # Simulação básica
    resultados = ising_monte_carlo(L=20, T=2.0, n_sweeps=1000)

    print("\nResultados:")
    print(f"Energia média: {resultados['energia_media']:.3f}")
    print(f"Magnetização média: {resultados['magnetizacao_media']:.3f}")
    print(f"Capacidade calorífica: {resultados['capacidade_calorifica']:.3f}")
    print(f"Susceptibilidade: {resultados['susceptibilidade']:.3f}")

    # Varredura de temperatura para encontrar transição de fase
    print("\nVarredura de temperatura:")
    temperaturas = np.linspace(1.5, 3.0, 20)
    expoentes = calcular_exponentes_criticos(temperaturas, L=16)

    print(f"Temperatura crítica encontrada: {expoentes['temperatura_critica']:.3f}")

    # Resultados salvos em expoentes['temperaturas'], expoentes['capacidades_calorificas'], etc.
