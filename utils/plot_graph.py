from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class SecantPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(SecantPlotCanvas, self).__init__(self.fig)

    def plot(self, f, a, b, iterations):
        # Limpiar el eje antes de volver a dibujar
        self.ax.clear()

        # Obtener los puntos de la gráfica en un intervalo ajustado
        root = iterations[-1][2]
        x_vals = np.linspace(root - 5, root + 5, 400)
        y_vals = f(x_vals)
        # Graficar la función f(x)
        self.ax.plot(x_vals, y_vals, label="f(x)")

        # Marcar la raíz encontrada en la gráfica
        self.ax.axvline(root, color='g', linestyle='--', label=f"Raíz encontrada = {root:.6f}")

        # Etiquetas y título
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title('Método de la Secante')
        self.ax.legend()

        # Actualizar límites del eje y para que la raíz sea visible
        self.ax.set_xlim(root - 5, root + 5)
        self.ax.set_ylim(min(y_vals) - 1, max(y_vals) + 1)

        # Actualizar
        self.draw()
