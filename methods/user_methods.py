import requests
import allure
from data import *
from helpers import *


class UserMethods:
    """Методы для работы с пользователями."""

    @allure.step('Создание пользователя')
    def post_create_user(self, params=None):
        """Создание нового пользователя."""
        if params is None:
            params = generate_user_data()
        response = requests.post(CREATE_USER_URL, json=params)
        return response.status_code, response.json(), params

    @allure.step('Авторизация пользователя в системе')
    def post_login_user(self, json_data):
        """Авторизация существующего пользователя."""
        response = requests.post(LOGIN_USER_URL, json=json_data)
        return response.status_code, response.json()

    @allure.step('Удаление пользователя из системы')
    def delete_user(self, access_token, json_data):
        """Удаление пользователя."""
        response = requests.delete(
            DELETE_USER_URL,
            headers={"Authorization": access_token},
            json=json_data
        )
        return response.status_code, response.json()

    @allure.step('Обновление информации о пользователе')
    def patch_change_user(self, access_token, json_data):
        """Изменение данных пользователя."""
        response = requests.patch(
            UPDATE_USER_DATA_URL,
            headers={"Authorization": access_token},
            json=json_data
        )
        return response.status_code, response.json()
