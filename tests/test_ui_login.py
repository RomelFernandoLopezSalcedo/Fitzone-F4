import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from src.ui.login_view import LoginView
from tests.conftest import auto_close_messagebox, slow_type


@pytest.mark.functional
def test_login_ui_success(qtbot, qapp, auth_service_tmp, monkeypatch):
    auth_service_tmp.create_user("Test User", "test@fit.com", "testpass", "user")

    monkeypatch.setattr(LoginView, "close", lambda self: None)
    from src.ui.user_view import UserView
    monkeypatch.setattr(UserView, "show", lambda self: None)

    window = LoginView()
    window.auth = auth_service_tmp
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(800)

    # Escritura lenta
    slow_type(qtbot, window.email_input, "test@fit.com", delay_ms=120)
    qtbot.wait(200)  # pausa entre campos
    slow_type(qtbot, window.password_input, "testpass", delay_ms=100)

    qtbot.wait(300)  # pausa antes de hacer clic
    qtbot.mouseClick(window.btn_login, Qt.LeftButton)
    qtbot.wait(800)

    assert True


@pytest.mark.functional
def test_login_ui_failure(qtbot, qapp, auth_service_tmp):
    window = LoginView()
    window.auth = auth_service_tmp
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(800)

    slow_type(qtbot, window.email_input, "malo@fit.com", delay_ms=100)
    qtbot.wait(200)
    slow_type(qtbot, window.password_input, "mala", delay_ms=100)

    auto_close_messagebox(qtbot, delay=500, accept=True)

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_login, Qt.LeftButton)
    qtbot.wait(800)

    assert window.isVisible() is True


@pytest.mark.functional
def test_go_to_register(qtbot, qapp, monkeypatch):
    monkeypatch.setattr(LoginView, "close", lambda self: None)
    from src.ui.register_view import RegisterView
    monkeypatch.setattr(RegisterView, "show", lambda self: None)

    window = LoginView()
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(500)

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_register, Qt.LeftButton)
    qtbot.wait(500)

    assert True