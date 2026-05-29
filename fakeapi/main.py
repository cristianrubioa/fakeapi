import asyncio
from contextlib import asynccontextmanager
from datetime import UTC
from datetime import datetime

from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from fakeapi.api.admin.routers import router as admin_router
from fakeapi.api.projects.routers import router as projects_router
from fakeapi.api.tasks.routers import router as tasks_router
from fakeapi.api.users.routers import router as users_router
from fakeapi.api.workspaces import services as workspace_services
from fakeapi.api.workspaces.routers import router as workspaces_router
from fakeapi.common.limiter import limiter
from fakeapi.common.middleware import BodySizeLimitMiddleware
from fakeapi.common.routers import router as common_router


async def _cleanup_loop():
    while True:
        await asyncio.sleep(3600)
        workspace_services.cleanup_expired()


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(_cleanup_loop())
    app.state.started_at = datetime.now(UTC)
    app.state.limiter = limiter
    yield
    task.cancel()


app = FastAPI(title="FakeAPI", version="2.0.0", lifespan=lifespan)
app.state.limiter = limiter


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": f"Rate limit exceeded: {exc.detail}"},
        headers={"Retry-After": str(exc.retry_after) if hasattr(exc, "retry_after") else "60"},
    )


app.add_middleware(BodySizeLimitMiddleware)

app.include_router(common_router)
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])
app.include_router(workspaces_router, prefix="/api/workspaces", tags=["Workspaces"])
app.include_router(tasks_router, prefix="/api/workspaces/{workspace_id}/tasks", tags=["Tasks"])
app.include_router(users_router, prefix="/api/workspaces/{workspace_id}/users", tags=["Users"])
app.include_router(projects_router, prefix="/api/workspaces/{workspace_id}/projects", tags=["Projects"])
