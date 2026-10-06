from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
)


class CuttingPlanPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("CUTTING PLAN")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        description = QLabel(
            "HEAL cutting plan and manual cutting plan will be generated here."
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()