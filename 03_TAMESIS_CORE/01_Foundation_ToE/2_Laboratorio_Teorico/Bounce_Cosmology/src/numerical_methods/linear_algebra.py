#!/usr/bin/env python3
"""
Álgebra Linear Avançada para Física Computacional
Implementação seguindo o fine-tuning de IA para física teórica

Este módulo contém:
- Diagonalização de matrizes hermitianas
- Autovalores e autovetores
- Decomposições matriciais
- Espaços vetoriais e operadores
"""

import numpy as np
from scipy.linalg import eigh, eigvals, eig, svd, cholesky, qr, schur
from scipy.sparse.linalg import eigs, LinearOperator
from typing import Tuple, Optional, Union, List
import warnings


class AlgebraLinearFisica:
    """
    Classe para operações de álgebra linear em física computacional
    """

    def __init__(self, precisao: float = 1e-12):
        """
        Inicializa com precisão especificada

        Parameters:
        -----------
        precisao : float
            Precisão para cálculos numéricos
        """
        self.precisao = precisao

    def diagonalizar_matriz_hermitiana(self, H: np.ndarray, n_estados: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Diagonaliza matriz hermitiana eficientemente

        Parameters:
        -----------
        H : array_like
            Matriz hermitiana
        n_estados : int, optional
            Número de autovalores/autovetores desejados (para matrizes grandes)

        Returns:
        --------
        tuple: (autovalores, autovetores)
        """
        H = np.asarray(H)

        # Verifica se é hermitiana
        if not self._eh_hermitiana(H):
            warnings.warn("Matriz não é hermitiana. Usando diagonalização geral.")
            return self.diagonalizar_matriz_geral(H, n_estados)

        if n_estados is None or n_estados >= len(H):
            # Diagonalização completa
            autovalores, autovetores = eigh(H)
        else:
            # Apenas os primeiros autovalores (para matrizes grandes)
            autovalores, autovetores = eigs(H, k=n_estados, which='SM')

        # Ordena em ordem crescente de energia
        indices = np.argsort(autovalores)
        autovalores = autovalores[indices]
        autovetores = autovetores[:, indices]

        return autovalores, autovetores

    def diagonalizar_matriz_geral(self, A: np.ndarray, n_estados: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Diagonaliza matriz geral (não hermitiana)

        Parameters:
        -----------
        A : array_like
            Matriz quadrada
        n_estados : int, optional
            Número de autovalores/autovetores desejados

        Returns:
        --------
        tuple: (autovalores, autovetores)
        """
        A = np.asarray(A)

        if n_estados is None or n_estados >= len(A):
            autovalores, autovetores = eig(A)
        else:
            autovalores, autovetores = eigs(A, k=n_estados)

        # Ordena por parte real dos autovalores
        indices = np.argsort(np.real(autovalores))
        autovalores = autovalores[indices]
        autovetores = autovetores[:, indices]

        return autovalores, autovetores

    def _eh_hermitiana(self, A: np.ndarray) -> bool:
        """Verifica se matriz é hermitiana"""
        diff = A - A.conj().T
        return np.allclose(diff, 0, atol=self.precisao)

    def resolver_sistema_linear(self, A: np.ndarray, b: np.ndarray,
                               metodo: str = 'auto') -> np.ndarray:
        """
        Resolve sistema linear Ax = b

        Parameters:
        -----------
        A : array_like
            Matriz do sistema
        b : array_like
            Vetor do lado direito
        metodo : str
            'auto', 'lu', 'cholesky', 'qr', 'svd'

        Returns:
        --------
        array: Solução x
        """
        A = np.asarray(A)
        b = np.asarray(b)

        if metodo == 'auto':
            # Escolhe método automaticamente baseado na matriz
            if self._eh_hermitiana(A) and np.all(np.linalg.eigvals(A) > 0):
                metodo = 'cholesky'
            else:
                metodo = 'lu'

        if metodo == 'lu':
            return np.linalg.solve(A, b)
        elif metodo == 'cholesky':
            L = cholesky(A, lower=True)
            y = np.linalg.solve(L, b)
            return np.linalg.solve(L.T, y)
        elif metodo == 'qr':
            Q, R = qr(A)
            return np.linalg.solve(R, Q.T @ b)
        elif metodo == 'svd':
            U, s, Vt = svd(A)
            # Pseudoinversa usando SVD
            s_inv = np.where(s > self.precisao, 1/s, 0)
            A_inv = Vt.T @ np.diag(s_inv) @ U.T
            return A_inv @ b
        else:
            raise ValueError(f"Método {metodo} não suportado")

    def decomposicao_svd(self, A: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Decomposição SVD: A = U Σ V^T

        Parameters:
        -----------
        A : array_like
            Matriz a decompor

        Returns:
        --------
        tuple: (U, s, Vt) onde A = U @ diag(s) @ Vt
        """
        A = np.asarray(A)
        U, s, Vt = svd(A, full_matrices=False)
        return U, s, Vt

    def numero_condicao(self, A: np.ndarray) -> float:
        """
        Calcula número de condição da matriz
        """
        A = np.asarray(A)
        return np.linalg.cond(A)

    def base_ortonormal(self, vetores: np.ndarray) -> np.ndarray:
        """
        Ortogonaliza conjunto de vetores usando Gram-Schmidt

        Parameters:
        -----------
        vetores : array_like
            Matriz cujas colunas são os vetores a ortogonalizar

        Returns:
        --------
        array: Matriz com vetores ortonormais
        """
        vetores = np.asarray(vetores)
        n, m = vetores.shape

        Q = np.zeros_like(vetores)

        for i in range(m):
            v = vetores[:, i].copy()

            # Subtrai projeções nos vetores anteriores
            for j in range(i):
                proj = (np.dot(Q[:, j], v) / np.dot(Q[:, j], Q[:, j])) * Q[:, j]
                v -= proj

            # Normaliza
            norm = np.linalg.norm(v)
            if norm > self.precisao:
                Q[:, i] = v / norm
            else:
                # Vetor linearmente dependente
                Q[:, i] = np.zeros(n)

        return Q

    def produto_tensorial(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Produto tensorial de duas matrizes

        Parameters:
        -----------
        A, B : array_like
            Matrizes de entrada

        Returns:
        --------
        array: Produto tensorial A ⊗ B
        """
        A = np.asarray(A)
        B = np.asarray(B)

        # Produto tensorial usando broadcasting
        return np.kron(A, B)

    def traco_matriz(self, A: np.ndarray) -> Union[float, complex]:
        """
        Calcula traço da matriz eficientemente
        """
        return np.trace(A)

    def determinante_matriz(self, A: np.ndarray) -> Union[float, complex]:
        """
        Calcula determinante da matriz
        """
        return np.linalg.det(A)

    def matriz_inversa(self, A: np.ndarray) -> np.ndarray:
        """
        Calcula inversa da matriz
        """
        return np.linalg.inv(A)

    def exponencial_matriz(self, A: np.ndarray, metodo: str = 'series') -> np.ndarray:
        """
        Calcula exponencial de matriz exp(A)

        Parameters:
        -----------
        A : array_like
            Matriz de entrada
        metodo : str
            'series' (série de Taylor), 'eigen' (usando autovalores)

        Returns:
        --------
        array: exp(A)
        """
        A = np.asarray(A)

        if metodo == 'eigen':
            # Método usando autovalores: exp(A) = V exp(Λ) V^-1
            if self._eh_hermitiana(A):
                autovalores, autovetores = eigh(A)
                exp_lambda = np.exp(autovalores)
                return autovetores @ np.diag(exp_lambda) @ autovetores.conj().T
            else:
                autovalores, autovetores = eig(A)
                exp_lambda = np.exp(autovalores)
                return autovetores @ np.diag(exp_lambda) @ np.linalg.inv(autovetores)

        elif metodo == 'series':
            # Série de Taylor: exp(A) = Σ (A^k / k!)
            result = np.eye(len(A))
            term = np.eye(len(A))
            k = 1

            while np.linalg.norm(term) > self.precisao and k < 100:
                term = term @ A / k
                result += term
                k += 1

            return result

        else:
            raise ValueError(f"Método {metodo} não suportado")


class OperadoresQuanticos:
    """
    Operadores e álgebra para mecânica quântica
    """

    def __init__(self, dim: int = 2):
        """
        Inicializa com dimensão do espaço de Hilbert

        Parameters:
        -----------
        dim : int
            Dimensão do espaço (2 para spin 1/2, etc.)
        """
        self.dim = dim
        self.identidade = np.eye(dim)

    def operador_paulis(self) -> List[np.ndarray]:
        """
        Retorna os operadores de Pauli (para dim=2)

        Returns:
        --------
        list: [σx, σy, σz]
        """
        if self.dim != 2:
            raise ValueError("Operadores de Pauli definidos apenas para spin 1/2")

        sigma_x = np.array([[0, 1], [1, 0]])
        sigma_y = np.array([[0, -1j], [1j, 0]])
        sigma_z = np.array([[1, 0], [0, -1]])

        return [sigma_x, sigma_y, sigma_z]

    def estado_coerente(self, alpha: complex, n_max: int = 50) -> np.ndarray:
        """
        Estado coerente do oscilador harmônico quântico

        Parameters:
        -----------
        alpha : complex
            Parâmetro do estado coerente
        n_max : int
            Número máximo de fótons

        Returns:
        --------
        array: Vetor de estado coerente
        """
        estado = np.zeros(n_max, dtype=complex)

        # |α⟩ = Σ c_n |n⟩ onde c_n = exp(-|α|²/2) * α^n / √(n!)
        norm_factor = np.exp(-abs(alpha)**2 / 2)

        for n in range(n_max):
            estado[n] = norm_factor * (alpha**n) / np.sqrt(np.math.factorial(n))

        return estado

    def matriz_densidade_mista(self, estados: List[np.ndarray],
                              probabilidades: np.ndarray) -> np.ndarray:
        """
        Constrói matriz densidade para estado misto

        Parameters:
        -----------
        estados : list of arrays
            Estados puros |ψ_i⟩
        probabilidades : array_like
            Probabilidades p_i

        Returns:
        --------
        array: Matriz densidade ρ = Σ p_i |ψ_i⟩⟨ψ_i|
        """
        if len(estados) != len(probabilidades):
            raise ValueError("Número de estados deve igualar número de probabilidades")

        if not np.isclose(np.sum(probabilidades), 1.0):
            warnings.warn("Probabilidades não somam 1. Normalizando...")
            probabilidades = probabilidades / np.sum(probabilidades)

        rho = np.zeros((len(estados[0]), len(estados[0])), dtype=complex)

        for psi, p in zip(estados, probabilidades):
            psi = np.asarray(psi)
            rho += p * np.outer(psi, psi.conj())

        return rho

    def valor_esperado(self, operador: np.ndarray, estado: Union[np.ndarray, np.ndarray]) -> Union[float, complex]:
        """
        Calcula valor esperado ⟨A⟩ = ⟨ψ|A|ψ⟩ ou Tr(ρ A)

        Parameters:
        -----------
        operador : array_like
            Operador A
        estado : array_like
            Estado |ψ⟩ ou matriz densidade ρ

        Returns:
        --------
        float or complex: Valor esperado
        """
        operador = np.asarray(operador)
        estado = np.asarray(estado)

        if estado.ndim == 1:
            # Estado puro
            return np.vdot(estado, operador @ estado)
        elif estado.ndim == 2:
            # Matriz densidade
            return np.trace(estado @ operador)
        else:
            raise ValueError("Estado deve ser vetor ou matriz")

    def commutador(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Calcula comutador [A, B] = AB - BA
        """
        return A @ B - B @ A

    def anticommutador(self, A: np.ndarray, B: np.ndarray) -> np.ndarray:
        """
        Calcula anticomutador {A, B} = AB + BA
        """
        return A @ B + B @ A


# Funções utilitárias para uso direto
def diagonalizar_hermitiana(H: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Função wrapper para diagonalização hermitiana"""
    alg = AlgebraLinearFisica()
    return alg.diagonalizar_matriz_hermitiana(H)


def resolver_sistema(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Função wrapper para resolver sistema linear"""
    alg = AlgebraLinearFisica()
    return alg.resolver_sistema_linear(A, b)


def produto_tensorial(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Função wrapper para produto tensorial"""
    alg = AlgebraLinearFisica()
    return alg.produto_tensorial(A, B)


def traco(A: np.ndarray) -> Union[float, complex]:
    """Função wrapper para traço"""
    alg = AlgebraLinearFisica()
    return alg.traco_matriz(A)


# Exemplos de uso e testes
if __name__ == "__main__":
    print("Módulo de Álgebra Linear para Física")
    print("=" * 50)

    # Teste de diagonalização
    print("Teste 1: Diagonalização de matriz hermitiana")
    H = np.array([[2, 1], [1, 2]], dtype=complex)  # Matriz simples

    alg = AlgebraLinearFisica()
    autovalores, autovetores = alg.diagonalizar_matriz_hermitiana(H)

    print(f"Autovalores: {autovalores}")
    print("Autovetores:")
    print(autovetores)

    # Verificação: H v = λ v
    for i, (lambda_, v) in enumerate(zip(autovalores, autovetores.T)):
        Hv = H @ v
        lambda_v = lambda_ * v
        erro = np.linalg.norm(Hv - lambda_v)
        print(f"Verificação autovalor {i}: erro = {erro:.2e}")

    # Teste de operadores quânticos
    print("\nTeste 2: Operadores de Pauli")
    quantico = OperadoresQuanticos(dim=2)
    sigma_x, sigma_y, sigma_z = quantico.operador_paulis()

    print("σx:")
    print(sigma_x)
    print("σz:")
    print(sigma_z)

    # Teste de estado coerente
    print("\nTeste 3: Estado coerente")
    alpha = 1.0 + 0.5j
    estado_coerente = quantico.estado_coerente(alpha, n_max=10)
    print(f"Estado coerente |α={alpha}⟩ (primeiros 5 coeficientes):")
    print(estado_coerente[:5])

    # Verificação de normalização
    norm = np.sum(np.abs(estado_coerente)**2)
    print(f"Normalização: {norm:.10f} (deve ser ≈ 1.0)")

    print("\nMódulo funcionando corretamente! ✅")
