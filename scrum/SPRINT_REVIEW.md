# Sprint Review Reports
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Purpose of the Sprint Review

The **Sprint Review** is held at the conclusion of each sprint to inspect the shippable increment delivered by the Scrum Team, demonstrate working software to stakeholders and the Product Owner, and adapt the Product Backlog if necessary.

---

## 2. Sprint 1 Review Report

- **Date:** Week 1, Day 7
- **Sprint Goal:** Establish SQLite database architecture and deliver secure user registration and session authentication.
- **Attendees:** Product Owner, Scrum Master, Development Team (Yash Karwa)
- **Demo Agenda:**
  1. Demonstration of user account registration with unique validation.
  2. Demonstration of password hashing using SHA-256 + salt.
  3. Demonstration of user login with role session assignment (`patient`, `doctor`, `admin`).
- **User Stories Evaluated:**
  - `US-01` (User Registration): Accepted ✅ — Meets all acceptance criteria.
  - `US-02` (Authentication & Login): Accepted ✅ — Invalid passwords cleanly rejected.
- **Velocity Metrics:**
  - Committed Points: 6 pts | Completed Points: 6 pts | Completion: 100%
- **Stakeholder Feedback:** The authentication engine was praised for security. Recommendation made to ensure clear error messages when duplicate usernames are entered.

---

## 3. Sprint 2 Review Report

- **Date:** Week 2, Day 7
- **Sprint Goal:** Enable doctors to publish consultation schedules and provide patients with a searchable directory of medical specialists.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Demonstration of adding consultation slots for doctors.
  2. Demonstration of specialist search (Cardiology, Neurology, Dermatology).
  3. Demonstration of querying available slots filtering out booked ones.
- **User Stories Evaluated:**
  - `US-03` (Search Doctors): Accepted ✅
  - `US-04` (View Availability): Accepted ✅
  - `US-10` (Doctor Availability Management): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 13 pts | Completed Points: 13 pts | Completion: 100%
- **Stakeholder Feedback:** Stakeholders requested displaying the consultation fee and bio prominently when searching for doctors. Incorporated into UI output.

---

## 4. Sprint 3 Review Report

- **Date:** Week 3, Day 7
- **Sprint Goal:** Implement an atomic booking pipeline that guarantees reservation integrity, eliminates double-booking race conditions, and tracks booking history.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Live walkthrough booking an open doctor slot.
  2. Stress test simulating two concurrent booking requests on the same slot (preventing race condition).
  3. Viewing updated patient appointment history.
- **User Stories Evaluated:**
  - `US-05` (Atomic Appointment Booking): Accepted ✅ — Double-booking lock verified.
  - `US-06` (Appointment History): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 11 pts | Completed Points: 11 pts | Completion: 100%
- **Stakeholder Feedback:** Transaction safety was confirmed. Product Owner requested clear cancellation workflows for the next sprint.

---

## 5. Sprint 4 Review Report

- **Date:** Week 4, Day 7
- **Sprint Goal:** Allow patients to cancel appointments with automatic slot release and reschedule to alternative dates without data duplication.
- **Attendees:** Product Owner, Scrum Master, Development Team
- **Demo Agenda:**
  1. Cancelling an existing booking; verifying that `availability.is_booked` flips from 1 back to 0.
  2. Rescheduling an appointment to a newly selected slot; verifying old slot is released and new slot is reserved.
- **User Stories Evaluated:**
  - `US-07` (Cancellation & Slot Recovery): Accepted ✅
  - `US-08` (Reschedule Appointment): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 10 pts | Completed Points: 10 pts | Completion: 100%
- **Stakeholder Feedback:** Very smooth workflow. Ensured unauthorized users cannot cancel other patients' appointments.

---

## 6. Sprint 5 Review Report (Final Release)

- **Date:** Week 5, Day 7
- **Sprint Goal:** Integrate the built-in Agile/Scrum project management system, terminal Kanban board, administrative oversight, end-to-end testing, and documentation.
- **Attendees:** Product Owner, Scrum Master, Development Team, Academic Evaluators
- **Demo Agenda:**
  1. Interactive terminal Kanban board rendering real-time SQLite user stories.
  2. Moving tasks between Kanban stages (`To Do` -> `In Progress` -> `Done`).
  3. Running the automated `--demo` flag showing the full system flow in 30 seconds.
  4. Executing automated test suite: 15 passing test cases.
- **User Stories Evaluated:**
  - `US-09` (Confirmation Receipts): Accepted ✅
  - `US-11` (Admin Oversight): Accepted ✅
  - `US-12` (In-App Scrum & Kanban Engine): Accepted ✅
- **Velocity Metrics:**
  - Committed Points: 14 pts | Completed Points: 14 pts | Completion: 100%
- **Final Product Owner Verdict:** Release 1.0 formally **APPROVED** for academic viva demonstration.
