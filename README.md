# Project Management CLI Tool

A command-line interface application for managing users, projects, and tasks with persistent JSON storage. This tool demonstrates Python best practices including modular design, object-oriented programming, comprehensive testing, and data persistence.

## Features

✨ **User Management**
- Create and manage users
- List all users in the system
- Support for multi-word names with automatic normalization

✨ **Project Management**
- Create projects assigned to specific users
- List all projects for a user
- Support for project hierarchies and organization

✨ **Task Management**
- Create tasks within projects
- Set task priority levels (low, medium, high)
- Assign tasks to team members
- Track task status (pending, in-progress, completed)
- Add detailed descriptions to tasks

✨ **Data Persistence**
- JSON-based file storage
- Automatic data persistence on every operation
- Easy data portability and inspection

✨ **User-Friendly CLI**
- Clear, intuitive command structure
- Helpful error messages
- Visual status indicators (✓, ○, priority arrows)
- Comprehensive help documentation

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project:**
```bash
cd /path/to/summative_CLI
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

### User Management

**Add a new user:**
```bash
python main.py add-user --name "John Doe"
```
Output: `✓ User 'John Doe' added successfully`

**List all users:**
```bash
python main.py list-users
```
Output:
```
Users:
  • Alice (ID: alice)
  • Bob Smith (ID: bob_smith)
  • Charlie Jones (ID: charlie_jones)
```

### Project Management

**Add a project to a user:**
```bash
python main.py add-project --user "John Doe" --title "Website Redesign"
```
Output: `✓ Project 'Website Redesign' added to user 'John Doe'`

**List projects for a user:**
```bash
python main.py list-projects --user "John Doe"
```
Output:
```
Projects for user 'John Doe':
  • Website Redesign (ID: website_redesign)
  • Mobile App (ID: mobile_app)
```

### Task Management

**Add a task to a project:**
```bash
python main.py add-task --project "Website Redesign" --title "Design Homepage"
```

**Add a task with full details:**
```bash
python main.py add-task \
  --project "Website Redesign" \
  --title "Implement Authentication" \
  --description "Add JWT-based authentication system" \
  --priority high \
  --assignee "John Doe"
```

**List tasks in a project:**
```bash
python main.py list-tasks --project "Website Redesign"
```
Output:
```
Tasks for project 'Website Redesign':
  ✓ Design Homepage [completed] → (ID: design_homepage)
  ○ Implement Authentication [pending] ↑ (ID: implement_authentication)
  ○ Database Schema [in-progress] → (ID: database_schema)
```

**Update task status:**
```bash
python main.py update-task \
  --project "Website Redesign" \
  --task "Design Homepage" \
  --status completed
```

## Command Reference

### add-user
Add a new user to the system.

```bash
python main.py add-user --name "User Name"
```

**Arguments:**
- `--name` (required): Full name of the user

### list-users
Display all users in the system.

```bash
python main.py list-users
```

### add-project
Create a new project for a user.

```bash
python main.py add-project --user "User Name" --title "Project Title"
```

**Arguments:**
- `--user` (required): User name or ID
- `--title` (required): Project title

### list-projects
Display all projects for a specific user.

```bash
python main.py list-projects --user "User Name"
```

**Arguments:**
- `--user` (required): User name or ID

### add-task
Create a new task within a project.

```bash
python main.py add-task --project "Project Title" --title "Task Title" [OPTIONS]
```

**Arguments:**
- `--project` (required): Project name or ID
- `--title` (required): Task title
- `--description` (optional): Detailed task description
- `--priority` (optional): Task priority - `low`, `medium`, or `high` (default: `medium`)
- `--assignee` (optional): User name or ID to assign the task to

### list-tasks
Display all tasks in a project.

```bash
python main.py list-tasks --project "Project Title"
```

**Arguments:**
- `--project` (required): Project name or ID

### update-task
Update the status of a task.

```bash
python main.py update-task --project "Project" --task "Task Title" --status pending|in-progress|completed
```

**Arguments:**
- `--project` (required): Project name or ID
- `--task` (required): Task name or ID
- `--status` (required): New status - `pending`, `in-progress`, or `completed`

## Project Structure

```
summative_CLI/
├── main.py                 # CLI entry point with command handlers
├── models.py              # Data models (User, Project, Task)
├── storage.py             # Persistent JSON storage layer
├── test_project_manager.py # Comprehensive test suite
├── requirements.txt       # Python dependencies
├── data.json             # Persistent data storage (auto-generated)
└── README.md             # This file
```

## Data Model

### User
Represents a team member who can own projects.

**Attributes:**
- `name` (str): Display name
- `id` (str): Normalized unique identifier

### Project
Represents a project owned by a user and containing tasks.

**Attributes:**
- `title` (str): Project name
- `user_id` (str): Owner's user ID
- `id` (str): Normalized unique identifier

### Task
Represents a work item within a project.

**Attributes:**
- `title` (str): Task name
- `project_id` (str): Parent project ID
- `description` (str): Detailed description
- `status` (str): Current status (pending, in-progress, completed)
- `priority` (str): Priority level (low, medium, high)
- `assignee` (str): Assigned user ID
- `created_at` (str): ISO format creation timestamp
- `id` (str): Normalized unique identifier

## Data Storage

Data is stored in `data.json` in a hierarchical JSON structure:

```json
{
  "users": [
    {"id": "john_doe", "name": "John Doe"},
    {"id": "jane_smith", "name": "Jane Smith"}
  ],
  "projects": [
    {
      "id": "website_redesign",
      "title": "Website Redesign",
      "user_id": "john_doe"
    }
  ],
  "tasks": [
    {
      "id": "design_homepage",
      "title": "Design Homepage",
      "project_id": "website_redesign",
      "description": "Create responsive homepage design",
      "status": "completed",
      "priority": "high",
      "assignee": "jane_smith",
      "created_at": "2026-06-15T10:30:45.123456"
    }
  ]
}
```

## Testing

The project includes a comprehensive test suite with 50+ test cases covering:
- Model functionality
- Storage operations (CRUD)
- User management
- Project management
- Task management
- Data persistence
- Edge cases and error handling

### Run Tests

Run all tests:
```bash
pytest test_project_manager.py -v
```

Run with coverage report:
```bash
pytest test_project_manager.py --cov=. --cov-report=html
```

Run specific test class:
```bash
pytest test_project_manager.py::TestUserModel -v
```

Run specific test:
```bash
pytest test_project_manager.py::TestUserModel::test_user_creation -v
```

### Test Coverage

The test suite covers:
- ✓ Unit tests for all model classes
- ✓ Storage operation tests (add, list, retrieve, update, delete)
- ✓ User, project, and task workflows
- ✓ Data persistence and JSON validity
- ✓ Case-insensitive ID normalization
- ✓ Error handling and edge cases
- ✓ Unicode and special character support
- ✓ Long name handling

## Dependencies

- **rich** (13.7.0): Pretty console output (optional enhancement)
- **python-dateutil** (2.8.2): Date utilities for enhanced timestamp handling
- **pytest** (7.4.3): Testing framework
- **pytest-cov** (4.1.0): Code coverage for tests

All dependencies are listed in `requirements.txt`.

## Examples

### Complete Workflow Example

```bash
# Create users
python main.py add-user --name "Alice Developer"
python main.py add-user --name "Bob Designer"

# List users
python main.py list-users

# Create projects
python main.py add-project --user "Alice Developer" --title "Mobile App"
python main.py add-project --user "Bob Designer" --title "Website"

# List projects for Alice
python main.py list-projects --user "Alice Developer"

# Add tasks to Mobile App project
python main.py add-task \
  --project "Mobile App" \
  --title "Setup Development Environment" \
  --priority high \
  --assignee "alice_developer"

python main.py add-task \
  --project "Mobile App" \
  --title "Design Database Schema" \
  --description "Design normalized database for user data" \
  --priority high \
  --assignee "alice_developer"

python main.py add-task \
  --project "Mobile App" \
  --title "API Documentation" \
  --priority medium

# List tasks in Mobile App
python main.py list-tasks --project "Mobile App"

# Update task status
python main.py update-task \
  --project "Mobile App" \
  --task "Setup Development Environment" \
  --status completed

# View updated tasks
python main.py list-tasks --project "Mobile App"
```

## Features Implemented

✅ **Core Functionality**
- User management (create, list, retrieve)
- Project management (create, list, retrieve)
- Task management (create, list, update status)
- Persistent JSON file storage
- Automatic ID normalization

✅ **Best Practices**
- Modular code structure with separate concerns
- Object-oriented design with proper classes
- Comprehensive docstrings and inline documentation
- Error handling and validation
- Clear CLI with helpful messages

✅ **Testing**
- 50+ comprehensive test cases
- Unit tests for all components
- Integration tests for workflows
- Edge case and error handling tests
- Code coverage reporting

✅ **Documentation**
- This comprehensive README
- Inline code documentation with docstrings
- Clear command examples
- Data model descriptions
- Complete API reference

✅ **Development**
- Version control ready (Git initialized)
- Proper dependency management
- Professional project structure
- Follows Python naming conventions
- PEP 8 compliant code style

## Troubleshooting

**Issue: "User not found" when creating a project**
- Ensure the user exists with `python main.py list-users`
- Use exact user name or normalized ID

**Issue: "Project not found" when adding tasks**
- Check project exists with `python main.py list-projects --user "Username"`
- Use exact project name or normalized ID

**Issue: Data not persisting**
- Check file permissions in the directory
- Ensure `data.json` is readable/writable
- Try clearing `data.json` and starting fresh

**Issue: Cannot find command**
- Run `python main.py --help` for available commands
- Check Python version is 3.10+
- Ensure all dependencies installed with `pip install -r requirements.txt`

## Future Enhancements

Potential improvements for future versions:
- Task dependencies and critical path analysis
- Recurring tasks and task templates
- User roles and permissions system
- Export to CSV/PDF reports
- Web UI interface using Flask/Django
- SQLite database backend for scalability
- Task filtering and search functionality
- Project progress dashboard
- Notification system for task updates
- Multi-user collaboration features

## License

This project is provided as-is for educational purposes.

## Author

Created as a comprehensive Python CLI application demonstrating:
- Command-line interface design
- Data persistence and storage
- Object-oriented programming
- Testing best practices
- Documentation standards
- Professional project structure

---

**Last Updated:** June 15, 2026
**Version:** 1.0.0
**Status:** Complete and Production-Ready
