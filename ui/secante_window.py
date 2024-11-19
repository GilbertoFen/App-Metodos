from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QTableWidget, \
    QTableWidgetItem, QSizePolicy, QScrollArea
from Metodos.metodo_secante import secant_method
from utils.plot_graph import SecantPlotCanvas
import sympy as sp
import numpy as np
from PyQt6.QtCore import Qt

class SecantMethodWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.table_visible = False

    def initUI(self):
        # Crear un área de scroll para toda la ventana
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Widget contenedor para el área de scroll
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        description_label= QLabel("El método de la secante es un método numérico iterativo utilizado para encontrar raíces de funciones no lineales, "
                                  "es decir, resolver ecuaciones de la forma 𝑓(𝑥)=0."
                                  "Es una alternativa al método de Newton-Raphson que no requiere el cálculo de derivadas, "
                                  "lo que lo hace más eficiente cuando estas son difíciles de obtener.\n"
                                  "El método utiliza dos aproximaciones iniciales cercanas a la raíz en lugar de una sola, y en cada iteración, "
                                  "traza una línea secante que conecta los puntos (𝑥𝑛−1,𝑓( 𝑥𝑛−1)) y(𝑥𝑛, 𝑓(𝑥𝑛)). "
                                  "Luego, la intersección de esta línea con el eje 𝑥  "
                                  "proporciona una nueva aproximación 𝑥𝑛+1.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        scroll_layout.addWidget(description_label)

        # Título
        self.label = QLabel("Método de la secante")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.label)

        # Campo para ingresar la función
        self.function_input = QLineEdit(self)
        self.function_input.setPlaceholderText("Ingresa una función (e.g., x**2 + 2*x + 3)")
        self.function_input.textChanged.connect(self.auto_plot_function)  # Conectar aquí
        scroll_layout.addWidget(self.function_input)

        # Campo para ingresar el intervalo
        interval_layout = QHBoxLayout()
        self.label_interval = QLabel("Ingresa un intervalo:", self)
        interval_layout.addWidget(self.label_interval)

        self.input_a = QLineEdit(self)
        self.input_a.setPlaceholderText("a")
        interval_layout.addWidget(self.input_a)

        self.input_b = QLineEdit(self)
        self.input_b.setPlaceholderText("b")
        interval_layout.addWidget(self.input_b)

        scroll_layout.addLayout(interval_layout)

        # Botón para graficar la función
        self.graph_button = QPushButton("Graficar función", self)
        self.graph_button.clicked.connect(self.plot_function)
        scroll_layout.addWidget(self.graph_button)

        # Botón para ver la tabla de iteraciones
        self.iterations_button = QPushButton("Ver tabla de iteraciones", self)
        self.iterations_button.clicked.connect(self.toggle_iterations)
        scroll_layout.addWidget(self.iterations_button)

        # Campo para la gráfica
        self.canvas = SecantPlotCanvas(self, width=5, height=4)
        scroll_layout.addWidget(self.canvas)

        # Tabla para mostrar las iteraciones
        self.iterations_table = QTableWidget(self)
        self.iterations_table.setColumnCount(7)
        self.iterations_table.setHorizontalHeaderLabels(["a", "b", "xn", "f(a)", "f(b)", "f(xn)", "Error relativo"])
        self.iterations_table.setVisible(False)
        scroll_layout.addWidget(self.iterations_table)

        # Asignar el contenido al área de scroll
        scroll_area.setWidget(scroll_content)

        # Layout principal para la ventana
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def auto_plot_function(self):
        """
        Intenta graficar la función automáticamente al escribir en el input.
        """
        try:
            function_text = self.function_input.text()

            # Validar si el texto no está vacío
            if not function_text.strip():
                return

            # Convertir el texto a una función válida de SymPy
            x = sp.symbols('x')
            func = sp.sympify(function_text)
            f = sp.lambdify(x, func, modules=["numpy"])

            # Rango predeterminado para graficar
            x_min, x_max = -10, 10
            x_vals = np.linspace(x_min, x_max, 400)
            y_vals = f(x_vals)

            # Verificar si hay valores inválidos (NaN o Inf)
            if np.any(np.isnan(y_vals)) or np.any(np.isinf(y_vals)):
                raise ValueError("La función contiene valores inválidos en el rango seleccionado.")

            # Graficar la función automáticamente
            self.canvas.plot(f)
        except Exception as e:
            # Manejar errores sin detener la aplicación
            self.canvas.ax.clear()
            self.canvas.ax.text(0.5, 0.5, f"Error: {str(e)}",
                                ha='center', va='center', transform=self.canvas.ax.transAxes, color='red')
            self.canvas.draw()


    def plot_function(self):
        try:
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            function_text = self.function_input.text()
            # Establecemos la variable que leera sympy
            x = sp.symbols('x')
            func = sp.sympify(function_text)
            """ 
            lambdify hace que f sea una funcion, recibe nuestra variable, la funcion transformada 
            en algebraica y modules=["numpy"] permite que usemos funciones como sen,cos,e 
            """
            f = sp.lambdify(x, func, modules=["numpy"])

            if np.isinf(f(a)) or np.isinf(f(b)) or np.isnan(f(a)) or np.isnan(f(b)):
                raise ValueError("La función no es válida en los puntos dados")
            # Llamada al metodo de la secante
            root, iterations = secant_method(f, a, b)

            if root is None:
                self.label.setText("No se pudo encontrar la raíz.")
            else:
                self.canvas.plot(f, a, b, iterations)
                self.label.setText(f"Raíz encontrada: {root:.6f}")

        except Exception as e:
            self.label.setText(f"Error: {e}")

    def toggle_iterations(self):

        if self.table_visible:
            self.iterations_table.setVisible(False)
            self.iterations_button.setText("Ver tabla de iteraciones")
        else:
            self.show_iterations_table()
            self.iterations_table.setVisible(True)
            self.iterations_button.setText("Ocultar tabla de iteraciones")

        self.table_visible = not self.table_visible

    def show_iterations_table(self):
        try:
            a = float(self.input_a.text())
            b = float(self.input_b.text())
            function_text = self.function_input.text()

            x = sp.symbols('x')
            func = sp.sympify(function_text)
            f = sp.lambdify(x, func, modules=["numpy"])
            # Aqui usamos la misma logica pero para realizar la tabla de iteraciones
            _, iterations = secant_method(f, a, b)

            if not iterations:
                raise ValueError("No se encontraron iteraciones")

            # Creamos la tabla con sus columnas por cada variable
            self.iterations_table.setRowCount(len(iterations))
            for i, (val_a, val_b, xn, f_a, f_b, f_xn, error) in enumerate(iterations):
                self.iterations_table.setItem(i, 0, QTableWidgetItem(f'{val_a:.6f}'))
                self.iterations_table.setItem(i, 1, QTableWidgetItem(f'{val_b:.6f}'))
                self.iterations_table.setItem(i, 2, QTableWidgetItem(f'{xn:.6f}'))
                self.iterations_table.setItem(i, 3, QTableWidgetItem(f'{f_a:.6f}'))
                self.iterations_table.setItem(i, 4, QTableWidgetItem(f'{f_b:.6f}'))
                self.iterations_table.setItem(i, 5, QTableWidgetItem(f'{f_xn:.6f}'))
                self.iterations_table.setItem(i, 6, QTableWidgetItem(f'{error:.6f}'))

            self.iterations_table.setStyleSheet("color: white;")
        except Exception as e:
            self.label.setText(f"Error: {e}")
