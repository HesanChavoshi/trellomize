import User
import UserInfo
import project
import Task
import time
import os
import re
import uuid
from datetime import datetime


def sign_up():
    list_data = UserInfo.read_user_info()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to our program! Here you can sign up to our program. Follow the steps and fill out the information carefully.")
    print("Just a reminder to write down your username and password, you will need them to log in later on.")
    time.sleep(5)

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input("Enter Your Username: ")
        age = int(input("Enter Your Age: "))
        password = input("Enter a Password: ")
        email = input("Enter Your Email: ")

        if valid_username(username, list_data) == 1:
            print("This username is in use, please try another one.")
        elif valid_username(username, list_data) == 2:
            print("You cannot use '@' in your username.")

        if not valid_age(age):
            print("You have to be over 14 to be able to use this program.")

        if not valid_password(password):
            print("Your password must contain at least 10 characters.")

        if valid_email(email, list_data) == 2:
            print("This format is not correct for an e-mail, please try again.")
        elif valid_email(email, list_data) == 1:
            print("This e-mail is already in use, please try again.")

        if valid_username(username, list_data) == 0 and valid_age(age) and valid_password(password) and valid_email(email, list_data) == 0:
            break
        time.sleep(5)

    os.system('cls' if os.name == 'nt' else 'clear')
    user = User.User(username, age, password, email)
    dict_data = {"username": user.username, "age": user.age, "password": user.password, "email": user.email}
    list_data.append(dict_data)
    UserInfo.save_user_info(list_data)
    print("Congratulations, you managed to make an account in our program! We advice you to check out your account because there might be surprise for you;)")
    time.sleep(10)
    os.system('cls' if os.name == 'nt' else 'clear')


def login():
    print("Hello and welcome to our program! Here you can login into your account. Please fill out the information carefully.")
    time.sleep(5)
    list_data = UserInfo.read_user_info()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        if not valid_info(username, password, list_data):
            print("Login was unsuccessful! Wrong username or password.")
            time.sleep(3)
        else:
            print("Login was successful!")
            time.sleep(3)
            break
    user_data = find_user(username, list_data, 0)
    user = User.User(user_data["username"], user_data["age"], user_data["password"], user_data["email"])
    return user


def create_project():
    os.system('cls' if os.name == 'nt' else 'clear')
    list_data = UserInfo.read_user_info()
    print("Here you can create a project to your liking. Answer the questions carefully.")
    time.sleep(3)

    os.system('cls' if os.name == 'nt' else 'clear')
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    title = input("Enter the title for the project: ")
    random_id = str(uuid.uuid4())
    information = input("Enter the username or email of the people you want to assign this task to with a comma between their information: ").split(',')
    member = []
    for i in information:
        check = re.match(pattern, i)
        if check and find_user(i, list_data, 1) != "This user does not exist.":
            member.append(find_user(i, list_data, 1))
        elif not check and find_user(i, list_data, 0) != "This user does not exist.":
            member.append(find_user(i, list_data, 0))
    new_project = project.Project(random_id, title)
    for i in member:
        new_project.add_member(i)
    

def create_task():
    os.system('cls' if os.name == 'nt' else 'clear')
    list_data = UserInfo.read_user_info()
    print("In this part you can create a task and assign it to a member of your project.")
    time.sleep(3)

    os.system('cls' if os.name == 'nt' else 'clear')
    title = input("Enter a title for your task: ")

    identification_code = str(uuid.uuid4())

    info = input("You can write the details and important things about this task over here: ")

    start = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    information = input("Enter the username or email of the people you want to assign this task to with a comma between their information: ").split(',')
    assigned_to = []
    for i in information:
        check = re.match(pattern, i)
        if check and find_user(i, list_data, 1) != "This user does not exist.":
            assigned_to.append(find_user(i, list_data, 1))
        elif not check and find_user(i, list_data, 0) != "This user does not exist.":
            assigned_to.append(find_user(info, list_data, 0))

    priority_check = input("Choose the priority of this task: LOW, MEDIUM, HIGH, CRITICAL: ")
    if priority_check == "LOW":
        priority = Task.Priority.LOW
    elif priority_check == "MEDIUM":
        priority_check = Task.Priority.MEDIUM
    elif priority_check == "HIGH":
        priority = Task.Priority.HIGH
    elif priority_check == "CRITICAL":
        priority = Task.Priority.CRITICAL

    status_check = input("Choose the status of this task: BACKLOG, TODO, DOING, DONE, ARCHIVED: ")
    if status_check == "BACKLOG":
        status = Task.Status.BACKLOG
    elif status_check == "TODO":
        status = Task.Status.TODO
    elif status_check == "DOING":
        status = Task.Status.DOING
    elif status_check == "DONE":
        status = Task.Status.DONE
    elif status_check == "ARCHIVED":
        status = Task.Status.ARCHIVED


def valid_username(username, data):
    for i in username:
        if i == '@':
            return 2
    for i in data:
        if username == i["username"]:
            return 1
    return 0


def valid_age(age):
    if age < 15:
        return False
    return True


def valid_password(password):
    if len(password) < 10 or len(password) > 30:
        return False
    return True


def valid_email(email, data):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    check = re.match(pattern, email)
    if not check:
        return 2
    for i in data:
        if email == i["email"]:
            return 1
    return 0


def valid_info(username, password, data):
    for i in data:
        if username == i["username"]:
            for j in data:
                if password == j["password"]:
                    return True
            return False
    return False


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


# sign_up()