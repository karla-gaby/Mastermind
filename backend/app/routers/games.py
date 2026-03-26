from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies import obter_usuario_atual_id
from app.schemas.game import (
    RequisicaoTentativa,
    RespostaTentativa,
    RespostaInicioJogo,
    RespostaJogo,
    RegistroTentativa,
)
from app.services.game_service import ServicoJogo

roteador = APIRouter(prefix="/jogos", tags=["Jogos"])


def _mapear_jogo(jogo) -> RespostaJogo:
    tentativas = [RegistroTentativa(**t) for t in (jogo.matriz_tentativas or [])]
    return RespostaJogo(
        id=jogo.id,
        codigo=jogo.codigo,
        status=jogo.status,
        total_tentativas=jogo.total_tentativas,
        matriz_tentativas=tentativas,
        pontuacao=jogo.pontuacao,
        iniciado_em=jogo.iniciado_em,
        finalizado_em=jogo.finalizado_em,
        duracao_segundos=jogo.duracao_segundos,
    )


@roteador.get("/", response_model=List[RespostaJogo])
def listar_meus_jogos(
    usuario_id: int = Depends(obter_usuario_atual_id),
    db: Session = Depends(get_db),
):
    """Retorna o histórico de jogos do usuário autenticado."""
    servico = ServicoJogo(db)
    return [_mapear_jogo(j) for j in servico.buscar_historico_usuario(usuario_id)]


@roteador.post("/iniciar", response_model=RespostaInicioJogo, status_code=201)
def iniciar_jogo(
    usuario_id: int = Depends(obter_usuario_atual_id),
    db: Session = Depends(get_db),
):
    """Inicia um novo jogo Mastermind para o usuário autenticado."""
    servico = ServicoJogo(db)
    jogo = servico.iniciar_jogo(usuario_id)
    return RespostaInicioJogo(
        jogo_id=jogo.id,
        codigo=jogo.codigo,
        mensagem="Jogo iniciado! Adivinhe o código de 4 cores (R,G,B,Y,O,P). Você tem 10 tentativas.",
    )


@roteador.get("/{jogo_id}", response_model=RespostaJogo)
def buscar_jogo(
    jogo_id: int,
    usuario_id: int = Depends(obter_usuario_atual_id),
    db: Session = Depends(get_db),
):
    """Retorna o estado atual do jogo (sem revelar o código secreto)."""
    servico = ServicoJogo(db)
    return _mapear_jogo(servico.buscar_jogo(jogo_id=jogo_id, usuario_id=usuario_id))


@roteador.post("/{jogo_id}/abandonar", status_code=204)
def abandonar_jogo(
    jogo_id: int,
    usuario_id: int = Depends(obter_usuario_atual_id),
    db: Session = Depends(get_db),
):
    """Abandona um jogo ativo, marcando-o como perdido."""
    servico = ServicoJogo(db)
    servico.abandonar_jogo(jogo_id=jogo_id, usuario_id=usuario_id)


@roteador.post("/{jogo_id}/tentativa", response_model=RespostaTentativa)
def fazer_tentativa(
    jogo_id: int,
    corpo: RequisicaoTentativa,
    usuario_id: int = Depends(obter_usuario_atual_id),
    db: Session = Depends(get_db),
):
    """Submete uma tentativa para um jogo ativo."""
    servico = ServicoJogo(db)
    resultado = servico.fazer_tentativa(
        jogo_id=jogo_id, tentativa=corpo.tentativa, usuario_id=usuario_id
    )
    return RespostaTentativa(**resultado)
