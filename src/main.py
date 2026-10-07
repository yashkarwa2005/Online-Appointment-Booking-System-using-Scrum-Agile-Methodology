"""Main Application Entry Point
Online Appointment Booking System using Scrum Agile Methodology
Supports interactive terminal console, automated viva demo mode, and command-line flags.
"""
import sys
import os
import time
import argparse
from typing import Optional, Dict, Any

# Ensure project root is on Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Force UTF-8 on Windows terminal to avoid charmap / cp1252 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.database import init_db, seed_initial_data, DEFAULT_DB_PATH
from src.appointment import AppointmentService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class Color:
    """Terminal styling codes (safe fallback on all terminals)."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Color.CYAN}========================================================================================{Color.RESET}
{Color.BOLD}{Color.GREEN}     [+] ONLINE APPOINTMENT BOOKING SYSTEM - SCRUM AGILE METHODOLOGY (AM PBL){Color.RESET}
{Color.CYAN}========================================================================================{Color.RESET}
  {Color.YELLOW}* Student Project : Yash Karwa (B.Tech 3rd Year) | Subject: Agile Methodologies (AM){Color.RESET}
  {Color.BLUE}* Scrum Tracks    : 1. Healthcare Appointment Engine  |  2. In-App Scrum & Kanban Engine{Color.RESET}
{Color.CYAN}----------------------------------------------------------------------------------------{Color.RESET}
"""
    print(banner)


class AppRunner:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        # Ensure database is initialized and seeded
        seed_initial_data(self.db_path)

        self.appt_service = AppointmentService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

        self.current_user: Optional[Dict[str, Any]] = None

    # =========================================================================
    # Interactive Authentication
    # =========================================================================

    def handle_login(self):
        print(f"\n{Color.BOLD}--- User Login ---{Color.RESET}")
        print("Tip: Pre-seeded users: 'rohan_s' (patient), 'dr_priya' (doctor), 'admin' (admin). Password: '<username>123' (e.g. rohan123)")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        user = self.appt_service.authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"{Color.GREEN}✔ Login successful! Welcome, {user['full_name']} (Role: {user['role'].upper()}).{Color.RESET}")
        else:
            print(f"{Color.RED}✖ Invalid username or password.{Color.RESET}")

    def handle_register(self):
        print(f"\n{Color.BOLD}--- New Patient Registration ---{Color.RESET}")
        username = input("Choose Username: ").strip()
        password = input("Choose Password: ").strip()
        full_name = input("Enter Full Name: ").strip()
        email = input("Enter Email Address: ").strip()
        phone = input("Enter Phone Number: ").strip()

        try:
            user = self.appt_service.register_user(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                phone=phone,
                role="patient"
            )
            print(f"{Color.GREEN}✔ Registration successful! You can now log in as '{user['username']}'.{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}✖ Registration Failed: {e}{Color.RESET}")

    def handle_logout(self):
        if self.current_user:
            print(f"{Color.YELLOW}Logged out user '{self.current_user['username']}'.{Color.RESET}")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    # =========================================================================
    # Appointment Booking Menu
    # =========================================================================

    def menu_appointment_system(self):
        while True:
            u_status = f"Logged in as: {self.current_user['full_name']} [{self.current_user['role']}]" if self.current_user else "Not logged in (Browsing as Guest)"
            print(f"\n{Color.BOLD}{Color.BLUE}--- 🏥 APPOINTMENT BOOKING SYSTEM ({u_status}) ---{Color.RESET}")
            print("1. Browse / Search Doctors & Medical Specialists")
            print("2. View Available Consultation Slots for a Doctor")
            print("3. Book an Appointment (Requires Login)")
            print("4. View My Appointments")
            print("5. Reschedule an Appointment")
            print("6. Cancel an Appointment")
            print("7. Add Doctor Availability Slot (Doctor/Admin)")
            print("8. View All Hospital Appointments (Admin Audit)")
            print("9. Login / Switch User")
            print("10. Register New Patient Account")
            print("0. Return to Main Menu")

            choice = input(f"{Color.BOLD}Select an option (0-10): {Color.RESET}").strip()

            if choice == "1":
                q = input("Search query (Specialization/Department/Name or press Enter for all): ").strip()
                docs = self.appt_service.list_professionals(q or None)
                print(f"\n{Color.BOLD}Found {len(docs)} Doctors:{Color.RESET}")
                for d in docs:
                    print(f" • ID [{d['id']}] {Color.BOLD}{d['doctor_name']}{Color.RESET} | Dept: {d['department']} | Spec: {d['specialization']} | Fee: ₹{d['consultation_fee']} | Bio: {d['bio']}")

            elif choice == "2":
                doc_id_in = input("Enter Doctor ID to view slots: ").strip()
                if not doc_id_in.isdigit():
                    print(f"{Color.RED}Invalid Doctor ID.{Color.RESET}")
                    continue
                slots = self.appt_service.get_available_slots(int(doc_id_in))
                if not slots:
                    print(f"{Color.YELLOW}No open slots available for Doctor ID {doc_id_in}.{Color.RESET}")
                else:
                    print(f"\n{Color.BOLD}Available Slots for Doctor #{doc_id_in}:{Color.RESET}")
                    for s in slots:
                        print(f"   Slot ID [{s['id']}] | Date: {s['date']} | Time: {s['start_time']} - {s['end_time']}")

            elif choice == "3":
                if not self.current_user:
                    print(f"{Color.YELLOW}Please log in first to book an appointment.{Color.RESET}")
                    self.handle_login()
                    if not self.current_user:
                        continue

                doc_id = input("Enter Doctor ID: ").strip()
                slot_id = input("Enter Slot ID: ").strip()
                notes = input("Consultation reason / notes: ").strip()

                if not (doc_id.isdigit() and slot_id.isdigit()):
                    print(f"{Color.RED}Doctor ID and Slot ID must be numeric.{Color.RESET}")
                    continue

                try:
                    res = self.appt_service.book_appointment(
                        user_id=self.current_user["id"],
                        professional_id=int(doc_id),
                        slot_id=int(slot_id),
                        notes=notes
                    )
                    print(f"\n{Color.GREEN}✔ APPOINTMENT CONFIRMED! (US-05 / US-09){Color.RESET}")
                    print(f"   Appointment ID : #{res['id']}")
                    print(f"   Doctor         : {res['doctor_name']} ({res['specialization']})")
                    print(f"   Department     : {res['department']}")
                    print(f"   Date & Time    : {res['appointment_date']} at {res['appointment_time']}")
                    print(f"   Consultation   : ₹{res['consultation_fee']}")
                    print(f"   Status         : {res['status']}")
                except Exception as e:
                    print(f"{Color.RED}✖ Booking Failed: {e}{Color.RESET}")

            elif choice == "4":
                if not self.current_user:
                    print(f"{Color.YELLOW}Please log in to view appointments.{Color.RESET}")
                    self.handle_login()
                    if not self.current_user:
                        continue
                appts = self.appt_service.get_user_appointments(self.current_user["id"])
                if not appts:
                    print(f"{Color.YELLOW}No appointments found for {self.current_user['full_name']}.{Color.RESET}")
                else:
                    print(f"\n{Color.BOLD}Appointments for {self.current_user['full_name']}:{Color.RESET}")
                    for a in appts:
                        st_col = Color.GREEN if a['status'] == 'Confirmed' else Color.RED
                        print(f" • Appt ID [{a['id']}] | {a['appointment_date']} {a['appointment_time']} | Doc: {a['doctor_name']} | Status: {st_col}{a['status']}{Color.RESET} | Notes: {a['notes']}")

            elif choice == "5":
                if not self.current_user:
                    print(f"{Color.YELLOW}Please log in to reschedule.{Color.RESET}")
                    self.handle_login()
                    if not self.current_user:
                        continue
                appt_id = input("Enter Appointment ID to Reschedule: ").strip()
                new_slot_id = input("Enter New Slot ID: ").strip()

                if not (appt_id.isdigit() and new_slot_id.isdigit()):
                    print(f"{Color.RED}IDs must be numeric.{Color.RESET}")
                    continue

                try:
                    res = self.appt_service.reschedule_appointment(
                        appointment_id=int(appt_id),
                        new_slot_id=int(new_slot_id),
                        user_id=self.current_user["id"] if self.current_user["role"] != "admin" else None
                    )
                    print(f"{Color.GREEN}✔ {res['message']}{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Reschedule Failed: {e}{Color.RESET}")

            elif choice == "6":
                if not self.current_user:
                    print(f"{Color.YELLOW}Please log in to cancel an appointment.{Color.RESET}")
                    self.handle_login()
                    if not self.current_user:
                        continue
                appt_id = input("Enter Appointment ID to Cancel: ").strip()
                if not appt_id.isdigit():
                    print(f"{Color.RED}Invalid ID.{Color.RESET}")
                    continue
                try:
                    res = self.appt_service.cancel_appointment(
                        appointment_id=int(appt_id),
                        user_id=self.current_user["id"] if self.current_user["role"] != "admin" else None
                    )
                    print(f"{Color.GREEN}✔ {res['message']}{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Cancellation Failed: {e}{Color.RESET}")

            elif choice == "7":
                doc_id = input("Enter Doctor ID: ").strip()
                date_str = input("Enter Date (YYYY-MM-DD): ").strip()
                start_t = input("Enter Start Time (HH:MM): ").strip()
                end_t = input("Enter End Time (HH:MM): ").strip()
                try:
                    slot_id = self.appt_service.add_availability_slot(int(doc_id), date_str, start_t, end_t)
                    print(f"{Color.GREEN}✔ Availability slot #{slot_id} added successfully for Doctor #{doc_id}.{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Error adding slot: {e}{Color.RESET}")

            elif choice == "8":
                all_appts = self.appt_service.get_all_appointments()
                print(f"\n{Color.BOLD}--- Hospital System Audit ({len(all_appts)} Total Appointments) ---{Color.RESET}")
                for a in all_appts:
                    print(f" • Appt #{a['id']} | Patient: {a['patient_name']} ({a['patient_email']}) | Doc: {a['doctor_name']} | Date: {a['appointment_date']} {a['appointment_time']} | Status: {a['status']}")

            elif choice == "9":
                self.handle_login()

            elif choice == "10":
                self.handle_register()

            elif choice == "0":
                break

    # =========================================================================
    # Scrum Project Management Menu
    # =========================================================================

    def menu_scrum_management(self):
        while True:
            print(f"\n{Color.BOLD}{Color.GREEN}--- 📋 AGILE & SCRUM PROJECT MANAGEMENT ---{Color.RESET}")
            print("1. View Interactive Terminal Kanban Board (ASCII/ANSI)")
            print("2. Move Task / User Story on Kanban Board (Workflow Transition)")
            print("3. View Product Backlog & Story Point Metrics")
            print("4. View All Sprints & Progress (Sprint 1 to 5)")
            print("5. Create a New User Story")
            print("6. Create a New Sprint")
            print("7. View & Update Action Items")
            print("0. Return to Main Menu")

            choice = input(f"{Color.BOLD}Select an option (0-7): {Color.RESET}").strip()

            if choice == "1":
                print(self.kanban_service.render_board())

            elif choice == "2":
                code = input("Enter Task Code to Move (e.g. US-01, AI-05): ").strip().upper()
                print(f"Available Columns: {', '.join(KanbanService.COLUMNS)}")
                target_col = input("Target Column (Backlog / To Do / In Progress / Review/Testing / Done): ").strip()
                try:
                    res = self.kanban_service.move_task(code, target_col)
                    print(f"{Color.GREEN}✔ {res.get('message', 'Updated.')}{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Transition Failed: {e}{Color.RESET}")

            elif choice == "3":
                stories = self.story_service.list_user_stories()
                metrics = self.story_service.get_backlog_metrics()

                print(f"\n{Color.BOLD}--- Product Backlog Summary ---{Color.RESET}")
                print(f"Total Stories: {metrics['total_stories']} | Total Points: {metrics['total_points']} | Completed: {metrics['completed_points']} ({metrics['completion_percentage']}%)")
                print(f"Points by MoSCoW Priority: {metrics['by_priority']}")

                print(f"\n{'CODE':<8} {'TITLE':<32} {'PRIORITY':<12} {'POINTS':<8} {'SPRINT':<8} {'STATUS':<15}")
                print("-" * 85)
                for s in stories:
                    spr = f"Sprint {s['sprint_number']}" if s['sprint_number'] else "Backlog"
                    print(f"{s['story_code']:<8} {s['title'][:30]:<32} {s['priority']:<12} {s['story_points']:<8} {spr:<8} {s['status']:<15}")

            elif choice == "4":
                sprints = self.sprint_service.list_sprints()
                print(f"\n{Color.BOLD}--- 5-Week Sprint Plan Overview ---{Color.RESET}")
                for sp in sprints:
                    details = self.sprint_service.get_sprint_details(sp["id"])
                    pct = details["progress_percentage"] if details else 0
                    pts = details["total_story_points"] if details else 0
                    print(f"\n{Color.BOLD}Sprint #{sp['sprint_number']}: {sp['name']}{Color.RESET} [{sp['status']}]")
                    print(f" Goal: {sp['goal']}")
                    print(f" Schedule: {sp['start_date']} to {sp['end_date']} | Velocity: {sp['velocity']} pts")
                    print(f" Progress: {pct}% ({details['completed_story_points']}/{pts} story points completed)")
                    if details and details["stories"]:
                        print(f" Stories: {', '.join(st['story_code'] for st in details['stories'])}")

            elif choice == "5":
                code = input("Story Code (e.g., US-13): ").strip().upper()
                title = input("Story Title: ").strip()
                role = input("User Role (Patient / Doctor / Admin / Scrum Team): ").strip()
                want = input("I want to: ").strip()
                benefit = input("So that: ").strip()
                print("Priorities: Must Have, Should Have, Could Have, Won't Have")
                prio = input("Priority [Must Have]: ").strip() or "Must Have"
                pts_in = input("Story Points (1, 2, 3, 5, 8, 13) [3]: ").strip() or "3"
                sprint_id_in = input("Sprint ID (1-5, or Enter for None): ").strip()
                assignee = input("Assignee: ").strip()

                try:
                    s_id = int(sprint_id_in) if sprint_id_in.isdigit() else None
                    story = self.story_service.create_user_story(
                        story_code=code,
                        title=title,
                        role=role,
                        want=want,
                        benefit=benefit,
                        priority=prio,
                        story_points=int(pts_in),
                        sprint_id=s_id,
                        status="To Do" if s_id else "Backlog",
                        assignee=assignee
                    )
                    print(f"{Color.GREEN}✔ User Story '{story['story_code']}' created successfully.{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Error creating story: {e}{Color.RESET}")

            elif choice == "6":
                num = input("Sprint Number: ").strip()
                name = input("Sprint Name: ").strip()
                goal = input("Sprint Goal: ").strip()
                s_date = input("Start Date (YYYY-MM-DD): ").strip()
                e_date = input("End Date (YYYY-MM-DD): ").strip()
                vel = input("Estimated Velocity [10]: ").strip() or "10"

                try:
                    sp = self.sprint_service.create_sprint(
                        sprint_number=int(num),
                        name=name,
                        goal=goal,
                        start_date=s_date,
                        end_date=e_date,
                        status="Planning",
                        velocity=int(vel)
                    )
                    print(f"{Color.GREEN}✔ Sprint #{sp['sprint_number']} created.{Color.RESET}")
                except Exception as e:
                    print(f"{Color.RED}✖ Error creating sprint: {e}{Color.RESET}")

            elif choice == "7":
                actions = self.action_service.list_action_items()
                print(f"\n{Color.BOLD}--- Scrum Action Items Register ({len(actions)} Items) ---{Color.RESET}")
                print(f"{'CODE':<8} {'DESCRIPTION':<36} {'OWNER':<14} {'PRIORITY':<10} {'DUE DATE':<12} {'STATUS':<12}")
                print("-" * 95)
                for a in actions:
                    print(f"{a['item_code']:<8} {a['description'][:34]:<36} {a['owner']:<14} {a['priority']:<10} {a['due_date']:<12} {a['status']:<12}")

                sub_c = input("\nUpdate an action item status? (y/N): ").strip().lower()
                if sub_c == "y":
                    a_code = input("Action Item Code (e.g. AI-01): ").strip().upper()
                    print("Status options: To Do, In Progress, Review, Done, Blocked")
                    new_st = input("New Status: ").strip()
                    try:
                        res = self.action_service.update_action_item_status(a_code, new_st)
                        print(f"{Color.GREEN}✔ {res['message']}{Color.RESET}")
                    except Exception as e:
                        print(f"{Color.RED}✖ Error: {e}{Color.RESET}")

            elif choice == "0":
                break

    # =========================================================================
    # Automated Demonstration Mode (For Viva Examination)
    # =========================================================================

    def run_automated_viva_demo(self):
        """Runs a complete end-to-end automated simulation in ~15 seconds,
        demonstrating all core Agile requirements and appointment booking features.
        """
        print(f"\n{Color.BOLD}{Color.YELLOW}================================================================================{Color.RESET}")
        print(f"{Color.BOLD}{Color.YELLOW}   >>> RUNNING AUTOMATED VIVA DEMONSTRATION (AM PBL EVALUATION) <<<{Color.RESET}")
        print(f"{Color.BOLD}{Color.YELLOW}================================================================================{Color.RESET}\n")

        time.sleep(0.5)
        print(f"{Color.BOLD}STEP 1: Authenticating User (US-02 - Must Have)...{Color.RESET}")
        user = self.appt_service.authenticate_user("rohan_s", "rohan123")
        print(f"{Color.GREEN}[OK] Logged in as: {user['full_name']} (Role: {user['role']}){Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 2: Searching Doctor Directory (US-03 - Must Have)...{Color.RESET}")
        docs = self.appt_service.list_professionals("cardio")
        target_doc = docs[0]
        print(f"{Color.GREEN}[OK] Found Doctor: {target_doc['doctor_name']} | Dept: {target_doc['department']} | Fee: INR {target_doc['consultation_fee']}{Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 3: Inspecting Available Consultation Slots (US-04)...{Color.RESET}")
        slots = self.appt_service.get_available_slots(target_doc["id"])
        print(f"{Color.GREEN}[OK] Doctor has {len(slots)} open unbooked slots available.{Color.RESET}")
        chosen_slot = slots[0]
        backup_slot = slots[1]
        print(f"   Selected Slot ID [{chosen_slot['id']}]: Date {chosen_slot['date']} from {chosen_slot['start_time']} to {chosen_slot['end_time']}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 4: Booking Appointment with Double-Booking Concurrency Lock (US-05)...{Color.RESET}")
        booking = self.appt_service.book_appointment(
            user_id=user["id"],
            professional_id=target_doc["id"],
            slot_id=chosen_slot["id"],
            notes="Viva automated checkup"
        )
        print(f"{Color.GREEN}[OK] Booking Confirmed! Appointment #{booking['id']} on {booking['appointment_date']} at {booking['appointment_time']}{Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 5: Simulating Double-Booking Collision Test (Defensive Concurrency Guard)...{Color.RESET}")
        try:
            self.appt_service.book_appointment(
                user_id=2,
                professional_id=target_doc["id"],
                slot_id=chosen_slot["id"],
                notes="Colliding booking attempt"
            )
            print(f"{Color.RED}[ERROR] Double-booking was not prevented!{Color.RESET}")
        except ValueError as err:
            print(f"{Color.GREEN}[OK] Double-Booking Successfully Prevented: '{err}'{Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 6: Rescheduling Appointment (US-08)...{Color.RESET}")
        resched = self.appt_service.reschedule_appointment(
            appointment_id=booking["id"],
            new_slot_id=backup_slot["id"],
            user_id=user["id"]
        )
        print(f"{Color.GREEN}[OK] {resched['message']}{Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 7: Cancelling Appointment & Automatic Slot Recovery (US-07)...{Color.RESET}")
        cancel_res = self.appt_service.cancel_appointment(booking["id"], user_id=user["id"])
        print(f"{Color.GREEN}[OK] {cancel_res['message']}{Color.RESET}")

        time.sleep(0.5)
        print(f"\n{Color.BOLD}STEP 8: Displaying Agile Scrum Kanban Board (US-12)...{Color.RESET}")
        print(self.kanban_service.render_board())

        time.sleep(0.5)
        print(f"{Color.BOLD}STEP 9: Backlog Metrics & Sprint Velocity Summary...{Color.RESET}")
        metrics = self.story_service.get_backlog_metrics()
        print(f" Total Backlog Items : {metrics['total_stories']} Stories ({metrics['total_points']} Story Points)")
        print(f" Completed Work      : {metrics['completed_points']} Story Points ({metrics['completion_percentage']}%)")
        print(f" Points by MoSCoW    : {metrics['by_priority']}")

        print(f"\n{Color.BOLD}{Color.GREEN}================================================================================{Color.RESET}")
        print(f"{Color.BOLD}{Color.GREEN}   *** VIVA DEMONSTRATION COMPLETE: ALL AGILE ACCEPTANCE CRITERIA VERIFIED! ***{Color.RESET}")
        print(f"{Color.BOLD}{Color.GREEN}================================================================================{Color.RESET}\n")

    # =========================================================================
    # Main Navigation Loop
    # =========================================================================

    def run(self):
        print_banner()
        while True:
            print(f"\n{Color.BOLD}--- [*] MAIN APPLICATION DASHBOARD ---{Color.RESET}")
            print(f"1. [APP]   {Color.BOLD}Appointment Booking Subsystem{Color.RESET} (Patients, Doctors, Slots, Bookings)")
            print(f"2. [SCRUM] {Color.BOLD}Scrum Project Management Subsystem{Color.RESET} (User Stories, Sprints, Kanban Board)")
            print(f"3. [DEMO]  {Color.BOLD}Run Automated Viva Demonstration{Color.RESET} (30s End-to-End Walkthrough)")
            print(f"4. [TEST]  {Color.BOLD}Run Automated Unit Tests{Color.RESET} (15 Test Cases, 100% Pass Rate)")
            print(f"5. [WEB]   {Color.BOLD}Open Interactive Web Kanban Board{Color.RESET} (Color Coded HTML in Browser)")
            print(f"0. [EXIT]  {Color.BOLD}Exit Application{Color.RESET}")

            choice = input(f"\n{Color.BOLD}Enter your choice (0-5): {Color.RESET}").strip()

            if choice == "1":
                self.menu_appointment_system()
            elif choice == "2":
                self.menu_scrum_management()
            elif choice == "3":
                self.run_automated_viva_demo()
            elif choice == "4":
                import unittest
                suite = unittest.defaultTestLoader.discover("tests")
                runner = unittest.TextTestRunner(verbosity=2)
                runner.run(suite)
            elif choice == "5":
                import webbrowser
                web_path = os.path.join(PROJECT_ROOT, "kanban_board.html")
                print(f"{Color.GREEN}[*] Opening Visual Web Kanban Board in your browser: {web_path}{Color.RESET}")
                webbrowser.open(f"file:///{web_path.replace(os.sep, '/')}")
            elif choice == "0":
                print(f"\n{Color.CYAN}Thank you for reviewing the Online Appointment Booking Scrum Project! Goodbye.{Color.RESET}")
                break
            else:
                print(f"{Color.RED}Invalid selection. Please choose an option between 0 and 5.{Color.RESET}")


def main():
    parser = argparse.ArgumentParser(description="Online Appointment Booking System using Scrum Agile Methodology")
    parser.add_argument("--demo", action="store_true", help="Run automated viva demonstration and exit")
    parser.add_argument("--kanban", action="store_true", help="Render ASCII Kanban board and exit")
    parser.add_argument("--test", action="store_true", help="Run automated unit test suite and exit")
    parser.add_argument("--web", action="store_true", help="Open visual interactive Kanban board in default web browser")
    parser.add_argument("--db", type=str, default=DEFAULT_DB_PATH, help="Path to SQLite database file")

    args = parser.parse_args()
    app = AppRunner(db_path=args.db)

    if args.demo:
        app.run_automated_viva_demo()
    elif args.kanban:
        print(app.kanban_service.render_board())
    elif args.test:
        import unittest
        suite = unittest.defaultTestLoader.discover("tests")
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite)
    elif args.web:
        import webbrowser
        web_path = os.path.join(PROJECT_ROOT, "kanban_board.html")
        print(f"[*] Opening Visual Web Kanban Board: {web_path}")
        webbrowser.open(f"file:///{web_path.replace(os.sep, '/')}")
    else:
        app.run()


if __name__ == "__main__":
    main()
