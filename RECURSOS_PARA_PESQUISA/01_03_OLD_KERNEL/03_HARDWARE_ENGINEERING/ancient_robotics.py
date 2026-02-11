
import time
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class YantraComponent:
    def __init__(self, name, state=0):
        self.name = name
        self.state = state

class Automaton(YantraComponent):
    def __init__(self, role):
        super().__init__(role)
        self.triggers = []
        self.state_log = [] # Time, StateLabel
        self.time_step = 0
    
    def add_trigger(self, condition_func, action_func, state_label):
        self.triggers.append((condition_func, action_func, state_label))

    def update(self, environment_input):
        self.time_step += 1
        found_action = False
        current_state = "IDLE"
        
        for condition, action, label in self.triggers:
            if condition(environment_input):
                action()
                current_state = label
                found_action = True
                break 
        
        self.state_log.append((self.time_step, current_state))
        return current_state

def simulation_gatekeeper_visual():
    print("--- SIMULAÇÃO: AUTOMATON FSM LOGGING ---")
    
    dvarapala = Automaton("Guarda Mecânico")
    
    # Lógica
    def check_friend(env): return env.get('weight', 0) > 50 and env.get('knows_secret', False)
    def check_foe(env): return env.get('weight', 0) > 50 and not env.get('knows_secret', False)
    def check_noise(env): return env.get('weight', 0) <= 50
    
    def action_open(): print(f"[{dvarapala.time_step}] OPEN DOOR")
    def action_attack(): print(f"[{dvarapala.time_step}] ATTACK!")
    def action_wait(): print(f"[{dvarapala.time_step}] Waiting...")
    
    dvarapala.add_trigger(check_friend, action_open, "OPEN")
    dvarapala.add_trigger(check_foe, action_attack, "ATTACK")
    dvarapala.add_trigger(check_noise, action_wait, "IDLE") # Default implicit
    
    # Scenario Sequence
    inputs = [
        {'weight': 0, 'knows_secret': False}, # Nada
        {'weight': 10, 'knows_secret': False}, # Gato
        {'weight': 80, 'knows_secret': False}, # Inimigo
        {'weight': 80, 'knows_secret': False}, # Inimigo insiste
        {'weight': 0, 'knows_secret': False}, # Foge
        {'weight': 70, 'knows_secret': True}, # Rei Bhoja
        {'weight': 70, 'knows_secret': True}, # Rei Entra
        {'weight': 0, 'knows_secret': False}  # Fecha
    ]
    
    for inp in inputs:
        dvarapala.update(inp)
        
    # Visualização do Log de Estados
    fig, ax = plt.subplots(figsize=(10, 4))
    
    times = [x[0] for x in dvarapala.state_log]
    states = [x[1] for x in dvarapala.state_log]
    
    # Map states to Y-axis numbers
    state_map = {"IDLE": 0, "OPEN": 1, "ATTACK": -1}
    y_vals = [state_map.get(s, 0) for s in states]
    
    ax.step(times, y_vals, where='mid', linewidth=2, color='blue')
    ax.set_yticks([-1, 0, 1])
    ax.set_yticklabels(['ATTACK', 'IDLE', 'OPEN'])
    ax.set_xlabel('Time Steps')
    ax.set_title('Bhoja Automaton: Finite State Machine Execution Log')
    ax.grid(True)
    
    # Annotate events
    for i, txt in enumerate(states):
        ax.annotate(txt, (times[i], y_vals[i]), textcoords="offset points", xytext=(0,10), ha='center')

    output_path = r"d:\TamesisTheoryCompleteResearchArchive\RECURSOS_PARA_PESQUISA\01_03_OLD_KERNEL\imagens\robotics_fsm_log.png"
    plt.savefig(output_path)
    print(f"Log Visual salvo em: {output_path}")

if __name__ == "__main__":
    simulation_gatekeeper_visual()
