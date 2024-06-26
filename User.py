class User:
    def __init__(self, username, age, password, email, tasks: list, projects: list):
        self.username = username
        self.age = age
        self.password = password
        self.email = email
        self.status = 'on'
        self.tasks = tasks
        self.projects = projects
        self.dict = {"username": self.username, "age": self.age, "password": self.password, "email": self.email,
                     "status": self.status, "tasks": self.tasks, "projects": self.projects}

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
        print(self.tasks)
        print(self.projects)

    def add_task(self, task):
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def add_project(self, project):
        if project not in self.projects:
            self.projects.append(project)

    def remove_project(self, project):
        if project in self.projects:
            self.projects.remove(project)

    def change_status(self):
        if self.status == 'on':
            self.status = 'off'
        else:
            self.status = 'on'
