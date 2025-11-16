import allure


@allure.title("Проверка выхода из системы со всех устройств")
def test_delete_v1_account_login_all(
        auth_account_helper
):
    auth_account_helper.get_account_info()
    response = auth_account_helper.user_logout_from_all_devices()
    assert response.status_code == 204, "Пользователь не смог выйти из аккаунта со всех устройств"
