from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt
import numpy as np
from utils.matrix_input_widget import MatrixInputWidget
from Metodos.pivot_gauss_jordan import pivoteo_parcial, pivoteo_total, pivoteo_escalonado
from utils.html_generator import pivot_steps_to_html, vector_to_html_table, vector_comprobacion_table

class PivotGaussWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Método Gauss-Jordan con Estrategias de Pivoteo")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()

    def initUI(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.label = QLabel("Método Gauss-Jordan con Estrategias de Pivoteo", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.addWidget(self.label)

        description_label = QLabel("El pivoteo es una técnica utilizada para mejorar la estabilidad numérica al resolver sistemas de ecuaciones lineales. "
                                   "Su propósito es evitar errores de redondeo y dividir por números pequeños que podrían generar inestabilidad\n Pivoteo parcial:"
                                   "Se busca el elemento de mayor valor absoluto en la columna actual y se intercambia la fila correspondiente con la fila actual.\n"
                                   "Pivoteo total: Se busca el elemento de mayor valor absoluto en toda la submatriz restante y se intercambian tanto filas como columnas para posicionarlo en la diagonal.\n"
                                   "Pivoteo escalonado: Antes de realizar el pivoteo, se escalan las filas dividiendo cada elemento por el mayor valor absoluto en esa fila. Luego, se procede con el pivoteo parcial, pero usando los elementos escalados.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        scroll_layout.addWidget(description_label)

        self.matrix_inputs = MatrixInputWidget()
        scroll_layout.addWidget(self.matrix_inputs)

        # Botones para la estrategia de pivoteo
        button_layout = QHBoxLayout()
        self.button1 = QPushButton("Pivoteo Parcial")

        self.button1.clicked.connect(self.run_estrategia_1)
        self.button1.setObjectName("actionButton")
        button_layout.addWidget(self.button1)

        self.button2 = QPushButton("Pivoteo Total")
        self.button2.clicked.connect(self.run_estrategia_2)
        self.button2.setObjectName("actionButton")
        button_layout.addWidget(self.button2)

        self.button3 = QPushButton("Pivoteo Escalonado")
        self.button3.setObjectName("actionButton")
        self.button3.clicked.connect(self.run_estrategia_3)
        button_layout.addWidget(self.button3)

        scroll_layout.addLayout(button_layout)

        self.results_display = QLabel()
        self.results_display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.results_display.setWordWrap(True)
        self.results_display.setStyleSheet("padding: 10px;")

        results_scroll_area = QScrollArea()
        results_scroll_area.setWidgetResizable(True)

        results_scroll_area.setWidget(self.results_display)
        scroll_layout.addWidget(results_scroll_area)

        scroll_area.setWidget(scroll_content)

        # Layout principal para la ventana
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def display_results(self, steps, x, A, b):
        # Metodos de la clase html
        html_content = pivot_steps_to_html(steps)
        html_content += vector_to_html_table(x, "Vector Solución Final")
        b_computed = np.dot(A, x)
        html_content += vector_comprobacion_table(b, b_computed)

        self.results_display.setText(html_content)

    def run_estrategia_1(self):
        try:
            A, b = self.matrix_inputs.get_matrix_and_vector()
            x, steps = pivoteo_parcial(A, b)
            self.display_results(steps, x, A, b)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run_estrategia_2(self):
        try:
            A, b = self.matrix_inputs.get_matrix_and_vector()
            # _ quiere decir que no nos importa ese valor de retorno
            x, _, steps = pivoteo_total(A, b)
            self.display_results(steps, x, A, b)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def run_estrategia_3(self):
        try:
            A, b = self.matrix_inputs.get_matrix_and_vector()
            x, _, steps = pivoteo_escalonado(A, b)
            self.display_results(steps, x, A, b)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
