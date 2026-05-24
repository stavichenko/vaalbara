# Vaalbara

Web platform for creating local events and validating ideas through community voting.

## Documentation

- [Project Brief](docs/project-brief.md) — concept overview and key features
- [Tech Approach](docs/tech-approach.md) — stack, principles, and project layout

## Quick Start

**1. Install dependencies**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh  # skip if uv is already installed
uv sync
```

**2. Start PostgreSQL**
```bash
docker compose up -d
```

**3. Configure environment**
```bash
cp .env.example .env
```

Edit `.env` and fill in the values:
```
DATABASE_URL=postgresql+asyncpg://vaalbara:vaalbara@localhost:5432/vaalbara
JWT_SECRET=any-random-string
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

**4. Run migrations**
```bash
uv run alembic upgrade head
```

**5. Start the server**
```bash
uv run uvicorn main:app --reload --app-dir src
```

API: [http://localhost:8000](http://localhost:8000)  
Swagger UI: [http://localhost:8000/schema/swagger](http://localhost:8000/schema/swagger)
