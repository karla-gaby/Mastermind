from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_SECRETA = os.getenv("SECRET_KEY", "chave-dev-insegura-mude-em-producao")
ALGORITMO = os.getenv("ALGORITHM", "HS256")
MINUTOS_EXPIRACAO_TOKEN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

contexto_senha = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return contexto_senha.verify(senha_plana, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    return contexto_senha.hash(senha)


def criar_token_acesso(dados: dict, delta_expiracao: Optional[timedelta] = None) -> str:
    para_codificar = dados.copy()
    expira = datetime.utcnow() + (delta_expiracao or timedelta(minutes=MINUTOS_EXPIRACAO_TOKEN))
    para_codificar.update({"exp": expira})
    return jwt.encode(para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)


def decodificar_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
    except JWTError:
        return None
