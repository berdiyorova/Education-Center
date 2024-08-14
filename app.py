from file_manager import user_manager
from users.superadmin import super_admin_menu

superadmin_login = "superadmin"
superadmin_password = "sA0101"


def check_user(login, password):
    all_users = user_manager.read_data()
    for user in all_users:
        if user['login'] == login and user['password'] == password:
            user['is_login'] = True
            user_manager.write_data(all_users)
            return True
    return False


def check_superadmin(login, password):
    if login == superadmin_login and password == superadmin_password:
        return True
    return False


def show_auth_menu():
    print("""
    1. Login.
    2. Exit.
    """)

    user_input = input("Choose an option: ").strip()

    if user_input == "1":
        login = input("Enter your login: ").strip()
        password = input("Enter your password: ").strip()
        if check_superadmin(login=login, password=password):
            print("You have successfully logged in.")
            super_admin_menu()
        elif check_user(login=login, password=password):
            print("You have successfully logged in.")
            ...
        else:
            print("System cannot detect you, please try again!")
            show_auth_menu()
    elif user_input == "2":
        answer = input("Would you like to quit? (y/n): ").lower()
        if answer == "y":
            print("You quit the program.")
        else:
            return show_auth_menu()
    else:
        print("Invalid input, try again!")
        return show_auth_menu()


if __name__ == '__main__':
    show_auth_menu()
