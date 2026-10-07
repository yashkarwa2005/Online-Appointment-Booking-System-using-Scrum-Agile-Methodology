"""Action Item Module for Scrum Sprint Tracking
Tracks weekly action items, impediment status, and retrospective follow-ups.
"""
from typing import List, Dict, Any, Optional
import sqlite3
from src.database import get_connection


class ActionItemService:
    VALID_PRIORITIES = ("High", "Medium", "Low")
    VALID_STATUSES = ("To Do", "In Progress", "Review", "Done", "Blocked")

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def create_action_item(
        self,
        item_code: str,
        description: str,
        sprint_id: Optional[int],
        owner: str,
        priority: str = "High",
        due_date: str = "",
        status: str = "To Do"
    ) -> Dict[str, Any]:
        """Creates a trackable sprint action item."""
        item_code = item_code.strip().upper()
        description = description.strip()
        owner = owner.strip()

        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Allowed: {', '.join(self.VALID_PRIORITIES)}")

        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO action_items (item_code, description, sprint_id, owner, priority, due_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (item_code, description, sprint_id, owner, priority, due_date.strip(), status))
            conn.commit()
            item_id = cursor.lastrowid
            return {
                "id": item_id,
                "item_code": item_code,
                "description": description,
                "sprint_id": sprint_id,
                "owner": owner,
                "priority": priority,
                "due_date": due_date,
                "status": status
            }
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError(f"Action item with code '{item_code}' already exists.")
        finally:
            conn.close()

    def update_action_item_status(self, item_code: str, new_status: str) -> Dict[str, Any]:
        """Updates the status of an action item."""
        item_code = item_code.strip().upper()
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'. Allowed: {', '.join(self.VALID_STATUSES)}")

        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM action_items WHERE item_code = ?;", (item_code,))
        if not cursor.fetchone():
            conn.close()
            raise ValueError(f"Action item '{item_code}' not found.")

        cursor.execute("UPDATE action_items SET status = ? WHERE item_code = ?;", (new_status, item_code))
        conn.commit()
        conn.close()
        return {"item_code": item_code, "status": new_status, "message": f"Action item {item_code} moved to {new_status}."}

    def list_action_items(
        self,
        sprint_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Lists action items with optional filters."""
        conn = get_connection(self.db_path)
        cursor = conn.cursor()

        sql = """
            SELECT ai.*, s.name AS sprint_name, s.sprint_number
            FROM action_items ai
            LEFT JOIN sprints s ON ai.sprint_id = s.id
            WHERE 1=1
        """
        params = []
        if sprint_id is not None:
            sql += " AND ai.sprint_id = ?"
            params.append(sprint_id)
        if status:
            sql += " AND ai.status = ?"
            params.append(status)

        sql += " ORDER BY ai.id ASC;"
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
