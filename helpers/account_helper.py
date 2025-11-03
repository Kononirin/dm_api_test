import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активацонного токена")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.user_login(login=login, password=password)
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        token = self.user_login(login=login, password=old_password)
        self.dm_account_api.account_api.post_v1_account_password(
            json_data={
                "login": login,
                "email": email
            },
            headers={
                "x-dm-auth-token": token.headers["x-dm-auth-token"]
            }
        )
        token = self.get_reset_token_by_login(login=login)
        self.dm_account_api.account_api.put_v1_account_password(
            json_data={
                "login": login,
                "oldPassword": old_password,
                "newPassword": new_password,
                "token": token
            }
        )

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не был создан"
        start_time = time.time()
        token = self.get_mails_and_activation_token_by_login(login=login)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации токена превышено"
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.activate_user_by_token(token)
        assert response.status_code == 200, "Пользователь не был активирован"

        return response

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        # Авторизация пользователя
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.headers["x-dm-auth-token"], "Токен для пользователя не был получен"
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        return response

    def change_email(
            self,
            json_data
    ):
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Имейл пользователя не изменён"

    def activate_user_by_token(
            self,
            token
    ):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

        return response

    @retrier
    def get_mails_and_activation_token_by_login(
            self,
            login
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        for item in response.json()['items']:
            user_data = (loads(item['Content']['Body']))
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @retrier
    def get_reset_token_by_login(
            self,
            login
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                # Проверяем наличие ключа
                if 'ConfirmationLinkUri' in user_data:
                    token = user_data['ConfirmationLinkUri'].split('/')[-1]
                    break
        return token
