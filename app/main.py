from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.config import settings
from app.db.base import Base
from app.db.session import engine
from app.routers import books, comments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Managament API")

app.include_router(books.router)
app.include_router(comments.router)

@app.get("/", include_in_schema=False)
def docs_redirect():
    response = RedirectResponse(url=("/docs"))
    return response