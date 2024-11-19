import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
#Metodo para abrir el archivo de estilos
def get_resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Usar la función para cargar el archivo QSS
def apply_stylesheet(app):
    qss_file_path = get_resource_path("styles.qss")
    try:
        with open(qss_file_path, "r") as file:
            stylesheet = file.read()
            app.setStyleSheet(stylesheet)
    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo styles.qss")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
