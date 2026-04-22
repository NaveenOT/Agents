from langchain_core.tools import tool
from state import get_todo

@tool
def set_tasks(tasks: list[str]) -> str:
    """Replace the entire todo list with the provided list of tasks."""
    todo = get_todo()
    todo.clear()
    for task in tasks:
        todo.append({"task": task, "done": False})
    return f"Initialized todo list with {len(todo)} tasks."

@tool
def add_task(task: str) -> str:
    """Add a single task to the todo list."""
    todo = get_todo()
    todo.append({"task": task, "done": False})
    return f"Added task: '{task}'. Total tasks now: {len(todo)}."

@tool
def complete_task(task: str) -> str:
    """Remove a task from the todo list. Supports partial matching."""
    todo = get_todo()
    for t in todo:
        if task.lower() in t["task"].lower():
            t["done"] = True
            return f"Task Marked as completed"
    return f"No matching task found for: '{task}'."

@tool
def view_tasks() -> str:
    """View all current tasks in the todo list."""
    todo = get_todo()
    if not todo:
        return "The todo list is currently empty."
    return "\n".join([f"{i}. {task['task']}" for i, task in enumerate(todo, 1)])
