from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.user_repository import RepositorioUsuario
from app.schemas.auth import RegistroUsuario, EntradaUsuario, Token
from app.security import verificar_senha, gerar_hash_senha, criar_token_acesso
from app.models.user import Usuario


class ServicoAutenticacao:
    def __init__(self, db: Session):
        self.repositorio = RepositorioUsuario(db)

    def registrar(self, dados: RegistroUsuario) -> Usuario:
        if self.repositorio.buscar_por_nome_usuario(dados.nome_usuario):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuário já está em uso",
            )
        if self.repositorio.buscar_por_email(dados.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail já cadastrado",
            )
        hash_senha = gerar_hash_senha(dados.senha)
        return self.repositorio.criar(
            nome_usuario=dados.nome_usuario,
            email=dados.email,
            senha_hash=hash_senha,
        )

    def autenticar(self, dados: EntradaUsuario) -> Token:
        usuario = self.repositorio.buscar_por_nome_ou_email(dados.nome_usuario)
        if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = criar_token_acesso({"sub": str(usuario.id)})
        return Token(
            token_acesso=token,
            tipo_token="bearer",
            usuario_id=usuario.id,
            nome_usuario=usuario.nome_usuario,
        )

    def buscar_usuario_atual(self, usuario_id: int) -> Usuario:
        usuario = self.repositorio.buscar_por_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
            )
        return usuario
