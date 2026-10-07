# Online Appointment Booking System using Scrum Agile Methodology

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)](https://www.sqlite.org/)
[![Agile Methodology](https://img.shields.io/badge/Methodology-Scrum%20%2F%20Kanban-success.svg)](https://www.scrum.org/)
[![Tests](https://img.shields.io/badge/Unit%20Tests-15%20Passed%20(100%25)-brightgreen.svg)](tests/test_appointment.py)
[![License](https://img.shields.io/badge/License-Academic%20PBL-orange.svg)](#)

> **B.Tech 3rd-Year Project-Based Learning (PBL) Submission**  
> **Course:** Agile Methodologies & IT (AM)  
> **Author / Scrum Lead:** Yash Karwa  
> **Repository:** [Online-Appointment-Booking-System-using-Scrum-Agile-Methodology](https://github.com/yashkarwa2005/Online-Appointment-Booking-System-using-Scrum-Agile-Methodology.git)

---

## 1. Project Overview

The **Online Appointment Booking System** is an end-to-end, domain-driven software solution engineered to streamline outpatient medical scheduling, eliminate double-booking concurrency conflicts, and deliver transparent calendar availability for both patients and healthcare specialists.

More importantly, the entire development lifecycle serves as a practical demonstration of **Scrum Agile Methodology**. To satisfy the B.Tech Agile Methodologies curriculum, the delivered codebase features a **dual-track architecture**:
1. **Clinical Appointment Engine:** User authentication, directory search, slot inspection, atomic reservation, cancellation, and rescheduling.
2. **Built-in Scrum & Kanban Management Engine:** Persistent SQLite tables for user stories, sprint lifecycles, action items, and a real-time ASCII terminal Kanban board.

---

## 2. Problem Statement

Traditional hospital appointment workflows suffer from three critical bottlenecks:
- **Phone Queue Frustration & Miscommunication:** Patients face long wait times to check doctor schedules.
- **Double-Booking & Schedule Collisions:** Lack of transactional concurrency locks results in multiple patients being assigned to the same time slot.
- **Stranded Capacity on Cancellations:** When patients cancel consultations late, open slots remain orphaned rather than immediately recycling into available inventory.

From a software engineering perspective, projects often fail due to monolithic waterfall planning, poor visibility into progress, and scope creep. This project solves both the healthcare domain problem and the software project management problem through disciplined Scrum iterations.

---

## 3. Project Objectives

- **Zero Concurrency Collisions:** Enforce atomic database transactions to guarantee that no doctor consultation slot is double-booked.
- **Full Lifecycle Management:** Enable self-service registration, doctor search, booking, cancellation with automatic slot recycling, and single-step rescheduling.
- **Authentic Scrum Execution:** Practice all Scrum roles, ceremonies, artifacts, INVEST-compliant user stories, and Gherkin-formatted acceptance criteria.
- **In-App Agile Tooling:** Integrate real-time Kanban visualization and backlog metrics directly inside the Python console.
- **Zero Third-Party Hurdles:** Implement using pure Python standard libraries (`sqlite3`, `hashlib`, `unittest`) to run out-of-the-box on any evaluation machine.

For detailed curriculum mapping and academic objectives, see [docs/PROJECT_OBJECTIVES.md](docs/PROJECT_OBJECTIVES.md).

---

## 4. Key Features

### 🏥 Healthcare Appointment Subsystem
- **Salted SHA-256 Authentication:** Secure registration and login for patients, doctors, and hospital administrators.
- **Specialist Directory Search:** Case-insensitive search across doctors, departments (Cardiology, Neurology, Dermatology), and fee structures.
- **Dynamic Slot Availability:** Real-time query of unbooked consultation windows.
- **Atomic Booking Engine:** Immediate slot reservation with unique appointment reference generation.
- **Defensive Double-Booking Prevention:** Concurrency checks rejecting conflicting reservation attempts.
- **Self-Service Rescheduling:** Atomic slot swap (releases previous slot and locks new slot in a single transaction).
- **Cancellation & Slot Recovery:** Automatically unlocks cancelled slots (`is_booked = 0`) for subsequent patient use.
- **Administrative Audit Log:** Global appointment oversight for clinic administrators.

### 📋 Scrum Project Management Subsystem
- **Interactive Terminal Kanban Board:** 5-column ASCII board (`Backlog -> To Do -> In Progress -> Review/Testing -> Done`) with task cards, story points, and priority badges.
- **Product Backlog Management:** Full tracking of user stories with MoSCoW prioritization and estimation.
- **5-Week Sprint Cadence:** Sprint goal tracking, committed vs completed points, and velocity calculations.
- **Action Item Register:** Weekly impediment and task tracking with ownership and statuses.
- **Instant Automated Viva Demo (`--demo`):** Automated walkthrough executing the entire system in under 30 seconds.

---

## 5. Technology Stack

| Component | Technology | Rationale |
|---|---|---|
| **Programming Language** | Python 3.8+ (Tested on 3.13) | Clean, readable syntax; standard in enterprise and academia. |
| **Persistence / Database** | SQLite 3 (`sqlite3`) | Zero-configuration relational database with ACID compliance and foreign key enforcement. |
| **Cryptography** | `hashlib` (SHA-256 + Salt) | Secure password storage defending against rainbow tables. |
| **Testing Framework** | `unittest` | Built-in unit and integration test runner requiring zero pip packages. |
| **Version Control** | Git & GitHub | Distributed version control, milestone planning, and release tracking. |
| **User Interface** | ANSI Terminal Console | Portable, lightweight, cross-platform CLI with color badge support. |

---

## 6. Scrum Methodology Implementation

The project strictly follows the Scrum Framework as defined in the Scrum Guide:

```text
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SCRUM METHODOLOGY CADENCE                             │
└─────────────────────────────────────────────────────────────────────────────────┘
  Product Vision ──► Product Backlog (Refined & Estimated via Planning Poker)
                            │
                            ▼
                     Sprint Planning (Commitment & Goal Definition)
                            │
                            ▼
               Sprint Execution (Weekly Sprints 1 to 5)
                 ├── Daily Scrum & Impediment Removal
                 └── Kanban Flow (WIP Limits, Column Progression)
                            │
                            ▼
               Sprint Review (Live Demo & Acceptance Criteria Verification)
                            │
                            ▼
               Sprint Retrospective (Continuous Improvement / Action Items)
                            │
                            ▼
                Shippable Product Increment (Definition of Done)
```

---

## 7. Scrum Team Roles

- **Product Owner:** Responsible for maximizing product value, writing user stories, maintaining the Product Backlog, and accepting deliverables based on defined Acceptance Criteria.
- **Scrum Master:** Facilitates daily scrums, sprint planning, reviews, and retrospectives; eliminates team impediments and enforces Agile best practices.
- **Development Team (Led by Yash Karwa):** Cross-functional team responsible for database architecture, business logic implementation, CLI design, and test suite automation.

---

## 8. Requirement Priorities (MoSCoW)

Requirements are prioritized using the MoSCoW framework:
- 🔴 **MUST HAVE (32 Points):** Authentication, Doctor Directory, Availability Query, Atomic Booking, Concurrency Guard, Cancellation, Slot Management.
- 🟠 **SHOULD HAVE (16 Points):** Booking History, Rescheduling, Confirmation Receipts, In-App Scrum & Kanban Engine.
- 🟢 **COULD HAVE (8 Points):** Admin Audit View, Fee Filters, Terminal Color Badges.
- ⚪ **WON'T HAVE (Deferred):** Online Stripe/Razorpay Payment Gateway, WebRTC Video Calling, Automated SMS Gateway.

👉 Full MoSCoW breakdown and point distribution: [scrum/REQUIREMENT_PRIORITIES.md](scrum/REQUIREMENT_PRIORITIES.md)

---

## 9. 5-Week Sprint Overview

The project was executed across five structured 1-week sprint iterations:

| Sprint | Theme / Milestone | Committed | Completed | Velocity | Status |
|---|---|---|---|---|---|
| **Sprint 1** | User Authentication, Profile Management & Core DB | 6 pts | 6 pts | 6 pts | 🟢 Done |
| **Sprint 2** | Doctor Profiles, Directory Search & Availability | 13 pts | 13 pts | 13 pts | 🟢 Done |
| **Sprint 3** | Core Booking Engine & Double-Booking Lock | 11 pts | 11 pts | 11 pts | 🟢 Done |
| **Sprint 4** | Appointment Cancellation, Rescheduling & Slot Recovery | 10 pts | 10 pts | 10 pts | 🟢 Done |
| **Sprint 5** | Built-in Scrum Engine, Terminal Kanban, Tests & Release | 14 pts | 14 pts | 14 pts | 🟢 Done |

👉 Detailed sprint goals, task breakdown, and velocity reports: [scrum/SPRINT_PLAN.md](scrum/SPRINT_PLAN.md)

---

## 10. Kanban Board Workflow

The project tracks work through five explicit stages:
```text
BACKLOG ──► TODO ──► IN PROGRESS ──► REVIEW/TESTING ──► DONE
```
- **Live Terminal Board:** Run `python src/main.py --kanban` to render the ASCII board directly from the SQLite database.
- **GitHub Projects Guide:** Comprehensive steps for creating GitHub Issues, labels (`priority: high`, `type: user-story`), and GitHub Projects board views.

👉 Complete Kanban documentation and GitHub setup guide: [scrum/KANBAN_BOARD.md](scrum/KANBAN_BOARD.md)

---

## 11. Project Directory Structure

```text
Online-Appointment-Booking-System-using-Scrum-Agile-Methodology/
│
├── README.md                         # Main project overview & documentation hub
├── requirements.txt                  # Python dependencies (zero-friction standard library)
├── .gitignore                        # Git ignore patterns for Python, IDEs, and SQLite
│
├── src/                              # Core application source code
│   ├── __init__.py                   # Package marker
│   ├── main.py                       # Application entry point, CLI menus & --demo runner
│   ├── database.py                   # SQLite schema, connection manager & seed loader
│   ├── appointment.py                # Appointment booking service & concurrency engine
│   ├── user_story.py                 # User Story service & backlog metrics
│   ├── sprint.py                     # Sprint planning & velocity tracking service
│   ├── action_item.py                # Action item register service
│   └── kanban.py                     # Terminal ASCII Kanban board renderer & transitions
│
├── database/                         # Database storage directory
│   └── appointment.db                # SQLite database (auto-generated & seeded on first run)
│
├── readme/                           # Core Agile requirement specifications
│   ├── USER_STORY.md                 # 12 INVEST user stories with priorities & estimates
│   └── ACCEPTANCE_CRITERIA.md        # Verifiable Given-When-Then criteria & DoD
│
├── scrum/                            # Scrum artifacts and ceremony reports
│   ├── PRODUCT_BACKLOG.md            # Prioritized Product Backlog & Epics
│   ├── SPRINT_PLAN.md                # 5-week sprint breakdown, goals & task estimates
│   ├── ACTION_ITEMS.md               # Weekly action items & retrospective register
│   ├── KANBAN_BOARD.md               # 5-column Kanban board & GitHub Projects guide
│   ├── REQUIREMENT_PRIORITIES.md     # MoSCoW prioritization & point distribution
│   ├── SPRINT_REVIEW.md              # Sprint review reports & stakeholder feedback
│   └── SPRINT_RETROSPECTIVE.md       # Retrospective logs & continuous improvements (Kaizen)
│
├── tests/                            # Automated test suite
│   ├── __init__.py                   # Test package marker
│   └── test_appointment.py          # 15 automated unit & integration test cases
│
└── docs/                             # Academic & architectural documentation
    ├── PROJECT_OBJECTIVES.md         # Syllabus mapping & project objectives
    ├── SYSTEM_DESIGN.md              # 3-tier architecture, ERD & sequence diagrams
    └── TESTING.md                    # Test strategy, execution report & traceability matrix
```

---

## 12. Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your machine ([Download Python](https://www.python.org/downloads/)).
- Git installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/yashkarwa2005/Online-Appointment-Booking-System-using-Scrum-Agile-Methodology.git
cd Online-Appointment-Booking-System-using-Scrum-Agile-Methodology
```

### Step 2: (Optional) Install Dependencies
The application runs out of the box with zero external packages. For optional enhanced terminal formatting:
```bash
pip install -r requirements.txt
```

---

## 13. Running the Application

### Option A: Interactive Menu (Recommended for Exploration)
Launch the full interactive console:
```bash
python src/main.py
```
Pre-seeded accounts for immediate testing:
- **Patient Account:** Username: `rohan_s` | Password: `rohan123`
- **Doctor Account:** Username: `dr_priya` | Password: `priya123`
- **Admin Account:** Username: `admin` | Password: `admin123`

### Option B: Instant Automated Viva Demonstration Mode (Recommended for Viva)
Walk through all Agile user stories and booking operations automatically in under 30 seconds:
```bash
python src/main.py --demo
```

### Option C: Direct Kanban Board Display
Display the live SQLite-driven ASCII Kanban board directly:
```bash
python src/main.py --kanban
```

---

## 14. Testing & Quality Verification

Run the complete automated test suite using Python's built-in `unittest` runner:
```bash
python -m unittest discover tests -v
```
or via the application CLI:
```bash
python src/main.py --test
```

### Test Results Summary:
```text
Ran 15 tests in 0.636s
OK (100% Pass Rate - 0 Failures, 0 Errors)
```
- `TC-01` to `TC-04`: User Registration & Authentication Verification
- `TC-05` to `TC-06`: Doctor Search & Availability Query Verification
- `TC-07` to `TC-08`: Atomic Booking & Double-Booking Lock Verification
- `TC-09` to `TC-11`: History, Cancellation & Rescheduling Verification
- `TC-12` to `TC-13`: Doctor Slot Management & Admin Audit Verification
- `TC-14` to `TC-15`: User Story Backlog & Kanban Transition Verification

👉 Complete test specifications and execution details: [docs/TESTING.md](docs/TESTING.md)

---

## 15. Agile & Scrum Documentation Links

### Core Agile Specifications
- 📖 [User Stories (readme/USER_STORY.md)](readme/USER_STORY.md) — 12 INVEST-compliant user stories with story points and sprint mapping.
- 🎯 [Acceptance Criteria (readme/ACCEPTANCE_CRITERIA.md)](readme/ACCEPTANCE_CRITERIA.md) — Gherkin Given-When-Then criteria and Definition of Done.

### Scrum Artifacts & Ceremonies
- 📊 [Product Backlog (scrum/PRODUCT_BACKLOG.md)](scrum/PRODUCT_BACKLOG.md) — Ranked backlog, themes, and Planning Poker estimation.
- 📅 [Sprint Plan (scrum/SPRINT_PLAN.md)](scrum/SPRINT_PLAN.md) — 5-week schedule, sprint goals, and velocity targets.
- 📌 [Requirement Priorities (scrum/REQUIREMENT_PRIORITIES.md)](scrum/REQUIREMENT_PRIORITIES.md) — MoSCoW prioritization model.
- 📋 [Kanban Board (scrum/KANBAN_BOARD.md)](scrum/KANBAN_BOARD.md) — Visual board workflow and GitHub Projects integration guide.
- 📝 [Action Items Register (scrum/ACTION_ITEMS.md)](scrum/ACTION_ITEMS.md) — Weekly task and impediment register.
- 🔍 [Sprint Review Reports (scrum/SPRINT_REVIEW.md)](scrum/SPRINT_REVIEW.md) — Formal sprint reviews and stakeholder feedback.
- 🔄 [Sprint Retrospectives (scrum/SPRINT_RETROSPECTIVE.md)](scrum/SPRINT_RETROSPECTIVE.md) — Continuous improvement (Kaizen) logs.

### Technical & Academic Documentation
- 🎯 [Project Objectives (docs/PROJECT_OBJECTIVES.md)](docs/PROJECT_OBJECTIVES.md) — Mapping to AM syllabus and viva checklist.
- 📐 [System Design & Architecture (docs/SYSTEM_DESIGN.md)](docs/SYSTEM_DESIGN.md) — Layered architecture, ER diagrams, and sequence flows.
- 🧪 [Testing Strategy (docs/TESTING.md)](docs/TESTING.md) — Unit testing, integration testing, and test case matrix.

---

## 16. Future Scope & Roadmap (Sprint 6+)

- **Online Payment Gateway:** Integration with Razorpay / Stripe for advance consultation deposits.
- **WebRTC Video Consultations:** Encrypted in-browser teleconsultation video streams for remote patients.
- **SMS & Email Notification Service:** Integration with Twilio / SendGrid for instant booking and reminder dispatches.
- **RESTful API Backend:** Decoupling the service layer with FastAPI for mobile apps (Flutter/React Native).
- **Multi-Hospital Federation:** Supporting multi-branch clinics with cross-hospital referral workflows.

---

## 17. Conclusion & Viva Readiness

This project demonstrates both academic rigor and practical software engineering excellence. It provides a complete working implementation of an online appointment booking system while embodying the core principles of Agile and Scrum: iterative development, continuous feedback, test-driven validation, and transparent work visualization.
