
import time
import random

class YantraComponent:
    """
    Componente base de um Yantra (Máquina de Bhoja).
    Pode ser uma engrenagem, uma corda (Sutra) ou uma câmara de ar.
    """
    def __init__(self, name, state=0):
        self.name = name
        self.state = state # 0 (Parado), 1 (Ativo)

    def transmit(self, input_energy):
        # A física da transmissão mecânica (Perda de entropia)
        # Eficiência de 90%
        return input_energy * 0.9

class Automaton(YantraComponent):
    """
    O Robô (Putrika). Uma Máquina de Estados Finitos (FSM).
    """
    def __init__(self, role):
        super().__init__(role)
        self.triggers = [] # Sensores (Bija)
    
    def add_trigger(self, condition_func, action_func):
        self.triggers.append((condition_func, action_func))

    def update(self, environment_input):
        """O Ciclo de Clock do Autômato"""
        print(f"[{self.name}] Analisando Input: {environment_input}")
        found_trigger = False
        for condition, action in self.triggers:
            if condition(environment_input):
                print(f"[{self.name}] CONDIÇÃO ATIVADA! Executando ação...")
                action()
                found_trigger = True
                break # FSM geralmente executa uma transição por vez
        
        if not found_trigger:
            print(f"[{self.name}] Nenhuma ação disparada. Estado de espera.")

# CENÁRIO: O Porteiro Mecânico de Bhoja
# Descrição: "Um guarda que impede a entrada de quem não sabe a senha (peso/toque)"

def simulation_gatekeeper():
    print("--- SIMULAÇÃO: O PORTEIRO DE BHOJA (Cap. 31) ---")
    print("Objetivo: Validar que lógica complexa emerge de componentes mecânicos simples (FSM).")
    
    # Estado do Sistema
    door_state = "FECHADA"
    
    # O Robô
    dvarapala = Automaton("Guarda Mecânico")
    
    # Lógica (Programação Mecânica via Engrenagens/Válvulas)
    # 1. Sensor de Peso (Bija de Pressão)
    # 2. Chave de Segurança (Kila/Pino)
    
    def check_friend(env):
        # Amigo: Tem o peso correto E sabe o segredo (apertou o pino)
        return env.get('weight', 0) > 50 and env.get('knows_secret', False)
    
    def check_foe(env):
        # Inimigo: Tem peso (humano) MAS não sabe o segredo
        return env.get('weight', 0) > 50 and not env.get('knows_secret', False)
    
    def action_welcome():
        nonlocal door_state
        door_state = "ABERTA"
        print(">> Ação Mecânica: Válvula Hidráulica Abertura. Contra-peso desce.")
        print(f"   [STATUS PORTA]: {door_state}")

    def action_attack():
        print(">> Ação Mecânica: Mola Comprimida Liberada. Lança Disparada!")
        print("   [STATUS ALERTA]: INTRUSO DETECTADO")
        
    dvarapala.add_trigger(check_friend, action_welcome)
    dvarapala.add_trigger(check_foe, action_attack)
    
    # Teste 1: Inimigo (Soldado Invasor)
    print("\n[Teste 1] Invasor se aproxima...")
    env_enemy = {'weight': 85, 'knows_secret': False}
    dvarapala.update(env_enemy)
    
    # Teste 2: Rei Bhoja (Autorizado)
    print("\n[Teste 2] Rei Bhoja se aproxima...")
    env_friend = {'weight': 75, 'knows_secret': True}
    dvarapala.update(env_friend)
    
    # Teste 3: Animal Pequeno (Ruído)
    print("\n[Teste 3] Gato passa pelo sensor...")
    env_noise = {'weight': 5, 'knows_secret': False}
    dvarapala.update(env_noise)

if __name__ == "__main__":
    simulation_gatekeeper()
