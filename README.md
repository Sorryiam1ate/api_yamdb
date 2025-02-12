# Название проекта
Проект **YaMDb** собирает отзывы (*Review*) пользователей на произведения (*Titles*).

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (*Category*) может быть расширен администратором.

Произведению может быть присвоен жанр (*Genre*) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (*Review*) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — *рейтинг* (целое число). На одно произведение пользователь может оставить только один отзыв.

## Содержание
- [Технологии](#технологии)
- [Как развернуть проект](#как-развернуть-проект)
- [Примеры запросов](#примеры-запросов)
- [Команда проекта](#команда-проекта)


## Технологии
- [Django REST framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)


## Как развернуть проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:beguuun/api_final_yatube.git
```

```
api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Примеры запросов
Документация по всем доступным запросам к API находится по адресу: http://127.0.0.1:8000/redoc/

Пример запроса:
```sh
GET api/v1/titles/
```

Ответ:
```typescript
{
"count": 123,
"next": "http://api.example.org/accounts/?offset=400&limit=100",
"previous": "http://api.example.org/accounts/?offset=200&limit=100",
"results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "^-$"
        }
      ],
      "category": {
        "name": "string",
        "slug": "^-$"
      }
    }
  ]
}
```

## Команда проекта
Шагиев Рамиль - Backend-разработчик
Сатбаев Алишер - Backend-разработчик
Николаев Максим - Backend-разработчик

Контакты:
- [Рамиль](https://t.me/beguuun)
- [GitHub](https://github.com/beguuun/)

- [Алишер](https://t.me/Sorryiam1ate)
- [GitHub](https://github.com/Sorryiam1ate)

- [Максим](https://t.me/maxim_zlodey000)
- [GitHub](https://github.com/Maxim-Nikolaev-76)