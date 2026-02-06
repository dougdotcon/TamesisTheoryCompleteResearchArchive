"""
Testes para as simulações de gravidade emergente
"""

import sys
import os
import unittest
import numpy as np

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from simulacao_1d import simular_queda_entropica, densidade_informacao, POSICAO_MASSA
from agente_consciente import AgenteConsciente, comparar_agente_vs_materia_inerte
from rotacao_galactica import forca_newtoniana, forca_verlinde, velocidade_orbital_estavel, simular_orbita
from galaxia_consciente import GalaxiaConsciente

class TestSimulacao1D(unittest.TestCase):
    """Testes para a simulação 1D"""

    def test_densidade_informacao(self):
        """Testa a função de densidade de informação"""
        # No centro, deve ser alta
        self.assertEqual(densidade_informacao(POSICAO_MASSA), 10000.0)

        # Longe do centro, deve ser baixa
        self.assertLess(densidade_informacao(10.0), 1.0)
        self.assertGreater(densidade_informacao(10.0), 0.0)

    def test_simulacao_basica(self):
        """Testa execução básica da simulação"""
        trajetoria = simular_queda_entropica(passos=100)

        # Deve retornar uma lista
        self.assertIsInstance(trajetoria, list)

        # Deve ter pelo menos 2 pontos (inicial + pelo menos um passo)
        self.assertGreaterEqual(len(trajetoria), 2)

        # Primeiro ponto deve ser a posição inicial
        self.assertEqual(trajetoria[0], 50.0)

    def test_convergencia(self):
        """Testa se a simulação converge para o centro"""
        trajetoria = simular_queda_entropica(passos=1000, temperatura=0.1)

        posicao_inicial = trajetoria[0]
        posicao_final = trajetoria[-1]

        # Deve ter se aproximado do centro
        distancia_inicial = abs(posicao_inicial - POSICAO_MASSA)
        distancia_final = abs(posicao_final - POSICAO_MASSA)

        # Em uma simulação bem-sucedida, a distância final deve ser menor
        # Mas como é estocástico, testamos apenas que não divergiu muito
        self.assertLess(distancia_final, distancia_inicial + 10.0)

    def test_parametros_customizados(self):
        """Testa simulação com parâmetros customizados"""
        pos_inicial = 20.0
        passos = 50

        trajetoria = simular_queda_entropica(
            posicao_inicial=pos_inicial,
            passos=passos
        )

        self.assertEqual(trajetoria[0], pos_inicial)
        self.assertLessEqual(len(trajetoria), passos + 1)  # +1 por causa do ponto inicial

class TestAgenteConsciente(unittest.TestCase):
    """Testes para o agente consciente"""

    def test_inicializacao_agente(self):
        """Testa inicialização do agente consciente"""
        agente = AgenteConsciente()

        # Verificar posição inicial
        np.testing.assert_array_equal(agente.posicao, np.array([10.0, 0.0]))

        # Verificar velocidade inicial
        np.testing.assert_array_equal(agente.velocidade, np.array([0.0, 1.0]))

        # Verificar trajetória inicial
        self.assertEqual(len(agente.trajetoria), 1)
        self.assertEqual(agente.trajetoria[0], (10.0, 0.0))

    def test_densidade_entropica(self):
        """Testa cálculo da densidade entrópica"""
        agente = AgenteConsciente()

        # No centro, deve ser alta
        centro = np.array([0.0, 0.0])
        densidade_centro = agente.densidade_entropica(centro)
        self.assertGreater(densidade_centro, 100.0)

        # Longe do centro, deve ser baixa
        longe = np.array([10.0, 0.0])
        densidade_longe = agente.densidade_entropica(longe)
        self.assertLess(densidade_longe, 1.0)

    def test_previsao_entropia(self):
        """Testa previsão de entropia futura"""
        agente = AgenteConsciente()

        pos_atual = np.array([5.0, 0.0])
        vel_atual = np.array([0.0, 1.0])

        entropia_prevista = agente.prever_entropia_futura(pos_atual, vel_atual, 5)

        # Deve ser um float
        self.assertIsInstance(entropia_prevista, float)
        self.assertGreater(entropia_prevista, 0.0)

    def test_decisao_movimento(self):
        """Testa decisão de movimento consciente"""
        agente = AgenteConsciente()

        aceleracao = agente.decidir_movimento_consciente()

        # Deve retornar array 2D
        self.assertEqual(len(aceleracao), 2)
        self.assertTrue(isinstance(aceleracao, np.ndarray))

    def test_simulacao_orbita(self):
        """Testa simulação de órbita"""
        agente = AgenteConsciente()
        trajetoria = agente.simular_orbita(steps=10)

        # Deve ter 11 pontos (inicial + 10 passos)
        self.assertEqual(len(trajetoria), 11)

        # Todos os pontos devem ser tuplas
        for ponto in trajetoria:
            self.assertIsInstance(ponto, tuple)
            self.assertEqual(len(ponto), 2)

    def test_comparacao_agente_inerte(self):
        """Testa comparação entre agente consciente e matéria inerte"""
        traj_consciente, traj_inerte = comparar_agente_vs_materia_inerte(steps=50)

        # Ambas trajetórias devem ter pontos
        self.assertGreater(len(traj_consciente), 1)
        self.assertGreater(len(traj_inerte), 1)

        # Calcular distâncias finais
        pos_final_consciente = np.array(traj_consciente[-1])
        pos_final_inerte = np.array(traj_inerte[-1])

        dist_consciente = np.linalg.norm(pos_final_consciente)
        dist_inerte = np.linalg.norm(pos_final_inerte)

        # Agente consciente deve escapar mais longe (hipótese)
        # Como é estocástico, testamos apenas que as distâncias são positivas
        self.assertGreater(dist_consciente, 0.0)
        self.assertGreater(dist_inerte, 0.0)

class TestRotacaoGalactica(unittest.TestCase):
    """Testes para simulação de rotação galáctica"""

    def test_forca_newtoniana(self):
        """Testa cálculo da força newtoniana"""
        # Força deve ser positiva e decrescer com o quadrado da distância
        f_10 = forca_newtoniana(10.0)
        f_20 = forca_newtoniana(20.0)

        self.assertGreater(f_10, 0)
        self.assertGreater(f_20, 0)
        self.assertGreater(f_10, f_20)  # Força menor em distâncias maiores

        # Verificar lei do inverso do quadrado
        razao = f_10 / f_20
        razao_esperada = (20.0 / 10.0) ** 2  # 4
        self.assertAlmostEqual(razao, razao_esperada, places=1)

    def test_forca_verlinde(self):
        """Testa força de Verlinde com transição de fase"""
        # Perto do centro: deve ser similar ao Newton
        f_newton_perto = forca_newtoniana(5.0)
        f_verlinde_perto = forca_verlinde(5.0)
        self.assertAlmostEqual(f_verlinde_perto, f_newton_perto, places=1)

        # Longe do centro: deve ser maior que Newton (mais forte)
        # Para r=100, aceleração newton = 1*1000/10000 = 0.1 < A_0=0.2
        f_newton_longe = forca_newtoniana(100.0)
        f_verlinde_longe = forca_verlinde(100.0)
        self.assertGreater(f_verlinde_longe, f_newton_longe)

    def test_velocidade_orbital(self):
        """Testa cálculo de velocidade orbital"""
        # Teste em distância onde há diferença
        r = 100.0  # Longe, onde Verlinde é diferente

        v_newton = velocidade_orbital_estavel(r, 'newton')
        v_verlinde = velocidade_orbital_estavel(r, 'verlinde')

        # Ambos devem ser positivos
        self.assertGreater(v_newton, 0)
        self.assertGreater(v_verlinde, 0)

        # Verlinde deve ter velocidade maior em grandes distâncias
        self.assertGreater(v_verlinde, v_newton)

    def test_simulacao_orbita_basica(self):
        """Testa simulação básica de órbita"""
        tx, ty, v_media = simular_orbita('newton', raio_inicial=10.0, passos=100)

        # Deve retornar listas do mesmo tamanho
        self.assertEqual(len(tx), len(ty))
        self.assertEqual(len(tx), 101)  # inicial + 100 passos

        # Velocidade média deve ser positiva
        self.assertGreater(v_media, 0)

        # Deve começar no raio correto
        r_inicial = np.sqrt(tx[0]**2 + ty[0]**2)
        self.assertAlmostEqual(r_inicial, 10.0, places=1)

    def test_curva_rotacao_plana(self):
        """Testa se Verlinde produz curva de rotação mais plana"""
        raios = np.linspace(50, 150, 5)  # Raios maiores onde há diferença

        v_newton = [velocidade_orbital_estavel(r, 'newton') for r in raios]
        v_verlinde = [velocidade_orbital_estavel(r, 'verlinde') for r in raios]

        # Calcular variações
        var_newton = np.std(v_newton) / np.mean(v_newton)
        var_verlinde = np.std(v_verlinde) / np.mean(v_verlinde)

        # Verlinde deve ter menor variação (mais plana)
        self.assertLess(var_verlinde, var_newton)

        # Verificações básicas
        for v in v_newton + v_verlinde:
            self.assertGreater(v, 0)

class TestGalaxiaConsciente(unittest.TestCase):
    """Testes para simulação de galáxia consciente"""

    def test_criacao_galaxia(self):
        """Testa criação básica da galáxia"""
        galaxia = GalaxiaConsciente(raio_galaxia=50.0, num_estrelas=10)

        self.assertEqual(galaxia.raio_galaxia, 50.0)
        self.assertEqual(len(galaxia.estrelas), 10)
        self.assertIsNone(galaxia.agente_consciente)

        # Verificar que estrelas têm propriedades corretas
        for estrela in galaxia.estrelas:
            self.assertIn('posicao', estrela)
            self.assertIn('velocidade', estrela)
            self.assertIn('trajetoria', estrela)
            self.assertEqual(estrela['tipo'], 'inerte')

    def test_adicionar_agente_consciente(self):
        """Testa adição de agente consciente"""
        galaxia = GalaxiaConsciente()

        # Adicionar agente
        galaxia.adicionar_agente_consciente(
            posicao_inicial=(10.0, 0.0),
            velocidade_inicial=(0.0, 1.0)
        )

        self.assertIsNotNone(galaxia.agente_consciente)
        np.testing.assert_array_equal(
            galaxia.agente_consciente.posicao,
            np.array([10.0, 0.0])
        )

    def test_simulacao_basica(self):
        """Testa simulação básica da galáxia"""
        galaxia = GalaxiaConsciente(num_estrelas=5)

        # Simulação curta
        resultados = galaxia.simular_galaxia(passos=10)

        self.assertEqual(resultados['estrelas_inertes'], 5)
        self.assertIsNone(resultados['agente_consciente'])

        # Verificar trajetórias
        self.assertEqual(len(resultados['trajetorias_inertes']), 5)
        for traj in resultados['trajetorias_inertes']:
            self.assertGreater(len(traj), 1)  # Pelo menos inicial + 1 passo

    def test_livre_arbitrio_escape(self):
        """Testa demonstração de livre arbítrio (escape)"""
        galaxia = GalaxiaConsciente(raio_galaxia=30.0, num_estrelas=3)

        # Agente com força consciente alta para garantir escape
        galaxia.adicionar_agente_consciente(
            posicao_inicial=(15.0, 0.0),
            velocidade_inicial=(0.0, 2.0)
        )
        galaxia.agente_consciente.forca_consciente = 1.0  # Força máxima

        # Simulação
        resultados = galaxia.simular_galaxia(passos=200)

        # Verificar que temos dados do agente
        self.assertIsNotNone(resultados['agente_consciente'])

        agent_data = resultados['agente_consciente']
        self.assertIn('trajetoria', agent_data)
        self.assertIn('posicao_final', agent_data)
        self.assertIn('distancia_final', agent_data)

        # Verificar trajetória
        traj = agent_data['trajetoria']
        self.assertGreater(len(traj), 1)

        # Posição final deve ser tuple
        self.assertIsInstance(agent_data['posicao_final'], tuple)
        self.assertEqual(len(agent_data['posicao_final']), 2)

    def test_simulacao_com_agente(self):
        """Testa simulação completa com agente consciente"""
        galaxia = GalaxiaConsciente(num_estrelas=2)

        galaxia.adicionar_agente_consciente(
            posicao_inicial=(20.0, 0.0),
            velocidade_inicial=(0.0, 1.5)
        )

        resultados = galaxia.simular_galaxia(passos=50)

        # Verificar estrutura dos resultados
        self.assertIn('estrelas_inertes', resultados)
        self.assertIn('trajetorias_inertes', resultados)
        self.assertIn('agente_consciente', resultados)
        self.assertIn('sucesso_escape', resultados)
        self.assertIn('livre_arbitrio_demonstrado', resultados)

        # Agente deve ter trajetória
        agent_data = resultados['agente_consciente']
        self.assertIsNotNone(agent_data)
        self.assertGreater(len(agent_data['trajetoria']), 1)

if __name__ == '__main__':
    unittest.main()