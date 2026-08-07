# Vaalbara — Project Context

## What this is

REST API for a community platform where users propose ideas, collect votes, and convert validated ideas into location-bound events. This repo contains only the API code.

## Docs to read first

- `docs/project-brief.md` — concept, entities, features
- `docs/tech-approach.md` — stack, principles, project layout, DTO approach

## Stack

- Python 3.12+, Litestar framework
- PostgreSQL + PostGIS, SQLAlchemy ORM, asyncpg, Alembic
- REST only

## Key entities

- **Idea** — community proposal without location, users vote (likes), author converts to Event when ready
- **Event (Initiative)** — location-bound happening, lifecycle: Draft → Open → In Progress → Completed / Cancelled
- **Tag** — shared by Ideas and Events; users subscribe to tags for notifications
- **User** — nickname, verified phone + email, karma

## Code rules (enforced, not negotiable)

- Use standard Litestar features — no custom machinery where a built-in exists
- No obscure third-party libraries
- No premature abstractions — extract only when a pattern appears 3+ times and the abstraction is obvious
- Shared building blocks that ARE used: `ListResponse` DTO, single `exception_handler`, base repository methods
- DTOs via `SQLAlchemyDTO[Model]` + `DTOConfig` — no separate DTO classes unless the shape diverges from the ORM model
- Each domain folder owns: `models.py`, `dto.py`, `repository.py`, `handlers.py`
- No cross-domain imports except through explicit service calls
- Type hints everywhere
- No explanatory comments — only write a comment when the *why* is non-obvious

## Running

```bash
uv sync
PYTHONPATH=src uvicorn main:app --reload
```

## Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Project layout

```
src/
  main.py           # Litestar app, registers routers + global dependencies
  config.py         # Settings via pydantic-settings (.env)
  db.py             # SQLAlchemy engine, SessionFactory, Base, provide_db
  exceptions.py     # AppError hierarchy + app_exception_handler
  common/
    dto.py          # ListResponse[T]
    repository.py   # BaseRepository: get_by_id, list_paginated
  users/
    models.py       # User, UserOAuthAccount
    repository.py   # UserRepository
    dto.py          # UserReadDTO (SQLAlchemyDTO)
    handlers.py     # GET /users/me, PATCH /users/me
  auth/
    providers/
      base.py       # OAuthProvider Protocol + OAuthUserInfo dataclass
      google.py     # GoogleOAuthProvider
      __init__.py   # PROVIDERS dict — add new providers here
    jwt.py          # create_token / decode_token
    dependencies.py # provide_current_user
    handlers.py     # POST /auth/{provider}
alembic/
  env.py
```

## Auth flow

Frontend handles OAuth redirect. API exposes a single endpoint:

```
POST /auth/{provider}
Body: {"code": "...", "redirect_uri": "..."}
Response: {"token": "..."}
```

To add a new provider: implement `OAuthProvider` protocol in `auth/providers/`, add to `PROVIDERS` dict in `auth/providers/__init__.py`.

## Global dependencies (src/main.py)

- `db: AsyncSession` — SQLAlchemy session, injected into any handler that declares it
- `current_user: User` — resolved only for handlers that declare this parameter; raises 401 if token is missing/invalid

## What we are NOT doing

- No background task queue, no caching, no GraphQL, no WebSockets, no CQRS
