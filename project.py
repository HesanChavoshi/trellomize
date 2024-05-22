# Project.py
from rich.console import Console
from rich.table import Table

class Project:
    def __init__(self, ID, Title):
        self.ID = ID
        self.Title = Title
        self.members = []
        self.tasks = []

    def get_id(self):
        return self.ID
    
    def get_title(self):
        return self.Title
    
    
    def add_member(self, name):
        if name not in self.members:
            self.members.append(name)

    def Table(self):
        console = Console()
        table = Table(title=self.Title)

        table.add_column("Task Title", style="cyan", justify="center")
        table.add_column("Description", style="magenta", justify="center")
        table.add_column("Start date and time", style="yellow", justify="center")
        table.add_column("End date and time", style="green", justify="center")
        table.add_column("Assignees", style="blue", justify="center")
        table.add_column("Priority", style="red", justify="center")

        for task in self.tasks:
            table.add_row(
                task.Title,
                task.Description,
                task.Start_date_and_time,
                task.End_date_and_time,
                task.Assignees,
                task.Priority,
            )

        console.print(table)

    
    def __del__(self):
        print("Project deleted")