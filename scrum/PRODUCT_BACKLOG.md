# Product Backlog
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Product Vision & Backlog Strategy

### Vision Statement
> *"To engineer a high-reliability, zero-friction online medical appointment booking platform that empowers patients to discover specialized physicians, inspect real-time availability, and secure reservations instantaneously without double-booking risks, while exemplifying disciplined Scrum Agile engineering practices."*

### Product Backlog Overview
The **Product Backlog** is an emergent, ordered list of what is needed to improve the product. It is the single source of work undertaken by the Scrum Team, managed and prioritized by the **Product Owner**.

Items are ordered based on:
1. **Business Value & Criticality** (MoSCoW priority).
2. **Technical Feasibility & Dependencies** (Foundational infrastructure prior to business logic).
3. **Risk Reduction** (Double-booking concurrency addressed early).

---

## 2. Product Epics & Architecture Themes

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PRODUCT BACKLOG EPICS                           │
└────────────────────────────────────────────────────────────────────────┘
     │
     ├── EPIC 1: Security & Identity Management (US-01, US-02)
     ├── EPIC 2: Professional Directory & Schedule Management (US-03, US-04, US-10)
     ├── EPIC 3: Core Booking & Concurrency Engine (US-05, US-06)
     ├── EPIC 4: Appointment Lifecycle & Slot Recovery (US-07, US-08)
     └── EPIC 5: Operational Auditing & Agile Governance (US-09, US-11, US-12)
```

---

## 3. Prioritized Product Backlog Inventory

| Backlog Rank | Story ID | Title & Epic | Role | Priority | Story Points | Sprint Target | Status |
|---|---|---|---|---|---|---|---|
| **01** | `US-01` | User Registration & Profile Initialization (Epic 1) | Patient / User | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **02** | `US-02` | Secure Credential Authentication & Session (Epic 1) | All Users | 🔴 Must Have | 3 | Sprint 1 | 🟢 Done |
| **03** | `US-10` | Doctor Consultation Slot Generation (Epic 2) | Doctor | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **04** | `US-03` | Search & Filter Doctors by Specialization (Epic 2) | Patient | 🔴 Must Have | 5 | Sprint 2 | 🟢 Done |
| **05** | `US-04` | Real-time Doctor Schedule & Slot Query (Epic 2) | Patient | 🔴 Must Have | 3 | Sprint 2 | 🟢 Done |
| **06** | `US-05` | Atomic Appointment Booking & Double-Booking Lock (Epic 3) | Patient | 🔴 Must Have | 8 | Sprint 3 | 🟢 Done |
| **07** | `US-06` | View Patient Appointment History & Status (Epic 3) | Patient | 🟠 Should Have | 3 | Sprint 3 | 🟢 Done |
| **08** | `US-07` | Cancel Appointment & Atomically Release Slot (Epic 4) | Patient | 🔴 Must Have | 5 | Sprint 4 | 🟢 Done |
| **09** | `US-08` | Reschedule Booking to Alternative Open Slot (Epic 4) | Patient | 🟠 Should Have | 5 | Sprint 4 | 🟢 Done |
| **10** | `US-09` | Real-time Transaction Confirmation Receipts (Epic 5) | Patient | 🟠 Should Have | 3 | Sprint 5 | 🟢 Done |
| **11** | `US-11` | Hospital Administrative Audit Log & Monitoring (Epic 5) | Administrator | 🟢 Could Have | 3 | Sprint 5 | 🟢 Done |
| **12** | `US-12` | In-App Scrum Backlog, Sprint & Kanban Engine (Epic 5) | Scrum Team | 🔴 Must Have | 8 | Sprint 5 | 🟢 Done |

**Total Estimated Backlog Effort:** 51 Story Points  
**Estimation Scale:** Modified Fibonacci Sequence (1, 2, 3, 5, 8, 13) via Planning Poker.

---

## 4. Backlog Refinement (Grooming) Ceremonies

Backlog grooming occurred mid-sprint to keep items ready for future sprint planning:
1. **Splitting Large Stories:** The original monolithic *"Manage Appointments"* story was sliced into three independently testable stories: `US-05 (Booking)`, `US-07 (Cancellation)`, and `US-08 (Rescheduling)`.
2. **Clarifying Acceptance Criteria:** Strict conditions for atomic transactions and slot rollback were attached to `US-05` and `US-08`.
3. **Re-evaluating Estimates:** `US-05` was initially estimated at 5 points, but after team review of potential race conditions in double-booking prevention, was increased to 8 points.

---

## 5. Artifact Links
- User Stories Detail: [readme/USER_STORY.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/USER_STORY.md)
- Acceptance Criteria Detail: [readme/ACCEPTANCE_CRITERIA.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/readme/ACCEPTANCE_CRITERIA.md)
- Requirement Priorities: [scrum/REQUIREMENT_PRIORITIES.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/scrum/REQUIREMENT_PRIORITIES.md)
- Sprint Plan: [scrum/SPRINT_PLAN.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/scrum/SPRINT_PLAN.md)
