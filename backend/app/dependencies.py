from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import decodificar_token

esquema_bearer = HTTPBearer()


def obter_usuario_atual_id(
    credenciais: HTTPAuthorizationCredentials = Depends(esquema_bearer),
) -> int:
    token = credenciais.credentials
    payload = decodificar_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    usuario_id = payload.get("sub")
    if not usuario_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Payload do token inválido",
        )
    return int(usuario_id)
