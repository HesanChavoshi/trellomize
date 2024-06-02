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
    def __init__(self, title, description, assignees: list, history: list, comments: list, project, start, end):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.start = start  # or datetime.now()
        self.end = end  # or (self.start + timedelta(days=1))
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

    def change_start(self, start):
        self.start = start

    def change_end(self, end):
        self.end = end

    def show_assignees(self):
        assignees_str = ''
        for assignee in self.assignees:
            if assignee != '':
                assignees_str += assignee + ', '
        return assignees_str

    def show_history(self):
        history_str = ''
        for history in self.history:
            if history != '':
                history_str += history + ', '
        return history_str

    def show_comments(self):
        comments_str = ''
        for comment in self.comments:
            if comment != '':
                comments_str += comment + ', '
        return comments_str
