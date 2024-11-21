from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QScrollArea, QSizePolicy
from PyQt6.QtCore import Qt
from utils.matrix_input_widget import MatrixInputWidget
from utils.html_generator import intercambio_steps_to_html, matrix_result_to_html, vector_to_html_table, comprobacion_to_html
from Metodos.metodo_intercambio import metodo_intercambio
# Clase heredada de QWidget
class IntercambioMethodWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Método de Intercambio")
        self.setGeometry(100, 100, 1000, 700)
        self.initUI()

    def initUI(self):
        # Crear un area de scroll para toda la ventana
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Widget contenedor para el area de scroll
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        # Título del metodo
        self.label = QLabel("Método de Intercambio", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.label)
        # Descripcion del metodo
        description_label = QLabel("El método de intercambio es una técnica utilizada para resolver sistemas de ecuaciones lineales que "
                                   "involucran sistemas mal condicionados o matrices que presentan dificultades para su solución directa"
                                   " mediante métodos estándar como Gauss-Jordan. "
                                   "La idea principal es intercambiar filas y/o columnas de la matriz para mejorar "
                                   "la estabilidad numérica y facilitar el proceso de solución\n Pasos:\n"
                                   "Identificar el mejor pivote en la columna actual (el valor absoluto más grande)."
                                   "Intercambiar la fila actual con la fila que contiene el mejor pivote. Continuar con el método de eliminación (como en Gauss o Gauss-Jordan)..")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        scroll_layout.addWidget(description_label)

        # Añadir el widget de entrada de matrices
        self.matrix_widget = MatrixInputWidget()
        scroll_layout.addWidget(self.matrix_widget)

        # Boton para ejecutar el método de intercambio
        self.calculate_button = QPushButton("Calcular", self)
        self.calculate_button.setObjectName("actionButton")
        self.calculate_button.clicked.connect(self.run_intercambio)
        scroll_layout.addWidget(self.calculate_button)

        # Crear un QLabel para mostrar los resultados
        self.results_display = QLabel(self)
        self.results_display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.results_display.setWordWrap(True)
        self.results_display.setStyleSheet("padding: 10px;")

        # Añadir el QLabel a un area de scroll para los resultados
        results_scroll_area = QScrollArea()
        results_scroll_area.setWidgetResizable(True)
        results_scroll_area.setWidget(self.results_display)
        scroll_layout.addWidget(results_scroll_area)

        results_scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
        results_scroll_area.setMinimumHeight(400)
        scroll_layout.addWidget(results_scroll_area)

        scroll_area.setWidget(scroll_content)

        # Layout principal para la ventana
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def run_intercambio(self):
        # Metodo de la clase de input de matrices
        A, b = self.matrix_widget.get_matrix_and_vector()
        if A is not None and b is not None:
            try:
                # Ejecutar el método de intercambio
                matrices_intermedias, A_intercambio, A_numpy_inv, x_correcto, b_computed_correct = metodo_intercambio(A, b)

                # Generar contenido HTML para mostrar los resultados
                # Metodos de la clase html_generator
                html_content = intercambio_steps_to_html(matrices_intermedias)
                html_content += matrix_result_to_html(A_intercambio, "Matriz Final Resultante")
                html_content += matrix_result_to_html(A_numpy_inv, "Matriz Inversa Original")
                html_content += vector_to_html_table(x_correcto, "Vector Solución")
                html_content += comprobacion_to_html(b, b_computed_correct)

                # Mostrar los resultados en la interfaz
                self.results_display.setText(html_content)

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos de la matriz y el vector.")
