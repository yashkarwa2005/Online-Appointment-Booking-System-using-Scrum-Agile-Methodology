"""MediFlow · Online Appointment Booking System (AM & ITL Lab Project)
Standalone Python Web Application with Embedded REST API & Responsive Dashboard.
Zero mandatory external dependencies - uses standard library http.server + sqlite3.
"""
import os
import sys
import json
import sqlite3
import urllib.parse
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading
import time

# Add root directory to sys.path so src imports work cleanly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from src.database import get_connection, seed_initial_data
    from src.appointment import AppointmentService
except ImportError:
    # If running inside Online_Appointment_Booking_System_ITL_Lab
    from src.database import get_connection, seed_initial_data
    from src.appointment import AppointmentService

DEFAULT_PORT = 5000


def ensure_audit_table():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL,
        user_id INTEGER,
        user_name TEXT,
        details TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    c.execute("SELECT COUNT(*) FROM audit_logs;")
    if c.fetchone()[0] == 0:
        sample_logs = [
            ("SYSTEM_INIT", 1, "System Administrator", "Database schema initialized with SQLite foreign key enforcement."),
            ("SEED_DATA", 1, "System Administrator", "Initial 3 specialists, 45 availability slots, and 15 Agile User Stories populated."),
            ("SLOT_LOCK_CHECK", 5, "Rohan Sharma", "Concurrency lock validated for Dr. Priya Verma Cardiology slot.")
        ]
        c.executemany("INSERT INTO audit_logs (action_type, user_id, user_name, details) VALUES (?, ?, ?, ?);", sample_logs)
        conn.commit()
    conn.close()


def log_audit(action_type: str, user_id: int, user_name: str, details: str):
    try:
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO audit_logs (action_type, user_id, user_name, details)
            VALUES (?, ?, ?, ?);
        """, (action_type, user_id, user_name, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] Audit log error: {e}")


class MediFlowRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def send_json(self, data, status_code=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status_code=400):
        self.send_json({"error": message}, status_code=status_code)

    def parse_body(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            return {}
        raw = self.rfile.read(content_len).decode("utf-8")
        try:
            return json.loads(raw)
        except Exception:
            return urllib.parse.parse_qs(raw)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        # 1. Frontend Homepage
        if path == "/" or path == "/index.html":
            template_path = os.path.join(BASE_DIR, "templates", "index.html")
            if not os.path.exists(template_path):
                # Fallback to parent directory if in subfolder
                template_path = os.path.join(os.path.dirname(BASE_DIR), "templates", "index.html")

            if os.path.exists(template_path):
                with open(template_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Template index.html not found")
                return

        # 2. API: Users
        if path == "/api/users":
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT id, username, full_name, email, phone, role FROM users ORDER BY id ASC;")
            users = [dict(r) for r in c.fetchall()]
            conn.close()
            self.send_json(users)
            return

        # 3. API: Doctors
        if path == "/api/doctors":
            svc = AppointmentService()
            docs = svc.list_professionals()
            self.send_json(docs)
            return

        # 4. API: Doctor Available Slots
        if path == "/api/slots":
            doctor_id = query.get("doctor_id", [None])[0]
            date = query.get("date", [None])[0]
            if not doctor_id:
                self.send_error_json("doctor_id is required")
                return
            svc = AppointmentService()
            slots = svc.get_available_slots(int(doctor_id), date=date)
            self.send_json(slots)
            return

        # 5. API: Patient Appointments
        if path == "/api/appointments/patient":
            user_id = query.get("user_id", [None])[0]
            if not user_id:
                self.send_error_json("user_id is required")
                return
            svc = AppointmentService()
            appts = svc.get_user_appointments(int(user_id))
            self.send_json(appts)
            return

        # 6. API: Doctor Consultations Queue
        if path == "/api/appointments/doctor":
            doc_id = query.get("doctor_id", [None])[0]
            if not doc_id:
                self.send_error_json("doctor_id is required")
                return
            svc = AppointmentService()
            appts = svc.get_doctor_appointments(int(doc_id))
            self.send_json(appts)
            return

        # 7. API: Admin Analytics KPIs
        if path == "/api/admin/stats":
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT COUNT(*) FROM users WHERE role = 'patient';")
            pat_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM professionals;")
            doc_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM appointments WHERE status = 'Confirmed';")
            conf_count = c.fetchone()[0]
            c.execute("""
                SELECT COALESCE(SUM(p.consultation_fee), 0)
                FROM appointments a
                JOIN professionals p ON a.professional_id = p.id
                WHERE a.status IN ('Confirmed', 'Completed');
            """)
            rev = c.fetchone()[0]
            conn.close()
            self.send_json({
                "patients_count": pat_count,
                "doctors_count": doc_count,
                "confirmed_appointments": conf_count,
                "total_revenue": rev
            })
            return

        # 8. API: Audit Logs
        if path == "/api/admin/audit_logs":
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM audit_logs ORDER BY id DESC LIMIT 50;")
            logs = [dict(r) for r in c.fetchall()]
            conn.close()
            self.send_json(logs)
            return

        # 9. API: Kanban Stories
        if path == "/api/scrum/kanban":
            conn = get_connection()
            c = conn.cursor()
            c.execute("SELECT * FROM user_stories ORDER BY id ASC;")
            stories = [dict(r) for r in c.fetchall()]
            conn.close()
            # Group by status
            board = {
                "Backlog": [],
                "To Do": [],
                "In Progress": [],
                "Review/Testing": [],
                "Done": []
            }
            for s in stories:
                st = s.get("status", "Backlog")
                if st in board:
                    board[st].append(s)
                else:
                    board["Backlog"].append(s)
            self.send_json(board)
            return

        self.send_error(404, "Endpoint not found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_body()

        # 1. Book Appointment
        if path == "/api/appointments/book":
            user_id = body.get("user_id")
            prof_id = body.get("professional_id")
            slot_id = body.get("slot_id")
            notes = body.get("notes", "")

            if not (user_id and prof_id and slot_id):
                self.send_error_json("Missing mandatory booking parameters")
                return

            try:
                svc = AppointmentService()
                appt = svc.book_appointment(int(user_id), int(prof_id), int(slot_id), notes=notes)
                u = svc.get_user_by_id(int(user_id))
                user_name = u["full_name"] if u else f"User #{user_id}"
                appt_id = appt.get("appointment_id") or appt.get("id", "N/A")
                doc_name = appt.get("doctor_name", "Doctor")
                appt_date = appt.get("appointment_date", "")
                appt_time = appt.get("appointment_time", "")
                log_audit("APPOINTMENT_BOOKED", int(user_id), user_name,
                          f"Booked appointment #{appt_id} with {doc_name} on {appt_date} at {appt_time}.")
                self.send_json(appt, status_code=201)
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        # 2. Cancel Appointment & Free Slot
        if path == "/api/appointments/cancel":
            appt_id = body.get("appointment_id")
            if not appt_id:
                self.send_error_json("appointment_id is required")
                return
            try:
                svc = AppointmentService()
                res = svc.cancel_appointment(int(appt_id))
                log_audit("APPOINTMENT_CANCELLED", 0, "Patient/Admin",
                          f"Cancelled appointment #{appt_id}. Availability slot was atomically freed.")
                self.send_json(res)
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        # 3. Reschedule Appointment
        if path == "/api/appointments/reschedule":
            appt_id = body.get("appointment_id")
            new_slot_id = body.get("new_slot_id")
            if not (appt_id and new_slot_id):
                self.send_error_json("appointment_id and new_slot_id required")
                return
            try:
                svc = AppointmentService()
                res = svc.reschedule_appointment(int(appt_id), int(new_slot_id))
                log_audit("APPOINTMENT_RESCHEDULED", 0, "Patient",
                          f"Rescheduled appointment #{appt_id} to new slot #{new_slot_id}.")
                self.send_json(res)
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        # 4. Doctor Adds Availability Slot
        if path == "/api/doctor/add_slot":
            prof_id = body.get("professional_id")
            date = body.get("date")
            start = body.get("start_time")
            end = body.get("end_time")
            if not (prof_id and date and start and end):
                self.send_error_json("Missing slot creation fields")
                return
            try:
                svc = AppointmentService()
                slot_id = svc.add_availability_slot(int(prof_id), date, start, end)
                log_audit("SLOT_CREATED", int(prof_id), "Doctor",
                          f"Doctor #{prof_id} published new slot #{slot_id} on {date} ({start}-{end}).")
                self.send_json({"slot_id": slot_id, "status": "Created"})
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        # 5. Doctor Marks Consultation Completed
        if path == "/api/doctor/complete":
            appt_id = body.get("appointment_id")
            if not appt_id:
                self.send_error_json("appointment_id required")
                return
            try:
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE appointments SET status = 'Completed' WHERE id = ?;", (int(appt_id),))
                conn.commit()
                conn.close()
                log_audit("APPOINTMENT_COMPLETED", 0, "Doctor", f"Marked consultation #{appt_id} as Completed.")
                self.send_json({"status": "Completed"})
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        # 6. Move Kanban Story
        if path == "/api/scrum/move_story":
            code = body.get("story_code")
            new_status = body.get("status")
            if not (code and new_status):
                self.send_error_json("story_code and status required")
                return
            try:
                conn = get_connection()
                c = conn.cursor()
                c.execute("UPDATE user_stories SET status = ? WHERE story_code = ?;", (new_status, code))
                conn.commit()
                conn.close()
                log_audit("KANBAN_MOVE", 0, "Scrum Team", f"Moved story {code} to '{new_status}' stage.")
                self.send_json({"status": "Updated", "story_code": code, "new_status": new_status})
            except Exception as e:
                self.send_error_json(str(e), status_code=400)
            return

        self.send_error(404, "Endpoint not found")


def open_browser_delayed(url):
    time.sleep(1.2)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def start_server(port=DEFAULT_PORT):
    seed_initial_data()
    ensure_audit_table()

    # Find open port if 5000 is occupied
    server = None
    for p in [port, 5001, 8080, 8000]:
        try:
            server = ThreadingHTTPServer(("127.0.0.1", p), MediFlowRequestHandler)
            port = p
            break
        except OSError:
            continue

    if not server:
        print("[-] Could not bind to any test port (5000, 5001, 8080, 8000).")
        sys.exit(1)

    url = f"http://127.0.0.1:{port}"
    print("=" * 72)
    print(" [MEDIFLOW] ONLINE APPOINTMENT BOOKING SYSTEM")
    print(" Agile Scrum PBL & ITL Lab Evaluation Server")
    print("=" * 72)
    print(f" [+] SQLite Database Connected: Active Concurrency Guard (ACID)")
    print(f" [+] Scrum Engine: 15 User Stories, 5 Sprints, Velocity: 54 pts")
    print(f" [+] Web Dashboard URL: {url}")
    print(" [+] Opening dashboard automatically in your browser...")
    print("=" * 72)
    print(" Press Ctrl+C in this terminal anytime to stop the server.")
    print("=" * 72)

    threading.Thread(target=open_browser_delayed, args=(url,), daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping MediFlow server cleanly. Goodbye!")
        server.server_close()


if __name__ == "__main__":
    start_server()
