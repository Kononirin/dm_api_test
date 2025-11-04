def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.get_account_info()
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def test_get_v1_account_no_auth(
        account_helper
):
    response = account_helper.get_account_info()
    assert response.status_code == 401, "Пользователь успешно авторизовался"
