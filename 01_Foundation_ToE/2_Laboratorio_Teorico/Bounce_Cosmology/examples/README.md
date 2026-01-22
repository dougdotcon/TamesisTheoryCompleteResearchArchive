# 📚 Exemplos Práticos do Framework de Física Computacional

Este diretório contém exemplos práticos que demonstram o uso do framework de física computacional desenvolvido baseado no fine-tuning de IA especializada.

## 🎯 Exemplos Disponíveis

### 🚀 `demonstracao_completa.py`
**Demonstração completa de todas as funcionalidades do framework**

Este exemplo abrangente mostra:
- ✅ **Integração numérica avançada** com Runge-Kutta e validação
- ✅ **Simulações Monte Carlo** do modelo de Ising 2D
- ✅ **Mecânica quântica computacional** com oscilador harmônico
- ✅ **Relatividade geral numérica** com cosmologia LCDM
- ✅ **Benchmarking e otimização** automática de parâmetros
- ✅ **Funções especiais** da física matemática

**Como executar:**
```bash
cd /caminho/para/fisica-bigbang
python examples/demonstracao_completa.py
```

**Resultados gerados:**
- `resultados/demonstracao_integracao.png` - Evolução temporal de sistemas dinâmicos
- `resultados/demonstracao_ising.png` - Configuração final do modelo de Ising
- `resultados/demonstracao_quantica.png` - Funções de onda quânticas
- `resultados/demonstracao_cosmo.png` - Evolução cosmológica
- `resultados/demonstracao_funcoes.png` - Funções especiais
- `resultados/resumo_demonstracao.json` - Resumo completo dos resultados

## 🧪 Como Usar os Exemplos

### Pré-requisitos
```bash
# Instalar dependências básicas
pip install numpy scipy matplotlib

# Para funcionalidades avançadas
pip install qutip astropy gwpy classy
```

### Estrutura dos Exemplos

Cada exemplo segue a estrutura:
1. **Importação** dos módulos necessários
2. **Configuração** dos parâmetros físicos
3. **Execução** das simulações
4. **Análise** dos resultados
5. **Visualização** com matplotlib
6. **Salvamento** dos resultados

### Personalização

Os exemplos podem ser facilmente adaptados:

```python
# Modificar parâmetros físicos
omega = 2.0 * np.pi  # Frequência do oscilador
L = 32              # Tamanho do sistema Ising
H0 = 70             # Constante de Hubble

# Ajustar configurações numéricas
rtol = 1e-10        # Tolerância relativa
n_sweeps = 2000     # Número de sweeps Monte Carlo
```

## 📊 Interpretação dos Resultados

### Integração Numérica
- **Convergência**: Erros < 10⁻¹⁰ indicam precisão excelente
- **Estabilidade**: Manutenção de conservação de energia
- **Performance**: Comparação entre métodos RK45, DOP853, etc.

### Monte Carlo
- **Transição de fase**: Pico na capacidade calorífica ~ T = 2.27
- **Magnetização**: Queda brusca na temperatura crítica
- **Correlações**: Função de autocorrelação temporal

### Mecânica Quântica
- **Precisão**: Comparação analítica vs numérica
- **Estados excitados**: Energia cresce como (n + 1/2)ℏω
- **Funções de onda**: Oscilações características

### Relatividade Geral
- **Idade do universo**: ~13.8 Gyr para LCDM
- **Expansão acelerada**: Domínio de energia escura
- **Parâmetro de Hubble**: H(z) crescente com redshift

## 🔧 Desenvolvimento de Novos Exemplos

Para criar novos exemplos:

```python
# 1. Importar módulos necessários
from src.numerical_methods.integrators import IntegratorNumerico
from src.physics_models.quantum_mechanics import EquacaoSchrodinger

# 2. Definir sistema físico
def potencial_custom(x):
    return 0.5 * x**2 + 0.1 * x**4  # Potencial anarmônico

# 3. Configurar simulação
schrodinger = EquacaoSchrodinger(potencial_custom, -5, 5, 1000)

# 4. Executar e analisar
energias, wavefunctions = schrodinger.resolver_estados_ligados(5)

# 5. Visualizar resultados
plt.plot(schrodinger.x, wavefunctions[:, 0]**2)
plt.xlabel('x')
plt.ylabel('|ψ₀(x)|²')
plt.title('Estado Fundamental')
plt.show()
```

## 📈 Métricas de Qualidade

O framework inclui métricas automáticas:

- **Precisão numérica**: Erros relativos e absolutos
- **Convergência**: Taxa de convergência dos métodos
- **Estabilidade**: Manutenção de quantidades conservadas
- **Performance**: Tempo de execução e uso de memória
- **Validação**: Comparação com soluções analíticas

## 🎓 Exemplos Educacionais

Estes exemplos servem também para:
- **Ensino**: Demonstração de conceitos físicos
- **Pesquisa**: Base para investigações avançadas
- **Validação**: Teste de novas implementações
- **Benchmarking**: Comparação de performance

## 📞 Suporte

Para dúvidas sobre os exemplos:
- Verifique a documentação dos módulos em `src/`
- Consulte os testes em `tests/`
- Revise o fine-tuning em `fine-tuning-ia-fisica-teorica.md`

---

**🎯 Framework de Física Computacional - Pronto para Pesquisa Avançada!**
