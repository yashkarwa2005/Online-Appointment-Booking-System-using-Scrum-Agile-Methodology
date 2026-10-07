"""Database Module for Online Appointment Booking System
Manages SQLite connection, schema definition, foreign key enforcement, and seed data.
"""
import os
import sqlite3
import hashlib
from typing import Optional

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database")
DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "appointment.db")


def hash_password(password: str, salt: str = "scrum_salt_2026") -> str:
    """Hashes a password with salt using SHA-256."""
    return hashlib.sha256(f"{salt}_{password}".encode("utf-8")).hexdigest()


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Returns a SQLite connection with foreign keys enabled and row_factory set to sqlite3.Row."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    elif db_path != ":memory:":
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Creates database schema if tables do not exist."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        role TEXT NOT NULL CHECK(role IN ('patient', 'doctor', 'admin')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Professionals / Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professionals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        specialization TEXT NOT NULL,
        department TEXT NOT NULL,
        consultation_fee REAL NOT NULL,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. Availability Slots Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professional_id INTEGER NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
        date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        is_booked INTEGER DEFAULT 0 CHECK(is_booked IN (0, 1)),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        professional_id INTEGER NOT NULL REFERENCES professionals(id) ON DELETE CASCADE,
        availability_id INTEGER NOT NULL REFERENCES availability(id),
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Confirmed' CHECK(status IN ('Confirmed', 'Cancelled', 'Completed')),
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Sprints Table (Scrum Management)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sprint_number INTEGER UNIQUE NOT NULL,
        name TEXT NOT NULL,
        goal TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Planning' CHECK(status IN ('Planning', 'Active', 'Completed')),
        velocity INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 6. User Stories Table (Product Backlog & Sprint Backlog)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        role TEXT NOT NULL,
        want TEXT NOT NULL,
        benefit TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('Must Have', 'Should Have', 'Could Have', 'Won''t Have')),
        story_points INTEGER NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        status TEXT NOT NULL DEFAULT 'Backlog' CHECK(status IN ('Backlog', 'To Do', 'In Progress', 'Review/Testing', 'Done')),
        assignee TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 7. Action Items Table (Sprint Action Items & Standups)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_code TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        sprint_id INTEGER REFERENCES sprints(id) ON DELETE SET NULL,
        owner TEXT NOT NULL,
        priority TEXT NOT NULL CHECK(priority IN ('High', 'Medium', 'Low')),
        due_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'To Do' CHECK(status IN ('To Do', 'In Progress', 'Review', 'Done', 'Blocked')),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


def seed_initial_data(db_path: Optional[str] = None) -> None:
    """Populates realistic initial data for demonstration and testing if the DB is empty."""
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM users;")
    if cursor.fetchone()["count"] > 0:
        conn.close()
        return  # Data already seeded

    # Seed Default Users (Admin, Doctors, Patients)
    default_users = [
        ("admin", hash_password("admin123"), "System Administrator", "admin@hospital.org", "9876500000", "admin"),
        ("dr_priya", hash_password("priya123"), "Dr. Priya Verma", "priya.verma@hospital.org", "9876511111", "doctor"),
        ("dr_amit", hash_password("amit123"), "Dr. Amit Patel", "amit.patel@hospital.org", "9876522222", "doctor"),
        ("dr_sneha", hash_password("sneha123"), "Dr. Sneha Roy", "sneha.roy@hospital.org", "9876533333", "doctor"),
        ("rohan_s", hash_password("rohan123"), "Rohan Sharma", "rohan.sharma@gmail.com", "9876544444", "patient"),
        ("ananya_m", hash_password("ananya123"), "Ananya Mishra", "ananya.m@gmail.com", "9876555555", "patient"),
    ]
    cursor.executemany("""
        INSERT INTO users (username, password_hash, full_name, email, phone, role)
        VALUES (?, ?, ?, ?, ?, ?);
    """, default_users)

    # Fetch User IDs for doctors
    cursor.execute("SELECT id, username FROM users WHERE role = 'doctor';")
    doc_map = {row["username"]: row["id"] for row in cursor.fetchall()}

    # Seed Doctor Profiles
    doctor_profiles = [
        (doc_map["dr_priya"], "Cardiology", "Heart & Vascular Care", 1200.0, "Senior Interventional Cardiologist with 12 years clinical experience."),
        (doc_map["dr_amit"], "Neurology", "Neuroscience & Brain Health", 1500.0, "Chief Neurologist specializing in stroke management and epilepsy care."),
        (doc_map["dr_sneha"], "Dermatology", "Skin & Aesthetics Center", 800.0, "Consultant Dermatologist focusing on clinical trichology and skin wellness."),
    ]
    cursor.executemany("""
        INSERT INTO professionals (user_id, specialization, department, consultation_fee, bio)
        VALUES (?, ?, ?, ?, ?);
    """, doctor_profiles)

    # Fetch professional IDs
    cursor.execute("SELECT id, specialization FROM professionals;")
    prof_list = cursor.fetchall()
    prof_ids = [row["id"] for row in prof_list]

    # Seed Availability Slots for each doctor
    sample_dates = ["2026-10-15", "2026-10-16", "2026-10-17"]
    sample_times = [
        ("09:00", "09:30"),
        ("10:00", "10:30"),
        ("11:30", "12:00"),
        ("14:00", "14:30"),
        ("15:30", "16:00")
    ]
    slots = []
    for pid in prof_ids:
        for d in sample_dates:
            for st, et in sample_times:
                slots.append((pid, d, st, et, 0))

    cursor.executemany("""
        INSERT INTO availability (professional_id, date, start_time, end_time, is_booked)
        VALUES (?, ?, ?, ?, ?);
    """, slots)

    # Seed Sprints (Sprint 1 to Sprint 5)
    sprints = [
        (1, "Sprint 1: Auth & User Core", "Deliver user registration, authentication and database architecture.", "2026-09-01", "2026-09-07", "Completed", 6),
        (2, "Sprint 2: Doctor Directory", "Deliver doctor listing, search filtering, and calendar availability.", "2026-09-08", "2026-09-14", "Completed", 13),
        (3, "Sprint 3: Booking Engine", "Implement atomic appointment booking and double-booking guard.", "2026-09-15", "2026-09-21", "Completed", 11),
        (4, "Sprint 4: Cancellation & Rescheduling", "Support full appointment lifecycle with automatic slot recovery.", "2026-09-22", "2026-09-28", "Completed", 10),
        (5, "Sprint 5: Scrum Engine & Release", "Integrate in-app Scrum/Kanban board, test coverage, and final viva release.", "2026-09-29", "2026-10-06", "Completed", 14),
    ]
    cursor.executemany("""
        INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, sprints)

    # Seed User Stories (Matching USER_STORY.md)
    user_stories = [
        ("US-01", "User Registration", "Patient", "register an account", "access booking platform securely", "Must Have", 3, 1, "Done", "Yash Karwa", "Enforce secure SHA-256 salted password hashing."),
        ("US-02", "User Authentication & Login", "User", "log in with credentials", "access role-based dashboard", "Must Have", 3, 1, "Done", "Dev Team", "Provide session authentication with validation."),
        ("US-03", "Search Doctors by Specialization", "Patient", "search doctors by specialty", "find appropriate healthcare specialist", "Must Have", 5, 2, "Done", "Dev Team", "Filter by department, fee, and name."),
        ("US-04", "View Doctor Available Slots", "Patient", "view open consultation slots", "pick suitable consultation time", "Must Have", 3, 2, "Done", "Dev Team", "Query unbooked slots in real-time."),
        ("US-05", "Book Appointment & Slot Lock", "Patient", "book an open slot", "reserve consultation without double-booking", "Must Have", 8, 3, "Done", "Yash Karwa", "Execute atomic transaction locking slot."),
        ("US-06", "View Appointment History", "Patient", "view my active and past bookings", "track scheduled consultations", "Should Have", 3, 3, "Done", "Dev Team", "Tabular display of booking records."),
        ("US-07", "Cancel Appointment & Release Slot", "Patient", "cancel a scheduled appointment", "free slot for other patients", "Must Have", 5, 4, "Done", "Dev Team", "Atomically flip is_booked back to 0."),
        ("US-08", "Reschedule Appointment", "Patient", "reschedule to alternative slot", "adjust consultation date cleanly", "Should Have", 5, 4, "Done", "Yash Karwa", "Release old slot and lock new slot atomically."),
        ("US-09", "Instant Confirmation Receipts", "Patient", "view booking receipt summary", "confirm consultation details", "Should Have", 3, 5, "Done", "Dev Team", "Formatted appointment receipt."),
        ("US-10", "Doctor Availability Management", "Doctor", "publish consultation schedule", "enable patients to book slots", "Must Have", 5, 2, "Done", "Dev Team", "Add new date/time availability windows."),
        ("US-11", "Admin Appointment Oversight", "Admin", "view all clinic appointments", "monitor clinic operations and audit", "Could Have", 3, 5, "Done", "Dev Team", "Global appointment oversight screen."),
        ("US-12", "In-App Scrum & Kanban Engine", "Scrum Team", "track stories and Kanban board", "practice transparent Agile development", "Must Have", 8, 5, "Done", "Yash Karwa", "ASCII Kanban board and sprint metrics."),
    ]
    cursor.executemany("""
        INSERT INTO user_stories (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, user_stories)

    # Seed Action Items (Matching ACTION_ITEMS.md)
    action_items = [
        ("AI-01", "Initialize Git repository and directory layout", 1, "Yash Karwa", "High", "2026-09-02", "Done"),
        ("AI-02", "Design SQLite schema with foreign key checks", 1, "Dev Team", "High", "2026-09-04", "Done"),
        ("AI-03", "Implement SHA-256 password salting module", 1, "Yash Karwa", "High", "2026-09-05", "Done"),
        ("AI-04", "Draft User Story and Acceptance Criteria docs", 1, "Product Owner", "Medium", "2026-09-06", "Done"),
        ("AI-05", "Build physician directory with search query", 2, "Dev Team", "High", "2026-09-10", "Done"),
        ("AI-06", "Build doctor schedule slot generation utility", 2, "Yash Karwa", "High", "2026-09-11", "Done"),
        ("AI-07", "Populate mock specialist dataset", 2, "Dev Team", "Low", "2026-09-13", "Done"),
        ("AI-08", "Implement atomic booking transaction logic", 3, "Yash Karwa", "High", "2026-09-17", "Done"),
        ("AI-09", "Add defensive double-booking concurrency lock", 3, "Yash Karwa", "High", "2026-09-18", "Done"),
        ("AI-10", "Construct patient appointment history view", 3, "Dev Team", "Medium", "2026-09-20", "Done"),
        ("AI-11", "Build cancellation with automatic slot recovery", 4, "Dev Team", "High", "2026-09-24", "Done"),
        ("AI-12", "Engineer atomic slot swap algorithm for rescheduling", 4, "Yash Karwa", "High", "2026-09-26", "Done"),
        ("AI-13", "Implement built-in Scrum project management tables", 5, "Yash Karwa", "High", "2026-09-30", "Done"),
        ("AI-14", "Create interactive ASCII terminal Kanban board", 5, "Yash Karwa", "High", "2026-10-01", "Done"),
        ("AI-15", "Implement 15 automated unit tests with 100% pass", 5, "Yash Karwa", "High", "2026-10-02", "Done"),
        ("AI-16", "Prepare System Design and architecture diagrams", 5, "Dev Team", "Medium", "2026-10-03", "Done"),
        ("AI-17", "Conduct Sprint Review, Retrospective and Viva trial", 5, "Scrum Master", "High", "2026-10-04", "Done"),
        ("AI-18", "Push verified commits and docs to GitHub remote", 5, "Yash Karwa", "High", "2026-10-05", "Done"),
    ]
    cursor.executemany("""
        INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, action_items)

    # Seed a couple of initial sample appointments for patient Rohan Sharma
    cursor.execute("SELECT id FROM users WHERE username = 'rohan_s';")
    rohan_id = cursor.fetchone()["id"]
    cursor.execute("SELECT id, professional_id, date, start_time FROM availability WHERE is_booked = 0 LIMIT 2;")
    avail_rows = cursor.fetchall()

    if avail_rows:
        first_slot = avail_rows[0]
        cursor.execute("""
            INSERT INTO appointments (user_id, professional_id, availability_id, appointment_date, appointment_time, status, notes)
            VALUES (?, ?, ?, ?, ?, 'Confirmed', 'Routine cardiology consultation');
        """, (rohan_id, first_slot["professional_id"], first_slot["id"], first_slot["date"], first_slot["start_time"]))
        cursor.execute("UPDATE availability SET is_booked = 1 WHERE id = ?;", (first_slot["id"],))

    conn.commit()
    conn.close()
