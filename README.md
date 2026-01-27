# Модуль расчёта показателей успеваемости студентов

Учебный проект: backend на FastAPI и frontend на HTML/JS для расчёта и визуализации показателей успеваемости.

## Запуск backend

1. Перейдите в папку `backend`.
2. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
3. Запустите сервер:
   ```
   uvicorn app.main:app --reload
   ```

API будет доступен по адресу: `http://localhost:8000`  
Документация Swagger UI: `http://localhost:8000/docs`

## Запуск frontend

Откройте файл `frontend/index.html` в браузере.
Frontend обращается к backend по адресу `http://localhost:8000`.

## Формат входных данных

### JSON

Пример файла: `data/sample_data.json`

### CSV

Обязательные столбцы:
```
id,name,group,subject,score,date
```

Пример строки:
```
1,Иванов Иван,ПР-21,Математика,85,2025-12-15
```

## Тестирование

Запуск тестов:
```
pytest
```

## Экспорт отчётов

Эндпоинт: `GET /api/export/{format}`  
Поддерживаемые форматы: `json`, `csv`, `txt`

## Публикация на GitHub

1. Откройте терминал в папке проекта (или Git Bash).

2. Инициализация и первый коммит:
   ```
   git init
   git add .
   git commit -m "Initial commit: модуль расчёта показателей успеваемости"
   ```

3. На [github.com](https://github.com) создайте новый репозиторий (без README, без .gitignore).

4. Подключите удалённый репозиторий и отправьте код:
   ```
   git branch -M main
   git remote add origin https://github.com/ВАШ_ЛОГИН/ИМЯ_РЕПОЗИТОРИЯ.git
   git push -u origin main
   ```

   Вместо `ВАШ_ЛОГИН` и `ИМЯ_РЕПОЗИТОРИЯ` подставьте свой логин GitHub и название репозитория.
