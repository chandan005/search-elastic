from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from app.router import search
from app.exception.custom_exceptions import CustomException
from app.middleware.response_logger import ResponseLoggerMiddleware
from app.config.config import settings
from app.exception.handlers import custom_exception_handler

app = FastAPI()

app.include_router(search.router)

app.add_exception_handler(Exception, custom_exception_handler)

def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(ResponseLoggerMiddleware),
    ]
    return middleware

def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Search API",
        description="Search API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        middleware=make_middleware(),
    )
    return app_

if __name__ == '__main__':
    app = create_app()
