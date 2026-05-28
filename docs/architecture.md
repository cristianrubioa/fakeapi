# Architecture

## System Overview

```mermaid
flowchart TD
    Client([HTTP Client]) --> MW

    subgraph FakeAPI["FakeAPI — FastAPI"]
        MW["Middleware · BodySizeLimit · RateLimit"]
        MW --> R

        subgraph R["Routers"]
            ROOT["GET /"]
            ADMIN["GET /admin/stats"]
            WS["POST · GET /workspaces/"]
            WSA["GET · extend · reset /workspaces/{id}"]
            TASKS["/ws/{id}/tasks — full CRUD"]
            USERS["/ws/{id}/users — full CRUD"]
            PROJ["/ws/{id}/projects — full CRUD"]
        end

        R --> DEP["get_workspace · validates id · checks expiry"]
        DEP --> SVC["Services"]
        SVC --> STG[("InMemoryStorage")]
    end

    CL["Cleanup loop · every 1h"] --> STG
```

## Request Pipeline — List Endpoints

Every list endpoint runs through three stacked decorators before returning a response.

```mermaid
flowchart LR
    Handler["Route handler"] --> Sort["@sort · sort_by param · prefix - for desc"]
    Sort --> Filter["@filter · field=value query params · exact match"]
    Filter --> Paginate["@paginate · page · page_size · max 100"]
    Paginate --> Resp["{ count, next, previous, results }"]
```

## Workspace Lifecycle

```mermaid
flowchart TD
    POST["POST /workspaces/"] --> Check["IP limit · global limit"]
    Check -->|ok| Seed["Snapshot seed data · 30 tasks · 10 users · 10 projects"]
    Check -->|exceeded| Err(["429 · 503"])
    Seed --> WS[("Workspace · UUID · 24h TTL")]

    WS --> CRUD["CRUD on tasks · users · projects · isolated per workspace"]
    WS --> Extend["POST /extend · +24h · max 3 times"]
    WS --> Reset["POST /reset · restore seed snapshot"]

    Extend --> WS
    Reset --> WS

    WS -->|expires_at passes| Expired
    Expired["Expired workspace"] --> Cleanup["Cleanup loop · purged every 1h"]
```

## Module Layout

```mermaid
flowchart TD
    main["main.py · FastAPI app · lifespan · middleware · routers"]

    main --> common["common/ · middleware · limiter · pagination · decorators · enums"]
    main --> admin["admin/ · /admin/stats"]
    main --> workspaces["workspaces/ · models · services · routers · dependencies"]
    main --> tasks["tasks/ · models · enums · services · routers"]
    main --> users["users/ · models · enums · services · routers"]
    main --> projects["projects/ · models · enums · services · routers"]

    workspaces --> storage["storage/ · WorkspaceStorage ABC · InMemoryStorage"]
    tasks --> storage
    users --> storage
    projects --> storage

    storage --> seed["seed.py · get_seed_snapshot · deep copy per workspace"]
    workspaces --> seed
```
