# FR1 & FR8


from models import Task

class TaskService:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, description, deadline, priority):
        task = Task(title, description, deadline, priority)
        self.tasks.append(task)
        return task

    def edit_task(self, index, title=None, description=None, deadline=None, priority=None):
        task = self.tasks[index]
        if title:
            task.title = title
        if description:
            task.description = description
        if deadline:
            task.deadline = deadline
        if priority:
            task.priority = priority
        return task

    def delete_task(self, index):
        self.tasks.pop(index)

    def mark_completed(self, index):
        self.tasks[index].status = "Completed"

    def list_tasks(self):
        return self.tasks

    def sort_by_deadline(self):
        self.tasks.sort(key=lambda t: t.deadline)

    def sort_by_priority(self):
        order = {"High": 1, "Medium": 2, "Low": 3}
        self.tasks.sort(key=lambda t: order[t.priority])

    def filter_tasks(self, filter_type):
        if filter_type == "completed":
            return [t for t in self.tasks if t.status == "Completed"]
        if filter_type == "not_completed":
            return [t for t in self.tasks if t.status != "Completed"]
        if filter_type == "high_priority":
            return [t for t in self.tasks if t.priority == "High"]
        return self.tasks
