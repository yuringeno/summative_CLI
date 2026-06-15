"""Comprehensive test suite for the project management CLI.

Tests cover:
- User management (add, list, retrieve)
- Project management (add, list, retrieve)
- Task management (add, list, update status)
- Error handling and edge cases
- Data persistence
"""

import pytest
import json
import os
from pathlib import Path
from storage import Storage
from models import User, Project, Task


@pytest.fixture
def test_storage():
    """Create a fresh Storage instance with test data file."""
    test_file = "test_data.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    storage = Storage(test_file)
    yield storage
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)


class TestUserModel:
    """Test the User model."""
    
    def test_user_creation(self):
        """Test user object creation."""
        user = User("John Doe")
        assert user.name == "John Doe"
        assert user.id == "john_doe"
    
    def test_user_id_normalization(self):
        """Test that user IDs are properly normalized."""
        user1 = User("Alice Smith")
        user2 = User("ALICE SMITH")
        user3 = User("alice smith")
        assert user1.id == user2.id == user3.id == "alice_smith"
    
    def test_user_repr(self):
        """Test string representation of user."""
        user = User("Bob")
        assert "Bob" in repr(user)
        assert "bob" in repr(user)


class TestProjectModel:
    """Test the Project model."""
    
    def test_project_creation(self):
        """Test project object creation."""
        project = Project("Website Redesign", "alice")
        assert project.title == "Website Redesign"
        assert project.user_id == "alice"
        assert project.id == "website_redesign"
    
    def test_project_id_normalization(self):
        """Test that project IDs are properly normalized."""
        proj1 = Project("Mobile App", "user1")
        proj2 = Project("MOBILE APP", "user1")
        assert proj1.id == proj2.id == "mobile_app"
    
    def test_project_repr(self):
        """Test string representation of project."""
        project = Project("API Documentation", "bob")
        assert "API Documentation" in repr(project)


class TestTaskModel:
    """Test the Task model."""
    
    def test_task_creation(self):
        """Test task object creation."""
        task = Task("Write tests", "mobile_app", priority="high", assignee="alice")
        assert task.title == "Write tests"
        assert task.project_id == "mobile_app"
        assert task.status == "pending"
        assert task.priority == "high"
        assert task.assignee == "alice"
    
    def test_task_status_transitions(self):
        """Test task status changes."""
        task = Task("Implementation", "web_project")
        assert task.status == "pending"
        
        task.mark_in_progress()
        assert task.status == "in-progress"
        
        task.mark_complete()
        assert task.status == "completed"
    
    def test_task_default_values(self):
        """Test task creation with default values."""
        task = Task("Simple task", "project1")
        assert task.description == ""
        assert task.priority == "medium"
        assert task.assignee is None
        assert task.status == "pending"


class TestStorageUserOperations:
    """Test user storage operations."""
    
    def test_add_user(self, test_storage):
        """Test adding a user."""
        result = test_storage.add_user("Alice")
        assert result is True
        assert len(test_storage.list_users()) == 1
    
    def test_add_duplicate_user(self, test_storage):
        """Test that adding duplicate user returns False."""
        test_storage.add_user("Bob")
        result = test_storage.add_user("Bob")
        assert result is False
        assert len(test_storage.list_users()) == 1
    
    def test_list_users(self, test_storage):
        """Test listing all users."""
        test_storage.add_user("Alice")
        test_storage.add_user("Bob Smith")
        users = test_storage.list_users()
        assert len(users) == 2
        assert users[0]["name"] == "Alice"
        assert users[1]["name"] == "Bob Smith"
    
    def test_get_user(self, test_storage):
        """Test retrieving a specific user."""
        test_storage.add_user("Charlie")
        user = test_storage.get_user("charlie")
        assert user is not None
        assert user["name"] == "Charlie"
    
    def test_get_user_case_insensitive(self, test_storage):
        """Test that user retrieval is case-insensitive."""
        test_storage.add_user("Diana")
        user1 = test_storage.get_user("DIANA")
        user2 = test_storage.get_user("diana")
        user3 = test_storage.get_user("Diana")
        assert user1 == user2 == user3
    
    def test_get_nonexistent_user(self, test_storage):
        """Test retrieving non-existent user returns None."""
        result = test_storage.get_user("nonexistent")
        assert result is None
    
    def test_user_persistence(self, test_storage):
        """Test that users are persisted to disk."""
        test_storage.add_user("Eve")
        
        # Create new storage instance with same file
        storage2 = Storage("test_data.json")
        users = storage2.list_users()
        assert len(users) == 1
        assert users[0]["name"] == "Eve"


class TestStorageProjectOperations:
    """Test project storage operations."""
    
    def test_add_project(self, test_storage):
        """Test adding a project."""
        test_storage.add_user("Alice")
        result = test_storage.add_project("Alice", "Website")
        assert result is True
    
    def test_add_project_nonexistent_user(self, test_storage):
        """Test adding project to non-existent user fails."""
        result = test_storage.add_project("NonExistent", "Project")
        assert result is False
    
    def test_add_duplicate_project(self, test_storage):
        """Test that duplicate projects are rejected."""
        test_storage.add_user("Bob")
        test_storage.add_project("Bob", "CLI Tool")
        result = test_storage.add_project("Bob", "CLI Tool")
        assert result is False
    
    def test_list_user_projects(self, test_storage):
        """Test listing projects for a user."""
        test_storage.add_user("Charlie")
        test_storage.add_project("Charlie", "Project A")
        test_storage.add_project("Charlie", "Project B")
        
        projects = test_storage.get_user_projects("Charlie")
        assert len(projects) == 2
        assert projects[0]["title"] == "Project A"
        assert projects[1]["title"] == "Project B"
    
    def test_get_project(self, test_storage):
        """Test retrieving a specific project."""
        test_storage.add_user("Diana")
        test_storage.add_project("Diana", "Mobile App")
        project = test_storage.get_project("Mobile App")
        assert project is not None
        assert project["title"] == "Mobile App"
    
    def test_get_project_case_insensitive(self, test_storage):
        """Test project retrieval with case normalization."""
        test_storage.add_user("Eve")
        test_storage.add_project("Eve", "Web Platform")
        proj1 = test_storage.get_project("web platform")
        proj2 = test_storage.get_project("WEB PLATFORM")
        assert proj1 == proj2
    
    def test_project_isolation_by_user(self, test_storage):
        """Test that projects are isolated by user."""
        test_storage.add_user("Frank")
        test_storage.add_user("Grace")
        test_storage.add_project("Frank", "Project X")
        test_storage.add_project("Grace", "Project X")
        
        frank_projects = test_storage.get_user_projects("Frank")
        grace_projects = test_storage.get_user_projects("Grace")
        assert len(frank_projects) == 1
        assert len(grace_projects) == 1
        assert frank_projects[0]["user_id"] == "frank"
        assert grace_projects[0]["user_id"] == "grace"


class TestStorageTaskOperations:
    """Test task storage operations."""
    
    def test_add_task(self, test_storage):
        """Test adding a task to a project."""
        test_storage.add_user("Henry")
        test_storage.add_project("Henry", "API")
        result = test_storage.add_task("API", "Implement GET endpoint")
        assert result is True
    
    def test_add_task_nonexistent_project(self, test_storage):
        """Test adding task to non-existent project fails."""
        result = test_storage.add_task("NonExistent", "Task")
        assert result is False
    
    def test_add_task_with_metadata(self, test_storage):
        """Test adding task with description, priority, and assignee."""
        test_storage.add_user("Ivy")
        test_storage.add_project("Ivy", "Dashboard")
        test_storage.add_task(
            "Dashboard",
            "Design UI",
            description="Create mockups for dashboard",
            priority="high",
            assignee="ivy"
        )
        tasks = test_storage.get_project_tasks("Dashboard")
        assert len(tasks) == 1
        assert tasks[0]["description"] == "Create mockups for dashboard"
        assert tasks[0]["priority"] == "high"
        assert tasks[0]["assignee"] == "ivy"
    
    def test_list_project_tasks(self, test_storage):
        """Test listing tasks for a project."""
        test_storage.add_user("Jack")
        test_storage.add_project("Jack", "Backend")
        test_storage.add_task("Backend", "Task 1")
        test_storage.add_task("Backend", "Task 2")
        test_storage.add_task("Backend", "Task 3")
        
        tasks = test_storage.get_project_tasks("Backend")
        assert len(tasks) == 3
    
    def test_update_task_status(self, test_storage):
        """Test updating task status."""
        test_storage.add_user("Kate")
        test_storage.add_project("Kate", "Frontend")
        test_storage.add_task("Frontend", "Write CSS")
        
        result = test_storage.update_task_status("Frontend", "Write CSS", "in-progress")
        assert result is True
        
        tasks = test_storage.get_project_tasks("Frontend")
        assert tasks[0]["status"] == "in-progress"
    
    def test_update_task_to_completed(self, test_storage):
        """Test marking task as completed."""
        test_storage.add_user("Leo")
        test_storage.add_project("Leo", "Testing")
        test_storage.add_task("Testing", "Run unit tests")
        
        result = test_storage.update_task_status("Testing", "Run unit tests", "completed")
        assert result is True
        
        tasks = test_storage.get_project_tasks("Testing")
        assert tasks[0]["status"] == "completed"
    
    def test_update_task_invalid_status(self, test_storage):
        """Test updating task with invalid status fails."""
        test_storage.add_user("Mia")
        test_storage.add_project("Mia", "Project")
        test_storage.add_task("Project", "Task")
        
        result = test_storage.update_task_status("Project", "Task", "invalid_status")
        assert result is False
    
    def test_update_nonexistent_task(self, test_storage):
        """Test updating non-existent task fails."""
        test_storage.add_user("Noah")
        test_storage.add_project("Noah", "Project")
        
        result = test_storage.update_task_status("Project", "NonExistent", "completed")
        assert result is False
    
    def test_get_task(self, test_storage):
        """Test retrieving a specific task."""
        test_storage.add_user("Olivia")
        test_storage.add_project("Olivia", "Research")
        test_storage.add_task("Research", "Gather Data")
        
        task = test_storage.get_task("Gather Data")
        assert task is not None
        assert task["title"] == "Gather Data"
    
    def test_task_persistence(self, test_storage):
        """Test that tasks are persisted to disk."""
        test_storage.add_user("Paul")
        test_storage.add_project("Paul", "Deployment")
        test_storage.add_task("Deployment", "Setup CI/CD")
        
        # Create new storage instance
        storage2 = Storage("test_data.json")
        tasks = storage2.get_project_tasks("Deployment")
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Setup CI/CD"


class TestDataPersistence:
    """Test overall data persistence."""
    
    def test_full_workflow_persistence(self, test_storage):
        """Test complete workflow with persistence."""
        # Add users
        test_storage.add_user("Quinn")
        test_storage.add_user("Rachel")
        
        # Add projects
        test_storage.add_project("Quinn", "CRM")
        test_storage.add_project("Rachel", "Analytics")
        
        # Add tasks
        test_storage.add_task("CRM", "Database schema")
        test_storage.add_task("CRM", "API design", priority="high")
        test_storage.add_task("Analytics", "Dashboard")
        
        # Update task
        test_storage.update_task_status("CRM", "Database schema", "completed")
        
        # Reload from disk
        storage2 = Storage("test_data.json")
        assert len(storage2.list_users()) == 2
        assert len(storage2.get_user_projects("Quinn")) == 1
        assert len(storage2.get_project_tasks("CRM")) == 2
        
        crm_tasks = storage2.get_project_tasks("CRM")
        assert crm_tasks[0]["status"] == "completed"
    
    def test_json_format_validity(self, test_storage):
        """Test that stored JSON is valid."""
        test_storage.add_user("Sam")
        test_storage.add_project("Sam", "Testing")
        test_storage.add_task("Testing", "Write tests")
        
        # Read and parse JSON
        with open("test_data.json", "r") as f:
            data = json.load(f)
        
        assert "users" in data
        assert "projects" in data
        assert "tasks" in data
        assert len(data["users"]) == 1
        assert len(data["projects"]) == 1
        assert len(data["tasks"]) == 1


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_storage(self, test_storage):
        """Test operations on empty storage."""
        assert test_storage.list_users() == []
        assert test_storage.get_user_projects("anyone") == []
        assert test_storage.get_project_tasks("any_project") == []
    
    def test_special_characters_in_names(self, test_storage):
        """Test handling of special characters."""
        test_storage.add_user("Alice-Marie")
        test_storage.add_user("Bob_Jr")
        users = test_storage.list_users()
        assert len(users) == 2
    
    def test_unicode_characters(self, test_storage):
        """Test handling of unicode characters."""
        test_storage.add_user("José")
        test_storage.add_user("李明")
        users = test_storage.list_users()
        assert len(users) == 2
        assert "José" in [u["name"] for u in users]
    
    def test_long_names(self, test_storage):
        """Test handling of long names."""
        long_name = "A" * 100
        result = test_storage.add_user(long_name)
        assert result is True
        assert test_storage.get_user(long_name) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=.", "--cov-report=html"])
