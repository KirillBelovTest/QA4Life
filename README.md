# QA4Life

## TMS

TMS - Test Managment System - система управления тестированием - ТМС.

В ней есть:

- Тестировщики
- Сценарии

Админ ТМС может добавить, получить, удалить и переименовать тестировщика из системы по имени.
Все остальные действия в системе выполняет сам тестировщик.

Тестировщик может создать, отредактировать, удалить сценарий, шаг и баг.
Это три безнес-сущности системы, которые связаны между собой.

## Установка

Для разработки из репозитория

```bash
git clone https://github.com/kirillbelovtest/QA4Life.git
cd QA4Life
python -m venv .venv
.venv\Scripts\Activate.ps1 # source venv/bin/activate for mac | linux
pip install -e .[dev]
```

## Запуск

```bash
uvicorn tms.api:api --reload
```

## Где API

Создаем тестера

```bash
curl -X POST "http://localhost:8000/tester" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Kirill",
    "level": 1
  }'
```

Получаем тестера

```bash
curl -X GET "http://localhost:8000/tester?name=Kirill"
```

Получаем данные о ТМС

```bash
curl -X GET "http://localhost:8000"
```

## OpenAPI документация

Здесь: `http://localhost:8000/docs`

## Запуск тестов

```bash
pytest .
```