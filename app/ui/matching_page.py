from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class MatchingPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("SHEET MATCHING")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel(
            "Generated odd/even sheets and matching results will be displayed here."
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()