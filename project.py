# Project.py
from rich.console import Console
from rich.table import Table
import json

class Project:
    def __init__(self, ID, Title, Leader):
        self.id = ID
        self.title = Title
        self.leader = Leader
        self.members = []
        self.tasks = []

    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title
    
    
    def add_member(self, name):
        if name not in self.members:
            self.members.append(name)

    def delete_member(self, name):
        if name in self.members:
            self.members.remove(name)

    def assign_task(self, task_id, member):
        if member not in self.members:
            print(f"Member {member} is not part of the project.")
        else:
            for task in self.tasks:
                if task.id ==  task_id:
                    task.assign(member)
                    print(f"Task {task.title} assigned to {member}.")

    # def table(self, member):
    def __rich__(self, member):
        console = Console()
        table = Table(title=self.title)

        table.add_column("Task Title", style="cyan", justify="center")
        table.add_column("Description", style="magenta", justify="center")
        table.add_column("Start date and time", style="yellow", justify="center")
        table.add_column("End date and time", style="green", justify="center")
        table.add_column("Assignees", style="blue", justify="center")
        table.add_column("Priority", style="red", justify="center")

        for task in self.tasks:
            if member in task.assignees:
                table.add_row(
                    task.title,
                    task.description,
                    task.start_date_and_time,
                    task.end_date_and_time,
                    task.assignees,
                    task.priority,
                )
            elif len(task.assignees) == 0:
                table.add_row(
                    task.title,
                    task.description,
                    task.start_date_and_time,
                    task.end_date_and_time,
                    task.assignees,
                    task.priority,
                )

        console.print(table)
        # return table

    def update_table(self, member):
        pass

    def save_project_data(self):
        data = {"id":self.id, "title":self.title, "leader":self.leader, "tasks":self.tasks, "members":self.members}
        try:
            with open(f'{self.title}.json', 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def __del__(self):
        print("Project deleted")