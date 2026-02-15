from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError

from pdf_service.app.core.config import settings

bearer = HTTPBearer(auto_error=False)


def get_current_claims(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = creds.credentials
    try:
        claims = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    # minimal required claims
    required = ["email", "name", "surname", "date_of_birth"]
    missing = [k for k in required if k not in claims]
    if missing:
        raise HTTPException(status_code=400, detail=f"Token missing claims: {missing}")

    return claims
