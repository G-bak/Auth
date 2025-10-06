# FastAPI 기반 계정 인증 서비스 디렉토리 구조 제안

## 1. 전체 개요
- **목표**: 회원가입, 로그인, 로그아웃, 토큰 관리 등 계정 기능을 독립 서비스로 개발하여 다양한 사내 시스템에서 공통으로 활용할 수 있도록 함.
- **핵심 가치**: 마이크로서비스 관점의 확장성, 기능별 책임 분리, 테스트 및 배포 자동화 용이성, 도메인 주도 설계를 고려한 모듈화.
- **전제**: FastAPI + SQLAlchemy (또는 비동기 ORM), 메시지 큐(옵션), CI/CD 환경, 인프라 환경(예: Kubernetes, Docker)과의 연동.
- **UI 전략**: 동일 서비스 내에서 로그인/회원가입 페이지를 SSR 방식으로 제공하여 빠른 온보딩을 돕고, 차후 별도 프론트엔드와 연동할 때는 API·웹 라우터를 분리 배포할 수 있도록 설계.

## 2. 디렉토리 구조
```
AuthService/
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   │   ├── permission.py
│   │   ├── routes/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   ├── roles.py
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
│   │   │   ├── role.py
│   │   │   ├── user_role.py
│   │   │   └── __init__.py
│   │   ├── repositories/
│   │   │   ├── user_repository.py
│   │   │   ├── role_repository.py
│   │   │   └── __init__.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── user_entity.py
│   │   │   ├── role_entity.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── auth_service.py
│   │   │   ├── permission_service.py
│   │   │   └── __init__.py
│   │   ├── value_objects/
│   │   │   ├── email.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── permission.py
│   │   └── __init__.py
│   ├── web/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── auth.py
│   │   ├── templates/
│   │   │   ├── auth/
│   │   │   │   ├── login.html
│   │   │   │   └── register.html
│   │   │   └── shared/
│   │   │       ├── base.html
│   │   │       └── flash.html
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── auth.css
│   │   │   ├── js/
│   │   │   │   └── auth.js
│   │   │   └── images/
│   │   └── __init__.py
│   ├── utils/
│   │   ├── password.py
│   │   ├── jwt.py
│   │   └── __init__.py
│   ├── events/
│   │   ├── publishers/
│   │   │   ├── permission_events.py
│   │   ├── subscribers/
│   │   └── __init__.py
│   ├── main.py
│   └── __init__.py
├── docs/
│   ├── backend_directory_structure.md/
│   ├── project_plan.md/
├── tests/
│   ├── api/
│   ├── domain/
│   ├── e2e/
│   ├── web/
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
- `dependencies/permission.py`는 엔드포인트 호출 시 필요한 최소 권한을 선언하고 `permission_service`를 통해 검증.
- `routes/v1/roles.py`는 권한 CRUD, 사용자 권한 할당/회수 API를 제공.

### 3.2 app/core
- **config.py**: 설정 관리. pydantic Settings 또는 dynaconf 사용. 환경별 설정(.env, configmap)을 한 곳에서 관리.
- **security.py**: 보안 관련 핵심 로직(JWT 서명 키 관리, 암호화/복호화, OAuth2 설정 등).

### 3.3 app/db
- **migrations**: Alembic 기반 DB 마이그레이션 스크립트.
- **models**: ORM 모델 정의. SQLAlchemy 또는 Tortoise ORM 등을 활용. `role.py`, `user_role.py`로 권한/사용자 관계를 관리.
- **repositories**: 데이터 접근 레이어. 모델과 데이터를 핸들링하며 서비스 레이어에 데이터를 전달. `role_repository.py`에서 권한 CRUD 및 정책 조회를 담당.
- **session.py**: 세션팩토리, 엔진 생성 등 DB 연결 관리.

### 3.4 app/domain (도메인 계층)
- **entities**: 도메인 엔티티 정의. ORM 모델과 분리하여 비즈니스 규칙 집중. `role_entity.py`는 레벨 1~5 권한 정의, 추가 정책(예: 접근 가능한 리소스 리스트)을 속성으로 보관.
- **services**: 도메인 서비스. 비즈니스 로직을 담당하며 API 레이어에서 호출. `permission_service.py`는 사용자-권한 매핑, 레벨 비교, 상위 레벨 권한 상속 규칙을 캡슐화하여 다른 서비스에서 재사용 가능하게 한다.
- **value_objects**: 이메일, 패스워드 정책 등 값 객체. 불변성과 검증 로직을 담아 재사용성 향상.

### 3.5 app/schemas
- Pydantic 모델. 요청/응답 검증, 직렬화/역직렬화 담당. `permission.py`는 권한 레벨(정수 1~5), 역할명, 부가 정책을 직렬화하여 API 계약을 명확히 한다.

### 3.6 app/utils
- 재사용 가능한 유틸 함수. 암호 해시, JWT 생성/검증, 시간 관련 도구 등.

### 3.7 app/web
- 인증 UI를 FastAPI 애플리케이션 내부에서 바로 제공하기 위한 계층.
- **routes**: `/signup`, `/login`, `/logout` 등 브라우저 요청을 처리하는 라우터. 폼 데이터 유효성 검증 후 `auth_service`, `user_service`를 호출하여 회원가입/로그인을 처리하고, 쿠키 기반 세션 혹은 JWT 발급 후 리디렉션을 수행.
- **templates**: Jinja2 기반 템플릿. `auth/login.html`, `auth/register.html`에서 공통 레이아웃(`shared/base.html`)을 상속받고, CSRF 토큰 삽입, 에러 메시지 노출(`shared/flash.html`)을 포함.
- **static**: UI 리소스(CSS, JS, 이미지). `css/auth.css`는 반응형 폼 스타일링, `js/auth.js`는 클라이언트 측 유효성 검사나 UX 향상을 위한 인터랙션을 담당.
- FastAPI `StaticFiles`, `Jinja2Templates`를 초기화하는 헬퍼를 `app/web/__init__.py` 또는 전용 팩토리 함수로 제공하여 `main.py`에서 쉽게 마운트.

### 3.8 app/events
- 이벤트 기반 확장을 위한 구조. 예: 사용자 가입 시 메시지 큐(Kafka, RabbitMQ) 발행.
- **publishers/subscribers** 디렉토리로 나눠 확장성 확보.
- `publishers/permission_events.py`로 권한 변경, 감사 로깅, 이상 징후 알림 이벤트를 발행.

### 3.9 tests
- **api**: 라우트 단위 테스트.
- **domain**: 도메인 서비스, 엔티티 테스트.
- **e2e**: 실제 API 엔드포인트 통합 테스트. TestClient 또는 HTTPX 활용.
- **web**: 로그인/회원가입 페이지 렌더링 및 폼 제출 시나리오 테스트. FastAPI TestClient로 서버 사이드 렌더링 응답 상태, CSRF 토큰 존재 여부, 폼 유효성 검사 메시지 등을 검증. 필요 시 Playwright/Selenium으로 브라우저 기반 테스트 확장.
- pytest 기반 설정을 위한 `conftest.py` 포함.

### 3.10 scripts
- 컨테이너 시작 전 실행되는 스크립트(prestart), DB 초기화, OpenAPI 문서 자동 생성 등 운영 편의 스크립트.

### 3.11 루트 파일
- `alembic.ini`: 마이그레이션 설정.
- `pyproject.toml` 또는 `requirements.txt`: 패키지 관리.
- `.env.example`: 환경 변수 템플릿.
- `README.md`: 서비스 개요, 로컬 실행 방법, 배포 전략 안내.

## 4. 권한(레벨 1~5) 기반 접근 제어 설계

### 4.1 권한 계층 구조
- **레벨 1 (Guest)**: 최소 권한. 로그인만 가능, 민감 정보 접근 불가.
- **레벨 2 (Member)**: 일반 직원 권한. 자기 계정 정보 조회/수정, 기본 리소스 접근.
- **레벨 3 (Manager)**: 팀/프로젝트 리소스 관리 권한. 하위 레벨 사용자 권한 부여 요청 가능.
- **레벨 4 (Admin)**: 조직 단위 설정 변경, 권한 정책 관리, 사용자 강제 로그아웃 등 고급 기능 수행.
- **레벨 5 (Super Admin)**: 시스템 전체 제어. 보안 설정, 감사 로그 접근, 다중 테넌트 관리.

### 4.2 데이터 모델링
- `app/db/models/role.py`: 권한 레벨, 명칭, 설명, 상위 레벨과의 상속 관계 정의.
- `app/db/models/user_role.py` (또는 `user.py`의 관계 필드): 사용자-권한 매핑.
- `app/db/repositories/role_repository.py`: 권한 CRUD, 정책 조회 담당.
- 마이그레이션(`app/db/migrations/`)에 레벨 1~5 초기 데이터 시드 로직 포함.

### 4.3 서비스 계층 로직
- `permission_service.py`: 권한 검증/비교, 상위 권한 상속 규칙, 권한 변경 트랜잭션 처리.
- `auth_service.py`: 인증 성공 시 토큰 클레임에 권한 레벨 포함, 세션 갱신 시 권한 동기화.
- 이벤트 발행(`app/events/publishers/permission_events.py`)을 통해 감사 로그 또는 보안 알림 시스템과 연동.

### 4.4 API 레이어 설계
- `app/api/dependencies/permission.py`: 엔드포인트 최소 권한 선언, 요청 시 권한 검사.
- `app/api/routes/v1/roles.py`: 권한 CRUD, 권한 레벨 조회, 사용자 권한 할당 API 제공.
- 기존 사용자 라우터(`users.py`)에 권한 변경/조회 엔드포인트 추가.
- OpenAPI 생성 스크립트(`scripts/generate_openapi.py`)에 권한 스키마 반영.

### 4.5 웹 페이지 통합 전략
- 로그인/회원가입 페이지는 `app/web/routes/auth.py`에서 관리하며 API 계층과 동일한 서비스/스키마를 활용해 중복 로직을 제거.
- 세션/쿠키 기반 로그인 UX와 API 기반 JWT 인증을 동시에 지원하기 위해 `auth_service`에서 토큰 발급 방식을 추상화하고, 웹 라우터가 브라우저 친화적인 응답(HTML, 리디렉션, 플래시 메시지)을 제공하도록 설계.
- CSRF 토큰 발급 및 검증 로직을 `app/web/routes` 또는 전용 `app/web/security.py`에서 제공하여 폼 요청 보호.
- 템플릿에서 권한 레벨에 따라 UI 요소를 제어할 수 있도록 `request.state` 혹은 컨텍스트 프로세서를 통해 현재 사용자 권한을 주입.

### 4.6 보안 및 운영 고려사항
- `app/utils/jwt.py` 토큰에 권한 레벨과 정책 버전을 포함하여 정책 변경 시 토큰 무효화 전략 수립.
- 중앙 감사 로그(예: ELK, Cloud Logging)에 권한 변경 이벤트 수집.
- 권한 매트릭스 기반 테스트 케이스를 `tests/` 디렉토리에 추가하여 회귀 방지.
- 운영 문서(`docs/`)에 역할 정의, 권한 변경 프로세스, 응급 롤백 절차를 명시.

## 5. 확장 전략
- **모듈화**: 기능 확장 시 app 내 디렉토리 추가(예: `app/domain/services/token_service.py`).
- **버저닝**: API 버전별 폴더를 추가하여 호환성 유지.
- **인증 전략**: JWT 외에도 SSO, OAuth2, SAML 등 추가 전략을 `app/core/security.py`와 `app/domain/services/auth_service.py`에 구현.
- **감사 로그**: `events` 디렉토리에서 감사 로그 전송 또는 분석 파이프라인 연동.

## 6. 운영/배포 고려사항
- **CI/CD**: GitHub Actions, GitLab CI 등을 활용하여 lint, test, build, deploy 파이프라인 구성. 결과물은 Docker 이미지.
- **관측성**: Logging, Metrics, Tracing 구조를 `app/core/logging.py`, `app/core/observability.py` 등으로 확장.
- **설정 분리**: 환경별 `.env` 또는 Vault, AWS Parameter Store 등을 통해 비밀정보 분리.
- **도메인 주도 설계**: 엔티티, 서비스, 값 객체를 명확히 분리하여 유지보수성과 테스트 용이성 확보.

## 7. 요약
- FastAPI 기반 인증 서비스는 API 계층, 도메인 계층, 데이터 계층을 명확히 분리하는 것이 핵심.
- 디렉토리 구조를 통해 책임을 명확히 하고 버전 관리, 테스트, 배포 전략과 긴밀히 연결.
- 위 구조는 실무 환경에서 팀 단위 협업과 마이크로서비스 통합에 최적화된 패턴.
