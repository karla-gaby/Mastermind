from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.game import Jogo
from app.models.user import Usuario


class RepositorioJogo:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_id(self, jogo_id: int) -> Optional[Jogo]:
        return self.db.query(Jogo).filter(Jogo.id == jogo_id).first()

    def buscar_por_codigo(self, codigo: str) -> Optional[Jogo]:
        return self.db.query(Jogo).filter(Jogo.codigo == codigo).first()

    def buscar_por_usuario(self, usuario_id: int) -> List[Jogo]:
        return (
            self.db.query(Jogo)
            .filter(Jogo.usuario_id == usuario_id)
            .order_by(Jogo.iniciado_em.desc())
            .all()
        )

    def criar(self, usuario_id: int, codigo: str, codigo_secreto: str) -> Jogo:
        jogo = Jogo(
            usuario_id=usuario_id,
            codigo=codigo,
            codigo_secreto=codigo_secreto,
            matriz_tentativas=[],
        )
        self.db.add(jogo)
        self.db.commit()
        self.db.refresh(jogo)
        return jogo

    def salvar(self, jogo: Jogo) -> Jogo:
        self.db.commit()
        self.db.refresh(jogo)
        return jogo

    def buscar_ranking_global(self, limite: int = 50) -> List[dict]:
        """Retorna as melhores pontuações globais (apenas jogos ganhos)."""
        linhas = (
            self.db.query(
                Usuario.nome_usuario,
                Jogo.pontuacao,
                Jogo.total_tentativas,
                Jogo.duracao_segundos,
                Jogo.finalizado_em,
            )
            .join(Usuario, Jogo.usuario_id == Usuario.id)
            .filter(Jogo.status == "ganhou")
            .order_by(Jogo.pontuacao.desc(), Jogo.total_tentativas.asc())
            .limit(limite)
            .all()
        )
        return [
            {
                "nome_usuario": r.nome_usuario,
                "pontuacao": r.pontuacao,
                "total_tentativas": r.total_tentativas,
                "duracao_segundos": r.duracao_segundos,
                "finalizado_em": r.finalizado_em,
            }
            for r in linhas
        ]
