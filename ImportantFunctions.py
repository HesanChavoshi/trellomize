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
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')


# Checks if the username is valid or not.
def valid_username(username, data: list):
    if '@' in username:
        return 2
    if data is not None or isinstance(data, list):
        for i in data:
            if 'username' in i and username == i["username"]:
                return 1
    return 0


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


# Function to hash a password
def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def check_password(hashed_password, user_password):
    # Convert the hashed password to bytes if it's a string
    hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password

    # Hash the entered password and compare it with the stored hashed password
    return bcrypt.checkpw(user_password.encode('utf-8'), hashed_bytes)


# You use this function to sign up in the program. It gets your information and then makes a user object and saves those
# information.
def sign_up():
    user_data = UserInfo.read_user_info()
    log = logging.getLogger(__name__)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to our program! Here you can sign up to our program. Follow the steps and fill out the information carefully.")
    print("Just a reminder to write down your username and password, you will need them to log in later on.")
    time.sleep(5)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        # username = input("Enter Your Username: ")
        # age = int(input("Enter Your Age: "))
        # password = input("Enter a Password: ")
        # email = input("Enter Your Email: ")

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

        if valid_username(username, user_data) == 1:
            print("This username is in use, please try another one.")
        elif valid_username(username, user_data) == 2:
            print("You cannot use '@' in your username.")

        if not valid_age(age):
            print("You have to be over 14 to be able to use this program.")

        if not valid_password(password):
            print("Your password must contain at least 10 characters.")

        if valid_email(email, user_data) == 2:
            print("This format is not correct for an e-mail, please try again.")
        elif valid_email(email, user_data) == 1:
            print("This e-mail is already in use, please try again.")

        if valid_username(username, user_data) == 0 and valid_age(age) and valid_password(password) and valid_email(email, user_data) == 0:
            log.info("'" + username + "' has made an account.")
            break
        time.sleep(5)

    os.system('cls' if os.name == 'nt' else 'clear')
    hashed = hash_password(password).decode('utf-8')
    user = User.User(username, age, hashed, email)
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

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        # username = input("Please enter your username: ")
        # password = input("Please enter your password: ")
        questions = [
            inquirer.Text('username', message="Enter Your Username"),
            inquirer.Password('password', message="Enter a Password"),
        ]
        answers = inquirer.prompt(questions)
        username = answers['username']
        password = answers['password']
        # hashed = hash_password(password).decode('utf-8')
        if not valid_info(username, password, user_data):
            print("Login was unsuccessful! Wrong username or password.")
            time.sleep(3)
        else:
            print("Login was successful!")
            time.sleep(3)
            log.info("'" + username + "' has login into his/her account.")
            break
    found_user = find_user(username, user_data, 0)
    user = User.User(found_user["username"], found_user["age"], found_user["password"], found_user["email"])
    if user.status == 'on':
        return user
    else:
        return "This user has been baned from using this program."


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

    title = input("Enter the title for the project: ")
    random_id = str(uuid.uuid4())
    leader = user.username
    members = input("Enter the username or email of the people you want to add them to the project board. Enter these information with comma between them: ").split(',')
    new_project = project.Project(random_id, title, leader)

    for i in members:
        if i != "":
            user_found = find_user(i, user_data, re.match(pattern, i) is not None)
            if user_found != "This user does not exist.":
                new_project.members.append(user_found["username"])
                new_user = User.User(user_found["username"], user_found["age"], user_found["password"], user_found["email"])
                new_user.add_project(new_project.id)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
            else:
                print(user_found)
        else:
            break

    project_data.append(new_project.dict)
    UserInfo.save_project_info(project_data)

    user.add_project(new_project.id)
    user_data.append(user.dict)
    change_user_info(user, user_data)
    log.info("'" + user.username + "' has made the project '" + new_project.title + "'")


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

    os.system('cls' if os.name == 'nt' else 'clear')
    title = input("Enter a title for your task: ")
    description = input("Add any information you want: ")
    task = Task.Task(title, description)
    new_project.add_task(task.id)
    members = input("Enter the username or email of the people you want to assign this task to with a comma between their information: ").split(',')

    for i in members:
        if i != "":
            user_found = find_user(i, user_data, re.match(pattern, i) is not None)
            if user_found != "This user does not exist.":
                new_project.members.append(user_found["username"])
                new_user = User.User(user_found["username"], user_found["age"], user_found["password"], user_found["email"])
                new_user.add_task(task.id)
                user_data.append(new_user.dict)
                change_user_info(new_user, user_data)
            else:
                print(user_found)
        else:
            break
    project_data.append(new_project)
    change_project_info(project_data)
    status = input("Enter the status of this task (backlog, todo, doing, done, archived): ")
    priority = input("Enter the priority of this task (low, medium, high, critical): ")
    if status.lower() == 'backlog':
        task.change_status(Task.Status.BACKLOG)
    elif status.lower() == 'todo':
        task.change_status(Task.Status.TODO)
    elif status.lower() == 'doing':
        task.change_status(Task.Status.DOING)
    elif status.lower() == 'done':
        task.change_status(Task.Status.DONE)
    elif status.lower() == 'archived':
        task.change_status(Task.Status.ARCHIVED)

    if priority.lower() == 'low':
        task.change_priority(Task.Priority.LOW)
    elif priority.lower() == 'medium':
        task.change_priority(Task.Priority.MEDIUM)
    elif priority.lower() == 'high':
        task.change_priority(Task.Priority.HIGH)
    elif priority.lower() == 'critical':
        task.change_priority(Task.Priority.CRITICAL)

    comment = input("Add a comment to the project: ")
    if comment != '':
        task.add_comment(comment)
    task_data.append(task)
    log.info("'" + user.username + "' has made the task '" + task.title + "' in project '" + new_project.title + "'")


# Changes the status variable in a user which shows whether you are banned or not.
def admin_ban_and_unban(user: User.User):
    user.change_status()


# This deletes all the information in users.json, projects.json, tasks.json and app.log.
def admin_delete_all_data():
    UserInfo.delete_user_info()
    UserInfo.delete_project_info()
    UserInfo.delete_task_info()
    open('app.log', 'w').close()


# sign_up()
# login()
# dataset = UserInfo.read_user_info()
# user = User.User("mohsen", 18, "1234567890", "mohsen@gmail.com")
# dataset.append(user.dict)
# UserInfo.save_user_info(dataset)
# print("hello")
