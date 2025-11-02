def test_put_v1_account_email(
        account_helper,
        prepare_user
        ):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

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