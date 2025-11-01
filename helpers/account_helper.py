from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


class AccountHelper:
    # Регистрация пользователя
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

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
        token = self.get_mails_and_activation_token_by_login(login=login)
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

        return response

    def change_email(
            self,
            json_data
    ):
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, "Имейл пользователя не изменён"

    def activate_user_by_token(self, token):
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"

        return response

    def get_mails_and_activation_token_by_login(
            self,
            login
    ):
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = None
        for item in response.json()['items']:
            user_data = (loads(item['Content']['Body']))
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
