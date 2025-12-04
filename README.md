# 🤖 Q-Gato: Agente de Tic-Tac-Toe con Q-Learning

Este proyecto implementa el clásico juego de **Tic-Tac-Toe (Gato)** y entrena un agente de **Inteligencia Artificial** utilizando el algoritmo de **Q-Learning** (Aprendizaje por Refuerzo) para que juegue de manera óptima.

## ✨ Características Principales

* **Juego Base:** Implementación de la lógica del Gato (tablero 3x3, verificación de victoria en filas, columnas y diagonales).
* **Agente Inteligente:** Clase `Agent` que utiliza el algoritmo Q-Learning para aprender la mejor jugada para cada estado del tablero.
* **Aprendizaje Estratégico:** Uso de la política **$\epsilon$-Greedy** para balancear la explotación (mejor jugada conocida) y la exploración (jugadas aleatorias).
* **Persistencia:** Capacidad de **guardar y cargar la Q-Tabla** (modelo entrenado) en un archivo JSON, evitando tener que re-entrenar al agente.
* **Modo Interactivo:** Permite al usuario jugar directamente contra el agente entrenado.

---

## 💻 Estructura de Archivos

| Archivo | Descripción Principal |
| :--- | :--- |
| `juego_gato.py` | Contiene la clase `Gato` que maneja el **tablero, movimientos, y la verificación** de las condiciones de victoria/empate. |
| `q_learn.py` | Contiene la clase `Q` que implementa la **fórmula de actualización de Q-Learning** y la búsqueda de la acción óptima. |
| `agente.py` | Contiene la clase `Agent` que gestiona el **entrenamiento** (simulación de episodios, decaimiento de $\epsilon$) y la **persistencia** del modelo. |
| `main.py` | Script de ejecución principal. **Coordina la carga/entrenamiento** del agente y el **modo de juego interactivo** contra el humano. |

---