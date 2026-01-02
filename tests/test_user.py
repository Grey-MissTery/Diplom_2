import pytest
import allure
from data import *
from helpers import *
from methods.user_methods import UserMethods


class TestUserCreate:
    """Тесты создания пользователей."""

    @allure.title('Создание уникального пользователя с заполнением всех обязательных полей')
    @allure.description('ОР: Пользователь успешно создан')
    def test_create_user_email_password_name_created_successfully(self, create_user):
        """Создание уникального пользователя со всеми обязательными полями."""
        status_code, response_data, _ = create_user
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response_data["success"] is True, f"Success должен быть True, получен {response_data.get('success')}"
        assert "user" in response_data, "В ответе должен быть объект user"
        assert "accessToken" in response_data, "В ответе должен быть accessToken"
        assert response_data["user"]["email"] is not None, "Email не должен быть пустым"
        assert response_data["user"]["name"] is not None, "Name не должен быть пустым"

    @allure.title('Создание пользователя, который уже зарегистрирован в системе')
    @allure.description('ОР: Пользователь не создан, запрос возвращает ошибку')
    def test_create_user_already_exists_error(self, create_user):
        """Попытка создания пользователя с уже существующим email."""
        _, _, existing_user = create_user
        
        params = {
            "email": existing_user["email"],
            "password": existing_user["password"],
            "name": existing_user["name"]
        }
        status_code, response_data, _ = UserMethods().post_create_user(params)
        
        assert status_code == 403, f"Ожидался статус 403, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == USER_EXISTS, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{USER_EXISTS}')"
        )

    @allure.title('Создание пользователя без заполнения одного из обязательных полей')
    @allure.description('ОР: Пользователь не создан, запрос возвращает ошибку')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_missing_required_field(self, missing_field):
        """Попытка создания пользователя без обязательного поля."""
        user_data = generate_user_data()
        user_data.pop(missing_field)  # Удаляем одно поле
        
        status_code, response_data, _ = UserMethods().post_create_user(params=user_data)
        
        # По документации API при отсутствии обязательных полей возвращается 403
        assert status_code == 403, f"Ожидался статус 403, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == REQUIRED_FIELDS, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{REQUIRED_FIELDS}')"
        )


class TestUserLogin:
    """Тесты авторизации пользователей."""

    @allure.title('Успешная авторизация уже зарегистрированного пользователя')
    @allure.description('ОР: Пользователь успешно авторизован')
    def test_login_existing_user_success(self, create_user):
        """Авторизация существующего пользователя с правильными данными."""
        _, _, user_data = create_user
        
        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json_data=params)
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response_data["success"] is True, f"Success должен быть True, получен {response_data.get('success')}"
        assert "accessToken" in response_data, "В ответе должен быть accessToken"
        assert response_data["user"]["email"] == user_data["email"], (
            f"Email: {response_data.get('user', {}).get('email')} (ожидался {user_data['email']})"
        )
        assert response_data["user"]["name"] == user_data["name"], (
            f"Name: {response_data.get('user', {}).get('name')} (ожидался {user_data['name']})"
        )

    @allure.title('Попытка авторизации пользователя с неверным паролем')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_login_wrong_password_error(self, create_user):
        """Попытка авторизации с неверным паролем."""
        _, _, user_data = create_user
        
        params = {
            "email": user_data["email"],
            "password": "invalid_pass_" + user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json_data=params)
        
        assert status_code == 401, f"Ожидался статус 401, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == LOGIN_ERROR, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{LOGIN_ERROR}')"
        )

    @allure.title('Попытка авторизации пользователя с несуществующим email')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_login_non_existing_email_error(self):
        """Попытка авторизации с несуществующим email."""
        user_data = generate_user_data()
        
        params = {
            "email": "invalid_email_" + user_data["email"],
            "password": user_data["password"]
        }
        status_code, response_data = UserMethods().post_login_user(json_data=params)
        
        assert status_code == 401, f"Ожидался статус 401, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == LOGIN_ERROR, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{LOGIN_ERROR}')"
        )

    @allure.title('Попытка авторизации пользователя без заполнения одного из обязательных полей')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    @pytest.mark.parametrize('missing_field', ['email', 'password'])
    def test_login_missing_required_field(self, missing_field):
        """Попытка авторизации без обязательного поля."""
        user_data = generate_user_data()
        params = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        params.pop(missing_field)  # Удаляем одно поле
        
        status_code, response_data = UserMethods().post_login_user(json_data=params)
        
        assert status_code == 401, f"Ожидался статус 401, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == LOGIN_ERROR, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{LOGIN_ERROR}')"
        )


class TestUserUpdate:
    """Тесты изменения данных пользователя."""

    @allure.title('Изменение информации об авторизованном пользователе')
    @allure.description('ОР: Данные пользователя успешно изменены')
    def test_update_user_data_success(self, authorization_user):
        """Изменение данных авторизованного пользователя."""
        user_data = authorization_user
        new_data = generate_user_data()
        
        update_data = {
            "email": new_data["email"],
            "name": new_data["name"]
        }
        status_code, response_data = UserMethods().patch_change_user(
            access_token=user_data["accessToken"],
            json_data=update_data
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response_data["success"] is True, f"Success должен быть True, получен {response_data.get('success')}"
        assert response_data["user"]["email"] == update_data["email"], (
            f"Email: {response_data.get('user', {}).get('email')} (ожидался {update_data['email']})"
        )
        assert response_data["user"]["name"] == update_data["name"], (
            f"Name: {response_data.get('user', {}).get('name')} (ожидался {update_data['name']})"
        )

    @pytest.mark.parametrize('field,value', [
        ('email', 'updated_email@test.ru'),
        ('name', 'Updated Name')
    ], ids=['update_email', 'update_name'])
    @allure.title('Изменение конкретного поля авторизованного пользователя ({field})')
    @allure.description('ОР: Поле успешно изменено')
    def test_update_user_single_field_success(self, authorization_user, field, value):
        """Изменение отдельного поля пользователя."""
        user_data = authorization_user

        if field == 'email':
            value = generate_user_data()["email"]  # Уникальный email
        else:  # если field == 'name'
            value = 'Updated Name'  # Простое имя
        
        update_data = {field: value}
        status_code, response_data = UserMethods().patch_change_user(
            access_token=user_data["accessToken"],
            json_data=update_data
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response_data["success"] is True, f"Success должен быть True, получен {response_data.get('success')}"
        assert response_data["user"][field] == value, (
            f"{field}: {response_data.get('user', {}).get(field)} (ожидался {value})"
        )

    

    @pytest.mark.parametrize('field,value', [
        ('email', 'unauth_email@test.ru'),
        ('name', 'Unauthorized Name')
    ], ids=['unauth_update_email', 'unauth_update_name'])
    @allure.title('Попытка изменения поля неавторизованного пользователя ({field})')
    @allure.description('ОР: Система возвращает ошибку 401 Unauthorized')
    def test_update_user_single_field_unauthorized(self, field, value):
        """Попытка изменения отдельного поля без авторизации."""
        update_data = {field: value}
        status_code, response_data = UserMethods().patch_change_user(
            access_token="invalid_token",
            json_data=update_data
        )
        
        assert status_code == 401, f"Ожидался статус 401, получен {status_code}"
        assert response_data["success"] is False, f"Success должен быть False, получен {response_data.get('success')}"
        assert response_data["message"] == AUTH_REQUIRED, (
            f"Сообщение: '{response_data.get('message')}' (ожидалось '{AUTH_REQUIRED}')"
        )
