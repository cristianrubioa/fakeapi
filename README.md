# FakeAPI

A REST API for testing and prototyping — real in-memory CRUD that persists within an isolated workspace session. No database, no auth.

## Stack

| | |
|---|---|
| Runtime | Python 3.12 · FastAPI · Pydantic v2 |
| Rate limiting | slowapi |
| Testing | pytest · pytest-cov |
| Packaging | Poetry |

## Quick start

```bash
# Create a workspace — isolated copy of all seed data
curl -X POST https://fakeapi.crubio.fyi/workspaces/

# Use it
curl https://fakeapi.crubio.fyi/ws/{id}/tasks/?status=pending&sort_by=-created_at

# Reset to seed state any time
curl -X POST https://fakeapi.crubio.fyi/ws/{id}/reset
```

Interactive docs at `/docs`.

## Resources

Each workspace comes pre-loaded with seed data and supports full CRUD, filtering, sorting, and pagination.

| Resource | Endpoint | Seed |
|---|---|---|
| Tasks | `/ws/{id}/tasks/` | 30 records |
| Users | `/ws/{id}/users/` | 10 records |
| Projects | `/ws/{id}/projects/` | 10 records |

Nested routes: `GET /ws/{id}/users/{user_id}/tasks` · `GET /ws/{id}/projects/{project_id}/tasks`

## Limits (free plan)

| | |
|---|---|
| Workspaces per IP | 3 |
| Records per resource | 100 |
| Workspace TTL | 24h · extendable up to 3x |
| Rate limit | 60 req/min |

## Live

**[https://fakeapi.crubio.fyi](https://fakeapi.crubio.fyi)** — dedicated server via Cloudflare tunnel, always on.

## Smoke tests

Contract validation against a live deployment:

```bash
cp .env.example .env        # set SMOKE_BASE_URL to the target deployment
make smoke
```

`SMOKE_BASE_URL` can also be passed inline: `SMOKE_BASE_URL=http://localhost:8000 make smoke`.

Postman collection with pre-loaded examples: [docs/postman_collection.json](docs/postman_collection.json).

## Docs

- [Architecture](docs/architecture.md)
- [Models](docs/models.md)
- [CI](docs/ci.md)
