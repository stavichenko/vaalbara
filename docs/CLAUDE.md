# Vaalbara — Project Context

## What this is

REST API for a community platform where users propose ideas, collect endorsements, 
and convert validated ideas into location-bound events. This repo contains only the API code.

## Docs to read first

- `docs/project-brief.md` — concept, entities, features
- `docs/tech-approach.md` — stack, principles, project layout, DTO approach
- `docs/auth.md` — auth flow

## Stack

- Python 3.12+, Litestar framework
- PostgreSQL + PostGIS, SQLAlchemy ORM, asyncpg, Alembic


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
