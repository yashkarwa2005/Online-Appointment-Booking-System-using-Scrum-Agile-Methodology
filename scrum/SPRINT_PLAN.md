# Sprint Plan (5-Week Scrum Iteration Schedule)
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Scrum Sprint Cadence & Team Roles

The project was executed over **5 weekly Sprints** (7 calendar days per sprint iteration).

### Scrum Team Roles & Responsibilities
- **Product Owner:** Defines the product vision, maintains and prioritizes the Product Backlog, and accepts completed increments based on Acceptance Criteria.
- **Scrum Master:** Facilitates daily scrums, sprint planning, reviews, and retrospectives; eliminates roadblocks; ensures adherence to Scrum best practices.
- **Development Team (Led by Yash Karwa):** Multi-disciplinary developers responsible for schema design, business logic, CLI interface, and automated test suites.

---

## 2. Weekly Sprint Breakdown

---

### 🏃 SPRINT 1 (Week 1)
**Theme:** User Authentication, Profile Management & Core Infrastructure

- **Sprint Goal:** Establish the SQLite database architecture and deliver a secure, testable user registration and session authentication system.
- **Sprint Duration:** Week 1
- **Committed Story Points:** 6 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 1:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-01` | User Registration & Credential Hashing | 🔴 Must Have | 3 | Yash Karwa |
| `US-02` | User Authentication & Session Management | 🔴 Must Have | 3 | Dev Team |

#### Sprint 1 Task Breakdown:
1. Initialize project structure, `.gitignore`, and Git repository. (Owner: Yash Karwa, Est: 2h)
2. Design and implement `src/database.py` with `users` table and foreign key support. (Owner: Dev Team, Est: 3h)
3. Implement password hashing using SHA-256 with salt. (Owner: Yash Karwa, Est: 2h)
4. Implement `register_user` and `login_user` methods in `src/appointment.py`. (Owner: Dev Team, Est: 3h)
5. Write unit test cases `TC-01`, `TC-02`, `TC-03`, `TC-04` in `tests/test_appointment.py`. (Owner: Yash Karwa, Est: 2h)

- **Expected Increment:** Working authentication engine where users can register with unique usernames/emails, passwords are encrypted, and logins return valid user sessions.
- **Actual Increment Delivered:** 100% completed, zero defects.

---

### 🏃 SPRINT 2 (Week 2)
**Theme:** Doctor Profiles, Directory Search & Availability Management

- **Sprint Goal:** Enable doctors to publish consultation schedules and provide patients with a searchable directory of medical specialists.
- **Sprint Duration:** Week 2
- **Committed Story Points:** 13 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 2:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-03` | Search & Filter Doctors by Specialization | 🔴 Must Have | 5 | Dev Team |
| `US-04` | Real-time Doctor Availability & Time Slot Query | 🔴 Must Have | 3 | Dev Team |
| `US-10` | Doctor Schedule & Availability Slot Management | 🔴 Must Have | 5 | Yash Karwa |

#### Sprint 2 Task Breakdown:
1. Create `professionals` and `availability` schema in `src/database.py`. (Owner: Dev Team, Est: 2h)
2. Implement doctor directory listing with filter by name, department, or specialization. (Owner: Dev Team, Est: 3h)
3. Implement `get_available_slots(doctor_id)` with date sorting. (Owner: Yash Karwa, Est: 3h)
4. Build `add_availability_slot` allowing physicians to publish consultation windows. (Owner: Yash Karwa, Est: 3h)
5. Seed initial realistic doctor data across Cardiology, Neurology, Dermatology. (Owner: Dev Team, Est: 2h)
6. Add unit test coverage for doctor discovery and slot queries (`TC-05`, `TC-06`, `TC-12`). (Owner: Yash Karwa, Est: 2h)

- **Expected Increment:** A searchable physician catalog and availability query system showing only unbooked slots.
- **Actual Increment Delivered:** Full physician discovery operational with robust date/time slot listing.

---

### 🏃 SPRINT 3 (Week 3)
**Theme:** Core Appointment Booking Engine & Double-Booking Prevention

- **Sprint Goal:** Implement an atomic booking pipeline that guarantees reservation integrity, eliminates double-booking race conditions, and tracks booking history.
- **Sprint Duration:** Week 3
- **Committed Story Points:** 11 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 3:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-05` | Atomic Appointment Booking & Double-Booking Lock | 🔴 Must Have | 8 | Yash Karwa |
| `US-06` | Patient Appointment History & Status Overview | 🟠 Should Have | 3 | Dev Team |

#### Sprint 3 Task Breakdown:
1. Create `appointments` table with foreign keys referencing `users`, `professionals`, and `availability`. (Owner: Dev Team, Est: 2h)
2. Implement atomic SQL transaction: verify `is_booked = 0`, update `is_booked = 1`, and insert into `appointments`. (Owner: Yash Karwa, Est: 5h)
3. Handle error states and rollbacks when conflicting bookings collide. (Owner: Yash Karwa, Est: 3h)
4. Implement `get_user_appointments(user_id)` to list upcoming and past bookings. (Owner: Dev Team, Est: 2h)
5. Add unit tests `TC-07`, `TC-08`, `TC-09` verifying booking success, double-booking rejection, and history. (Owner: Yash Karwa, Est: 3h)

- **Expected Increment:** End-to-end appointment booking system where slots are immediately locked upon reservation.
- **Actual Increment Delivered:** 100% achieved; double-booking rigorously defended by database integrity checks.

---

### 🏃 SPRINT 4 (Week 4)
**Theme:** Appointment Cancellation, Rescheduling & Slot Lifecycle

- **Sprint Goal:** Allow patients to cancel appointments with automatic slot release and reschedule to alternative dates without data duplication.
- **Sprint Duration:** Week 4
- **Committed Story Points:** 10 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 4:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-07` | Cancel Appointment & Atomically Release Slot | 🔴 Must Have | 5 | Dev Team |
| `US-08` | Reschedule Booking to Alternative Open Slot | 🟠 Should Have | 5 | Yash Karwa |

#### Sprint 4 Task Breakdown:
1. Implement `cancel_appointment`: update status to `Cancelled` and reset slot `is_booked = 0`. (Owner: Dev Team, Est: 3h)
2. Prevent cancelling already cancelled appointments or appointments belonging to other users. (Owner: Dev Team, Est: 2h)
3. Implement `reschedule_appointment`: atomic slot swap (release old slot, lock new slot, update record). (Owner: Yash Karwa, Est: 4h)
4. Validate edge cases where the target rescheduling slot is unavailable. (Owner: Yash Karwa, Est: 2h)
5. Add automated unit tests `TC-10` and `TC-11`. (Owner: Dev Team, Est: 2h)

- **Expected Increment:** Complete appointment lifecycle management with zero stranded or orphaned slots.
- **Actual Increment Delivered:** Rescheduling and cancellation both verified with full slot reuse.

---

### 🏃 SPRINT 5 (Week 5)
**Theme:** In-App Scrum & Kanban Engine, Operational Auditing, Integration & Viva Prep

- **Sprint Goal:** Integrate the built-in Agile/Scrum project management system, terminal Kanban board, administrative oversight, end-to-end testing, and documentation.
- **Sprint Duration:** Week 5
- **Committed Story Points:** 14 Points
- **Sprint Status:** 🟢 Completed

#### User Stories in Sprint 5:
| Story ID | Story Title | Priority | Story Points | Assignee |
|---|---|---|---|---|
| `US-09` | Real-time Transaction Confirmation Receipts | 🟠 Should Have | 3 | Dev Team |
| `US-11` | Hospital Administrative Audit Log & Monitoring | 🟢 Could Have | 3 | Dev Team |
| `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine | 🔴 Must Have | 8 | Yash Karwa |

#### Sprint 5 Task Breakdown:
1. Create `sprints`, `user_stories`, and `action_items` tables in `src/database.py`. (Owner: Dev Team, Est: 3h)
2. Implement `UserStoryService`, `SprintService`, and `ActionItemService`. (Owner: Yash Karwa, Est: 4h)
3. Implement `KanbanService` rendering 5 columns with color coding. (Owner: Yash Karwa, Est: 4h)
4. Implement unified interactive CLI menu and instant automated `--demo` runner. (Owner: Yash Karwa, Est: 4h)
5. Execute end-to-end regression testing and generate test report in `docs/TESTING.md`. (Owner: Dev Team, Est: 3h)
6. Prepare final Scrum documentation, Review, and Retrospective artifacts. (Owner: Dev Team, Est: 3h)

- **Expected Increment:** Complete, polished, and demonstrable dual-track application (Appointment System + Scrum Management Engine) ready for B.Tech 3rd-year viva demonstration.
- **Actual Increment Delivered:** Fully delivered, verified with 15 passing automated test cases and zero dependencies.

---

## 3. Sprint Velocity Summary

| Sprint | Goal | Committed Pts | Completed Pts | Velocity |
|---|---|---|---|---|
| **Sprint 1** | Auth & Architecture | 6 | 6 | 6 pts |
| **Sprint 2** | Directory & Schedules | 13 | 13 | 13 pts |
| **Sprint 3** | Booking & Concurrency | 11 | 11 | 11 pts |
| **Sprint 4** | Cancel & Reschedule | 10 | 10 | 10 pts |
| **Sprint 5** | Scrum Engine & Testing | 14 | 14 | 14 pts |
| **TOTAL** | **Entire System** | **54** | **54** | **10.8 pts/wk (Avg)** |
