import pytest
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from src.ui.admin_view import AdminView
from tests.conftest import auto_close_messagebox, slow_type


@pytest.fixture
def admin_window(qtbot, qapp, auth_service_tmp):
    """Crea una ventana AdminView con datos de prueba."""
    auth_service_tmp.create_user("Admin Master", "admin@fit.com", "adminpass", "admin")
    auth_service_tmp.create_user("Cliente Uno", "cliente1@fit.com", "pass1", "user")

    window = AdminView(auth_service_tmp)
    qtbot.addWidget(window)
    window.show()
    qtbot.wait(800)
    return window, auth_service_tmp


@pytest.mark.functional
def test_admin_load_users_table(admin_window):
    window, _ = admin_window
    table = window.table
    assert table.rowCount() == 2
    assert table.item(0, 1).text() == "admin@fit.com"
    assert table.item(1, 1).text() == "cliente1@fit.com"


@pytest.mark.functional
def test_admin_create_user_visible(qtbot, admin_window):
    window, auth = admin_window

    slow_type(qtbot, window.name_input, "Nuevo Usuario", delay_ms=80)
    qtbot.wait(150)
    slow_type(qtbot, window.email_input, "nuevo@fit.com", delay_ms=80)
    qtbot.wait(150)
    slow_type(qtbot, window.password_input, "newpass", delay_ms=80)
    qtbot.wait(150)
    window.role_input.setCurrentText("security")
    qtbot.wait(200)

    auto_close_messagebox(qtbot, delay=500, accept=True)

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_add, Qt.LeftButton)
    qtbot.wait(1000)

    assert window.table.rowCount() == 3


@pytest.mark.functional
def test_admin_select_and_delete_user(qtbot, admin_window):
    window, auth = admin_window
    table = window.table

    # Seleccionar segunda fila (cliente1)
    item_rect = table.visualItemRect(table.item(1, 0))
    qtbot.wait(200)
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=item_rect.center())
    qtbot.wait(300)

    assert window.email_input.text() == "cliente1@fit.com"

    auto_close_messagebox(qtbot, delay=500, accept=True)

    qtbot.wait(300)
    qtbot.mouseClick(window.btn_delete, Qt.LeftButton)
    qtbot.wait(800)

    assert window.table.rowCount() == 1


@pytest.mark.functional
def test_admin_edit_user(qtbot, admin_window):
    window, auth = admin_window
    table = window.table

    # Seleccionar primer usuario
    item_rect = table.visualItemRect(table.item(0, 0))
    qtbot.wait(200)
    qtbot.mouseClick(table.viewport(), Qt.LeftButton, pos=item_rect.center())
    qtbot.wait(300)

    window.name_input.clear()
    slow_type(qtbot, window.name_input, "Admin Renombrado", delay_ms=80)
    qtbot.wait(200)

    qtbot.mouseClick(window.btn_update, Qt.LeftButton)
    qtbot.wait(500)

    assert table.item(0, 0).text() == "Admin Renombrado"