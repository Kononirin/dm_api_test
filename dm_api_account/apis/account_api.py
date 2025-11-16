import allure

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.error_envelope import ErrorEnvelope
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    @allure.step("Зарегистрировать нового пользователя")
    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :param registration:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )

        return response

    @allure.step("Получить данные о пользователе")
    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        :param validate_response:
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs,
        )
        if validate_response:
            data = response.json()

            if response.status_code == 200:
                return UserDetailsEnvelope(**data)
            elif 400 <= response.status_code < 600:
                return ErrorEnvelope(**data)

        return response

    @allure.step("Активировать пользователя")
    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        Activate registered user
        :param validate_response:
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain',
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Изменить имейл зарегистрированного пользователя")
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response = True
    ):
        """
        Change registered user email
        :param change_email:
        :return:
        """

        headers = {
            'accept': 'text/plain',
        }

        response = self.put(
            path=f'/v1/account/email',
            headers=headers,
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Сбросить пароль зарегистрированного пользователя")
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response=True,
            **kwargs
    ):
        """
        Reset registered user password
        :param reset_password:
        :return:
        """
        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response

    @allure.step("Изменить пароль зарегистрированного пользователя")
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=True,
            **kwargs
    ):
        """
        Change registered user password
        :return:
        """
        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())

        return response
