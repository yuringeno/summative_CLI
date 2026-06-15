#!/usr/bin/env python3
"""CLI application for project management.

This module provides a command-line interface for managing users, projects, and tasks.
It supports creating, listing, and updating entities with persistent JSON storage.

Usage:
    python main.py add-user --name "John Doe"
    python main.py list-users
    python main.py add-project --user "John Doe" --title "My Project"
    python main.py list-projects --user "John Doe"
    python main.py add-task --project "My Project" --title "Task 1"
    python main.py list-tasks --project "My Project"
    python main.py update-task --project "My Project" --task "Task 1" --status completed
"""

import argparse
from storage import Storage


def format_users(users):
    """Format users list for display.
    
    Args:
        users (list): List of user dictionaries
        
    Returns:
        str: Formatted user list
    """
    if not users:
        return "No users found"
    return "\n".join([f"  • {user['name']} (ID: {user['id']})" for user in users])


def format_projects(projects):
    """Format projects list for display.
    
    Args:
        projects (list): List of project dictionaries
        
    Returns:
        str: Formatted project list
    """
    if not projects:
        return "No projects found"
    return "\n".join([f"  • {proj['title']} (ID: {proj['id']})" for proj in projects])


def format_tasks(tasks):
    """Format tasks list for display.
    
    Args:
        tasks (list): List of task dictionaries
        
    Returns:
        str: Formatted task list
    """
    if not tasks:
        return "No tasks found"
    
    output = []
    for task in tasks:
        status_icon = "✓" if task["status"] == "completed" else "○"
        priority_indicator = {"low": "↓", "medium": "→", "high": "↑"}.get(task.get("priority", "medium"), "→")
        output.append(
            f"  {status_icon} {task['title']} [{task['status']}] {priority_indicator} (ID: {task['id']})"
        )
    return "\n".join(output)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Project Management CLI - Manage users, projects, and tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add-user --name "John Doe"
  python main.py add-project --user "John Doe" --title "Website"
  python main.py add-task --project "Website" --title "Design Homepage"
  python main.py update-task --project "Website" --task "Design Homepage" --status completed
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ============ USER COMMANDS ============
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True, help="User name")

    subparsers.add_parser("list-users", help="List all users")

    # ============ PROJECT COMMANDS ============
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project to a user")
    add_project_parser.add_argument("--user", required=True, help="User name or ID")
    add_project_parser.add_argument("--title", required=True, help="Project title")

    list_projects_parser = subparsers.add_parser("list-projects", help="List projects for a user")
    list_projects_parser.add_argument("--user", required=True, help="User name or ID")

    # ============ TASK COMMANDS ============
    add_task_parser = subparsers.add_parser("add-task", help="Add a new task to a project")
    add_task_parser.add_argument("--project", required=True, help="Project title or ID")
    add_task_parser.add_argument("--title", required=True, help="Task title")
    add_task_parser.add_argument("--description", default="", help="Task description")
    add_task_parser.add_argument(
        "--priority", 
        choices=["low", "medium", "high"], 
        default="medium", 
        help="Task priority level"
    )
    add_task_parser.add_argument("--assignee", help="Assignee user name or ID")

    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks for a project")
    list_tasks_parser.add_argument("--project", required=True, help="Project title or ID")

    update_task_parser = subparsers.add_parser("update-task", help="Update task status")
    update_task_parser.add_argument("--project", required=True, help="Project title or ID")
    update_task_parser.add_argument("--task", required=True, help="Task title or ID")
    update_task_parser.add_argument(
        "--status", 
        required=True,
        choices=["pending", "in-progress", "completed"],
        help="New task status"
    )

    args = parser.parse_args()
    storage = Storage()

    # ============ USER COMMAND HANDLERS ============
    if args.command == "add-user":
        if storage.add_user(args.name):
            print(f"✓ User '{args.name}' added successfully")
        else:
            print(f"✗ User '{args.name}' already exists")
    
    elif args.command == "list-users":
        users = storage.list_users()
        print("Users:")
        print(format_users(users))

    # ============ PROJECT COMMAND HANDLERS ============
    elif args.command == "add-project":
        if storage.add_project(args.user, args.title):
            print(f"✓ Project '{args.title}' added to user '{args.user}'")
        else:
            print(f"✗ Failed to add project. User may not exist or project already exists.")
    
    elif args.command == "list-projects":
        projects = storage.get_user_projects(args.user)
        print(f"Projects for user '{args.user}':")
        print(format_projects(projects))

    # ============ TASK COMMAND HANDLERS ============
    elif args.command == "add-task":
        if storage.add_task(
            args.project, 
            args.title, 
            description=args.description,
            priority=args.priority,
            assignee=args.assignee
        ):
            print(f"✓ Task '{args.title}' added to project '{args.project}'")
        else:
            print(f"✗ Failed to add task. Project may not exist.")
    
    elif args.command == "list-tasks":
        tasks = storage.get_project_tasks(args.project)
        print(f"Tasks for project '{args.project}':")
        print(format_tasks(tasks))
    
    elif args.command == "update-task":
        if storage.update_task_status(args.project, args.task, args.status):
            print(f"✓ Task '{args.task}' status updated to '{args.status}'")
        else:
            print(f"✗ Failed to update task. Task or project may not exist.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()