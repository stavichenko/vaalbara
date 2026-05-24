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

## Project layout

```
src/
  main.py
  config.py
  db.py
  exceptions.py
  common/
    dto.py        # ListResponse, shared DTOs
    repository.py # base get_by_id, list_with_pagination
  users/
  ideas/
  events/
  tags/
```

## What we are NOT doing

- No background task queue, no caching, no GraphQL, no WebSockets, no CQRS
