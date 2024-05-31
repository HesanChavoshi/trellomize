from enum import Enum
import string
import uuid
from datetime import datetime, timedelta


class Priority(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Status(Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    DOING = "DOING"
    DONE = "DONE"
    ARCHIVED = "ARCHIVED"


class Task:
    def __init__(self, title, description, assignees: list, history: list, comments: list, project, start=None, end=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.start = start or datetime.now()
        self.end = end or (self.start + timedelta(days=1))
        self.assignees = assignees
        self.priority = Priority.LOW
        self.status = Status.BACKLOG
        self.history = history
        self.comments = comments
        self.project = project
        self.dict = {"ID": self.id, "title": self.title, "description": self.description, "start": str(self.start),
                     "end": str(self.end), "assignees": self.assignees, "priority": self.priority, "status": self.status,
                     "project": self.project, "history": self.history, "comments": self.comments}

    def add_assignee(self, user):
        self.assignees.append(user)

    def remove_assignee(self, user):
        if user in self.assignees:
            self.assignees.remove(user)

    def change_priority(self, new_priority):
        self.priority = new_priority

    def change_status(self, new_status):
        self.status = new_status

    def add_comment(self, username, comment):
        self.comments.append(username + ': ' + comment)

    def add_history(self, history):
        self.history.append(history)


# task1 = Task(title="Implement authentication", description="Implement user authentication in the app")
# task1.add_assignee("user1")
# task1.change_priority(Priority.HIGH)
# task1.change_status(Status.DOING)
# task1.add_comment("user2", "Good progress so far!")
#
# print(f"Task ID: {task1.id}")
# print(f"Title: {task1.title}")
# print(f"Description: {task1.description}")
# print(f"Start Time: {task1.start_time}")
# print(f"End Time: {task1.end_time}")
# print(f"Assignees: {task1.assignees}")
# print(f"Priority: {task1.priority}")
# print(f"Status: {task1.status}")
# print(f"Comments: {task1.comments}")
