import requests, pytest, random

@pytest.mark.api
class TestBalanceReplenishment:  # ===== тест пополнения баланса
    def test_balance_replenishment(self):
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
        token = login_admin_response.json().get("token")

        # ======================= создаем пользователя, прокинули токен админа, чтобы создать юзера
        username = f"Malkin{random.randint(100, 999)}"
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        # ======================= авторизовались пользователем которого создали, взяли токен юзера
        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": username,
                "password": "Pas!sw0rd",
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        # ======================= создаем счет для юзера с помощью его токена
        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {token}",
            }

        )
        assert create_account_response.status_code == 201
        assert create_account_response.json()["balance"] == 0

        accountId = create_account_response.json()["id"]

        #========================================== пополнение баланса
        replenish_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": accountId,
                "amount": 2060
            },
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {token}",
            }
        )

        assert replenish_response.status_code == 200
        assert replenish_response.json()["balance"] == 2060
        print(f'Баланс счета: {replenish_response.json()["balance"]}')
        print(f'ID аккаунта: {accountId}')

