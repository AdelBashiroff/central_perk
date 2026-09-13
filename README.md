# ☕ Central Perk

Платформа для фанатов сериала "Друзья" (Friends).

![Django](https://img.shields.io/badge/Django-4.2-green)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Docker](https://img.shields.io/badge/Docker-ready-blue)

---

## 📖 О проекте

**Central Perk** — это веб-приложение для фанатов сериала "Друзья". Здесь можно:
- 📝 Делиться любимыми цитатами
- 💬 Обсуждать серии
- ❤️ Ставить лайки
- 👥 Находить друзей
- 🔔 Получать уведомления

### Целевая аудитория

- Фанаты сериала "Друзья"
- Люди, любящие цитаты и юмор

### Проблема, которую решаем

Фанатам "Друзей" негде собрать любимые цитаты, обсудить серии и найти единомышленников. Central Perk — это единое место для всего этого.

---

## 🚀 Функциональность

- ✅ Регистрация и аутентификация
- ✅ OAuth2 (GitHub, VK)
- ✅ Профиль пользователя
- ✅ Django Channels
- ✅ CRUD для цитат
- ✅ CRUD для обсуждений
- ✅ Комментарии
- ✅ Лайки
- ✅ API (DRF + Swagger)
- ✅ Docker
- ✅ CI (GitHub Actions)
- ✅ Тесты

---

## 🛠️ Технологии

| Технология | Версия | Зачем |
|------------|--------|-------|
| **Python** | 3.11 | Язык |
| **Django** | 4.2 | Backend |
| **PostgreSQL** | 15 | БД |
| **Redis** | 7 | Хранилище для Channels  |
| **Docker** | 24+ | Контейнеризация |
| **DRF** | 3.14 | API |
| **drf-spectacular** | 0.27 | Swagger |
| **dj-rest-auth** | 5.0 | Аутентификация |
| **Channels** | 4.0 | WebSocket |

---

## 📦 Установка и запуск

### Вариант 1: Через Docker (рекомендуется)

#### 1. Установите Docker Desktop

- [macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Linux](https://docs.docker.com/desktop/install/linux-install/)

#### 2. Клонируйте репозиторий

```bash
git clone https://github.com/AdelBashiroff/central_perk.git
cd central_perk
```

#### 3. Запустите Docker

```bash
docker compose up --build
```

#### 4. Откройте в браузере

```
http://127.0.0.1:8000/
```
---

### Вариант 2: Локально

#### 1. Клонируйте репозиторий

```bash
git clone https://github.com/AdelBashiroff/central_perk.git
cd central_perk
```

#### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# или
venv\Scripts\activate  # Windows
```

#### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

#### 4. Установите PostgreSQL

```bash
# macOS
brew install postgresql@14
brew services start postgresql@14

# Ubuntu
sudo apt install postgresql
sudo systemctl start postgresql
```

#### 5. Создайте БД

```bash
createdb central_perk
```

#### 6. Создайте `.env`

```env
SECRET_KEY=django-insecure-local-key
DEBUG=True
DB_NAME=central_perk
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

#### 7. Примените миграции

```bash
python manage.py migrate
```

#### 8. Создайте админа

```bash
python manage.py createsuperuser
```

#### 9. Запустите

```bash
python manage.py runserver
```

#### 10. Откройте

```
http://127.0.0.1:8000/
```

---

## 📚 Документация API

После запуска откройте:

- **Swagger:** http://127.0.0.1:8000/api/swagger-ui/
- **ReDoc:** http://127.0.0.1:8000/api/schema/

### Эндпоинты

| Метод | URL | Что делает |
|-------|-----|------------|
| GET | `/api/quotes/` | Список цитат |
| GET | `/api/quotes/1/` | Цитата #1 |
| POST | `/api/quotes/1/like/` | Лайкнуть цитату |
| GET | `/api/characters/` | Список персонажей |
| GET | `/api/users/me/` | Текущий пользователь |
| POST | `/api/auth/` | Вход |
| POST | `/api/auth/registration/` | Регистрация |


---

## 🧪 Тесты

### Запуск локально

```bash
pytest
```

### Запуск в Docker

```bash
docker compose exec web pytest
```

### С покрытием

```bash
pytest --cov=. --cov-report=html
```

**Отчёт:** `htmlcov/index.html`

---

## 🐳 Docker

### Команды

```bash
# Запустить
docker compose up --build

# Запустить в фоне
docker compose up -d

# Остановить
docker compose down

# Логи
docker compose logs -f web

# Выполнить команду
docker compose exec web python manage.py <команда>

# Пересобрать
docker compose up --build --force-recreate
```

---

## 🔄 CI/CD

Проект использует **GitHub Actions** для автоматического тестирования.

При каждом `git push` запускаются:
- ✅ Установка зависимостей
- ✅ Применение миграций
- ✅ Запуск тестов
- ✅ Проверка покрытия

**Статус:** [![Django Tests](https://github.com/AdelBashiroff/central_perk/actions/workflows/tests.yml/badge.svg)](https://github.com/AdelBashiroff/central_perk/actions)

---

## 📁 Структура проекта

```
central_perk/
├── .github/
│   └── workflows/
│       └── tests.yml          # CI
├── accounts/                  # Пользователи
├── api/                       # REST API
├── characters/                # Персонажи
├── project/                    #Настройки Django
├── discussions/               # Обсуждения
├── episodes/                  # Серии
├── friends/                   # Друзья
├── notifications/             # Уведомления
├── quotes/                    # Цитаты
├── reviews/                   # Отзывы
├── templates/                 # Шаблоны
├── tests/                     # Тесты
├── docker-compose.yml         # Docker Compose
├── dockerfile                 # Docker
├── manage.py                  # Django
├── pytest.ini                 # Pytest
└── requirements.txt           # Зависимости
```

---

## 👨‍💻 Автор

**Баширов Адель 11-411**

- GitHub: [@AdelBashiroff](https://github.com/AdelBashiroff)