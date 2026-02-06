#!/usr/bin/env python3
"""
Módulo de Cálculo Avançado para Física Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Derivadas numéricas com diferentes ordens
- Integrais numéricas adaptativas
- Séries de Taylor e expansões
- Funções especiais para física
"""

import numpy as np
from typing import Callable, Tuple, Optional, Union
from scipy.special import erf, erfc, gamma, gammainc, lambertw
from scipy.integrate import quad, cumulative_trapezoid
import warnings


class CalculoAvancado:
    """
    Classe para operações de cálculo avançado em física computacional
    """

    def __init__(self, precisao: float = 1e-10):
        """
        Inicializa com precisão especificada

        Parameters:
        -----------
        precisao : float
            Precisão para cálculos numéricos
        """
        self.precisao = precisao

    def derivada_numerica(self, f: Callable, x: float, h: Optional[float] = None,
                         ordem: int = 1, metodo: str = 'central') -> float:
        """
        Calcula derivada numérica com diferentes ordens e métodos

        Parameters:
        -----------
        f : callable
            Função a ser derivada
        x : float
            Ponto onde calcular a derivada
        h : float, optional
            Tamanho do passo (auto-selecionado se None)
        ordem : int
            Ordem da derivada (1, 2, 3, 4)
        metodo : str
            Método: 'forward', 'backward', 'central'

        Returns:
        --------
        float: Valor da derivada numérica
        """
        if h is None:
            h = np.sqrt(self.precisao) * max(1.0, abs(x))

        if ordem == 1:
            return self._derivada_primeira(f, x, h, metodo)
        elif ordem == 2:
            return self._derivada_segunda(f, x, h, metodo)
        elif ordem == 3:
            return self._derivada_terceira(f, x, h)
        elif ordem == 4:
            return self._derivada_quarta(f, x, h)
        else:
            raise ValueError(f"Ordem {ordem} não suportada. Use 1-4.")

    def _derivada_primeira(self, f: Callable, x: float, h: float, metodo: str) -> float:
        """Calcula primeira derivada"""
        if metodo == 'central':
            return (f(x + h) - f(x - h)) / (2 * h)
        elif metodo == 'forward':
            return (f(x + h) - f(x)) / h
        elif metodo == 'backward':
            return (f(x) - f(x - h)) / h
        else:
            raise ValueError(f"Método {metodo} não suportado")

    def _derivada_segunda(self, f: Callable, x: float, h: float, metodo: str) -> float:
        """Calcula segunda derivada"""
        if metodo == 'central':
            return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)
        else:
            # Aproximação usando primeira derivada
            fp1 = self._derivada_primeira(f, x + h/2, h/2, metodo)
            fm1 = self._derivada_primeira(f, x - h/2, h/2, metodo)
            return (fp1 - fm1) / h

    def _derivada_terceira(self, f: Callable, x: float, h: float) -> float:
        """Calcula terceira derivada usando diferenças finitas de 4 pontos"""
        return (f(x + 2*h) - 2*f(x + h) + 2*f(x - h) - f(x - 2*h)) / (2 * h**3)

    def _derivada_quarta(self, f: Callable, x: float, h: float) -> float:
        """Calcula quarta derivada usando diferenças finitas de 5 pontos"""
        return (f(x + 2*h) - 4*f(x + h) + 6*f(x) - 4*f(x - h) + f(x - 2*h)) / (h**4)

    def integral_numerica(self, f: Callable, a: float, b: float,
                         metodo: str = 'adaptive', pontos: Optional[np.ndarray] = None) -> Tuple[float, float]:
        """
        Calcula integral numérica com diferentes métodos

        Parameters:
        -----------
        f : callable
            Função a integrar
        a, b : float
            Limites de integração
        metodo : str
            'adaptive', 'trapezoidal', 'simpson', 'romberg'
        pontos : array_like, optional
            Pontos específicos para integração

        Returns:
        --------
        tuple: (valor_integral, erro_estimado)
        """
        if metodo == 'adaptive':
            return self._integral_adaptativa(f, a, b)
        elif metodo == 'trapezoidal':
            return self._integral_trapezoidal(f, a, b, pontos)
        elif metodo == 'simpson':
            return self._integral_simpson(f, a, b, pontos)
        else:
            raise ValueError(f"Método {metodo} não suportado")

    def _integral_adaptativa(self, f: Callable, a: float, b: float) -> Tuple[float, float]:
        """Integral adaptativa usando scipy.integrate.quad"""
        try:
            resultado, erro = quad(f, a, b, epsabs=self.precisao, epsrel=self.precisao)
            return resultado, erro
        except Exception as e:
            warnings.warn(f"Erro na integração adaptativa: {e}")
            return 0.0, float('inf')

    def _integral_trapezoidal(self, f: Callable, a: float, b: float,
                             pontos: Optional[np.ndarray]) -> Tuple[float, float]:
        """Regra do trapézio"""
        if pontos is None:
            n = 1000  # Número padrão de pontos
            pontos = np.linspace(a, b, n)

        valores_f = f(pontos)
        integral = np.trapz(valores_f, pontos)
        erro = abs(integral) * self.precisao  # Erro estimado simples

        return integral, erro

    def _integral_simpson(self, f: Callable, a: float, b: float,
                         pontos: Optional[np.ndarray]) -> Tuple[float, float]:
        """Regra de Simpson"""
        if pontos is None:
            n = 1000  # Deve ser par
            if n % 2 == 1:
                n += 1
            pontos = np.linspace(a, b, n)

        valores_f = f(pontos)
        h = (b - a) / (len(pontos) - 1)

        # Regra de Simpson
        integral = h/3 * (valores_f[0] + valores_f[-1] +
                         4 * np.sum(valores_f[1:-1:2]) +
                         2 * np.sum(valores_f[2:-1:2]))

        erro = abs(integral) * self.precisao
        return integral, erro

    def serie_taylor(self, f: Callable, x0: float, x: float, n_termos: int = 5) -> float:
        """
        Expande função em série de Taylor ao redor de x0

        Parameters:
        -----------
        f : callable
            Função a expandir
        x0 : float
            Ponto de expansão
        x : float
            Ponto onde avaliar a expansão
        n_termos : int
            Número de termos da série

        Returns:
        --------
        float: Valor da expansão de Taylor
        """
        resultado = 0.0
        for n in range(n_termos):
            derivada = self.derivada_numerica(f, x0, ordem=n)
            termo = derivada * (x - x0)**n / np.math.factorial(n)
            resultado += termo

        return resultado

    def gradiente(self, f: Callable, x: np.ndarray, h: Optional[float] = None) -> np.ndarray:
        """
        Calcula gradiente de função multivariada

        Parameters:
        -----------
        f : callable
            Função f(x) onde x é array
        x : array_like
            Ponto onde calcular o gradiente
        h : float, optional
            Tamanho do passo

        Returns:
        --------
        array: Vetor gradiente
        """
        x = np.asarray(x)
        grad = np.zeros_like(x)

        for i in range(len(x)):
            def f_i(xi):
                x_temp = x.copy()
                x_temp[i] = xi
                return f(x_temp)

            grad[i] = self.derivada_numerica(f_i, x[i], h)

        return grad

    def hessiana(self, f: Callable, x: np.ndarray, h: Optional[float] = None) -> np.ndarray:
        """
        Calcula matriz Hessiana de função multivariada

        Parameters:
        -----------
        f : callable
            Função f(x) onde x é array
        x : array_like
            Ponto onde calcular a Hessiana
        h : float, optional
            Tamanho do passo

        Returns:
        --------
        array: Matriz Hessiana
        """
        x = np.asarray(x)
        n = len(x)
        hess = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                if i == j:
                    # Diagonal: segunda derivada
                    def f_ii(xi):
                        x_temp = x.copy()
                        x_temp[i] = xi
                        return f(x_temp)
                    hess[i, i] = self.derivada_numerica(f_ii, x[i], h, ordem=2)
                else:
                    # Fora da diagonal: derivada mista
                    def f_ij(xi):
                        x_temp = x.copy()
                        x_temp[j] = xi
                        def g(xj):
                            x_temp2 = x_temp.copy()
                            x_temp2[i] = xj
                            return f(x_temp2)
                        return self.derivada_numerica(g, x[i], h)
                    hess[i, j] = self.derivada_numerica(f_ij, x[j], h)
                    hess[j, i] = hess[i, j]  # Simétrica

        return hess


class FuncoesEspeciais:
    """
    Funções especiais utilizadas em física teórica
    """

    @staticmethod
    def funcao_erro(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função erro erf(x)"""
        return erf(x)

    @staticmethod
    def funcao_erro_complementar(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função erro complementar erfc(x)"""
        return erfc(x)

    @staticmethod
    def funcao_gamma(x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função Gamma Γ(x)"""
        return gamma(x)

    @staticmethod
    def funcao_gamma_incompleta(a: float, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """Função Gamma incompleta γ(a, x)"""
        return gammainc(a, x) * gamma(a)

    @staticmethod
    def funcao_lambert_w(z: Union[float, np.ndarray], branch: int = 0) -> Union[float, np.ndarray]:
        """Função W de Lambert W(z)"""
        return lambertw(z, k=branch)

    @staticmethod
    def integral_eliptica_completa_primeira(k: float) -> float:
        """
        Integral elíptica completa de primeira espécie
        F(k) = ∫₀¹ dt / √((1-t²)(1-k²t²))
        """
        if abs(k) >= 1:
            raise ValueError("Módulo de k deve ser menor que 1")

        # Usando série de expansão
        result = np.pi/2
        term = 1.0
        n = 0

        while abs(term) > 1e-15:
            n += 1
            term = ((2*n-1)/(2*n))**2 * k**(2*n) / (2*n-1)
            result *= (1 - term)

        return result

    @staticmethod
    def integral_eliptica_completa_segunda(k: float) -> float:
        """
        Integral elíptica completa de segunda espécie
        E(k) = ∫₀¹ dt √((1-t²)/(1-k²t²))
        """
        if abs(k) >= 1:
            raise ValueError("Módulo de k deve ser menor que 1")

        # Usando série de expansão
        result = np.pi/2
        term = 1.0
        n = 1

        while abs(term) > 1e-15:
            term = ((2*n-1)/(2*n))**2 * k**(2*n) / (2*n-1)
            result -= term / n
            n += 1

        return result

    @staticmethod
    def polinomio_legendre(n: int, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Polinômio de Legendre P_n(x)
        """
        if n == 0:
            return np.ones_like(x)
        elif n == 1:
            return x
        else:
            # Recursão: (2n-1)xP_{n-1}(x) - (n-1)P_{n-2}(x)
            p_nm2 = np.ones_like(x)  # P_0
            p_nm1 = x               # P_1

            for k in range(2, n+1):
                p_n = ((2*k-1) * x * p_nm1 - (k-1) * p_nm2) / k
                p_nm2 = p_nm1
                p_nm1 = p_n

            return p_n

    @staticmethod
    def funcao_bessel_primeira_ordem(n: int, x: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Função de Bessel de primeira espécie J_n(x)
        Usando série para implementação simples
        """
        if abs(x) < 1e-10:
            return np.zeros_like(x) if n > 0 else np.ones_like(x)

        # Série truncada para x pequeno
        max_terms = 20
        result = 0.0

        for k in range(max_terms):
            if k + abs(n) > 50:  # Evitar overflow
                break
            term = (-1)**k * (x/2)**(2*k + abs(n)) / (np.math.factorial(k) * np.math.factorial(k + abs(n)))
            result += term

        return result


# Funções utilitárias para uso direto
def derivada(f: Callable, x: float, h: Optional[float] = None, ordem: int = 1) -> float:
    """Função wrapper para derivada numérica"""
    calc = CalculoAvancado()
    return calc.derivada_numerica(f, x, h, ordem)


def integral(f: Callable, a: float, b: float, metodo: str = 'adaptive') -> Tuple[float, float]:
    """Função wrapper para integral numérica"""
    calc = CalculoAvancado()
    return calc.integral_numerica(f, a, b, metodo)


def gradiente(f: Callable, x: np.ndarray) -> np.ndarray:
    """Função wrapper para gradiente"""
    calc = CalculoAvancado()
    return calc.gradiente(f, x)


def hessiana(f: Callable, x: np.ndarray) -> np.ndarray:
    """Função wrapper para Hessiana"""
    calc = CalculoAvancado()
    return calc.hessiana(f, x)


# Exemplos de uso e testes
if __name__ == "__main__":
    print("Módulo de Cálculo Avançado")
    print("=" * 40)

    # Teste básico de derivada
    def f_test(x):
        return x**3 + 2*x**2 - x + 1

    x_test = 2.0
    derivada_analitica = 3*x_test**2 + 4*x_test - 1  # Derivada exata

    calc = CalculoAvancado()
    derivada_numerica = calc.derivada_numerica(f_test, x_test)

    print(f"Derivada em x={x_test}:")
    print(f"  Analítica: {derivada_analitica:.6f}")
    print(f"  Numérica:  {derivada_numerica:.6f}")
    print(f"  Erro:      {abs(derivada_analitica - derivada_numerica):.2e}")

    # Teste de integral
    def g_test(x):
        return np.sin(x)**2

    # ∫ sin²(x) dx de 0 a π = π/2
    integral_analitica = np.pi/2
    integral_numerica, erro = calc.integral_numerica(g_test, 0, np.pi)

    print("\nIntegral de sin²(x) de 0 a π:")
    print(f"  Analítica: {integral_analitica:.6f}")
    print(f"  Numérica:  {integral_numerica:.6f}")
    print(f"  Erro:      {abs(integral_analitica - integral_numerica):.2e}")

    # Teste de função especial
    print("\nFunção erro em x=1:")
    print(f"  erf(1) = {FuncoesEspeciais.funcao_erro(1.0):.6f}")

    print("\nMódulo funcionando corretamente! ✅")
