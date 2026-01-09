import pytest
import allure
from data import *
from helpers import *
from methods.order_methods import OrderMethods


class TestOrderCreate:
    """Тесты создания заказов."""

    @allure.title('Создание заказа с авторизацией (2 ингредиента)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_authorized_2_ingredients_success(self, authorization_user, ingredients):
        """Создание заказа авторизованным пользователем с 2 валидными ингредиентами."""
        # Проверяем данные пользователя
        assert authorization_user is not None, "Пользователь должен быть создан"
        assert authorization_user.get("accessToken"), "У пользователя должен быть accessToken"
        
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 2, f"Нужно минимум 2 ингредиента, есть {len(ingredients)}"
        
        user_data = authorization_user
        valid_ingredients = [ingredients[0]["_id"], ingredients[1]["_id"]]
        
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @allure.title('Создание заказа с авторизацией (3 ингредиента)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_authorized_3_ingredients_success(self, authorization_user, ingredients):
        """Создание заказа авторизованным пользователем с 3 валидными ингредиентами."""
        # Проверяем данные пользователя
        assert authorization_user is not None, "Пользователь должен быть создан"
        assert authorization_user.get("accessToken"), "У пользователя должен быть accessToken"
        
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 3, f"Нужно минимум 3 ингредиента, есть {len(ingredients)}"
        
        user_data = authorization_user
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:3]]
        
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @allure.title('Создание заказа с авторизацией (5 ингредиентов)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_authorized_5_ingredients_success(self, authorization_user, ingredients):
        """Создание заказа авторизованным пользователем с 5 валидными ингредиентами."""
        # Проверяем данные пользователя
        assert authorization_user is not None, "Пользователь должен быть создан"
        assert authorization_user.get("accessToken"), "У пользователя должен быть accessToken"
        
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 5, f"Нужно минимум 5 ингредиентов, есть {len(ingredients)}"
        
        user_data = authorization_user
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:5]]
        
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @allure.title('Создание заказа без авторизации (2 ингредиента)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_unauthorized_2_ingredients_success(self, ingredients):
        """Создание заказа без авторизации с 2 валидными ингредиентами."""
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 2, f"Нужно минимум 2 ингредиента, есть {len(ingredients)}"
        
        valid_ingredients = [ingredients[0]["_id"], ingredients[1]["_id"]]
        
        status_code, response = OrderMethods().post_create_order_no_token(
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @allure.title('Создание заказа без авторизации (3 ингредиента)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_unauthorized_3_ingredients_success(self, ingredients):
        """Создание заказа без авторизации с 3 валидными ингредиентами."""
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 3, f"Нужно минимум 3 ингредиента, есть {len(ingredients)}"
        
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:3]]
        
        status_code, response = OrderMethods().post_create_order_no_token(
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @allure.title('Создание заказа без авторизации (5 ингредиентов)')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_unauthorized_5_ingredients_success(self, ingredients):
        """Создание заказа без авторизации с 5 валидными ингредиентами."""
        # Проверяем наличие ингредиентов
        assert len(ingredients) >= 5, f"Нужно минимум 5 ингредиентов, есть {len(ingredients)}"
        
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:5]]
        
        status_code, response = OrderMethods().post_create_order_no_token(
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @pytest.mark.parametrize("invalid_data", INVALID_ORDER_DATA,
                             ids=lambda x: x[1])  # используем второй элемент кортежа как ID теста
    @allure.title(f'Создание заказа с авторизацией и невалидными ингредиентами ({{invalid_data[1]}})')
    @allure.description('ОР: Система возвращает ошибку 400/500')
    def test_create_order_authorized_invalid_ingredients(self, authorization_user,
                                                         invalid_data):
        """Создание заказа с невалидными ингредиентами."""
        user_data = authorization_user
        invalid_ingredients, test_id = invalid_data  # распаковываем кортеж
        
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": invalid_ingredients}
        )
        
        # API может возвращать 400 или 500 для невалидных ингредиентов
        assert status_code in [400, 500], (
            f"Ожидался статус 400 или 500, получен {status_code}\n"
            f"Тип невалидных данных: {test_id}\n"
            f"Использованные ингредиенты: {invalid_ingredients}\n"
            f"Ответ сервера: {response}"
        )

    @allure.title('Создание заказа без ингредиентов')
    @allure.description('ОР: Система возвращает ошибку 400 Bad Request')
    def test_create_order_no_ingredients_error(self, authorization_user):
        """Создание заказа без указания ингредиентов."""
        user_data = authorization_user
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": []}
        )
        
        assert status_code == 400, f"Ожидался статус 400, получен {status_code}"
        assert response["success"] is False, f"Success должен быть False, получен {response.get('success')}"
        assert response["message"] == NO_INGREDIENTS, (
            f"Сообщение: '{response.get('message')}' (ожидалось '{NO_INGREDIENTS}')"
        )


class TestGetOrder:
    """Тесты получения заказов."""

    @allure.title('Получение заказов авторизованного пользователя')
    @allure.description('ОР: Возвращается список заказов пользователя со статусом 200')
    def test_get_user_orders_authorized_success(self, authorization_user, ingredients):
        """Получение заказов авторизованного пользователя."""
        user_data = authorization_user
        
        # Сначала создаем заказ
        if len(ingredients) >= 2:
            ingredient_hashes = [ingredients[0]["_id"], ingredients[1]["_id"]]
            OrderMethods().post_create_order_with_token(
                access_token=user_data["accessToken"],
                json_data={"ingredients": ingredient_hashes}
            )
        
        # Получаем заказы
        status_code, response = OrderMethods().get_order_with_token(
            access_token=user_data["accessToken"]
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert isinstance(response["orders"], list), "orders должен быть списком"
        assert "total" in response, "В ответе должен быть total"
        assert "totalToday" in response, "В ответе должен быть totalToday"

    @allure.title('Получение заказов неавторизованного пользователя')
    @allure.description('ОР: Возвращается ошибка 401 Unauthorized')
    def test_get_user_orders_unauthorized_fail(self):
        """Попытка получения заказов без авторизации."""
        status_code, response = OrderMethods().get_order_no_token()
        
        assert status_code == 401, f"Ожидался статус 401, получен {status_code}"
        assert response["success"] is False, f"Success должен быть False, получен {response.get('success')}"
        assert response["message"] == AUTH_REQUIRED, (
            f"Сообщение: '{response.get('message')}' (ожидалось '{AUTH_REQUIRED}')"
        )
