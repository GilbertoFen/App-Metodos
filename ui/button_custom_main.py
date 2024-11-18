from PyQt6.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text, callback, parent=None):
        super().__init__(text, parent)
        self.callback = callback
        self.setObjectName("customButton")
        # Conectar el clic del botón al método callback
        self.clicked.connect(self.on_click)

    def on_click(self):
        #si self.callback no se ha definido no se cumple la condicion
        if callable(self.callback):
            self.callback()
