# A small REST API project built with FastAPI and PostgreSQL

It includes:
- **Auth Service**: user registration + login with JWT
- **PDF Service**: generates a **PDF with the user profile** and returns it as a downloadable file

Services are split and communicate **only via JWT** (no shared database).

---

## Tech Stack

- Python 3.12+
- FastAPI (async endpoints)
- PostgreSQL 16
- SQLAlchemy 2.0 (async) + `asyncpg`
- Alembic migrations
- JWT (HMAC / HS256)
- Pytest + pytest-asyncio + httpx
- Docker + docker-compose

---

## Services

### 1) Auth Service (port **8000**)

- `POST /auth/register` — register new user  
  Fields: `name`, `surname`, `email`, `date_of_birth`, `password`
- `POST /auth/login` — login and receive JWT (`access_token`)
- `GET /health` — health check

Docs (Swagger):
- http://localhost:8000/docs

---

### 2) PDF Service (port **8001**)

- `GET /profile/pdf` — returns a downloadable `profile.pdf` with:
  - Name
  - Surname
  - Email
  - Date of birth

Auth: **Bearer JWT** in `Authorization` header.
- Valid JWT → `200` + PDF file
- Invalid JWT → `401`

Docs (Swagger):
- http://localhost:8001/docs

---

## Quick Start (one command)

> Main runner: **docker compose**

```bash
docker compose up --build
```

---
## After startup:

Auth service: http://localhost:8000/docs

PDF service: http://localhost:8001/docs

---

## Stop:
```bash
docker compose down
```

---
## Remove data volume (fresh database):

```bash
docker compose down -v
```

## Database & Migrations

Auth service uses PostgreSQL + SQLAlchemy 2.0 async (`asyncpg`) with connection pooling.

Migrations are managed with Alembic.

## Running Tests (isolated)

A separate compose file (`docker-compose.test.yml`) is used to run tests with an isolated PostgreSQL database (`test_db`).

### Run the full test stack (auth + pdf + test_db)
```bash
docker compose -f docker-compose.yml -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from auth_tests
```

### Clean run (fresh volumes)
```bash
docker compose -f docker-compose.yml -f docker-compose.test.yml down -v --remove-orphans
```

## Services are independent:

- **Auth Service** stores users in PostgreSQL.
- **PDF Service** has **no database** and validates requests **only via JWT**.
- JWT contains enough profile claims to generate the PDF.
- All endpoints are async; DB uses connection pooling.
