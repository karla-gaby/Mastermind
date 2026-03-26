from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.database import engine, Base
from app.routers import auth, games, ranking
from app.excecoes import (
    handler_http_exception,
    handler_validacao,
    handler_erro_generico,
)

import app.models.user  
import app.models.game  

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Mastermind",
    description="Backend para o jogo web Mastermind",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_exception_handler(HTTPException, handler_http_exception)
app.add_exception_handler(RequestValidationError, handler_validacao)
app.add_exception_handler(Exception, handler_erro_generico)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.roteador)
app.include_router(games.roteador)
app.include_router(ranking.roteador)


@app.get("/", tags=["Saúde"])
def raiz():
    return {"status": "ok", "mensagem": "API Mastermind está funcionando"}
