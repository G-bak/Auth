"""Authentication API routes."""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies.permission import get_auth_service, get_current_user
from app.core.config import get_settings
from app.domain import AuthService, UserEntity
from app.schemas import LoginRequest, RegisterRequest, Token, UserRead

router = APIRouter()


def _to_user_read(user: UserEntity) -> UserRead:
    return UserRead(
        id=user.id or 0,
        email=str(user.email),
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        role_levels=user.role_levels,
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Register a new account")
def register_user(payload: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> UserRead:
    try:
        user = auth_service.register(email=payload.email, password=payload.password, full_name=payload.full_name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return _to_user_read(user)


@router.post("/login", response_model=Token, summary="Exchange credentials for an access token")
def login(payload: LoginRequest, response: Response, auth_service: AuthService = Depends(get_auth_service)) -> Token:
    try:
        _, token = auth_service.authenticate(email=payload.email, password=payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    settings = get_settings()
    expires_minutes = settings.access_token_expire_minutes
    expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
    response.set_cookie("access_token", token, httponly=True, max_age=int(expires_minutes * 60))
    return Token(access_token=token, expires_at=expires_at)


@router.get("/me", response_model=UserRead, summary="Return the current user profile")
def read_me(current_user: UserEntity = Depends(get_current_user)) -> UserRead:
    return _to_user_read(current_user)