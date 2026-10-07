"""User Story Module for Scrum Project Management
Provides functionality to create, update, prioritize, and track user stories in the product and sprint backlogs.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class UserStoryService:
    VALID_PRIORITIES = ("Must Have", "Should Have", "Could Have", "Won't Have")
    VALID_STATUSES = ("Backlog", "To Do", "In Progress", "Review/Testing", "Done")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_user_story(
        self,
        story_code: str,
        title: str,
        role: str,
        want: str,
        benefit: str,
        priority: str = "Must Have",
        story_points: int = 3,
        sprint_id: Optional[int] = None,
        status: str = "Backlog",
        assignee: str = "",
        description: str = ""
    ) -> Dict[str, Any]:
        """Creates a new User Story following standard Agile formatting."""
        story_code = story_code.strip().upper()
        title = title.strip()
        role = role.strip()
        want = want.strip()
        benefit = benefit.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO user_stories (
                    story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee, description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (story_code, title, role, want, benefit, priority, story_points, sprint_id, status, assignee.strip(), description.strip()))
            conn.commit()
            story_id = cursor.lastrowid
            return {
                "id": story_id,
                "story_code": story_code,
                "title": title,
                "role": role,
                "want": want,
                "benefit": benefit,
                "priority": priority,
                "story_points": story_points,
                "sprint_id": sprint_id,
                "status": status,
                "assignee": assignee,
                "description": description
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"User Story with code '{story_code}' already exists.")
        finally:
            conn.close()

    def update_user_story_status(self, story_code: str, new_status: str) -> Dict[str, Any]:
        """Transitions a user story across Kanban / Scrum lifecycle states."""
        story_code = story_code.strip().upper()
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM user_stories WHERE story_code = ?;", (story_code,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"User story '{story_code}' not found.")

        cursor.execute("UPDATE user_stories SET status = ? WHERE story_code = ?;", (new_status, story_code))
        conn.commit()
        conn.close()
        return {"story_code": story_code, "status": new_status, "message": f"Story {story_code} moved to {new_status}."}

    def assign_to_sprint(self, story_code: str, sprint_id: int) -> Dict[str, Any]:
        """Assigns a user story to a specific sprint iteration."""
        story_code = story_code.strip().upper()
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM sprints WHERE id = ?;", (sprint_id,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"Sprint with ID {sprint_id} does not exist.")

        cursor.execute("UPDATE user_stories SET sprint_id = ?, status = 'To Do' WHERE story_code = ?;", (sprint_id, story_code))
        conn.commit()
        conn.close()
        return {"story_code": story_code, "sprint_id": sprint_id, "message": f"Story {story_code} assigned to Sprint #{sprint_id}."}

    def get_user_story(self, story_code: str) -> Optional[Dict[str, Any]]:
        """Retrieves details of a user story by story code."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT us.*, s.name AS sprint_name, s.sprint_number
            FROM user_stories us
            LEFT JOIN sprints s ON us.sprint_id = s.id
            WHERE us.story_code = ?;
        """, (story_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def list_user_stories(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists user stories with optional filtering."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT us.*, s.name AS sprint_name, s.sprint_number
            FROM user_stories us
            LEFT JOIN sprints s ON us.sprint_id = s.id
            WHERE 1=1
        """
        params = []
        if sprint_id is not None:
            sql += " AND us.sprint_id = ?"
            params.append(sprint_id)
        if status:
            sql += " AND us.status = ?"
            params.append(status)
        if priority:
            sql += " AND us.priority = ?"
            params.append(priority)

        sql += " ORDER BY us.id ASC;"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_backlog_metrics(self) -> Dict[str, Any]:
        """Calculates story point totals, status counts, and priority breakdown."""
        stories = self.list_user_stories()
        total_points = sum(s["story_points"] for s in stories)
        completed_points = sum(s["story_points"] for s in stories if s["status"] == "Done")

        by_priority = {}
        by_status = {}
        for s in stories:
            by_priority[s["priority"]] = by_priority.get(s["priority"], 0) + s["story_points"]
            by_status[s["status"]] = by_status.get(s["status"], 0) + 1

        return {
            "total_stories": len(stories),
            "total_points": total_points,
            "completed_points": completed_points,
            "completion_percentage": round((completed_points / total_points * 100), 1) if total_points else 0.0,
            "by_priority": by_priority,
            "by_status": by_status
        }
