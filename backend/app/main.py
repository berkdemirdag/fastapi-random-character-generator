from fastapi import FastAPI
from app.routers import auth as auth_router
from app.routers import character as character_router
from app.routers import user as user_router

app = FastAPI(
    title="Random Character Generator API",
    description="A professional API for D&D-style character management",
    version="1.0.0"
)
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(character_router.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to the Random Character Generator API",
        "docs": "/docs"
    }