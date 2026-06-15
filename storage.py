"""Storage layer for the Project Management CLI.

Persists users, projects, and tasks as nested JSON:

{
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "projects": [
        {
          "id": 1,
          "title": "Website",
          "tasks": [
            {
              "id": 1,
              "title": "Design Homepage",
              "description": "",
              "status": "pending",
              "priority": "medium",
              "assignee": null
            }
          ]
        }
      ]
    }
  ]
}
"""

import json
import os


DEFAULT_DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "data.json"
)


class Storage:
    """Handles loading, saving, and querying users/projects/tasks data."""

    def __init__(self, path=DEFAULT_DATA_FILE):
        self.path = path
        self.data = self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self):
        """Load data from disk, tolerating missing or malformed files."""
        if not os.path.exists(self.path):
            return {"users": []}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: could not load data file ({e}). Starting with empty data.")
            return {"users": []}

        if not isinstance(data, dict) or "users" not in data:
            return {"users": []}
        return data

    def _save(self):
        """Persist current data to disk."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except OSError as e:
            print(f"Error: could not save data ({e}).")

    # ------------------------------------------------------------------
    # Internal lookup helpers
    # ------------------------------------------------------------------

    def _next_id(self, items):
        """Return the next sequential id for a list of dicts with 'id' keys."""
        if not items:
            return 1
        return max(item["id"] for item in items) + 1

    def _find_user(self, identifier):
        """Find a user dict by name (case-insensitive) or numeric ID (as string/int)."""
        for user in self.data["users"]:
            if str(user["id"]) == str(identifier):
                return user
            if user["name"].lower() == str(identifier).lower():
                return user
        return None

    def _find_project(self, user, identifier):
        """Find a project dict within a user's projects by title or ID."""
        for project in user.get("projects", []):
            if str(project["id"]) == str(identifier):
                return project
            if project["title"].lower() == str(identifier).lower():
                return project
        return None

    def _find_project_anywhere(self, identifier):
        """Find a (user, project) pair across all users by project title or ID."""
        for user in self.data["users"]:
            project = self._find_project(user, identifier)
            if project is not None:
                return user, project
        return None, None

    def _find_task(self, project, identifier):
        """Find a task dict within a project's tasks by title or ID."""
        for task in project.get("tasks", []):
            if str(task["id"]) == str(identifier):
                return task
            if task["title"].lower() == str(identifier).lower():
                return task
        return None

    # ------------------------------------------------------------------
    # User operations
    # ------------------------------------------------------------------

    def add_user(self, name):
        """Add a new user. Returns False if a user with that name already exists."""
        if self._find_user(name) is not None:
            return False

        user = {
            "id": self._next_id(self.data["users"]),
            "name": name,
            "projects": [],
        }
        self.data["users"].append(user)
        self._save()
        return True

    def list_users(self):
        """Return a flat list of {id, name} dicts for all users."""
        return [{"id": u["id"], "name": u["name"]} for u in self.data["users"]]

    # ------------------------------------------------------------------
    # Project operations
    # ------------------------------------------------------------------

    def add_project(self, user_identifier, title):
        """Add a project to a user. Returns False if the user doesn't exist
        or a project with that title already exists for the user."""
        user = self._find_user(user_identifier)
        if user is None:
            return False

        if self._find_project(user, title) is not None:
            return False

        project = {
            "id": self._next_id(user.get("projects", [])),
            "title": title,
            "tasks": [],
        }
        user.setdefault("projects", []).append(project)
        self._save()
        return True

    def get_user_projects(self, user_identifier):
        """Return a flat list of {id, title} dicts for a user's projects.

        Returns an empty list if the user doesn't exist or has no projects.
        """
        user = self._find_user(user_identifier)
        if user is None:
            return []
        return [{"id": p["id"], "title": p["title"]} for p in user.get("projects", [])]

    # ------------------------------------------------------------------
    # Task operations
    # ------------------------------------------------------------------

    def add_task(self, project_identifier, title, description="", priority="medium", assignee=None):
        """Add a task to a project (looked up across all users).

        Returns False if the project doesn't exist or a task with that
        title already exists in the project.
        """
        _, project = self._find_project_anywhere(project_identifier)
        if project is None:
            return False

        if self._find_task(project, title) is not None:
            return False

        task = {
            "id": self._next_id(project.get("tasks", [])),
            "title": title,
            "description": description,
            "status": "pending",
            "priority": priority,
            "assignee": assignee,
        }
        project.setdefault("tasks", []).append(task)
        self._save()
        return True

    def get_project_tasks(self, project_identifier):
        """Return the list of task dicts for a project.

        Returns an empty list if the project doesn't exist or has no tasks.
        """
        _, project = self._find_project_anywhere(project_identifier)
        if project is None:
            return []
        return project.get("tasks", [])

    def update_task_status(self, project_identifier, task_identifier, status):
        """Update a task's status. Returns False if the project or task
        cannot be found."""
        _, project = self._find_project_anywhere(project_identifier)
        if project is None:
            return False

        task = self._find_task(project, task_identifier)
        if task is None:
            return False

        task["status"] = status
        self._save()
        return True