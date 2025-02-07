from fastapi import FastAPI

app = FastAPI(title="Fake API", version="0.1.0")


@app.get("/", tags=["Root"])
async def root():
    return {"Hello": "World!"}
