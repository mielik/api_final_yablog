# api_final
REST API для Yatube. Через этот интерфейс смогут работать мобильное приложение или чат-бот; через него же можно будет передавать данные в любое приложение или на фронтенд.

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/mielik/api_final_yatube
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source env/bin/activate
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

### Примеры команд
Получение публикаций:
```
http://127.0.0.1:8000/api/v1/posts/
```
Добавление комментария к посту:
```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
{
"text": "string"
}
```
Возвращает все подписки пользователя, сделавшего запрос:
```
http://127.0.0.1:8000/api/v1/follow/
```
