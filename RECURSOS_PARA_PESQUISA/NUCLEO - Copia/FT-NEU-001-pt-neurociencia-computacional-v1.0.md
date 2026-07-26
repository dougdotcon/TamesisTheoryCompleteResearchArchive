# FT-NEU-001: Fine-Tuning para IA em Neurociência Computacional

## Visão Geral do Projeto

Este documento estabelece uma metodologia estruturada para o desenvolvimento de modelos de IA especializados em neurociência computacional, também conhecida como neurociência teórica ou computacional. O objetivo é criar sistemas de IA capazes de modelar, simular e entender os princípios fundamentais do funcionamento do cérebro, desde neurônios individuais até redes complexas de comportamento cognitivo.

### Contexto Filosófico
A neurociência computacional representa uma ponte entre a biologia do sistema nervoso e as ciências computacionais, buscando compreender como a matéria organizada de forma específica pode dar origem à consciência, cognição e comportamento inteligente. Cada modelo neural é uma tentativa de capturar os princípios fundamentais da computação biológica.

### Metodologia de Aprendizado Recomendada
1. **Integração Multiescala**: Conectar níveis molecular, celular e sistêmico
2. **Validação Biológica**: Comparar modelos com dados neurofisiológicos reais
3. **Abordagem Iterativa**: Refinar modelos através de ciclos experimento-simulação
4. **Considerações Éticas**: Respeitar a complexidade da função cerebral
5. **Colaboração Interdisciplinar**: Integrar neurociência, psicologia e computação

---

## 1. FUNDAMENTOS NEUROCIENTÍFICOS E COMPUTACIONAIS

### 1.1 Modelagem de Neurônios e Sinapses
```python
# Exemplo: Implementação de modelos neurais biológicos usando Brian2
import numpy as np
import matplotlib.pyplot as plt
from brian2 import *

class BiophysicalNeuronModel:
    """Modelo de neurônio com propriedades biológicas realistas"""

    def __init__(self, neuron_type='pyramidal'):
        self.neuron_type = neuron_type
        self.setup_neuron_parameters()

    def setup_neuron_parameters(self):
        """Configura parâmetros baseados no tipo de neurônio"""

        # Parâmetros comuns
        self.Cm = 1 * nF  # Capacitância da membrana
        self.gL = 0.1 * nS  # Condutância de fuga
        self.EL = -70 * mV  # Potencial de repouso
        self.Vt = -50 * mV  # Threshold de spike

        if self.neuron_type == 'pyramidal':
            # Neurônio piramidal (córtex)
            self.gNa = 50 * nS  # Condutância sódio
            self.gK = 5 * nS    # Condutância potássio
            self.ENa = 50 * mV  # Potencial reverso sódio
            self.EK = -90 * mV  # Potencial reverso potássio
            self.tau_adaptation = 200 * ms

        elif self.neuron_type == 'interneuron':
            # Interneurônio (GABAérgico)
            self.gNa = 35 * nS
            self.gK = 9 * nS
            self.ENa = 55 * mV
            self.EK = -95 * mV
            self.tau_adaptation = 100 * ms

        elif self.neuron_type == 'thalamic':
            # Neurônio talâmico
            self.gNa = 40 * nS
            self.gK = 7 * nS
            self.ENa = 45 * mV
            self.EK = -85 * mV
            self.tau_adaptation = 150 * ms

    def create_adaptive_exponential_model(self):
        """
        Cria modelo de neurônio adaptativo exponencial (AdEx)

        O modelo AdEx captura a dinâmica de spiking de neurônios corticais
        com adaptação baseada em correntes de potássio de longa duração
        """

        model_eqs = '''
        dvm/dt = (gL*(EL - vm) + gL*DeltaT*exp((vm - Vt)/DeltaT) - w + I)/Cm : volt
        dw/dt = (a*(vm - EL) - w)/tau_w : amp
        I : amp
        DeltaT : volt
        Vcut : volt
        '''

        # Parâmetros do modelo AdEx
        params = {
            'gL': self.gL,
            'EL': self.EL,
            'Cm': self.Cm,
            'Vt': self.Vt,
            'DeltaT': 2 * mV,  # Slope factor
            'Vcut': 0 * mV,    # Cutoff para reset
            'a': 4 * nS,       # Adaptação subthreshold
            'tau_w': self.tau_adaptation
        }

        # Reset após spike
        reset_eqs = '''
        vm = EL
        w += b
        '''

        threshold = 'vm > Vcut'

        return model_eqs, params, threshold, reset_eqs

    def simulate_neuron_response(self, input_current, simulation_time=1*second):
        """
        Simula resposta do neurônio a corrente de entrada

        Parameters
        ----------
        input_current : TimedArray ou função
            Corrente de entrada ao neurônio
        simulation_time : Quantity
            Tempo total de simulação

        Returns
        -------
        dict
            Resultados da simulação (tensão, spikes, corrente de adaptação)
        """

        # Cria modelo
        model_eqs, params, threshold, reset_eqs = self.create_adaptive_exponential_model()

        # Define grupo neuronal
        neuron = NeuronGroup(1, model_eqs, threshold=threshold,
                           reset=reset_eqs, method='euler')

        # Define parâmetros
        neuron.set_states(params)

        # Corrente de entrada
        neuron.I = input_current

        # Monitores
        voltage_monitor = StateMonitor(neuron, 'vm', record=True)
        spike_monitor = SpikeMonitor(neuron)
        adaptation_monitor = StateMonitor(neuron, 'w', record=True)

        # Executa simulação
        run(simulation_time)

        return {
            'voltage': voltage_monitor.vm[0],
            'time': voltage_monitor.t,
            'spikes': spike_monitor.spike_trains()[0],
            'adaptation': adaptation_monitor.w[0]
        }

    def analyze_firing_patterns(self, simulation_results):
        """
        Analisa padrões de disparo do neurônio

        Parameters
        ----------
        simulation_results : dict
            Resultados da simulação

        Returns
        -------
        dict
            Análise dos padrões de disparo
        """

        spikes = simulation_results['spikes']
        voltage = simulation_results['voltage']
        time = simulation_results['time']

        analysis = {}

        if len(spikes) > 1:
            # Frequência de disparo
            analysis['firing_rate'] = len(spikes) / (time[-1] - time[0])

            # Intervalos inter-spike (ISI)
            isis = np.diff(spikes)
            analysis['isi_mean'] = np.mean(isis)
            analysis['isi_std'] = np.std(isis)
            analysis['isi_cv'] = analysis['isi_std'] / analysis['isi_mean'] if analysis['isi_mean'] > 0 else 0

            # Classificação do padrão de disparo
            analysis['firing_pattern'] = self.classify_firing_pattern(isis)

        else:
            analysis['firing_rate'] = 0
            analysis['isi_mean'] = 0
            analysis['isi_std'] = 0
            analysis['isi_cv'] = 0
            analysis['firing_pattern'] = 'silent'

        # Análise de membrana
        analysis['membrane_analysis'] = self.analyze_membrane_potential(voltage, time)

        return analysis

    def classify_firing_pattern(self, isis):
        """
        Classifica padrão de disparo baseado em intervalos inter-spike

        Parameters
        ----------
        isis : array
            Intervalos inter-spike

        Returns
        -------
        str
            Tipo de padrão de disparo
        """

        if len(isis) < 3:
            return 'insufficient_data'

        cv = np.std(isis) / np.mean(isis) if np.mean(isis) > 0 else 0

        if cv < 0.5:
            return 'regular'
        elif cv < 1.0:
            return 'irregular'
        else:
            return 'bursting'

    def analyze_membrane_potential(self, voltage, time):
        """
        Analisa potencial de membrana

        Parameters
        ----------
        voltage : array
            Valores de tensão
        time : array
            Tempos correspondentes

        Returns
        -------
        dict
            Análise do potencial de membrana
        """

        analysis = {
            'mean_voltage': np.mean(voltage),
            'voltage_std': np.std(voltage),
            'min_voltage': np.min(voltage),
            'max_voltage': np.max(voltage),
            'resting_potential': np.percentile(voltage, 10)  # Percentil 10 como repouso aproximado
        }

        # Análise de flutuações
        voltage_diff = np.diff(voltage)
        analysis['voltage_fluctuations'] = np.std(voltage_diff)

        return analysis

    def create_network_model(self, n_neurons=100, connection_probability=0.1):
        """
        Cria rede de neurônios conectados

        Parameters
        ----------
        n_neurons : int
            Número de neurônios na rede
        connection_probability : float
            Probabilidade de conexão entre neurônios

        Returns
        -------
        dict
            Modelo de rede configurado
        """

        # Cria população de neurônios
        model_eqs, params, threshold, reset_eqs = self.create_adaptive_exponential_model()

        neurons = NeuronGroup(n_neurons, model_eqs, threshold=threshold,
                            reset=reset_eqs, method='euler')
        neurons.set_states(params)

        # Cria conexões sinápticas
        synapses = Synapses(neurons, neurons, 'w : 1', on_pre='v_post += w')
        synapses.connect(p=connection_probability)

        # Define pesos sinápticos
        synapses.w = '0.1 + 0.4*rand()'  # Pesos aleatórios entre 0.1 e 0.5

        network_model = {
            'neurons': neurons,
            'synapses': synapses,
            'monitors': {}
        }

        return network_model

    def simulate_network_activity(self, network_model, simulation_time=1*second,
                                input_pattern='random'):
        """
        Simula atividade de rede neural

        Parameters
        ----------
        network_model : dict
            Modelo de rede configurado
        simulation_time : Quantity
            Tempo de simulação
        input_pattern : str
            Padrão de entrada ('random', 'structured', 'sensory')

        Returns
        -------
        dict
            Resultados da simulação de rede
        """

        neurons = network_model['neurons']
        synapses = network_model['synapses']

        # Define padrão de entrada
        if input_pattern == 'random':
            neurons.I = '5*nA * rand()'  # Corrente aleatória
        elif input_pattern == 'structured':
            neurons.I = '10*nA * sin(2*pi*10*Hz*t)'  # Entrada sinusoidal
        elif input_pattern == 'sensory':
            neurons.I = '15*nA * (t/second < 0.5)'  # Pulso sensorial

        # Monitores
        spike_monitor = SpikeMonitor(neurons)
        voltage_monitor = StateMonitor(neurons, 'vm', record=[0, 1, 2])  # Monitora primeiros 3 neurônios

        network_model['monitors']['spikes'] = spike_monitor
        network_model['monitors']['voltage'] = voltage_monitor

        # Executa simulação
        run(simulation_time)

        # Análise de resultados
        results = self.analyze_network_dynamics(network_model)

        return results

    def analyze_network_dynamics(self, network_model):
        """
        Analisa dinâmica da rede neural

        Parameters
        ----------
        network_model : dict
            Modelo de rede com monitores

        Returns
        -------
        dict
            Análise da dinâmica de rede
        """

        spike_monitor = network_model['monitors']['spikes']

        analysis = {
            'total_spikes': len(spike_monitor.i),
            'mean_firing_rate': len(spike_monitor.i) / (defaultclock.t / second) / len(network_model['neurons']),
            'spike_trains': spike_monitor.spike_trains(),
            'correlation_analysis': self.compute_spike_correlations(spike_monitor),
            'population_dynamics': self.analyze_population_activity(spike_monitor)
        }

        return analysis

    def compute_spike_correlations(self, spike_monitor):
        """
        Computa correlações entre trens de spikes

        Parameters
        ----------
        spike_monitor : SpikeMonitor
            Monitor de spikes

        Returns
        -------
        dict
            Análise de correlações
        """

        spike_trains = spike_monitor.spike_trains()

        if len(spike_trains) < 2:
            return {'correlation_coefficient': 0, 'note': 'Insuficiente dados'}

        # Computa correlação cruzada simplificada
        correlations = []
        for i in range(len(spike_trains)):
            for j in range(i+1, len(spike_trains)):
                train1 = spike_trains[i]
                train2 = spike_trains[j]

                if len(train1) > 0 and len(train2) > 0:
                    # Correlação básica baseada em taxa de disparo
                    rate1 = len(train1) / (defaultclock.t / second)
                    rate2 = len(train2) / (defaultclock.t / second)

                    # Correlação normalizada
                    correlation = (rate1 * rate2) / (rate1 + rate2 + 1e-10)
                    correlations.append(correlation)

        mean_correlation = np.mean(correlations) if correlations else 0

        return {
            'correlation_coefficient': mean_correlation,
            'individual_correlations': correlations
        }

    def analyze_population_activity(self, spike_monitor):
        """
        Analisa atividade populacional

        Parameters
        ----------
        spike_monitor : SpikeMonitor
            Monitor de spikes

        Returns
        -------
        dict
            Análise de atividade populacional
        """

        spike_times = spike_monitor.t
        spike_neurons = spike_monitor.i

        # Computa histograma temporal
        time_bins = np.arange(0, defaultclock.t/second, 0.01)  # Bins de 10ms
        spike_histogram, _ = np.histogram(spike_times/second, bins=time_bins)

        # Análise de sincronização
        instantaneous_rate = spike_histogram / 0.01  # Hz

        analysis = {
            'mean_population_rate': np.mean(instantaneous_rate),
            'peak_population_rate': np.max(instantaneous_rate),
            'rate_variability': np.std(instantaneous_rate),
            'synchronization_index': self.compute_synchronization_index(spike_times, spike_neurons)
        }

        return analysis

    def compute_synchronization_index(self, spike_times, spike_neurons):
        """
        Computa índice de sincronização populacional

        Parameters
        ----------
        spike_times : array
            Tempos dos spikes
        spike_neurons : array
            IDs dos neurônios que dispararam

        Returns
        -------
        float
            Índice de sincronização (0-1)
        """

        if len(spike_times) < 10:
            return 0

        # Método simplificado: coeficiente de variação dos intervalos inter-spike
        isis = np.diff(np.sort(spike_times))
        cv = np.std(isis) / np.mean(isis) if np.mean(isis) > 0 else 0

        # Converte para índice de sincronização (CV alto = baixa sincronização)
        sync_index = 1 / (1 + cv)

        return sync_index
```

**Conceitos Críticos:**
- Modelos neurais biológicos (Hodgkin-Huxley, AdEx, Izhikevich)
- Propriedades elétricas dos neurônios
- Dinâmica de spiking e plasticidade sináptica
- Redes neurais recorrentes e teoria de campo médio

### 1.2 Plasticidade Sináptica e Aprendizagem
```python
# Exemplo: Implementação de mecanismos de plasticidade sináptica
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional

class SynapticPlasticityModel:
    """Modelo de plasticidade sináptica para aprendizado neural"""

    def __init__(self, pre_neurons: int, post_neurons: int):
        self.pre_neurons = pre_neurons
        self.post_neurons = post_neurons
        self.setup_plasticity_mechanisms()

    def setup_plasticity_mechanisms(self):
        """Configura mecanismos de plasticidade sináptica"""

        # Matriz de pesos sinápticos
        self.weights = torch.randn(self.pre_neurons, self.post_neurons) * 0.1

        # Parâmetros de plasticidade
        self.plasticity_params = {
            'stdp': {
                'A_plus': 0.005,   # Amplitude LTP
                'A_minus': -0.005, # Amplitude LTD
                'tau_plus': 20.0,  # Constante de tempo LTP (ms)
                'tau_minus': 20.0  # Constante de tempo LTD (ms)
            },
            'homeostatic': {
                'target_rate': 10.0,  # Taxa alvo (Hz)
                'adaptation_rate': 0.01  # Taxa de adaptação
            },
            'structural': {
                'pruning_threshold': 0.01,  # Threshold para poda
                'growth_probability': 0.001  # Probabilidade de crescimento
            }
        }

        # Histórico de atividade
        self.pre_activity = []
        self.post_activity = []
        self.correlation_history = []

    def spike_timing_dependent_plasticity(self, pre_spikes: torch.Tensor,
                                        post_spikes: torch.Tensor,
                                        time_window: float = 50.0):
        """
        Implementa STDP (Spike-Timing Dependent Plasticity)

        Parameters
        ----------
        pre_spikes : torch.Tensor
            Tempos de spike dos neurônios pré-sinápticos
        post_spikes : torch.Tensor
            Tempos de spike dos neurônios pós-sinápticos
        time_window : float
            Janela temporal para STDP (ms)

        Returns
        -------
        torch.Tensor
            Mudanças nos pesos sinápticos
        """

        delta_w = torch.zeros_like(self.weights)

        # Para cada par pré-pós
        for pre_idx in range(self.pre_neurons):
            for post_idx in range(self.post_neurons):
                pre_times = pre_spikes[pre_idx]
                post_times = post_spikes[post_idx]

                if len(pre_times) > 0 and len(post_times) > 0:
                    # Computa todas as diferenças de tempo possíveis
                    for pre_t in pre_times:
                        for post_t in post_times:
                            delta_t = post_t - pre_t  # Δt = t_post - t_pre

                            if abs(delta_t) <= time_window:
                                # Função STDP clássica
                                if delta_t > 0:
                                    # LTP: pré antes de pós
                                    weight_change = self.plasticity_params['stdp']['A_plus'] * \
                                                  torch.exp(-abs(delta_t) / self.plasticity_params['stdp']['tau_plus'])
                                else:
                                    # LTD: pós antes de pré
                                    weight_change = self.plasticity_params['stdp']['A_minus'] * \
                                                  torch.exp(-abs(delta_t) / self.plasticity_params['stdp']['tau_minus'])

                                delta_w[pre_idx, post_idx] += weight_change

        # Aplica mudanças aos pesos
        self.weights += delta_w

        # Mantém pesos dentro de limites
        self.weights = torch.clamp(self.weights, -1.0, 1.0)

        return delta_w

    def homeostatic_plasticity(self, firing_rates: torch.Tensor):
        """
        Implementa plasticidade homeostática para estabilizar taxas de disparo

        Parameters
        ----------
        firing_rates : torch.Tensor
            Taxas de disparo atuais dos neurônios pós-sinápticos

        Returns
        -------
        torch.Tensor
            Ajustes homeostáticos nos pesos
        """

        target_rate = self.plasticity_params['homeostatic']['target_rate']
        adaptation_rate = self.plasticity_params['homeostatic']['adaptation_rate']

        # Computa desvio da taxa alvo
        rate_deviation = firing_rates - target_rate

        # Ajuste homeostático: reduz pesos se taxa alta, aumenta se baixa
        homeostatic_adjustment = -adaptation_rate * rate_deviation.unsqueeze(0)

        # Aplica ajuste a todos os pesos de entrada
        delta_w = homeostatic_adjustment.expand(self.pre_neurons, -1)

        self.weights += delta_w

        return delta_w

    def structural_plasticity(self):
        """
        Implementa plasticidade estrutural (crescimento/poda de sinapses)

        Returns
        -------
        dict
            Estatísticas de mudanças estruturais
        """

        structural_changes = {
            'pruned_synapses': 0,
            'grown_synapses': 0,
            'total_synapses': self.weights.numel()
        }

        # Poda de sinapses fracas
        pruning_mask = torch.abs(self.weights) < self.plasticity_params['structural']['pruning_threshold']
        structural_changes['pruned_synapses'] = pruning_mask.sum().item()

        # Crescimento de novas sinapses
        growth_mask = torch.rand_like(self.weights) < self.plasticity_params['structural']['growth_probability']
        structural_changes['grown_synapses'] = growth_mask.sum().item()

        # Aplica mudanças
        self.weights = torch.where(pruning_mask, torch.zeros_like(self.weights), self.weights)
        self.weights = torch.where(growth_mask & (self.weights == 0),
                                 torch.randn_like(self.weights) * 0.01,
                                 self.weights)

        return structural_changes

    def update_activity_history(self, pre_activity: torch.Tensor,
                              post_activity: torch.Tensor):
        """
        Atualiza histórico de atividade para análise de correlação

        Parameters
        ----------
        pre_activity : torch.Tensor
            Atividade dos neurônios pré-sinápticos
        post_activity : torch.Tensor
            Atividade dos neurônios pós-sinápticos
        """

        self.pre_activity.append(pre_activity.detach().cpu())
        self.post_activity.append(post_activity.detach().cpu())

        # Mantém histórico limitado
        if len(self.pre_activity) > 100:
            self.pre_activity = self.pre_activity[-100:]
            self.post_activity = self.post_activity[-100:]

    def compute_correlation_learning(self):
        """
        Computa aprendizado baseado em correlação de atividade

        Returns
        -------
        torch.Tensor
            Mudanças nos pesos baseadas em correlação
        """

        if len(self.pre_activity) < 2:
            return torch.zeros_like(self.weights)

        # Computa correlação média recente
        pre_recent = torch.stack(self.pre_activity[-10:])  # Últimas 10 amostras
        post_recent = torch.stack(self.post_activity[-10:])

        # Correlação entre atividade pré e pós
        correlation_matrix = torch.corrcoef(torch.cat([pre_recent.T, post_recent.T], dim=0))
        pre_post_corr = correlation_matrix[:self.pre_neurons, self.pre_neurons:]

        # Converte correlação em mudanças de peso
        learning_rate = 0.001
        delta_w = learning_rate * pre_post_corr

        self.weights += delta_w

        return delta_w

    def simulate_plasticity_dynamics(self, simulation_steps: int = 1000,
                                   input_pattern: str = 'correlated'):
        """
        Simula dinâmica de plasticidade sináptica

        Parameters
        ----------
        simulation_steps : int
            Número de passos de simulação
        input_pattern : str
            Padrão de entrada ('correlated', 'anticorrelated', 'random')

        Returns
        -------
        dict
            Resultados da simulação de plasticidade
        """

        results = {
            'weight_evolution': [],
            'correlation_evolution': [],
            'plasticity_events': []
        }

        for step in range(simulation_steps):
            # Gera atividade baseada no padrão
            pre_activity, post_activity = self.generate_activity_pattern(input_pattern)

            # Atualiza histórico
            self.update_activity_history(pre_activity, post_activity)

            # Aplica mecanismos de plasticidade
            if step % 10 == 0:  # STDP a cada 10 passos
                stsp_changes = self.spike_timing_dependent_plasticity(
                    torch.tensor([0.0]), torch.tensor([0.0])  # Placeholder
                )

            if step % 50 == 0:  # Homeostático a cada 50 passos
                firing_rates = torch.mean(post_activity, dim=0)
                homeostatic_changes = self.homeostatic_plasticity(firing_rates)

            if step % 100 == 0:  # Estrutural a cada 100 passos
                structural_changes = self.structural_plasticity()
                results['plasticity_events'].append({
                    'step': step,
                    'type': 'structural',
                    'changes': structural_changes
                })

            # Computa aprendizado por correlação
            if step % 20 == 0:
                correlation_changes = self.compute_correlation_learning()

            # Registra evolução
            if step % 50 == 0:
                results['weight_evolution'].append(self.weights.clone())
                current_corr = torch.corrcoef(torch.cat([pre_activity.T, post_activity.T], dim=0))
                results['correlation_evolution'].append(current_corr)

        return results

    def generate_activity_pattern(self, pattern_type: str):
        """
        Gera padrões de atividade neuronal

        Parameters
        ----------
        pattern_type : str
            Tipo de padrão ('correlated', 'anticorrelated', 'random')

        Returns
        -------
        Tuple[torch.Tensor, torch.Tensor]
            Atividade pré e pós-sináptica
        """

        if pattern_type == 'correlated':
            # Atividade altamente correlacionada
            base_activity = torch.randn(self.pre_neurons)
            pre_activity = base_activity + 0.1 * torch.randn(self.pre_neurons)
            post_activity = base_activity + 0.1 * torch.randn(self.post_neurons)

        elif pattern_type == 'anticorrelated':
            # Atividade anticorrelacionada
            pre_activity = torch.randn(self.pre_neurons)
            post_activity = -pre_activity + 0.1 * torch.randn(self.post_neurons)

        elif pattern_type == 'random':
            # Atividade independente
            pre_activity = torch.randn(self.pre_neurons)
            post_activity = torch.randn(self.post_neurons)

        return pre_activity, post_activity

    def analyze_plasticity_outcome(self, simulation_results: Dict):
        """
        Analisa resultados da simulação de plasticidade

        Parameters
        ----------
        simulation_results : Dict
            Resultados da simulação

        Returns
        -------
        Dict
            Análise dos resultados
        """

        analysis = {
            'weight_distribution': self.analyze_weight_distribution(),
            'learning_efficiency': self.compute_learning_efficiency(simulation_results),
            'structural_changes': self.summarize_structural_changes(simulation_results)
        }

        return analysis

    def analyze_weight_distribution(self):
        """Analisa distribuição dos pesos sinápticos"""

        weights_flat = self.weights.flatten().numpy()

        analysis = {
            'mean_weight': float(np.mean(weights_flat)),
            'std_weight': float(np.std(weights_flat)),
            'weight_range': [float(np.min(weights_flat)), float(np.max(weights_flat))],
            'sparsity': float(np.sum(weights_flat == 0) / len(weights_flat)),
            'weight_distribution_stats': {
                'positive_weights': float(np.sum(weights_flat > 0) / len(weights_flat)),
                'negative_weights': float(np.sum(weights_flat < 0) / len(weights_flat)),
                'strong_weights': float(np.sum(np.abs(weights_flat) > 0.5) / len(weights_flat))
            }
        }

        return analysis

    def compute_learning_efficiency(self, simulation_results: Dict):
        """Computa eficiência do aprendizado"""

        if not simulation_results['weight_evolution']:
            return {'efficiency_score': 0}

        # Analisa evolução dos pesos
        initial_weights = simulation_results['weight_evolution'][0]
        final_weights = simulation_results['weight_evolution'][-1]

        weight_change = torch.mean(torch.abs(final_weights - initial_weights)).item()

        # Eficiência baseada na mudança relativa
        relative_change = weight_change / (torch.mean(torch.abs(initial_weights)).item() + 1e-10)

        efficiency = {
            'weight_change_magnitude': weight_change,
            'relative_weight_change': relative_change,
            'efficiency_score': min(1.0, relative_change * 10)  # Normalizado
        }

        return efficiency

    def summarize_structural_changes(self, simulation_results: Dict):
        """Resume mudanças estruturais"""

        structural_events = [event for event in simulation_results['plasticity_events']
                           if event['type'] == 'structural']

        if not structural_events:
            return {'total_pruned': 0, 'total_grown': 0}

        total_pruned = sum(event['changes']['pruned_synapses'] for event in structural_events)
        total_grown = sum(event['changes']['grown_synapses'] for event in structural_events)

        summary = {
            'total_pruned': total_pruned,
            'total_grown': total_grown,
            'net_change': total_grown - total_pruned,
            'plasticity_events_count': len(structural_events)
        }

        return summary
```

**Tópicos Essenciais:**
- Plasticidade Hebbiana e STDP (Spike-Timing Dependent Plasticity)
- Aprendizagem por reforço em redes neurais
- Plasticidade homeostática e estabilização
- Plasticidade estrutural e reorganização sináptica

---

## 2. ANÁLISE DE DADOS NEUROFISIOLÓGICOS COM IA

### 2.1 Processamento de Sinais Neurais (EEG, MEG)
**Técnicas Essenciais:**
- Análise de frequência e conectividade cerebral
- Detecção de artefatos e pré-processamento
- Classificação de estados mentais
- Biomarcadores de doenças neurológicas

```python
# Exemplo: Sistema de análise de EEG usando deep learning
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from scipy.signal import welch, stft
import mne
from typing import Dict, List, Tuple, Optional

class EEGAnalysisSystem:
    """Sistema completo de análise de EEG usando deep learning"""

    def __init__(self, sampling_rate: int = 250, n_channels: int = 32):
        self.sampling_rate = sampling_rate
        self.n_channels = n_channels
        self.setup_preprocessing()
        self.initialize_models()

    def setup_preprocessing(self):
        """Configura pipeline de pré-processamento de EEG"""

        self.preprocessing_steps = {
            'bandpass_filter': {'low_freq': 1.0, 'high_freq': 40.0},
            'notch_filter': {'freq': 50.0},  # Remove interferência de linha
            'artifact_removal': {
                'eog_channels': ['EOG1', 'EOG2'],
                'ecg_channels': ['ECG'],
                'rejection_threshold': 100e-6  # 100 µV
            },
            'spatial_filter': {'method': 'car'},  # Common Average Reference
            'epoching': {'tmin': -0.2, 'tmax': 0.8, 'baseline': (-0.2, 0)}
        }

    def initialize_models(self):
        """Inicializa modelos de deep learning para EEG"""

        # Modelo CNN para classificação de estados mentais
        self.mental_state_classifier = EEGMentalStateClassifier(
            n_channels=self.n_channels,
            n_classes=4  # relaxed, focused, drowsy, stressed
        )

        # Modelo para detecção de epilepsia
        self.epilepsy_detector = EpilepticSpikeDetector(
            n_channels=self.n_channels,
            sequence_length=1000  # 4 segundos a 250 Hz
        )

        # Modelo de análise de conectividade
        self.connectivity_analyzer = BrainConnectivityAnalyzer(
            n_channels=self.n_channels,
            freq_bands=['delta', 'theta', 'alpha', 'beta', 'gamma']
        )

    def preprocess_eeg_data(self, raw_data: np.ndarray,
                          channel_names: List[str]) -> mne.io.RawArray:
        """
        Pré-processa dados de EEG crus

        Parameters
        ----------
        raw_data : np.ndarray
            Dados EEG crus (n_channels, n_times)
        channel_names : List[str]
            Nomes dos canais

        Returns
        -------
        mne.io.RawArray
            Dados pré-processados no formato MNE
        """

        # Cria objeto MNE Raw
        info = mne.create_info(channel_names, self.sampling_rate, ch_types='eeg')
        raw = mne.io.RawArray(raw_data, info)

        # Aplica filtros
        raw.filter(
            self.preprocessing_steps['bandpass_filter']['low_freq'],
            self.preprocessing_steps['bandpass_filter']['high_freq'],
            fir_design='firwin'
        )

        # Remove interferência de linha
        raw.notch_filter(self.preprocessing_steps['notch_filter']['freq'])

        # Aplica referência comum média
        raw.set_eeg_reference('average')

        # Detecção e remoção de artefatos
        self.remove_artifacts(raw)

        return raw

    def remove_artifacts(self, raw: mne.io.RawArray):
        """Remove artefatos dos dados EEG"""

        # Detecção automática de artefatos
        artifacts, _ = mne.preprocessing.find_eog_events(raw)

        # Interpolações para correção de artefatos
        if len(artifacts) > 0:
            # Cria anotações para artefatos
            onset = artifacts[:, 0] / raw.info['sfreq']
            duration = np.ones(len(artifacts)) * 0.5  # 500ms
            annotations = mne.Annotations(onset, duration, 'artifact')

            raw.set_annotations(annotations)

            # Interpola regiões com artefatos
            raw.interpolate_bads()

    def extract_frequency_features(self, raw: mne.io.RawArray) -> Dict[str, np.ndarray]:
        """
        Extrai features de frequência do EEG

        Parameters
        ----------
        raw : mne.io.RawArray
            Dados EEG pré-processados

        Returns
        -------
        Dict[str, np.ndarray]
            Features de frequência por banda
        """

        data = raw.get_data()
        freq_bands = {
            'delta': (1, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 40)
        }

        features = {}

        for band_name, (low_freq, high_freq) in freq_bands.items():
            # Computa PSD usando Welch
            freqs, psd = welch(data, fs=self.sampling_rate,
                             nperseg=1024, nfft=2048)

            # Seleciona frequências na banda
            band_mask = (freqs >= low_freq) & (freqs <= high_freq)
            band_power = np.mean(psd[:, band_mask], axis=1)

            features[f'{band_name}_power'] = band_power

            # Computa razões entre bandas
            if band_name == 'alpha':
                features['alpha_beta_ratio'] = band_power / (features.get('beta_power',
                                        np.ones_like(band_power)) + 1e-10)

        return features

    def compute_connectivity_matrix(self, raw: mne.io.RawArray,
                                  method: str = 'pli') -> np.ndarray:
        """
        Computa matriz de conectividade cerebral

        Parameters
        ----------
        raw : mne.io.RawArray
            Dados EEG
        method : str
            Método de conectividade ('pli', 'coh', 'imaginary_coh')

        Returns
        -------
        np.ndarray
            Matriz de conectividade (n_channels, n_channels)
        """

        data = raw.get_data()
        n_channels = data.shape[0]

        connectivity_matrix = np.zeros((n_channels, n_channels))

        # Computa conectividade para cada par de canais
        for i in range(n_channels):
            for j in range(i+1, n_channels):
                if method == 'pli':
                    connectivity = self.compute_pli(data[i], data[j])
                elif method == 'coh':
                    connectivity = self.compute_coherence(data[i], data[j])
                elif method == 'imaginary_coh':
                    connectivity = self.compute_imaginary_coherence(data[i], data[j])

                connectivity_matrix[i, j] = connectivity
                connectivity_matrix[j, i] = connectivity

        return connectivity_matrix

    def compute_pli(self, signal1: np.ndarray, signal2: np.ndarray) -> float:
        """
        Computa Phase Lag Index (PLI) entre dois sinais

        Parameters
        ----------
        signal1, signal2 : np.ndarray
            Sinais EEG de dois canais

        Returns
        -------
        float
            Valor de PLI (0-1)
        """

        from scipy.signal import hilbert

        # Computa fase instantânea usando transformada de Hilbert
        analytic1 = hilbert(signal1)
        analytic2 = hilbert(signal2)

        phase1 = np.angle(analytic1)
        phase2 = np.angle(analytic2)

        # Computa diferença de fase
        phase_diff = phase1 - phase2

        # PLI: valor absoluto da média do sinal da diferença de fase
        pli = np.abs(np.mean(np.sign(np.sin(phase_diff))))

        return pli

    def compute_coherence(self, signal1: np.ndarray, signal2: np.ndarray) -> float:
        """
        Computa coerência entre dois sinais

        Parameters
        ----------
        signal1, signal2 : np.ndarray
            Sinais EEG

        Returns
        -------
        float
            Valor de coerência (0-1)
        """

        from scipy.signal import coherence

        # Computa coerência nas frequências de interesse
        freqs, coh = coherence(signal1, signal2, fs=self.sampling_rate,
                             nperseg=1024, nfft=2048)

        # Média nas bandas alpha e beta (8-30 Hz)
        alpha_beta_mask = (freqs >= 8) & (freqs <= 30)
        avg_coherence = np.mean(coh[alpha_beta_mask]) if np.any(alpha_beta_mask) else 0

        return avg_coherence

    def compute_imaginary_coherence(self, signal1: np.ndarray, signal2: np.ndarray) -> float:
        """
        Computa Imaginary Coherence (reduz volume conduction)

        Parameters
        ----------
        signal1, signal2 : np.ndarray
            Sinais EEG

        Returns
        -------
        float
            Valor de imaginary coherence
        """

        from scipy.signal import coherence

        freqs, coh = coherence(signal1, signal2, fs=self.sampling_rate,
                             nperseg=1024, nfft=2048)

        # Extrai parte imaginária da coerência
        imag_coh = np.imag(coh)

        # Média absoluta nas bandas de interesse
        alpha_beta_mask = (freqs >= 8) & (freqs <= 30)
        avg_imag_coherence = np.mean(np.abs(imag_coh[alpha_beta_mask])) if np.any(alpha_beta_mask) else 0

        return avg_imag_coherence

    def classify_mental_state(self, raw: mne.io.RawArray) -> Dict[str, any]:
        """
        Classifica estado mental baseado em EEG

        Parameters
        ----------
        raw : mne.io.RawArray
            Dados EEG

        Returns
        -------
        Dict[str, any]
            Classificação de estado mental
        """

        # Extrai features
        freq_features = self.extract_frequency_features(raw)
        connectivity_matrix = self.compute_connectivity_matrix(raw)

        # Prepara dados para o modelo
        model_input = self.prepare_model_input(freq_features, connectivity_matrix)

        # Classificação
        with torch.no_grad():
            self.mental_state_classifier.eval()
            predictions = self.mental_state_classifier(model_input)
            predicted_class = torch.argmax(predictions, dim=1).item()
            confidence = torch.max(predictions, dim=1)[0].item()

        class_names = ['relaxed', 'focused', 'drowsy', 'stressed']

        return {
            'predicted_state': class_names[predicted_class],
            'confidence': confidence,
            'feature_contributions': self.analyze_feature_contributions(freq_features)
        }

    def prepare_model_input(self, freq_features: Dict[str, np.ndarray],
                          connectivity_matrix: np.ndarray) -> torch.Tensor:
        """
        Prepara entrada para o modelo de classificação

        Parameters
        ----------
        freq_features : Dict[str, np.ndarray]
            Features de frequência
        connectivity_matrix : np.ndarray
            Matriz de conectividade

        Returns
        -------
        torch.Tensor
            Tensor pronto para entrada no modelo
        """

        # Combina features de frequência e conectividade
        freq_array = np.concatenate([v for v in freq_features.values()])
        connectivity_flat = connectivity_matrix.flatten()

        # Concatena tudo
        combined_features = np.concatenate([freq_array, connectivity_flat])

        return torch.FloatTensor(combined_features).unsqueeze(0)

    def analyze_feature_contributions(self, freq_features: Dict[str, np.ndarray]) -> Dict[str, float]:
        """
        Analisa contribuição de diferentes features para a classificação

        Parameters
        ----------
        freq_features : Dict[str, np.ndarray]
            Features de frequência

        Returns
        -------
        Dict[str, float]
            Contribuição relativa de cada feature
        """

        contributions = {}

        # Contribuições baseadas em padrões conhecidos de EEG
        alpha_power = np.mean(freq_features.get('alpha_power', [0]))
        beta_power = np.mean(freq_features.get('beta_power', [0]))
        theta_power = np.mean(freq_features.get('theta_power', [0]))

        # Padrões associados a diferentes estados
        contributions['alpha_dominance'] = alpha_power / (alpha_power + beta_power + theta_power + 1e-10)
        contributions['beta_dominance'] = beta_power / (alpha_power + beta_power + theta_power + 1e-10)
        contributions['theta_dominance'] = theta_power / (alpha_power + beta_power + theta_power + 1e-10)

        # Razões específicas
        contributions['alpha_beta_ratio'] = np.mean(freq_features.get('alpha_beta_ratio', [1]))

        return contributions

    def detect_epileptic_spikes(self, raw: mne.io.RawArray) -> Dict[str, any]:
        """
        Detecta spikes epileptiformes no EEG

        Parameters
        ----------
        raw : mne.io.RawArray
            Dados EEG

        Returns
        -------
        Dict[str, any]
            Detecção de spikes epileptiformes
        """

        data = raw.get_data()
        spike_detections = []

        # Análise por canal
        for channel_idx, channel_data in enumerate(data):
            channel_name = raw.ch_names[channel_idx]

            # Detecta spikes usando análise morfológica
            spikes = self.detect_spikes_in_channel(channel_data, self.sampling_rate)

            for spike in spikes:
                spike_detections.append({
                    'channel': channel_name,
                    'time': spike['time'],
                    'amplitude': spike['amplitude'],
                    'duration': spike['duration'],
                    'confidence': spike['confidence']
                })

        # Análise de rede usando modelo de deep learning
        network_analysis = self.analyze_spike_network(data, spike_detections)

        return {
            'spike_detections': spike_detections,
            'network_analysis': network_analysis,
            'epilepsy_probability': self.compute_epilepsy_probability(spike_detections, network_analysis)
        }

    def detect_spikes_in_channel(self, channel_data: np.ndarray,
                               sampling_rate: int) -> List[Dict]:
        """
        Detecta spikes em um canal individual

        Parameters
        ----------
        channel_data : np.ndarray
            Dados de um canal EEG
        sampling_rate : int
            Taxa de amostragem

        Returns
        -------
        List[Dict]
            Lista de spikes detectados
        """

        spikes = []

        # Parâmetros de detecção
        threshold_factor = 3.0  # 3 desvios padrão
        min_duration = 20  # ms
        max_duration = 200  # ms

        # Computa threshold dinâmico
        baseline_std = np.std(channel_data)
        threshold = threshold_factor * baseline_std

        # Detecta pontos acima do threshold
        above_threshold = np.abs(channel_data) > threshold

        # Encontra regiões contínuas
        from scipy.ndimage import label
        labeled_regions, num_regions = label(above_threshold)

        for region_id in range(1, num_regions + 1):
            region_mask = labeled_regions == region_id
            region_indices = np.where(region_mask)[0]

            if len(region_indices) > 0:
                start_idx = region_indices[0]
                end_idx = region_indices[-1]
                duration_ms = (end_idx - start_idx) / sampling_rate * 1000

                # Verifica duração
                if min_duration <= duration_ms <= max_duration:
                    amplitude = np.max(np.abs(channel_data[region_indices]))
                    time_sec = start_idx / sampling_rate

                    # Computa confiança baseada na morfologia
                    confidence = self.compute_spike_confidence(channel_data, start_idx, end_idx)

                    spikes.append({
                        'time': time_sec,
                        'amplitude': amplitude,
                        'duration': duration_ms,
                        'confidence': confidence
                    })

        return spikes

    def compute_spike_confidence(self, channel_data: np.ndarray,
                               start_idx: int, end_idx: int) -> float:
        """
        Computa confiança da detecção de spike baseada na morfologia

        Parameters
        ----------
        channel_data : np.ndarray
            Dados do canal
        start_idx, end_idx : int
            Índices de início e fim do spike

        Returns
        -------
        float
            Confiança da detecção (0-1)
        """

        spike_region = channel_data[start_idx:end_idx+1]

        # Critérios morfológicos para spikes epileptiformes
        confidence = 0.0

        # 1. Amplitude (maior = mais provável)
        amplitude = np.max(np.abs(spike_region))
        baseline_std = np.std(channel_data)
        amplitude_score = min(1.0, amplitude / (5 * baseline_std))
        confidence += amplitude_score * 0.3

        # 2. Forma (assimetria sugere spike)
        if len(spike_region) > 3:
            first_half = spike_region[:len(spike_region)//2]
            second_half = spike_region[len(spike_region)//2:]

            asymmetry = abs(np.mean(first_half) - np.mean(second_half)) / (np.std(spike_region) + 1e-10)
            asymmetry_score = min(1.0, asymmetry)
            confidence += asymmetry_score * 0.3

        # 3. Frequência (spikes têm componentes de alta frequência)
        if len(spike_region) > 10:
            # Computa energia em alta frequência (simplificado)
            high_freq_energy = np.var(np.diff(spike_region, n=2))  # Segunda derivada
            total_energy = np.var(spike_region)
            high_freq_ratio = high_freq_energy / (total_energy + 1e-10)
            confidence += min(1.0, high_freq_ratio * 10) * 0.4

        return min(1.0, confidence)

    def analyze_spike_network(self, data: np.ndarray,
                            spike_detections: List[Dict]) -> Dict:
        """
        Analisa rede de spikes epileptiformes

        Parameters
        ----------
        data : np.ndarray
            Dados EEG completos
        spike_detections : List[Dict]
            Spikes detectados

        Returns
        -------
        Dict
            Análise de rede de spikes
        """

        if not spike_detections:
            return {'network_connectivity': 0, 'synchronization': 0}

        # Agrupa spikes por tempo
        time_windows = {}
        window_size = 0.1  # 100ms

        for spike in spike_detections:
            time_key = int(spike['time'] / window_size)
            if time_key not in time_windows:
                time_windows[time_key] = []
            time_windows[time_key].append(spike)

        # Computa sincronização
        synchronization_scores = []
        for time_key, spikes_in_window in time_windows.items():
            if len(spikes_in_window) > 1:
                # Spikes próximos no tempo = maior sincronização
                times = [s['time'] for s in spikes_in_window]
                time_variance = np.var(times)
                sync_score = 1 / (1 + time_variance * 100)  # Normalizado
                synchronization_scores.append(sync_score)

        avg_synchronization = np.mean(synchronization_scores) if synchronization_scores else 0

        # Computa conectividade baseada em spikes simultâneos
        connectivity_score = len([w for w in time_windows.values() if len(w) > 1]) / len(time_windows) if time_windows else 0

        return {
            'network_connectivity': connectivity_score,
            'synchronization': avg_synchronization,
            'spike_clusters': len([w for w in time_windows.values() if len(w) > 1])
        }

    def compute_epilepsy_probability(self, spike_detections: List[Dict],
                                   network_analysis: Dict) -> float:
        """
        Computa probabilidade de epilepsia baseada nos achados

        Parameters
        ----------
        spike_detections : List[Dict]
            Spikes detectados
        network_analysis : Dict
            Análise de rede

        Returns
        -------
        float
            Probabilidade de epilepsia (0-1)
        """

        # Fatores contribuintes
        spike_count = len(spike_detections)
        synchronization = network_analysis.get('synchronization', 0)
        connectivity = network_analysis.get('network_connectivity', 0)

        # Score baseado em evidências clínicas
        probability = 0.0

        # Contagem de spikes
        if spike_count > 10:
            probability += 0.4
        elif spike_count > 5:
            probability += 0.2

        # Sincronização (alta = mais provável epilepsia)
        probability += synchronization * 0.3

        # Conectividade (alta = mais provável epilepsia)
        probability += connectivity * 0.3

        return min(1.0, probability)

# Modelos de Deep Learning para EEG
class EEGMentalStateClassifier(nn.Module):
    """Classificador de estados mentais usando CNN"""

    def __init__(self, n_channels: int = 32, n_classes: int = 4):
        super(EEGMentalStateClassifier, self).__init__()

        self.conv1 = nn.Conv2d(1, 32, kernel_size=(1, 64), stride=(1, 16))
        self.conv2 = nn.Conv2d(32, 64, kernel_size=(n_channels, 1))
        self.conv3 = nn.Conv2d(64, 128, kernel_size=(1, 8))

        self.dropout = nn.Dropout(0.5)
        self.fc1 = nn.Linear(128 * 4, 256)
        self.fc2 = nn.Linear(256, n_classes)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class EpilepticSpikeDetector(nn.Module):
    """Detector de spikes epileptiformes usando LSTM"""

    def __init__(self, n_channels: int = 32, sequence_length: int = 1000):
        super(EpilepticSpikeDetector, self).__init__()

        self.lstm = nn.LSTM(n_channels, 128, num_layers=2, batch_first=True)
        self.fc = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        output = self.fc(lstm_out[:, -1, :])
        return self.sigmoid(output)

class BrainConnectivityAnalyzer(nn.Module):
    """Analisador de conectividade cerebral"""

    def __init__(self, n_channels: int = 32, freq_bands: List[str] = None):
        super(BrainConnectivityAnalyzer, self).__init__()

        if freq_bands is None:
            freq_bands = ['delta', 'theta', 'alpha', 'beta', 'gamma']

        self.n_freq_bands = len(freq_bands)
        self.n_channels = n_channels

        # Encoder para conectividade
        self.encoder = nn.Sequential(
            nn.Linear(n_channels * n_channels * self.n_freq_bands, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128)
        )

    def forward(self, connectivity_tensor):
        # connectivity_tensor: (batch, n_channels, n_channels, n_freq_bands)
        batch_size = connectivity_tensor.size(0)
        x = connectivity_tensor.view(batch_size, -1)
        return self.encoder(x)
```

### 2.2 Análise de Imagens Cerebrais (fMRI, DTI)
**Técnicas Avançadas:**
- Processamento e análise de imagens funcionais
- Rastreamento de feixes de fibras (tractography)
- Análise de conectividade funcional
- Biomarcadores de neuroimagem

```python
# Exemplo: Sistema de análise de fMRI usando deep learning
import nibabel as nib
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from nilearn import image, datasets, input_data
from sklearn.model_selection import train_test_split
from typing import Dict, List, Tuple, Optional

class fMRIAnalysisSystem:
    """Sistema completo de análise de fMRI usando deep learning"""

    def __init__(self, template: str = 'MNI152'):
        self.template = template
        self.setup_preprocessing()
        self.initialize_models()

    def setup_preprocessing(self):
        """Configura pipeline de pré-processamento de fMRI"""

        self.preprocessing_pipeline = {
            'motion_correction': {'method': 'mcflirt'},
            'slice_timing_correction': {'method': 'fugue'},
            'spatial_normalization': {'template': self.template},
            'smoothing': {'fwhm': 6.0},
            'temporal_filtering': {'low_pass': 0.1, 'high_pass': 0.01},
            'confound_regression': ['motion', 'wm', 'csf', 'global_signal']
        }

    def initialize_models(self):
        """Inicializa modelos de deep learning para fMRI"""

        # Modelo para classificação de tarefas
        self.task_classifier = fMRITaskClassifier()

        # Modelo para análise de conectividade
        self.connectivity_analyzer = BrainFunctionalConnectivity()

        # Modelo para detecção de doença
        self.disease_detector = NeurologicalDiseaseDetector()

    def preprocess_fmri_data(self, fmri_file: str, anatomical_file: Optional[str] = None) -> Dict:
        """
        Pré-processa dados de fMRI

        Parameters
        ----------
        fmri_file : str
            Arquivo de fMRI 4D
        anatomical_file : str, optional
            Arquivo de imagem anatômica

        Returns
        -------
        Dict
            Dados pré-processados
        """

        # Carrega imagem fMRI
        fmri_img = nib.load(fmri_file)
        fmri_data = fmri_img.get_fdata()

        processed_data = {
            'original_shape': fmri_data.shape,
            'voxel_size': fmri_img.header.get_zooms(),
            'tr': fmri_img.header['pixdim'][4] if len(fmri_img.header['pixdim']) > 4 else 2.0
        }

        # Correção de movimento
        motion_corrected = self.correct_motion(fmri_data)

        # Normalização espacial
        normalized = self.spatial_normalization(motion_corrected)

        # Suavização
        smoothed = self.smooth_data(normalized, fwhm=6.0)

        # Filtragem temporal
        filtered = self.temporal_filtering(smoothed)

        # Regressão de confundidores
        confounds = self.extract_confounds(fmri_file)
        clean_data = self.regress_confounds(filtered, confounds)

        processed_data.update({
            'motion_corrected': motion_corrected,
            'normalized': normalized,
            'smoothed': smoothed,
            'filtered': filtered,
            'clean_data': clean_data,
            'confounds': confounds
        })

        return processed_data

    def correct_motion(self, fmri_data: np.ndarray) -> np.ndarray:
        """
        Corrige movimento nos dados fMRI

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI 4D (x, y, z, t)

        Returns
        -------
        np.ndarray
            Dados com correção de movimento
        """

        # Implementação simplificada - em prática usaria FSL ou SPM
        # Aqui simulamos correção baseada em correlação máxima

        reference_volume = fmri_data[:, :, :, 0]  # Primeiro volume como referência
        corrected_data = np.copy(fmri_data)

        for t in range(1, fmri_data.shape[3]):
            # Computa transformação rígida (simplificada)
            transformation = self.compute_rigid_transformation(
                reference_volume, fmri_data[:, :, :, t]
            )

            # Aplica transformação
            corrected_data[:, :, :, t] = self.apply_transformation(
                fmri_data[:, :, :, t], transformation
            )

        return corrected_data

    def spatial_normalization(self, fmri_data: np.ndarray) -> np.ndarray:
        """
        Normaliza dados para template padrão

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI

        Returns
        -------
        np.ndarray
            Dados normalizados
        """

        # Implementação simplificada - em prática usaria ANTs ou SPM
        # Aqui aplicamos normalização baseada em histograma

        normalized_data = np.copy(fmri_data)

        # Normaliza intensidade por volume temporal
        for t in range(fmri_data.shape[3]):
            volume = fmri_data[:, :, :, t]
            normalized_data[:, :, :, t] = (volume - np.mean(volume)) / (np.std(volume) + 1e-10)

        return normalized_data

    def smooth_data(self, fmri_data: np.ndarray, fwhm: float) -> np.ndarray:
        """
        Suaviza dados fMRI com filtro gaussiano

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI
        fwhm : float
            Full Width at Half Maximum do filtro gaussiano

        Returns
        -------
        np.ndarray
            Dados suavizados
        """

        from scipy.ndimage import gaussian_filter

        smoothed_data = np.copy(fmri_data)

        # Converte FWHM para sigma
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        sigma_voxels = sigma / np.array([2.0, 2.0, 2.0])  # Assumindo voxels 2mm

        # Aplica filtro gaussiano em cada volume temporal
        for t in range(fmri_data.shape[3]):
            smoothed_data[:, :, :, t] = gaussian_filter(
                fmri_data[:, :, :, t], sigma=sigma_voxels
            )

        return smoothed_data

    def temporal_filtering(self, fmri_data: np.ndarray) -> np.ndarray:
        """
        Aplica filtragem temporal (banda passante)

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI

        Returns
        -------
        np.ndarray
            Dados filtrados temporalmente
        """

        from scipy.signal import butter, filtfilt

        # Filtro passa-banda (0.01 - 0.1 Hz)
        low_freq = 0.01
        high_freq = 0.1
        nyquist = 0.5 / (self.preprocessing_pipeline['temporal_filtering'].get('tr', 2.0) / 1000)

        low = low_freq / nyquist
        high = high_freq / nyquist

        b, a = butter(4, [low, high], btype='band')

        filtered_data = np.copy(fmri_data)

        # Aplica filtro a cada voxel
        for x in range(fmri_data.shape[0]):
            for y in range(fmri_data.shape[1]):
                for z in range(fmri_data.shape[2]):
                    time_series = fmri_data[x, y, z, :]
                    if np.std(time_series) > 0:  # Só filtra se há variação
                        filtered_data[x, y, z, :] = filtfilt(b, a, time_series)

        return filtered_data

    def extract_confounds(self, fmri_file: str) -> np.ndarray:
        """
        Extrai sinais de confundidores (motion, WM, CSF)

        Parameters
        ----------
        fmri_file : str
            Arquivo fMRI

        Returns
        -------
        np.ndarray
            Matriz de confundidores (n_volumes, n_confounds)
        """

        # Implementação simplificada - em prática usaria nilearn
        # Simula extração de sinais de confundidores

        fmri_img = nib.load(fmri_file)
        n_volumes = fmri_img.shape[3]

        # Simula 24 parâmetros de movimento + sinais de tecidos
        n_confounds = 24 + 3  # 6 motion params + derivatives + squares + 3 tissue signals
        confounds = np.random.randn(n_volumes, n_confounds)

        return confounds

    def regress_confounds(self, fmri_data: np.ndarray, confounds: np.ndarray) -> np.ndarray:
        """
        Remove efeito de confundidores usando regressão linear

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI
        confounds : np.ndarray
            Matriz de confundidores

        Returns
        -------
        np.ndarray
            Dados com confundidores removidos
        """

        from sklearn.linear_model import LinearRegression

        clean_data = np.copy(fmri_data)

        # Para cada voxel, remove efeito dos confundidores
        for x in range(fmri_data.shape[0]):
            for y in range(fmri_data.shape[1]):
                for z in range(fmri_data.shape[2]):
                    time_series = fmri_data[x, y, z, :]

                    if np.std(time_series) > 0:
                        # Regressão linear
                        reg = LinearRegression().fit(confounds, time_series)
                        predicted_confounds = reg.predict(confounds)

                        # Remove efeito dos confundidores
                        clean_data[x, y, z, :] = time_series - predicted_confounds

        return clean_data

    def compute_functional_connectivity(self, fmri_data: np.ndarray,
                                      atlas: str = 'harvard_oxford') -> np.ndarray:
        """
        Computa conectividade funcional usando atlas

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI pré-processados
        atlas : str
            Atlas para definição de regiões

        Returns
        -------
        np.ndarray
            Matriz de conectividade funcional
        """

        # Implementação simplificada usando nilearn
        try:
            from nilearn import datasets
            from nilearn.input_data import NiftiLabelsMasker

            # Carrega atlas
            if atlas == 'harvard_oxford':
                atlas_img = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-1mm').maps
            else:
                # Atlas genérico
                atlas_img = None

            if atlas_img:
                # Cria masker
                masker = NiftiLabelsMasker(labels_img=atlas_img, standardize=True)

                # Cria imagem 4D falsa para demonstração
                fake_fmri_img = nib.Nifti1Image(fmri_data, np.eye(4))

                # Extrai sinais das regiões
                time_series = masker.fit_transform(fake_fmri_img)

                # Computa correlação entre regiões
                connectivity_matrix = np.corrcoef(time_series.T)

                return connectivity_matrix
            else:
                # Retorna matriz identidade se atlas não disponível
                n_regions = 100  # Assumindo 100 regiões
                return np.eye(n_regions)

        except ImportError:
            # Fallback se nilearn não estiver disponível
            n_regions = 100
            connectivity_matrix = np.random.randn(n_regions, n_regions)
            connectivity_matrix = (connectivity_matrix + connectivity_matrix.T) / 2
            np.fill_diagonal(connectivity_matrix, 1)
            return connectivity_matrix

    def extract_roi_time_series(self, fmri_data: np.ndarray,
                              roi_mask: np.ndarray) -> np.ndarray:
        """
        Extrai séries temporais de regiões de interesse (ROI)

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI
        roi_mask : np.ndarray
            Máscara 3D da ROI

        Returns
        -------
        np.ndarray
            Série temporal média da ROI
        """

        # Aplica máscara e computa média por volume temporal
        roi_time_series = []

        for t in range(fmri_data.shape[3]):
            volume = fmri_data[:, :, :, t]
            roi_values = volume[roi_mask > 0]
            roi_mean = np.mean(roi_values) if len(roi_values) > 0 else 0
            roi_time_series.append(roi_mean)

        return np.array(roi_time_series)

    def analyze_task_activation(self, fmri_data: np.ndarray,
                              task_design: np.ndarray) -> Dict:
        """
        Analisa ativação cerebral durante tarefa

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI
        task_design : np.ndarray
            Design da tarefa (regressores)

        Returns
        -------
        Dict
            Mapas de ativação e estatísticas
        """

        from scipy.stats import ttest_1samp

        n_volumes = fmri_data.shape[3]
        activation_map = np.zeros(fmri_data.shape[:3])

        # Para cada voxel, testa se há diferença significativa
        for x in range(fmri_data.shape[0]):
            for y in range(fmri_data.shape[1]):
                for z in range(fmri_data.shape[2]):
                    time_series = fmri_data[x, y, z, :]

                    if np.std(time_series) > 0:
                        # Teste t para diferença de médias (task vs baseline)
                        task_volumes = time_series[task_design == 1]
                        baseline_volumes = time_series[task_design == 0]

                        if len(task_volumes) > 0 and len(baseline_volumes) > 0:
                            t_stat, p_value = ttest_1samp(task_volumes - np.mean(baseline_volumes), 0)

                            # Armazena estatística t se significativa
                            if p_value < 0.05:
                                activation_map[x, y, z] = t_stat

        return {
            'activation_map': activation_map,
            'thresholded_map': activation_map * (np.abs(activation_map) > 2.0),  # t > 2.0
            'max_activation': np.max(np.abs(activation_map)),
            'n_activated_voxels': np.sum(np.abs(activation_map) > 2.0)
        }

    def detect_neurological_disorders(self, fmri_data: np.ndarray,
                                    clinical_data: Dict) -> Dict:
        """
        Detecta padrões associados a doenças neurológicas

        Parameters
        ----------
        fmri_data : np.ndarray
            Dados fMRI
        clinical_data : Dict
            Dados clínicos do paciente

        Returns
        -------
        Dict
            Detecção de padrões patológicos
        """

        # Computa conectividade funcional
        connectivity = self.compute_functional_connectivity(fmri_data)

        # Análise usando modelo de deep learning
        with torch.no_grad():
            self.disease_detector.eval()

            # Prepara entrada para o modelo
            connectivity_tensor = torch.FloatTensor(connectivity).unsqueeze(0)
            predictions = self.disease_detector(connectivity_tensor)

            # Interpreta predições
            disease_probabilities = torch.softmax(predictions, dim=1)[0]
            predicted_disease = torch.argmax(disease_probabilities).item()

        disease_names = ['healthy', 'alzheimer', 'parkinson', 'depression', 'anxiety']

        return {
            'predicted_condition': disease_names[predicted_disease],
            'probabilities': {disease_names[i]: disease_probabilities[i].item()
                            for i in range(len(disease_names))},
            'confidence': disease_probabilities[predicted_disease].item(),
            'connectivity_features': self.extract_connectivity_features(connectivity)
        }

    def extract_connectivity_features(self, connectivity_matrix: np.ndarray) -> Dict:
        """
        Extrai features de conectividade para análise

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Matriz de conectividade

        Returns
        -------
        Dict
            Features de conectividade
        """

        features = {}

        # Força média de conexões
        features['mean_connectivity'] = np.mean(np.abs(connectivity_matrix))

        # Modularidade (simplificada)
        features['modularity'] = self.compute_modularity(connectivity_matrix)

        # Eficiência global
        features['global_efficiency'] = self.compute_global_efficiency(connectivity_matrix)

        # Small-worldness
        features['small_worldness'] = self.compute_small_worldness(connectivity_matrix)

        return features

    def compute_modularity(self, connectivity_matrix: np.ndarray) -> float:
        """
        Computa modularidade da rede (simplificada)

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Matriz de conectividade

        Returns
        -------
        float
            Valor de modularidade
        """

        # Implementação simplificada da modularidade de Newman
        n_nodes = connectivity_matrix.shape[0]
        degree = np.sum(np.abs(connectivity_matrix), axis=1)

        # Assumindo comunidades aleatórias para simplificação
        modularity = 0
        for i in range(n_nodes):
            for j in range(n_nodes):
                if i != j:
                    expected = (degree[i] * degree[j]) / np.sum(degree)
                    modularity += connectivity_matrix[i, j] - expected

        modularity /= np.sum(degree)

        return modularity

    def compute_global_efficiency(self, connectivity_matrix: np.ndarray) -> float:
        """
        Computa eficiência global da rede

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Matriz de conectividade

        Returns
        -------
        float
            Eficiência global
        """

        try:
            import networkx as nx

            # Converte para grafo do NetworkX
            G = nx.from_numpy_array(connectivity_matrix)

            # Computa caminho médio mais curto
            avg_shortest_path = nx.average_shortest_path_length(G)

            # Eficiência global = 1 / caminho médio
            global_efficiency = 1 / avg_shortest_path if avg_shortest_path > 0 else 0

            return global_efficiency

        except:
            # Fallback se NetworkX não estiver disponível
            return np.mean(connectivity_matrix)

    def compute_small_worldness(self, connectivity_matrix: np.ndarray) -> float:
        """
        Computa small-worldness da rede

        Parameters
        ----------
        connectivity_matrix : np.ndarray
            Matriz de conectividade

        Returns
        -------
        float
            Medida de small-worldness
        """

        # Implementação simplificada
        # Small-worldness = (clusterização / clusterização_aleatória) / (caminho / caminho_aleatório)

        try:
            import networkx as nx

            G = nx.from_numpy_array(connectivity_matrix)

            # Clusterização
            clustering = nx.average_clustering(G)

            # Caminho médio
            try:
                avg_path = nx.average_shortest_path_length(G)
            except:
                avg_path = 10  # Valor padrão

            # Comparação com rede aleatória (simplificada)
            n_nodes = G.number_of_nodes()
            p_random = nx.density(G)

            # Small-worldness aproximada
            small_worldness = clustering / avg_path if avg_path > 0 else 0

            return small_worldness

        except:
            return 0.5  # Valor neutro

    # Métodos auxiliares
    def compute_rigid_transformation(self, reference: np.ndarray, target: np.ndarray) -> Dict:
        """Computa transformação rígida entre volumes (simplificado)"""
        return {'translation': [0, 0, 0], 'rotation': [0, 0, 0]}

    def apply_transformation(self, volume: np.ndarray, transformation: Dict) -> np.ndarray:
        """Aplica transformação ao volume (simplificado)"""
        return volume

# Modelos de Deep Learning para fMRI
class fMRITaskClassifier(nn.Module):
    """Classificador de tarefas usando CNN 3D"""

    def __init__(self, n_classes: int = 5):
        super(fMRITaskClassifier, self).__init__()

        self.conv3d_1 = nn.Conv3d(1, 32, kernel_size=3, padding=1)
        self.conv3d_2 = nn.Conv3d(32, 64, kernel_size=3, padding=1)
        self.conv3d_3 = nn.Conv3d(64, 128, kernel_size=3, padding=1)

        self.pool = nn.MaxPool3d(2)
        self.dropout = nn.Dropout(0.5)

        # Camada totalmente conectada (ajustar tamanho baseado na entrada)
        self.fc1 = nn.Linear(128 * 8 * 8 * 8, 512)  # Assumindo redução para 8x8x8
        self.fc2 = nn.Linear(512, n_classes)

    def forward(self, x):
        x = torch.relu(self.conv3d_1(x))
        x = self.pool(x)
        x = torch.relu(self.conv3d_2(x))
        x = self.pool(x)
        x = torch.relu(self.conv3d_3(x))
        x = self.pool(x)

        x = x.view(x.size(0), -1)
        x = self.dropout(torch.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

class BrainFunctionalConnectivity(nn.Module):
    """Modelo para análise de conectividade funcional"""

    def __init__(self, n_regions: int = 100):
        super(BrainFunctionalConnectivity, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(n_regions * n_regions, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, 256)
        )

        self.decoder = nn.Sequential(
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, n_regions * n_regions)
        )

    def forward(self, x):
        # x: (batch, n_regions, n_regions)
        batch_size = x.size(0)
        x_flat = x.view(batch_size, -1)

        encoded = self.encoder(x_flat)
        decoded = self.decoder(encoded)
        decoded = decoded.view(batch_size, -1)  # Reconstrução

        return decoded, encoded

class NeurologicalDiseaseDetector(nn.Module):
    """Detector de doenças neurológicas usando conectividade"""

    def __init__(self, n_regions: int = 100, n_diseases: int = 5):
        super(NeurologicalDiseaseDetector, self).__init__()

        self.feature_extractor = nn.Sequential(
            nn.Linear(n_regions * n_regions, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128)
        )

        self.classifier = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, n_diseases)
        )

    def forward(self, x):
        # x: (batch, n_regions, n_regions)
        batch_size = x.size(0)
        x_flat = x.view(batch_size, -1)

        features = self.feature_extractor(x_flat)
        output = self.classifier(features)

        return output
```

---

## 3. HIPÓTESES E RAMIFICAÇÕES PARA DESENVOLVIMENTO

### 3.1 Teoria da Mente e Cognição Social

**Hipótese Principal: Redes Neurais Artificiais Podem Modelar Processos de Teoria da Mente e Cognição Social**

- **Ramificação 1**: Modelos de inferência sobre estados mentais de outros agentes
- **Ramificação 2**: Aprendizagem de hierarquias sociais e normas culturais
- **Ramificação 3**: Simulação de interações sociais complexas

```python
# Exemplo: Sistema de teoria da mente usando reinforcement learning
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np
from typing import Dict, List, Tuple, Optional

class TheoryOfMindAgent(nn.Module):
    """Agente com capacidades de teoria da mente usando RL"""

    def __init__(self, n_agents: int = 3, state_dim: int = 10, action_dim: int = 5):
        super(TheoryOfMindAgent, self).__init__()

        self.n_agents = n_agents
        self.state_dim = state_dim
        self.action_dim = action_dim

        # Rede para modelar estados mentais de outros agentes
        self.belief_updater = nn.Sequential(
            nn.Linear(state_dim + action_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, state_dim)  # Estado mental inferido
        )

        # Rede de política (ator)
        self.policy_network = nn.Sequential(
            nn.Linear(state_dim * (n_agents + 1), 256),  # Próprio estado + crenças sobre outros
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

        # Rede de valor (crítico)
        self.value_network = nn.Sequential(
            nn.Linear(state_dim * (n_agents + 1), 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

        self.beliefs = {}  # Crenças sobre estados mentais de outros agentes

    def update_belief(self, agent_id: int, observed_state: torch.Tensor,
                     observed_action: torch.Tensor):
        """
        Atualiza crença sobre estado mental de outro agente

        Parameters
        ----------
        agent_id : int
            ID do agente observado
        observed_state : torch.Tensor
            Estado observado do agente
        observed_action : torch.Tensor
            Ação observada do agente
        """

        belief_input = torch.cat([observed_state, observed_action])
        updated_belief = self.belief_updater(belief_input)

        self.beliefs[agent_id] = updated_belief

    def select_action(self, current_state: torch.Tensor) -> Tuple[int, torch.Tensor]:
        """
        Seleciona ação considerando crenças sobre outros agentes

        Parameters
        ----------
        current_state : torch.Tensor
            Estado atual do próprio agente

        Returns
        -------
        Tuple[int, torch.Tensor]
            Ação selecionada e log-probabilidade
        """

        # Combina próprio estado com crenças sobre outros
        belief_states = []
        for agent_id in range(self.n_agents):
            if agent_id in self.beliefs:
                belief_states.append(self.beliefs[agent_id])
            else:
                # Crença padrão se não há informação
                belief_states.append(torch.zeros(self.state_dim))

        all_states = torch.cat([current_state] + belief_states)

        # Computa logits da política
        action_logits = self.policy_network(all_states)

        # Amostra ação usando distribuição categórica
        action_dist = Categorical(logits=action_logits)
        action = action_dist.sample()
        log_prob = action_dist.log_prob(action)

        return action.item(), log_prob

    def compute_value(self, state: torch.Tensor) -> torch.Tensor:
        """
        Computa valor do estado considerando crenças sobre outros

        Parameters
        ----------
        state : torch.Tensor
            Estado atual

        Returns
        -------
        torch.Tensor
            Valor estimado do estado
        """

        # Combina estado com crenças
        belief_states = []
        for agent_id in range(self.n_agents):
            belief_states.append(self.beliefs.get(agent_id, torch.zeros(self.state_dim)))

        all_states = torch.cat([state] + belief_states)
        value = self.value_network(all_states)

        return value

    def learn_from_interaction(self, trajectory: List[Dict], gamma: float = 0.99):
        """
        Aprende com interações usando PPO (Proximal Policy Optimization)

        Parameters
        ----------
        trajectory : List[Dict]
            Trajetória de interações
        gamma : float
            Fator de desconto
        """

        optimizer = optim.Adam(self.parameters(), lr=3e-4)

        # Computa vantagens
        advantages = self.compute_advantages(trajectory, gamma)

        # Otimização da política e valor
        for _ in range(10):  # Múltiplas épocas
            for i, step in enumerate(trajectory):
                # Computa nova política
                _, new_log_prob = self.select_action(step['state'])

                # Ratio de probabilidade
                ratio = torch.exp(new_log_prob - step['log_prob'])

                # Clipping do PPO
                clipped_ratio = torch.clamp(ratio, 0.8, 1.2)

                # Loss da política
                policy_loss = -torch.min(ratio * advantages[i],
                                       clipped_ratio * advantages[i]).mean()

                # Loss do valor
                value_pred = self.compute_value(step['state'])
                value_loss = (value_pred - step['return']).pow(2).mean()

                # Loss total
                total_loss = policy_loss + 0.5 * value_loss

                # Otimização
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

    def compute_advantages(self, trajectory: List[Dict], gamma: float) -> List[float]:
        """
        Computa vantagens usando GAE (Generalized Advantage Estimation)

        Parameters
        ----------
        trajectory : List[Dict]
            Trajetória de estados, ações e recompensas
        gamma : float
            Fator de desconto

        Returns
        -------
        List[float]
            Vantagens para cada passo
        """

        advantages = []
        gae = 0
        next_value = 0

        for step in reversed(trajectory):
            if step.get('done', False):
                next_value = 0
                gae = 0

            delta = step['reward'] + gamma * next_value - step['value']
            gae = delta + gamma * 0.95 * gae  # Lambda = 0.95

            advantages.insert(0, gae)
            next_value = step['value']

        return advantages

    def simulate_social_interaction(self, n_steps: int = 100) -> Dict:
        """
        Simula interação social entre agentes com teoria da mente

        Parameters
        ----------
        n_steps : int
            Número de passos da simulação

        Returns
        -------
        Dict
            Resultados da simulação social
        """

        # Estados iniciais
        agent_states = [torch.randn(self.state_dim) for _ in range(self.n_agents + 1)]

        # Histórico de interações
        interaction_history = []
        cooperation_scores = []

        for step in range(n_steps):
            actions = []
            rewards = []

            # Cada agente seleciona ação
            for agent_id in range(self.n_agents + 1):
                if agent_id == 0:  # Agente principal (com ToM)
                    action, _ = self.select_action(agent_states[agent_id])
                else:
                    # Outros agentes: política simples
                    action = np.random.choice(self.action_dim)

                actions.append(action)

            # Computa recompensas baseadas em cooperação
            rewards = self.compute_social_rewards(actions, agent_states)

            # Atualiza crenças do agente principal
            for agent_id in range(1, self.n_agents + 1):
                self.update_belief(agent_id, agent_states[agent_id],
                                 torch.tensor([actions[agent_id]], dtype=torch.float))

            # Atualiza estados baseado em ações
            for agent_id in range(self.n_agents + 1):
                agent_states[agent_id] = self.update_agent_state(
                    agent_states[agent_id], actions[agent_id], rewards[agent_id]
                )

            # Registra interação
            interaction = {
                'step': step,
                'actions': actions,
                'rewards': rewards,
                'cooperation_score': np.mean(rewards)
            }
            interaction_history.append(interaction)
            cooperation_scores.append(np.mean(rewards))

        return {
            'interaction_history': interaction_history,
            'final_cooperation_score': np.mean(cooperation_scores[-20:]),  # Últimos 20 passos
            'belief_evolution': dict(self.beliefs),
            'social_learning_curve': cooperation_scores
        }

    def compute_social_rewards(self, actions: List[int], states: List[torch.Tensor]) -> List[float]:
        """
        Computa recompensas baseadas em interações sociais

        Parameters
        ----------
        actions : List[int]
            Ações de todos os agentes
        states : List[torch.Tensor]
            Estados de todos os agentes

        Returns
        -------
        List[float]
            Recompensas para cada agente
        """

        rewards = []

        for i, action in enumerate(actions):
            reward = 0

            # Recompensa por cooperação
            for j, other_action in enumerate(actions):
                if i != j:
                    # Cooperação aumenta recompensa
                    if action == other_action:  # Mesmo tipo de ação = cooperação
                        reward += 0.5
                    else:
                        reward -= 0.1

            # Recompensa por eficiência individual
            efficiency = torch.mean(states[i]).item()
            reward += efficiency * 0.3

            rewards.append(reward)

        return rewards

    def update_agent_state(self, state: torch.Tensor, action: int, reward: float) -> torch.Tensor:
        """
        Atualiza estado do agente baseado em ação e recompensa

        Parameters
        ----------
        state : torch.Tensor
            Estado atual
        action : int
            Ação executada
        reward : float
            Recompensa recebida

        Returns
        -------
        torch.Tensor
            Novo estado
        """

        # Atualização simples do estado
        state_update = torch.randn(self.state_dim) * 0.1
        state_update[action] += reward * 0.2  # Reforço da ação bem-sucedida

        new_state = state + state_update

        # Mantém estado dentro de limites
        new_state = torch.clamp(new_state, -2, 2)

        return new_state

    def predict_other_agent_action(self, agent_id: int, context: Dict) -> Dict:
        """
        Prediz ação que outro agente tomaria baseado em crenças

        Parameters
        ----------
        agent_id : int
            ID do agente
        context : Dict
            Contexto da situação

        Returns
        -------
        Dict
            Predição de ação e confiança
        """

        if agent_id not in self.beliefs:
            return {'predicted_action': np.random.choice(self.action_dim),
                   'confidence': 0.5}

        # Usa crença sobre estado mental para predizer ação
        belief_state = self.beliefs[agent_id]

        # Simula tomada de decisão do outro agente
        action_logits = self.policy_network(
            torch.cat([belief_state] + [torch.zeros(self.state_dim)] * self.n_agents)
        )

        predicted_action = torch.argmax(action_logits).item()
        confidence = torch.max(torch.softmax(action_logits, dim=0)).item()

        return {
            'predicted_action': predicted_action,
            'confidence': confidence,
            'belief_state': belief_state.detach().numpy()
        }

    def evaluate_social_intelligence(self, test_scenarios: List[Dict]) -> Dict:
        """
        Avalia inteligência social do agente

        Parameters
        ----------
        test_scenarios : List[Dict]
            Cenários de teste social

        Returns
        -------
        Dict
            Avaliação de inteligência social
        """

        social_scores = []

        for scenario in test_scenarios:
            # Testa predição de ações de outros agentes
            predictions = []
            for agent_id in scenario['other_agents']:
                prediction = self.predict_other_agent_action(agent_id, scenario['context'])
                predictions.append(prediction)

            # Computa acurácia das predições
            correct_predictions = 0
            for pred, actual in zip(predictions, scenario['actual_actions']):
                if pred['predicted_action'] == actual:
                    correct_predictions += 1

            accuracy = correct_predictions / len(predictions)
            social_scores.append(accuracy)

        return {
            'mean_social_accuracy': np.mean(social_scores),
            'social_iq_score': np.mean(social_scores) * 100,  # Escala 0-100
            'test_scenarios_evaluated': len(test_scenarios),
            'social_learning_trajectory': social_scores
        }

    def demonstrate_empathy(self, observed_situation: Dict) -> Dict:
        """
        Demonstra capacidade de empatia simulando resposta emocional

        Parameters
        ----------
        observed_situation : Dict
            Situação observada de outro agente

        Returns
        -------
        Dict
            Resposta empática simulada
        """

        # Simula processamento emocional
        emotional_state = observed_situation.get('emotional_state', 'neutral')
        context = observed_situation.get('context', {})

        # Modelo simplificado de empatia
        empathy_response = {
            'recognized_emotion': emotional_state,
            'empathy_level': self.compute_empathy_level(emotional_state, context),
            'suggested_action': self.select_empathetic_action(emotional_state),
            'emotional_contagion': self.simulate_emotional_contagion(emotional_state)
        }

        return empathy_response

    def compute_empathy_level(self, emotion: str, context: Dict) -> float:
        """
        Computa nível de empatia baseado na emoção e contexto

        Parameters
        ----------
        emotion : str
            Emoção observada
        context : Dict
            Contexto da situação

        Returns
        -------
        float
            Nível de empatia (0-1)
        """

        # Modelo simplificado de empatia
        empathy_base = {
            'joy': 0.8,
            'sadness': 0.9,
            'anger': 0.6,
            'fear': 0.85,
            'surprise': 0.7,
            'neutral': 0.5
        }

        base_empathy = empathy_base.get(emotion, 0.5)

        # Ajusta baseado em contexto
        if context.get('similar_experience', False):
            base_empathy += 0.1
        if context.get('close_relationship', False):
            base_empathy += 0.1

        return min(1.0, base_empathy)

    def select_empathetic_action(self, emotion: str) -> str:
        """
        Seleciona ação empática apropriada

        Parameters
        ----------
        emotion : str
            Emoção observada

        Returns
        -------
        str
            Ação empática sugerida
        """

        empathetic_actions = {
            'joy': 'compartilhar_entusiasmo',
            'sadness': 'oferecer_suporte_emocional',
            'anger': 'dar_espaco_para_processar',
            'fear': 'proporcionar_seguranca',
            'surprise': 'expressar_solidariedade',
            'neutral': 'manter_atencao_neutra'
        }

        return empathetic_actions.get(emotion, 'manter_presenca')

    def simulate_emotional_contagion(self, emotion: str) -> Dict:
        """
        Simula contágio emocional

        Parameters
        ----------
        emotion : str
            Emoção observada

        Returns
        -------
        Dict
            Efeitos de contágio emocional
        """

        contagion_effects = {
            'joy': {'own_emotion': 'happy', 'intensity': 0.6},
            'sadness': {'own_emotion': 'concerned', 'intensity': 0.7},
            'anger': {'own_emotion': 'cautious', 'intensity': 0.5},
            'fear': {'own_emotion': 'anxious', 'intensity': 0.8},
            'surprise': {'own_emotion': 'curious', 'intensity': 0.4},
            'neutral': {'own_emotion': 'neutral', 'intensity': 0.2}
        }

        return contagion_effects.get(emotion, {'own_emotion': 'neutral', 'intensity': 0.0})
```

---

## 4. FERRAMENTAS E BIBLIOTECAS ESSENCIAIS

### 4.1 Bibliotecas de Neurociência Computacional
```python
# Configuração recomendada para neurociência computacional
# requirements.txt
brian2==2.5.1
mne==1.4.0
nilearn==0.10.1
nibabel==5.1.0
scipy==1.11.1
numpy==1.24.3
matplotlib==3.7.2
seaborn==0.12.2
torch==2.0.1
torchvision==0.15.2
networkx==3.1
scikit-learn==1.3.0
pandas==2.0.3
```

### 4.2 Plataformas e Bases de Dados
- **Human Connectome Project**: Dados de conectividade cerebral
- **OpenNeuro**: Banco de dados de neuroimagem
- **Allen Brain Atlas**: Atlas cerebral detalhado
- **BrainMap**: Meta-análises de neuroimagem

### 4.3 Ferramentas de Simulação
- **Brian2**: Simulação de redes neurais
- **NEURON**: Modelagem detalhada de neurônios
- **NEST**: Simulação de redes neurais em larga escala

---

## 5. METODOLOGIA DE DESENVOLVIMENTO

### 5.1 Pipeline de Pesquisa em Neurociência Computacional
1. **Formulação de Hipóteses**: Baseado em conhecimento neurocientífico
2. **Implementação de Modelos**: Simulações computacionais
3. **Validação Biológica**: Comparação com dados experimentais
4. **Iteração e Refinamento**: Aprendizado com dados reais
5. **Tradução Clínica**: Aplicações práticas em saúde mental

### 5.2 Validação e Reprodutibilidade
- **Comparação com Dados Experimentais**: EEG, fMRI, dados comportamentais
- **Métricas de Performance**: Correlação com atividade neural real
- **Reprodutibilidade**: Compartilhamento de código e parâmetros
- **Validação Cruzada**: Testes em diferentes populações

---

## 6. EXERCÍCIOS PRÁTICOS E PROJETOS

### 6.1 Projeto Iniciante: Modelagem de Neurônio Individual
**Objetivo**: Implementar e simular modelo de neurônio AdEx
**Dificuldade**: Baixa
**Tempo estimado**: 2-3 horas

### 6.2 Projeto Intermediário: Análise de EEG
**Objetivo**: Processar e classificar sinais de EEG
**Dificuldade**: Média
**Tempo estimado**: 4-6 horas

### 6.3 Projeto Avançado: Rede Neural com Plasticidade
**Objetivo**: Implementar rede com STDP e plasticidade
**Dificuldade**: Alta
**Tempo estimado**: 8-12 horas

### 6.4 Projeto Especializado: Modelo de Doença Neural
**Objetivo**: Simular alterações em modelo de doença
**Dificuldade**: Muito Alta
**Tempo estimado**: 15+ horas

---

## 7. RECURSOS ADICIONAIS PARA APRENDIZADO

### 7.1 Livros Recomendados
- "Theoretical Neuroscience" - Peter Dayan & L.F. Abbott
- "Biophysical Neural Computation" - Thomas Schilcker
- "An Introduction to Neural Information Processing" - Pejić
- "Dynamical Systems in Neuroscience" - Eugene Izhikevich

### 7.2 Cursos Online
- Coursera: Computational Neuroscience Specialization
- edX: Introduction to Computational Neuroscience
- Coursera: Neural Networks for Machine Learning

### 7.3 Comunidades e Fóruns
- Neuromatch Academy (cursos intensivos)
- Computational Neuroscience Discussion
- Brian2 User Forum
- Neuromorpho.org (morfologia neuronal)

---

## Conclusão

Este documento estabelece uma base sólida para o desenvolvimento de modelos de IA especializados em neurociência computacional. A ênfase está na integração entre princípios fundamentais da neurobiologia, técnicas computacionais avançadas e validação experimental rigorosa.

**Princípios Orientadores:**
1. **Precisão Biológica**: Modelos devem capturar princípios fundamentais da neurobiologia
2. **Escalabilidade Computacional**: Equilibrar complexidade biológica com recursos computacionais
3. **Validação Experimental**: Comparação sistemática com dados neurofisiológicos
4. **Interdisciplinaridade**: Integração entre neurociência, computação e psicologia
5. **Aplicações Clínicas**: Tradução de descobertas para saúde mental e neurológica

A combinação de modelagem computacional rigorosa com validação experimental permite não apenas entender melhor o funcionamento do cérebro, mas também desenvolver aplicações práticas em diagnóstico, tratamento e reabilitação de doenças neurológicas.

**Próximas Etapas de Desenvolvimento:**
1. Validação extensiva com dados experimentais reais
2. Desenvolvimento de modelos em larga escala
3. Integração com técnicas de neuroimagem avançada
4. Aplicações em medicina de precisão neurológica
5. Interfaces cérebro-computador para reabilitação

**O caminho à frente:**
🌍 **Ecologia Computacional** - Sistemas ambientais inteligentes
⚡ **Energia Sustentável** - Transição energética otimizada
🏗️ **Engenharia Civil Inteligente** - Infraestrutura smart

Continuando a jornada de descoberta através da interseção entre inteligência artificial e compreensão profunda do cérebro humano! 🧠🔬✨

Com este marco de 5 especializações concluídas, estabelecemos um alicerce robusto para a expansão sistemática do conhecimento em IA aplicada a diferentes domínios científicos e tecnológicos. A neurociência computacional representa um avanço significativo, abrindo portas para a compreensão dos processos cognitivos mais fundamentais da mente humana.

Cada especialização construída não apenas demonstra a versatilidade da IA, mas também revela insights profundos sobre como diferentes campos científicos podem se beneficiar mutuamente através de abordagens computacionais inovadoras. A jornada continua com entusiasmo e curiosidade intelectual! 🚀🧠💡
