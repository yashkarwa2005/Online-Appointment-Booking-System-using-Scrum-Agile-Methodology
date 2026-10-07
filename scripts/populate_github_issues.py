"""Script to populate GitHub Issues, Labels, and Milestones
Uses the GitHub REST API to synchronize the project's User Stories and Action Items
with color-coded priority labels (High = Red, Medium = Orange/Yellow, Low = Green).
"""
import urllib.request
import urllib.error
import json
import time
import os

TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = "yashkarwa2005"
REPO = "Online-Appointment-Booking-System-using-Scrum-Agile-Methodology"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "User-Agent": "Agile-PBL-Setup",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json"
}


def api_request(endpoint, method="GET", data=None):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=HEADERS,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        # 422 if label/milestone already exists
        return {"error": e.code, "message": err_msg}


def create_or_update_label(name, color, description):
    res = api_request("labels", method="POST", data={
        "name": name,
        "color": color,
        "description": description
    })
    if "error" in res and res["error"] == 422:
        # Update existing label
        safe_name = urllib.parse.quote(name)
        api_request(f"labels/{safe_name}", method="PATCH", data={
            "color": color,
            "description": description
        })
    print(f"[*] Label '{name}' configured with color #{color}")


def create_milestones():
    milestones = [
        ("Sprint 1 - User Authentication & Architecture", "Deliver user registration, authentication and database architecture.", 1),
        ("Sprint 2 - Doctor Directory & Schedules", "Deliver doctor listing, search filtering, and calendar availability.", 2),
        ("Sprint 3 - Core Booking & Concurrency Lock", "Implement atomic appointment booking and double-booking guard.", 3),
        ("Sprint 4 - Cancellation & Rescheduling", "Support full appointment lifecycle with automatic slot recovery.", 4),
        ("Sprint 5 - Scrum Engine, Tests & Release", "Integrate in-app Scrum/Kanban board, test coverage, and final viva release.", 5),
    ]
    created = {}
    for title, desc, num in milestones:
        res = api_request("milestones", method="POST", data={
            "title": title,
            "description": desc,
            "state": "closed" if num <= 4 else "open"
        })
        if "number" in res:
            created[num] = res["number"]
            print(f"[*] Created Milestone '{title}' (# {res['number']})")
        else:
            # Fetch existing
            list_res = api_request("milestones?state=all")
            for m in list_res:
                if m["title"] == title:
                    created[num] = m["number"]
                    break
    return created


def main():
    import urllib.parse

    print("=== Step 1: Setting up Priority and Status Labels with Color Coding ===")
    labels = [
        # Color coding for priorities:
        ("priority: high", "d73a4a", "High Priority - Must Have [Red]"),
        ("priority: medium", "fbca04", "Medium Priority - Should Have [Amber/Yellow]"),
        ("priority: low", "0e8a16", "Low Priority - Could Have [Green]"),
        # Types:
        ("type: user-story", "7057ff", "Agile User Story [Purple]"),
        ("type: action-item", "0075ca", "Scrum Action Item [Blue]"),
        # Status columns for Kanban:
        ("status: backlog", "cfd3d7", "Kanban Column: Backlog"),
        ("status: todo", "1d76db", "Kanban Column: To Do"),
        ("status: in-progress", "d93f0b", "Kanban Column: In Progress"),
        ("status: review", "a2eeef", "Kanban Column: Review/Testing"),
        ("status: done", "0e8a16", "Kanban Column: Done"),
    ]
    for name, color, desc in labels:
        create_or_update_label(name, color, desc)

    print("\n=== Step 2: Creating Sprint Milestones ===")
    milestone_map = create_milestones()

    print("\n=== Step 3: Populating User Stories as GitHub Issues ===")
    user_stories = [
        {
            "code": "US-01",
            "title": "[US-01] User Registration & Credential Hashing",
            "body": """### User Story
**As a** new patient,  
**I want** to register an account with username, email, and password,  
**So that** I can access the appointment platform securely.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1

### Acceptance Criteria
- [x] Validates unique username and email.
- [x] Hashes passwords securely with SHA-256 + salt.
- [x] Prevents duplicate accounts.
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-02",
            "title": "[US-02] Secure Credential Authentication & Login",
            "body": """### User Story
**As a** registered user,  
**I want** to log in using my credentials,  
**So that** the system loads my authenticated session.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 1

### Acceptance Criteria
- [x] Verifies password hash against stored hash.
- [x] Rejects invalid credentials cleanly.
- [x] Assigns session role (patient, doctor, admin).
""",
            "priority": "priority: high",
            "sprint": 1,
            "status": "status: done"
        },
        {
            "code": "US-03",
            "title": "[US-03] Search & Filter Doctors by Specialization",
            "body": """### User Story
**As a** patient,  
**I want** to search doctors by specialization, department, and fee,  
**So that** I can choose the right medical specialist.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Case-insensitive keyword search for doctors.
- [x] Displays department, fee, and doctor bio.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-04",
            "title": "[US-04] Real-time Doctor Schedule & Open Slot Query",
            "body": """### User Story
**As a** patient,  
**I want** to view open consultation slots for a doctor,  
**So that** I can pick an available time.

### Story Points: 3 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Filters slots where `is_booked = 0`.
- [x] Formats date and time cleanly.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-05",
            "title": "[US-05] Atomic Appointment Booking & Double-Booking Lock",
            "body": """### User Story
**As a** patient,  
**I want** to reserve an open consultation slot,  
**So that** it is locked immediately and cannot be double-booked.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 3

### Acceptance Criteria
- [x] Atomic SQLite transaction locking slot.
- [x] Concurrency check aborting conflicting bookings.
- [x] Unique appointment ID generated.
""",
            "priority": "priority: high",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-06",
            "title": "[US-06] Patient Appointment History & Status Overview",
            "body": """### User Story
**As a** patient,  
**I want** to review all my scheduled and past appointments,  
**So that** I can keep track of my consultations.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 3

### Acceptance Criteria
- [x] Returns all bookings for authenticated patient.
- [x] Shows doctor, date, time, and status.
""",
            "priority": "priority: medium",
            "sprint": 3,
            "status": "status: done"
        },
        {
            "code": "US-07",
            "title": "[US-07] Cancel Appointment & Atomically Release Slot",
            "body": """### User Story
**As a** patient,  
**I want** to cancel a scheduled appointment,  
**So that** the doctor's slot is freed for other patients.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 4

### Acceptance Criteria
- [x] Sets appointment status to `Cancelled`.
- [x] Releases slot `is_booked = 0`.
- [x] Prevents duplicate cancellation.
""",
            "priority": "priority: high",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-08",
            "title": "[US-08] Reschedule Booking to Alternative Open Slot",
            "body": """### User Story
**As a** patient,  
**I want** to reschedule my booking to a new open slot,  
**So that** I can adjust my consultation date cleanly.

### Story Points: 5 | Priority: Medium (Should Have)
### Target Sprint: Sprint 4

### Acceptance Criteria
- [x] Releases old slot atomically.
- [x] Locks new target slot.
- [x] Updates appointment date and time.
""",
            "priority": "priority: medium",
            "sprint": 4,
            "status": "status: done"
        },
        {
            "code": "US-09",
            "title": "[US-09] Real-time Booking Confirmation Receipts",
            "body": """### User Story
**As a** patient,  
**I want** to receive a clear confirmation receipt,  
**So that** I have reassurance of my booking details.

### Story Points: 3 | Priority: Medium (Should Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Displays appointment reference, doctor, date, fee, and notes.
""",
            "priority": "priority: medium",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-10",
            "title": "[US-10] Doctor Consultation Schedule & Slot Management",
            "body": """### User Story
**As a** doctor,  
**I want** to publish open consultation slots,  
**So that** patients can book appointments with me.

### Story Points: 5 | Priority: High (Must Have)
### Target Sprint: Sprint 2

### Acceptance Criteria
- [x] Validates date and start/end time.
- [x] Inserts new slot into availability table.
""",
            "priority": "priority: high",
            "sprint": 2,
            "status": "status: done"
        },
        {
            "code": "US-11",
            "title": "[US-11] Hospital Administrative Audit Log & Oversight",
            "body": """### User Story
**As an** administrator,  
**I want** to view all appointments across all doctors,  
**So that** I can monitor hospital utilization.

### Story Points: 3 | Priority: Low (Could Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Centralized view across all patients and doctors.
""",
            "priority": "priority: low",
            "sprint": 5,
            "status": "status: done"
        },
        {
            "code": "US-12",
            "title": "[US-12] In-App Scrum Backlog, Sprint & Kanban Engine",
            "body": """### User Story
**As a** Scrum team member,  
**I want** to track user stories and Kanban board within the software,  
**So that** our team practices transparent Agile software engineering.

### Story Points: 8 | Priority: High (Must Have)
### Target Sprint: Sprint 5

### Acceptance Criteria
- [x] Persistent SQLite user stories and sprints tables.
- [x] Terminal ASCII Kanban board with 5 columns.
- [x] Dynamic card movement and progress tracking.
""",
            "priority": "priority: high",
            "sprint": 5,
            "status": "status: done"
        }
    ]

    for st in user_stories:
        data = {
            "title": st["title"],
            "body": st["body"],
            "labels": [st["priority"], "type: user-story", st["status"]],
        }
        if st["sprint"] in milestone_map:
            data["milestone"] = milestone_map[st["sprint"]]

        res = api_request("issues", method="POST", data=data)
        if "number" in res:
            print(f"[+] Created Issue #{res['number']}: {st['title']}")
        else:
            print(f"[-] Issue error: {res}")
        time.sleep(0.3)

    print("\n[SUCCESS] All labels, milestones, and issues created on GitHub with color coding!")


if __name__ == "__main__":
    main()
