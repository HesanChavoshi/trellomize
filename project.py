# Project.py
from rich.console import Console
from rich.table import Table
# import json
import ImportantFunctions
import UserInfo
import Task


class Project:
    def __init__(self, ID, title, leader, members: list, tasks: list):
        self.id = ID
        self.title = title
        self.leader = leader
        self.members = members
        self.tasks = tasks
        self.dict = {"ID": self.id, "title": self.title, "leader": self.leader, "members": self.members,
                     "tasks": self.tasks}

    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title

    def add_member(self, name):
        if name not in self.members:
            self.members.append(name)

    def remove_member(self, name):
        if name in self.members:
            self.members.remove(name)

    def add_task(self, task_id):
        if task_id not in self.tasks:
            self.tasks.append(task_id)

    def remove_task(self, task_id):
        if task_id in self.tasks:
            self.tasks.remove(task_id)

    def assign_task(self, task_id, member):
        if member not in self.members:
            print(f"Member {member} is not part of the project.")
        else:
            for task in self.tasks:
                if task.id == task_id:
                    task.add_assignee(member)
                    print(f"Task {task.title} assigned to {member}.")

    def table(self, member):
        console = Console()
        table = Table(title=self.title)

        table.add_column("Task Title", style="cyan", justify="center")
        table.add_column("Description", style="magenta", justify="center")
        table.add_column("Start date and time", style="yellow", justify="center")
        table.add_column("End date and time", style="green", justify="center")
        table.add_column("Assignees", style="blue", justify="center")
        table.add_column("Priority", style="red", justify="center")
        table.add_column("History", style="red", justify="center")
        table.add_column("Comments", style="red", justify="center")

        for task in self.tasks:
            task_data = UserInfo.read_task_info()
            found_task = ImportantFunctions.find_task(task, task_data)
            if found_task != "This task does not exist.":
                new_task = Task.Task(title=found_task["title"], description=found_task["description"],
                                     assignees=found_task.get("assignees", []), history=found_task.get("history", []),
                                     comments=found_task.get("comments", []), project=found_task["project"],
                                     start=found_task["start"], end=found_task["end"])
                if member.username in new_task.assignees:
                    table.add_row(
                        new_task.title,
                        new_task.description,
                        new_task.start,
                        new_task.end,
                        new_task.show_assignees(),
                        new_task.priority,
                        new_task.show_history(),
                        new_task.show_comments(),
                    )
                elif len(new_task.assignees) == 0:
                    table.add_row(
                        new_task.title,
                        new_task.description,
                        new_task.start,
                        new_task.end,
                        new_task.show_assignees(),
                        new_task.priority,
                        new_task.show_history(),
                        new_task.show_comments(),
                )

        return table

    def update_table(self, member):
        pass
