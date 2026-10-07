# Testing Strategy & Test Execution Report
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Testing Strategy in Scrum Agile

In Agile development, testing is not an afterthought phase; it is an integral, continuous activity performed during every sprint iteration.

### Testing Levels Implemented
1. **Unit Testing:** Validates isolated methods (e.g., password hashing, story points calculation, status validation) in `unittest`.
2. **Integration Testing:** Validates transactional multi-table flows (e.g., booking an appointment locks an availability slot).
3. **Negative & Edge-Case Testing:** Explicitly stresses error handling, such as duplicate registration, invalid passwords, double-booking collisions, and unauthorized cancellations.
4. **Acceptance Testing:** Verifies that completed user stories satisfy 100% of the criteria outlined in [readme/ACCEPTANCE_CRITERIA.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md) before passing the Definition of Done (DoD).

---

## 2. Test Execution Environment
- **Test Framework:** Python `unittest` (Built-in standard library)
- **Database Engine:** SQLite (In-Memory `:memory:` and dedicated test database)
- **Test Suite Location:** `tests/test_appointment.py`
- **Execution Command:**
  ```bash
  python -m unittest discover tests -v
  ```
  or
  ```bash
  python src/main.py --test
  ```

---

## 3. Comprehensive Test Case Specifications & Results

| Test ID | Module / Story | Test Scenario | Preconditions | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| **TC-01** | `US-01` Auth | User registration with valid new credentials | Empty test user table | username: `new_user`, password: `Secret@123`, role: `patient` | User created with unique ID and hashed password | User created, hashed password verified | 🟢 PASS |
| **TC-02** | `US-01` Auth | Duplicate username registration rejection | User `rohan_s` exists | username: `rohan_s`, email: `diff@example.com` | Registration rejected with duplicate error | Rejected with `ValueError: Username already exists` | 🟢 PASS |
| **TC-03** | `US-02` Auth | User login with valid credentials | User `rohan_s` registered | username: `rohan_s`, password: `Password123!` | Valid session dictionary with role `patient` | Session returned with matching user details | 🟢 PASS |
| **TC-04** | `US-02` Auth | User login with invalid password | User `rohan_s` registered | username: `rohan_s`, password: `WrongPassword` | Authentication fails; returns None / Error | Returns None; login rejected | 🟢 PASS |
| **TC-05** | `US-03` Search | Search doctors by specialization keyword | Doctors seeded in DB | query: `cardio` | Returns list containing Dr. Priya Verma (Cardiologist) | Returns Cardiology specialist records | 🟢 PASS |
| **TC-06** | `US-04` Slots | Query unbooked slots for doctor | Doctor has 3 open slots | doctor_id: `1` | Returns only slots where `is_booked = 0` | 3 slots returned; booked slots excluded | 🟢 PASS |
| **TC-07** | `US-05` Booking | Book an open appointment slot | Slot `S1` is unbooked (`is_booked=0`) | user_id: `1`, slot_id: `S1` | Appointment created as `Confirmed`; slot `is_booked` becomes `1` | Appointment ID generated; slot locked | 🟢 PASS |
| **TC-08** | `US-05` Booking | Prevent double-booking on already booked slot | Slot `S1` is already booked | user_id: `2`, slot_id: `S1` | Booking rejected with conflict error; no duplicate record | `ValueError: Slot already booked` raised; no change | 🟢 PASS |
| **TC-09** | `US-06` History | Retrieve patient appointment history | Patient has 2 bookings | user_id: `1` | List of 2 bookings with doctor name, date, and status | Exactly 2 bookings retrieved with correct fields | 🟢 PASS |
| **TC-10** | `US-07` Cancel | Cancel confirmed appointment & release slot | Active booking on slot `S1` | appointment_id: `A1`, user_id: `1` | Status changed to `Cancelled`; slot `S1` becomes `is_booked = 0` | Status updated; slot unlocked for reuse | 🟢 PASS |
| **TC-11** | `US-08` Resched | Reschedule appointment to new open slot | Active booking on `S1`, open slot `S2` | appt_id: `A1`, new_slot_id: `S2` | Old slot `S1` freed (0); new slot `S2` locked (1); appt updated | Atomic swap succeeded; dates updated | 🟢 PASS |
| **TC-12** | `US-10` Doctor | Doctor publishes new availability slot | Valid doctor profile | date: `2026-10-25`, start: `14:00`, end: `14:30` | New slot inserted with `is_booked = 0` | Slot ID returned; visible in doctor schedule | 🟢 PASS |
| **TC-13** | `US-11` Admin | Admin views all cross-hospital appointments | Multiple patient bookings | admin user authenticated | Returns complete audit list across all doctors and patients | Complete appointment records returned | 🟢 PASS |
| **TC-14** | `US-12` Scrum | Create User Story and assign MoSCoW priority | Sprint exists in DB | code: `US-99`, pts: `5`, priority: `Must Have` | Story created in `Backlog` with 5 story points | Story stored in SQLite `user_stories` | 🟢 PASS |
| **TC-15** | `US-12` Scrum | Kanban workflow card transition & sprint progress | Story in `To Do`, Action item in `To Do` | transition status to `Done` | Status updated; Kanban groups story under `DONE` column | Story moved to `DONE`; velocity updated | 🟢 PASS |

---

## 4. Test Execution Summary

```text
======================================================================
TEST EXECUTION SUMMARY
======================================================================
Total Test Cases Executed : 15
Passing Tests             : 15
Failing Tests             : 0
Errors                    : 0
Success Rate              : 100.0%
Execution Duration        : ~0.08 seconds
Quality Gate Status       : ✅ PASSED (Ready for Viva & Production)
======================================================================
```
