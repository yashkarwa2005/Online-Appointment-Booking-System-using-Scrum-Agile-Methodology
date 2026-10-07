# Action Items Register
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Action Items Management in Scrum

In Scrum, **Action Items** are concrete, measurable tasks identified during **Sprint Planning**, **Daily Scrum**, or **Sprint Retrospectives** to drive immediate progress or eliminate identified impediments.

### Status Indicators:
- 🔵 **To Do:** Item is queued for execution in the current iteration.
- 🟡 **In Progress:** Work is currently being actively performed.
- 🟣 **Review:** Work is implemented and undergoing verification, test checks, or code review.
- 🟢 **Done:** Item is completed and verified against the Definition of Done.
- 🔴 **Blocked:** Item is stalled due to an external impediment or dependency.

---

## 2. Weekly Action Items Register

| ID | Action Item | Sprint | Owner | Priority | Due Date | Status |
|---|---|---|---|---|---|---|
| **AI-01** | Set up GitHub repository structure, `.gitignore`, and licensing | Sprint 1 | Yash Karwa | 🔴 High | Week 1 - Day 2 | 🟢 Done |
| **AI-02** | Design normalized SQLite schema with foreign key constraints | Sprint 1 | Dev Team | 🔴 High | Week 1 - Day 4 | 🟢 Done |
| **AI-03** | Implement SHA-256 password salting and hashing module | Sprint 1 | Yash Karwa | 🔴 High | Week 1 - Day 5 | 🟢 Done |
| **AI-04** | Draft User Story and Acceptance Criteria specifications | Sprint 1 | Product Owner | 🟠 Medium | Week 1 - Day 6 | 🟢 Done |
| **AI-05** | Build physician directory query with case-insensitive search | Sprint 2 | Dev Team | 🔴 High | Week 2 - Day 3 | 🟢 Done |
| **AI-06** | Develop slot generation utility for doctor calendar setup | Sprint 2 | Yash Karwa | 🔴 High | Week 2 - Day 4 | 🟢 Done |
| **AI-07** | Populate mock specialist dataset (Cardio, Neuro, Derma) | Sprint 2 | Dev Team | 🟢 Low | Week 2 - Day 6 | 🟢 Done |
| **AI-08** | Implement atomic appointment reservation transaction logic | Sprint 3 | Yash Karwa | 🔴 High | Week 3 - Day 3 | 🟢 Done |
| **AI-09** | Add defensive concurrency guard preventing double bookings | Sprint 3 | Yash Karwa | 🔴 High | Week 3 - Day 4 | 🟢 Done |
| **AI-10** | Construct patient booking history tabular view | Sprint 3 | Dev Team | 🟠 Medium | Week 3 - Day 6 | 🟢 Done |
| **AI-11** | Build appointment cancellation with automatic slot recovery | Sprint 4 | Dev Team | 🔴 High | Week 4 - Day 3 | 🟢 Done |
| **AI-12** | Engineer atomic slot swap algorithm for rescheduling | Sprint 4 | Yash Karwa | 🔴 High | Week 4 - Day 5 | 🟢 Done |
| **AI-13** | Implement built-in Scrum project management database tables | Sprint 5 | Yash Karwa | 🔴 High | Week 5 - Day 2 | 🟢 Done |
| **AI-14** | Create interactive ASCII terminal Kanban board renderer | Sprint 5 | Yash Karwa | 🔴 High | Week 5 - Day 3 | 🟢 Done |
| **AI-15** | Implement 15 automated unit tests with 100% pass rate | Sprint 5 | Yash Karwa | 🔴 High | Week 5 - Day 4 | 🟢 Done |
| **AI-16** | Prepare comprehensive System Design & Architecture diagrams | Sprint 5 | Dev Team | 🟠 Medium | Week 5 - Day 5 | 🟢 Done |
| **AI-17** | Conduct Sprint Review, Retrospective, and final Viva rehearsal | Sprint 5 | Scrum Master | 🔴 High | Week 5 - Day 6 | 🟢 Done |
| **AI-18** | Push all verified commits and documentation to GitHub remote | Sprint 5 | Yash Karwa | 🔴 High | Week 5 - Day 7 | 🟢 Done |

---

## 3. Retrospective Continuous Improvement Action Items

The following action items originated directly from Sprint Retrospectives to drive continuous improvement:

| Source Ceremony | Identified Issue | Agreed Improvement Action | Owner | Outcome |
|---|---|---|---|---|
| **Sprint 1 Retrospective** | Manual database testing caused slowdowns | Introduce an in-memory SQLite fixture for rapid unit testing | Yash Karwa | Implemented in Sprint 2; reduced test cycle to 0.1s. |
| **Sprint 2 Retrospective** | Ambiguity regarding doctor time slot boundaries | Standardize 30-minute consultation slot windows | Dev Team | Applied to all mock seed data and validation logic. |
| **Sprint 3 Retrospective** | Double-booking race conditions during booking | Use explicit SQLite transactional commits and lock checks | Yash Karwa | Eliminated race conditions; 100% verified in `TC-08`. |
| **Sprint 4 Retrospective** | Complex CLI inputs caused demonstration typos | Add an automated `--demo` flag for instant viva walkthrough | Yash Karwa | Created one-command automated demo in `main.py`. |
