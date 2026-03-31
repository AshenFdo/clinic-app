# backend/app/main.py

from fastapi import FastAPI
import app.models
from app.routers import user
from app.routers import auth

app = FastAPI(
    title="Clinic Management System",
                docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc UI at http://localhost:8000/redoc
    )

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Clinic API is running"}