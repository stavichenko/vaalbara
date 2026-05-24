# Tech Approach

## Stack

| Layer | Choice |
|---|---|
| Language | Python 3.12+ |
| Framework | [Litestar](https://litestar.dev/) |
| Database | PostgreSQL 16+ with PostGIS |
| API style | REST |

## Principles

### Low barrier to entry

New contributors should be able to read any file and understand what it does without prior context about the project's internal conventions.

- **Prefer standard Litestar features** over custom machinery. If Litestar has a built-in way to do something, use it.
- **Avoid obscure third-party libraries.** A dependency is justified if it solves a genuinely hard problem (e.g., PostGIS bindings) and has wide adoption. Otherwise, write the 10-line helper yourself.
- **Solve the current problem only.** No speculative generality, no "we might need this later" abstractions. Three similar endpoints are better than a premature base class for two.

### Don't repeat yourself — but carefully

Duplication is fine up to a point. When the same pattern appears three or more times and the abstraction is obvious, extract it. Keep the abstraction thin and close to the call site.

Examples of shared building blocks that are worthwhile:

- **`ListResponse`** — a common dataclass/DTO wrapping paginated results (`items`, `total`, `limit`, `offset`) so every list endpoint returns the same shape.
- **`exception_handler`** — a single Litestar exception handler that maps domain exceptions to HTTP status codes, instead of `try/except` blocks scattered across handlers.
- **Base repository methods** — `get_by_id`, `list_with_pagination` shared across repositories so each one only defines entity-specific queries.

Everything else is written inline until the need to extract is clear.

### Code style

- Functions and methods do one thing.
- No deeply nested logic — early returns over `else` chains.
- Type hints everywhere; Litestar uses them for validation and OpenAPI generation.
- No comments that restate what the code says. A comment is only written when the *why* is non-obvious.

## Project layout (planned)

```
src/
  main.py            # Litestar app factory
  config.py          # Settings (via pydantic-settings or os.environ)
  db.py              # SQLAlchemy engine + session factory
  exceptions.py      # Domain exceptions + Litestar exception handler
  common/
    dto.py           # Shared DTOs (ListResponse, etc.)
    repository.py    # Base repository helpers
  users/
    models.py
    repository.py
    handlers.py
    dto.py
  ideas/
    ...
  events/
    ...
  tags/
    ...
```

Each domain folder owns its models, DTOs, repository, and HTTP handlers. No cross-domain imports except through explicit service calls.

## DTOs

We use Litestar's built-in `SQLAlchemyDTO` — DTOs are derived directly from ORM models, eliminating a separate DTO layer.

```python
class UserReadDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"password_hash"})

class UserCreateDTO(SQLAlchemyDTO[User]):
    config = DTOConfig(exclude={"id", "karma"})
```

`DTOConfig` controls which fields are exposed or writable per endpoint. A standalone dataclass or Pydantic model is only introduced when the request/response shape diverges significantly from the ORM model (e.g., aggregated input, computed fields).

The `dto.py` file in each domain folder contains only these `SQLAlchemyDTO` subclasses.

## Database access

SQLAlchemy ORM with asyncpg driver. Raw SQL is acceptable for complex PostGIS queries where the ORM abstraction adds noise. Migrations via Alembic.

## What we are not doing (yet)

- No background task queue — if async work is needed, revisit then.
- No caching layer.
- No GraphQL or WebSocket endpoints.
- No event sourcing or CQRS.
