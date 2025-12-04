
class Gato:
    def __init__(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.player = 1
        self.repr = {0: ".", 1: "x", -1: "o"}




    def get_winner(self):
            # --- 1. Verificar Ganador en Filas (Horizontal) ---
            for i in range(3):
                # Si la suma absoluta de una fila es 3, significa que un jugador (1 o -1)
                # ocupó las 3 celdas.
                if abs(sum(self.board[i])) == 3:
                    return self.board[i][0]

            # --- 2. Verificar Ganador en Columnas (Vertical) ---
            for i in range(3):
                # Suma de la columna i
                col_sum = sum(self.board[j][i] for j in range(3))
                if abs(col_sum) == 3:
                    return self.board[0][i]

            # --- 3. Verificar Ganador en Diagonales ---
            # Diagonal Principal: (0,0), (1,1), (2,2)
            diag_principal_sum = self.board[0][0] + self.board[1][1] + self.board[2][2]
            if abs(diag_principal_sum) == 3:
                return self.board[0][0]

            # Diagonal Secundaria: (0,2), (1,1), (2,0)
            diag_secundaria_sum = self.board[0][2] + self.board[1][1] + self.board[2][0]
            if abs(diag_secundaria_sum) == 3:
                return self.board[0][2]

            return None



    def get_state(self):
        return str(self.board)
   
    def get_valid_actions(self):
            actions = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == 0:
                        actions.append((i, j))
            return actions
   
    def is_ended(self):  
            # Si hay un ganador
            if self.get_winner() is not None:
                return True
            # Si no hay movimientos válidos (empate)
            if not self.get_valid_actions():
                return True
            # El juego continúa
            return False


    def _print(self):
        print("-------------")
        for row in self.board:
            # Reemplaza 1, -1, 0 con 'x', 'o', '.' y une con espacios
            print("| " + " | ".join(self.repr[cell] for cell in row) + " |")
            print("-------------")
        print(f"Turno: {self.repr[self.player]}")



    def play(self, x, y):
        # Si la celda ya está ocupada
        if self.board[x][y] != 0:
            print("Posición no válida. Intenta de nuevo.")
            return None

        # Realizar el movimiento
        self.board[x][y] = self.player

        # Imprimir el tablero después del movimiento
        self._print()

        # Verificar si hay un ganador
        winner = self.get_winner()
        if winner:
            print(f"¡El jugador {self.repr[winner]} ha ganado!")
            return winner

        # Verificar si hay empate
        if self.is_ended():
             print("¡Juego terminado en empate!")
             return 0 # 0 puede representar un empate

        # Si no ha terminado, cambiar el turno al otro jugador
        self.player *= -1
        return None

