from pprint import pprint
import requests
from json import loads


def test_post_v1_account():
    # Регистрация пользователя
    login = 'kirka5'
    email = f'{login}@mail.ru'
    password = 'qwerty123'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 201, "Пользователь не был создан"

    # Получить письма из почтового сервера
    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)
    # pprint(response.json())

    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = None
    for item in response.json()['items']:
        user_data = (loads(item['Content']['Body']))
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, "Пользователь не смог авторизоваться"
