from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.backend.books_utils.books import books_router
from src.backend.jwt_utils.validation import is_admin
from src.backend.jwt_utils.demo_jwt_auth import router

app = FastAPI()
app.mount("/images", StaticFiles(directory="src/frontend/public/images"), name="images")
app.include_router(router)
app.include_router(books_router)
origins = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:5005",
    "http://localhost:5000",
    "http://localhost:5010",
    "http://127.0.0.1:5000"

]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def read_root():
    return {"Hello": "World"}


@app.get("/is-admin")
async def check_admin():
    admin = await is_admin()
    return admin

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5005)
