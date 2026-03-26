from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("mastermind")

DESCRICAO_HTTP = {
    400: "Requisição inválida",
    401: "Não autorizado",
    403: "Acesso negado",
    404: "Não encontrado",
    405: "Método não permitido",
    409: "Conflito",
    422: "Dados inválidos",
    500: "Erro interno do servidor",
}


def _resposta_erro(codigo: int, mensagem: str) -> JSONResponse:
    return JSONResponse(
        status_code=codigo,
        content={
            "codigo": codigo,
            "erro": DESCRICAO_HTTP.get(codigo, "Erro"),
            "mensagem": mensagem,
        },
    )


async def handler_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """Captura todos os HTTPException lançados nos serviços/rotas."""
    return _resposta_erro(exc.status_code, exc.detail)


async def handler_validacao(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Captura erros de validação do Pydantic (422).
    Extrai a primeira mensagem de erro e retorna 422 com formato padronizado.
    """
    erros = exc.errors()
    if erros:
        primeiro = erros[0]
        campo = " → ".join(str(p) for p in primeiro.get("loc", []) if p != "body")
        mensagem = f"{campo}: {primeiro['msg']}" if campo else primeiro["msg"]
    else:
        mensagem = "Dados inválidos na requisição"

    return _resposta_erro(422, mensagem)


async def handler_erro_generico(request: Request, exc: Exception) -> JSONResponse:
    """
    Captura qualquer exceção não tratada e retorna 500.
    Registra o erro completo no log sem expô-lo ao cliente.
    """
    logger.exception("Erro não tratado em %s %s", request.method, request.url)
    return _resposta_erro(500, "Ocorreu um erro interno. Tente novamente mais tarde.")
