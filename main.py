import SignUp


def main_menu():
    while True:
        print("Choose your option: ")
        print("[1]Login")
        print("[2]Sign up")
        print("[3]Exit")
        choice = int(input())
        if choice == 1:
            pass
        elif choice == 2:
            user = SignUp.sign_up()
            pass
        elif choice == 3:
            break


main_menu()
