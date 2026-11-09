import requests, pytest, random

@pytest.mark.api
class TestTransfer:
    # ====================================== авторизуемся под админом, забираем токен
    login_admin_response = requests.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            "username": "admin",
            "password": "123456"
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    assert login_admin_response.status_code == 200
    admin_token = login_admin_response.json().get("token")

    # ======================= создаем пользователя 1, прокинули токен админа, чтобы создать юзера
    username_1 = f"Malkin{random.randint(100, 999)}"
    create_user_response = requests.post(
        url="http://localhost:4111/api/admin/create",
        json={
            "username": username_1,
            "password": "Pas!sw0rd",
            "role": "ROLE_USER"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"
        }
    )
    assert create_user_response.status_code == 200

    # ======================= авторизовались пользователем 1, которого создали, взяли токен юзера
    login_user_response = requests.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            "username": username_1,
            "password": "Pas!sw0rd",
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    assert login_user_response.status_code == 200
    user_token_1 = login_user_response.json().get("token")       # get TOKEN user 1

    # ======================= создаем счет для юзера1 с помощью его токена
    create_account_response = requests.post(
        url="http://localhost:4111/api/account/create",
        headers={
            "accept": "*/*",
            "Authorization": f"Bearer {user_token_1}",
        }

    )
    assert create_account_response.status_code == 201
    assert create_account_response.json()["balance"] == 0

    accountId_1 = create_account_response.json()["id"]          # get ID user 1

     #========================================== пополнение баланса
    replenish_response = requests.post(
        url="http://localhost:4111/api/account/deposit",
        json={
            "accountId": accountId_1,
            "amount": 3500
        },
        headers={
            "accept": "*/*",
            "Authorization": f"Bearer {user_token_1}",
        }
    )
    assert replenish_response.status_code == 200
    assert replenish_response.json()["balance"] == 3500

# ======================= user 2 ====================================

    # ====================================== авторизуемся под админом, забираем токен
    login_admin_response = requests.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            "username": "admin",
            "password": "123456"
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    assert login_admin_response.status_code == 200
    admin_token = login_admin_response.json().get("token")

    # ======================= создаем пользователя 2, прокинули токен админа, чтобы создать юзера
    username_2 = f"Malkin{random.randint(100, 999)}"
    create_user_response = requests.post(
        url="http://localhost:4111/api/admin/create",
        json={
            "username": username_2,
            "password": "Pas!sw0rd",
            "role": "ROLE_USER"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"
        }
    )
    assert create_user_response.status_code == 200

    # ======================= авторизовались пользователем 2, которого создали, взяли токен юзера
    login_user_response = requests.post(
        url="http://localhost:4111/api/auth/token/login",
        json={
            "username": username_2,
            "password": "Pas!sw0rd",
        },
        headers={
            "accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    assert login_user_response.status_code == 200
    user_token_2 = login_user_response.json().get("token")          # get TOKEN user 1

    # ======================= создаем счет для юзера2 с помощью его токена
    create_account_response = requests.post(
        url="http://localhost:4111/api/account/create",
        headers={
            "accept": "*/*",
            "Authorization": f"Bearer {user_token_2}",
        }

    )
    assert create_account_response.status_code == 201
    assert create_account_response.json()["balance"] == 0

    accountId_2 = create_account_response.json()["id"]   # get ID user 2

    def test_transfer_positive(self):
        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": TestTransfer.accountId_1,
                "toAccountId": TestTransfer.accountId_2,
                "amount": 500
            },
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {TestTransfer.user_token_1}",
                "Content-Type": "application/json"
            }
        )
        assert transfer_response.status_code == 200
        assert transfer_response.json()["fromAccountIdBalance"] == 3000

    @pytest.mark.parametrize(
        "amount, expected_error", [
                   (-1, "Amount must be greater than 0"),
                   (0, "Amount must be greater than 0"),
                   (499, "Amount must be between 500 and 10000"),
                   (10001, "Amount must be between 500 and 10000")
        ]
    )
    def test_transfer_negative(self, amount, expected_error):
        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": TestTransfer.accountId_1,
                "toAccountId": TestTransfer.accountId_2,
                "amount": amount
            },
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {TestTransfer.user_token_1}",
                "Content-Type": "application/json"
            }
        )
        assert transfer_response.status_code == 400

        response_json = transfer_response.json()
        error_message = response_json.get("error","")
        assert expected_error in error_message






