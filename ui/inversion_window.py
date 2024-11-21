from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QScrollArea, QMessageBox, \
    QSizePolicy
from PyQt6.QtCore import Qt
from utils.matrix_input_widget import MatrixInputWidget
from utils.html_generator import matrix_to_html_table, vector_to_html_table, vector_comprobacion_table, steps_to_html
from Metodos.inversion_matrices import gauss_jordan_partitioned
from Metodos.gauss_jordan import gauss_jordan

class InversionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Inversión de Matrices - Gauss Jordan Particionado")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()

    def initUI(self):
        # Crear el area de scroll
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_area.setWidget(scroll_content)

        # Layout principal dentro del area de scroll
        main_layout = QVBoxLayout(scroll_content)
        # Titulo centrado
        self.label = QLabel("Inversión de Matrices - Gauss Jordan Particionado", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.label)

        # Descripcion del método
        description_label = QLabel("Gauss-Jordan: El método de Gauss-Jordan es una técnica para encontrar la inversa de una matriz cuadrada y resolver sistemas de ecuaciones lineales. "
                                   "El enfoque consiste en transformar la matriz original 𝐴  en la matriz identidad 𝐼  utilizando operaciones elementales de matrices. Durante este proceso, una matriz identidad adjunta a la "
                                   "derecha se transforma en la inversa de 𝐴.\nGauss-Jordan Particionado: Divide la matriz en bloques más pequeños (usualmente 3x3)"
                                   " y realiza operaciones en submatrices."
                                   "Es eficiente para matrices grandes, aprovechando la partición para optimizar los cálculos.")
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setObjectName("descriptionLabel")
        description_label.setWordWrap(True)
        main_layout.addWidget(description_label)



        # Widget para la entrada de matriz y vector
        self.matrix_widget = MatrixInputWidget()
        main_layout.addWidget(self.matrix_widget)

        # Controles para resolver el sistema
        controls_layout = QHBoxLayout()
        self.gj_button = QPushButton("Resolver por Gauss-Jordan")
        self.gj_button.setObjectName("actionButton")
        self.gj_button.clicked.connect(self.solve_gauss_jordan)
        controls_layout.addWidget(self.gj_button)

        self.partitioned_button = QPushButton("Resolver por Gauss-Jordan Particionado")
        self.partitioned_button.setObjectName("actionButton")
        self.partitioned_button.clicked.connect(self.solve_gauss_jordan_partitioned)
        controls_layout.addWidget(self.partitioned_button)

        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addLayout(controls_layout)

        # Contenedor para mostrar los resultados
        self.steps_display = QTextEdit()
        self.steps_display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.steps_display.setReadOnly(True)
        self.steps_display.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding )
        self.steps_display.setMinimumHeight(400)
        main_layout.addWidget(self.steps_display)

        # Establecer el layout principal del widget actual
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def solve_gauss_jordan(self):
        try:
            # Metodo de la clase de los inputs de la matriz
            A, b = self.matrix_widget.get_matrix_and_vector()
            if A is None or b is None:
                raise ValueError("Por favor, complete todos los campos")

            # Resolver usando Gauss-Jordan normal
            A_inv, steps = gauss_jordan(A)
            # Usamos @ para la multiplicacion de matrices
            solution = A_inv @ b
            html_steps = self.generate_html_steps(steps, solution=solution, inverse=A_inv)
            self.steps_display.setHtml(html_steps)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def solve_gauss_jordan_partitioned(self):
        try:
            A, b = self.matrix_widget.get_matrix_and_vector()
            if A is None or b is None:
                raise ValueError("Por favor, complete todos los campos")

            # Resolver usando Gauss Jordan particionado
            x, steps, inverse = gauss_jordan_partitioned(A, b)
            html_steps = self.generate_html_steps(steps, solution=x, inverse=inverse)
            self.steps_display.setHtml(html_steps)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generate_html_steps(self, steps, solution=None, inverse=None):
        html_content = steps_to_html(steps)

        # Mostrar la matriz inversa final si esta disponible
        if inverse is not None:
            html_content += matrix_to_html_table(inverse, "Matriz Inversa Final")

        # Mostrar el vector solución final si esta disponible
        if solution is not None:
            html_content += vector_to_html_table(solution, "Vector Solución Final")

        # Comprobacion Ax = b
        A, b = self.matrix_widget.get_matrix_and_vector()
        if A is not None and b is not None and solution is not None:
            b_computed = A @ solution
            html_content += vector_comprobacion_table(b, b_computed)

        return html_content
