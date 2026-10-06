from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class HealPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("HEAL CUTTING LENGTH CALCULATION")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel(
            "Matched sheet lengths, C values and shearing allowance "
            "will be used to calculate HEAL cutting lengths."
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()