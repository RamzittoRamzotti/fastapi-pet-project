from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
    pass