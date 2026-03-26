from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.game import EntradaRanking
from app.services.game_service import ServicoJogo

roteador = APIRouter(prefix="/ranking", tags=["Ranking"])


@roteador.get("/", response_model=List[EntradaRanking])
def buscar_ranking(db: Session = Depends(get_db)):
    """Retorna o ranking global ordenado pela melhor pontuação."""
    servico = ServicoJogo(db)
    entradas = servico.buscar_ranking()
    return [
        EntradaRanking(
            posicao=i + 1,
            nome_usuario=e["nome_usuario"],
            pontuacao=e["pontuacao"],
            total_tentativas=e["total_tentativas"],
            duracao_segundos=e["duracao_segundos"],
            finalizado_em=e["finalizado_em"],
        )
        for i, e in enumerate(entradas)
    ]
