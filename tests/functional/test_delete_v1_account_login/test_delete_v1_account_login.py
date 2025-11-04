def test_delete_v1_account_login(
        auth_account_helper
):
    auth_account_helper.get_account_info()
    response = auth_account_helper.user_logout()
    assert response.status_code == 204, "Пользователь не смог выйти из аккаунта"
