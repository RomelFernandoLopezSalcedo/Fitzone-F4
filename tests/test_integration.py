import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from src.ui.login_view import LoginView
from tests.conftest import auto_close_messagebox


@pytest.mark.integration
def test_login_admin_flow(qtbot, qapp, auth_service_tmp, monkeypatch):
    """
    Prueba completa: login como admin, se abre el panel de administración
    y se verifica que la tabla contiene usuarios.
    """
    # Preparar datos
    auth_service_tmp.create_user("Admin", "admin@fit.com", "admin123", "admin")
    auth_service_tmp.create_user("User1", "user1@fit.com", "user", "user")

    # Evitar que se cierren ventanas
    monkeypatch.setattr(LoginView, "close", lambda self: None)
    from src.ui.admin_view import AdminView
    monkeypatch.setattr(AdminView, "show", lambda self: self.setVisible(True))

    # Login
    login = LoginView()
    login.auth = auth_service_tmp
    qtbot.addWidget(login)
    login.show()
    qtbot.wait(800)

    qtbot.keyClicks(login.email_input, "admin@fit.com")
    qtbot.keyClicks(login.password_input, "admin123")

    # Programar cierre automático de cualquier MessageBox (aunque no debería aparecer en login exitoso)
    auto_close_messagebox(qtbot, delay=600, accept=True)

    qtbot.mouseClick(login.btn_login, Qt.LeftButton)
    qtbot.wait(800)

    # Verificar que se creó la ventana admin
    assert hasattr(login, 'admin')
    admin_window = login.admin
    qtbot.addWidget(admin_window)
    admin_window.show()
    qtbot.wait(800)

    # Verificar contenido
    assert admin_window.table.rowCount() >= 2