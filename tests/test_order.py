import pytest
import allure
from data import *
from helpers import *
from methods.order_methods import OrderMethods


class TestOrderCreate:
    """Тесты создания заказов."""

    @pytest.mark.parametrize("ingredient_count", [2, 3, 5],
                             ids=["2_ingredients", "3_ingredients", "5_ingredients"])
    @allure.title(f'Создание заказа с авторизацией (ингредиентов: {{ingredient_count}})')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_authorized_valid_ingredients_success(self, authorization_user,
                                                               ingredients, ingredient_count):
        """Создание заказа авторизованным пользователем с валидными ингредиентами."""
        user_data = authorization_user
        
        # Проверяем, что есть достаточно ингредиентов
        if len(ingredients) < ingredient_count:
            pytest.skip(f"Недостаточно ингредиентов: требуется {ingredient_count}, доступно {len(ingredients)}")
        
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:ingredient_count]]
        status_code, response = OrderMethods().post_create_order_with_token(
            access_token=user_data["accessToken"],
            json_data={"ingredients": valid_ingredients}
        )
        
        assert status_code == 200, f"Ожидался статус 200, получен {status_code}"
        assert response["success"] is True, f"Success должен быть True, получен {response.get('success')}"
        assert "order" in response, "В ответе должен быть объект order"
        assert "name" in response, "В ответе должен быть name"

    @pytest.mark.parametrize("ingredient_count", [2, 3, 5],
                             ids=["2_ingredients", "3_ingredients", "5_ingredients"])
    @allure.title(f'Создание заказа без авторизации (ингредиентов: {{ingredient_count}})')
    @allure.description('ОР: Заказ успешно создан, возвращается номер заказа')
    def test_create_order_unauthorized_valid_ingredients_success(self, ingredients,
                                                                 ingredient_count):
        """Создание заказа без авторизации с валидными ингредиентами."""
        # Проверяем, что есть достаточно ингредиентов
        if len(ingredients) < ingredient_count:
            pytest.skip(f"Недостаточно ингредиентов: требуется {ingredient_count}, доступно {len(ingredients)}")
        
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients[:ingredient_count]]
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
