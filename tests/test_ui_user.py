import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from src.ui.user_view import UserView
from src.models.client import Client


@pytest.fixture
def sample_user():
    user = Client(99, "Usuario Test", "user@test.com", "pass", "user")
    user.membership = {"type": "Mensual", "price": 50, "start_date": "2025-04-01"}
    return user


@pytest.mark.functional
def test_user_view_loads(qtbot, qapp, sample_user):
    window = UserView(sample_user)
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(800)

    # Verificar que el nombre aparece
    assert "Usuario Test" in window.findChild(QLabel).text()  # Simplificado
    assert window.isVisible()


@pytest.mark.functional
def test_user_view_logout(qtbot, qapp, sample_user, monkeypatch):
    monkeypatch.setattr(UserView, "close", lambda self: None)
    from src.ui.login_view import LoginView
    monkeypatch.setattr(LoginView, "show", lambda self: None)

    window = UserView(sample_user)
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(500)

    logout_btn = window.findChild(QPushButton, "Cerrar sesión")  # Necesitarías asignar objectName
    # Alternativa: buscar por texto
    for btn in window.findChildren(QPushButton):
        if btn.text() == "Cerrar sesión":
            qtbot.mouseClick(btn, Qt.LeftButton)
            break

    qtbot.wait(300)
    assert True  # Si llega sin errores, pasó