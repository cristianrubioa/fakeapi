# FakeAPI

**FakeAPI** is a multi-resource REST API built with FastAPI for testing, prototyping, and learning purposes. Unlike other fake APIs, FakeAPI does **real in-memory CRUD** — your changes actually persist within a workspace session. No database required.

## Quickstart

```bash
# 1. Create a workspace — your isolated copy of all seed data
curl -X POST https://fakeapi.crubio.fyi/workspaces/
# → {"id": "abc-123", "expires_at": "...", "extend_count": 0, "plan": "free"}

# 2. Use it
curl https://fakeapi.crubio.fyi/ws/abc-123/tasks/?status=pending&sort_by=-created_at

# 3. Reset to seed state any time
curl -X POST https://fakeapi.crubio.fyi/ws/abc-123/reset
```

## Resources

Each workspace contains three resources with full CRUD, filtering, sorting, and pagination:

| Resource | Endpoint | Seed records |
|---|---|---|
| Tasks | `/ws/{id}/tasks/` | 30 |
| Users | `/ws/{id}/users/` | 10 |
| Projects | `/ws/{id}/projects/` | 10 |

Tasks carry `user_id` and `project_id` foreign keys. Nested routes expose the relations:

```
GET /ws/{id}/users/{user_id}/tasks
GET /ws/{id}/projects/{project_id}/tasks
```

## Query Parameters

All list endpoints support:

| Param | Example | Description |
|---|---|---|
| `sort_by` | `?sort_by=-created_at` | Prefix `-` for descending |
| `page` | `?page=2` | 1-based page number |
| `page_size` | `?page_size=10` | Items per page (max 100) |
| `status` | `?status=pending` | Filter by any field value |

## Workspace Lifecycle

Workspaces are **ephemeral by design** — the perfect clean slate for testing.

| Endpoint | Description |
|---|---|
| `POST /workspaces/` | Create a workspace (pre-loaded with seed data) |
| `GET /workspaces/{id}` | Get workspace metadata and TTL |
| `POST /workspaces/{id}/extend` | Add 24h to TTL (max 3 times) |
| `POST /workspaces/{id}/reset` | Restore all data to initial seed state |

Workspaces expire after **24 hours**. Inactive workspaces are cleaned up automatically.

## Limits (free plan)

- Max 3 workspaces per IP
- Max 100 records per resource per workspace
- Rate limit: 60 requests/minute

## Features

- Real CRUD — POST/PATCH/DELETE actually modify workspace state
- Workspace isolation — changes in one workspace don't affect others
- Nested routes — `GET /ws/{id}/users/1/tasks` returns user 1's tasks
- Full query params on every list endpoint
- OpenAPI docs at `/docs`
- No authentication required

## Live Demo

**URL:** [https://fakeapi.crubio.fyi](https://fakeapi.crubio.fyi)

*Deployed on a dedicated server via Cloudflare tunnel — always on, no cold starts.*

Legacy Render demo (v1): [https://fakeapi-kynw.onrender.com](https://fakeapi-kynw.onrender.com) *(may sleep)*

## Tech Stack

- Python 3.12
- FastAPI
- slowapi (rate limiting)
- Pydantic v2
- Poetry
