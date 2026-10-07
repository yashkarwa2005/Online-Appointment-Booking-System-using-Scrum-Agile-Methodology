"""Sprint Management Module for Scrum Lifecycle
Handles Sprint planning, activation, completion, velocity tracking, and progress metrics.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class SprintService:
    VALID_STATUSES = ("Planning", "Active", "Completed")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_sprint(
        self,
        sprint_number: int,
        name: str,
        goal: str,
        start_date: str,
        end_date: str,
        status: str = "Planning",
        velocity: int = 0
    ) -> Dict[str, Any]:
        """Creates a new Sprint iteration in the Scrum schedule."""
        name = name.strip()
        goal = goal.strip()

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sprints (sprint_number, name, goal, start_date, end_date, status, velocity)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (sprint_number, name, goal, start_date.strip(), end_date.strip(), status, velocity))
            conn.commit()
            sprint_id = cursor.lastrowid
            return {
                "id": sprint_id,
                "sprint_number": sprint_number,
                "name": name,
                "goal": goal,
                "start_date": start_date,
                "end_date": end_date,
                "status": status,
                "velocity": velocity
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Sprint #{sprint_number} already exists.")
        finally:
            conn.close()

    def update_sprint_status(self, sprint_id: int, new_status: str) -> Dict[str, Any]:
        """Transitions sprint lifecycle state (Planning -> Active -> Completed)."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM sprints WHERE id = ?;", (sprint_id,))
        sprint = cursor.fetchone()
        if not sprint:
            conn.close()
            raise ValueError(f"Sprint with ID {sprint_id} does not exist.")

        cursor.execute("UPDATE sprints SET status = ? WHERE id = ?;", (new_status, sprint_id))
        conn.commit()
        conn.close()
        return {"id": sprint_id, "name": sprint["name"], "status": new_status}

    def list_sprints(self) -> List[Dict[str, Any]]:
        """Lists all sprints in chronological iteration order."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sprints ORDER BY sprint_number ASC;")
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_sprint_details(self, sprint_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves comprehensive sprint information including assigned stories and action items."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sprints WHERE id = ?;", (sprint_id,))
        sprint_row = cursor.fetchone()
        if not sprint_row:
            conn.close()
            return None

        sprint_dict = dict(sprint_row)

        # Assigned User Stories
        cursor.execute("SELECT * FROM user_stories WHERE sprint_id = ? ORDER BY id ASC;", (sprint_id,))
        stories = [dict(r) for r in cursor.fetchall()]

        # Assigned Action Items
        cursor.execute("SELECT * FROM action_items WHERE sprint_id = ? ORDER BY id ASC;", (sprint_id,))
        action_items = [dict(r) for r in cursor.fetchall()]

        conn.close()

        total_pts = sum(s["story_points"] for s in stories)
        done_pts = sum(s["story_points"] for s in stories if s["status"] == "Done")

        sprint_dict["stories"] = stories
        sprint_dict["action_items"] = action_items
        sprint_dict["total_story_points"] = total_pts
        sprint_dict["completed_story_points"] = done_pts
        sprint_dict["progress_percentage"] = round((done_pts / total_pts * 100), 1) if total_pts > 0 else 0.0

        return sprint_dict
