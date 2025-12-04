# main.py

import random
# 1. Importar la clase del juego
from juego_gato import Gato 
# 2. Importar la clase del Agente de Q-Learning
from agente import Agent 

# --- CONFIGURACIÓN ---
Q_TABLE_FILE = "q_table_gato.pkl"
NUM_EPISODES = 500000 
# ---------------------

def train_or_load_agent():
    """
    Función que gestiona la persistencia del modelo. 
    Intenta cargar la Q-Tabla. Si falla, entrena el agente y guarda el resultado.
    """
    print("--- 🧠 GESTIÓN DEL MODELO ---")
    
    # 1. Crear la instancia del Agente
    agent = Agent()
    
    # 2. Intentar Cargar el modelo entrenado
    if agent.load_q_table(Q_TABLE_FILE):
        print("\n✅ MODELO CARGADO. Listo para jugar.")
        # La función load_q_table debe establecer agent.eps = 0.0
        return agent
    
    # 3. Si la carga falla (archivo no encontrado o error), iniciar el entrenamiento
    print(f"Modelo no encontrado. Iniciando entrenamiento con {NUM_EPISODES} episodios...")
    
    agent.learn(NUM_EPISODES, Gato)
    
    # 4. Guardar el modelo recién entrenado
    agent.save_q_table(Q_TABLE_FILE)
    
    # Desactivar epsilon para jugar después del entrenamiento
    agent.eps = 0.0
    
    print(f"\n✅ ENTRENAMIENTO FINALIZADO. Q-Tabla aprendida con {len(agent.qlearner.values)} estados únicos y guardada en {Q_TABLE_FILE}.")
    return agent

# --------------------------------------------------------------------------------------
## FUNCIÓN DE JUEGO
# --------------------------------------------------------------------------------------

def play_against_agent(trained_agent):
    """
    Permite jugar contra el agente entrenado.
    El agente no usará la exploración (epsilon=0) para jugar con su política óptima.
    """
    print("\n--- 🎮 INICIANDO JUEGO CONTRA AGENTE ENTRENADO ---")
    
    # Asegurarse de que la exploración esté desactivada
    trained_agent.eps = 0.0
    
    game = Gato()
    
    print("El Agente es 'x' y juega primero.")
    print("Usa las coordenadas (fila, columna) de 00 a 22.")

    while not game.is_ended():
        
        current_state = game.get_state()
        valid_actions = game.get_valid_actions()

        if game.player == 1:
            # --- Turno del Agente (x) ---
            print("\nTurno del Agente (x)...")
            
            # El agente usa su acción óptima basada en la Q-Tabla
            # Nota: get_action usará la explotación pura (eps=0)
            x, y = trained_agent.get_action(current_state, valid_actions)
            print(f"Agente juega en: ({x}, {y})")
            game.play(x, y) 
        
        else:
            # --- Turno del Jugador Humano (o) ---
            print("\nTurno del Jugador (o)...")
            
            # Bucle para asegurar que el input sea válido
            while True:
                try:
                    move_str = input("Ingresa tu movimiento (ej: 01 para Fila 0, Columna 1): ")
                    if len(move_str) != 2: raise ValueError
                    r, c = int(move_str[0]), int(move_str[1])
                    
                    if (r, c) in valid_actions:
                        game.play(r, c)
                        break
                    else:
                        print("Movimiento inválido o celda ya ocupada. Intenta de nuevo.")
                except:
                    print("Formato inválido. Usa dos dígitos (00, 01, ..., 22).")
        
        # Verificar el estado después de cada movimiento
        winner = game.get_winner()
        if winner is not None:
            game._print() 
            return f"RESULTADO: ¡El ganador es {game.repr[winner]}!"
        
        if not game.get_valid_actions():
            game._print()
            return "RESULTADO: ¡Empate! No quedan movimientos."
        
    return "Juego Terminado."

# --------------------------------------------------------------------------------------
## EJECUCIÓN PRINCIPAL
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    # 1. Cargar el modelo entrenado o iniciar el entrenamiento
    agent = train_or_load_agent()
    
    # 2. Jugar contra el agente entrenado
    print("\n---------------------------------------------------------")
    print(play_against_agent(agent))
    print("---------------------------------------------------------")