def test_put_v1_account_password(
        account_helper,
        prepare_user,
        auth_account_helper
):
    # Изменение пароля
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    print(f'Password 1 is {password}')
    account_helper.user_login(login=login, password=password)
    print(f'Password 2 is {password}')

    account_helper.change_password(login=login, oldPassword=password, newPassword='qwerty456')




