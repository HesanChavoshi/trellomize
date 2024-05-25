import argparse
import os
import json


def create_admin(username, password):
    admin_file = 'admin.json'

    if os.path.exists(admin_file):
        raise FileExistsError(f"Admin file '{admin_file}' already exists.")

    admin_data = {
        'username': username,
        'password': password
    }

    with open(admin_file, 'w') as f:
        json.dump(admin_data, f)

    print(f"Admin user '{username}' created successfully.")


def main():
    parser = argparse.ArgumentParser(description='Manage system admin user.')
    parser.add_argument('command', choices=['create-admin'], help='Command to execute')
    parser.add_argument('--username', required=True, help='Admin username')
    parser.add_argument('--password', required=True, help='Admin password')

    args = parser.parse_args()

    if args.command == 'create-admin':
        create_admin(args.username, args.password)


if __name__ == "__main__":
    main()
