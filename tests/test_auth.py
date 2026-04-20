import pytest


@pytest.mark.unit
def test_create_user(auth_service_tmp):
    user = auth_service_tmp.create_user("Ana Perez", "ana@fit.com", "secreta", "user")
    assert user.get_name() == "Ana Perez"
    assert user.get_email() == "ana@fit.com"
    assert user.get_role() == "user"
    assert len(auth_service_tmp.users) == 1
    assert auth_service_tmp.id_counter == 2


@pytest.mark.unit
def test_login_success(auth_service_tmp):
    auth_service_tmp.create_user("Carlos", "carlos@fit.com", "clave123", "admin")
    user = auth_service_tmp.login("carlos@fit.com", "clave123")
    assert user is not None
    assert user.get_name() == "Carlos"


@pytest.mark.unit
def test_login_wrong_password(auth_service_tmp):
    auth_service_tmp.create_user("Eva", "eva@fit.com", "correcta", "user")
    user = auth_service_tmp.login("eva@fit.com", "incorrecta")
    assert user is None


@pytest.mark.unit
def test_login_nonexistent_user(auth_service_tmp):
    user = auth_service_tmp.login("noexiste@mail.com", "pass")
    assert user is None


@pytest.mark.unit
def test_add_payment(auth_service_tmp):
    auth_service_tmp.create_user("Luis", "luis@fit.com", "123", "user")
    result = auth_service_tmp.add_payment("luis@fit.com", 50.0, "efectivo")
    assert result is True
    user = auth_service_tmp.users[0]
    assert len(user.payments) == 1
    assert user.payments[0]["value"] == 50.0
    assert user.payments[0]["method"] == "efectivo"


@pytest.mark.unit
def test_delete_user(auth_service_tmp):
    auth_service_tmp.create_user("Borrar", "borrar@fit.com", "123", "user")
    assert len(auth_service_tmp.users) == 1
    result = auth_service_tmp.delete_user("borrar@fit.com")
    assert result is True
    assert len(auth_service_tmp.users) == 0