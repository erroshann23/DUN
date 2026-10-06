from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
)

from ui.input_page import InputPage
from ui.matching_page import MatchingPage
from ui.heal_page import HealPage
from ui.cutting_plan_page import CuttingPlanPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DUN Shearing Plan Automation")
        self.resize(1200, 750)

        self.pages = QStackedWidget()

        self.input_page = InputPage()
        self.matching_page = MatchingPage()
        self.heal_page = HealPage()
        self.cutting_plan_page = CuttingPlanPage()

        self.pages.addWidget(self.input_page)
        self.pages.addWidget(self.matching_page)
        self.pages.addWidget(self.heal_page)
        self.pages.addWidget(self.cutting_plan_page)

        self.status_label = QLabel("Ready")

        self.back_button = QPushButton("Back")
        self.next_button = QPushButton("Next")

        self.back_button.clicked.connect(self.go_back)
        self.next_button.clicked.connect(self.go_next)

        navigation = QHBoxLayout()
        navigation.addWidget(self.back_button)
        navigation.addStretch()
        navigation.addWidget(self.status_label)
        navigation.addStretch()
        navigation.addWidget(self.next_button)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.pages)
        layout.addLayout(navigation)

        self.setCentralWidget(central_widget)

        self.pages.currentChanged.connect(self.update_navigation)

        self.update_navigation(0)

    def go_next(self):
        current = self.pages.currentIndex()

        if current < self.pages.count() - 1:
            self.pages.setCurrentIndex(current + 1)

    def go_back(self):
        current = self.pages.currentIndex()

        if current > 0:
            self.pages.setCurrentIndex(current - 1)

    def update_navigation(self, index):
        page_names = [
            "Project Input",
            "Sheet Matching",
            "HEAL Calculation",
            "Cutting Plan",
        ]

        self.status_label.setText(page_names[index])

        self.back_button.setEnabled(index > 0)
        self.next_button.setEnabled(index < self.pages.count() - 1)