import requests, random


class TestCreditRepay:
    # ================================ авторизуемся под админом чтобы создать пользователя
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

    # ======================= создаем пользователя, прокинули токен админа, чтобы создать юзера ROLE_CREDIT_SECRET
    username_1 = f"Malkin{random.randint(100, 999)}"
    create_user_response = requests.post(
        url="http://localhost:4111/api/admin/create",
        json={
            "username": username_1,
            "password": "Pas!sw0rd",
            "role": "ROLE_CREDIT_SECRET"
        },
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {admin_token}"
        }
    )
    assert create_user_response.status_code == 200

    # ======================= авторизовались пользователем, которого создали, взяли токен юзера
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
    user_token = login_user_response.json().get("token")  # get TOKEN user

    # ======================= создаем счет для юзера с помощью его токена
    create_account_response = requests.post(
        url="http://localhost:4111/api/account/create",
        headers={
            "accept": "*/*",
            "Authorization": f"Bearer {user_token}",
        }

    )
    assert create_account_response.status_code == 201
    assert create_account_response.json()["balance"] == 0

    accountId = create_account_response.json()["id"]  # get ID user

    #===================================== запрашиваем кредит
    credit_response = requests.post(
        url="http://localhost:4111/api/credit/request",
        json={
            "accountId": accountId,
            "amount": 10000,
            "termMonths": 12
        },
        headers={
            "accept": "*/*",
            "Authorization": f"Bearer {user_token}",
        }
    )
    assert credit_response.status_code == 201
    assert credit_response.json().get("balance") == 10000

    creditID = credit_response.json()["creditId"]     # get credit ID number
    print(f'Кредитный ID: {creditID}')

    # тесты =====================================

    def test_credit_repay_negative(self):
        repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": TestCreditRepay.creditID,
                "accountId": TestCreditRepay.accountId,
                "amount": 5000,
            },
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {TestCreditRepay.user_token}",
            }
        )
        assert repay_response.status_code == 422
        assert "The amount is not enough" in repay_response.json()["error"]

    def test_credit_repay_positive(self):
        repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": TestCreditRepay.creditID,
                "accountId": TestCreditRepay.accountId,
                "amount": 10000,
            },
            headers={
                "accept": "*/*",
                "Authorization": f"Bearer {TestCreditRepay.user_token}",
            }
        )
        assert repay_response.status_code == 200
        assert repay_response.json()["amountDeposited"] == 10000

