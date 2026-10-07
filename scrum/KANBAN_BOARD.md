# Kanban Board & Workflow
## Online Appointment Booking System using Scrum Agile Methodology

---

## 1. Kanban Methodology Overview

**Kanban** is a visual workflow management method that emphasizes real-time capacity communication, limiting Work-in-Progress (WIP), and maximizing efficiency. In this project, the development lifecycle was visualized across five core stages:

```text
┌───────────┐     ┌──────────┐     ┌─────────────┐     ┌────────────────┐     ┌──────────┐
│  BACKLOG  │ ──► │   TODO   │ ──► │ IN PROGRESS │ ──► │ REVIEW/TESTING │ ──► │   DONE   │
└───────────┘     └──────────┘     └─────────────┘     └────────────────┘     └──────────┘
```

### Core Kanban Rules Applied
1. **Visualize the Workflow:** All user stories and technical tasks are represented as visual cards.
2. **Limit Work In Progress (WIP):** Maximum of 2 tasks per developer in `IN PROGRESS` to prevent multitasking bottlenecks.
3. **Manage Flow:** Daily standups focus on moving cards rightward rather than starting new cards.
4. **Continuous Quality Gate:** Items cannot move to `DONE` without passing automated unit tests.

### Priority Badges:
- 🔴 **High Priority (Must Have)**
- 🟠 **Medium Priority (Should Have)**
- 🟢 **Low Priority (Could Have)**

---

## 2. Live Project Kanban Board (Sprint 5 Final State)

| 📋 BACKLOG | 📝 TODO | ⚙️ IN PROGRESS | 🔍 REVIEW / TESTING | ✅ DONE |
|---|---|---|---|---|
| 🟢 `US-EXT-1` [3 pts]<br>Fee Filter & Doctor Sorting<br>_Assignee: Unassigned_ | 🟢 `US-EXT-2` [2 pts]<br>Terminal ASCII Color Badges<br>_Assignee: Dev Team_ | 🟠 `AI-16` [2 pts]<br>Prepare Comprehensive System Design diagrams<br>_Assignee: Dev Team_ | 🔴 `AI-17` [3 pts]<br>Sprint Review & Viva rehearsal<br>_Assignee: Scrum Master_ | 🔴 `US-01` [3 pts]<br>User Registration Module<br>_Assignee: Yash Karwa_ |
| 🟢 `US-EXT-3` [2 pts]<br>SMS Gateway Integration<br>_Assignee: Unassigned_ | | | | 🔴 `US-02` [3 pts]<br>Authentication & Session Auth<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-03` [5 pts]<br>Search Doctors Directory<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-04` [3 pts]<br>Doctor Availability & Slots<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-05` [8 pts]<br>Atomic Appointment Booking<br>_Assignee: Yash Karwa_ |
| | | | | 🟠 `US-06` [3 pts]<br>Patient Booking History<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-07` [5 pts]<br>Cancel & Free Slot<br>_Assignee: Dev Team_ |
| | | | | 🟠 `US-08` [5 pts]<br>Reschedule Appointment<br>_Assignee: Yash Karwa_ |
| | | | | 🟠 `US-09` [3 pts]<br>Confirmation Receipts<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-10` [5 pts]<br>Doctor Schedule Manager<br>_Assignee: Yash Karwa_ |
| | | | | 🟢 `US-11` [3 pts]<br>Admin Oversight Audit<br>_Assignee: Dev Team_ |
| | | | | 🔴 `US-12` [8 pts]<br>In-App Scrum & Kanban Engine<br>_Assignee: Yash Karwa_ |
| | | | | 🔴 `AI-15` [3 pts]<br>Automated Unit Tests (15/15)<br>_Assignee: Yash Karwa_ |

---

## 3. Terminal Interactive Kanban Board

In addition to this Markdown documentation, the application includes a **dynamic terminal Kanban board** built directly into the Python application (`src/kanban.py`).

To display the live database-driven Kanban board in your terminal, run:

```bash
python src/main.py --kanban
```

This queries the SQLite `user_stories` table in real time and renders formatted ASCII cards organized by current column status.

---

## 4. How to Implement this Board on GitHub Projects & GitHub Issues

> **Important Disclosure:** The table above represents the architectural Kanban board designed and tracked by the Scrum team. While GitHub provides the web-based "Projects" tool, this repository contains the complete specification and in-app engine so that anyone can configure a native GitHub Project board in seconds.

### Step-by-Step GitHub Setup Guide

#### Step 1: Create GitHub Issue Labels
In your GitHub repository, navigate to **Issues > Labels** and create the following priority and type labels:
- `priority: high` (🔴 Color: `#d73a4a`)
- `priority: medium` (🟠 Color: `#fbca04`)
- `priority: low` (🟢 Color: `#0e8a16`)
- `type: user-story` (🟣 Color: `#7057ff`)
- `type: action-item` (🔵 Color: `#0075ca`)

#### Step 2: Create GitHub Milestones
Navigate to **Issues > Milestones** and create one milestone per weekly sprint:
- `Sprint 1 - User Management & Authentication`
- `Sprint 2 - Doctor Directory & Schedules`
- `Sprint 3 - Core Booking & Concurrency`
- `Sprint 4 - Cancellation & Rescheduling`
- `Sprint 5 - Scrum Engine, Testing & Release`

#### Step 3: Convert User Stories to GitHub Issues
For each story in `readme/USER_STORY.md`:
1. Click **New Issue**.
2. Title: `[US-05] Book Appointment & Slot Lock`.
3. Body: Paste the User Story and Acceptance Criteria from `readme/ACCEPTANCE_CRITERIA.md`.
4. Assignees: Select team member.
5. Milestone: Set to `Sprint 3`.
6. Labels: `type: user-story`, `priority: high`.

#### Step 4: Create a GitHub Project (Board View)
1. Go to repository tab **Projects > New Project**.
2. Select the **Board** layout template.
3. Configure the 5 columns:
   - `Backlog`
   - `Todo`
   - `In Progress`
   - `Review / Testing`
   - `Done`
4. Enable built-in GitHub workflows:
   - Automatically move newly opened issues to `Todo`.
   - Automatically move pull requests / closed issues to `Done`.
