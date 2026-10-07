# backend/app/main.py

from fastapi import FastAPI
import app.models
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth


app = FastAPI(
    title="Clinic Management System",
                docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc UI at http://localhost:8000/redoc
    )

# CORS configuration to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server URL
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth.router) 

@app.get("/")
async def root():
    return {"message": "Clinic API is running"}