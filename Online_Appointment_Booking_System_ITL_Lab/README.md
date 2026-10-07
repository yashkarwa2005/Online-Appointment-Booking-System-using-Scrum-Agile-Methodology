# MediFlow · Online Appointment Booking System
### ITL Lab Project & Scrum Agile PBL

A complete, self-contained Python web application for scheduling and managing healthcare appointments with atomic concurrency control, live printable receipts, and an integrated Agile Scrum Kanban management engine.

---

## Quickstart (Run on Laptop)

### Double-click:
Just double-click **`run.bat`** in this folder!

### Or via Terminal:
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser.

---

## Run Automated Unit Tests (15/15 Pass)
```bash
python -m unittest discover tests -v
```

---

## Project Structure
```text
Online_Appointment_Booking_System_ITL_Lab/
├── app.py                     # Web server & REST API backend (Python standard library)
├── run.bat                    # One-click Windows launcher
├── ITL_LAB_MANUAL.md          # Complete lab report and Viva questions/answers
├── requirements.txt           # Dependency requirements (Zero mandatory pip packages needed)
├── database/
│   └── appointment.db         # SQLite database pre-seeded with specialists & slots
├── src/
│   ├── database.py            # SQLite schema, hashing & seed data
│   ├── appointment.py         # Business logic: atomic booking, cancel, reschedule
│   ├── user_story.py          # Agile User Story manager
│   ├── sprint.py              # Sprint metrics & burndown engine
│   ├── action_item.py         # Scrum Action Item tracker
│   └── kanban.py              # Terminal & SQLite Kanban renderer
├── templates/
│   └── index.html             # Full-featured responsive Web Dashboard
└── tests/
    └── test_appointment_system.py # 15 automated unit test cases
```
