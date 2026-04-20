from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QGridLayout,
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt


class UserView(QWidget):
    def __init__(self, user, auth_service=None):
        super().__init__()
        self.user = user
        self.auth = auth_service

        self.setWindowTitle("FitZone - Mi Entrenamiento")
        self.setGeometry(200, 100, 900, 600)
        self.setMinimumSize(800, 500)
        self.setStyleSheet("background-color: #f8f9fa;")

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Cabecera
        header = self._create_header()
        main_layout.addLayout(header)

        # Contenido con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)

        welcome_card = self._create_welcome_card()
        content_layout.addWidget(welcome_card)

        training_section = self._create_training_plan()
        content_layout.addWidget(training_section)

        stats_card = self._create_stats_card()
        content_layout.addWidget(stats_card)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def _create_header(self):
        header_layout = QHBoxLayout()
        logo_label = QLabel("🏋️ FitZone")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d3436;")
        header_layout.addWidget(logo_label)
        header_layout.addStretch()

        logout_btn = QPushButton("Cerrar sesión")
        logout_btn.setFixedWidth(140)
        logout_btn.setStyleSheet(self._button_style("#d63031", hover_color="#c0392b"))
        logout_btn.clicked.connect(self.logout)
        header_layout.addWidget(logout_btn)

        return header_layout

    def _create_welcome_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: 1px solid #e0e0e0; }")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(30, 20, 30, 20)

        text_layout = QVBoxLayout()
        name_label = QLabel(f"¡Hola, {self.user.nombre}!")
        name_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2d3436;")
        text_layout.addWidget(name_label)

        if self.user.membership:
            member_type = self.user.membership.get("type", "Básico")
            status_text = f"Membresía {member_type} activa"
        else:
            status_text = "Sin membresía activa"

        status_label = QLabel(status_text)
        status_label.setStyleSheet("font-size: 16px; color: #636e72;")
        text_layout.addWidget(status_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        icon_label = QLabel("💪")
        icon_label.setStyleSheet("font-size: 60px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        return card

    def _create_training_plan(self):
        container = QFrame()
        container.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: 1px solid #e0e0e0; }")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)

        title = QLabel("📅 Plan de entrenamiento semanal")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2d3436;")
        layout.addWidget(title)

        week_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        exercises = [
            "Pecho y tríceps",
            "Espalda y bíceps",
            "Piernas y glúteos",
            "Hombros y abdominales",
            "Cardio + HIIT",
            "Estiramientos / Yoga",
            "Descanso"
        ]

        grid = QGridLayout()
        grid.setVerticalSpacing(12)
        grid.setHorizontalSpacing(20)

        for i, (day, ex) in enumerate(zip(week_days, exercises)):
            row = i // 2
            col = (i % 2) * 2

            day_lbl = QLabel(day)
            day_lbl.setStyleSheet("font-weight: bold; color: #0984e3; font-size: 14px;")
            grid.addWidget(day_lbl, row, col)

            ex_lbl = QLabel(ex)
            ex_lbl.setStyleSheet("color: #2d3436; font-size: 14px;")
            grid.addWidget(ex_lbl, row, col + 1)

        layout.addLayout(grid)

        details_btn = QPushButton("Ver rutina completa")
        details_btn.setStyleSheet(self._button_style("#00b894", hover_color="#00a381"))
        details_btn.setFixedWidth(180)
        details_btn.clicked.connect(self.show_routine_details)
        layout.addWidget(details_btn, alignment=Qt.AlignRight)

        return container

    def _create_stats_card(self):
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; border: 1px solid #e0e0e0; }")
        layout = QHBoxLayout(card)
        layout.setContentsMargins(30, 20, 30, 20)

        progress_layout = QVBoxLayout()
        progress_title = QLabel("Progreso semanal")
        progress_title.setStyleSheet("font-weight: bold; color: #2d3436; font-size: 16px;")
        progress_layout.addWidget(progress_title)

        progress_bar = QProgressBar()
        progress_bar.setValue(65)
        progress_bar.setTextVisible(True)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #ecf0f1;
                border-radius: 10px;
                height: 20px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #0984e3;
                border-radius: 10px;
            }
        """)
        progress_bar.setFormat("%p% completado")
        progress_layout.addWidget(progress_bar)

        layout.addLayout(progress_layout)
        layout.addSpacing(40)

        stats_layout = QGridLayout()
        stats_layout.setHorizontalSpacing(30)

        days_label = QLabel("Días este mes")
        days_label.setStyleSheet("color: #636e72;")
        days_value = QLabel("12")
        days_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #2d3436;")

        cal_label = QLabel("Calorías (aprox)")
        cal_label.setStyleSheet("color: #636e72;")
        cal_value = QLabel("4,200")
        cal_value.setStyleSheet("font-size: 22px; font-weight: bold; color: #2d3436;")

        stats_layout.addWidget(days_label, 0, 0)
        stats_layout.addWidget(days_value, 1, 0)
        stats_layout.addWidget(cal_label, 0, 1)
        stats_layout.addWidget(cal_value, 1, 1)

        layout.addLayout(stats_layout)
        layout.addStretch()

        return card

    def show_routine_details(self):
        QMessageBox.information(
            self,
            "Rutina completa",
            "Aquí se mostrarían ejercicios detallados con series, repeticiones y descanso.\n¡Próximamente!"
        )

    def logout(self):
        from src.ui.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()

    def _button_style(self, bg_color, hover_color=None):
        if hover_color is None:
            hover_color = self._darken_color(bg_color)
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: white;
                padding: 10px 15px;
                border-radius: 10px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """

    def _darken_color(self, hex_color, factor=0.7):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"