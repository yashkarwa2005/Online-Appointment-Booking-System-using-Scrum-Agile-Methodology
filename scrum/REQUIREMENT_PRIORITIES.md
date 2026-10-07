# Requirement Prioritization (MoSCoW Method)
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Overview of the MoSCoW Prioritization Framework

In Agile software engineering, requirements change rapidly based on stakeholder feedback, user testing, and time constraints. To ensure predictable, value-driven delivery within fixed sprint boundaries, the **MoSCoW** prioritization method is employed:

- **🔴 MUST HAVE (M):** Non-negotiable requirements essential for a viable product. If omitted, the release is deemed a failure.
- **🟠 SHOULD HAVE (S):** High-priority features that significantly enhance functionality, but workarounds exist if time is constrained.
- **🟢 COULD HAVE (C):** Desirable enhancements that provide incremental delight or utility, implemented only if capacity allows.
- **⚪ WON'T HAVE (W):** Explicitly agreed out-of-scope items for the current release window, preserved for future roadmap releases.

---

## 2. MoSCoW Category Breakdown

### 🔴 1. MUST HAVE (Critical Core — 32 Story Points)
Without these capabilities, the appointment system cannot perform its fundamental function of facilitating doctor-patient bookings:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-01** | User Registration with secure credential hashing | 3 | Required to establish authenticated patient identity. |
| **US-02** | User Authentication & Session Management | 3 | Essential for role separation (Patient, Doctor, Admin). |
| **US-03** | Search & Directory of Medical Professionals | 5 | Patients cannot book without finding eligible doctors. |
| **US-04** | Real-time Doctor Availability & Time Slot Inspection | 3 | Core scheduling prerequisite to prevent timing mismatches. |
| **US-05** | Atomic Appointment Booking & Double-Booking Prevention | 8 | Core business transaction; absolute transactional integrity required. |
| **US-07** | Appointment Cancellation & Immediate Slot Recovery | 5 | Vital for freeing doctor consultation capacity upon schedule changes. |
| **US-10** | Doctor Consultation Slot Generation & Management | 5 | Doctors must be able to publish open calendar slots. |

---

### 🟠 2. SHOULD HAVE (Important Enhancements — 16 Story Points)
These features significantly improve user experience, operational efficiency, and system transparency:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-06** | Patient Appointment History & Status Overview | 3 | Allows patients to review active bookings and previous consultations. |
| **US-08** | Appointment Rescheduling to Alternative Slot | 5 | Reduces patient friction compared to manually cancelling and re-booking. |
| **US-09** | Instant Confirmation Summary & Booking Receipt | 3 | Provides immediate positive feedback and verification records. |
| **US-12** | Integrated Agile Backlog, Sprint & Kanban Management | 5 | Crucial for the PBL academic requirement demonstrating Scrum in action. |

---

### 🟢 3. COULD HAVE (Desirable Features — 8 Story Points)
These items add convenience and administrative depth without blocking the primary booking flow:

| Story ID | Requirement Description | Story Points | Justification |
|---|---|---|---|
| **US-11** | Administrative Audit Log & System Overview | 3 | Offers centralized hospital management oversight across departments. |
| **US-EXT-1** | Consultation Fee Filter & Doctor Sorting | 2 | Enhances search filtering for budget-conscious patients. |
| **US-EXT-2** | Visual Terminal ASCII Color Badges | 3 | Polishes the presentation interface during viva demonstrations. |

---

### ⚪ 4. WON'T HAVE (Deferred to Future Releases / Roadmap)
To preserve project focus and meet tight academic deadlines, the following features are intentionally out of scope for Release 1.0:

1. **Third-Party Payment Gateway Integration (Stripe/Razorpay):** Offline clinic payment or cash at desk is assumed for this release.
2. **Video Teleconsultation Stream (WebRTC):** Requires heavy streaming infrastructure; in-person clinic appointments are prioritized.
3. **Automated SMS Gateway (Twilio):** Real-time terminal receipts and local logging suffice for current demonstration.
4. **Multi-Hospital Federation:** System is scoped to a unified single hospital / clinic network.

---

## 3. Story Point & Priority Distribution

```text
MoSCoW Category Breakdown:
🔴 Must Have   : 32 Points (57.1%) [██████████████████████████████░░░░░░░░░░░░░░░]
🟠 Should Have : 16 Points (28.6%) [███████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
🟢 Could Have  :  8 Points (14.3%) [███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]
Total Backlog  : 56 Points (100%)
```

### Sprint Velocity Alignment
- Target Team Velocity: **~11 - 16 Story Points per weekly sprint**.
- Total Duration: **5 Sprints (5 Weeks)**.
- Total Committed Capacity: **~56 Story Points**.
- Must-Have items are scheduled into early sprints (Sprints 1 through 3) to mitigate risk and guarantee a shippable increment.

---

## 4. Priority Transition Protocol

If unforeseen impediments arise during a sprint (e.g., technical debt, complex concurrency challenges in double-booking prevention):
1. **Never compromise Must-Have scope or quality.**
2. Under Scrum Master facilitation, the Product Owner downgrades or defers **Could Have** items first.
3. If variance persists, **Should Have** items (e.g., rescheduling automation) are simplified into two-step cancellation-rebooking workflows.
4. All trade-off decisions are formally recorded in [SPRINT_REVIEW.md](file:///d:/COLLEGE/Sem-5/AM&IT/yash/pbl/scrum/SPRINT_REVIEW.md).
