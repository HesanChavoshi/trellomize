from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
import inquirer
import ImportantFunctions
import project
import os

def main():
    console = Console()

    questions = [
        inquirer.List('action',
                    message="What do you want to do?",
                    choices=['Login', 'Signup'])
    ]
    action = inquirer.prompt(questions)['action']

    user = None
    if action == 'Login':
        user = ImportantFunctions.login()
    elif action == 'Signup':
        user = ImportantFunctions.sign_up()

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

    header = Panel(Text("Welcome to Trellomize", style="bold white"), style="bold blue")
    layout["header"].update(header)

    profile = Panel(Text("Username: " + user.username + '\n' + "Age: " + str(user.age) + '\n' + "Email: " + user.email, style="bold white"), style="bold blue")
    layout["profile"].update(profile)

    # result = []
    # for i in user.projects:
    #     a = 
    #     result.append(a)


    projects = Panel(Text('\n'.join(user.projects), style="bold white"), style="bold blue")
    layout["projects"].update(projects)

    console.print(layout)

    new = None
    table = None
    while True:
        Questions = [
            inquirer.List('Action',
                          message="What do you want to do?",
                          choices=['Create Project', 'Create Task', 'Logout'])
        ]
        Action = inquirer.prompt(Questions)['Action']

        if Action == 'Create Project':
            new = ImportantFunctions.create_project(user)
            table = Panel(new.table(user), style="bold blue")
            layout['table'].update(table)
        elif Action == 'Create Task':
            ImportantFunctions.create_task(user, new)
            layout['table'].update(table)
        elif Action == 'Logout':
            break
        
        projects = Panel(Text('\n'.join(user.projects), style="bold white"), style="bold blue")
        layout["projects"].update(projects)
        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(layout)

if __name__ == "__main__":
    main()