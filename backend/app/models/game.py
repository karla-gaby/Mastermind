from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Jogo(Base):
    __tablename__ = "jogos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(16), unique=True, index=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    codigo_secreto = Column(String(20), nullable=False)
    matriz_tentativas = Column(JSON, default=list)
    total_tentativas = Column(Integer, default=0)
    status = Column(String(10), default="ativo")
    pontuacao = Column(Integer, default=0)
    duracao_segundos = Column(Float, nullable=True)
    iniciado_em = Column(DateTime, default=datetime.utcnow)
    finalizado_em = Column(DateTime, nullable=True)

    usuario = relationship("Usuario", back_populates="jogos")
