# 데이터베이스 마이그레이션

이 디렉터리는 Alembic 기반 데이터베이스 마이그레이션 스크립트를 저장합니다. 생성된 리비전 파일은 `versions/` 하위 폴더에 배치되며, `env.py`는 프로젝트 설정(`app.core.config.Settings`)을 사용해 데이터베이스 URL을 자동으로 불러옵니다.

## 주요 명령어

```bash
# 최신 스키마로 업그레이드
alembic upgrade head

# 이전 리비전으로 롤백
alembic downgrade -1

# 새 리비전 자동 생성 (모델 변경 후)
alembic revision --autogenerate -m "explain the change"
```

> `alembic.ini`는 루트 경로에 있으며 `prepend_sys_path = .` 옵션을 통해 프로젝트 모듈을 참조합니다. 명령 실행 전 `.env` 또는 환경 변수에 `DATABASE_URL`을 올바르게 설정하세요.