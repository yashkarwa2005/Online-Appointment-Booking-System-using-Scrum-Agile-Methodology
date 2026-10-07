"""Appointment Service Module
Handles user registration, authentication, physician directory queries,
appointment booking with double-booking prevention, cancellation, and rescheduling.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection, hash_password


class AppointmentService:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    # =========================================================================
    # User Authentication & Management
    # =========================================================================

    def register_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: str,
        phone: str = "",
        role: str = "patient"
    ) -> Dict[str, Any]:
        """Registers a new user with salted SHA-256 hashed password.
        Raises ValueError if username/email already exists or inputs are invalid.
        """
        username = username.strip()
        email = email.strip()
        full_name = full_name.strip()

        if not username or not password or not full_name or not email:
            raise ValueError("All mandatory fields (username, password, full_name, email) must be provided.")

        if role not in ("patient", "doctor", "admin"):
            raise ValueError(f"Invalid role '{role}'. Allowed roles: patient, doctor, admin.")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Check unique constraints
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?;", (username, email))
        if cursor.fetchone():
            conn.close()
            raise ValueError(f"Username '{username}' or email '{email}' is already registered.")

        pw_hash = hash_password(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, full_name, email, phone, role)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (username, pw_hash, full_name, email, phone, role))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {
                "id": user_id,
                "username": username,
                "full_name": full_name,
                "email": email,
                "phone": phone,
                "role": role
            }
        except Exception as e:
            conn.close()
            raise ValueError(f"Registration failed: {str(e)}")

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Verifies credentials. Returns user dictionary if valid, None otherwise."""
        username = username.strip()
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password_hash, full_name, email, phone, role
            FROM users WHERE username = ?;
        """, (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        if hash_password(password) == row["password_hash"]:
            return {
                "id": row["id"],
                "username": row["username"],
                "full_name": row["full_name"],
                "email": row["email"],
                "phone": row["phone"],
                "role": row["role"]
            }
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Fetches user details by user ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, full_name, email, phone, role FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # =========================================================================
    # Healthcare Professionals & Schedules
    # =========================================================================

    def list_professionals(self, search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lists registered medical professionals with optional filter by name, specialization, or department."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT p.id, p.user_id, u.full_name AS doctor_name, u.email, u.phone,
                   p.specialization, p.department, p.consultation_fee, p.bio
            FROM professionals p
            JOIN users u ON p.user_id = u.id
        """
        params = []
        if search_query and search_query.strip():
            q = f"%{search_query.strip()}%"
            sql += """
                WHERE u.full_name LIKE ?
                   OR p.specialization LIKE ?
                   OR p.department LIKE ?
            """
            params.extend([q, q, q])

        sql += " ORDER BY p.department, u.full_name ASC;"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_professional_by_id(self, prof_id: int) -> Optional[Dict[str, Any]]:
        """Fetches single doctor profile with professional ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.user_id, u.full_name AS doctor_name, u.email, u.phone,
                   p.specialization, p.department, p.consultation_fee, p.bio
            FROM professionals p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = ?;
        """, (prof_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def add_availability_slot(
        self,
        professional_id: int,
        date: str,
        start_time: str,
        end_time: str
    ) -> int:
        """Adds a consultation time slot for a doctor. Returns new slot ID."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        # Validate doctor exists
        cursor.execute("SELECT id FROM professionals WHERE id = ?;", (professional_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"Professional with ID {professional_id} does not exist.")

        cursor.execute("""
            INSERT INTO availability (professional_id, date, start_time, end_time, is_booked)
            VALUES (?, ?, ?, ?, 0);
        """, (professional_id, date.strip(), start_time.strip(), end_time.strip()))
        conn.commit()
        slot_id = cursor.lastrowid
        conn.close()
        return slot_id

    def get_available_slots(self, professional_id: int, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all open, unbooked consultation slots for a given doctor."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT id, professional_id, date, start_time, end_time, is_booked
            FROM availability
            WHERE professional_id = ? AND is_booked = 0
        """
        params = [professional_id]
        if date and date.strip():
            sql += " AND date = ?"
            params.append(date.strip())

        sql += " ORDER BY date, start_time ASC;"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # =========================================================================
    # Appointment Booking, Cancellation & Rescheduling
    # =========================================================================

    def book_appointment(
        self,
        user_id: int,
        professional_id: int,
        slot_id: int,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Atomically reserves an appointment slot and locks the slot to prevent double-booking.
        Raises ValueError if the slot is invalid, does not belong to the doctor, or is already booked.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            # Atomic lock check inside transaction
            cursor.execute("""
                SELECT id, professional_id, date, start_time, end_time, is_booked
                FROM availability
                WHERE id = ?;
            """, (slot_id,))
            slot = cursor.fetchone()

            if not slot:
                raise ValueError(f"Slot ID {slot_id} not found.")

            if slot["professional_id"] != professional_id:
                raise ValueError(f"Slot ID {slot_id} does not belong to professional ID {professional_id}.")

            if slot["is_booked"] != 0:
                raise ValueError(f"Slot ID {slot_id} on {slot['date']} at {slot['start_time']} is already booked.")

            # Mark slot as booked
            cursor.execute("UPDATE availability SET is_booked = 1 WHERE id = ?;", (slot_id,))

            # Create appointment record
            cursor.execute("""
                INSERT INTO appointments (
                    user_id, professional_id, availability_id, appointment_date, appointment_time, status, notes
                ) VALUES (?, ?, ?, ?, ?, 'Confirmed', ?);
            """, (user_id, professional_id, slot_id, slot["date"], slot["start_time"], notes.strip()))

            appt_id = cursor.lastrowid
            conn.commit()

            # Retrieve doctor details for complete receipt
            cursor.execute("""
                SELECT u.full_name AS doctor_name, p.specialization, p.department, p.consultation_fee
                FROM professionals p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = ?;
            """, (professional_id,))
            doc_row = cursor.fetchone()

            return {
                "id": appt_id,
                "appointment_id": appt_id,
                "user_id": user_id,
                "professional_id": professional_id,
                "doctor_name": doc_row["doctor_name"] if doc_row else "Doctor",
                "specialization": doc_row["specialization"] if doc_row else "",
                "department": doc_row["department"] if doc_row else "",
                "consultation_fee": doc_row["consultation_fee"] if doc_row else 0.0,
                "availability_id": slot_id,
                "appointment_date": slot["date"],
                "appointment_time": slot["start_time"],
                "status": "Confirmed",
                "notes": notes.strip()
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def cancel_appointment(self, appointment_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Cancels an active appointment and atomically releases the reserved availability slot.
        Raises ValueError if appointment is not found or already cancelled.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, user_id, availability_id, appointment_date, appointment_time, status
                FROM appointments WHERE id = ?;
            """, (appointment_id,))
            appt = cursor.fetchone()

            if not appt:
                raise ValueError(f"Appointment ID {appointment_id} does not exist.")

            if user_id is not None and appt["user_id"] != user_id:
                raise ValueError("Unauthorized: You can only cancel your own appointments.")

            if appt["status"] == "Cancelled":
                raise ValueError(f"Appointment ID {appointment_id} is already cancelled.")

            # Update appointment status
            cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE id = ?;", (appointment_id,))

            # Release availability slot
            if appt["availability_id"]:
                cursor.execute("UPDATE availability SET is_booked = 0 WHERE id = ?;", (appt["availability_id"],))

            conn.commit()
            return {
                "id": appt["id"],
                "status": "Cancelled",
                "message": f"Appointment #{appointment_id} successfully cancelled. Slot released."
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def reschedule_appointment(
        self,
        appointment_id: int,
        new_slot_id: int,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Atomically swaps slots: releases old slot, reserves new slot, and updates appointment."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, user_id, professional_id, availability_id, status
                FROM appointments WHERE id = ?;
            """, (appointment_id,))
            appt = cursor.fetchone()

            if not appt:
                raise ValueError(f"Appointment ID {appointment_id} not found.")

            if user_id is not None and appt["user_id"] != user_id:
                raise ValueError("Unauthorized: You can only reschedule your own appointments.")

            if appt["status"] != "Confirmed":
                raise ValueError(f"Cannot reschedule an appointment with status '{appt['status']}'.")

            old_slot_id = appt["availability_id"]
            prof_id = appt["professional_id"]

            # Inspect new slot
            cursor.execute("""
                SELECT id, professional_id, date, start_time, is_booked
                FROM availability WHERE id = ?;
            """, (new_slot_id,))
            new_slot = cursor.fetchone()

            if not new_slot:
                raise ValueError(f"Target slot ID {new_slot_id} does not exist.")

            if new_slot["professional_id"] != prof_id:
                raise ValueError("Rescheduling must be with the same healthcare professional.")

            if new_slot["is_booked"] != 0:
                raise ValueError(f"Target slot on {new_slot['date']} at {new_slot['start_time']} is already booked.")

            # Release old slot
            cursor.execute("UPDATE availability SET is_booked = 0 WHERE id = ?;", (old_slot_id,))

            # Reserve new slot
            cursor.execute("UPDATE availability SET is_booked = 1 WHERE id = ?;", (new_slot_id,))

            # Update appointment
            cursor.execute("""
                UPDATE appointments
                SET availability_id = ?, appointment_date = ?, appointment_time = ?
                WHERE id = ?;
            """, (new_slot_id, new_slot["date"], new_slot["start_time"], appointment_id))

            conn.commit()
            return {
                "id": appointment_id,
                "status": "Confirmed",
                "new_date": new_slot["date"],
                "new_time": new_slot["start_time"],
                "message": f"Appointment #{appointment_id} rescheduled to {new_slot['date']} at {new_slot['start_time']}."
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_user_appointments(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieves all appointments for a patient."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.id, a.professional_id, u.full_name AS doctor_name, p.specialization,
                   p.department, p.consultation_fee, a.appointment_date, a.appointment_time,
                   a.status, a.notes, a.created_at
            FROM appointments a
            JOIN professionals p ON a.professional_id = p.id
            JOIN users u ON p.user_id = u.id
            WHERE a.user_id = ?
            ORDER BY a.appointment_date DESC, a.appointment_time DESC;
        """, (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        """Admin audit view: Retrieves all appointments across all patients and doctors."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT a.id, a.user_id, pat.full_name AS patient_name, pat.email AS patient_email,
                   a.professional_id, doc.full_name AS doctor_name, p.specialization,
                   a.appointment_date, a.appointment_time, a.status, a.notes, a.created_at
            FROM appointments a
            JOIN users pat ON a.user_id = pat.id
            JOIN professionals p ON a.professional_id = p.id
            JOIN users doc ON p.user_id = doc.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC;
        """, ())
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
