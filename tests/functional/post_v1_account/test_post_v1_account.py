import pytest

from checkers.http_checkers import (
    check_status_code_http
)
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)


@pytest.mark.parametrize(
    'login, password, email, expected_message', [
        # Короткий пароль
        ("valid_login", "qwe", "valid@email.com", "Validation failed"),
        # Короткий логин
        ("q", "valid_password", "valid@email.com", "Validation failed"),
        # Некорректный email
        ("valid_login", "valid_password", "invalid_email", "Validation failed")]
)
def test_post_v1_account_negative_invalid_credentials(
        account_helper,
        login,
        password,
        email,
        expected_message

):
    with check_status_code_http(400, expected_message):
        account_helper.register_new_user(login=login, password=password, email=email)

    with check_status_code_http(400, "One or more validation errors occurred."):
        account_helper.user_login(login=login, password=password, validate_response=True)
