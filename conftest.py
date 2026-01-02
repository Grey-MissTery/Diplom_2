import pytest
from methods.user_methods import UserMethods
from methods.order_methods import OrderMethods


@pytest.fixture
def create_user():
    """
    Фикстура создаёт нового пользователя и возвращает его данные.
    После завершения теста тестовые данные удаляются.
    """
    user_methods = UserMethods()
    status_code, response_data, payload = user_methods.post_create_user()

    # Если пользователь успешно создан, формируем user_data
    if status_code == 200 and response_data.get("success"):
        user_data = {
            "email": response_data["user"]["email"],
            "password": payload["password"],  # Пароль из payload, не из response!
            "name": response_data["user"]["name"],
            "accessToken": response_data["accessToken"],  # Токен уже получен при создании
            "refreshToken": response_data.get("refreshToken", "")
        }
    else:
        # Если создание не удалось, всё равно возвращаем данные для теста
        user_data = {
            "email": payload.get("email", ""),
            "password": payload.get("password", ""),
            "name": payload.get("name", ""),
            "accessToken": "",
            "refreshToken": ""
        }

    yield status_code, response_data, user_data

    # Удаляем пользователя только если он был успешно создан и есть токен
    if user_data.get("accessToken"):
        try:
            user_methods.delete_user(
                access_token=user_data["accessToken"],
                json_data={"email": user_data["email"], "password": user_data["password"]}
            )
        except Exception as e:
            # Логируем ошибку удаления, но не падаем
            print(f"Ошибка при удалении пользователя: {e}")


@pytest.fixture
def authorization_user(create_user):
    """
    Фикстура возвращает данные авторизованного пользователя.
    Пользователь уже создан и имеет валидные токены.
    """
    status_code, response_data, user_data = create_user
    
    # Проверяем успешность создания пользователя
    assert status_code == 200, f"Ожидался статус 200 при создании пользователя, получен {status_code}"
    assert response_data.get("success") is True, "Пользователь не был создан успешно"
    
    # Проверяем наличие необходимых данных
    assert "accessToken" in user_data and user_data["accessToken"], "Отсутствует accessToken"
    assert "email" in user_data, "Отсутствует email"
    
    yield user_data


@pytest.fixture
def ingredients():
    """Фикстура возвращает список ингредиентов."""
    status_code, response = OrderMethods().get_ingredients()
    if status_code == 200 and response.get("success"):
        return response.get("data", [])
    return []
