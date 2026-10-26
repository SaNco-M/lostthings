# LostThings — Сервис поиска потерянных животных

**Лабораторная работа № 0**

Веб-приложение для публикации и поиска объявлений о потерянных и найденных животных.

## Архитектура и технологии

- **Database:** PostgreSQL 15, Docker Compose, persistent volume `postgres_data`
- **Backend:** FastAPI, SQLAlchemy 2.0 (AsyncIO), Alembic, Pydantic V2
- **Frontend:** SPA-клиент на HTML5, CSS3 и Vanilla JavaScript

## Быстрый старт

### 1. Настройка окружения

Создайте файл `.env` на основе шаблона.

**Linux / macOS:**
```bash
cp backend/.env.example backend/.env
```

**Windows (PowerShell):**
```powershell
Copy-Item backend/.env.example backend/.env
```

Настройте переменные окружения и параметры подключения к базе данных в `backend/.env`.

### 2. Запуск базы данных

Из корневой директории проекта выполните:

```bash
docker compose up -d postgresSQL
```

### 3. Запуск бэкенда

Перейдите в директорию `backend`, установите зависимости и выполните миграции:

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
python seed.py
uvicorn app.main:app --reload
```

После запуска API будет доступно по адресу:

- **API:** http://127.0.0.1:8000
- **Swagger UI:** http://127.0.0.1:8000/docs

### 4. Запуск фронтенда

Откройте файл `frontend/index.html` в браузере.