import requests, pytest, random


@pytest.mark.api
class TestUserLogin:
    # ====================================== тест авторизации под админом
    def test_login_admin(self):
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
        assert login_admin_response.json()["user"]["username"] == "admin"
        assert login_admin_response.json()["user"]["role"] == "ROLE_ADMIN"




    def test_login_user(self):
        # ====================================== авторизуемся под админом
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

        # ====================================== создаем пользователя
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
        assert login_user_response.json()["user"]["username"] == username
        assert login_user_response.json()["user"]["role"] == "ROLE_USER"
