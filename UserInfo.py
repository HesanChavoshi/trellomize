# UserInfo.py
import json


def read_user_info():
    try:
        with open('Users.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("User.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return None


def save_user_info(data):
    try:
        with open('Users.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

