import json


def read_user_info():
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("users.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return []


def save_user_info(data):
    try:
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def delete_user_info():
    data = []
    try:
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def read_project_info():
    try:
        with open('projects.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("projects.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return None


def save_project_info(data):
    try:
        with open('projects.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def delete_project_info():
    data = []
    try:
        with open('projects.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def read_task_info():
    try:
        with open('tasks.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("tasks.json file not found.")
        return None
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return None


def save_task_info(data):
    try:
        with open('tasks.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def delete_task_info():
    data = []
    try:
        with open('tasks.json', 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def read_admin_info():
    try:
        with open('admin.json', 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("users.json file not found.")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON data.")
        return []
