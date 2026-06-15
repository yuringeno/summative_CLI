"""Data models for project tracker.

This module defines the core data models for the project management system:
- User: Represents a team member who can own projects
- Project: Represents a project owned by a user that contains tasks
- Task: Represents a task within a project with status tracking
"""

from datetime import datetime


class User:
    """Represents a user/team member in the project tracker.
    
    Attributes:
        name (str): The display name of the user
        id (str): A normalized unique identifier for the user
    """
    
    def __init__(self, name):
        """Initialize a User with a normalized ID based on name."""
        self.name = name
        self.id = name.lower().replace(" ", "_")
    
    def __repr__(self):
        return f"User(name='{self.name}', id='{self.id}')"


class Project:
    """Represents a project owned by a user.
    
    Attributes:
        title (str): The project title
        user_id (str): The normalized user ID of the project owner
        id (str): A normalized unique identifier for the project
    """
    
    def __init__(self, title, user_id):
        """Initialize a Project with a normalized ID based on title."""
        self.title = title
        self.user_id = user_id
        self.id = title.lower().replace(" ", "_")
    
    def __repr__(self):
        return f"Project(title='{self.title}', user_id='{self.user_id}')"


class Task:
    """Represents a task within a project.
    
    Attributes:
        title (str): The task title
        project_id (str): The normalized project ID this task belongs to
        description (str): Optional task description
        status (str): Current status ('pending', 'in-progress', or 'completed')
        priority (str): Priority level ('low', 'medium', or 'high')
        assignee (str): Optional user ID of the task assignee
        created_at (str): ISO format timestamp of task creation
        id (str): A normalized unique identifier for the task
    """
    
    def __init__(self, title, project_id, description="", priority="medium", assignee=None):
        """Initialize a Task with optional metadata."""
        self.title = title
        self.project_id = project_id
        self.description = description
        self.priority = priority
        self.assignee = assignee
        self.status = "pending"
        self.created_at = datetime.now().isoformat()
        self.id = title.lower().replace(" ", "_")
    
    def mark_complete(self):
        """Mark the task as completed."""
        self.status = "completed"
    
    def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = "in-progress"
    
    def __repr__(self):
        return f"Task(title='{self.title}', status='{self.status}', priority='{self.priority}')"
