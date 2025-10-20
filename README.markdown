# API для управления пользователями

Это API на Django REST Framework для регистрации пользователей, аутентификации, управления профилем и отслеживания истории входов.

## Возможности
- **Регистрация пользователей**: Создание новых пользователей с email и паролем.
- **Активация аккаунта**: Подтверждение аккаунта по уникальному коду.
- **Аутентификация**: Вход с использованием JWT-токенов (access и refresh).
- **Управление профилем**: Просмотр и обновление данных пользователя (имя, email).
- **История входов**: Просмотр логов входа (IP, устройство, страна).

## Технологии
- **Django**: Фреймворк для backend.
- **Django REST Framework**: Для создания API.
- **djangorestframework-simplejwt**: Для аутентификации по JWT-токенам.
- **psycopg2-binary**: Для работы с PostgreSQL.
- **python-decouple**: Для управления конфигурацией через `.env`.
- **requests**: Для запросов к внешним сервисам (например, `ipinfo.io`).
- **django-filter**: Для фильтрации данных в API.
- **Python**: Язык программирования.
- **PostgreSQL**: База данных.

## Установка
1. **Клонируйте репозиторий**:
   git clone <URL_репозитория>
   cd <директория_проекта>

2. **Создайте виртуальное окружение**:
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate

3. **Установите зависимости**:
   Создайте файл `requirements.txt` с содержимым:text
   djangorestframework
   djangorestframework-simplejwt
   psycopg2-binary
   python-decouple
   requests
   django-filter

   *Затем выполните:*\
   pip install -r requirements.txt

4. **Настройте базу данных**:
   - Убедитесь, что PostgreSQL установлен и запущен.
   - Создайте базу данных `test_db`:

     psql -U postgres
     CREATE DATABASE test_db;
     \q


5. **Настройте переменные окружения**:  
   Создайте файл `.env` в корне проекта:env  
   SECRET_KEY=django-insecure-4=ddr=^3qo#%59xn$k!_!n0r)ilp3zmva)q(y4vtikk_yi%&v*  
   DB_NAME=test_db  
   DB_USER=user  
   DB_PASSWORD=1  
   DB_HOST=localhost  
   DB_PORT=5432  
   EMAIL_HOST_USER=amangulov03@gmail.com  
   EMAIL_HOST_PASSWORD=sien gflz vaaa aqxp  
   HOST_FOR_SEND_MAIL=http://localhost:8000  

6. **Примените миграции**:
   python manage.py migrate

7. **Запустите сервер**:
   python manage.py runserver

## Эндпоинты API

*Требуется токены (ДА/Нет)*\
`POST` | `/api/v1/users/register/` - Регистрация нового пользователя | Нет |\
`GET` | `/api/v1/account/activate/?u=<код_активации>` - Активация аккаунта | Нет |\
`POST` | `/api/v1/auth/token/` - Получение токенов (вход) | Нет |\
`POST` | `/api/v1/auth/token/refresh/` | Обновление access-токена | Нет |\
`GET` | `/api/v1/users/me/` - Просмотр профиля | Да |\
`PATCH` | `/api/v1/users/me/` - Обновление профиля | Да |\
`GET` | `/api/v1/logs/login/` - Список логов входа (фильтры по пользователю и датам) | Да |\

### Примеры запросов
1. **Регистрация пользователя**:
   curl -X POST http://127.0.0.1:8000/api/v1/users/register/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@example.com", "password": "MyPass123", "password2": "MyPass123"}'
   **Ответ**: `"Вы успешно зарегистрировались"`

2. **Вход**:
   curl -X POST http://127.0.0.1:8000/api/v1/auth/token/ \
   -H "Content-Type: application/json" \
   -d '{"email": "user@example.com", "password": "MyPass123"}'
   **Ответ**:json
   {
     "refresh": "<refresh_token>",
     "access": "<access_token>"
   }

3. **Просмотр профиля**:
   curl -X GET http://127.0.0.1:8000/api/v1/users/me/ \
   -H "Authorization: Bearer <access_token>"
   **Ответ**:json
   {
     "id": 1,
     "username": "user1",
     "email": "user@example.com"
   }

4. **Просмотр логов входа**:
   curl -X GET "http://127.0.0.1:8000/api/v1/logs/login/?user=1&start_date=2025-10-01" \
   -H "Authorization: Bearer <access_token>"
   **Ответ**:json
   [
     {
       "id": 1,
       "user": 1,
       "timestamp": "2025-10-20T15:49:00+06:00",
       "ip_address": "192.168.1.1",
       "user_agent": "Chrome/5.0",
       "country": "KG"
     }
   ]

## Модели базы данных
- **User**: Пользовательская модель с email (основной идентификатор), именем, фамилией, кодом активации и статусом активности.
- **LoginLog**: Хранит информацию о входах (пользователь, время, IP, устройство, страна).

## Пагинация
- Максимум элементов на странице: 100