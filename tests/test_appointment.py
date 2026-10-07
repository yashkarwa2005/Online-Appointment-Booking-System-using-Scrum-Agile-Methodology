"""Comprehensive Test Suite for Online Appointment Booking System
Covers Authentication, Scheduling, Concurrency Guard, Cancellation, Rescheduling,
Scrum Story Backlog, Sprint Lifecycles, and Kanban Board.
"""
import os
import unittest
import tempfile
from src.database import init_db, seed_initial_data, get_connection
from src.appointment import AppointmentService
from src.user_story import UserStoryService
from src.sprint import SprintService
from src.action_item import ActionItemService
from src.kanban import KanbanService


class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        """Creates an isolated temporary SQLite database for each test case."""
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_file.close()
        self.db_path = self.temp_file.name
        seed_initial_data(self.db_path)

        self.appt_service = AppointmentService(self.db_path)
        self.story_service = UserStoryService(self.db_path)
        self.sprint_service = SprintService(self.db_path)
        self.action_service = ActionItemService(self.db_path)
        self.kanban_service = KanbanService(self.db_path)

    def tearDown(self):
        """Cleans up temporary database file after test completion."""
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    # =========================================================================
    # TC-01 & TC-02: User Registration Tests
    # =========================================================================

    def test_tc01_user_registration_success(self):
        """TC-01: Verify successful user registration with valid new credentials."""
        user = self.appt_service.register_user(
            username="rajesh_k",
            password="SecurePass@123",
            full_name="Rajesh Kumar",
            email="rajesh.kumar@example.com",
            phone="9811122233",
            role="patient"
        )
        self.assertIsNotNone(user["id"])
        self.assertEqual(user["username"], "rajesh_k")
        self.assertEqual(user["role"], "patient")

    def test_tc02_duplicate_user_registration_rejection(self):
        """TC-02: Verify duplicate username registration is rejected."""
        with self.assertRaises(ValueError):
            self.appt_service.register_user(
                username="rohan_s",  # Already in seed data
                password="AnotherPassword",
                full_name="Duplicate Rohan",
                email="different.email@example.com",
                role="patient"
            )

    # =========================================================================
    # TC-03 & TC-04: User Authentication Tests
    # =========================================================================

    def test_tc03_user_login_success(self):
        """TC-03: Verify successful login with correct username and password."""
        user = self.appt_service.authenticate_user("rohan_s", "rohan123")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "rohan_s")
        self.assertEqual(user["role"], "patient")

    def test_tc04_user_login_invalid_password(self):
        """TC-04: Verify login fails on invalid credentials."""
        user = self.appt_service.authenticate_user("rohan_s", "WrongPassword!")
        self.assertIsNone(user)

    # =========================================================================
    # TC-05 & TC-06: Doctor Directory & Availability Queries
    # =========================================================================

    def test_tc05_search_doctors_by_specialization(self):
        """TC-05: Verify search for doctors by specialization."""
        cardio_docs = self.appt_service.list_professionals(search_query="cardio")
        self.assertTrue(len(cardio_docs) >= 1)
        self.assertIn("Cardiology", cardio_docs[0]["specialization"])

    def test_tc06_query_available_slots(self):
        """TC-06: Verify querying open, unbooked slots for a doctor."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        slots = self.appt_service.get_available_slots(doc_id)
        self.assertTrue(len(slots) > 0)
        for s in slots:
            self.assertEqual(s["is_booked"], 0)

    # =========================================================================
    # TC-07 & TC-08: Appointment Booking & Concurrency Guard
    # =========================================================================

    def test_tc07_book_appointment_success(self):
        """TC-07: Verify booking an open slot succeeds and locks the slot."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        slots = self.appt_service.get_available_slots(doc_id)
        target_slot = slots[0]

        booking = self.appt_service.book_appointment(
            user_id=1,
            professional_id=doc_id,
            slot_id=target_slot["id"],
            notes="Comprehensive heart health checkup"
        )
        self.assertIsNotNone(booking["id"])
        self.assertEqual(booking["status"], "Confirmed")

        # Verify slot is marked booked
        updated_slots = self.appt_service.get_available_slots(doc_id)
        slot_ids = [s["id"] for s in updated_slots]
        self.assertNotIn(target_slot["id"], slot_ids)

    def test_tc08_prevent_double_booking(self):
        """TC-08: Verify double-booking prevention raises conflict error."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        slots = self.appt_service.get_available_slots(doc_id)
        target_slot = slots[0]

        # First booking succeeds
        self.appt_service.book_appointment(
            user_id=1,
            professional_id=doc_id,
            slot_id=target_slot["id"],
            notes="First patient booking"
        )

        # Second booking on the exact same slot must raise ValueError
        with self.assertRaises(ValueError) as ctx:
            self.appt_service.book_appointment(
                user_id=2,
                professional_id=doc_id,
                slot_id=target_slot["id"],
                notes="Second patient booking attempt"
            )
        self.assertIn("already booked", str(ctx.exception).lower())

    # =========================================================================
    # TC-09, TC-10, TC-11: Appointment History, Cancellation & Rescheduling
    # =========================================================================

    def test_tc09_retrieve_appointment_history(self):
        """TC-09: Verify patient appointment history retrieves active bookings."""
        user = self.appt_service.authenticate_user("rohan_s", "rohan123")
        history = self.appt_service.get_user_appointments(user["id"])
        self.assertTrue(len(history) >= 1)
        self.assertEqual(history[0]["status"], "Confirmed")

    def test_tc10_cancel_appointment_and_release_slot(self):
        """TC-10: Verify cancelling appointment updates status and releases slot."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        slots = self.appt_service.get_available_slots(doc_id)
        target_slot = slots[0]

        # Book slot
        booking = self.appt_service.book_appointment(
            user_id=1,
            professional_id=doc_id,
            slot_id=target_slot["id"],
            notes="To be cancelled"
        )
        appt_id = booking["id"]

        # Cancel
        res = self.appt_service.cancel_appointment(appt_id, user_id=1)
        self.assertEqual(res["status"], "Cancelled")

        # Verify slot is unbooked again
        available = self.appt_service.get_available_slots(doc_id)
        self.assertIn(target_slot["id"], [s["id"] for s in available])

    def test_tc11_reschedule_appointment(self):
        """TC-11: Verify rescheduling swaps old slot for new slot atomically."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        slots = self.appt_service.get_available_slots(doc_id)
        slot1 = slots[0]
        slot2 = slots[1]

        # Book slot 1
        booking = self.appt_service.book_appointment(
            user_id=1,
            professional_id=doc_id,
            slot_id=slot1["id"],
            notes="Initial booking"
        )
        appt_id = booking["id"]

        # Reschedule to slot 2
        resched = self.appt_service.reschedule_appointment(appt_id, slot2["id"], user_id=1)
        self.assertEqual(resched["status"], "Confirmed")
        self.assertEqual(resched["new_date"], slot2["date"])

        # Check slot 1 is freed and slot 2 is booked
        available = self.appt_service.get_available_slots(doc_id)
        avail_ids = [s["id"] for s in available]
        self.assertIn(slot1["id"], avail_ids)
        self.assertNotIn(slot2["id"], avail_ids)

    # =========================================================================
    # TC-12 & TC-13: Doctor Slot Management & Admin Audit
    # =========================================================================

    def test_tc12_doctor_add_availability_slot(self):
        """TC-12: Verify doctor can add new consultation slot."""
        docs = self.appt_service.list_professionals()
        doc_id = docs[0]["id"]
        new_slot_id = self.appt_service.add_availability_slot(
            professional_id=doc_id,
            date="2026-11-01",
            start_time="16:00",
            end_time="16:30"
        )
        self.assertIsNotNone(new_slot_id)
        slots = self.appt_service.get_available_slots(doc_id, date="2026-11-01")
        self.assertTrue(any(s["id"] == new_slot_id for s in slots))

    def test_tc13_admin_view_all_appointments(self):
        """TC-13: Verify admin can query all hospital appointments."""
        all_appts = self.appt_service.get_all_appointments()
        self.assertTrue(len(all_appts) >= 1)
        self.assertIn("patient_name", all_appts[0])
        self.assertIn("doctor_name", all_appts[0])

    # =========================================================================
    # TC-14 & TC-15: Scrum Story, Sprint & Kanban Management
    # =========================================================================

    def test_tc14_create_user_story_and_metrics(self):
        """TC-14: Verify user story creation, priority validation, and backlog metrics."""
        story = self.story_service.create_user_story(
            story_code="US-TEST",
            title="Telemedicine Video Call",
            role="Patient",
            want="connect via video stream",
            benefit="consult doctor remotely",
            priority="Could Have",
            story_points=5,
            sprint_id=5,
            status="Backlog",
            assignee="Yash Karwa",
            description="WebRTC audio video stream"
        )
        self.assertEqual(story["story_code"], "US-TEST")
        self.assertEqual(story["story_points"], 5)

        # Retrieve and verify metrics
        metrics = self.story_service.get_backlog_metrics()
        self.assertTrue(metrics["total_stories"] > 12)
        self.assertTrue(metrics["total_points"] >= 50)

    def test_tc15_kanban_transition_and_sprint_lifecycle(self):
        """TC-15: Verify moving cards across Kanban workflow and sprint progress."""
        # Create a new sprint
        sprint = self.sprint_service.create_sprint(
            sprint_number=6,
            name="Sprint 6: Future Roadmap",
            goal="Add international payment gateway",
            start_date="2026-10-10",
            end_date="2026-10-17",
            status="Planning",
            velocity=10
        )
        self.assertEqual(sprint["sprint_number"], 6)

        # Transition sprint to Active
        updated_sprint = self.sprint_service.update_sprint_status(sprint["id"], "Active")
        self.assertEqual(updated_sprint["status"], "Active")

        # Move a story on Kanban board to "In Progress" then "Done"
        self.kanban_service.move_task("US-01", "In Progress")
        story = self.story_service.get_user_story("US-01")
        self.assertEqual(story["status"], "In Progress")

        self.kanban_service.move_task("US-01", "Done")
        story_done = self.story_service.get_user_story("US-01")
        self.assertEqual(story_done["status"], "Done")

        # Test Kanban board ASCII rendering
        board_text = self.kanban_service.render_board(show_all=False)
        self.assertIn("AGILE SCRUM KANBAN BOARD", board_text)
        self.assertIn("DONE", board_text)


if __name__ == "__main__":
    unittest.main()
