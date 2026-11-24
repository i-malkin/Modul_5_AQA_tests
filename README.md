# Bank API · AQA tests

Автотесты для учебного банковского приложения: **REST API** и **проверки состояния в БД**.
Стек: `Python` · `pytest` · `requests` · `pydantic` · `SQLAlchemy` · `PostgreSQL` · `Allure`

---

## Что покрыто

| Область | Ручки / сценарии | Тесты |
|---|---|---|
| Администратор | `POST /admin/create` (создание юзера) | позитив + 9 негативных (валидация логина и пароля) |
| Авторизация | `POST /auth/token/login` | админ и обычный пользователь |
| Счета | `POST /account/create` | создание счёта |
| Пополнение | `POST /account/deposit` | позитив + границы суммы (1000–9000) |
| Перевод | `POST /account/transfer` | позитив + границы суммы (500–10000) |
| Кредит | `POST /credit/request`, `POST /credit/repay` | выдача и полное погашение, границы (5000–15000), частичное погашение запрещено |

Каждый сценарий проверяется **двумя каналами**: ответ API и состояние базы (остатки счетов, кредиты, операции `deposit`, `transfer`, `credit_issuance`, `credit_repayment`).

---

## Структура проекта

```
src/main/api/
├── tests/         тесты: по файлу на ручку, позитив и негатив
├── steps/         бизнес-шаги: admin_steps, user_steps
├── classes/       api_manager — единая точка доступа ко всем шагам
├── foundation/    ядро: Endpoint (Enum), CrudEndpoint (Protocol),
│                  http_requester → crud_requester → validate_crud_requester
├── models/        pydantic-модели запросов и ответов
├── specs/         заголовки запросов и проверки статус-кодов
├── generators/    RandomModelGenerator (случайные модели по type hints и regex),
│                  test_data — диапазоны сумм, тексты ошибок и генераторы данных
├── db/            слой БД (SQLAlchemy): engine, ORM-модели таблиц, CRUD-запросы
├── fixtures/      pytest-фикстуры: api_manager, юзеры, счета, funded_account
│                  (счёт с депозитом), кредит, db_session, автоочистка данных
└── configs/       Config (Singleton), читает resources/urls.properties
resources/         urls.properties — адреса API и базы данных
conftest.py        регистрация фикстур · pytest.ini — маркеры и настройки запуска
```

**Как это работает:** предусловия (пользователь, счёт, депозит, кредит) готовят фикстуры, поэтому тест состоит из целевого шага и проверок. Шаг вызывается через `api_manager` → steps → requesters (с отчётами Allure). Результат проверяется по ответу API и запросом в БД через `db_session`.

**Принципы кода:**
* Тестовые данные не хардкодятся: суммы генерируются в допустимых диапазонах (`generators/test_data.py`), невалидные значения считаются от границ диапазона.
* Везде проставлены аннотации типов (`api_manager: ApiManager`).
* У каждого `assert` есть сообщение, объясняющее причину падения.

---

## Запуск

1. Подними стенд банка (Docker): API `http://localhost:4111/api`, PostgreSQL `localhost:5432`
2. Установи зависимости: `pip install -r requirements.txt` (нужен Python 3.12+)
3. Запусти тесты: `pytest -m api`
4. Отчёт Allure: `pytest --alluredir=allure-results`, затем `allure serve allure-results`

Маркеры: `api` — API-тесты (с проверками БД), `db` — зарезервирован для отдельных БД-тестов.

---

## Ветки

`junior` → `middle` → `master` — эволюция архитектуры: плоские тесты → слои (models, requests, specs) → фреймворк (foundation, steps, фикстуры, генераторы, БД).
