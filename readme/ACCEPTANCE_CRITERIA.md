# Acceptance Criteria Documentation
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. What are Acceptance Criteria?

In Scrum and Agile software engineering, **Acceptance Criteria (AC)** are the formal, predetermined conditions that a software product or user story must satisfy to be accepted by the Product Owner, stakeholders, and end users.

### Purpose of Acceptance Criteria
1. **Defines Boundaries:** Clearly marks the scope of a user story, preventing scope creep.
2. **Establishes Consensus:** Aligns the Product Owner and Development Team on what "completed" means.
3. **Forms the Basis for Testing:** Translates directly into automated unit, integration, and user acceptance test cases.
4. **Supports the Definition of Done (DoD):** A user story cannot transition to `Done` until 100% of its acceptance criteria pass verification.

---

## 2. Reusable Template

Two standard formats are employed in Agile industry practice:

### A. Scenario-Oriented Format (Gherkin Syntax)
```gherkin
Scenario: [Title of scenario]
Given [Initial context / precondition]
When [Action triggered by the user or system]
Then [Expected outcome / postcondition]
And [Additional condition or consequence]
```

### B. Rule-Oriented Checklist Format
```markdown
- [ ] Requirement 1: [Specific system behavior]
- [ ] Requirement 2: [Validation / Edge case rule]
- [ ] Requirement 3: [Security / Error response]
```

---

## 3. Detailed Acceptance Criteria for Core User Stories

---

### AC-US01: User Registration
**Linked Story:** [US-01: User Registration](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-01-user-registration)

#### Scenario 1: Successful patient account registration
- **Given** an unregistered user accesses the registration interface,
- **When** the user provides a valid username (`rohan_s`), strong password (`Pass@123`), full name (`Rohan Sharma`), email (`rohan@example.com`), and phone (`9876543210`),
- **Then** the system hashes the password securely using SHA-256 with salt,
- **And** stores the new user record in the `users` database table with role `patient`,
- **And** displays a success message: `"Registration successful. You can now log in."`.

#### Scenario 2: Duplicate username or email rejection
- **Given** a user is on the registration interface,
- **When** the user attempts to register with a username or email that already exists in the `users` table,
- **Then** the database unique constraint prevents duplicate insertion,
- **And** the system catches the conflict and displays: `"Error: Username or Email already registered."`,
- **And** no duplicate database records are created.

#### Scenario 3: Missing mandatory fields
- **Given** a user is entering registration details,
- **When** any mandatory field (username, password, email, full name) is left blank or whitespace,
- **Then** the system rejects submission with: `"Error: All required fields must be provided."`.

---

### AC-US02: User Authentication & Login
**Linked Story:** [US-02: Secure Authentication & Login](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-02-secure-authentication--login)

#### Scenario 1: Successful login with valid credentials
- **Given** a registered user with active credentials exists in the database,
- **When** the user inputs their correct username and password,
- **Then** the system verifies the password hash against the stored hash,
- **And** creates an authenticated session containing `user_id`, `username`, and `role`,
- **And** routes the user to their role-specific dashboard with a personalized greeting.

#### Scenario 2: Login failure on invalid password
- **Given** a registered user exists in the system,
- **When** the user enters an incorrect password,
- **Then** the system rejects the authentication attempt,
- **And** displays: `"Invalid username or password."`,
- **And** no active session is created.

#### Scenario 3: Non-existent user login attempt
- **Given** a username that does not exist in the database,
- **When** credentials are submitted with that username,
- **Then** the system displays: `"Invalid username or password."`,
- **And** prevents user enumeration by not revealing whether the username exists.

---

### AC-US03: Search Doctors & Professionals
**Linked Story:** [US-03: Search Doctors by Specialization](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-03-search-doctors-by-specialization--department)

#### Scenario 1: Browse all medical specialists
- **Given** an authenticated user is on the Doctor Directory screen,
- **When** the user chooses to view all doctors without filters,
- **Then** the system retrieves and displays all registered professionals with their full name, medical department, specialization, consultation fee, and bio.

#### Scenario 2: Filter doctors by specialization keyword
- **Given** multiple doctors with various specialties (e.g., Cardiology, Neurology, Dermatology) exist,
- **When** the user searches with keyword `"cardio"`,
- **Then** the system performs a case-insensitive search and returns only doctors whose specialization or department matches `"Cardiology"`.

#### Scenario 3: Search with no matching results
- **Given** a user searches for an unavailable specialization (e.g., `"Pediatrics"`),
- **When** no records match the criteria,
- **Then** the system displays: `"No doctors found matching your query."`.

---

### AC-US04: View Doctor Availability & Slots
**Linked Story:** [US-04: View Doctor Availability & Real-Time Slots](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-04-view-doctor-availability--real-time-slots)

#### Scenario 1: Display open consultation slots
- **Given** a selected doctor has configured availability in the database,
- **When** the patient requests available slots for that doctor,
- **Then** the system queries the `availability` table filtering `professional_id = ?` AND `is_booked = 0`,
- **And** displays a chronological list of slots with Slot ID, Date, Start Time, and End Time.

#### Scenario 2: Doctor with zero open slots
- **Given** all slots for a doctor are marked `is_booked = 1` or no slots are configured,
- **When** the patient inspects that doctor's schedule,
- **Then** the system displays: `"No available slots found for this doctor."`.

---

### AC-US05: Book Appointment & Slot Lock
**Linked Story:** [US-05: Book Appointment & Slot Lock](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-05-book-appointment--slot-lock)

#### Scenario 1: Successful appointment booking
- **Given** an authenticated patient and an open slot (`is_booked = 0`),
- **When** the patient selects the slot and inputs consultation notes (e.g., `"Routine heart checkup"`),
- **Then** the system executes an atomic transaction that:
  1. Inserts a new row in `appointments` with `status = 'Confirmed'`.
  2. Updates `availability.is_booked = 1` for the chosen `slot_id`.
- **And** displays a confirmed receipt with unique Appointment ID, Doctor Name, Date, and Time.

#### Scenario 2: Double-booking prevention
- **Given** a slot has already been booked (`is_booked = 1`),
- **When** a user attempts to book the same slot,
- **Then** the system detects the booked status prior to insertion,
- **And** aborts the transaction,
- **And** raises an error: `"Error: Selected slot is already booked or invalid."`,
- **And** preserves database integrity without duplicate appointment records.

---

### AC-US06: View Appointment History
**Linked Story:** [US-06: View Appointment History & Active Bookings](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-06-view-appointment-history--active-bookings)

#### Scenario 1: Patient views their booking list
- **Given** a patient has scheduled, completed, and cancelled appointments in the database,
- **When** the patient views the `"My Appointments"` screen,
- **Then** the system displays all bookings associated with their `user_id`,
- **And** includes Booking ID, Doctor Name, Department, Date, Time, Status badge (`Confirmed`, `Cancelled`), and Notes.

#### Scenario 2: New patient with zero bookings
- **Given** a patient has never booked an appointment,
- **When** the patient navigates to `"My Appointments"`,
- **Then** the system displays: `"You have no appointments on record."`.

---

### AC-US07: Cancel Appointment & Slot Recovery
**Linked Story:** [US-07: Cancel Existing Appointment & Release Slot](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-07-cancel-existing-appointment--release-slot)

#### Scenario 1: Successful cancellation and slot release
- **Given** an authenticated patient has an active appointment (`status = 'Confirmed'`) linked to slot `S1`,
- **When** the patient confirms cancellation for this appointment,
- **Then** the system updates the appointment `status = 'Cancelled'`,
- **And** resets the linked slot `is_booked = 0` in the `availability` table,
- **And** displays confirmation: `"Appointment #X cancelled successfully. The slot has been released."`.

#### Scenario 2: Attempting to cancel an already cancelled appointment
- **Given** an appointment already marked `Cancelled`,
- **When** a user requests cancellation again,
- **Then** the system rejects the operation with: `"Error: Appointment is already cancelled."`.

#### Scenario 3: Unauthorized cancellation prevention
- **Given** an appointment belonging to Patient A,
- **When** Patient B attempts to cancel Patient A's appointment ID,
- **Then** the system blocks the request: `"Unauthorized: You can only manage your own appointments."`.

---

### AC-US08: Reschedule Appointment
**Linked Story:** [US-08: Reschedule Appointment to Alternative Slot](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-08-reschedule-appointment-to-alternative-slot)

#### Scenario 1: Successful rescheduling to a new slot
- **Given** an active appointment linked to slot `S1` (`is_booked = 1`),
- **When** the patient selects a new open slot `S2` (`is_booked = 0`) for the same doctor,
- **Then** the system performs an atomic swap:
  1. Releases old slot `S1`: sets `is_booked = 0`.
  2. Claims new slot `S2`: sets `is_booked = 1`.
  3. Updates appointment record with new `availability_id`, new date, and new time.
- **And** returns confirmation: `"Appointment rescheduled successfully to new date and time."`.

#### Scenario 2: Rescheduling to an unavailable slot
- **Given** a patient attempts to reschedule to slot `S3`,
- **When** slot `S3` is already marked `is_booked = 1`,
- **Then** the transaction aborts,
- **And** displays: `"Error: Selected new slot is not available."`,
- **And** the original appointment and slot `S1` remain completely unchanged.

---

### AC-US09: Booking Confirmation & Feedback
**Linked Story:** [US-09: Instant Confirmation & Feedback](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-09-instant-confirmation--feedback)

#### Scenario 1: Immediate confirmation summary
- **Given** any booking transaction finishes successfully,
- **When** the confirmation view is rendered,
- **Then** it clearly lists:
  - Booking Reference / Appointment ID
  - Doctor Name & Medical Department
  - Appointment Date & Start Time
  - Consultation Fee (INR)
  - Booking Status (`Confirmed`)
  - Patient Consultation Notes

---

### AC-US10: Manage Doctor Availability
**Linked Story:** [US-10: Doctor Schedule & Availability Management](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-10-doctor-schedule--availability-management)

#### Scenario 1: Doctor adds new consultation slot
- **Given** an authenticated doctor or admin,
- **When** they input Date (`YYYY-MM-DD`), Start Time (`HH:MM`), and End Time (`HH:MM`),
- **Then** the system validates date format and ensures start time precedes end time,
- **And** inserts the new row into the `availability` table with `is_booked = 0`,
- **And** displays: `"Availability slot added successfully."`.

---

### AC-US11: Admin Oversight
**Linked Story:** [US-11: Admin Appointment Oversight & Audit Log](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-11-admin-appointment-oversight--audit-log)

#### Scenario 1: Comprehensive system audit view
- **Given** a user logged in with `admin` privileges,
- **When** the admin selects the System Appointments view,
- **Then** the system returns all appointments across all patients and doctors, displaying patient name, doctor name, date, time, status, and creation timestamp.

---

### AC-US12: Agile Backlog, Sprint & Kanban Tracking
**Linked Story:** [US-12: Agile Backlog, Sprint & Kanban Management](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md#us-12-agile-backlog-sprint--kanban-management)

#### Scenario 1: Interactive Kanban board rendering
- **Given** user stories and action items stored in the SQLite database,
- **When** a user requests the Kanban board view,
- **Then** the system categorizes tasks into 5 columns: `BACKLOG`, `TODO`, `IN PROGRESS`, `REVIEW/TESTING`, and `DONE`,
- **And** displays visual cards with ID, Title, Story Points, Priority badge (🔴, 🟠, 🟢), and Assignee.

#### Scenario 2: Transitioning task across Kanban workflow
- **Given** a user story currently in `To Do`,
- **When** the developer changes its status to `In Progress`,
- **Then** the database updates `user_stories.status = 'In Progress'`,
- **And** the task immediately shifts into the `IN PROGRESS` column on subsequent Kanban board renders.

#### Scenario 3: Sprint velocity & progress calculation
- **Given** a sprint with committed user stories,
- **When** sprint progress is inspected,
- **Then** the system computes:
  - Total committed story points
  - Completed story points (stories in `Done` status)
  - Completion percentage = `(Completed Points / Total Points) * 100`.

---

## 4. Definition of Ready (DoR) and Definition of Done (DoD)

### Definition of Ready (DoR)
A user story is ready to enter a Sprint Backlog when:
- [x] Clear title and description following standard format (`As a... I want... So that...`).
- [x] Specific, testable Acceptance Criteria written in Given-When-Then format.
- [x] Story points estimated by the team via Planning Poker.
- [x] Dependencies identified and resolved.
- [x] MoSCoW priority assigned.

### Definition of Done (DoD)
A user story is marked `Done` when:
- [x] Code is implemented satisfying 100% of defined Acceptance Criteria.
- [x] Unit tests pass with 0 failures in `tests/test_appointment.py`.
- [x] Peer code review conducted without blockers.
- [x] Database migrations and integrity verified with foreign keys enabled.
- [x] Demonstrated and accepted during Sprint Review.
- [x] No regression bugs introduced.
