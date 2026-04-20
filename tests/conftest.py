import sys
from pathlib import Path

# Agregar la carpeta raíz al PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import json
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest
from src.services.auth_service import AuthService


@pytest.fixture(scope="session")
def qapp():
    """Garantiza una única instancia de QApplication para todas las pruebas."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(["pytest"])
    yield app


@pytest.fixture
def auth_service_tmp(tmp_path):
    """
    Crea un AuthService que usa archivos temporales aislados.
    No interfiere con los datos reales del proyecto.
    """
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    users_file = data_dir / "users.json"
    logs_file = data_dir / "logs.json"

    users_file.write_text("[]")
    logs_file.write_text("[]")

    service = AuthService()
    service.user_file = str(users_file)
    service.log_file = str(logs_file)

    service.users = []
    service.logs = []
    service.id_counter = 1

    def load_users_mock():
        if os.path.exists(service.user_file):
            with open(service.user_file, "r") as f:
                data = json.load(f)
                service.users = []
                for u in data:
                    from src.models.client import Client
                    user = Client(
                        u["id"],
                        u["name"],
                        u["email"],
                        u["password"],
                        u["role"]
                    )
                    user.payments = u.get("payments", [])
                    user.membership = u.get("membership", None)
                    service.users.append(user)
                    if u["id"] >= service.id_counter:
                        service.id_counter = u["id"] + 1

    def load_logs_mock():
        if os.path.exists(service.log_file):
            with open(service.log_file, "r") as f:
                service.logs = json.load(f)
        else:
            service.logs = []

    service.load_users = load_users_mock
    service.load_logs = load_logs_mock

    service.load_users()
    service.load_logs()

    return service


def auto_close_messagebox(qtbot, delay=500, accept=True):
    """
    Programa el cierre automático de cualquier QMessageBox que aparezca.
    """
    def handle_dialog():
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, QMessageBox) and widget.isVisible():
                if accept:
                    widget.accept()
                else:
                    QTest.keyClick(widget, Qt.Key_Escape)
                break
    QTimer.singleShot(delay, handle_dialog)


def slow_type(qtbot, widget, text, delay_ms=100):
    """
    Simula la escritura humana letra por letra.
    - qtbot: fixture de pytest-qt
    - widget: QLineEdit donde escribir
    - text: texto a escribir
    - delay_ms: milisegundos entre cada carácter (por defecto 100 ms)
    """
    widget.clear()
    widget.setFocus()
    for char in text:
        QTest.keyClick(widget, char)
        qtbot.wait(delay_ms)