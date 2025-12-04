
from collections import defaultdict


class Q:
    def __init__(self, alpha=0.5, discount=0.5):
        self.alpha = alpha
        self.discount = discount
        self.values = defaultdict(lambda: defaultdict(lambda: 0.0))


        
    def update(self,state, action, next_state, reward):
        value = self.values[state][action]
        v = list(self.values[next_state].values())
        next_q = max(v) if v else 0
        value = value + self.alpha * (reward + self.discount * next_q - value)
        self.values[state][action] = value


    def get_best_action(self, state):
            actions_q = self.values[state]
            if not actions_q:
                # No hay acciones registradas para este estado
                return None
            
            # Encontrar la acción con el valor Q máximo
            # max() con un key utiliza la función lambda para comparar por el valor
            best_action = max(actions_q, key=actions_q.get)
            return best_action


