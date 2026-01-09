import random
import string


def generate_user_data():
    """Генерирует случайные данные пользователя."""
    
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    email = f"test_{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = f"User_{generate_random_string(10)}"
    
    return {
        "email": email,
        "password": password,
        "name": name
    }
