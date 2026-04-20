from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class TrainingCard(QFrame):
    def __init__(self, texto):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 15px;
                border: 1px solid #dcdde1;
                padding: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        self.label = QLabel(texto)
        layout.addWidget(self.label)

        self.setLayout(layout)