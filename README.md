### Hexlet tests and linter status:
[![Actions Status](https://github.com/EugeneAnisimov97/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/EugeneAnisimov97/python-project-83/actions)
![workflow_githubaction](https://github.com/EugeneAnisimov97/python-project-83/actions/workflows/pyci.yml/badge.svg)

__Page Analyzer__ - третий проект, разработанный в рамках обучения на курсе Хекслет. Это сайт, который анализирует указанные страницы на SEO-пригодность.

🔗 [Перейти к проекту](https://python-project-83-5noi.onrender.com) | 💻 [Render](https://render.com)

## Описание проекта

**Page Analyzer** – это веб-приложение, которое анализирует указанные страницы на SEO-пригодность, аналогично [PageSpeed Insights](https://pagespeed.web.dev/). 

## Использованные технологии

В данном проекте использовались следующие технологии и библиотеки:

- [**Flask**](https://flask.palletsprojects.com/en/3.0.x/) - фреймворк веб-приложений на Python.
- [**dotenv**](https://pypi.org/project/python-dotenv/) - для управления переменными окружения.
- [**beautifulsoup4 (bs4)**](https://pypi.org/project/beautifulsoup4/) - для парсинга HTML.
- [**urllib**](https://docs.python.org/3/library/urllib.html) - для работы с URL.
- [**requests**](https://pypi.org/project/requests/) - для выполнения HTTP-запросов.
- [**os**](https://pythonworld.ru/moduli/modul-os.html) - модуль для работы с операционной системой.
- [**validators**](https://pypi.org/project/validators/) - для валидации данных.
- [**datetime**](https://docs.python.org/3/library/datetime.html) - для работы с датами и временем.
- [**psycopg2**](https://pypi.org/project/psycopg2/) - для работы с PostgreSQL в Python.

***
## Перед установкой
Для установки и запуска проекта вам потребуется Python версии  3.10 и выше, инструмент для управления зависимостями Poetry и база данных PostgreSQL.

Перед началом использования проекта убедитесь, что вышеописанные утилиты установлены на вашем устройстве.

## Установка

1. Склонируйте репозиторий с проектом на ваше локальное устройство:
```
git clone git@github.com:EugeneAnisimov97/python-project-83.git
```
2. Перейдите в директорию проекта:
```
cd python-project-83
```
3. Установите необходимые зависимости с помощью Poetry:
```
poetry install
```
4. Создайте файл .env, который будет содержать ваши конфиденциальные настройки:

```
Откройте файл .env и ознакомтесь с его содержимым. Замените значение ключей SECRET_KEY и DATABASE_URL.
```
5. Затем запустите команды из database.sql в SQL-консоли вашей базы данных, чтобы создать необходимые таблицы.

***

## Использование
1. Для запуска сервера Flask с помощью Gunicorn выполните команду:

```
make start
```
По умолчанию сервер будет доступен по адресу http://0.0.0.0:8000.

2. Также можно запустить сервер локально в режиме разработки с активным отладчиком:

```
make dev
```
Сервер для разработки будет доступен по адресу http://127.0.0.1:5000.

Чтобы добавить новый сайт, введите его адрес в форму на главной странице. Введенный адрес будет проверен и добавлен в базу данных.

После добавления сайта можно начать его проверку. На странице каждого конкретного сайта появится кнопка, и нажав на нее, вы создадите запись в таблице проверки.

Все добавленные URL можно увидеть на странице /urls.
***
## Способы использования
Проект можно использовать локально и онлайн (например с помощью стороннего сервиса [render.com](https://dashboard.render.com/)). Следуйте инструкциям с официального сайта для добавления веб-сервиса и онлайн базы данных. Не забывайте про использования переменных окружения.

***

## Контакты

- Автор: Eugene Anisimov
- [GitHub](https://github.com/EugeneAnisimov97)
- [Email](zero0061@mail.ru)
- [telegram](https://t.me/Eugene_Anisimov)