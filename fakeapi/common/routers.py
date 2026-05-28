from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Root"])
async def root():
    return {"name": "FakeAPI", "version": "2.0.0", "docs": "/docs"}
