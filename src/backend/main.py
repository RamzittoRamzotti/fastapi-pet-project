import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@app.post("/isauth")
async def isauth():
    pass
