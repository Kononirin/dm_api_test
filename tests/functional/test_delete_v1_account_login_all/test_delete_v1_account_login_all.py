def test_get_v1_account_auth(
        auth_account_helper
):
    auth_account_helper.dm_account_api.account_api.get_v1_account()
    response = auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all()
    assert response.status_code == 204, "Пользователь не смог выйти из аккаунта со всех устройств"
