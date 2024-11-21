from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt
from utils.matrix_input_widget import MatrixInputWidget
from utils.html_generator import iterations_to_html, matrix_T_to_html, equations_to_html, vector_to_html_table, vector_comprobacion_table
from Metodos.metodo_jacobi import jacobi

class JacobiMethodWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Método de Jacobi")
        self.setGeometry(100, 100, 1000, 700)
        self.initUI()

    def initUI(self):
        # Crear un area de scroll para toda la ventana
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Widget contenedor para el area de scroll
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # Titulo del método
        self.label = QLabel("Método de Jacobi", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.label)

        description_label = QLabel("Jacobi: El método parte de una aproximación inicial de la solución y mejora iterativamente esta estimación hasta alcanzar un nivel "
                                   "de precisión deseado. La clave es descomponer la matriz 𝐴 en su parte "
                                   "diagonal 𝐷 y el resto 𝑅: x=D−1(b−Rx(k))\n"
                                   "Pasos: Reorganizar el sistema para expresar cada incógnita en función de las demás\n."
                                   "Elegir una aproximación inicial𝑥(0).\n"
                                   "Iterar utilizando la fórmula anterior hasta que el cambio entre iteraciones sea menor que una tolerancia\n"
                                   "Si la matriz 𝐴  es diagonalmente dominante el metodo converge hacia una solucion. Si la matriz no es dominante diagonalmente"
                                   "Deberemos hacer el calculo de su radio espectral y para que el metodo converga este "
                                   "debera ser < 1. De lo contrario el metodo nunca va a converger")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        scroll_layout.addWidget(description_label)

        # Widget para la entrada de matrices
        self.matrix_inputs = MatrixInputWidget()
        scroll_layout.addWidget(self.matrix_inputs)

        # Boton para calcular
        self.calculate_button = QPushButton("Calcular", self)
        self.calculate_button.clicked.connect(self.run_jacobi)
        self.calculate_button.setObjectName("actionButton")
        scroll_layout.addWidget(self.calculate_button)

        # Contenedor para los resultados con su propio area de scroll
        self.results_display = QLabel()
        self.results_display.setWordWrap(True)
        self.results_display.setStyleSheet("padding: 10px;")

        # Area de scroll para los resultados
        results_scroll_area = QScrollArea()
        results_scroll_area.setWidgetResizable(True)
        results_scroll_area.setWidget(self.results_display)

        results_scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        results_scroll_area.setMinimumHeight(400)
        scroll_layout.addWidget(results_scroll_area)

        # Asignar el contenido al area de scroll principal
        scroll_area.setWidget(scroll_content)

        # Layout principal para la ventana
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def run_jacobi(self):
        try:
            A, b = self.matrix_inputs.get_matrix_and_vector()


            # Ejecutar el metodo de Jacobi
            result, steps, spectral_radius, T, equations, Ax = jacobi(A, b)

            if spectral_radius >= 1:
                QMessageBox.warning(self, "Advertencia", "El método no converge, el radio espectral es mayor o igual a 1.")


            # Generar el contenido HTML para los resultados

            html_content = iterations_to_html(steps)
            # Mostrar el radio espectral
            html_content += f"<h4>Radio Espectral: {spectral_radius:.4f}</h4>"
            html_content += matrix_T_to_html(T)
            html_content += equations_to_html(equations)
            html_content += vector_to_html_table(result, "Vector Solución Final")
            html_content += vector_comprobacion_table(b, Ax)

            # Mostrar el contenido en el QLabel
            self.results_display.setText(html_content)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
