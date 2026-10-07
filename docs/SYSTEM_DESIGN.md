# System Design & Architecture
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. System Architecture

The project is architected following a modular **3-Tier Layered Architecture**, separating user interaction, business rules, and persistent data storage.

```mermaid
graph TD
    subgraph Presentation_Layer [Presentation Layer / CLI]
        CLI[Interactive CLI & Terminal UI - main.py]
        KanbanRenderer[Terminal Kanban ASCII Renderer - kanban.py]
        DemoEngine[Automated Viva Demo Engine]
    end

    subgraph Service_Layer [Service & Business Logic Layer]
        ApptService[Appointment & User Service - appointment.py]
        StoryService[User Story Service - user_story.py]
        SprintService[Sprint Planning Service - sprint.py]
        ActionService[Action Items Service - action_item.py]
    end

    subgraph Data_Layer [Data & Persistence Layer]
        DBManager[Database Manager & SQLite Engine - database.py]
        SQLiteDB[(SQLite Database - appointment.db)]
    end

    CLI --> ApptService
    CLI --> StoryService
    CLI --> SprintService
    CLI --> ActionService
    CLI --> KanbanRenderer

    ApptService --> DBManager
    StoryService --> DBManager
    SprintService --> DBManager
    ActionService --> DBManager
    KanbanRenderer --> StoryService
    KanbanRenderer --> ActionService

    DBManager --> SQLiteDB
```

---

## 2. Database Design & Entity-Relationship Diagram (ERD)

The system utilizes an embedded relational database (SQLite) with strict foreign key constraints enabled.

```mermaid
erDiagram
    USERS ||--o{ PROFESSIONALS : "is profile of"
    USERS ||--o{ APPOINTMENTS : "books"
    PROFESSIONALS ||--o{ AVAILABILITY : "publishes"
    PROFESSIONALS ||--o{ APPOINTMENTS : "attends"
    AVAILABILITY ||--o| APPOINTMENTS : "allocated to"
    SPRINTS ||--o{ USER_STORIES : "contains"
    SPRINTS ||--o{ ACTION_ITEMS : "tracks"

    USERS {
        int id PK
        string username UK
        string password_hash
        string full_name
        string email UK
        string phone
        string role
        timestamp created_at
    }

    PROFESSIONALS {
        int id PK
        int user_id FK
        string specialization
        string department
        real consultation_fee
        string bio
        timestamp created_at
    }

    AVAILABILITY {
        int id PK
        int professional_id FK
        string date
        string start_time
        string end_time
        int is_booked
        timestamp created_at
    }

    APPOINTMENTS {
        int id PK
        int user_id FK
        int professional_id FK
        int availability_id FK
        string appointment_date
        string appointment_time
        string status
        string notes
        timestamp created_at
    }

    SPRINTS {
        int id PK
        int sprint_number UK
        string name
        string goal
        string start_date
        string end_date
        string status
        int velocity
        timestamp created_at
    }

    USER_STORIES {
        int id PK
        string story_code UK
        string title
        string role
        string want
        string benefit
        string priority
        int story_points
        int sprint_id FK
        string status
        string assignee
        string description
        timestamp created_at
    }

    ACTION_ITEMS {
        int id PK
        string item_code UK
        string description
        int sprint_id FK
        string owner
        string priority
        string due_date
        string status
        timestamp created_at
    }
```

---

## 3. Sequence Diagrams

### A. Appointment Booking & Double-Booking Lock Flow
```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant CLI as Presentation CLI
    participant Service as AppointmentService
    participant DB as SQLite Database

    Patient->>CLI: Select Doctor & View Available Slots
    CLI->>Service: get_available_slots(doctor_id)
    Service->>DB: SELECT * FROM availability WHERE professional_id = ? AND is_booked = 0
    DB-->>Service: Return open slots
    Service-->>CLI: Display slots to Patient

    Patient->>CLI: Choose Slot #S1 and Confirm Booking
    CLI->>Service: book_appointment(patient_id, doctor_id, slot_id, notes)
    Service->>DB: BEGIN TRANSACTION
    Service->>DB: SELECT is_booked FROM availability WHERE id = ?
    alt Slot is already booked (is_booked == 1)
        Service->>DB: ROLLBACK
        Service-->>CLI: Error: Slot already booked!
        CLI-->>Patient: Display Error Alert
    else Slot is open (is_booked == 0)
        Service->>DB: UPDATE availability SET is_booked = 1 WHERE id = ?
        Service->>DB: INSERT INTO appointments (...) VALUES (...)
        Service->>DB: COMMIT TRANSACTION
        DB-->>Service: Appointment ID & Success
        Service-->>CLI: Booking Confirmed Details
        CLI-->>Patient: Display Confirmation Receipt
    end
```

---

### B. Rescheduling Flow (Atomic Slot Swap)
```mermaid
sequenceDiagram
    autonumber
    actor Patient
    participant CLI as Presentation CLI
    participant Service as AppointmentService
    participant DB as SQLite Database

    Patient->>CLI: Request Reschedule for Appointment #A1
    CLI->>Service: get_available_slots(doctor_id)
    Service-->>CLI: Open slot list
    Patient->>CLI: Select New Slot #S2
    CLI->>Service: reschedule_appointment(appointment_id, new_slot_id, patient_id)
    Service->>DB: BEGIN TRANSACTION
    Service->>DB: Check new slot is_booked == 0
    Service->>DB: UPDATE availability SET is_booked = 0 WHERE id = old_slot_id
    Service->>DB: UPDATE availability SET is_booked = 1 WHERE id = new_slot_id
    Service->>DB: UPDATE appointments SET availability_id = new_slot_id, ... WHERE id = appt_id
    Service->>DB: COMMIT TRANSACTION
    Service-->>CLI: Rescheduling Confirmed
    CLI-->>Patient: Display Updated Booking Receipt
```

---

### C. Scrum User Story Transition Flow
```mermaid
sequenceDiagram
    autonumber
    actor Developer
    participant CLI as Terminal Menu
    participant Kanban as KanbanService
    participant DB as SQLite Database

    Developer->>CLI: Select "Move Task on Kanban Board"
    CLI->>Kanban: get_kanban_board()
    Kanban->>DB: SELECT * FROM user_stories ORDER BY priority
    DB-->>Kanban: Stories grouped by status
    Kanban-->>CLI: Render ASCII Kanban Board
    Developer->>CLI: Select Story (US-05) -> Change status to "In Progress"
    CLI->>Kanban: update_story_status(story_code, "In Progress")
    Kanban->>DB: UPDATE user_stories SET status = 'In Progress' WHERE story_code = ?
    DB-->>Kanban: Row Updated
    Kanban-->>CLI: Success Confirmation
    CLI->>Kanban: Render Updated Board
    Kanban-->>Developer: Card US-05 now rendered under [IN PROGRESS] column
```

---

## 4. Key Design Decisions & Security Considerations

1. **Transactional Integrity & Concurrency:**
   - Double-booking is strictly prohibited through atomic SQLite transactions. Before any booking insertion, the system verifies `is_booked == 0` within the transaction and issues an immediate lock update.
2. **Password Security:**
   - Passwords are never stored in plain text. Passwords use SHA-256 with a unique salt per account to defend against rainbow table lookups.
3. **Data Relational Integrity:**
   - Foreign keys are enforced on SQLite startup using `PRAGMA foreign_keys = ON;`. Deleting a user cascade-protects or safely restricts dependent appointments.
4. **Portability:**
   - Built exclusively with Python standard libraries (`sqlite3`, `hashlib`, `datetime`, `unittest`) ensures immediate portability across Windows, macOS, and Linux without environment setup headaches.
