# Bank API · AQA tests

Автотесты REST API учебного банка. **Python · pytest · requests · pydantic · Allure**

## Что проверяем
Админ и пользователь: создание юзера, логин, счёт, пополнение, перевод, кредит и погашение
(`/admin/create`, `/auth/token/login`, `/account/create|deposit|transfer`, `/credit/request|repay`).

## Структура (`src/main/api/`)
```
tests/        тесты, по файлу на ручку (позитив + негатив)
steps/        бизнес-шаги: admin_steps, user_steps
classes/      api_manager: единая точка доступа к шагам
foundation/   ядро: Endpoint (Enum), http / crud / validate requesters
models/       pydantic-модели запросов и ответов
generators/   RandomModelGenerator: случайные данные по type hints и regex
fixtures/     pytest-фикстуры: юзер, счёт, кредит, очистка данных
specs/        заголовки запросов и проверки статус-кодов
configs/      Config (Singleton), читает resources/urls.properties
```

## Запуск
1. Подними стенд банка в Docker (API: `http://localhost:4111/api`)
2. `pip install -r requirements.txt`
3. `pytest -m api`
4. Отчёт: `pytest --alluredir=allure-results`, затем `allure serve allure-results`

## Ветки
`junior` → `middle` → `master` (Senior): эволюция архитектуры от плоских тестов до слоёв и фикстур.

## В планах
Проверки состояния в БД (SQLAlchemy, слой `db/`, маркер `db`).
