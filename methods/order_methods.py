import requests
import allure
from data import *


class OrderMethods:
    """Методы для работы с заказами."""

    @allure.step('Создание заказа с авторизацией')
    def post_create_order_with_token(self, access_token, json_data):
        """Создание заказа авторизованным пользователем."""
        headers = {"Authorization": access_token} if access_token else {}
        response = requests.post(CREATE_ORDER_URL, headers=headers, json=json_data)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, response.text

    @allure.step('Создание заказа без авторизации')
    def post_create_order_no_token(self, json_data):
        """Создание заказа без авторизации."""
        response = requests.post(CREATE_ORDER_URL, json=json_data)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, response.text

    @allure.step('Получение заказов авторизованного пользователя')
    def get_order_with_token(self, access_token):
        """Получение заказов с токеном авторизации."""
        response = requests.get(GET_ORDER_URL, headers={"Authorization": access_token})
        return response.status_code, response.json()

    @allure.step('Получение заказов неавторизованного пользователя')
    def get_order_no_token(self):
        """Получение заказов без токена авторизации."""
        response = requests.get(GET_ORDER_URL)
        return response.status_code, response.json()

    @allure.step('Получение информации об ингредиентах')
    def get_ingredients(self):
        """Получение списка доступных ингредиентов."""
        response = requests.get(GET_INGREDIENTS_URL)
        return response.status_code, response.json()
