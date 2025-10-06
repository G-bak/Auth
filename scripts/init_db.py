"""Database bootstrap utility."""

from app.core.config import get_settings
from app.db.repositories import RoleRepository, UserRepository
from app.db.session import init_db, session_scope
from app.utils.password import hash_password

ROLE_PRESETS = {
    1: "Viewer",
    2: "Reporter",
    3: "Editor",
    4: "Manager",
    5: "Administrator",
}


def main() -> None:
    settings = get_settings()
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


if __name__ == "__main__":  # pragma: no cover
    main()