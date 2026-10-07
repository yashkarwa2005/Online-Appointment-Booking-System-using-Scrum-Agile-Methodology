"""Kanban Board Module for Agile Project Tracking
Visualizes task progression across 5 stages (Backlog -> To Do -> In Progress -> Review/Testing -> Done)
in an interactive terminal display.
"""
from typing import List, Dict, Any, Optional
from src.user_story import UserStoryService
from src.action_item import ActionItemService


class KanbanService:
    COLUMNS = ["Backlog", "To Do", "In Progress", "Review/Testing", "Done"]

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path
        self.story_service = UserStoryService(db_path)
        self.action_service = ActionItemService(db_path)

    def get_board_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups user stories and action items into the 5 Kanban columns."""
        stories = self.story_service.list_user_stories()
        actions = self.action_service.list_action_items()

        board: Dict[str, List[Dict[str, Any]]] = {col: [] for col in self.COLUMNS}

        # Map User Stories
        for s in stories:
            col = s["status"]
            if col in board:
                board[col].append({
                    "type": "STORY",
                    "code": s["story_code"],
                    "title": s["title"],
                    "priority": s["priority"],
                    "points": s["story_points"],
                    "assignee": s["assignee"] or "Unassigned"
                })

        # Map Action Items
        action_status_map = {
            "To Do": "To Do",
            "In Progress": "In Progress",
            "Review": "Review/Testing",
            "Done": "Done",
            "Blocked": "In Progress"
        }
        for a in actions:
            target_col = action_status_map.get(a["status"], "To Do")
            if target_col in board:
                board[target_col].append({
                    "type": "ACTION",
                    "code": a["item_code"],
                    "title": a["description"],
                    "priority": a["priority"],
                    "points": 1,
                    "assignee": a["owner"] or "Unassigned"
                })

        return board

    def get_priority_symbol(self, priority: str) -> str:
        """Returns colored badge or emoji representation for task priority."""
        p = priority.lower()
        if "must" in p or "high" in p:
            return "[!] High"
        elif "should" in p or "medium" in p:
            return "[-] Med"
        else:
            return "[*] Low"

    def render_board(self, show_all: bool = True) -> str:
        """Renders an ASCII Kanban board suitable for terminal display."""
        board = self.get_board_data()
        col_width = 24
        header_sep = "+" + ("-" * (col_width + 2) + "+") * len(self.COLUMNS)

        lines = []
        lines.append("\n" + "=" * 130)
        lines.append("                        AGILE SCRUM KANBAN BOARD (Sprint & Backlog Progression)")
        lines.append("=" * 130)

        # Print Column Headers
        col_headers = []
        for col in self.COLUMNS:
            count = len(board[col])
            header_text = f"{col.upper()} ({count})"
            col_headers.append(f"| {header_text.center(col_width)} ")
        lines.append(header_sep)
        lines.append("".join(col_headers) + "|")
        lines.append(header_sep)

        # Determine maximum cards in any single column
        max_rows = max(len(board[col]) for col in self.COLUMNS) if self.COLUMNS else 0

        if max_rows == 0:
            lines.append("|" + " No tasks currently on board ".center(128) + "|")
            lines.append(header_sep)
            return "\n".join(lines)

        display_limit = max_rows if show_all else min(max_rows, 10)

        for r in range(display_limit):
            # Line 1: Code + Priority
            row_l1 = []
            row_l2 = []
            row_l3 = []
            row_blank = []

            for col in self.COLUMNS:
                items = board[col]
                if r < len(items):
                    item = items[r]
                    p_badge = self.get_priority_symbol(item["priority"])
                    txt1 = f"{item['code']} {p_badge}"
                    # Truncate title
                    t = item["title"]
                    txt2 = (t[:col_width - 3] + "..") if len(t) > col_width else t
                    txt3 = f"{item['points']}pts | {item['assignee'][:10]}"
                else:
                    txt1 = ""
                    txt2 = ""
                    txt3 = ""

                row_l1.append(f"| {txt1.ljust(col_width)} ")
                row_l2.append(f"| {txt2.ljust(col_width)} ")
                row_l3.append(f"| {txt3.ljust(col_width)} ")
                row_blank.append(f"| {' ' * col_width} ")

            lines.append("".join(row_l1) + "|")
            lines.append("".join(row_l2) + "|")
            lines.append("".join(row_l3) + "|")
            lines.append("".join(row_blank) + "|")
            lines.append(header_sep)

        # Board Summary Footer
        total_items = sum(len(board[c]) for c in self.COLUMNS)
        done_items = len(board["Done"])
        progress = round(done_items / total_items * 100, 1) if total_items > 0 else 0.0

        lines.append(f" Total Work Items: {total_items} | Completed: {done_items} | Flow Progress: {progress}%")
        lines.append(" Workflow: BACKLOG -> TO DO -> IN PROGRESS -> REVIEW/TESTING -> DONE")
        lines.append("=" * 130 + "\n")

        return "\n".join(lines)

    def move_task(self, code: str, target_column: str) -> Dict[str, Any]:
        """Moves either a User Story or Action Item to the designated column."""
        code = code.strip().upper()
        if target_column not in self.COLUMNS:
            raise ValueError(f"Invalid column '{target_column}'. Allowed: {', '.join(self.COLUMNS)}")

        if code.startswith("US"):
            return self.story_service.update_user_story_status(code, target_column)
        elif code.startswith("AI"):
            # Map column to action item status
            col_to_action = {
                "Backlog": "To Do",
                "To Do": "To Do",
                "In Progress": "In Progress",
                "Review/Testing": "Review",
                "Done": "Done"
            }
            return self.action_service.update_action_item_status(code, col_to_action[target_column])
        else:
            raise ValueError(f"Unrecognized code prefix '{code}'. Must begin with 'US' or 'AI'.")
