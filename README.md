# Medical Appointment System

A full-stack medical appointment booking platform built with **Django REST Framework** on the backend and **React + Vite** on the frontend. Patients can find doctors, book time slots, and manage appointments. Doctors control their own schedule. Admins oversee the entire system.

---

## Team

| Member | Responsibility |
|---|---|
| **Mohamed Mahdy** | Project initialization · Auth system (JWT) · Login & Register pages · User profile page |
| **Ahmed Yahya** | Admin dashboard · Permissions · Appointment model & API · Appointment pages (frontend) |
| **Yamen Aly** | Patient profile model · Patient CRUD API · Patient pages (frontend) · Slot generation logic |
| **Mohamed Nasef** | Doctor profile model · Doctor CRUD API · Doctor pages (frontend) |
| **Zahwa Kandeel** | Availability model · Availability CRUD API · Availability page (frontend) · Email confirmation |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Django 4.x, Django REST Framework |
| Authentication | djangorestframework-simplejwt |
| Database | PostgreSQL (SQLite for development) |
| Frontend | React 18, Vite |
| Routing | React Router v6 |
| State | Context API |
| Styling | CSS custom properties (no Bootstrap) |
| API Docs | drf-spectacular (Swagger UI) |
| Email | Django SMTP / Console backend |

---

## Backend Setup

### 1. Clone the repository

```bash
git clone <https://github.com/Mohamed-Mahdy7/Medical-Project>
cd medical_project/backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=medical_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# Email — use console backend in development (prints to terminal, no SMTP needed)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
DEFAULT_FROM_EMAIL=noreply@medicalapp.com
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (Admin account)

```bash
python manage.py createsuperuser
```

You will be prompted to enter:

```
Username: admin
Email address: admin@clinic.com
Password: ••••••••
Password (again): ••••••••
```

Once created, this account has full admin access to:
- Django Admin panel at `http://localhost:8000/admin/`
- All admin API endpoints under `/api/v1/admin/`


## Frontend Setup

### 1. Navigate to the frontend directory

```bash
cd medical_project/frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

Frontend available at: `http://localhost:5173`

> Make sure the backend server is running before using the frontend — all API calls point to `http://localhost:8000`.

---

## User Roles

### Admin
- Created via `createsuperuser` in the terminal — not via the registration page
- Approves or blocks doctor accounts before they can use the system
- Manages specialties (Cardiology, Dermatology, etc.)
- Views all appointments across the entire system
- Full access to Django Admin panel

### Doctor
- Registers via the frontend `/register` page
- Account starts as **pending** — cannot log in until an admin approves it
- Once approved: sets weekly availability schedule, views and manages appointments, adds clinical notes after visits

### Patient
- Registers via the frontend `/register` page
- Account is **immediately active** — no approval step needed
- Browses doctors by name or specialty, views available time slots, books appointments, cancels or reschedules

---

## Appointment Status Lifecycle

```
PENDING ──► CONFIRMED ──► COMPLETED
   │              │
   └──────────────┴──► CANCELLED
```

| Status | Meaning | Who sets it |
|---|---|---|
| `PENDING` | Booked, waiting on doctor | System (automatic on booking) |
| `CONFIRMED` | Doctor accepted | Doctor |
| `COMPLETED` | Appointment took place | Doctor |
| `CANCELLED` | Dropped before visit | Patient or Doctor |

---
## Running Tests

```bash
cd backend
pytest
```

---

## Environment Variables Reference

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | Debug mode (`True` in dev, `False` in prod) |
| `DB_NAME` | PostgreSQL database name |
| `DB_USER` | PostgreSQL user |
| `DB_PASSWORD` | PostgreSQL password |
| `DB_HOST` | Database host (default: `localhost`) |
| `DB_PORT` | Database port (default: `5432`) |
| `ACCESS_TOKEN_LIFETIME_MINUTES` | JWT access token expiry |
| `REFRESH_TOKEN_LIFETIME_DAYS` | JWT refresh token expiry |
| `EMAIL_BACKEND` | Django email backend class |
| `EMAIL_HOST_USER` | SMTP sender address |
| `EMAIL_HOST_PASSWORD` | SMTP password |
| `DEFAULT_FROM_EMAIL` | Display address for outgoing emails |