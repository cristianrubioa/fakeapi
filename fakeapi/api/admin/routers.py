from datetime import UTC
from datetime import datetime

from fastapi import APIRouter
from fastapi import Request

from fakeapi.storage import storage

router = APIRouter()


@router.get("/admin/stats", tags=["Admin"])
async def admin_stats(request: Request):
    return {
        "active_workspaces": storage.total_count(),
        "uptime_seconds": int((datetime.now(UTC) - request.app.state.started_at).total_seconds()),
    }
