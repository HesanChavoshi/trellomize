import User
import os
import time
import re


def sign_up():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to our program! Here you can sign up to our program. Follow the steps and fill out the information carefully.")
    print("Just a reminder to write down your username and password, you will need them to log in later on.")
    time.sleep(5)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP1: ")
        username = input("Enter Your Username: ")
        if username == "Alireza":
            print("This user name is in use, please try another one.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP2: ")
        age = int(input("Enter Your Age: "))
        if age < 15:
            print("You have to be over 15 to be able to use this program.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP3: ")
        password = input("Enter a Password: ")
        if len(password) < 10:
            print("Your password must contain at least 10 characters.")
            time.sleep(3)
        else:
            break
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("STEP4: ")
        email = input("Enter Your Email: ")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        check = re.match(pattern, email)
        if not check:
            print("This format is not correct for an e-mail, please try again.")
            time.sleep(3)
        else:
            break
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Congratulations, you managed to make an account in our program! We advice you to check out your account because there might be surprise for you;)")
    time.sleep(10)
    os.system('cls' if os.name == 'nt' else 'clear')
    user = User.User(username, age, password, email)
    return user


sign_up()
