from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth_service.app.core.security import create_access_token, hash_password, verify_password
from auth_service.app.crud.users import create_user, get_user_by_email
from auth_service.app.db.session import get_session
from auth_service.app.models.user import User
from auth_service.app.schemas.auth import LoginIn, TokenOut
from auth_service.app.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)):
    existing = await get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        surname=payload.surname,
        email=str(payload.email).lower(),
        date_of_birth=payload.date_of_birth,
        password_hash=hash_password(payload.password),
    )
    return await create_user(session, user)


@router.post("/login", response_model=TokenOut)
async def login(payload: LoginIn, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, str(payload.email).lower())
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # include profile claims so pdf_service can generate PDF without DB
    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "date_of_birth": user.date_of_birth.isoformat(),
        }
    )
    return TokenOut(access_token=token)
