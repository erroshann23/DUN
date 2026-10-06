from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)


class InputPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("PROJECT INPUT")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel(
            "Enter project input parameters and calculate the required values."
        )

        calculate_button = QPushButton("CALCULATE")

        calculate_button.clicked.connect(self.calculate)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addSpacing(20)
        layout.addWidget(calculate_button)
        layout.addStretch()

    def calculate(self):
        print("Calculation button clicked")