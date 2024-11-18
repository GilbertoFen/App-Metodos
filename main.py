import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
#Metodo para abrir el archivo de estilos
def apply_stylesheet(app):
    with open("styles.qss", "r") as f:
        stylesheet = f.read()
        app.setStyleSheet(stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
