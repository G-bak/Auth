# FastAPI 기반 계정 인증 서비스 디렉토리 구조 제안

## 1. 전체 개요
- **목표**: 회원가입, 로그인, 로그아웃, 토큰 관리 등 계정 기능을 독립 서비스로 개발하여 다양한 사내 시스템에서 공통으로 활용할 수 있도록 함.
- **핵심 가치**: 마이크로서비스 관점의 확장성, 기능별 책임 분리, 테스트 및 배포 자동화 용이성, 도메인 주도 설계를 고려한 모듈화.
- **전제**: FastAPI + SQLAlchemy (또는 비동기 ORM), 메시지 큐(옵션), CI/CD 환경, 인프라 환경(예: Kubernetes, Docker)과의 연동.

## 2. 디렉토리 구조
```
AuthService/
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   ├── routes/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   └── health.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── migrations/
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   └── __init__.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user_entity.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── auth_service.py
│   │   │   └── __init__.py
│   │   ├── value_objects/
│   │   │   ├── email.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── password.py
│   │   ├── jwt.py
│   │   └── __init__.py
│   ├── events/
│   │   ├── publishers/
│   │   ├── subscribers/
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── tests/
│   ├── api/
│   ├── domain/
│   ├── e2e/
│   └── conftest.py
├── scripts/
│   ├── prestart.sh
│   ├── init_db.py
│   └── generate_openapi.py
├── alembic.ini
├── pyproject.toml (또는 requirements.txt)
├── README.md
└── .env.example
```

## 3. 세부 설명

### 3.1 app/api
- **routes**: FastAPI 라우터 정의. 버전별 디렉토리(v1, v2 등)로 나눠 API 변경에 대응.
- **dependencies**: 공통 의존성 주입 모듈(FastAPI Depends). 예: 사용자 인증 검증, DB 세션 주입, rate limiting 설정 등.

### 3.2 app/core
- **config.py**: 설정 관리. pydantic Settings 또는 dynaconf 사용. 환경별 설정(.env, configmap)을 한 곳에서 관리.
- **security.py**: 보안 관련 핵심 로직(JWT 서명 키 관리, 암호화/복호화, OAuth2 설정 등).

### 3.3 app/db
- **migrations**: Alembic 기반 DB 마이그레이션 스크립트.
- **models**: ORM 모델 정의. SQLAlchemy 또는 Tortoise ORM 등을 활용.
- **repositories**: 데이터 접근 레이어. 모델과 데이터를 핸들링하며 서비스 레이어에 데이터를 전달.
- **session.py**: 세션팩토리, 엔진 생성 등 DB 연결 관리.

### 3.4 app/domain (도메인 계층)
- **entities**: 도메인 엔티티 정의. ORM 모델과 분리하여 비즈니스 규칙 집중.
- **services**: 도메인 서비스. 비즈니스 로직을 담당하며 API 레이어에서 호출.
- **value_objects**: 이메일, 패스워드 정책 등 값 객체. 불변성과 검증 로직을 담아 재사용성 향상.

### 3.5 app/schemas
- Pydantic 모델. 요청/응답 검증, 직렬화/역직렬화 담당. API 계약 유지.

### 3.6 app/utils
- 재사용 가능한 유틸 함수. 암호 해시, JWT 생성/검증, 시간 관련 도구 등.

### 3.7 app/events
- 이벤트 기반 확장을 위한 구조. 예: 사용자 가입 시 메시지 큐(Kafka, RabbitMQ) 발행.
- **publishers/subscribers** 디렉토리로 나눠 확장성 확보.

### 3.8 tests
- **api**: 라우트 단위 테스트.
- **domain**: 도메인 서비스, 엔티티 테스트.
- **e2e**: 실제 API 엔드포인트 통합 테스트. TestClient 또는 HTTPX 활용.
- pytest 기반 설정을 위한 `conftest.py` 포함.

### 3.9 scripts
- 컨테이너 시작 전 실행되는 스크립트(prestart), DB 초기화, OpenAPI 문서 자동 생성 등 운영 편의 스크립트.

### 3.10 루트 파일
- `alembic.ini`: 마이그레이션 설정.
- `pyproject.toml` 또는 `requirements.txt`: 패키지 관리.
- `.env.example`: 환경 변수 템플릿.
- `README.md`: 서비스 개요, 로컬 실행 방법, 배포 전략 안내.

## 4. 확장 전략
- **모듈화**: 기능 확장 시 app 내 디렉토리 추가(예: `app/domain/services/token_service.py`).
- **버저닝**: API 버전별 폴더를 추가하여 호환성 유지.
- **인증 전략**: JWT 외에도 SSO, OAuth2, SAML 등 추가 전략을 `app/core/security.py`와 `app/domain/services/auth_service.py`에 구현.
- **감사 로그**: `events` 디렉토리에서 감사 로그 전송 또는 분석 파이프라인 연동.

## 5. 운영/배포 고려사항
- **CI/CD**: GitHub Actions, GitLab CI 등을 활용하여 lint, test, build, deploy 파이프라인 구성. 결과물은 Docker 이미지.
- **관측성**: Logging, Metrics, Tracing 구조를 `app/core/logging.py`, `app/core/observability.py` 등으로 확장.
- **설정 분리**: 환경별 `.env` 또는 Vault, AWS Parameter Store 등을 통해 비밀정보 분리.
- **도메인 주도 설계**: 엔티티, 서비스, 값 객체를 명확히 분리하여 유지보수성과 테스트 용이성 확보.

## 6. 요약
- FastAPI 기반 인증 서비스는 API 계층, 도메인 계층, 데이터 계층을 명확히 분리하는 것이 핵심.
- 디렉토리 구조를 통해 책임을 명확히 하고 버전 관리, 테스트, 배포 전략과 긴밀히 연결.
- 위 구조는 실무 환경에서 팀 단위 협업과 마이크로서비스 통합에 최적화된 패턴.
