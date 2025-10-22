import requests


def test_post_v1_account():
    # Регистрация пользователя

    login = 'kirka'
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

    # Получить письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.text)

    # Получить активационный токен
    ...

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/7264c537-a407-4db3-8879-ba7122f24941', headers=headers)
    print(response.status_code)
    print(response.text)

    # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.text)
