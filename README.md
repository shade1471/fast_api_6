# FastApi + Python, QA-Guru, Lesson 6 Продвинутые техники автоматизации REST

Микросервис на Python + FastAPI

## Установка

Инструкции по установке

```bash
# Клонируйте репозиторий:
git clone https://github.com/shade1471/fast_api_6
cd /fast_api_6

# Установите зависимости:
pip install -r requirements.txt

# Установите переменную APP_URL
Создайте файл .env в корне воспользовавшись шаблоном .env.sample и укажите переменные окружения

# Запустить сервис и БД используя docker
docker-compose up -d
* При запуске сервиса 12 пользователей будет добавлено в БД
* Сервис fastapi запускается на 8000 порту
```

## Запуск авто-тестов

```bash
# В новом окне терминала выполните команду:
Используя аргумент --env=[rc,dev,beta] можно управлять base_url.
По умолчанию, без явной передачи параметра, rc=127.0.0.1:8000

## Авто-тесты endpoint-ов api/users
pytest ./tests/test_fast_api.py
## Smoke авто-тесты
pytest ./tests/test_app_smoke.py
## Авто-тесты по пагинации
pytest ./tests/test_pagination.py
```

## Остановка сервиса

```bash
# Остановите докер контейнер с сервисом и БД
docker-compose down
Либо, если необходимо удалить volume после запуска автотестов
docker-compose down -v 
```

## Endpoint's

```
# Получить данные по пользователю
GET /api/users/{user_id}
Возвращает данные пользователя по ID.
```

```
# Получить данные всех пользователей с возможностью пагинации
GET /api/users/
Возвращает данные пользователя по ID.
```

```
# Создать пользователя
POST /api/users/
Создает нового пользователя. Ожидает JSON с полями name и job.
```

```
# Обновить пользователя
PUT /api/users/{user_id}
Обновляет данные существующего пользователя. Ожидает JSON с полями name и job.
```

```
# Удалить пользователя
DELETE /api/users/{user_id}
Удаляет пользователя по ID.
```

```
# Получить статус сервиса
GET /status
Показывает текущий статус, запущенного сервиса
```

## Предустановленные данные

При запуске сервиса, существует 12 пользователей, id c 1 по 12.
