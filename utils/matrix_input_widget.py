from PyQt6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt6.QtCore import Qt
import numpy as np


class MatrixInputWidget(QWidget):
    def __init__(self, initial_size=3):
        super().__init__()
        self.matrix_size = initial_size
        self.matrix_container = QGridLayout()
        self.vector_container = QGridLayout()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        inputs_layout = QHBoxLayout()

        # Etiquetas para la matriz y el vector
        variable_label =QLabel("Ingresa los coeficientes del sistema de ecuaciones x1, x2... xn")
        variable_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(variable_label)
        layout.addWidget(QLabel("Matriz A y vector b"))
        self.matrix_container.setSpacing(10)
        self.matrix_container.setContentsMargins(10,0,10,0)

        inputs_layout.addLayout(self.matrix_container)

        inputs_layout.addLayout(self.vector_container)
        layout.addLayout(inputs_layout)
        layout.addWidget(QLabel("Agregar o quitar filas y columnas"))
        # Botones para agregar/quitar filas y columnas
        controls_layout = QHBoxLayout()
        self.add_button = QPushButton("+")
        self.add_button.setObjectName("actionButton")
        self.add_button.clicked.connect(self.add_row_column)
        self.add_button.setMinimumSize(80,25)
        controls_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("-")
        self.remove_button.setObjectName("actionButton")
        self.remove_button.clicked.connect(self.remove_row_column)
        self.remove_button.setMinimumSize(80,25)
        controls_layout.addWidget(self.remove_button)

        layout.addLayout(controls_layout)
        self.setLayout(layout)
        self.create_inputs()

    def create_inputs(self):
        self.clear_inputs()

        try:
            # Crear entradas para la matriz
            for i in range(self.matrix_size):
                for j in range(self.matrix_size):
                    cell = QLineEdit()
                    cell.setFixedSize(50, 50)
                    cell.setContentsMargins(8,0,8,0)
                    self.matrix_container.addWidget(cell, i, j)


            # Crear entradas para el vector
            for i in range(self.matrix_size):
                vector_cell = QLineEdit()
                vector_cell.setFixedSize(50, 50)
                self.vector_container.addWidget(vector_cell, i, 0)
        except Exception as e:
            print(f"Error al crear los inputs: {e}")

    def clear_inputs(self):
        for i in reversed(range(self.matrix_container.count())):
            widget = self.matrix_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i in reversed(range(self.vector_container.count())):
            widget = self.vector_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def get_matrix_and_vector(self):
        try:
            A = np.zeros((self.matrix_size, self.matrix_size))
            b = np.zeros(self.matrix_size)

            for i in range(self.matrix_size):
                for j in range(self.matrix_size):
                    cell = self.matrix_container.itemAtPosition(i, j).widget()
                    if cell and cell.text():
                        A[i, j] = float(cell.text())
                    else:
                        raise ValueError("Por favor, complete todos los campos de la matriz.")

            for i in range(self.matrix_size):
                cell = self.vector_container.itemAtPosition(i, 0).widget()
                if cell and cell.text():
                    b[i] = float(cell.text())
                else:
                    raise ValueError("Por favor, complete todos los campos del vector.")
            return A, b

        except ValueError as ve:
            QMessageBox.critical(self, "Error", str(ve))
            return None, None
        except Exception as e:
            QMessageBox.critical(self, "Error inesperado", str(e))
            return None, None

    def add_row_column(self):
        self.matrix_size += 1
        self.create_inputs()

    def remove_row_column(self):
        if self.matrix_size > 2:
            self.matrix_size -= 1
            self.create_inputs()


