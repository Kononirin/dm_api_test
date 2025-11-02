import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True
        )
    ]
)

def test_put_v1_account_email():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'kirka_put_email_34'
    email = f'{login}@mail.ru'
    password = 'qwerty123'

    json_data = {
        'login': login,
        'password': password,
        'email': email,
    }

    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
    account_helper.change_email(json_data=json_data)
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, "Пользователь авторизовался"
    token = account_helper.get_mails_and_activation_token_by_login(login=login)
    account_helper.activate_user_by_token(token)
    account_helper.user_login(login=login, password=password)