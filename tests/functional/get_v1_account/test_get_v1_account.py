import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

@allure.title("Проверка получения данных о новом пользователя")
def test_get_v1_account_auth(
        auth_account_helper
):
    with check_status_code_http():
        response = auth_account_helper.get_account_info(True)
        GetV1Account.check_response_values(response)

@allure.title("Проверка получения данных о пользователя без аутентификации")
def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, "User must be authenticated"):
        account_helper.get_account_info()
