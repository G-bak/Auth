"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app.api import api_router
from app.core.config import get_settings
from app.db.repositories import RoleRepository, UserRepository
from app.db.session import init_db, session_scope
from app.utils.password import hash_password
from app.web import web_router

ROLE_PRESETS = {
    1: "Viewer",
    2: "Reporter",
    3: "Editor",
    4: "Manager",
    5: "Administrator",
}


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    app.include_router(web_router)

    app.mount("/static", StaticFiles(directory="app/web/static"), name="static")

    @app.get("/", include_in_schema=False)
    async def root_redirect() -> RedirectResponse:
        return RedirectResponse(url="/auth/login", status_code=307)

    @app.on_event("startup")
    def on_startup() -> None:
        init_db()
        with session_scope() as session:
            role_repo = RoleRepository(session)
            user_repo = UserRepository(session)
            role_repo.ensure_roles(ROLE_PRESETS)
            if not user_repo.get_by_email(settings.superuser_email):
                admin_role = role_repo.get_by_level(5)
                roles = [admin_role] if admin_role else None
                user_repo.create(
                    email=settings.superuser_email,
                    hashed_password=hash_password(settings.superuser_password),
                    full_name="System Administrator",
                    roles=roles,
                )

    return app


app = create_app()