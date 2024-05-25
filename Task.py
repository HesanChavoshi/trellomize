from enum import Enum
import string


class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status:
    BACKLOG = 1
    TODO = 2
    DOING = 3
    DONE = 4
    ARCHIVED = 5


class Task:
    def __init__(self, identification_code, title, info, start, end, assigned_to, priority: Priority, status: Status, history, comments):
        self.identification_code = identification_code
        self.title = title
        self.info = info
        self.start = start
        self.end = end
        self.assigned_to = assigned_to
        self.priority = priority
        self.status = status
        self.history = history
        self.comments = comments

    def set_identification_code(self, identification_code):
        self.identification_code = identification_code

    def get_identification_code(self):
        return self.identification_code

    def set_name(self, title):
        self.title = title

    def get_name(self):
        return self.title

    def set_info(self, info):
        self.info = info

    def get_info(self):
        return self.info

    def set_start(self, start):
        self.start = start

    def get_start(self):
        return self.start

    def set_end(self, end):
        self.end = end

    def get_end(self):
        return self.end

    def set_assigned_to(self, assigned_to):
        self.assigned_to = assigned_to

    def get_assigned_to(self):
        return self.assigned_to

    def set_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def set_history(self, history):
        self.history = history

    def get_history(self):
        return self.history

    def set_comments(self, comments):
        self.comments = comments

    def get_comments(self):
        return self.comments


my_task = Task(
    identification_code=1,
    title="Sample Task",
    info="Some task information",
    start="2024-05-22",
    end="2024-05-30",
    assigned_to="John Doe",
    priority=Priority.HIGH,
    status=Status.TODO,
    history=[],
    comments=[]
)

# Print task details
# print(my_task.get_name())
# print(my_task.get_priority())
# print(my_task.get_status())
# print(my_task.get_priority())
# print(Priority.HIGH)
