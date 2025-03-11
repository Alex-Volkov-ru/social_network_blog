📝 Social Network Blog

Social Network Blog — это платформа для ведения блогов, где пользователи могут публиковать статьи, комментировать посты и взаимодействовать друг с другом. Проект разработан на Django.

🛠️ Используемые технологии

Язык программирования: Python 3.11+

Фреймворк: Django 4+

База данных: PostgreSQL

Фронтенд: HTML, CSS (Bootstrap)

Авторизация: Django Authentication

Дополнительные библиотеки:

django-ckeditor (редактор для статей)

django-allauth (регистрация и авторизация)

gunicorn (развертывание на сервере)

🚀 Установка и запуск

🔹 1. Локальный запуск (без Docker)

📌 Требования:

Python 3.11+

PostgreSQL 15+

Установленный pip

🔧 Шаги установки:

# 1. Клонируем репозиторий
git clone https://github.com/ВАШ_НИК/social_network_blog.git
cd social_network_blog

# 2. Создаем виртуальное окружение и активируем его
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate  # Для Windows

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Создаем .env файл с настройками (см. ниже)

# 5. Применяем миграции базы данных
python manage.py migrate

# 6. Создаем суперпользователя
python manage.py createsuperuser

# 7. Запускаем сервер разработки
python manage.py runserver

🔹 2. Запуск через Docker

📌 Требования:

Установленный Docker и Docker Compose

🔧 Шаги:

Создайте .env файл (см. раздел Настройка переменных окружения ниже).

Соберите образ и запустите контейнер:

docker-compose up -d --build

Остановить контейнер:

docker-compose down

🔧 Настройка переменных окружения (.env)

Перед запуском создайте .env в корневой папке и добавьте туда переменные:

DJANGO_SECRET_KEY=секретный_ключ
DEBUG=True
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль
POSTGRES_DB=social_blog_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

📄 Структура проекта

/social_network_blog
│── /blog/                  # Приложение для публикаций
│── /users/                 # Приложение для пользователей
│── /static/                # Статические файлы (CSS, JS)
│── /templates/             # HTML-шаблоны
│── /media/                 # Загруженные пользователями файлы
│── manage.py               # Основной файл управления Django
│── requirements.txt        # Список зависимостей
│── .env                    # Переменные окружения
│── Dockerfile              # Файл для сборки Docker-образа
│── docker-compose.yaml     # Конфигурация Docker Compose
│── README.md               # Описание проекта

🛠 Полезные команды Django

🔹 Применить миграции вручную

python manage.py migrate

🔹 Создать суперпользователя

python manage.py createsuperuser

🔹 Собрать статические файлы

python manage.py collectstatic

🔹 Открыть Django shell
