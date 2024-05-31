import User
import UserInfo
import project
import Task
import time
import os
import re
import uuid
import logging
import inquirer
import bcrypt
import ast
from datetime import datetime, timedelta
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


# Checks if the username is valid or not.
def valid_username(username, data: list):
    if username != '' and username != '\t' and username != ' ':
        if '@' in username:
            return 2
        if data is not None or isinstance(data, list):
            for i in data:
                if 'username' in i and username == i["username"]:
                    return 1
        return 0
    else:
        return 3


# Checks if the age is valid or not.
def valid_age(age):
    if age < 15:
        return False
    return True


# Checks if the password is valid or not.
def valid_password(password):
    if len(password) < 10 or len(password) > 30:
        return False
    return True


# Checks if the email is valid or not.
def valid_email(email, data):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    check = re.match(pattern, email)
    if not check:
        return 2
    if data is not None or isinstance(data, list):
        for i in data:
            if email == i["email"]:
                return 1
    return 0


# Check if the given username and password are correct.
def valid_info(username, user_password, data):
    for user_record in data:
        if username == user_record["username"]:
            if check_password(user_record["password"], user_password):
                return True
            return False
    return False


# Finds users info using their email or username.
def find_user(info, data, check):
    if check == 0:
        for i in data:
            if info == i["username"]:
                return i
    else:
        for i in data:
            if info == i["email"]:
                return i
    return "This user does not exist."


def valid_assignee(username, new_project: project.Project):
    if username not in new_project.members:
        return False
    else:
        return True


# You use this function to save the user's info which have been changed.
def change_user_info(user: User.User, data: list):
    for i in range(len(data)):
        if user.username == data[i]["username"]:
            data.remove(data[i])
            break
    UserInfo.save_user_info(data)


# Finds projects by using their ID.
def find_project(info, data):
    for i in data:
        if info == i["ID"]:
            return i
    return "This project does not exist."


# You use this function to save the project's info which have been changed.
def change_project_info(pro: project.Project, data: list):
    for i in range(len(data)):
        if pro.id == data[i]["ID"]:
            data.remove(data[i])
            break
    UserInfo.save_project_info(data)


# Finds tasks by using their ID.
def find_task(info, data):
    for i in data:
        if info == i["ID"]:
            return i
    return "This project does not exist."


# You use this function to save the task's info which have been changed.
def change_task_info(task: Task.Task, data: list):
    for i in range(len(data)):
        if task.id == data[i]["ID"]:
            data.remove(data[i])
            break
    UserInfo.save_project_info(data)


# Function to hash a password
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


# In this function hashed_password is the variable which is saved in the users.json and user_password is the password given
# in login. This functions converts the user_password to bytes and then compares it with hashed password and returns
# True or False
def check_password(hashed_password, user_password):
    # Convert the hashed password to bytes if it's a string
    hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password

    # Hash the entered password and compare it with the stored hashed password
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_bytes)


# You use this function to sign up in the program. It gets your information and then makes a user object and saves those
# information.
def sign_up():
    # Reading the files needed.
    user_data = UserInfo.read_user_info()
    log = logging.getLogger(__name__)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to our program! Here you can sign up to our program. Follow the steps and fill out the information carefully.")
    print("Just a reminder to write down your username and password, you will need them to log in later on.")
    time.sleep(5)

    # Getting users information and checking it.
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        questions = [
            inquirer.Text('username', message="Enter Your Username"),
            inquirer.Text('age', message="Enter Your Age"),
            inquirer.Password('password', message="Enter a Password"),
            inquirer.Text('email', message="Enter Your Email"),
        ]
        answers = inquirer.prompt(questions)
        username = answers['username']
        password = answers['password']
        age = int(answers['age'])
        email = answers['email']

        # Checking if the info given are valid or not and giving the right errors.
        if valid_username(username, user_data) == 1:
            print("This username is in use, please try another one.")
        elif valid_username(username, user_data) == 2:
            print("You cannot use '@' in your username.")
        elif valid_username(username, user_data) == 3:
            print("You cannot leave this fild empty or only enter space or tab.")

        if not valid_age(age):
            print("You have to be over 14 to be able to use this program.")

        if not valid_password(password):
            print("Your password must contain at least 10 characters.")

        if valid_email(email, user_data) == 2:
            print("This format is not correct for an e-mail, please try again.")
        elif valid_email(email, user_data) == 1:
            print("This e-mail is already in use, please try again.")

        # If the info are valid we save the information on app.log and break from the loop.
        if valid_username(username, user_data) == 0 and valid_age(age) and valid_password(password) and valid_email(email, user_data) == 0:
            log.info("'" + username + "' has made an account.")
            break
        time.sleep(5)

    # Saving the information in users.json and making an object User and returning it.
    os.system('cls' if os.name == 'nt' else 'clear')
    hashed = hash_password(password).decode('utf-8')
    user = User.User(username, age, hashed, email, [], [])
    user_data.append(user.dict)
    UserInfo.save_user_info(user_data)
    print("Congratulations, you managed to make an account in our program! We advice you to check out your account because there might be surprise for you;)")
    time.sleep(10)
    os.system('cls' if os.name == 'nt' else 'clear')
    return user


# You use this function to log in. It gets your username and password and checks them and then lets you know whether
# the info you gave were correct or not.
def login():
    print("Hello and welcome to our program! Here you can login into your account. Please fill out the information carefully.")
    time.sleep(5)
    log = logging.getLogger(__name__)
    user_data = UserInfo.read_user_info()

    # Getting the user's information and checking it.
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        questions = [
            inquirer.Text('username', message="Enter Your Username"),
            inquirer.Password('password', message="Enter a Password"),
        ]
        answers = inquirer.prompt(questions)
        username = answers['username']
        password = answers['password']
        # Checking if the information are valid or not.
        if not valid_info(username, password, user_data):
            print("Login was unsuccessful! Wrong username or password.")
            time.sleep(3)
        # If the information are valid we break from this loop.
        else:
            print("Login was successful!")
            time.sleep(3)
            log.info("'" + username + "' has login into his/her account.")
            break
    # Finding the user with the information given and making an object User.
    found_user = find_user(username, user_data, 0)
    user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"],
                     ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
    # Checking if the user is banned or not and doing the appropriate thing.
    if user.status == 'on':
        return user
    else:
        return "This user has been baned from using this program."


# It is a login system but for the admin.
def admin_login():
    admin_data = UserInfo.read_admin_info()
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        if username == admin_data["username"] and password == admin_data["password"]:
            print("Login was successful.")
            break
        elif username != admin_data["username"] and password == admin_data["password"]:
            print("Username is wrong.")
        elif username == admin_data["username"] and password != admin_data["password"]:
            print("Password is wrong.")
        elif username != admin_data["username"] and password != admin_data["password"]:
            print("Username is wrong.")
            print("Password is wrong.")


# This gets the needed info and then makes a project object and then saves the information.
def create_project(user: User.User):
    print("In this part you can create a project and add members to it.")
    time.sleep(3)
    user_data = UserInfo.read_user_info()
    log = logging.getLogger(__name__)
    project_data = UserInfo.read_project_info()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Getting the information.
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title = input("Enter the title for the project: ")
        if title != '' and title != '\t' and title != ' ':
            print("You cannot leave this fild empty or only enter space or tab.")
        else:
            break
    random_id = str(uuid.uuid4())
    leader = user.username
    members = input("Enter the username or email of the people you want to add them to the project board. Enter these information with comma between them: ").split(',')
    new_project = project.Project(random_id, title, leader, [], [])
    log.info("'" + user.username + "' has made the project '" + new_project.title + "'")

    # Finding and adding usernames to the member variable of the Project object.
    for member in members:
        if member != "":
            found_user = find_user(member, user_data, re.match(pattern, member) is not None)
            if found_user != "This user does not exist.":
                new_project.add_member(found_user["username"])
                new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"],
                                     ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                new_user.add_project(new_project.id)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
            else:
                print(found_user)
        else:
            break

    # Saving all the changes and information.
    project_data.append(new_project.dict)
    UserInfo.save_project_info(project_data)

    user.add_project(new_project.id)
    user_data.append(user.dict)
    change_user_info(user, user_data)


# This one as well gets the information needed and then saves them.
def create_task(user: User.User, new_project: project.Project):
    os.system('cls' if os.name == 'nt' else 'clear')
    log = logging.getLogger(__name__)
    user_data = UserInfo.read_user_info()
    project_data = UserInfo.read_project_info()
    task_data = UserInfo.read_task_info()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    print("In this part you can create a task and assign it to a member of your project.")
    time.sleep(3)

    # Getting all the information needed.
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title = input("Enter a title for your task: ")
        if title != '' and title != '\t' and title != ' ':
            print("You cannot leave this fild empty or only enter space or tab.")
        else:
            break
    description = input("Add any information you want: ")
    task = Task.Task(title, description, [], [], [], new_project.id)
    new_project.add_task(task.id)

    print(new_project.members)
    # Adding assignees to the task.
    members = input("Enter the username or email of the people you want to assign this task to with a comma between their information: ").split(',')
    for member in members:
        if member != "":
            found_user = find_user(member, user_data, re.match(pattern, member) is not None)
            if found_user != "This user does not exist.":
                if valid_assignee(found_user["username"], new_project):
                    task.add_assignee(found_user["username"])
                    new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"],
                                         ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                    new_user.add_task(task.id)
                    user_data.append(new_user.dict)
                    change_user_info(new_user, user_data)
                else:
                    print("This user is not part of the project.")
            else:
                print(found_user)
        else:
            break

    # Saving the updated project information.
    project_data.append(new_project)
    change_project_info(new_project, project_data)

    # Determining status and priority of this task.
    status = input("Enter the status of this task (backlog, todo, doing, done, archived): ")
    priority = input("Enter the priority of this task (low, medium, high, critical): ")
    if status.lower() == 'backlog' or status.lower() == '' or status.lower() == '\t' or status.lower() == ' ':
        task.change_status(Task.Status.BACKLOG)
    elif status.lower() == 'todo':
        task.change_status(Task.Status.TODO)
    elif status.lower() == 'doing':
        task.change_status(Task.Status.DOING)
    elif status.lower() == 'done':
        task.change_status(Task.Status.DONE)
    elif status.lower() == 'archived':
        task.change_status(Task.Status.ARCHIVED)

    if priority.lower() == 'low' or priority.lower() == '' or priority.lower() == '\t' or priority.lower() == ' ':
        task.change_priority(Task.Priority.LOW)
    elif priority.lower() == 'medium':
        task.change_priority(Task.Priority.MEDIUM)
    elif priority.lower() == 'high':
        task.change_priority(Task.Priority.HIGH)
    elif priority.lower() == 'critical':
        task.change_priority(Task.Priority.CRITICAL)

    # Adding a comment.
    comment = input("Add a comment to the project: ")
    if comment != '' and comment != '\t':
        task.add_comment(user.username, comment)
    task_data.append(task)
    UserInfo.save_task_info(task_data)
    log.info("'" + user.username + "' has made the task '" + task.title + "' in project '" + new_project.title + "'")


# Changes the status to 'off' in a user which shows whether you are banned or not.
def admin_ban(user: User.User):
    log = logging.getLogger(__name__)
    if user.status == 'on':
        user.change_status()
        log.info("'" + user.username + "' has been baned.")
    else:
        return "This user has already been baned."


# Changes the status to 'on' in a user which shows whether you are banned or not.
def admin_unban(user: User.User):
    log = logging.getLogger(__name__)
    if user.status == 'off':
        user.change_status()
        log.info("'" + user.username + "' has been un-baned.")
    else:
        return "This user has not been baned."


# This deletes all the information in users.json, projects.json, tasks.json and app.log.
def admin_delete_all_data():
    UserInfo.delete_user_info()
    UserInfo.delete_project_info()
    UserInfo.delete_task_info()
    open('app.log', 'w').close()


# This function updates the information of a project that has already been made.
def update_project(new_project: project.Project):
    # Reading the information from files.
    user_data = UserInfo.read_user_info()
    project_data = UserInfo.read_project_info()
    log = logging.getLogger(__name__)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    print("These are all the members in your project: ")
    print(new_project.members)

    # Adding members to the project.
    add_members = input("Enter the username or email of the people you want to add to your project. Enter these information with comma between them: ")
    for member in add_members:
        if member != '':
            found_user = find_user(member, user_data, re.match(pattern, member) is not None)
            if found_user != "This user does not exist.":
                new_project.add_member(found_user["username"])
                new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"], ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                new_user.add_project(new_project.id)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
            else:
                print(found_user)
        else:
            break
    project_data.append(new_project)
    change_project_info(new_project, project_data)

    # Removing members from the project.
    remove_members = input("Enter the username or email of the people you want to remove from your project. Enter these information with comma between them: ")
    for member in remove_members:
        if member != '':
            found_user = find_user(member, user_data, re.match(pattern, member) is not None)
            if found_user != "This user does not exist.":
                new_project.remove_member(found_user["username"])
                new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"], ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                new_user.remove_project(new_project.id)
                for i in new_project.tasks:
                    new_user.remove_task(i)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
            else:
                print(found_user)
        else:
            break

    # Saving the information.
    project_data.append(new_project)
    change_project_info(new_project, project_data)
    log.info("'" + new_project.title + "' has been updated by '" + new_project.leader + "'")


# Updating a task that has already been made.
def update_task(user: User.User, new_project: project.Project, task: Task.Task):
    # Reading all the files.
    user_data = UserInfo.read_user_info()
    task_data = UserInfo.read_task_info()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    log = logging.getLogger(__name__)

    print("These are all the people who are assigned to do this task: ")
    print(task.assignees)

    # Adding new assignees.
    add_assignees = input("Enter the username or email of the people you want to assign this task to. Enter these information with comma between them: ")
    for assignee in add_assignees:
        if assignee != '':
            found_user = find_user(assignee, user_data, re.match(pattern, assignee) is not None)
            if found_user != "This user does not exist.":
                if valid_assignee(found_user["username"], new_project):
                    task.add_assignee(found_user["username"])
                    new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"], ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                    new_user.add_task(task.id)
                    user_data.append(new_user.dict)
                    change_user_info(new_user, user_data)
                    date = str(datetime.now())
                    history = "'" + new_user.username + "' has been assigned to do this task on " + date + " by '" + user.username + "."
                    task.add_history(history)
                else:
                    print("This user is not part of the project.")
            else:
                print(found_user)
        else:
            break

    # Removing assignees.
    remove_assignees = input("Enter the username or email of the people you want to remove from this task. Enter these information with comma between them: ")
    for assignee in remove_assignees:
        if assignee != '':
            found_user = find_user(assignee, user_data, re.match(pattern, assignee) is not None)
            if found_user != "This user does not exist." and valid_assignee(found_user["username"], new_project):
                task.remove_assignee(found_user["username"])
                new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"], ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
                new_user.remove_task(task.id)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
                date = str(datetime.now())
                history = "'" + new_user.username + "' has been removed from this task on " + date + " by '" + user.username + "."
                task.add_history(history)
            else:
                print(found_user)
        else:
            break

    # Updating status and priority of this task.
    status = input("Enter the status which you want to change the current status to (backlog, todo, doing, done, archived): ")
    check_status = False
    previous_status = task.status
    priority = input("Enter the priority which you want to change the current priority to (low, medium, high, critical): ")
    check_priority = False
    previous_priority = task.priority
    if status.lower() == 'backlog' or status.lower() == '' or status.lower() == '\t' or status.lower() == ' ':
        task.change_status(Task.Status.BACKLOG)
        check_status = True
    elif status.lower() == 'todo':
        task.change_status(Task.Status.TODO)
        check_status = True
    elif status.lower() == 'doing':
        task.change_status(Task.Status.DOING)
        check_status = True
    elif status.lower() == 'done':
        task.change_status(Task.Status.DONE)
        check_status = True
    elif status.lower() == 'archived':
        task.change_status(Task.Status.ARCHIVED)
        check_status = True

    if priority.lower() == 'low' or priority.lower() == '' or priority.lower() == '\t' or priority.lower() == ' ':
        task.change_priority(Task.Priority.LOW)
        check_priority = True
    elif priority.lower() == 'medium':
        task.change_priority(Task.Priority.MEDIUM)
        check_priority = True
    elif priority.lower() == 'high':
        task.change_priority(Task.Priority.HIGH)
        check_priority = True
    elif priority.lower() == 'critical':
        task.change_priority(Task.Priority.CRITICAL)
        check_priority = True

    if check_status and task.status != previous_status:
        date = str(datetime.now())
        history = "'" + user.username + "' has changed the status of this task on " + date + " from " + previous_status + " to " + task.status + "."
        task.add_history(history)
    if check_priority and task.priority != previous_priority:
        date = str(datetime.now())
        history = "'" + user.username + "' has changed the priority of this task on " + date + " from " + previous_priority + " to " + task.priority + "."
        task.add_history(history)

    # Adding a comment.
    comment = input("Add a comment to the project: ")
    if comment != '':
        task.add_comment(user.username, comment)

    # Saving the information.
    task_data.append(task)
    change_task_info(task, task_data)
    log.info("'" + task.title + "' has been updated by '" + user.username + "'")


def delete_task(task: Task.Task):
    # Reading all the files.
    user_data = UserInfo.read_user_info()
    project_data = UserInfo.read_project_info()
    task_data = UserInfo.read_task_info()

    # Removing the task from its project and saving this change.
    found_project = find_project(task.project, project_data)
    new_project = project.Project(found_project["ID"], found_project["title"], found_project["leader"], ast.literal_eval(found_project["members"]), ast.literal_eval(found_project["tasks"]))
    new_project.remove_task(task.id)
    project_data.append(new_project)
    change_project_info(new_project, project_data)

    # Removing this task form every assignee and saving this change.
    for assignee in task.assignees:
        found_user = find_user(assignee, user_data, 0)
        new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"],
                             ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
        new_user.remove_task(task.id)
        user_data.append(new_user)
        change_user_info(new_user, user_data)
    change_task_info(task, task_data)


def delete_project(new_project: project.Project):
    # Reading all the files.
    user_data = UserInfo.read_user_info()
    project_data = UserInfo.read_project_info()
    task_data = UserInfo.read_task_info()

    # Removing all the tasks related to this project and saving the change.
    for task in new_project.tasks:
        found_task = find_task(task, task_data)
        new_task = Task.Task(found_task["ID"], found_task["title"], ast.literal_eval(found_task["description"]),
                             ast.literal_eval(found_task["assignees"]), ast.literal_eval(found_task["history"]),
                             ast.literal_eval(found_task["comments"]))
        delete_task(new_task)

    # Removing this project form every member of this project and saving the change.
    for member in new_project.members:
        found_user = find_user(member, user_data, 0)
        new_user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"],
                             ast.literal_eval(found_user['tasks']), ast.literal_eval(found_user['projects']))
        new_user.remove_project(new_project.id)
        user_data.append(new_user)
        change_user_info(new_user, user_data)
    change_project_info(new_project, project_data)

