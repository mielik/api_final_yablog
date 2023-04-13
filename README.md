# api_final
REST API for Yablog. Through this interface, a mobile application or a chat bot will be able to work; through it it will be possible to transfer data to any application or to the frontend.

### Executing program:

Clone the repository and change into it on the command line:

```
git clone https://github.com/mielik/api_final_yatube
```

```
cd api_final_yatube
```

Create and activate virtual environment:

```
python3 -m venv venv
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Install dependencies from a file requirements.txt:

```
pip install -r requirements.txt
```

Run migrations:

```
python3 manage.py migrate
```

Run project:

```
python3 manage.py runserver
```

### Command examples
Getting publications:
```
http://127.0.0.1:8000/api/v1/posts/
```
Adding a comment to a post:
```
http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/
{
"text": "string"
}
```
Returns all subscriptions of the user who made the request:
```
http://127.0.0.1:8000/api/v1/follow/
```
