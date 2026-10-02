# Silver Auto — Vehicle Service Management System

A full-stack Django web app to run a vehicle service center end-to-end: customers book services, admins assign mechanics, drivers handle pickup/drop, mechanics update jobs, and the shop tracks inventory, invoices, payments, attendance and salary.

Built as a SEM-VI college project (Group No. 19, 2025–2026) and cleaned up for production-style best practices.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Database](https://img.shields.io/badge/DB-SQLite-lightgrey)
![Frontend](https://img.shields.io/badge/Frontend-Bootstrap5-purple)

## Key Features

**Role-based auth + dashboards**
- Admin, Mechanic, Driver, Customer — each with a separate dashboard and permissions
- Mechanic apply/approve flow (Pending → Approved / Rejected)

**Service workflow**
- Vehicle registration (number, brand, model, year, type)
- Service request with estimated price lookup from price chart
- Admin approve / reject, assign mechanic (status → In Progress → Completed)
- Mechanic job cards with repair notes + labor hours
- Pickup & drop scheduling with driver assignment

**Billing**
- Invoice generation with 18% GST auto-calc (total → tax → grand total)
- Payment via Cash / UPI / Card, customer invoice view
- Customer feedback with 1–5 star validation

**Shop management**
- Parts, suppliers, stock levels with low-stock alerts
- Part sales with stock deduction + insufficient-stock guard
- Mechanic attendance (Present / Absent) and monthly salary payments
- Reports page: revenue, completed jobs, payments, stock

**Tech highlights**
- 21 interconnected models across 4 apps (`accounts`, `vehicles`, `service`, `inventory`)
- Server-side validation on every form (no raw `KeyError` crashes)
- Ownership checks (e.g. customer can only use their own vehicle ID)
- Env-based settings (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`), `Asia/Kolkata` timezone
- Clean `manage.py check` with zero warnings

## Tech Stack

- Backend: Python 3.12, Django 5.2
- Database: SQLite (dev) — easy swap to PostgreSQL / MySQL via `DATABASES`
- Frontend: Django Templates + Bootstrap 5 + Bootstrap Icons (no build step)
- Auth: Django built-in User + OneToOne role profiles

## Project Structure

```
Source_Code/
├── README.md
├── .gitignore
└── silver_auto/              # Django project root (run commands here)
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    ├── db.sqlite3            # local only, git-ignored
    ├── silver_auto/          # settings, root urls, wsgi
    ├── accounts/             # users, roles, dashboards, attendance, salary
    ├── vehicles/             # vehicle types + vehicles
    ├── service/              # requests, assignments, repairs, pickup, invoice, payment, feedback
    ├── inventory/            # suppliers, parts, stock, sales
    └── templates/            # base + role-based pages (admin / customer / mechanic / driver)
```

## Quick Start

```bash
# 1. Go to Django project folder
cd silver_auto

# 2. Create + activate virtual env (Windows)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
# python3 -m venv .venv
# source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) configure env
copy .env.example .env
# Edit .env: DJANGO_SECRET_KEY, DJANGO_DEBUG, DJANGO_ALLOWED_HOSTS

# 5. Migrate + create admin
python manage.py migrate
python manage.py createsuperuser

# 6. Run server
python manage.py runserver
```

Open http://127.0.0.1:8000/

- `/` — home
- `/register/` — customer signup
- `/register/mechanic/` — mechanic application
- `/login/` — role-based redirect after login
- `/admin/` — Django admin
- `/dashboard/admin/` — shop owner dashboard

## Environment Variables

| Name | Default | Description |
|------|---------|-------------|
| `DJANGO_SECRET_KEY` | dev key | Set a strong random key in production |
| `DJANGO_DEBUG` | `True` | Set `False` in production |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts |

## Test Accounts (create locally)

No demo data is committed (DB is git-ignored). Create your own:

1. Admin: `python manage.py createsuperuser`
2. Customer: sign up at `/register/`
3. Mechanic: apply at `/register/mechanic/`, then approve as admin at `/dashboard/admin/mechanics/`
4. Driver: create `User` in `/admin/`, then add `Driver` profile linked to that user

## Useful Commands

```bash
python manage.py check              # zero warnings = healthy
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Screenshots

> Add screenshots here for recruiters (home, dashboards, service flow, invoice).

```
docs/screenshots/home.png
docs/screenshots/admin-dashboard.png
docs/screenshots/customer-request.png
docs/screenshots/invoice.png
```

## What Was Fixed in This Cleanup

- Added missing `requirements.txt`, `.env.example`, professional `.gitignore`
- Fixed `models.W042` warnings via `DEFAULT_AUTO_FIELD`
- Added missing `register/mechanic/` route (template existed but URL didn't)
- Hardened all POST handlers (`.get()` + validation, no `KeyError` / `ValueError` crashes)
- Fixed vehicle ownership check + null `vehicle_type` crash in price lookup
- Fixed mechanic approval to accept POST-only `approve` / `reject`
- Added quantity / amount / rating validation (inventory, salary, feedback, invoice, payment)
- Added duplicate username / mobile / vehicle-number guards
- Moved secrets to env vars, fixed `STATIC_URL`, added `STATIC_ROOT`, set `Asia/Kolkata` timezone
- Verified `check`, `migrate`, URL reverse all pass

## Future Improvements

- Class-based views + Django Forms for cleaner validation
- PostgreSQL + media storage for production deploy
- REST API (DRF) for mobile app
- Automated tests (currently 0 tests — good first contribution)
- CI (GitHub Actions: check + migrate + test)

## Team

SEM-VI Vehicle Service Management — Group No. 19 (2025–2026)

## License

MIT — free for learning and portfolio use.
