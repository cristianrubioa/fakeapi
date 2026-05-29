from pathlib import Path

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates

from fakeapi.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/", tags=["Root"])
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "base_url": settings.BASE_URL})
