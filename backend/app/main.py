# backend/app/main.py

from fastapi import FastAPI
import app.models
from app.routers import user, auth, doctor, timeslot, available_slots, patient,appointment

app = FastAPI(
    title="Clinic Management System",
                docs_url="/docs",       # Swagger UI at http://localhost:8000/docs
    redoc_url="/redoc",     # ReDoc UI at http://localhost:8000/redoc
    )

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(timeslot.router)
app.include_router(available_slots.router)
app.include_router(patient.router)
app.include_router(appointment.router)

@app.get("/")
async def root():
    return {"message": "Clinic API is running"}