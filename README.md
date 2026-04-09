# TeamFinder - Платформа для поиска команды

TeamFinder — это платформа, на которой разработчики, дизайнеры и другие специалисты могут находить единомышленников для совместной работы над pet-проектами.

## Функциональность

### Для всех пользователей:
- Просмотр списка проектов на главной странице
- Просмотр страниц проектов и профилей пользователей
- Регистрация нового аккаунта

### Для авторизованных пользователей:
- Вход/выход из системы
- Создание, редактирование и завершение своих проектов
- Добавление проектов в избранное
- Участие в проектах других пользователей
- Редактирование профиля
- Смена пароля

### Вариант реализации: Вариант 1
- Избранные проекты
- Фильтрация пользователей по критериям:
  - Авторы избранных проектов
  - Авторы проектов, в которых я участвую
  - Пользователи, которым нравятся мои проекты
  - Участники моих проектов

## Запуск проекта

### Требования
- Docker и Docker Compose
- Git

### Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd kittygram-final-ad
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

4. Откройте браузер и перейдите по адресу:
- http://localhost:9000 - основное приложение
- http://localhost:9000/admin - админ-панель Django

### Создание суперпользователя

После запуска контейнеров создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Структура проекта

```
.
├── backend/                 # Django бэкенд
│   ├── kittygram_backend/   # Настройки проекта
│   ├── users/               # Приложение пользователей
│   ├── projects/            # Приложение проектов
│   ├── templates/           # HTML шаблоны
│   ├── static/              # Статические файлы
│   └── manage.py
├── frontend/                # React фронтенд
├── nginx/                   # Конфигурация nginx
├── docker-compose.yml       # Оркестрация Docker
└── README.md
```

## Модели данных

### User (Пользователь)
- email — адрес электронной почты (уникальный)
- name — имя
- surname — фамилия
- avatar — аватарка (генерируется автоматически)
- phone — телефон (уникальный)
- github_url — ссылка на GitHub
- about — описание профиля
- favorites — избранные проекты (ManyToMany)

### Project (Проект)
- name — название проекта
- description — описание
- owner — автор проекта (ForeignKey на User)
- created_at — дата создания
- github_url — ссылка на GitHub
- status — статус (open/closed)
- participants — участники (ManyToMany на User)

## API Endpoints

### Проекты
- `GET /projects/list/` — список всех проектов
- `GET /projects/<id>/` — детальная информация о проекте
- `POST /projects/create-project/` — создание проекта
- `POST /projects/<id>/edit/` — редактирование проекта
- `POST /projects/<id>/complete/` — завершение проекта
- `POST /projects/<id>/toggle-participate/` — участие в проекте
- `POST /projects/<id>/toggle-favorite/` — добавить в избранное

### Пользователи
- `GET /users/list/` — список всех пользователей
- `GET /users/<id>/` — профиль пользователя
- `POST /users/register/` — регистрация
- `POST /users/login/` — вход
- `GET /users/logout/` — выход
- `POST /users/<id>/edit/` — редактирование профиля
- `POST /users/<id>/change-password/` — смена пароля

## Тестирование

Для запуска тестов:
```bash
docker-compose exec backend pytest
```

## Технологии

- **Backend**: Django 3.2.3, Django REST Framework
- **Database**: PostgreSQL 13
- **Frontend**: React
- **Web Server**: nginx
- **Containerization**: Docker, Docker Compose
