
from collections import defaultdict
import json
import pickle
import random
from q_learn import Q

class Agent:
    """Clase para generar el agente"""
    def __init__(self):
        self.eps = 1.0
        self.qlearner = Q()


    def get_action(self, state, valid_actions):
        if random.random() < self.eps:
            return random.choice(valid_actions)
        best = self.qlearner.get_best_action(state)
        if best is None:
            return random.choice(valid_actions)
        return best



    def learn_game(self, Gato_class):
            """
            Simula un juego completo (episodio) entre el Agente (Jugador 1) y un oponente aleatorio (Jugador -1).
            Recopila la historia de movimientos del Agente y devuelve la recompensa final y el estado final.
            """
            game = Gato_class() 
            self.history = []
            
            while not game.is_ended():
                current_state = game.get_state()
                valid_actions = game.get_valid_actions()

                if game.player == 1:
                    # --- Turno del Agente (Jugador 1) ---
                    action = self.get_action(current_state, valid_actions)
                    self.history.append((current_state, action))
                    x, y = action
                    game.board[x][y] = game.player # Realizar movimiento
                else:
                    # --- Turno del Oponente Aleatorio (Jugador -1) ---
                    opponent_action = random.choice(valid_actions)
                    x, y = opponent_action
                    game.board[x][y] = game.player # Realizar movimiento

                # Cambiar el turno manualmente
                game.player *= -1

            # --- Fin del Juego: Determinar Recompensa ---
            winner = game.get_winner()
            final_state = game.get_state()
            
            reward = 0
            if winner == 1:
                reward = 100  # Gana el Agente
            elif winner == -1:
                reward = -100 # Pierde el Agente
            # Si es empate, reward = 0

            return reward, final_state


    def learn(self, num_episodes, Gato_class):
        EPS_DECAY = 0.9995 
        
        print(f"Iniciando entrenamiento para {num_episodes} episodios...")
        for episode in range(num_episodes):
            
            # 1. Jugar el episodio
            final_reward, final_state = self.learn_game(Gato_class)
            
            # 2. Propagar la recompensa final (Actualización Q inversa)
            
            # Recorrer el historial de movimientos del Agente en reversa
            for state, action in reversed(self.history):
                
                # R es la recompensa final (solo para el movimiento que llevó al final)
                current_reward = final_reward
                
                # Actualizar el valor Q. El 'final_state' es el S' para este paso.
                self.qlearner.update(state, action, final_state, current_reward)
                
                # Preparamos los valores para el paso anterior (la siguiente iteración):
                # El S' para el movimiento anterior es el 'state' actual.
                final_state = state 
                
                # La recompensa instantánea R para los movimientos anteriores al final es 0.
                final_reward = 0 

            # 3. Decaimiento de Epsilon ($\epsilon$ decay)
            self.eps *= EPS_DECAY
            
            # Mantenemos una exploración mínima
            if self.eps < 0.05:
                self.eps = 0.05
            
            if (episode + 1) % 10000 == 0:
                print(f"Episodio: {episode + 1}/{num_episodes}. Epsilon: {self.eps:.4f}. Tamaño de Q-Tabla: {len(self.qlearner.values)}")

        print("Entrenamiento completado.")

    def save_q_table(self, filename):
        """Guarda la tabla Q en formato JSON, serializando las claves de tupla."""
        try:
            serializable_q_table = {}
            for state, actions_q_defaultdict in self.qlearner.values.items():
                
                # Nivel 1: Convertir la tupla 'state' a string (JSON solo acepta strings como claves)
                state_str = str(state) 
                
                actions_dict = {}
                for action, value in actions_q_defaultdict.items():
                    # Nivel 2: Convertir la tupla 'action' a string
                    action_str = str(action)
                    actions_dict[action_str] = value
                
                serializable_q_table[state_str] = actions_dict

            with open(filename, 'w') as f:
                json.dump(serializable_q_table, f)
                
            print(f"Tabla Q guardada exitosamente en {filename}. {len(serializable_q_table)} estados guardados.")
        except Exception as e:
            print(f"Error al guardar la tabla Q con JSON: {e}")

    def load_q_table(self, filename):
        """Carga la tabla Q desde JSON, deserializando las claves y convirtiendo a tupla."""
        try:
            with open(filename, 'r') as f:
                loaded_dict_str = json.load(f)
                
                # Limpiar la tabla Q actual
                self.qlearner.values.clear() 
                
                # Deserializar los dos niveles de strings a tuplas
                for state_str, actions_dict in loaded_dict_str.items():
                    
                    # 1. CONVERSIÓN DE CLAVE STATE (Tupla)
                    state_raw = eval(state_str)
                    # Forzar la conversión a tupla, ya sea si es una lista o una tupla
                    state_tuple = tuple(state_raw) 
                    
                    actions_q_defaultdict = defaultdict(float)
                    for action_str, value in actions_dict.items():
                        
                        # 2. CONVERSIÓN DE CLAVE ACTION (Tupla)
                        action_raw = eval(action_str)
                        action_tuple = tuple(action_raw) # Forzar la conversión a tupla
                        
                        actions_q_defaultdict[action_tuple] = value
                    
                    self.qlearner.values[state_tuple] = actions_q_defaultdict
                
            print(f"Tabla Q cargada exitosamente desde {filename}")
            self.eps = 0.0
            return True
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado.")
            return False
        except Exception as e:
            # Imprimir el error para depuración
            print(f"Error al cargar la tabla Q con JSON: {e}") 
            return False