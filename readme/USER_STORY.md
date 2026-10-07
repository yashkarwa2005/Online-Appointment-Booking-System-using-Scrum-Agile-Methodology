# User Story Documentation
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. What is a User Story?

In Agile and Scrum methodologies, a **User Story** is an informal, general explanation of a software feature written from the perspective of the end user or customer. Its primary purpose is to articulate how a software feature will deliver value to the user.

### Standard Agile Format
> **As a** `<type of user>`,  
> **I want** `<some goal / functionality>`,  
> **So that** `<some reason / benefit / value>`.

### The 3 C's of User Stories
1. **Card**: Written description of the story, serving as an invitation to conversation.
2. **Conversation**: Ongoing discussions between the Product Owner, Scrum Master, and Developers to clarify details.
3. **Confirmation**: Acceptance criteria that confirm the story has been implemented correctly and meets the Definition of Done (DoD).

### INVEST Criteria
All user stories in this project adhere to the **INVEST** principle:
- **I**ndependent: Minimal overlap and dependency on other stories.
- **N**egotiable: Open to discussion and refinement during backlog grooming.
- **V**aluable: Delivers clear, tangible value to patients, professionals, or administrators.
- **E**stimable: Sized realistically using story points (Fibonacci scale: 1, 2, 3, 5, 8).
- **S**mall: Scoped to be completed within a single 1-week sprint iteration.
- **T**estable: Accompanied by verifiable Acceptance Criteria ([ACCEPTANCE_CRITERIA.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md)).

---

## 2. User Roles & Personas

| Role | Persona Name | Description & Context |
|---|---|---|
| **Patient / Client** | Rohan Sharma | Needs a convenient, 24/7 self-service platform to find qualified doctors, check verified consultation slots, and book/reschedule appointments without waiting in phone queues. |
| **Medical Professional / Doctor** | Dr. Priya Verma | Specialist physician seeking an automated schedule manager to publish consultation availability, view daily appointments, and reduce patient no-shows. |
| **System Administrator** | Vikram Patel | Hospital IT administrator monitoring system integrity, auditing appointment records, overseeing user accounts, and generating operational reports. |
| **Scrum Development Team** | Agile Team Alpha | Product Owner, Scrum Master, and Engineers using built-in Scrum tooling to manage sprints, backlogs, and Kanban workflows. |

---

## 3. User Story Inventory & Backlog Mapping

The following table summarizes the complete set of User Stories mapped directly to the Product Backlog, Sprints, and MoSCoW priorities:

| Story ID | Story Title | Role | Priority | Story Points | Sprint | Status | Assignee |
|---|---|---|---|---|---|---|---|
| **US-01** | User Registration | Patient / Client | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Yash Karwa |
| **US-02** | Secure Authentication & Login | All Roles | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done | Dev Team |
| **US-03** | Search Doctors by Specialization | Patient / Client | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-04** | View Doctor Availability & Slots | Patient / Client | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done | Dev Team |
| **US-05** | Book Appointment & Slot Lock | Patient / Client | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done | Yash Karwa |
| **US-06** | View Appointment History & Active Bookings | Patient / Client | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done | Dev Team |
| **US-07** | Cancel Existing Appointment & Release Slot | Patient / Client | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done | Dev Team |
| **US-08** | Reschedule Appointment to Alternative Slot | Patient / Client | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done | Yash Karwa |
| **US-09** | Instant Booking & Cancellation Confirmation | Patient / Client | 🟠 Should Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-10** | Doctor Schedule & Availability Management | Doctor / Professional | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done | Dev Team |
| **US-11** | Admin Appointment Oversight & Audit Log | Administrator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done | Dev Team |
| **US-12** | Agile Backlog, Sprint & Kanban Management | Scrum Team / PO | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done | Yash Karwa |

---

## 4. Detailed User Story Specifications

### US-01: User Registration
- **Story ID:** `US-01`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** new patient,  
  > **I want** to register an account using my unique username, email, phone number, and password,  
  > **So that** I can access the appointment booking platform securely and manage my consultations.
- **Priority:** 🔴 Must Have (MoSCoW)
- **Story Points:** 3 (Fibonacci)
- **Sprint:** Sprint 1 (Week 1)
- **Status:** 🟢 Done
- **Assignee:** Yash Karwa
- **Description:** The system must provide a registration form validating unique usernames and emails, enforcing secure password hashing (SHA-256 with salt), and saving user profile details to the SQLite `users` table. Duplicate credentials must be gracefully rejected with user-friendly error messages.

---

### US-02: Secure Authentication & Login
- **Story ID:** `US-02`
- **User Role:** All Roles (Patient, Doctor, Admin)
- **User Story:**
  > **As a** registered user,  
  > **I want** to log in using my credentials,  
  > **So that** the system authenticates my identity and loads my role-specific dashboard and actions.
- **Priority:** 🔴 Must Have
- **Story Points:** 3
- **Sprint:** Sprint 1 (Week 1)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Validates user credentials against stored password hashes. On successful authentication, creates an active user session maintaining user ID, username, and role throughout session operations. Failed login attempts return clear feedback without exposing internal error details.

---

### US-03: Search Doctors by Specialization & Department
- **Story ID:** `US-03`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient seeking medical consultation,  
  > **I want** to browse and filter doctors by specialization, department, and consultation fee,  
  > **So that** I can easily select the most appropriate healthcare specialist for my health concern.
- **Priority:** 🔴 Must Have
- **Story Points:** 5
- **Sprint:** Sprint 2 (Week 2)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Queries the `professionals` joined with `users` table to display verified doctor profiles including full name, medical department, specialization (e.g., Cardiology, Neurology, Dermatology, General Medicine), fee structure, and bio. Allows case-insensitive search queries.

---

### US-04: View Doctor Availability & Real-Time Slots
- **Story ID:** `US-04`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient,  
  > **I want** to view all unbooked time slots for a specific doctor on upcoming dates,  
  > **So that** I can pick a consultation time that fits my personal daily schedule.
- **Priority:** 🔴 Must Have
- **Story Points:** 3
- **Sprint:** Sprint 2 (Week 2)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Fetches entries from the `availability` table where `is_booked = 0` for the selected doctor. Displays formatted date (YYYY-MM-DD), start time (HH:MM), and end time (HH:MM). Slots already booked by other patients are filtered out to prevent scheduling confusion.

---

### US-05: Book Appointment & Slot Lock
- **Story ID:** `US-05`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** logged-in patient,  
  > **I want** to select an open slot, enter consultation notes, and confirm my booking,  
  > **So that** the slot is immediately reserved for me and cannot be double-booked by anyone else.
- **Priority:** 🔴 Must Have
- **Story Points:** 8
- **Sprint:** Sprint 3 (Week 3)
- **Status:** 🟢 Done
- **Assignee:** Yash Karwa
- **Description:** Executes an atomic database transaction that creates a record in the `appointments` table with status `Confirmed` and immediately marks `is_booked = 1` in the `availability` table. If the slot was booked concurrently, the transaction rolls back and alerts the patient. Generates a unique appointment booking reference.

---

### US-06: View Appointment History & Active Bookings
- **Story ID:** `US-06`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient,  
  > **I want** to view a comprehensive list of all my upcoming and past appointments,  
  > **So that** I can keep track of my scheduled visits, doctor details, and consultation status.
- **Priority:** 🟠 Should Have
- **Story Points:** 3
- **Sprint:** Sprint 3 (Week 3)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Retrieves all appointment records associated with the logged-in user's ID, showing doctor name, specialization, date, time slot, current status (`Confirmed`, `Cancelled`, `Completed`), and notes in a clear tabular format.

---

### US-07: Cancel Existing Appointment & Release Slot
- **Story ID:** `US-07`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient who can no longer attend an appointment,  
  > **I want** to cancel my scheduled booking,  
  > **So that** the doctor is notified and the reserved slot is freed up for other patients in need.
- **Priority:** 🔴 Must Have
- **Story Points:** 5
- **Sprint:** Sprint 4 (Week 4)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Allows patients to cancel active appointments. Updates the appointment record's status to `Cancelled` and atomically toggles the corresponding `availability` slot `is_booked = 0`. Ensures patients can only cancel their own appointments and cannot cancel already-cancelled bookings.

---

### US-08: Reschedule Appointment to Alternative Slot
- **Story ID:** `US-08`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient with a schedule conflict,  
  > **I want** to reschedule an existing appointment to a newly selected open slot,  
  > **So that** I do not lose my consultation booking without having to cancel and start from scratch.
- **Priority:** 🟠 Should Have
- **Story Points:** 5
- **Sprint:** Sprint 4 (Week 4)
- **Status:** 🟢 Done
- **Assignee:** Yash Karwa
- **Description:** Implements a two-step transactional swap: releases the currently held slot (`is_booked = 0`), claims the newly chosen available slot (`is_booked = 1`), and updates the appointment's date, time, and `availability_id` while keeping the original booking identifier intact.

---

### US-09: Instant Confirmation & Feedback
- **Story ID:** `US-09`
- **User Role:** Patient / Client
- **User Story:**
  > **As a** patient performing booking or cancellation actions,  
  > **I want** to receive immediate visual confirmation with complete booking details,  
  > **So that** I have reassurance that my request was successfully recorded by the system.
- **Priority:** 🟠 Should Have
- **Story Points:** 3
- **Sprint:** Sprint 5 (Week 5)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Generates formatted confirmation receipts in the user interface showing Appointment ID, Doctor Name, Date, Time, Fee, and Status upon any booking, rescheduling, or cancellation action.

---

### US-10: Doctor Schedule & Availability Management
- **Story ID:** `US-10`
- **User Role:** Doctor / Professional
- **User Story:**
  > **As a** healthcare professional,  
  > **I want** to define and publish new consultation time slots for upcoming dates,  
  > **So that** patients can view my availability and book appointments according to my hospital schedule.
- **Priority:** 🔴 Must Have
- **Story Points:** 5
- **Sprint:** Sprint 2 (Week 2)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Enables medical professionals to add consultation time windows (e.g., 2026-10-15 09:00 - 09:30). Validates date formats and start/end time consistency before storing new records into the `availability` table.

---

### US-11: Admin Appointment Oversight & Audit Log
- **Story ID:** `US-11`
- **User Role:** System Administrator
- **User Story:**
  > **As a** hospital administrator,  
  > **I want** to view all appointments across all doctors, departments, and patients,  
  > **So that** I can monitor clinic utilization, resolve booking disputes, and ensure clinical compliance.
- **Priority:** 🟢 Could Have
- **Story Points:** 3
- **Sprint:** Sprint 5 (Week 5)
- **Status:** 🟢 Done
- **Assignee:** Dev Team
- **Description:** Provides an administrative overview module listing all system bookings with cross-filtering by date range, doctor, or status, supporting operational reporting and audit compliance.

---

### US-12: Agile Backlog, Sprint & Kanban Management
- **Story ID:** `US-12`
- **User Role:** Scrum Master / Product Owner / Team
- **User Story:**
  > **As a** Scrum team member,  
  > **I want** to track user stories, manage sprint lifecycles, and visualize tasks on an interactive Kanban board within the software,  
  > **So that** our team practices transparent, iterative Agile software engineering and monitors project progress continuously.
- **Priority:** 🔴 Must Have
- **Story Points:** 8
- **Sprint:** Sprint 5 (Week 5)
- **Status:** 🟢 Done
- **Assignee:** Yash Karwa
- **Description:** Implements dedicated Scrum project management commands and data tables inside the application (`user_stories`, `sprints`, `action_items`). Allows creating/updating stories, assigning story points, linking to sprints, moving items across Kanban columns (`Backlog`, `To Do`, `In Progress`, `Review/Testing`, `Done`), and rendering an ASCII terminal Kanban board for daily standups and sprint reviews.

---

## 5. Traceability Matrix

| User Story | Database Tables Involved | Acceptance Criteria Link | Test Case ID |
|---|---|---|---|
| **US-01** | `users` | [AC-US01](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us01-user-registration) | `TC-01`, `TC-02` |
| **US-02** | `users` | [AC-US02](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us02-user-authentication--login) | `TC-03`, `TC-04` |
| **US-03** | `professionals`, `users` | [AC-US03](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us03-search-doctors--professionals) | `TC-05` |
| **US-04** | `availability`, `professionals` | [AC-US04](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us04-view-doctor-availability--slots) | `TC-06` |
| **US-05** | `appointments`, `availability` | [AC-US05](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us05-book-appointment--slot-lock) | `TC-07`, `TC-08` |
| **US-06** | `appointments`, `professionals` | [AC-US06](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us06-view-appointment-history) | `TC-09` |
| **US-07** | `appointments`, `availability` | [AC-US07](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us07-cancel-appointment--slot-recovery) | `TC-10` |
| **US-08** | `appointments`, `availability` | [AC-US08](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us08-reschedule-appointment) | `TC-11` |
| **US-09** | `appointments` | [AC-US09](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us09-booking-confirmation--feedback) | `TC-07` |
| **US-10** | `availability`, `professionals` | [AC-US10](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us10-manage-doctor-availability) | `TC-12` |
| **US-11** | `appointments`, `users` | [AC-US11](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us11-admin-oversight) | `TC-13` |
| **US-12** | `user_stories`, `sprints`, `action_items` | [AC-US12](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md#ac-us12-agile-backlog-sprint--kanban-tracking) | `TC-14`, `TC-15` |
