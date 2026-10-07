# Online Appointment Booking System (MediFlow)
## Information Technology Lab (ITL) & Agile Methodologies (AM) PBL Project Manual
**Academic Year:** 2026-2027 | **Semester:** 5 | **Branch:** B.Tech Computer Engineering / Information Technology  
**Student Name:** Yash Karwa | **Topic:** Online Appointment Booking System using Scrum Agile Methodology  

---

## 1. Project Objective & Aim

To design, develop, and demonstrate a robust, concurrent **Online Appointment Booking System** (`MediFlow`) managed under the **Scrum Agile Methodology**. The system streamlines patient-doctor appointment scheduling, prevents double-booking through atomic database transactions, produces instant digital receipts, and provides transparent administrative oversight alongside a live Scrum Kanban engine.

---

## 2. Technology Stack & Prerequisites

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ (Tested on 3.13) | Standard library `http.server`, multi-threaded request dispatcher |
| **Database** | SQLite3 | Relational ACID database with Foreign Keys enabled (`PRAGMA foreign_keys = ON`) |
| **Security** | SHA-256 + Salted Hashing | Cryptographic credential protection against rainbow table attacks |
| **Frontend** | HTML5, CSS3, Vanilla JS | Dark/Light modern medical UI with glassmorphism card design |
| **Testing** | Python `unittest` framework | 15 comprehensive automated unit tests covering all core modules |
| **Agile Tools** | GitHub Projects V2 & In-App Kanban | 5-stage Kanban flow (Backlog, Todo, In Progress, Review, Done) |

---

## 3. How to Run the Project on Laptop for Demonstration

### Method 1: One-Click Double Click (Recommended)
1. Navigate to the project folder:
   ```text
   Online_Appointment_Booking_System_ITL_Lab/
   ```
2. Double-click the file:
   ```text
   run.bat
   ```
3. The terminal server starts, connects to `appointment.db`, and **automatically opens your web browser** at:
   ```text
   http://127.0.0.1:5000
   ```

### Method 2: Via Terminal Command Line
```powershell
# Open terminal inside the folder and execute:
python app.py
```

### Method 3: Run Automated Test Suite (To show 100% test pass to teacher)
```powershell
python -m unittest discover tests -v
```
*(All 15 unit tests pass in under 0.15s)*

---

## 4. Key Functional Modules Demonstrated to Evaluator

### Module 1: Patient Appointment Booking (Patient Portal)
- Filter doctors by department: **Cardiology**, **Neurology**, **Dermatology**.
- View doctor profile, clinical bio, and consultation fee.
- Real-time date selector (`2026-10-15`, `2026-10-16`, `2026-10-17`).
- Slot chips show open 30-minute intervals (`09:00 - 09:30`, `10:00 - 10:30`, etc.).
- Input patient symptoms and click **"Confirm & Lock Slot"**.

### Module 2: Official Printable Confirmation Slip / Receipt
- Upon confirmation, an official formatted slip is displayed:
  - Appointment ID (`#APT-101`)
  - Patient Name & Doctor Name
  - Specialization & Department
  - Appointment Date & Time
  - Fee Paid status
- Click **"Print / Download Slip"** to invoke real browser print preview.

### Module 3: Patient History & Atomic Slot Recovery
- Navigate to **"My Appointments"**.
- View list of upcoming and past consultations with status badges: `Confirmed` (Green), `Cancelled` (Red), `Completed` (Blue).
- One-click **Cancel Appointment**: The system atomically updates the appointment status and immediately restores the availability slot back to `is_booked = 0` for other patients.

### Module 4: Doctor Schedule & Clinic Consultation Queue
- Doctor can view their active daily patient queue.
- Doctor can mark appointments as **Completed**.
- Doctor can add new consultation time slots for upcoming dates.

### Module 5: Hospital Administration & System Audit Trail
- Real-time metrics: Total Registered Patients, Total Specialists, Confirmed Bookings, Total Clinic Revenue.
- **Audit Trail Log**: Real-time immutable record of system events (`APPOINTMENT_BOOKED`, `APPOINTMENT_CANCELLED`, `SLOT_CREATED`, `KANBAN_MOVE`).

### Module 6: Agile Scrum PBL Kanban Board
- Displays 15 User Stories across the 5 Scrum stages:
  1. `📋 Backlog` (Sprint 6+ future enhancements)
  2. `📝 To Do` (Upcoming sprint backlog)
  3. `⚙️ In Progress` (Active sprint tasks)
  4. `🔍 Review / Testing` (Verification & code review)
  5. `✅ Done` (Completed and accepted user stories)
- Stories show Story Points (`3 pts`, `5 pts`, `8 pts`) and MoSCoW Priority tags:
  - 🔴 **High Priority (Must Have)**
  - 🟠 **Medium Priority (Should Have)**
  - 🟢 **Low Priority (Could Have)**
- Click **◀** or **▶** on any card to move it across columns in real time, immediately persisting to the SQLite database!

---

## 5. Database Schema & Architecture

```
                  ┌──────────────────────┐
                  │        users         │
                  ├──────────────────────┤
                  │ id (PK)              │
                  │ username (UNIQUE)    │
                  │ password_hash        │
                  │ full_name            │
                  │ role (patient/doc)   │
                  └──────────┬───────────┘
                             │ 1:1
                             ▼
┌────────────────────────┐  ┌──────────────────────┐
│     availability       │  │    professionals     │
├────────────────────────┤  ├──────────────────────┤
│ id (PK)                │  │ id (PK)              │
│ professional_id (FK) ◄─┼──┤ user_id (FK)         │
│ date                   │  │ specialization       │
│ start_time / end_time  │  │ department           │
│ is_booked (0/1)        │  │ consultation_fee     │
└───────────┬────────────┘  └──────────┬───────────┘
            │ 1:1                      │ 1:N
            └────────────┬─────────────┘
                         │
                         ▼
             ┌────────────────────────┐
             │      appointments      │
             ├────────────────────────┤
             │ id (PK)                │
             │ user_id (FK)           │
             │ professional_id (FK)   │
             │ availability_id (FK)   │
             │ appointment_date       │
             │ status (Confirmed/...) │
             └────────────────────────┘
```

---

## 6. Viva-Voce Questions & Model Answers for Examiner

### Q1: How does your system prevent two patients from booking the exact same time slot concurrently (Race Condition)?
**Answer:**  
In `src/appointment.py`, slot reservation is enclosed within an **atomic database transaction**. When a patient attempts to book, SQLite executes an immediate check:
```sql
SELECT is_booked FROM availability WHERE id = ?;
```
If `is_booked != 0`, the transaction immediately aborts and raises a `ValueError("Slot already booked")`. If free, it sets `is_booked = 1` and creates the appointment record in the same atomic commit. This guarantees ACID isolation and prevents double-booking.

### Q2: How is Scrum Agile methodology applied in this project?
**Answer:**  
Development was executed across **5 distinct Sprints**:
- **Sprint 1:** Architecture & User Authentication (US-01, US-02)
- **Sprint 2:** Doctor Directory & Availability (US-03, US-04)
- **Sprint 3:** Atomic Booking & Concurrency Lock (US-05)
- **Sprint 4:** Cancellation, Rescheduling & Receipts (US-06 to US-09)
- **Sprint 5:** Doctor Management, Admin Audit & Kanban Engine (US-10 to US-12)
All user stories have Story Points (Fibonacci scale: 1, 2, 3, 5, 8), clear Acceptance Criteria, and MoSCoW prioritization.

### Q3: What is the purpose of the Backlog column?
**Answer:**  
The **Product Backlog** represents the master inventory of prioritized requirements and future features that have not yet been committed to an active Sprint (e.g., SMS Reminders, Telehealth Video Consultations). During Sprint Planning, the highest-priority items are refined and moved from the Backlog to the **To Do** column (Sprint Backlog).

### Q4: How are passwords secured in the database?
**Answer:**  
Passwords are never stored in plaintext. They are salted with a project-specific key and hashed using the cryptographic **SHA-256** algorithm (`hashlib.sha256(f"{salt}_{password}".encode()).hexdigest()`), protecting against dictionary and precomputed rainbow table attacks.
