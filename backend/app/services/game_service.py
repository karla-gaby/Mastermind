import random
import uuid
from datetime import datetime
from typing import List, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.game import Jogo
from app.repositories.game_repository import RepositorioJogo

CORES = ["R", "G", "B", "Y", "O", "P"]
TAMANHO_CODIGO = 4
MAX_TENTATIVAS = 10


class ServicoJogo:
    def __init__(self, db: Session):
        self.repositorio = RepositorioJogo(db)

    def iniciar_jogo(self, usuario_id: int) -> Jogo:
        secreto = random.choices(CORES, k=TAMANHO_CODIGO)
        codigo_secreto = ",".join(secreto)
        codigo = uuid.uuid4().hex[:8].upper()
        return self.repositorio.criar(
            usuario_id=usuario_id, codigo=codigo, codigo_secreto=codigo_secreto
        )

    def fazer_tentativa(
        self, jogo_id: int, tentativa: List[str], usuario_id: int
    ) -> dict:
        jogo = self._buscar_jogo_do_usuario(jogo_id, usuario_id)

        if jogo.status != "ativo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O jogo já está '{jogo.status}'",
            )

        secreto = jogo.codigo_secreto.split(",")
        exatos, cores_certas = self._avaliar(secreto, tentativa)

        matriz = list(jogo.matriz_tentativas or [])
        matriz.append(
            {
                "numero_tentativa": jogo.total_tentativas + 1,
                "tentativa": tentativa,
                "exatos": exatos,
                "cores_certas": cores_certas,
            }
        )
        jogo.matriz_tentativas = matriz
        jogo.total_tentativas += 1

        if exatos == TAMANHO_CODIGO:
            jogo.status = "ganhou"
            self._encerrar_jogo(jogo)
        elif jogo.total_tentativas >= MAX_TENTATIVAS:
            jogo.status = "perdeu"
            self._encerrar_jogo(jogo)

        self.repositorio.salvar(jogo)

        return {
            "exatos": exatos,
            "cores_certas": cores_certas,
            "numero_tentativa": jogo.total_tentativas,
            "status": jogo.status,
            "pontuacao": jogo.pontuacao if jogo.status != "ativo" else None,
        }

    def buscar_jogo(self, jogo_id: int, usuario_id: int) -> Jogo:
        return self._buscar_jogo_do_usuario(jogo_id, usuario_id)

    def abandonar_jogo(self, jogo_id: int, usuario_id: int) -> None:
        jogo = self._buscar_jogo_do_usuario(jogo_id, usuario_id)
        if jogo.status != "ativo":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Só é possível abandonar um jogo ativo",
            )
        jogo.status = "perdeu"
        self._encerrar_jogo(jogo)
        self.repositorio.salvar(jogo)

    def buscar_historico_usuario(self, usuario_id: int) -> List[Jogo]:
        return self.repositorio.buscar_por_usuario(usuario_id)

    def buscar_ranking(self) -> List[dict]:
        return self.repositorio.buscar_ranking_global()

    def _buscar_jogo_do_usuario(self, jogo_id: int, usuario_id: int) -> Jogo:
        jogo = self.repositorio.buscar_por_id(jogo_id)
        if not jogo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Jogo não encontrado"
            )
        if jogo.usuario_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
            )
        return jogo

    def _encerrar_jogo(self, jogo: Jogo) -> None:
        jogo.finalizado_em = datetime.utcnow()
        jogo.duracao_segundos = (
            jogo.finalizado_em - jogo.iniciado_em
        ).total_seconds()
        jogo.pontuacao = (
            self._calcular_pontuacao(jogo) if jogo.status == "ganhou" else 0
        )

    @staticmethod
    def _avaliar(secreto: List[str], tentativa: List[str]) -> Tuple[int, int]:
        exatos = sum(s == t for s, t in zip(secreto, tentativa))

        restante_secreto = [s for s, t in zip(secreto, tentativa) if s != t]
        restante_tentativa = [t for s, t in zip(secreto, tentativa) if s != t]
        cores_certas = sum(
            min(restante_secreto.count(c), restante_tentativa.count(c))
            for c in set(restante_tentativa)
        )
        return exatos, cores_certas

    @staticmethod
    def _calcular_pontuacao(jogo: Jogo) -> int:
        base = (MAX_TENTATIVAS - jogo.total_tentativas + 1) * 100
        bonus_tempo = max(0, 300 - int((jogo.duracao_segundos or 0) // 5))
        return base + bonus_tempo
