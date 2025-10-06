"""SSR routes for authentication flows."""

from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.dependencies import get_auth_service
from app.core.config import get_settings
from app.domain import AuthService, UserEntity

router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")
settings = get_settings()


def _context(request: Request, **extra):
    return {"request": request, **extra}


def _current_user(request: Request, auth_service: AuthService) -> UserEntity | None:
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        return auth_service.verify_token(token)
    except ValueError:
        return None


@router.get("/login", name="login")
async def login_form(request: Request) -> RedirectResponse | object:
    return templates.TemplateResponse("auth/login.html", _context(request))


@router.post("/login")
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        _, token = auth_service.authenticate(email=email, password=password)
    except ValueError:
        return templates.TemplateResponse(
            "auth/login.html",
            _context(request, error="이메일 또는 비밀번호가 올바르지 않습니다."),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=settings.access_token_expire_minutes * 60,
    )
    return response


@router.get("/register", name="register")
async def register_form(request: Request) -> object:
    return templates.TemplateResponse("auth/register.html", _context(request))


@router.post("/register")
async def register_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(""),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        auth_service.register(email=email, password=password, full_name=full_name or None)
    except ValueError as exc:
        return templates.TemplateResponse(
            "auth/register.html",
            _context(request, error=str(exc)),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    return response


@router.get("/logout")
async def logout() -> RedirectResponse:
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response


@router.get("/profile")
async def profile(request: Request, auth_service: AuthService = Depends(get_auth_service)) -> object:
    user = _current_user(request, auth_service)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("auth/profile.html", _context(request, user=user))


@router.get("/dashboard")
async def dashboard(request: Request, auth_service: AuthService = Depends(get_auth_service)) -> object:
    user = _current_user(request, auth_service)
    if not user:
        return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        "auth/dashboard.html",
        _context(
            request,
            user=user,
            expires_in=timedelta(minutes=settings.access_token_expire_minutes),
        ),
    )