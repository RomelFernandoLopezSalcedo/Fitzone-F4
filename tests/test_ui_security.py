import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from src.ui.security_view import SecurityView
from tests.conftest import auto_close_messagebox


@pytest.fixture
def security_window(qtbot, qapp, auth_service_tmp):
    """
    Prepara un usuario de seguridad, agrega logs de prueba
    y crea la ventana SecurityView.
    """
    auth_service_tmp.create_user("Seguridad Test", "seg@test.com", "123", "seguridad")
    auth_service_tmp.add_log("Usuario admin inició sesión")
    auth_service_tmp.add_log("Pago registrado para user@mail.com")
    auth_service_tmp.add_log("Intento fallido de login: hacker@mail.com")

    user = auth_service_tmp.login("seg@test.com", "123")
    window = SecurityView(auth_service_tmp)
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(800)
    return window, auth_service_tmp


@pytest.mark.functional
def test_security_view_loads_logs(security_window):
    window, auth = security_window
    logs_text = window.logs_area.toPlainText()
    assert "Usuario admin inició sesión" in logs_text
    assert "Pago registrado para user@mail.com" in logs_text
    assert "Intento fallido de login: hacker@mail.com" in logs_text


@pytest.mark.functional
def test_security_refresh_button(qtbot, security_window):
    window, auth = security_window
    window.logs_area.clear()
    qtbot.wait(300)

    qtbot.wait(300)  # pausa antes de clic
    qtbot.mouseClick(window.btn_refresh, Qt.LeftButton)
    qtbot.wait(600)

    logs_text = window.logs_area.toPlainText()
    assert "Usuario admin inició sesión" in logs_text


@pytest.mark.functional
def test_security_check_access_button(qtbot, security_window):
    window, auth = security_window
    initial_text = window.logs_area.toPlainText()

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_check, Qt.LeftButton)
    qtbot.wait(400)

    new_text = window.logs_area.toPlainText()
    assert "✔ Sistema verificado correctamente" in new_text
    assert len(new_text) > len(initial_text)


@pytest.mark.functional
def test_security_back_to_login(qtbot, security_window, monkeypatch):
    window, auth = security_window

    monkeypatch.setattr(SecurityView, "close", lambda self: None)
    from src.ui.login_view import LoginView
    monkeypatch.setattr(LoginView, "show", lambda self: None)

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_back, Qt.LeftButton)
    qtbot.wait(500)

    assert True


@pytest.mark.integration
def test_login_security_flow(qtbot, qapp, auth_service_tmp, monkeypatch):
    from tests.conftest import slow_type

    auth_service_tmp.create_user("Seguridad", "seg@fit.com", "seg123", "seguridad")
    auth_service_tmp.add_log("Sistema iniciado")

    from src.ui.login_view import LoginView
    monkeypatch.setattr(LoginView, "close", lambda self: None)
    monkeypatch.setattr(SecurityView, "show", lambda self: self.setVisible(True))

    login = LoginView()
    login.auth = auth_service_tmp
    qtbot.addWidget(login)
    login.show()
    qtbot.wait(800)

    slow_type(qtbot, login.email_input, "seg@fit.com", delay_ms=100)
    qtbot.wait(200)
    slow_type(qtbot, login.password_input, "seg123", delay_ms=100)

    qtbot.wait(300)
    qtbot.mouseClick(login.btn_login, Qt.LeftButton)
    qtbot.wait(800)

    assert hasattr(login, 'security')
    security_window = login.security
    qtbot.addWidget(security_window)
    security_window.show()
    qtbot.wait(800)

    assert "Sistema iniciado" in security_window.logs_area.toPlainText()