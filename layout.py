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

    if action == 'Login':
        ImportantFunctions.login()
    elif action == 'Signup':
        ImportantFunctions.sign_up()


    os.system('cls' if os.name == 'nt' else 'clear')

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer"),
    )

    layout["main"].split_row(
        Layout(name="profile"),
        Layout(name="projects"),
    )

    header = Panel(Text("Welcome to Trellomize", style="bold white"), style="bold blue")
    layout["header"].update(header)

    console.print(layout)

    while True:
        Questions = [
            inquirer.List('Action',
                          message="What do you want to do?",
                          choices=['Creat Project', 'Logout'])
        ]
        Action = inquirer.prompt(Questions)['Action']

        if Action == 'Create Project':
            ImportantFunctions.create_project()
        elif Action == 'Create Task':
            ImportantFunctions.create_task()
        elif Action == 'Logout':
            break

        os.system('cls' if os.name == 'nt' else 'clear')

        console.print(layout)

if __name__ == "__main__":
    main()