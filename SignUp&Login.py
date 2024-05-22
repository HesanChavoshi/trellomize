import User
import UserInfo
import time
import os
import re


def sign_up():
    list_data = UserInfo.read_user_info()
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to our program! Here you can sign up to our program. Follow the steps and fill out the information carefully.")
    print("Just a reminder to write down your username and password, you will need them to log in later on.")
    time.sleep(5)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP1: ")
        username = input("Enter Your Username: ")
        if not valid_username(username, list_data):
            print("This username is in use, please try another one.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP2: ")
        age = int(input("Enter Your Age: "))
        if not valid_age(age):
            print("You have to be over 14 to be able to use this program.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP3: ")
        password = input("Enter a Password: ")
        if not valid_password(password):
            print("Your password must contain at least 10 characters.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP4: ")
        email = input("Enter Your Email: ")
        if valid_email(email, list_data) == 2:
            print("This format is not correct for an e-mail, please try again.")
            time.sleep(3)
        elif valid_email(email, list_data) == 1:
            print("This e-mail is already in use, please try again.")
            time.sleep(3)
        else:
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    user = User.User(username, age, password, email)
    dict_data = {"username": user.username, "age": user.age, "password": user.password, "email": user.email}
    list_data.append(dict_data)
    UserInfo.save_user_info(list_data)
    print("Congratulations, you managed to make an account in our program! We advice you to check out your account because there might be surprise for you;)")
    time.sleep(10)
    os.system('cls' if os.name == 'nt' else 'clear')


def valid_username(username, data):
    for i in data:
        if username == i["username"]:
            return False
    return True


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


def valid_info(username, password, data):
    for i in data:
        if username == i["username"]:
            for j in data:
                if password == j["password"]:
                    return True
            return False
    return False
