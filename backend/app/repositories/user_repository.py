from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import Usuario


class RepositorioUsuario:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def buscar_por_nome_usuario(self, nome_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nome_usuario == nome_usuario).first()

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def buscar_por_nome_ou_email(self, identificador: str) -> Optional[Usuario]:
        return (
            self.db.query(Usuario)
            .filter(
                (Usuario.nome_usuario == identificador) | (Usuario.email == identificador)
            )
            .first()
        )

    def criar(self, nome_usuario: str, email: str, senha_hash: str) -> Usuario:
        usuario = Usuario(
            nome_usuario=nome_usuario, email=email, senha_hash=senha_hash
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
