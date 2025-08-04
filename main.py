from fastapi import FastAPI
from src.auth.routes import auth_router
from src.errors import register_error_handlers


version = "v1"


app = FastAPI(
    title = "bookly",
    description="a rest api for book review web service",
    version=version,
)

app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=["auth"])



register_error_handlers(app)