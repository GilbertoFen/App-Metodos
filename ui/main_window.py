from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QScrollArea, QHBoxLayout, \
    QGridLayout
from PyQt6.QtCore import Qt

from ui.intercambio_window import IntercambioMethodWindow
from ui.inversion_window import InversionWindow
from ui.pivot_gauss_window import PivotGaussWindow
from ui.button_custom_main import CustomButton
from ui.jacobi_window import JacobiMethodWindow
from ui.secante_window import SecantMethodWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Métodos Numéricos 1")
        self.setGeometry(100, 100, 1000, 900)
        self.secant_window = None
        self.inversion_window = None
        self.jacobi_window = None
        self.pivot_gauss_window = None
        self.intercambio_window = None
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))

        #Contenedor principal
        scroll_area = QScrollArea(self)
        main_container = QWidget()
        scroll_area.setWidget(main_container)
        scroll_area.setWidgetResizable(True)
        self.setCentralWidget(scroll_area)

        #Creamos una distribucion vetical para los widgets que añandimos
        main_layout = QVBoxLayout(main_container)
        main_layout.setSpacing(0)  # Reduce el espacio entre widgets
        main_layout.setContentsMargins(10, 10, 10, 10)

        #1er elemento del contenedor
        title_container = QHBoxLayout()
        title_container.setContentsMargins(5, 5, 5, 100)
        self.title_label = QLabel("Métodos Numéricos 1", self)
        self.title_label.setObjectName("Title")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setContentsMargins(5,5,5,0)
        title_container.addWidget(self.title_label)
        #Metodo que añade widgets a el contenedor
        main_layout.addLayout(title_container) 

        #2do elemento
        description_container = QHBoxLayout()
        description_container.setSpacing(0)
        description_label = QLabel("Los métodos numéricos son técnicas matemáticas utilizadas para resolver problemas que son "
                                   "difíciles o imposibles de solucionar de forma exacta mediante métodos analíticos. "
                                   "Estas técnicas emplean aproximaciones para obtener soluciones numéricas a problemas complejos,"
                                   "siendo especialmente útiles en ciencias, ingeniería y matemáticas aplicadas.\n\n"
                                   "Los métodos numéricos no buscan soluciones exactas, sino aproximaciones que sean suficientemente precisas.\n"
                                   "Muchos de estos métodos son iterativos, lo que significa que mejoran la solución paso a paso hasta alcanzar un nivel de error aceptable.\n"
                                   "Son capaces de manejar problemas con datos incompletos, ruidosos o con condiciones iniciales difíciles.\n"
                                   "Algunos métodos requieren garantizar que, tras suficientes iteraciones, convergerán a una solución correcta o cercana a la correcta.\n"
                                   "Los métodos numéricos se implementan con computadoras debido al alto volumen de cálculos repetitivos que requieren.")
        description_label.setObjectName("descriptionLabel")

        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setWordWrap(True)
        description_container.addWidget(description_label)
        main_layout.addLayout(description_container)

        #3er elemento: Opciones de la aplicacion
        button_names_callbacks = [
            ("Método de la Secante", self.open_secant_method),
            ("Inversa de matrices: Gauss Jordan particionado", self.open_inversion_method),
            ("Gauss Jordan Con pivoteo", self.open_pivot_gauss_method),
            ("Método de intercambio", self.open_intercambio_method),
            ("Método de Jacobi", self.open_jacobi_method)
        ]

        bottom_container = QWidget()
        option_layout = QGridLayout()

        for name, callback in button_names_callbacks:
            button = CustomButton(name, callback, self)
            option_layout.addWidget(button)

        bottom_container.setLayout(option_layout)
        main_layout.addWidget(bottom_container)

    # Metodo para conectar los eventos en las opciones
    def handle_button_click(self):
        sender = self.sender()
        if sender.text() == "Método de la Secante":
            self.open_secant_method()
        elif sender.text() == "Inversa de matrices: Gauss Jordan particionado":
            self.open_inversion_method()
        elif sender.text()=="Método de Jacobi":
            self.open_jacobi_method()
        elif sender.text()=="Método de intercambio":
            self.open_intercambio_method()
        elif sender.text()=="Gauss Jordan Con pivoteo":
            self.open_pivot_gauss_method()


    def open_secant_method(self):
        # Crea una ventana de secante
        self.secant_window = SecantMethodWindow(self)

        # Establecemos el widget principal como la secante
        self.setCentralWidget(self.secant_window)

        # Boton para ir al inicio
        back_button = QPushButton("Volver al Inicio", self.secant_window)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(lambda: (
            self.secant_window.deleteLater(),
            self.go_main()
        ))

        layout = self.secant_window.layout() \
            if self.secant_window.layout() \
            else QVBoxLayout(self.secant_window)
        layout.addWidget(back_button)
        self.secant_window.setLayout(layout)

    def open_inversion_method(self):
        self.inversion_window = InversionWindow()
        self.setCentralWidget(self.inversion_window)
        back_button = QPushButton("Volver al Inicio", self.inversion_window)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(lambda: (
            self.inversion_window.deleteLater(),
            self.go_main()
        ))

        layout = self.inversion_window.layout() \
            if self.inversion_window.layout() \
            else QVBoxLayout(self.inversion_window)
        layout.addWidget(back_button)
        self.inversion_window.setLayout(layout)

    def open_pivot_gauss_method(self):
        self.pivot_gauss_window = PivotGaussWindow()
        self.setCentralWidget(self.pivot_gauss_window)
        back_button = QPushButton("Volver al Inicio", self.pivot_gauss_window)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(lambda: (
            self.pivot_gauss_window.deleteLater(),
            self.go_main()
        ))
        layout = self.pivot_gauss_window.layout() \
            if self.pivot_gauss_window.layout() \
            else QVBoxLayout(self.pivot_gauss_window)
        layout.addWidget(back_button)
        self.pivot_gauss_window.setLayout(layout)

    def open_intercambio_method(self):
        self.intercambio_window = IntercambioMethodWindow()
        self.setCentralWidget(self.intercambio_window)
        back_button = QPushButton("Volver al Inicio", self.intercambio_window)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(lambda: (
            self.intercambio_window.deleteLater(),
            self.go_main()
        ))
        layout = self.intercambio_window.layout() \
            if self.intercambio_window.layout() \
            else QVBoxLayout(self.intercambio_window)
        layout.addWidget(back_button)
        self.intercambio_window.setLayout(layout)

    def open_jacobi_method(self):
        self.jacobi_window = JacobiMethodWindow()
        self.setCentralWidget(self.jacobi_window)
        back_button = QPushButton("Volver al Inicio", self.jacobi_window)
        back_button.setObjectName("backButton")
        back_button.clicked.connect(lambda: (
            self.jacobi_window.deleteLater(),
            self.go_main()
        ))
        layout = self.jacobi_window.layout() \
            if self.jacobi_window.layout() \
            else QVBoxLayout(self.jacobi_window)
        layout.addWidget(back_button)
        self.jacobi_window.setLayout(layout)

    def go_main(self):
        self.secant_window = None
        self.inversion_window = None
        self.jacobi_window = None
        self.pivot_gauss_window = None
        self.intercambio_window = None
        #Volvemos a iniciar el metodo initUi
        self.initUI()
