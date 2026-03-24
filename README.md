# 🏥 Clinic Management System

A web-based clinic management system that streamlines patient care by connecting patients, doctors, and administrators in one platform.

> 🚧 **Status: In Development**

---

## 💡 Project Overview

A full-stack web application for a local clinic that allows patients to book appointments, doctors to manage their schedules and patient records, and administrators to oversee the entire system.

### Key Features

- **Patient Portal** — Register, find doctors, book appointments, view medical history and prescriptions
- **Doctor Dashboard** — Manage schedule, record medical history, issue prescriptions
- **Admin Panel** — Manage doctors, patients, appointments, and the medicines list
- **Role-based Access** — Separate dashboards and permissions for Admin, Doctor, and Patient

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI (Python) |
| Database | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| AI / Chatbot | TBD — Separate repository |

---

## 🗂️ Repository Structure

```
clinic-app/          # This repo — Frontend + Backend
├── frontend/        # React application
├── backend/         # FastAPI application
│   ├── models/      # SQLAlchemy ORM models
│   ├── routers/     # API route handlers
│   └── schemas/     # Pydantic schemas
└── README.md

clinic-ai/           # Separate repo — AI/ML features (coming soon)
```

---

## 🗄️ Database

Hosted on **Supabase**. Core tables:

`User` · `Doctor` · `Patient` · `TimeSlot` · `AvailableSlot` · `Appointment` · `MedicalHistory` · `Prescription` · `PrescriptionItem` · `Medicine`

---

## 🚀 Getting Started

> Setup instructions will be added as the project progresses.

---

## 📌 Roadmap

- [ ] Database schema setup (Supabase)
- [ ] FastAPI backend — models, schemas, routes
- [ ] React frontend — all screens
- [ ] Authentication (Supabase Auth)
- [ ] AI chatbot integration

---

## 👤 Author

Built as a learning project to practice **React**, **FastAPI**, and **Supabase**.
