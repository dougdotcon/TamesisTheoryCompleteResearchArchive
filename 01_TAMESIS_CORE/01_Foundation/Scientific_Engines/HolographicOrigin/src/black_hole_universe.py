"""
Universos dentro de Buracos Negros (Conexão Gaztañaga)
Implementação da hipótese BHU (Black Hole Universe)

Este módulo conecta a geometria de Schwarzschild (interior) com cosmologia FLRW,
servindo como gerador de condições iniciais para o modelo de Rebote.

Referências:
- Gaztañaga, E. et al. (2024). "The Black Hole Universe".
- Pathria, R. K. (1972). "The Universe as a Black Hole".
"""

import numpy as np
from typing import Tuple, Dict, Optional, Union
from .relativity import BuracosNegros, CosmologiaRelatividade, CamposEscalarAcoplados

class UniversosBuracoNegro(BuracosNegros):
    """
    Simulador da hipótese de que nosso universo é o interior de um BN.
    Herda da classe base de Buracos Negros.
    """

    def __init__(self, M_parent: float, G: float = 6.674e-11, c: float = 2.998e8):
        """
        Parameters:
        -----------
        M_parent : float
            Massa do buraco negro "pai" (no universo exterior)
            Em unidades solares
        G : float
            Constante gravitacional (SI default)
        c : float
            Velocidade da luz (SI default)
        """
        self.G = G
        self.c = c
        self.M_parent = M_parent
        
        # Calcular raio de Schwarzschild do pai (Horizonte de Eventos)
        # R_s = 2GM/c²
        self.M_kg = M_parent * 1.989e30
        self.R_s_m = 2 * self.G * self.M_kg / (self.c**2)
        self.R_s_km = self.R_s_m / 1000.0

        # Tempo característico (SI)
        self.t_max = np.pi * self.G * self.M_kg / (self.c**3)
        
        # Constantes de Planck para adimensionalização
        self.hbar = 1.054e-34
        self.t_planck = np.sqrt(self.hbar * self.G / self.c**5)
        self.l_planck = self.c * self.t_planck
        self.m_planck = np.sqrt(self.hbar * self.c / self.G)
        self.rho_planck = self.m_planck / (self.l_planck**3) # Densidade de Planck

    def inversao_metrica_interior(self, r_interior: float) -> Dict[str, float]:
        """
        Realiza a inversão da métrica de Schwarzschild para o interior (r < Rs).
        Retorna valores em unidades SI.
        """
        if r_interior >= self.R_s_m:
            # Proteção para horizonte
             r_interior = self.R_s_m * 0.999999

        # Fator de escala efetivo (adimensionalizado pelo Rs)
        a_eff = r_interior / self.R_s_m
        
        # Densidade efetiva (SI)
        # rho ~ c^2 / (G r^2)
        rho_eff = 3 * (self.c**2) / (8 * np.pi * self.G * r_interior**2)
        
        # Hubble parameter (SI) 1/s
        term = (self.R_s_m / r_interior) - 1
        if term < 0: term = 0 
        
        H_eff = (self.c / r_interior) * np.sqrt(term)
        
        return {
            'a_eff': a_eff,
            'H_eff': H_eff,
            'rho_vacuum_eff': rho_eff
        }

    def verificar_condicao_bhu(self, H0_target: float) -> Tuple[bool, float]:
        """
        Verifica a hipótese BHU comparando Rs com Hubbard Radius.
        H0_target em km/s/Mpc
        """
        # H0 em unidades SI (1/s)
        # 1 Mpc = 3.086e19 km
        H0_si = H0_target / (3.086e19) 
        
        R_H = self.c / H0_si
        
        razao = self.R_s_m / R_H
        match = abs(razao - 1.0) < 0.2 # 20% de margem
        
        return match, razao

    def gerar_condicoes_iniciais_rebote(self) -> Dict[str, float]:
        """
        Gera condições iniciais em UNIDADES NATURAIS (G=c=hbar=1).
        Define o ponto de partida onde H ~ 0.1 (escala substancialmente Planckiana),
        evitando valores transfinitos que quebram o integrador.
        """
        
        # Encontrar r onde H_nat ~ 0.1
        # H_eff ~ c/r * sqrt(Rs/r) ~ c * sqrt(Rs) / r^(3/2)
        # H_nat = H_eff * t_planck ~ 0.1
        # c * sqrt(Rs) / r^(3/2) * t_planck = 0.1
        # r^(3/2) = c * sqrt(Rs) * t_planck / 0.1
        # r = (10 * c * t_planck * sqrt(Rs))^(2/3)
        
        # Simplificando: H_nat ~ l_planck * sqrt(Rs) / r^(3/2) ... (dimensionalmente approx)
        # Vamos calcular explicitamente
        
        target_H_nat = 0.1
        
        # H_eff_target = target_H_nat / self.t_planck
        H_eff_target = target_H_nat / self.t_planck
        
        # Resolvendo H_eff = c/r * sqrt(Rs/r) = c * Rs^0.5 * r^-1.5
        # r^1.5 = c * Rs^0.5 / H_eff
        # r = (c * Rs^0.5 / H_eff)^(2/3)
        
        term_numerator = self.c * np.sqrt(self.R_s_m)
        r_start = (term_numerator / H_eff_target)**(2/3)
        
        props_si = self.inversao_metrica_interior(r_start)
        
        # Conversão direta
        H_nat = props_si['H_eff'] * self.t_planck
        
        # Densidade Planckiana natural
        # rho_nat = 3 H^2 / 8pi
        rho_nat = 3 * H_nat**2 / (8 * np.pi)
        
        condicoes = {
            'a_inicial': props_si['a_eff'], # Adimensional
            'phi_inicial': 1.0, 
            'rho_m_inicial': 0.0, # Vácuo domina
            'H_inicial': H_nat, # Deve ser prox de 0.1
            'pi_phi_inicial': 0.0
        }
        
        return condicoes


def validar_multiverso(M_test_sun: float = 1e23):
    """
    Função de conveniência para rodar teste rápido
    Nosso universo tem massa aprox 10^23 M_sol se for um BN (densidade critica * volume Hubble)
    """
    bhu = UniversosBuracoNegro(M_parent=M_test_sun)
    match, razao = bhu.verificar_condicao_bhu(H0_target=70.0)
    
    print(f"Testando Universo com Massa M = {M_test_sun:.2e} M_sol")
    print(f"Raio de Schwarzschild: {bhu.R_s_km:.2e} km")
    print(f"Razão R_s / R_Hubble: {razao:.4f}")
    if match:
        print("✅ CONSISTENTE: Pode ser um Universo Buraco Negro (BHU)")
    else:
        print("❌ INCONSISTENTE com H0=70 km/s/Mpc")
        
    return bhu

if __name__ == "__main__":
    # Teste rápido: Universo com massa observável estimada
    # Massa dentro do horizonte ~ 10^53 kg ~ 5e22 M_sol
    validar_multiverso(5e22)
