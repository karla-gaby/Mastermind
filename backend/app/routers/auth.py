from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegistroUsuario, EntradaUsuario, Token, RespostaUsuario
from app.services.auth_service import ServicoAutenticacao

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


@roteador.post("/registrar", response_model=RespostaUsuario, status_code=201)
def registrar(dados: RegistroUsuario, db: Session = Depends(get_db)):
    """Cria uma nova conta de usuário."""
    servico = ServicoAutenticacao(db)
    usuario = servico.registrar(dados)
    return usuario


@roteador.post("/entrar", response_model=Token)
def entrar(dados: EntradaUsuario, db: Session = Depends(get_db)):
    """Autentica e retorna um token JWT."""
    servico = ServicoAutenticacao(db)
    return servico.autenticar(dados)
