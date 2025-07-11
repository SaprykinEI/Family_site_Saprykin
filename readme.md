# 👨‍👩‍👧‍👦 FamilyTree — семейный сайт на Django

**FamilyTree** — это персонализированная платформа для хранения и отображения информации о родословной семьи. Проект включает:

- Интерактивное генеалогическое древо
- Фотоальбомы и хронику событий
- Систему регистрации пользователей и разграничения ролей (админ, модератор, пользователь)
- Поддержку личных профилей и связей с людьми из дерева

---

## 📁 Структура проекта

Основные приложения проекта:

- `users/` — управление пользователями, профилями, ролями, регистрацией, авторизацией
- `family_tree/` — отображение генеалогического древа,  связей между людьми
- `gallery/` — фото и видеоальбомы, связанные с людьми и событиями
- `events/` — хранение и отображение семейных событий: годовщин, дней рождения, памятных дат

## 🔧 Установка и запуск проекта

### 1. Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/familytree.git
cd familytree
```

### 2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 4. Заполните .env файл согласно файла .env_sample

### 5. Создайте базу данных при помощи команды

```bash
python manage.py create_db
```

### 6. Примените миграции:

```bash
python manage.py migrate
```

### 7. Создайте пользователей

```bash
python manage.py create_admin
```

### 9. Запустите redis

```bash
redis-server 
```

### 10. Запустите сервер

```bash
python manage.py runserver
```

## ⚙️ Используемые технологии и библиотеки
## - Backend:
### Python 3.11+

### Django 4.2+

### mssql-django  
- Драйвер базы данных и бэкенд для Django, позволяющий работать с Microsoft SQL Server.
Позволяет использовать DATABASES с ENGINE = 'mssql' в settings.py.
Полная поддержка миграций, полей моделей и большинства стандартных возможностей Django ORM на MS SQL Server.

### python-dotenv
- Позволяет хранить чувствительные данные (секретные ключи, пароли, конфигурацию) в .env файле.
Удобно для разделения настроек по окружениям.

### Pillow
- Библиотека для обработки изображений на Python.
Применяется для загрузки и обработки пользовательских аватаров, генерации превью и т.д.
Django автоматически использует Pillow для работы с ImageField.

### djangorestframework
- Популярный инструмент для создания RESTful API в Django.
Поддерживает сериализацию моделей, аутентификацию, пагинацию, права доступа.
В нашем проекте используется для отрисовки семейного дерева.

### transliterate
- Для транслитерации текста (например, кириллицы в латиницу).
Удобно при генерации URL-слуг, username на латинице и т. д.

### django-redis
- Позволяет Django использовать Redis как бэкенд для кеширования.
Кеширует страницы в приложении family_tree

### flake8
- Инструмент для статического анализа кода Python.
Проверяет стиль (PEP8), наличие потенциальных ошибок и предупреждений.
Используется для обеспечения единого стиля кода в команде.



### - Frontend:
- HTML5 + CSS3 (адаптированный шаблон Sepia)
- JavaScript (включая Dropzone.js, Treant.js, FullCalendar.js)

## 🔐 Пользователи и роли
Проект использует кастомную модель пользователя User с полем role:

ADMIN — полный доступ, управление пользователями и контентом

MODERATOR — может модерировать контент созданный им же

USER — обычный пользователь: может просматривать контент

Пользовательские поля:

- first_name, last_name, email, avatar
- is_verified — подтверждение почты
- confirmation_code — временный код для подтверждения
- person — связь с объектом Person из древа

## 🧩 Пользовательские команды
В папке users/management/commands доступны команды:

- python manage.py create_admin — создать пользователей
- python manage.py create_db — создать базу данных
- python manage.py drop_db — удалить базу данных (осторожно!)


## 🌐 Как пользоваться
### Регистрация:
- Перейти на страницу /users/register/

Ввести данные
- Получить письмо с подтверждением (если настроена почта)

### Вход:
Страница /users/
- Поддерживается запоминание входа

### Профиль:
- /users/profile/ — страница текущего пользователя

### Смена пароля:
- /users/change_password/

## 📁 Медиа и статика
Все загруженные пользователем изображения (аватары, фотографии) хранятся в MEDIA_ROOT

Статические файлы (CSS, JS, изображения шаблона) — в STATIC_ROOT


## 📝 Автор
FamilyTree — личный проект для документирования семейной истории.
-  Разработчик: Сапрыкин Евгений Игоревич
- Контакты: @Saprykin_Evgeniy
