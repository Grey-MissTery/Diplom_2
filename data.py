# API service endpoints:
BASE_URL = 'https://stellarburgers.education-services.ru/'
CREATE_USER_URL = f'{BASE_URL}/api/auth/register'
DELETE_USER_URL = f'{BASE_URL}/api/auth/user'        # DELETE - удаление пользователя
LOGIN_USER_URL = f'{BASE_URL}/api/auth/login'
UPDATE_USER_DATA_URL = f'{BASE_URL}/api/auth/user'   # PATCH - обновление данных о пользователе

# Эндпоинты для работы с заказами
# Исправляем копипасту - переименовываем второй одинаковый URL
CREATE_ORDER_URL = f'{BASE_URL}/api/orders'           # POST - создание заказа
GET_USER_ORDERS_URL = f'{BASE_URL}/api/orders'        # GET - получить заказы конкретного пользователя

GET_INGREDIENTS_URL = f'{BASE_URL}/api/ingredients'


# User service error messages:
USER_EXISTS = "User already exists"
REQUIRED_FIELDS = "Email, password and name are required fields"
LOGIN_ERROR = "email or password are incorrect"
AUTH_REQUIRED = "You should be authorised"
NO_INGREDIENTS = "Ingredient ids must be provided"


# Order service invalid data cases:
INVALID_ORDER_DATA = [
    # Полностью некорректные хеши
    (["invalid_hash_1", "invalid_hash_2"], "two_invalid_hashes"),
    # Пустая строка
    ([""], "empty_string_hash"),
    # Смешанные валидные и невалидные хеши (если API поддерживает такую проверку)
    (["invalid_hash_1", "60d3463f7034a000269f45e7"], "mixed_hashes"),
    # Неверный формат хеша
    (["not_a_hash"], "not_a_hash"),
    # Некорректный хеш с правильной длиной
    (["123456789012345678901234"], "wrong_hash_format")
]
