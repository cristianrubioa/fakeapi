# FakeAPI

A REST API for testing and prototyping — real in-memory CRUD that persists within an isolated workspace session. No database, no auth.

![FakeAPI](docs/screenshot.png)

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
curl -X POST https://fakeapi-kynw.onrender.com/api/workspaces/

# Use it
curl https://fakeapi-kynw.onrender.com/api/workspaces/{id}/tasks/?status=pending&sort_by=-created_at

# Reset to seed state any time
curl -X POST https://fakeapi-kynw.onrender.com/api/workspaces/{id}/reset
```

Interactive docs at `/docs`.

## Resources

Each workspace comes pre-loaded with seed data and supports full CRUD, filtering, sorting, and pagination.

| Resource | Endpoint | Seed |
|---|---|---|
| Tasks | `/api/workspaces/{id}/tasks/` | 30 records |
| Users | `/api/workspaces/{id}/users/` | 10 records |
| Projects | `/api/workspaces/{id}/projects/` | 10 records |

Nested routes: `GET /api/workspaces/{id}/users/{user_id}/tasks` · `GET /api/workspaces/{id}/projects/{project_id}/tasks`

## Limits (free plan)

| | |
|---|---|
| Workspaces per IP | 3 |
| Records per resource | 100 |
| Workspace TTL | 24h · extendable up to 3x |
| Rate limit | 60 req/min |

## Live

| | |
|---|---|
| **Render** | [https://fakeapi-kynw.onrender.com](https://fakeapi-kynw.onrender.com) — free tier, always available. First request may take ~1 min to wake the server. |
| **Personal** | [https://fakeapi.crubio.fyi](https://fakeapi.crubio.fyi) — runs from my machine via a Cloudflare tunnel. May be offline. Use Render if this doesn't respond. |

## Smoke tests

Contract validation against a live deployment:

```bash
cp .env.example .env        # set FakeAPI_BASE_URL to the target deployment
make smoke
```

`FakeAPI_BASE_URL` can also be passed inline: `FakeAPI_BASE_URL=http://localhost:8000 make smoke`.

Postman collection with pre-loaded examples: [docs/postman_collection.json](docs/postman_collection.json).

## Docs

- [Architecture](docs/architecture.md)
- [Models](docs/models.md)
- [CI](docs/ci.md)
