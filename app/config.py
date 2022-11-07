from pydantic import BaseSettings, AnyUrl, validator

class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./books.db"
    BOOKS_PROVIDER_URL: AnyUrl = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=details"
    #BOOKS_PROVIDER_URL: AnyUrl = "https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"   
    @validator("BOOKS_PROVIDER_URL", pre=True)
    def books_isbn_tag(cls, v: str):
        if not "{isbn}" in v:
            raise ValueError("must containt {isbn} tag")
        return v 

settings = Settings()