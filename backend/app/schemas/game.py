from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime

CORES_VALIDAS = {"R", "G", "B", "Y", "O", "P"}
TAMANHO_CODIGO = 4


class RequisicaoTentativa(BaseModel):
    tentativa: List[str]

    @field_validator("tentativa")
    @classmethod
    def validar_tentativa(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("A tentativa não pode ser vazia")
        if len(v) != TAMANHO_CODIGO:
            raise ValueError(
                f"A tentativa deve conter exatamente {TAMANHO_CODIGO} cores "
                f"(recebido: {len(v)})"
            )
        cores_invalidas = [c for c in v if c not in CORES_VALIDAS]
        if cores_invalidas:
            raise ValueError(
                f"Cor(es) inválida(s): {cores_invalidas}. "
                f"Cores válidas: {sorted(CORES_VALIDAS)}"
            )
        return v


class RegistroTentativa(BaseModel):
    numero_tentativa: int
    tentativa: List[str]
    exatos: int
    cores_certas: int


class RespostaTentativa(BaseModel):
    exatos: int
    cores_certas: int
    numero_tentativa: int
    status: str
    pontuacao: Optional[int] = None


class RespostaInicioJogo(BaseModel):
    jogo_id: int
    codigo: str
    mensagem: str


class RespostaJogo(BaseModel):
    id: int
    codigo: str
    status: str
    total_tentativas: int
    matriz_tentativas: List[RegistroTentativa]
    pontuacao: int
    iniciado_em: datetime
    finalizado_em: Optional[datetime] = None
    duracao_segundos: Optional[float] = None

    model_config = {"from_attributes": True}


class EntradaRanking(BaseModel):
    posicao: int
    nome_usuario: str
    pontuacao: int
    total_tentativas: int
    duracao_segundos: Optional[float]
    finalizado_em: Optional[datetime]
