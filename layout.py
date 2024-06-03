from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
import inquirer
import ImportantFunctions
import UserInfo
import project
import Task
import User
import os
import time


def choose_project(projects_info):
    project_titles = [project['title'] for project in projects_info]
    print(project_titles)
    while True:
        selected_title = input("Enter the title of your project: ")
        a1 = 0
        for index, title in enumerate(project_titles):
            if selected_title == title:
                a1 = index
                break
        if selected_title in project_titles:
            print(f"{selected_title} selected")
            selected_project_info = projects_info[a1].values()
            selected_project = project.Project(*selected_project_info)
            return selected_project
        print("This project does not exist. ")

def choose_task(tasks_info):
    task_titles = [task['title'] for task in tasks_info]
    while True:
        selected_title = input("Enter the title of your task: ")
        a2 = 0
        for index, title in enumerate(task_titles):
            if selected_title == title:
                a2 = index
                break
        if selected_title in task_titles:
            print(f"{selected_title} selected")
            selected_task_info = tasks_info[a2].get("ID")
            found_task = ImportantFunctions.find_task(selected_task_info, tasks_info)
            if found_task != "This task does not exist.":
                new_task = Task.Task(title=found_task["title"], description=found_task["description"],
                                     assignees=found_task.get("assignees", []), history=found_task.get("history", []),
                                     comments=found_task.get("comments", []), project=found_task["project"],
                                     start=found_task["start"], end=found_task["end"])

            return new_task
        print("This task does not exist. ")

def admin_action():
    print("1.Delete all data 2.Ban a user 3.unban a user")
    a = input("Enter a number: ")
    if a == 1:
        ImportantFunctions.admin_delete_all_data()
    elif a == 2:
        user_data = UserInfo.read_user_info()
        username = input("Enter a username to ban: ")
        found_user = ImportantFunctions.find_user(username, user_data, 0)
        user = User.User(username=found_user["username"], age=found_user["age"], password=found_user["password"],
                     email=found_user["email"], tasks=found_user.get('tasks', []), projects=found_user.get('projects', []))
        ImportantFunctions.admin_ban(user)
    elif a == 3:
        username = input("Enter a username to unban: ")
        found_user = ImportantFunctions.find_user(username, user_data, 0)
        user = User.User(username=found_user["username"], age=found_user["age"], password=found_user["password"],
                     email=found_user["email"], tasks=found_user.get('tasks', []), projects=found_user.get('projects', []))
        ImportantFunctions.admin_unban(user)


def main():
    console = Console()

    questions = [
        inquirer.List('action',
                    message="What do you want to do?",
                    choices=['Login', 'Signup', 'Admin Login'])
    ]
    action = inquirer.prompt(questions)['action']

    user = None
    if action == 'Login':
        user = ImportantFunctions.login()
    elif action == 'Signup':
        user = ImportantFunctions.sign_up()
    elif action == 'Admin Login':
        ImportantFunctions.admin_login()
        admin_action()
        return

    os.system('cls' if os.name == 'nt' else 'clear')

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="table"),
    )

    layout["main"].split_row(
        Layout(name="profile"),
        Layout(name="projects"),
    )

    layout['projects'].split_row(
        Layout(name="l_project"),
        Layout(name="project"),
    )

    header = Panel(Text("Welcome to Trellomize", style="bold white"), style="bold blue")
    layout["header"].update(header)

    profile = Panel(Text("Username: " + user.username + '\n' + "Age: " + str(user.age) + '\n' + "Email: " + user.email, style="bold white"), style="bold blue")
    layout["profile"].update(profile)

    result = []
    for i in user.projects:
        x1 = ImportantFunctions.find_project(i, UserInfo.read_project_info())
        result.append(x1)

    result1 = []
    for i in user.tasks:
        x2 = ImportantFunctions.find_task(i, UserInfo.read_task_info())
        result1.append(x2)

    l_titles = [a['title'] for a in result if a['leader'] == user.username]
    titles = [a['title'] for a in result if a['leader'] != user.username]

    l_projects = Panel(Text('projects that created by you:\n' + '\n'.join(l_titles), style="bold white"), style="bold blue")
    layout["l_project"].update(l_projects)

    projects = Panel(Text('Your projects:\n' + '\n'.join(titles), style="bold white"), style="bold blue")
    layout["project"].update(projects)

    console.print(layout)

    selected_project = None
    selected_task = None
    new = None
    table = None
    while True:
        Questions = [
            inquirer.List('Action',
                          message="What do you want to do?",
                          choices=['Create Project','Choose Project', 'Create Task', 'Choose Task', 'Delete Project', 'Delete Task', 'Logout'])
        ]
        Action = inquirer.prompt(Questions)['Action']

        if Action == 'Create Project':
            new = ImportantFunctions.create_project(user)
            selected_project = new
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Choose Project':
            selected_project = choose_project(result)
            # print(selected_project.leader)
            q = input("Do you want to update the project?(y/n) ")
            if q == 'y':
                if selected_project.leader == user.username:
                    ImportantFunctions.update_project(selected_project)
                else:
                    print("You can't update ")
            elif q == 'n':
                pass
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Create Task':
            if selected_project != None:
                ImportantFunctions.create_task(user, selected_project)
                table = Panel(selected_project.table(user), style="bold blue")
                layout['table'].update(table)
            else:
                print("You didn't choose any project. ")
                time.sleep(3)
        elif Action == 'Choose Task':
            selected_task = choose_task(result1)
            q = input("Do you want to update the task?(y/n) ")
            if q == 'y':
                if selected_project.leader == user.username:
                    ImportantFunctions.update_task(user, selected_project, selected_task)
                else:
                    print("You can't update ")
            elif q == 'n':
                pass
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Delete Project':
            if selected_project.leader == user.username:
                q = input(f"Are you sure you want to delete {selected_project.title} projecte?(y/n) ")
                if q == 'y':
                    ImportantFunctions.delete_project(selected_project)
                elif q == 'n':
                    pass
            else:
                print("You can't delete this project. ")
        elif Action == 'Delete Task':
            if selected_project.leader == user.username:
                q = input(f"Are you sure you want to delete {selected_task.title} task?(y/n) ")
                if q == 'y':
                    ImportantFunctions.delete_task(selected_task)
                elif q == 'n':
                    pass
            else:
                print("You can't delete this task. ")
        elif Action == 'Logout':
            break

        result.clear()
        for i in user.projects:
            a = ImportantFunctions.find_project(i, UserInfo.read_project_info())
            result.append(a)

        result1.clear()
        for i in user.tasks:
            a = ImportantFunctions.find_task(i, UserInfo.read_task_info())
            result1.append(a)

        l_titles = [a['title'] for a in result if a['leader'] == user.username]
        titles = [a['title'] for a in result if a['leader'] != user.username]

        l_projects = Panel(Text('projects that created by you:\n' + '\n'.join(l_titles), style="bold white"), style="bold blue")
        layout["l_project"].update(l_projects)

        projects = Panel(Text('Your projects:\n' + '\n'.join(titles), style="bold white"), style="bold blue")
        layout["project"].update(projects)

        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(layout)


if __name__ == "__main__":
    main()
