import re
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


_REGEX_NOME_USUARIO = re.compile(r"^[\w\-]+$", re.UNICODE)


class RegistroUsuario(BaseModel):
    nome_usuario: str
    email: EmailStr
    senha: str

    @field_validator("nome_usuario")
    @classmethod
    def validar_nome_usuario(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Nome de usuário não pode ser vazio")
        if len(v) < 3:
            raise ValueError("Nome de usuário deve ter pelo menos 3 caracteres")
        if len(v) > 50:
            raise ValueError("Nome de usuário deve ter no máximo 50 caracteres")
        if not _REGEX_NOME_USUARIO.match(v):
            raise ValueError(
                "Nome de usuário só pode conter letras, números, underscore (_) e hífen (-)"
            )
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Senha não pode ser vazia")
        if len(v) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        if len(v) > 128:
            raise ValueError("Senha deve ter no máximo 128 caracteres")
        return v


class EntradaUsuario(BaseModel):
    nome_usuario: str  
    senha: str

    @field_validator("nome_usuario")
    @classmethod
    def validar_identificador(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Usuário ou e-mail não pode ser vazio")
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Senha não pode ser vazia")
        return v


class Token(BaseModel):
    token_acesso: str
    tipo_token: str
    usuario_id: int
    nome_usuario: str


class RespostaUsuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    criado_em: datetime

    model_config = {"from_attributes": True}
