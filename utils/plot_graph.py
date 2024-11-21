from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class SecantPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = self.fig.add_subplot(111)
        super(SecantPlotCanvas, self).__init__(self.fig)

    def plot(self, f, a=None, b=None, iterations=None):
        self.ax.clear() 
        # Limpiar el gráfico anterior

        # Rango de x a y b si se ingresan de lo contrario usar predeterminado
        if a is not None and b is not None:
            x_vals = np.linspace(a, b, 400)
        else:
            x_vals = np.linspace(-10, 10, 400)

        y_vals = f(x_vals)

        # Verificar si hay valores NaN o Inf
        if np.any(np.isnan(y_vals)) or np.any(np.isinf(y_vals)):
            raise ValueError("La función tiene valores inválidos en el rango seleccionado.")

        self.ax.plot(x_vals, y_vals, label="f(x)")
        self.ax.axhline(0, color="black", linestyle="--", linewidth=0.8)

        if iterations:
            root = iterations[-1][2]  
            # Raíz aproximada
            self.ax.axvline(root, color='g', linestyle='--', label=f"Raíz: {root:.6f}")

        self.ax.set_title("Gráfica de la función")
        self.ax.legend()
        self.draw()
