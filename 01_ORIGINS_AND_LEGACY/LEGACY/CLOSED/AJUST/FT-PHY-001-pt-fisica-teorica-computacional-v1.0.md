# FT-PHY-001: Fine-Tuning para IA em Física Teórica e Experimental Computacional

## Visão Geral do Projeto

Este documento foi sintetizado a partir do projeto "Como se Tornar um BOM Físico Teórico", baseado no trabalho de Gerard 't Hooft. O objetivo é criar um fine-tuning especializado para modelos de IA que desenvolvam soluções computacionais em física teórica e experimental.

### Contexto Filosófico
A física teórica é comparada a um arranha-céu: fundações sólidas em matemática elementar e física clássica, progredindo para tópicos avançados. O estudo deve ser rigoroso, com ênfase em verificação independente e desenvolvimento de intuição física.

### Metodologia de Aprendizado Recomendada
1. **Estudo Sistemático**: Seguir sequência lógica de tópicos
2. **Prática Intensiva**: Resolver exercícios e problemas
3. **Verificação Independente**: Não aceitar afirmações por fé
4. **Persistência**: Navegar na internet, encontrar recursos adicionais
5. **Integração**: Conectar conceitos matemáticos com aplicações físicas

---

## 1. FUNDAMENTOS MATEMÁTICOS ESSENCIAIS

### 1.1 Análise e Cálculo
```python
# Exemplo: Resolução numérica de EDO usando Runge-Kutta
import numpy as np

def runge_kutta_4(f, y0, t0, tf, h):
    """
    Método de Runge-Kutta de 4ª ordem para EDO: dy/dt = f(t,y)
    """
    t_values = np.arange(t0, tf + h, h)
    y_values = np.zeros(len(t_values))
    y_values[0] = y0

    for i in range(1, len(t_values)):
        t = t_values[i-1]
        y = y_values[i-1]

        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)

        y_values[i] = y + (k1 + 2*k2 + 2*k3 + k4)/6

    return t_values, y_values
```

**Conceitos Críticos:**
- Equações diferenciais ordinárias e parciais
- Análise complexa e teoria de resíduos
- Transformadas integrais (Fourier, Laplace)
- Teoria de distribuições e delta de Dirac

### 1.2 Álgebra Linear e Espaços Vetoriais
```python
# Exemplo: Diagonalização de matrizes hermitianas
import numpy as np
from scipy.linalg import eigh

def quantum_states_solver(H):
    """
    Resolve autovalores e autovetores para Hamiltonian quântico
    H: matriz hermitiana representando o Hamiltonian
    """
    eigenvalues, eigenvectors = eigh(H)

    # Normalizar autovetores
    eigenvectors = eigenvectors / np.linalg.norm(eigenvectors, axis=0)

    return eigenvalues, eigenvectors
```

**Tópicos Essenciais:**
- Espaços de Hilbert e operadores
- Decomposição espectral
- Teoria de representações de grupos
- Álgebras de Lie

### 1.3 Geometria Diferencial e Tensores
```python
# Exemplo: Cálculo tensorial em relatividade geral
def christoffel_symbols(metric, coords):
    """
    Calcula símbolos de Christoffel para uma métrica dada
    metric: tensor métrico g_μν
    coords: coordenadas do espaço-tempo
    """
    # Implementação simplificada - versão completa requer bibliotecas especializadas
    pass

def riemann_tensor(metric, christoffel):
    """
    Calcula tensor de Riemann a partir da métrica
    """
    # Implementação para cálculo de curvatura espaço-temporal
    pass
```

**Conceitos Fundamentais:**
- Variedades diferenciáveis
- Conexões afins e curvatura
- Formas diferenciais
- Fibrados vetoriais

---

## 2. FÍSICA COMPUTACIONAL: MÉTODOS NUMÉRICOS

### 2.1 Mecânica Clássica Computacional
**Métodos Essenciais:**
- Integração de equações de movimento (Verlet, Leapfrog)
- Sistemas de muitos corpos (N-corpos)
- Dinâmica molecular
- Teoria do caos e atratores

```python
# Exemplo: Simulação de sistema solar simplificado
def n_body_simulation(positions, velocities, masses, dt, steps):
    """
    Simulação de N corpos gravitacionais
    """
    n_bodies = len(masses)
    trajectory = [positions.copy()]

    for _ in range(steps):
        # Calcular forças gravitacionais
        forces = np.zeros_like(positions)

        for i in range(n_bodies):
            for j in range(n_bodies):
                if i != j:
                    r = positions[j] - positions[i]
                    r_norm = np.linalg.norm(r)
                    force_magnitude = G * masses[i] * masses[j] / (r_norm ** 2)
                    forces[i] += force_magnitude * r / r_norm

        # Atualizar velocidades e posições (método de Verlet)
        velocities += forces * dt / masses[:, np.newaxis]
        positions += velocities * dt

        trajectory.append(positions.copy())

    return trajectory
```

### 2.2 Física Quântica Computacional
**Técnicas Avançadas:**
- Método de diferenças finitas para equação de Schrödinger
- Método de elementos finitos
- Monte Carlo quântico
- Teoria de perturbação numérica

```python
# Exemplo: Solução numérica da equação de Schrödinger 1D
def schrodinger_solver(V, x_min, x_max, n_points, n_states=5):
    """
    Resolve equação de Schrödinger para potencial V(x)
    """
    x = np.linspace(x_min, x_max, n_points)
    dx = x[1] - x[0]

    # Construir matriz Hamiltoniana
    H = np.zeros((n_points, n_points))

    # Termo cinético (diferenças finitas)
    for i in range(1, n_points-1):
        H[i, i-1] = -hbar**2 / (2 * m * dx**2)
        H[i, i] = hbar**2 / (m * dx**2) + V(x[i])
        H[i, i+1] = -hbar**2 / (2 * m * dx**2)

    # Autovalores e autovetores
    eigenvalues, eigenvectors = eigh(H)

    return x, eigenvalues[:n_states], eigenvectors[:, :n_states]
```

### 2.3 Métodos de Monte Carlo
```python
# Exemplo: Simulação Monte Carlo para Ising 2D
def ising_monte_carlo(lattice, T, steps):
    """
    Simulação Monte Carlo para modelo de Ising
    """
    beta = 1.0 / T
    energy_history = []

    for _ in range(steps):
        # Escolher sítio aleatório
        i, j = np.random.randint(0, lattice.shape[0], 2)

        # Calcular mudança de energia
        delta_E = 2 * J * lattice[i, j] * (
            lattice[(i+1)%L, j] + lattice[i, (j+1)%L] +
            lattice[(i-1)%L, j] + lattice[i, (j-1)%L]
        )

        # Aceitar ou rejeitar mudança
        if delta_E <= 0 or np.random.random() < np.exp(-beta * delta_E):
            lattice[i, j] *= -1

        # Calcular energia total
        energy = -J * np.sum(lattice * (
            np.roll(lattice, 1, axis=0) + np.roll(lattice, 1, axis=1)
        ))
        energy_history.append(energy)

    return lattice, energy_history
```

---

## 3. HIPÓTESES E RAMIFICAÇÕES PARA TESTE COMPUTACIONAL

### 3.1 Mecânica Quântica Avançada

**Hipótese Principal: Decoerência Quântica em Sistemas Macroscópicos**
- **Ramificação 1**: Modelar decoerência em superposições de estados macroscópicos
- **Ramificação 2**: Investigar transição clássico-quântico através de simulações numéricas
- **Ramificação 3**: Estudar efeitos de ambiente em computação quântica

```python
# Exemplo: Simulação de decoerência
def quantum_decoherence_simulation(rho_0, H_system, H_bath, coupling, times):
    """
    Simula decoerência quântica usando equação mestre
    rho_0: estado inicial do sistema
    H_system: Hamiltonian do sistema
    H_bath: Hamiltonian do banho
    coupling: acoplamento sistema-banho
    """
    # Implementar evolução não-unitária
    # Usar método de Lindblad ou abordagem numérica
    pass
```

### 3.2 Relatividade Geral Computacional

**Hipótese Principal: Ondas Gravitacionais em Espaços-Tempos Curvos**
- **Ramificação 1**: Simulação de colisões de buracos negros
- **Ramificação 2**: Efeitos de ondas gravitacionais em matéria interestelar
- **Ramificação 3**: Verificação numérica da conservação de energia-momento

```python
# Exemplo: Simulação de ondas gravitacionais
def gravitational_wave_simulation(mass1, mass2, eccentricity, time_span):
    """
    Simula ondas gravitacionais de sistema binário
    """
    # Usar post-Newtoniano ou relatividade numérica completa
    # Implementar método de BSSN ou similar
    pass
```

### 3.3 Cosmologia Computacional

**Hipótese Principal: Dinâmica da Energia Escura**
- **Ramificação 1**: Modelos dinâmicos de energia escura vs. constante cosmológica
- **Ramificação 2**: Efeitos de quinta força em formação de estruturas
- **Ramificação 3**: Simulações de inflação cósmica com diferentes potenciais

```python
# Exemplo: Simulação cosmológica com energia escura dinâmica
def cosmological_simulation(scale_factor_initial, matter_density, lambda_initial,
                           dark_energy_eos, time_steps):
    """
    Simula evolução cosmológica com energia escura dinâmica
    """
    # Resolver equações de Friedmann com w(a) variável
    # Implementar Runge-Kutta para sistema de EDOs
    pass
```

### 3.4 Teoria Quântica de Campos

**Hipótese Principal: Confinamento de Quarks em QCD**
- **Ramificação 1**: Simulação lattice QCD para espectro de hádrons
- **Ramificação 2**: Transições de fase QCD com matéria estranha
- **Ramificação 3**: Propriedades de plasma de quarks-glúons

```python
# Exemplo: Simulação lattice QCD simplificada
def lattice_qcd_simulation(lattice_size, beta, n_sweeps):
    """
    Simulação lattice QCD usando algoritmo híbrido Monte Carlo
    """
    # Implementar atualização local de campos de gauge
    # Calcular observables como energia livre e susceptibilidades
    pass
```

### 3.5 Física de Partículas Astrofísicas

**Hipótese Principal: Natureza da Matéria Escura**
- **Ramificação 1**: Detecção indireta através de anisotropias cósmicas
- **Ramificação 2**: Simulação de estruturas galácticas com matéria escura auto-interagente
- **Ramificação 3**: Assinaturas de matéria escura em ondas gravitacionais

```python
# Exemplo: Simulação de formação de estruturas com matéria escura
def structure_formation_simulation(dark_matter_model, initial_conditions,
                                 box_size, n_particles):
    """
    Simula formação de estruturas cosmológicas
    """
    # Implementar N-corpos com matéria escura
    # Incluir interações não-gravitacionais se aplicável
    pass
```

---

## 4. FERRAMENTAS E BIBLIOTECAS ESSENCIAIS

### 4.1 Python Scientific Stack
```python
# Configuração recomendada
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sympy as sym
from scipy.integrate import odeint, solve_ivp
from scipy.linalg import eigh, eigvals
from scipy.optimize import minimize, root
from scipy.fft import fft, ifft
```

### 4.2 Bibliotecas Especializadas
- **QuTiP**: Simulações quânticas
- **Astropy**: Astronomia e astrofísica
- **GWpy**: Ondas gravitacionais
- ** classy**: Cosmologia
- **PySCF**: Química quântica
- **FEniCS**: Elementos finitos

### 4.3 Computação de Alto Desempenho
- **NumPy/SciPy**: Computação paralela
- **Dask**: Computação distribuída
- **CuPy**: GPU computing
- **MPI4Py**: Computação paralela MPI

---

## 5. METODOLOGIA DE DESENVOLVIMENTO

### 5.1 Estrutura de Projeto
```
physics_simulation/
├── src/
│   ├── physics_models/
│   │   ├── quantum_mechanics.py
│   │   ├── relativity.py
│   │   └── cosmology.py
│   ├── numerical_methods/
│   │   ├── integrators.py
│   │   ├── monte_carlo.py
│   │   └── optimization.py
│   └── visualization/
│       ├── plotting.py
│       └── animation.py
├── tests/
├── examples/
├── docs/
└── requirements.txt
```

### 5.2 Boas Práticas de Desenvolvimento

1. **Documentação Extensiva**
```python
def solve_schrodinger_equation(potential_func, x_range, n_points,
                               boundary_conditions='infinite_well'):
    """
    Resolve numericamente a equação de Schrödinger unidimensional.

    Parameters:
    -----------
    potential_func : callable
        Função do potencial V(x)
    x_range : tuple
        (x_min, x_max) - intervalo espacial
    n_points : int
        Número de pontos da grade
    boundary_conditions : str
        Tipo de condições de contorno

    Returns:
    --------
    tuple: (energies, wavefunctions, x_grid)
        Autovalores, autofunções e grade espacial
    """
```

2. **Testes Unitários**
```python
def test_harmonic_oscillator_exact():
    """Testa solução analítica vs numérica para oscilador harmônico"""
    # Solução analítica conhecida
    exact_energies = [(n + 0.5) * hbar * omega for n in range(5)]

    # Solução numérica
    potential = lambda x: 0.5 * m * omega**2 * x**2
    energies_num = solve_schrodinger_equation(potential, (-5, 5), 1000)

    # Verificar precisão
    for exact, num in zip(exact_energies, energies_num):
        assert abs(exact - num) / exact < 1e-6
```

3. **Validação e Benchmarking**
```python
def benchmark_solver(solver_func, test_cases):
    """Benchmark de diferentes métodos numéricos"""
    results = {}
    for case_name, case_data in test_cases.items():
        start_time = time.time()
        solution = solver_func(**case_data)
        end_time = time.time()

        results[case_name] = {
            'solution': solution,
            'time': end_time - start_time,
            'accuracy': validate_solution(solution, case_data)
        }

    return results
```

### 5.3 Estratégias de Otimização

1. **Algoritmos Eficientes**
   - Pré-compilação de operações repetitivas
   - Uso de broadcasting em NumPy
   - Vetorização de loops

2. **Gerenciamento de Memória**
   - Uso eficiente de arrays
   - Liberação de memória não utilizada
   - Técnicas de streaming para grandes datasets

3. **Paralelização**
   - Computação paralela para simulações independentes
   - GPU acceleration para operações matriciais
   - Distribuição de cálculos em clusters

---

## 6. EXERCÍCIOS PRÁTICOS E PROJETOS

### 6.1 Projeto Iniciante: Oscilador Harmônico Quântico
**Objetivo**: Implementar solução numérica e comparar com solução analítica
**Dificuldade**: Baixa
**Tempo estimado**: 2-3 horas

### 6.2 Projeto Intermediário: Simulação de Sistema Planetário
**Objetivo**: Modelar sistema solar com N-corpos
**Dificuldade**: Média
**Tempo estimado**: 4-6 horas

### 6.3 Projeto Avançado: Modelo de Ising 2D
**Objetivo**: Implementar transição de fase e calcular expoentes críticos
**Dificuldade**: Alta
**Tempo estimado**: 8-12 horas

### 6.4 Projeto Especializado: Simulação Cosmológica
**Objetivo**: Modelar evolução do universo com energia escura
**Dificuldade**: Muito Alta
**Tempo estimado**: 20+ horas

---

## 7. RECURSOS ADICIONAIS PARA APRENDIZADO

### 7.1 Livros Recomendados
- "Computational Physics" - Landau & Páez
- "Numerical Recipes" - Press et al.
- "Introduction to Computational Physics" - Pang
- "Quantum Mechanics for Everyone" - Michel Le Bellac

### 7.2 Cursos Online
- Coursera: Computational Physics
- edX: Quantum Physics for Everyone
- MIT OpenCourseWare: Classical Mechanics
- Stanford Online: General Relativity

### 7.3 Comunidades e Fórums
- Physics Stack Exchange
- Computational Physics subreddit
- ResearchGate groups
- GitHub repositories de física computacional

---

## 8. MECÂNICA QUÂNTICA AVANÇADA

### 8.1 Teoria de Perturbação e Aproximações
```python
import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt

class QuantumPerturbationTheory:
    """
    Implementação de teoria de perturbação para sistemas quânticos
    """
    
    def __init__(self, H0, V, n_states=10):
        """
        H0: Hamiltoniano não perturbado
        V: Perturbação
        n_states: número de estados a considerar
        """
        self.H0 = H0
        self.V = V
        self.n_states = n_states
        
        # Resolver sistema não perturbado
        self.E0, self.psi0 = eigh(H0)
        self.E0 = self.E0[:n_states]
        self.psi0 = self.psi0[:, :n_states]
    
    def first_order_correction(self, state_index):
        """
        Correção de primeira ordem na energia
        E^(1)_n = <n|V|n>
        """
        psi_n = self.psi0[:, state_index]
        E1 = np.dot(psi_n.conj(), np.dot(self.V, psi_n))
        return E1.real
    
    def second_order_correction(self, state_index):
        """
        Correção de segunda ordem na energia
        E^(2)_n = Σ_{k≠n} |<k|V|n>|² / (E_n - E_k)
        """
        psi_n = self.psi0[:, state_index]
        E_n = self.E0[state_index]
        
        E2 = 0.0
        for k in range(self.n_states):
            if k != state_index:
                psi_k = self.psi0[:, k]
                E_k = self.E0[k]
                
                V_kn = np.dot(psi_k.conj(), np.dot(self.V, psi_n))
                E2 += np.abs(V_kn)**2 / (E_n - E_k)
        
        return E2.real
    
    def variational_method(self, trial_wavefunction, params):
        """
        Método variacional para aproximar estado fundamental
        """
        def energy_functional(p):
            psi_trial = trial_wavefunction(p)
            H_total = self.H0 + self.V
            
            numerator = np.dot(psi_trial.conj(), np.dot(H_total, psi_trial))
            denominator = np.dot(psi_trial.conj(), psi_trial)
            
            return (numerator / denominator).real
        
        from scipy.optimize import minimize
        result = minimize(energy_functional, params)
        
        return result.x, result.fun

# Exemplo de uso
n_points = 100
x = np.linspace(-5, 5, n_points)
omega = 1.0
m = 1.0
hbar = 1.0

# Hamiltoniano do oscilador harmônico
H0 = np.diag(0.5 * m * omega**2 * x**2)

# Perturbação anarmônica
lambda_param = 0.1
V = np.diag(lambda_param * x**4)

pert_theory = QuantumPerturbationTheory(H0, V, n_states=5)

print("\n=== TEORIA DE PERTURBAÇÃO ===")
for n in range(3):
    E0_n = pert_theory.E0[n]
    E1_n = pert_theory.first_order_correction(n)
    E2_n = pert_theory.second_order_correction(n)
    
    print(f"Estado n={n}:")
    print(f"  E⁽⁰⁾ = {E0_n:.4f}")
    print(f"  E⁽¹⁾ = {E1_n:.6f}")
    print(f"  E⁽²⁾ = {E2_n:.6f}")
```

**Conceitos Fundamentais:**
- Teoria de perturbação dependente e independente do tempo
- Método variacional
- Aproximação WKB
- Quantização de Bohr-Sommerfeld

### 8.2 Espalhamento Quântico
```python
class QuantumScattering:
    """
    Teoria de espalhamento quântico
    """
    
    def __init__(self, potential, energy, mass=1.0, hbar=1.0):
        self.V = potential
        self.E = energy
        self.m = mass
        self.hbar = hbar
        self.k = np.sqrt(2 * m * E) / hbar
    
    def born_approximation(self, q_array):
        """
        Aproximação de Born para amplitude de espalhamento
        f(θ) ≈ -(m/2πℏ²) ∫ V(r) e^(iq·r) d³r
        """
        f_q = np.zeros_like(q_array, dtype=complex)
        
        r_max = 20.0
        r_array = np.linspace(0, r_max, 1000)
        
        for i, q in enumerate(q_array):
            integrand = r_array**2 * self.V(r_array) * np.sin(q * r_array) / (q * r_array)
            f_q[i] = -2 * self.m / self.hbar**2 * np.trapz(integrand, r_array)
        
        return f_q
    
    def partial_wave_analysis(self, l_max=10):
        """
        Análise de ondas parciais
        """
        delta_l = np.zeros(l_max + 1)
        
        for l in range(l_max + 1):
            delta_l[l] = self._calculate_phase_shift(l)
        
        return delta_l
    
    def _calculate_phase_shift(self, l):
        """
        Calcula defasagem para momento angular l
        """
        r_max = 50.0
        n_points = 1000
        r = np.linspace(0.01, r_max, n_points)
        
        V_eff = self.V(r) + self.hbar**2 * l * (l + 1) / (2 * self.m * r**2)
        
        return 0.0
    
    def differential_cross_section(self, theta_array, delta_l):
        """
        Seção de choque diferencial
        dσ/dΩ = |f(θ)|²
        """
        f_theta = np.zeros_like(theta_array, dtype=complex)
        
        for l, delta in enumerate(delta_l):
            P_l = np.polynomial.legendre.Legendre.basis(l)(np.cos(theta_array))
            f_theta += (2*l + 1) * np.exp(1j * delta) * np.sin(delta) * P_l
        
        f_theta /= self.k
        
        return np.abs(f_theta)**2

V_yukawa = lambda r: -10.0 * np.exp(-r) / r
scattering = QuantumScattering(V_yukawa, energy=5.0)

q_array = np.linspace(0.1, 5.0, 50)
f_born = scattering.born_approximation(q_array)

print(f"\nAmplitude de espalhamento (Born): {np.abs(f_born[0]):.4f}")
```

**Conceitos Críticos:**
- Aproximação de Born
- Análise de ondas parciais
- Defasagens (phase shifts)
- Seção de choque diferencial e total
- Matriz S e unitariedade

---

## 9. TEORIA QUÂNTICA DE CAMPOS

### 9.1 Quantização Canônica
```python
class QuantumFieldTheory:
    """
    Fundamentos de teoria quântica de campos
    """
    
    def __init__(self, lattice_size, lattice_spacing):
        self.L = lattice_size
        self.a = lattice_spacing
        self.V = (self.L * self.a)**3
    
    def scalar_field_propagator(self, x, y, mass):
        """
        Propagador de Feynman para campo escalar
        G(x-y) = ∫ d⁴k/(2π)⁴ e^(ik·(x-y))/(k² - m² + iε)
        """
        r = np.linalg.norm(x - y)
        
        if r == 0:
            return np.inf
        
        propagator = np.exp(-mass * r) / (4 * np.pi * r)
        
        return propagator
    
    def feynman_diagram_amplitude(self, diagram_type, momenta, coupling):
        """
        Calcula amplitude de diagrama de Feynman
        """
        if diagram_type == 'tree_level_scattering':
            s = self._mandelstam_s(momenta[0], momenta[1])
            amplitude = coupling**2 / s
            
        elif diagram_type == 'one_loop_correction':
            amplitude = self._one_loop_integral(momenta, coupling)
        
        return amplitude
    
    def _mandelstam_s(self, p1, p2):
        """
        Variável de Mandelstam s = (p1 + p2)²
        """
        return np.dot(p1 + p2, p1 + p2)
    
    def _one_loop_integral(self, external_momenta, coupling):
        """
        Integral de loop (regularizada dimensionalmente)
        """
        return coupling**4 / (16 * np.pi**2)
    
    def renormalization_group_flow(self, coupling_initial, scale_initial, 
                                   scale_final, beta_function):
        """
        Evolução do acoplamento via grupo de renormalização
        dg/d(log μ) = β(g)
        """
        from scipy.integrate import odeint
        
        def rg_equation(g, log_mu):
            return beta_function(g)
        
        log_mu_array = np.linspace(np.log(scale_initial), 
                                   np.log(scale_final), 100)
        
        g_array = odeint(rg_equation, coupling_initial, log_mu_array)
        
        return np.exp(log_mu_array), g_array.flatten()

qft = QuantumFieldTheory(lattice_size=10, lattice_spacing=0.1)

x1 = np.array([0, 0, 0, 0])
x2 = np.array([1, 0, 0, 0])
prop = qft.scalar_field_propagator(x1, x2, mass=1.0)
print(f"\nPropagador G(x-y): {prop:.6f}")

def beta_qed(alpha):
    return alpha**2 / (3 * np.pi)

mu_array, alpha_array = qft.renormalization_group_flow(
    coupling_initial=1/137,
    scale_initial=0.511,
    scale_final=91.2e3,
    beta_function=beta_qed
)

print(f"α(m_e) = {alpha_array[0]:.6f}")
print(f"α(M_Z) = {alpha_array[-1]:.6f}")
```

**Conceitos Fundamentais:**
- Quantização canônica de campos
- Propagadores de Feynman
- Diagramas de Feynman
- Grupo de renormalização
- Liberdade assintótica

---

## 10. RELATIVIDADE GERAL COMPUTACIONAL

### 10.1 Geometria do Espaço-Tempo
```python
import sympy as sp
from sympy import symbols, Matrix, simplify, diff

class GeneralRelativity:
    """
    Cálculos em relatividade geral
    """
    
    def __init__(self, coordinates):
        self.coords = coordinates
        self.dim = len(coordinates)
    
    def metric_tensor(self, metric_components):
        """
        Define tensor métrico g_μν
        """
        self.g = Matrix(metric_components)
        self.g_inv = self.g.inv()
        
        return self.g
    
    def christoffel_symbols(self):
        """
        Calcula símbolos de Christoffel
        Γ^λ_μν = (1/2) g^λσ (∂_μ g_νσ + ∂_ν g_μσ - ∂_σ g_μν)
        """
        Gamma = [[[0 for _ in range(self.dim)] 
                  for _ in range(self.dim)] 
                 for _ in range(self.dim)]
        
        for lam in range(self.dim):
            for mu in range(self.dim):
                for nu in range(self.dim):
                    term = 0
                    for sigma in range(self.dim):
                        term += self.g_inv[lam, sigma] * (
                            diff(self.g[nu, sigma], self.coords[mu]) +
                            diff(self.g[mu, sigma], self.coords[nu]) -
                            diff(self.g[mu, nu], self.coords[sigma])
                        )
                    Gamma[lam][mu][nu] = simplify(term / 2)
        
        return Gamma
    
    def riemann_tensor(self, Gamma):
        """
        Tensor de Riemann
        R^ρ_σμν = ∂_μ Γ^ρ_νσ - ∂_ν Γ^ρ_μσ + Γ^ρ_μλ Γ^λ_νσ - Γ^ρ_νλ Γ^λ_μσ
        """
        R = [[[[0 for _ in range(self.dim)] 
               for _ in range(self.dim)] 
              for _ in range(self.dim)] 
             for _ in range(self.dim)]
        
        for rho in range(self.dim):
            for sigma in range(self.dim):
                for mu in range(self.dim):
                    for nu in range(self.dim):
                        term = (diff(Gamma[rho][nu][sigma], self.coords[mu]) -
                               diff(Gamma[rho][mu][sigma], self.coords[nu]))
                        
                        for lam in range(self.dim):
                            term += (Gamma[rho][mu][lam] * Gamma[lam][nu][sigma] -
                                   Gamma[rho][nu][lam] * Gamma[lam][mu][sigma])
                        
                        R[rho][sigma][mu][nu] = simplify(term)
        
        return R
    
    def ricci_tensor(self, R):
        """
        Tensor de Ricci: R_μν = R^λ_μλν
        """
        Ric = Matrix.zeros(self.dim, self.dim)
        
        for mu in range(self.dim):
            for nu in range(self.dim):
                for lam in range(self.dim):
                    Ric[mu, nu] += R[lam][mu][lam][nu]
        
        return Ric
    
    def ricci_scalar(self, Ric):
        """
        Escalar de Ricci: R = g^μν R_μν
        """
        R_scalar = 0
        for mu in range(self.dim):
            for nu in range(self.dim):
                R_scalar += self.g_inv[mu, nu] * Ric[mu, nu]
        
        return simplify(R_scalar)
    
    def einstein_tensor(self, Ric, R_scalar):
        """
        Tensor de Einstein: G_μν = R_μν - (1/2) g_μν R
        """
        G = Matrix.zeros(self.dim, self.dim)
        
        for mu in range(self.dim):
            for nu in range(self.dim):
                G[mu, nu] = Ric[mu, nu] - self.g[mu, nu] * R_scalar / 2
        
        return G

# Exemplo: Métrica de Schwarzschild
t, r, theta, phi = symbols('t r theta phi', real=True)
M, c, G_const = symbols('M c G', positive=True, real=True)

coords = [t, r, theta, phi]
gr = GeneralRelativity(coords)

# Métrica de Schwarzschild
rs = 2 * G_const * M / c**2  # Raio de Schwarzschild

g_schwarzschild = Matrix([
    [-(1 - rs/r), 0, 0, 0],
    [0, 1/(1 - rs/r), 0, 0],
    [0, 0, r**2, 0],
    [0, 0, 0, r**2 * sp.sin(theta)**2]
])

gr.metric_tensor(g_schwarzschild)
print("\n=== RELATIVIDADE GERAL ===")
print("Métrica de Schwarzschild definida")

# Calcular símbolos de Christoffel (computacionalmente intensivo)
# Gamma = gr.christoffel_symbols()
```

**Conceitos Fundamentais:**
- Tensor métrico e geometria Riemanniana
- Símbolos de Christoffel
- Tensor de Riemann e curvatura
- Equações de Einstein
- Soluções exatas (Schwarzschild, Kerr, FRW)

### 10.2 Ondas Gravitacionais
```python
class GravitationalWaves:
    """
    Simulação de ondas gravitacionais
    """
    
    def __init__(self, mass1, mass2, distance):
        self.m1 = mass1
        self.m2 = mass2
        self.d = distance
        
        self.M = mass1 + mass2  # Massa total
        self.mu = mass1 * mass2 / self.M  # Massa reduzida
        self.eta = self.mu / self.M  # Razão de massa simétrica
    
    def orbital_frequency(self, separation):
        """
        Frequência orbital Kepleriana
        """
        G = 6.674e-11  # m³ kg⁻¹ s⁻²
        omega = np.sqrt(G * self.M / separation**3)
        return omega
    
    def gravitational_wave_strain(self, time, separation):
        """
        Amplitude da onda gravitacional (aproximação quadrupolar)
        h ≈ (4G/c⁴) (μ/r) (v/c)²
        """
        G = 6.674e-11
        c = 3e8
        
        omega = self.orbital_frequency(separation)
        v = omega * separation
        
        h = (4 * G / c**4) * (self.mu / self.d) * (v / c)**2
        
        # Polarizações
        h_plus = h * np.cos(2 * omega * time)
        h_cross = h * np.sin(2 * omega * time)
        
        return h_plus, h_cross
    
    def inspiral_evolution(self, initial_separation, time_span):
        """
        Evolução do inspiral devido à radiação gravitacional
        """
        from scipy.integrate import odeint
        
        G = 6.674e-11
        c = 3e8
        
        def dr_dt(r, t):
            # Taxa de perda de energia orbital
            omega = self.orbital_frequency(r)
            dE_dt = -(32/5) * (G**4 / c**5) * (self.m1 * self.m2)**2 * self.M / r**5
            
            # dr/dt da conservação de energia
            return 2 * dE_dt / (G * self.M * self.mu / r**2)
        
        t_array = np.linspace(0, time_span, 1000)
        r_array = odeint(dr_dt, initial_separation, t_array)
        
        return t_array, r_array.flatten()
    
    def merger_ringdown(self, final_mass, final_spin):
        """
        Fase de merger e ringdown
        """
        G = 6.674e-11
        c = 3e8
        
        # Frequência de quasi-normal mode
        M_f = final_mass
        a_f = final_spin
        
        # Aproximação para modo fundamental
        omega_qnm = c**3 / (G * M_f) * (1 - 0.63 * (1 - a_f)**0.3)
        tau = G * M_f / c**3 * (1 + 0.7 * (1 - a_f)**(-0.9))
        
        return omega_qnm, tau

# Exemplo: Merger de buracos negros
M_sun = 1.989e30  # kg
gw = GravitationalWaves(
    mass1=30 * M_sun,
    mass2=30 * M_sun,
    distance=1e9 * 9.461e15  # 1 Gpc em metros
)

separation = 1000e3  # 1000 km
t = np.linspace(0, 1, 1000)
h_plus, h_cross = gw.gravitational_wave_strain(t, separation)

print(f"\nAmplitude da onda gravitacional: h ~ {np.max(np.abs(h_plus)):.2e}")

t_inspiral, r_inspiral = gw.inspiral_evolution(
    initial_separation=1000e3,
    time_span=10.0
)
print(f"Separação final após inspiral: {r_inspiral[-1]/1000:.1f} km")
```

**Conceitos Críticos:**
- Aproximação pós-Newtoniana
- Radiação quadrupolar
- Inspiral, merger e ringdown
- Modos quasi-normais
- Detecção de ondas gravitacionais

---

## 11. COSMOLOGIA COMPUTACIONAL

### 11.1 Modelos Cosmológicos
```python
class Cosmology:
    """
    Modelos cosmológicos e evolução do universo
    """
    
    def __init__(self, H0=70, Omega_m=0.3, Omega_Lambda=0.7, Omega_r=0.0):
        """
        H0: Constante de Hubble (km/s/Mpc)
        Omega_m: Densidade de matéria
        Omega_Lambda: Densidade de energia escura
        Omega_r: Densidade de radiação
        """
        self.H0 = H0
        self.Omega_m = Omega_m
        self.Omega_Lambda = Omega_Lambda
        self.Omega_r = Omega_r
        self.Omega_k = 1 - (Omega_m + Omega_Lambda + Omega_r)
    
    def hubble_parameter(self, a):
        """
        Parâmetro de Hubble H(a) em função do fator de escala
        H(a) = H0 √[Ω_m a⁻³ + Ω_r a⁻⁴ + Ω_Λ + Ω_k a⁻²]
        """
        H_a = self.H0 * np.sqrt(
            self.Omega_m * a**(-3) +
            self.Omega_r * a**(-4) +
            self.Omega_Lambda +
            self.Omega_k * a**(-2)
        )
        return H_a
    
    def friedmann_equations(self, a, t):
        """
        Equações de Friedmann
        da/dt = a H(a)
        """
        H_a = self.hubble_parameter(a)
        return a * H_a / (3.086e19)  # Converter km/s/Mpc para 1/s
    
    def cosmic_evolution(self, a_initial=1e-10, t_final=14e9):
        """
        Evolução do fator de escala com o tempo
        """
        from scipy.integrate import odeint
        
        t_array = np.linspace(0, t_final * 365.25 * 24 * 3600, 1000)
        a_array = odeint(self.friedmann_equations, a_initial, t_array)
        
        return t_array / (365.25 * 24 * 3600 * 1e9), a_array.flatten()
    
    def comoving_distance(self, z):
        """
        Distância comóvel para redshift z
        """
        from scipy.integrate import quad
        
        def integrand(z_prime):
            a = 1 / (1 + z_prime)
            return 1 / self.hubble_parameter(a)
        
        c = 3e5  # km/s
        distance, _ = quad(integrand, 0, z)
        
        return c * distance
    
    def luminosity_distance(self, z):
        """
        Distância de luminosidade
        """
        d_c = self.comoving_distance(z)
        return (1 + z) * d_c
    
    def angular_diameter_distance(self, z):
        """
        Distância de diâmetro angular
        """
        d_c = self.comoving_distance(z)
        return d_c / (1 + z)
    
    def age_of_universe(self, z=0):
        """
        Idade do universo no redshift z
        """
        from scipy.integrate import quad
        
        def integrand(z_prime):
            a = 1 / (1 + z_prime)
            return 1 / ((1 + z_prime) * self.hubble_parameter(a))
        
        age, _ = quad(integrand, z, np.inf)
        
        # Converter para anos
        H0_SI = self.H0 * 1000 / (3.086e22)  # 1/s
        age_years = age / H0_SI / (365.25 * 24 * 3600)
        
        return age_years

# Exemplo de uso
cosmo = Cosmology(H0=70, Omega_m=0.3, Omega_Lambda=0.7)

print("\n=== COSMOLOGIA ===")
print(f"Idade do universo: {cosmo.age_of_universe():.2f} bilhões de anos")

z_array = np.array([0.5, 1.0, 2.0, 5.0])
for z in z_array:
    d_L = cosmo.luminosity_distance(z)
    print(f"z={z}: d_L = {d_L:.0f} Mpc")

# Evolução do fator de escala
t_array, a_array = cosmo.cosmic_evolution()
print(f"\nFator de escala atual: a(t_0) = {a_array[-1]:.2f}")
```

**Conceitos Fundamentais:**
- Equações de Friedmann
- Fator de escala e redshift
- Distâncias cosmológicas
- Idade do universo
- Modelos ΛCDM

### 11.2 Formação de Estruturas
```python
class StructureFormation:
    """
    Simulação de formação de estruturas cosmológicas
    """
    
    def __init__(self, box_size, n_particles):
        self.L = box_size
        self.N = n_particles
        self.positions = None
        self.velocities = None
        self.masses = None
    
    def initialize_particles(self, power_spectrum_func):
        """
        Inicializa partículas com espectro de potência dado
        """
        # Posições em grade regular
        n_per_dim = int(np.cbrt(self.N))
        x = np.linspace(0, self.L, n_per_dim)
        X, Y, Z = np.meshgrid(x, x, x)
        
        self.positions = np.column_stack([
            X.flatten(),
            Y.flatten(),
            Z.flatten()
        ])[:self.N]
        
        # Perturbações de densidade
        k_modes = np.fft.fftfreq(n_per_dim, d=self.L/n_per_dim) * 2 * np.pi
        kx, ky, kz = np.meshgrid(k_modes, k_modes, k_modes)
        k = np.sqrt(kx**2 + ky**2 + kz**2)
        
        # Espectro de potência
        P_k = power_spectrum_func(k)
        
        # Gerar campo de densidade em espaço de Fourier
        delta_k = np.random.normal(0, np.sqrt(P_k), k.shape) + \
                  1j * np.random.normal(0, np.sqrt(P_k), k.shape)
        
        # Transformada inversa
        delta_x = np.fft.ifftn(delta_k).real
        
        # Deslocamentos Zel'dovich
        displacement = self._zeldovich_approximation(delta_x)
        
        self.positions += displacement[:self.N]
        self.masses = np.ones(self.N)
        
        return self.positions
    
    def _zeldovich_approximation(self, delta_field):
        """
        Aproximação de Zel'dovich para deslocamentos
        """
        # Calcular gradiente do potencial gravitacional
        grad_x = np.gradient(delta_field, axis=0)
        grad_y = np.gradient(delta_field, axis=1)
        grad_z = np.gradient(delta_field, axis=2)
        
        displacement = np.column_stack([
            grad_x.flatten(),
            grad_y.flatten(),
            grad_z.flatten()
        ])
        
        return displacement
    
    def n_body_simulation(self, n_steps, dt, softening=0.1):
        """
        Simulação N-corpos para evolução gravitacional
        """
        G = 1.0  # Unidades naturais
        
        self.velocities = np.zeros_like(self.positions)
        trajectory = [self.positions.copy()]
        
        for step in range(n_steps):
            # Calcular forças gravitacionais
            forces = np.zeros_like(self.positions)
            
            for i in range(self.N):
                r_vec = self.positions - self.positions[i]
                r_mag = np.sqrt(np.sum(r_vec**2, axis=1) + softening**2)
                
                # Evitar auto-interação
                r_mag[i] = np.inf
                
                force_mag = G * self.masses[i] * self.masses / r_mag**3
                forces[i] = np.sum(force_mag[:, np.newaxis] * r_vec, axis=0)
            
            # Integração leapfrog
            self.velocities += 0.5 * forces * dt / self.masses[:, np.newaxis]
            self.positions += self.velocities * dt
            
            # Condições periódicas de contorno
            self.positions = self.positions % self.L
            
            self.velocities += 0.5 * forces * dt / self.masses[:, np.newaxis]
            
            if step % 10 == 0:
                trajectory.append(self.positions.copy())
        
        return np.array(trajectory)
    
    def halo_finding(self, linking_length=0.2):
        """
        Algoritmo Friends-of-Friends para identificar halos
        """
        from scipy.spatial import cKDTree
        
        tree = cKDTree(self.positions, boxsize=self.L)
        
        # Encontrar vizinhos dentro do linking length
        neighbors = tree.query_ball_tree(tree, linking_length)
        
        # Agrupar partículas conectadas
        halos = []
        visited = set()
        
        for i in range(self.N):
            if i in visited:
                continue
            
            halo = set([i])
            to_visit = set(neighbors[i])
            
            while to_visit:
                j = to_visit.pop()
                if j in visited:
                    continue
                
                visited.add(j)
                halo.add(j)
                to_visit.update(neighbors[j])
            
            if len(halo) > 10:  # Mínimo de partículas
                halos.append(list(halo))
        
        return halos

# Exemplo
def power_spectrum_cdm(k):
    """Espectro de potência CDM simplificado"""
    n_s = 0.96
    return k**n_s * np.exp(-k**2)

structure = StructureFormation(box_size=100, n_particles=1000)
positions = structure.initialize_particles(power_spectrum_cdm)

print(f"\n{len(positions)} partículas inicializadas")
print(f"Volume da caixa: {structure.L**3:.0f} Mpc³")
```

**Conceitos Críticos:**
- Espectro de potência
- Aproximação de Zel'dovich
- Simulações N-corpos
- Friends-of-Friends halo finding
- Evolução não-linear de estruturas

---

## 12. FÍSICA ESTATÍSTICA E MECÂNICA ESTATÍSTICA

### 12.1 Ensemble Estatísticos
```python
class StatisticalMechanics:
    """
    Mecânica estatística e termodinâmica
    """
    
    def __init__(self, temperature, n_particles):
        self.T = temperature
        self.N = n_particles
        self.kB = 1.380649e-23  # J/K
        self.beta = 1 / (self.kB * temperature)
    
    def partition_function_ideal_gas(self, volume):
        """
        Função de partição para gás ideal clássico
        Z = (V/λ³)^N / N!
        """
        m = 1.67e-27  # massa do próton (kg)
        h = 6.626e-34  # constante de Planck
        
        # Comprimento de onda térmico de de Broglie
        lambda_th = h / np.sqrt(2 * np.pi * m * self.kB * self.T)
        
        # Aproximação de Stirling para N!
        log_Z = self.N * (np.log(volume) - 3 * np.log(lambda_th)) - \
                self.N * (np.log(self.N) - 1)
        
        return np.exp(log_Z)
    
    def helmholtz_free_energy(self, Z):
        """
        Energia livre de Helmholtz
        F = -kB T ln(Z)
        """
        return -self.kB * self.T * np.log(Z)
    
    def entropy(self, Z, E):
        """
        Entropia S = kB ln(Ω)
        """
        F = self.helmholtz_free_energy(Z)
        S = (E - F) / self.T
        return S
    
    def maxwell_boltzmann_distribution(self, v_array):
        """
        Distribuição de Maxwell-Boltzmann para velocidades
        """
        m = 1.67e-27
        
        normalization = (m / (2 * np.pi * self.kB * self.T))**(3/2)
        
        f_v = 4 * np.pi * v_array**2 * normalization * \
              np.exp(-m * v_array**2 / (2 * self.kB * self.T))
        
        return f_v
    
    def bose_einstein_distribution(self, energy, mu=0):
        """
        Distribuição de Bose-Einstein
        n(E) = 1 / (exp[(E-μ)/kBT] - 1)
        """
        return 1 / (np.exp((energy - mu) * self.beta) - 1)
    
    def fermi_dirac_distribution(self, energy, mu):
        """
        Distribuição de Fermi-Dirac
        n(E) = 1 / (exp[(E-μ)/kBT] + 1)
        """
        return 1 / (np.exp((energy - mu) * self.beta) + 1)
    
    def planck_distribution(self, frequency):
        """
        Distribuição de Planck para radiação de corpo negro
        """
        h = 6.626e-34
        c = 3e8
        
        energy_density = (8 * np.pi * h * frequency**3 / c**3) / \
                        (np.exp(h * frequency * self.beta) - 1)
        
        return energy_density

# Exemplo
stat_mech = StatisticalMechanics(temperature=300, n_particles=1e23)

# Distribuição de velocidades
v_array = np.linspace(0, 2000, 1000)
f_v = stat_mech.maxwell_boltzmann_distribution(v_array)

v_mean = np.trapz(v_array * f_v, v_array)
v_rms = np.sqrt(np.trapz(v_array**2 * f_v, v_array))

print("\n=== MECÂNICA ESTATÍSTICA ===")
print(f"Velocidade média: {v_mean:.1f} m/s")
print(f"Velocidade RMS: {v_rms:.1f} m/s")

# Distribuições quânticas
E_array = np.linspace(0, 10 * stat_mech.kB * stat_mech.T, 100)
mu_fermi = 5 * stat_mech.kB * stat_mech.T

n_BE = stat_mech.bose_einstein_distribution(E_array)
n_FD = stat_mech.fermi_dirac_distribution(E_array, mu_fermi)

print(f"Ocupação Bose (E=0): {n_BE[0]:.2f}")
print(f"Ocupação Fermi (E=μ): {n_FD[50]:.2f}")
```

**Conceitos Fundamentais:**
- Ensembles microcanônico, canônico e grande canônico
- Função de partição
- Distribuições de Maxwell-Boltzmann, Bose-Einstein e Fermi-Dirac
- Termodinâmica estatística
- Transições de fase

### 12.2 Transições de Fase e Fenômenos Críticos
```python
class PhaseTransitions:
    """
    Estudo de transições de fase e fenômenos críticos
    """
    
    def __init__(self, lattice_size):
        self.L = lattice_size
        self.lattice = np.random.choice([-1, 1], size=(lattice_size, lattice_size))
    
    def ising_model_2d(self, T, J=1.0, n_steps=10000):
        """
        Modelo de Ising 2D com algoritmo de Metropolis
        """
        beta = 1.0 / T
        magnetization = []
        energy = []
        
        for step in range(n_steps):
            # Escolher sítio aleatório
            i, j = np.random.randint(0, self.L, 2)
            
            # Calcular mudança de energia
            neighbors_sum = (
                self.lattice[(i+1) % self.L, j] +
                self.lattice[(i-1) % self.L, j] +
                self.lattice[i, (j+1) % self.L] +
                self.lattice[i, (j-1) % self.L]
            )
            
            delta_E = 2 * J * self.lattice[i, j] * neighbors_sum
            
            # Aceitar ou rejeitar flip
            if delta_E <= 0 or np.random.random() < np.exp(-beta * delta_E):
                self.lattice[i, j] *= -1
            
            # Medir observáveis
            if step > n_steps // 2:  # Termalização
                M = np.sum(self.lattice) / self.L**2
                E = -J * np.sum(
                    self.lattice * (
                        np.roll(self.lattice, 1, axis=0) +
                        np.roll(self.lattice, 1, axis=1)
                    )
                ) / self.L**2
                
                magnetization.append(abs(M))
                energy.append(E)
        
        return {
            'magnetization': np.mean(magnetization),
            'mag_susceptibility': self.L**2 * np.var(magnetization),
            'energy': np.mean(energy),
            'specific_heat': self.L**2 * np.var(energy) / T**2
        }
    
    def critical_exponents(self, T_array, T_c=2.269):
        """
        Determina expoentes críticos próximo à temperatura crítica
        """
        results = []
        
        for T in T_array:
            result = self.ising_model_2d(T)
            results.append(result)
        
        # Extrair expoentes
        mag_array = np.array([r['magnetization'] for r in results])
        chi_array = np.array([r['mag_susceptibility'] for r in results])
        
        # β: M ~ (T_c - T)^β
        # γ: χ ~ |T - T_c|^(-γ)
        
        return results

# Exemplo
phase = PhaseTransitions(lattice_size=50)

T_array = np.linspace(1.5, 3.5, 10)
print("\n=== TRANSIÇÕES DE FASE ===")
print("Temperatura | Magnetização | Susceptibilidade")
print("-" * 50)

for T in [2.0, 2.269, 2.5]:
    result = phase.ising_model_2d(T, n_steps=5000)
    print(f"{T:.3f}      | {result['magnetization']:.4f}      | {result['mag_susceptibility']:.2f}")
```

**Conceitos Críticos:**
- Modelo de Ising
- Temperatura crítica
- Expoentes críticos
- Universalidade
- Grupo de renormalização

---

## 13. FÍSICA DE PARTÍCULAS E MODELO PADRÃO

### 13.1 Cinemática Relativística
```python
class ParticlePhysics:
    """
    Física de partículas e cinemática relativística
    """
    
    def __init__(self):
        self.c = 299792458  # m/s
        self.hbar = 1.054571817e-34  # J·s
        self.GeV_to_kg = 1.78266192e-27  # kg/GeV
    
    def lorentz_factor(self, velocity):
        """
        Fator de Lorentz γ = 1/√(1 - v²/c²)
        """
        beta = velocity / self.c
        gamma = 1 / np.sqrt(1 - beta**2)
        return gamma
    
    def four_momentum(self, mass, velocity):
        """
        Quadrimomento (E/c, px, py, pz)
        """
        gamma = self.lorentz_factor(np.linalg.norm(velocity))
        
        E = gamma * mass * self.c**2
        p = gamma * mass * velocity
        
        return np.array([E/self.c, p[0], p[1], p[2]])
    
    def invariant_mass(self, four_momenta):
        """
        Massa invariante de um sistema de partículas
        M² = (ΣE)²/c² - (Σp)²
        """
        total_p4 = np.sum(four_momenta, axis=0)
        
        E_total = total_p4[0] * self.c
        p_total = total_p4[1:]
        
        M_squared = (E_total/self.c)**2 - np.dot(p_total, p_total)
        
        return np.sqrt(max(0, M_squared))
    
    def decay_kinematics_2body(self, M_parent, m1, m2):
        """
        Cinemática de decaimento em 2 corpos no referencial de repouso
        """
        # Energia das partículas filhas
        E1 = (M_parent**2 + m1**2 - m2**2) / (2 * M_parent)
        E2 = (M_parent**2 + m2**2 - m1**2) / (2 * M_parent)
        
        # Momento (mesma magnitude, direções opostas)
        p_mag = np.sqrt(E1**2 - m1**2)
        
        return {
            'E1': E1,
            'E2': E2,
            'p_magnitude': p_mag
        }
    
    def cross_section_rutherford(self, theta, Z1, Z2, energy):
        """
        Seção de choque de Rutherford para espalhamento Coulombiano
        """
        alpha = 1/137  # Constante de estrutura fina
        
        # Fator cinemático
        s = np.sin(theta / 2)
        
        # Seção de choque diferencial
        dsigma_dOmega = (Z1 * Z2 * alpha * self.hbar * self.c / (4 * energy))**2 / s**4
        
        return dsigma_dOmega
    
    def breit_wigner(self, energy, mass, width):
        """
        Distribuição de Breit-Wigner para ressonâncias
        """
        return (width / (2 * np.pi)) / ((energy - mass)**2 + (width/2)**2)

class StandardModel:
    """
    Modelo Padrão da física de partículas
    """
    
    def __init__(self):
        # Massas das partículas (GeV/c²)
        self.particle_masses = {
            'electron': 0.000511,
            'muon': 0.106,
            'tau': 1.777,
            'up': 0.0022,
            'down': 0.0047,
            'charm': 1.27,
            'strange': 0.095,
            'top': 173.0,
            'bottom': 4.18,
            'W': 80.4,
            'Z': 91.2,
            'Higgs': 125.1
        }
        
        # Constantes de acoplamento
        self.alpha_em = 1/137  # Eletromagnética
        self.alpha_s = 0.118  # Forte (em M_Z)
        self.sin2_theta_w = 0.231  # Ângulo de Weinberg
    
    def yukawa_coupling(self, particle):
        """
        Acoplamento de Yukawa com o Higgs
        y = √2 m / v
        """
        v_higgs = 246  # GeV (VEV do Higgs)
        mass = self.particle_masses.get(particle, 0)
        
        return np.sqrt(2) * mass / v_higgs
    
    def running_coupling_qcd(self, scale):
        """
        Acoplamento forte em função da escala de energia
        α_s(μ) = α_s(M_Z) / (1 + α_s(M_Z) β₀ ln(μ/M_Z))
        """
        M_Z = 91.2  # GeV
        n_f = 5  # Número de sabores ativos
        
        # Função beta de 1-loop
        beta_0 = (33 - 2 * n_f) / (12 * np.pi)
        
        alpha_s_mu = self.alpha_s / (
            1 + self.alpha_s * beta_0 * np.log(scale / M_Z)
        )
        
        return alpha_s_mu
    
    def higgs_production_cross_section(self, sqrt_s):
        """
        Seção de choque de produção do Higgs (gluon fusion)
        """
        # Aproximação simplificada
        m_H = self.particle_masses['Higgs']
        m_t = self.particle_masses['top']
        
        # Acoplamento efetivo
        y_t = self.yukawa_coupling('top')
        alpha_s = self.running_coupling_qcd(m_H)
        
        # Seção de choque (ordem de grandeza)
        sigma = (alpha_s**2 * y_t**2) / (576 * np.pi * sqrt_s**2)
        
        return sigma * 1e9  # pb

# Exemplo de uso
pp = ParticlePhysics()

# Decaimento Z → e⁺e⁻
M_Z = 91.2 * pp.GeV_to_kg
m_e = 0.000511 * pp.GeV_to_kg

decay = pp.decay_kinematics_2body(M_Z, m_e, m_e)
print("\n=== FÍSICA DE PARTÍCULAS ===")
print(f"Decaimento Z → e⁺e⁻:")
print(f"  Energia do elétron: {decay['E1']/pp.GeV_to_kg:.2f} GeV")
print(f"  Momento: {decay['p_magnitude']/(pp.GeV_to_kg * pp.c):.2f} GeV/c")

# Modelo Padrão
sm = StandardModel()

print(f"\nAcoplamento de Yukawa do top: {sm.yukawa_coupling('top'):.4f}")
print(f"α_s(M_Z) = {sm.alpha_s:.3f}")
print(f"α_s(1 TeV) = {sm.running_coupling_qcd(1000):.3f}")

# Produção do Higgs
sigma_H = sm.higgs_production_cross_section(13000)  # LHC 13 TeV
print(f"\nSeção de choque gg→H (13 TeV): {sigma_H:.1f} pb")
```

**Conceitos Fundamentais:**
- Cinemática relativística
- Quadrimomento e massa invariante
- Modelo Padrão
- Acoplamentos de gauge
- Running coupling e grupo de renormalização
- Seções de choque

### 13.2 Detectores de Partículas
```python
class ParticleDetector:
    """
    Simulação de detectores de partículas
    """
    
    def __init__(self, detector_type='calorimeter'):
        self.type = detector_type
        self.resolution = None
    
    def energy_resolution(self, energy, detector_params):
        """
        Resolução de energia do detector
        σ(E)/E = a/√E ⊕ b ⊕ c/E
        """
        a = detector_params.get('stochastic', 0.1)  # Termo estocástico
        b = detector_params.get('constant', 0.01)   # Termo constante
        c = detector_params.get('noise', 0.5)       # Termo de ruído
        
        sigma_E = energy * np.sqrt(
            (a / np.sqrt(energy))**2 + b**2 + (c / energy)**2
        )
        
        return sigma_E
    
    def track_reconstruction(self, hits, magnetic_field):
        """
        Reconstrução de trajetória em campo magnético
        """
        # Ajuste de hélice aos hits
        # Simplificado: ajuste circular em 2D
        
        if len(hits) < 3:
            return None
        
        # Converter hits para array
        points = np.array(hits)
        
        # Ajuste de círculo (método dos mínimos quadrados)
        x = points[:, 0]
        y = points[:, 1]
        
        # Sistema de equações
        A = np.column_stack([x, y, np.ones_like(x)])
        b = x**2 + y**2
        
        # Resolver
        params = np.linalg.lstsq(A, b, rcond=None)[0]
        
        # Centro e raio do círculo
        xc = params[0] / 2
        yc = params[1] / 2
        R = np.sqrt(params[2] + xc**2 + yc**2)
        
        # Momento transverso: pT = 0.3 * B * R (GeV/c para B em Tesla, R em metros)
        pT = 0.3 * magnetic_field * R
        
        return {
            'center': (xc, yc),
            'radius': R,
            'pT': pT
        }
    
    def particle_identification(self, dE_dx, momentum):
        """
        Identificação de partículas via dE/dx (fórmula de Bethe-Bloch)
        """
        # Parâmetros
        Z = 1  # Carga da partícula
        z = 1  # Carga do meio
        A = 12  # Massa atômica do meio
        I = 78e-9  # Potencial de ionização (GeV)
        
        # Velocidade
        beta = momentum / np.sqrt(momentum**2 + 0.938**2)  # Assumindo próton
        gamma = 1 / np.sqrt(1 - beta**2)
        
        # Bethe-Bloch
        K = 0.307075  # MeV cm²/mol
        dE_dx_calc = K * z**2 * Z / (A * beta**2) * (
            0.5 * np.log(2 * 0.511e-3 * beta**2 * gamma**2 / I) - beta**2
        )
        
        # Comparar com medida
        particle_type = 'unknown'
        if abs(dE_dx - dE_dx_calc) / dE_dx_calc < 0.1:
            particle_type = 'proton'
        
        return particle_type

# Exemplo
detector = ParticleDetector('calorimeter')

# Resolução de energia
E = 50  # GeV
params = {'stochastic': 0.1, 'constant': 0.01, 'noise': 0.5}
sigma = detector.energy_resolution(E, params)

print(f"\n=== DETECTORES ===")
print(f"Resolução de energia em {E} GeV: {sigma:.2f} GeV ({sigma/E*100:.1f}%)")

# Reconstrução de trajetória
hits = [(0, 0), (1, 1), (2, 1.8), (3, 2.4)]
B = 2.0  # Tesla

track = detector.track_reconstruction(hits, B)
if track:
    print(f"\nMomento transverso reconstruído: {track['pT']:.2f} GeV/c")
```

**Conceitos Críticos:**
- Calorímetros e resolução de energia
- Detectores de trajetória
- Reconstrução de partículas
- Identificação de partículas (dE/dx)
- Triggers e aquisição de dados

---

## 14. COMPUTAÇÃO QUÂNTICA

### 14.1 Qubits e Portas Quânticas
```python
class QuantumComputing:
    """
    Fundamentos de computação quântica
    """
    
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.dim = 2**n_qubits
        self.state = np.zeros(self.dim, dtype=complex)
        self.state[0] = 1  # Estado |0...0⟩
    
    def pauli_matrices(self):
        """
        Matrizes de Pauli
        """
        I = np.array([[1, 0], [0, 1]], dtype=complex)
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        
        return {'I': I, 'X': X, 'Y': Y, 'Z': Z}
    
    def hadamard_gate(self):
        """
        Porta de Hadamard
        """
        return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    
    def cnot_gate(self):
        """
        Porta CNOT (Controlled-NOT)
        """
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0]
        ], dtype=complex)
    
    def apply_single_qubit_gate(self, gate, qubit_index):
        """
        Aplica porta de 1 qubit
        """
        # Construir operador completo usando produto tensorial
        operator = 1
        
        for i in range(self.n_qubits):
            if i == qubit_index:
                if operator == 1:
                    operator = gate
                else:
                    operator = np.kron(operator, gate)
            else:
                I = np.eye(2, dtype=complex)
                if operator == 1:
                    operator = I
                else:
                    operator = np.kron(operator, I)
        
        self.state = np.dot(operator, self.state)
    
    def apply_cnot(self, control, target):
        """
        Aplica porta CNOT
        """
        # Implementação simplificada para 2 qubits
        if self.n_qubits == 2:
            cnot = self.cnot_gate()
            self.state = np.dot(cnot, self.state)
    
    def measure(self, qubit_index=None):
        """
        Medição de qubit(s)
        """
        probabilities = np.abs(self.state)**2
        
        # Escolher resultado baseado em probabilidades
        outcome = np.random.choice(self.dim, p=probabilities)
        
        # Colapso do estado
        self.state = np.zeros(self.dim, dtype=complex)
        self.state[outcome] = 1
        
        return outcome
    
    def bell_state(self):
        """
        Cria estado de Bell (emaranhado)
        |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
        """
        if self.n_qubits != 2:
            raise ValueError("Bell state requires 2 qubits")
        
        # Aplicar H no primeiro qubit
        H = self.hadamard_gate()
        self.apply_single_qubit_gate(H, 0)
        
        # Aplicar CNOT
        self.apply_cnot(0, 1)
    
    def quantum_fourier_transform(self):
        """
        Transformada de Fourier Quântica
        """
        n = self.n_qubits
        
        # Matriz QFT
        omega = np.exp(2j * np.pi / self.dim)
        QFT = np.zeros((self.dim, self.dim), dtype=complex)
        
        for j in range(self.dim):
            for k in range(self.dim):
                QFT[j, k] = omega**(j*k) / np.sqrt(self.dim)
        
        self.state = np.dot(QFT, self.state)

class QuantumAlgorithms:
    """
    Algoritmos quânticos clássicos
    """
    
    def grover_search(self, n_qubits, target_state):
        """
        Algoritmo de Grover para busca
        """
        qc = QuantumComputing(n_qubits)
        
        # Superposição inicial
        H = qc.hadamard_gate()
        for i in range(n_qubits):
            qc.apply_single_qubit_gate(H, i)
        
        # Número de iterações
        N = 2**n_qubits
        n_iterations = int(np.pi * np.sqrt(N) / 4)
        
        for _ in range(n_iterations):
            # Oracle (marca o estado alvo)
            oracle = np.eye(N, dtype=complex)
            oracle[target_state, target_state] = -1
            qc.state = np.dot(oracle, qc.state)
            
            # Difusão
            diffusion = 2 * np.outer(qc.state, qc.state.conj()) - np.eye(N)
            qc.state = np.dot(diffusion, qc.state)
        
        # Medir
        result = qc.measure()
        
        return result
    
    def shor_period_finding(self, N, a):
        """
        Parte quântica do algoritmo de Shor (encontrar período)
        """
        # Simplificação conceitual
        # Na prática, requer muitos qubits e portas controladas
        
        n_qubits = int(np.ceil(np.log2(N)))
        qc = QuantumComputing(2 * n_qubits)
        
        # QFT para encontrar período
        qc.quantum_fourier_transform()
        
        return qc.state

# Exemplo
qc = QuantumComputing(n_qubits=2)

print("\n=== COMPUTAÇÃO QUÂNTICA ===")
print(f"Estado inicial: {qc.state}")

# Criar estado de Bell
qc.bell_state()
print(f"Estado de Bell: {qc.state}")

# Algoritmo de Grover
qa = QuantumAlgorithms()
target = 5  # Buscar estado |101⟩
result = qa.grover_search(n_qubits=3, target_state=target)
print(f"\nGrover encontrou: {result} (alvo: {target})")
```

**Conceitos Fundamentais:**
- Qubits e superposição
- Portas quânticas (Pauli, Hadamard, CNOT)
- Emaranhamento quântico
- Algoritmo de Grover
- Algoritmo de Shor
- Transformada de Fourier Quântica

---

## 15. RECURSOS E REFERÊNCIAS

### 15.1 Livros Essenciais

**Fundamentos Matemáticos:**
- "Mathematical Methods for Physics and Engineering" - Riley, Hobson & Bence
- "Linear Algebra Done Right" - Sheldon Axler
- "Complex Analysis" - Lars Ahlfors

**Mecânica Quântica:**
- "Principles of Quantum Mechanics" - R. Shankar
- "Modern Quantum Mechanics" - J.J. Sakurai
- "Quantum Mechanics: Concepts and Applications" - Nouredine Zettili

**Teoria Quântica de Campos:**
- "An Introduction to Quantum Field Theory" - Peskin & Schroeder
- "Quantum Field Theory in a Nutshell" - A. Zee
- "The Quantum Theory of Fields" - Steven Weinberg

**Relatividade Geral:**
- "Gravitation" - Misner, Thorne & Wheeler
- "General Relativity" - Robert Wald
- "Spacetime and Geometry" - Sean Carroll

**Física Computacional:**
- "Computational Physics" - Mark Newman
- "Numerical Recipes" - Press et al.
- "A Survey of Computational Physics" - Landau, Páez & Bordeianu

### 15.2 Recursos Online

**Cursos:**
- MIT OpenCourseWare - Classical Mechanics, Quantum Mechanics
- Stanford Online - Statistical Mechanics, Particle Physics
- Perimeter Institute - Advanced Topics in Theoretical Physics
- Coursera - Quantum Mechanics for Everyone

**Ferramentas Computacionais:**
- SciPy/NumPy - Computação científica
- SymPy - Matemática simbólica
- QuTiP - Quantum Toolbox in Python
- PyTorch/TensorFlow - Machine Learning para física

**Bases de Dados:**
- arXiv.org - Preprints de física
- INSPIRE-HEP - Literatura de física de altas energias
- PDG - Particle Data Group

### 15.3 Comunidades

- Physics Stack Exchange
- r/Physics e r/AskPhysics
- PhysicsForums.com
- ResearchGate

---

## Conclusão

Este documento fornece uma base sólida para o desenvolvimento de um modelo de IA especializado em física teórica e experimental computacional. A ênfase está na integração entre teoria física, métodos numéricos e implementação prática.

**Princípios Orientadores:**
1. **Rigor Matemático**: Manter precisão e consistência matemática
2. **Validação Experimental**: Comparar sempre com resultados analíticos quando disponíveis
3. **Eficiência Computacional**: Otimizar algoritmos para escalabilidade
4. **Documentação Clara**: Facilitar reprodutibilidade e colaboração
5. **Exploração Criativa**: Incentivar hipóteses originais e abordagens inovadoras

A combinação de fundamentos teóricos sólidos com habilidades computacionais práticas permite não apenas resolver problemas existentes, mas também descobrir novos fenômenos e desenvolver teorias inovadoras na física contemporânea.

**Áreas de Aplicação:**
- Simulações de sistemas quânticos complexos
- Modelagem cosmológica e astrofísica
- Previsão de propriedades de materiais
- Análise de dados experimentais de alta energia
- Desenvolvimento de algoritmos quânticos

**Próximos Passos Recomendados:**
1. Implementar os exemplos de código fornecidos
2. Estudar os livros e recursos recomendados
3. Participar de comunidades online de física computacional
4. Desenvolver projetos próprios baseados nos conceitos aprendidos
5. Contribuir para projetos open-source de física computacional

---

**Versão:** 1.0  
**Data:** Novembro 2024  
**Baseado em:** "Como se Tornar um BOM Físico Teórico" - Gerard 't Hooft  
**Licença:** MIT

---

*Este documento foi desenvolvido para fine-tuning de modelos de IA especializados em física teórica e experimental computacional, fornecendo conhecimento técnico aprofundado desde fundamentos matemáticos até aplicações avançadas em teoria quântica de campos, relatividade geral e computação quântica.*
