# User.py


class User:
    def __init__(self, username, age, password, email, tasks: list):
        self.username = username
        self.age = age
        self.password = password
        self.email = email
        self.tasks = tasks
        self.dict = {"username": self.username, "age": self.age, "password": self.password, "email": self.email,
                     "tasks": self.tasks}

    def set_name(self, username):
        self.username = username

    def get_name(self):
        return self.username

    def set_age(self, age):
        self.age = age

    def get_age(self):
        return self.age

    def set_password(self, password):
        self.password = password

    def get_password(self):
        return self.password

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def print_info(self):
        print(self.username)
        print(self.age)
        print(self.password)
        print(self.email)

    def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)

    def delete_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

