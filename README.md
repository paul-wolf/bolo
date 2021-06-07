# bolo

This will create a project that have user authentication using FastAPI-users.

The project is called "bolo". No reason; it's just short and easy to type.

Clone the repo:

```
git clone git@github.com:paul-wolf/bolo.git
cd bolo
```


You need to create a `.env` file that has:

```
DB_CONNECT=postgresql+psycopg2://postgres:postgres@localhost/mydb
DB_CONNECT_ASYNC=postgresql://postgres:postgres@localhost/mydb
SECRET=<my secret key>
```

```
python -m venv .venv && source .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
```

Create a postgresql db:

```
createdb mydb
```

Make sure whatever db name you use is the same as in the connection strings defined in `.env`. 


Start the server:

```
uvicorn view.main:app --reload
```

Test server is working:

```
curl --request GET \
  --url http://127.0.0.1:8000/

```

Create a new user:

```
curl --request POST \
  --url http://localhost:8000/auth/register \
  --header 'Content-Type: application/json' \
  --data '{
	"email": "paul@yew.io",
	"password": "paul"
}'
```

