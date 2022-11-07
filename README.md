### Installation

#### Virtual environment:

```console
$ virtualenv venv -p 3.10
$ source venv/bin/activate
$ pip install --no-cache-dir --upgrade -r /code/requirements.txt
$ uvicorn app.main:app --reload 
```

#### Docker:

```console
$ docker build . -t books-challenge
$ docker run -p 8000:8000/tcp books-challenge:latest
```

### Configuration

Environment variables

**SQLALCHEMY_DATABASE_URL:** 
dialect+driver://username:password@host:port/database. Dialect names include the identifying name of the SQLAlchemy dialect, a name such as sqlite , mysql , postgresql , oracle , or mssql 
``console
default = "sqlite:///./books.db"
```

**BOOKS_PROVIDER_URL:**
A book api library url that receives an ISBN as parameter to provide book details. The url must contain the "{isbn}" tag to indicate where the ISBN number should be requested.
``console
default = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=details"
```

