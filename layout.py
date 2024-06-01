from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
import inquirer
import ImportantFunctions
import UserInfo
import project
import os


def choose_project(projects_info):
    project_titles = [project['title'] for project in projects_info]
    while True:
        selected_title = input("Enter the title of your project: ")
        if selected_title in project_titles:
            print(f"{selected_title} selected")
            selected_project_info = next(project for project in projects_info if project['title'] == selected_title)
            selected_project = project.Project(*selected_project_info)
            return selected_project
        else:
            print("This project does not exist.")

def choose_task(tasks_info):
    task_titles = [task['title'] for task in tasks_info]
    while True:
        selected_title = input("Enter the title of your project: ")
        if selected_title in task_titles:
            print(f"{selected_title} selected")
            selected_task_info = next(task for task in tasks_info if task['title'] == selected_title)
            selected_task = project.Project(*selected_task_info)
            return selected_task
        else:
            print("This task does not exist.")


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
        a = ImportantFunctions.find_project(i, UserInfo.read_project_info())
        result.append(a)

    result1 = []
    for i in user.tasks:
        a = ImportantFunctions.find_task(i, UserInfo.read_task_info())
        result1.append(a)

    l_titles = [a['title'] for a in result if a['leader'] == user.username]
    titles = [a['title'] for a in result if a['leader'] != user.username]

    l_projects = Panel(Text('projets that created by you:\n' + '\n'.join(l_titles), style="bold white"), style="bold blue")
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
                          choices=['Create Project','Choose Project', 'Create Task', 'Choose Task', 'Logout'])
        ]
        Action = inquirer.prompt(Questions)['Action']

        if Action == 'Create Project':
            new = ImportantFunctions.create_project(user)
            selected_project = new
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Choose Project':
            selected_project = choose_project(result)
            q = input("Do you want to update the project?(y/n) ")
            if q == 'y':
                if selected_project.leader == user.username:
                    ImportantFunctions.update_project(selected_project)
                else:
                    print("You can't update ")
                    pass
            elif q == 'n':
                pass
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Create Task':
            ImportantFunctions.create_task(user, selected_project)
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Choose Task':
            selected_task = choose_task(result1)
            q = input("Do you want to update the task?(y/n) ")
            if q == 'y':
                if selected_project.leader == user.username and selected_task.id in selected_project.tasks:
                    ImportantFunctions.update_task(user, selected_project, selected_task)
                else:
                    print("You can't update ")
                    pass
            elif q == 'n':
                pass
            table = Panel(selected_project.table(user), style="bold blue")
            layout['table'].update(table)
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

        l_projects = Panel(Text('projets that created by you:\n' + '\n'.join(l_titles), style="bold white"), style="bold blue")
        layout["l_project"].update(l_projects)

        projects = Panel(Text('Your projects:\n' + '\n'.join(titles), style="bold white"), style="bold blue")
        layout["project"].update(projects)

        # table = Panel(selected_project.table(user), style="bold blue")
        # layout['table'].update(table)

        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(layout)


if __name__ == "__main__":
    main()
