# backend/app/main.py

from fastapi import FastAPI
from app.routers import user

app = FastAPI(
    title="Clinic Management System",
                docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc UI at http://localhost:8000/redoc
    )

app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Clinic API is running"}