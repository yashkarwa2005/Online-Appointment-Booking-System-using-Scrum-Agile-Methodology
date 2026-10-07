# Sprint Retrospective Reports
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. The Retrospective Framework in Scrum

The **Sprint Retrospective** is an essential Scrum ceremony dedicated to **continuous improvement (Kaizen)**. The Scrum Team inspects how the iteration transpired with regard to individuals, interactions, processes, and tools, creating concrete action items for subsequent sprints.

We structured our retrospectives around three core exploratory questions:
1. 🌟 **What went well?** (Practices to celebrate and sustain)
2. ⚠️ **What didn't go as planned?** (Friction points, technical blockers, process gaps)
3. 🚀 **What can we improve next sprint?** (Measurable action items adopted by the team)

---

## 2. Sprint Retrospective Records

---

### 🔄 Sprint 1 Retrospective
- **Theme:** Development Environment, Schema Setup, Authentication
- **🌟 What went well:**
  - Fast consensus on using pure Python standard libraries (SQLite3, hashlib) for portability.
  - Salted SHA-256 password hashing established early security hygiene.
  - Good division of labor between database design and service classes.
- **⚠️ What didn't go as planned:**
  - Manual testing of database queries was repetitive and caused slight delays.
  - Initial error messages on database foreign key violations were cryptic.
- **🚀 Action Items for Next Sprint:**
  - Enabled SQLite foreign key enforcement explicitly (`PRAGMA foreign_keys = ON;`).
  - Adopted automated `unittest` test suites starting in Sprint 2 to catch regression bugs early.

---

### 🔄 Sprint 2 Retrospective
- **Theme:** Doctor Profiles, Availability Generation, Search Queries
- **🌟 What went well:**
  - Search queries with case-insensitive `LIKE` patterns delivered fast search response.
  - Pre-seeding doctors with distinct specialties provided great realistic testing data.
  - Unit tests helped quickly verify doctor listing and slot queries.
- **⚠️ What didn't go as planned:**
  - Time slot formats were initially inconsistent (`9:00` vs `09:00 AM`).
  - Doctors could theoretically enter overlapping consultation windows.
- **🚀 Action Items for Next Sprint:**
  - Standardized all database times to 24-hour `HH:MM` format.
  - Created strict slot duration validation before saving to `availability`.

---

### 🔄 Sprint 3 Retrospective
- **Theme:** Core Booking Engine, Double-Booking Prevention
- **🌟 What went well:**
  - Slicing booking into an atomic database transaction successfully stopped race conditions.
  - The team anticipated concurrency issues during planning poker and sized `US-05` to 8 points.
  - Patient booking history view worked seamlessly on the first pass.
- **⚠️ What didn't go as planned:**
  - Edge cases where a user attempted to book multiple slots at the same exact time needed manual test verification.
  - Database commit rollback handling was initially missing in the exception block.
- **🚀 Action Items for Next Sprint:**
  - Added explicit try/except blocks with `connection.rollback()` for transactional failure safety.
  - Added negative test assertions in `tests/test_appointment.py`.

---

### 🔄 Sprint 4 Retrospective
- **Theme:** Cancellation, Rescheduling & Slot Recycling
- **🌟 What went well:**
  - Atomic slot swap (releasing the old slot and claiming the new slot within the same transaction) proved extremely reliable.
  - Automatic slot recycling ensured that zero available doctor hours were wasted.
  - Team velocity remained steady at ~10-13 story points per week.
- **⚠️ What didn't go as planned:**
  - Rescheduling across different doctors was initially considered but found to complicate fee calculation.
- **🚀 Action Items for Next Sprint:**
  - Constrained rescheduling to the same medical professional to guarantee clinical continuity and consistent fee handling.

---

### 🔄 Sprint 5 Retrospective (Final Project Retrospective)
- **Theme:** Built-in Scrum Engine, Terminal Kanban Board, Integration & Viva Prep
- **🌟 What went well:**
  - Building the Scrum backlog and Kanban board inside the Python CLI directly proved to be a standout feature for the college viva!
  - 15 automated test cases ran in < 0.1s with 100% pass rate.
  - The automated `--demo` flag allows an examiner to see the entire system in action effortlessly.
- **⚠️ What didn't go as planned:**
  - Designing ASCII box drawing for terminal boards required testing across standard Windows Command Prompt and PowerShell windows.
- **🚀 Continuous Improvement Outcomes:**
  - Ensured Unicode/ASCII fallbacks so the Kanban board renders beautifully in any Windows or Linux terminal.
  - Documented complete system design and traceability matrices for examiner review.

---

## 3. Continuous Improvement Summary Matrix

```text
Iterative Improvement Cycle:
Sprint 1: Manual SQL Testing ──────► Sprint 2: Automated Unittest Framework
Sprint 2: Time Format Chaos  ──────► Sprint 3: Standardized 24h Formats
Sprint 3: Unhandled Rollbacks ─────► Sprint 4: Atomic Transactions & Rollbacks
Sprint 4: Manual Demo Friction ────► Sprint 5: Instant Automated Viva Mode (--demo)
```
