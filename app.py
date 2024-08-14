from file_manager import user_manager
from logs import log_decorator
from users.admin import show_groups, delete_group, add_student_to_group
from users.common import UserTypes, add_user, print_users, create_group
from users.superadmin import email_to_users, send_message, show_menu, delete, update, show_users, search

superadmin_login = "superadmin"
superadmin_password = "sA0101"



def check_superadmin(login, password):
    if login == superadmin_login and password == superadmin_password:
        return True
    return False


def check_user(login, password):
    all_users = user_manager.read_data()
    for user in all_users:
        if user['login'] == login and user['password'] == password:
            return True
    return False

def log_in(login, password):
    if check_user(login, password):
        all_users = user_manager.read_data()
        for user in all_users:
            if user['login'] == login and user['password'] == password:
                user['is_login'] = True
                user_manager.write_data(all_users)
                return user['user_type'], user['id']
        return None


def logout(id):
    all_users = user_manager.read_data()
    for user in all_users:
        if user['id'] == id:
            user['is_login'] = False
            user_manager.write_data(all_users)
            return True
    return False


def show_auth_menu():
    print("""
    1. Login.
    2. Exit.
    """)

    user_input = input("Choose an option: ").strip()

    if user_input == "1":
        login = input("Enter your login: ")
        password = input("Enter your password: ")
        if check_superadmin(login=login, password=password):
            print("You have successfully logged in.")
            super_admin_menu()
        elif check_user(login=login, password=password):
            print("You have successfully logged in.")
            user_type, id = log_in(login, password)
            if user_type == UserTypes.ADMIN.value:
                admin_menu(id)
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




"""     SUPER ADMIN     """

def super_admin_menu():
    print("""
        1. Admins
        2. Teachers
        3. Send message
        4. Logout
        """)
    choice = input("Enter your choice:  ")
    if choice == "1":
        user_settings(UserTypes.ADMIN.value)
    elif choice == "2":
        user_settings(UserTypes.TEACHER.value)
    elif choice == "3":
        users = email_to_users()
        send_message(users)
        super_admin_menu()
    elif choice == "4":
        show_auth_menu()
    else:
        print("Wrong choice !")
        super_admin_menu()


@log_decorator
def user_settings(user_type):
    print(show_menu(user_type))
    choice = input("Enter your choice: ")
    if choice == "1":
        if add_user(user_type):
            print(f"Successfully added new {user_type}.")
            user_settings(user_type)
    elif choice == "2":
        if delete('user_type', user_type):
            print(f"{user_type} successfully deleted.")
            user_settings(user_type)
    elif choice == "3":
        if update('user_type', user_type):
            print(f"{user_type} successfully updated.")
            user_settings(user_type)
    elif choice == "4":
        show_users('user_type', user_type)
        user_settings(user_type)
    elif choice == "5":
        users = search('user_type', user_type)
        if users:
            print_users(users)
        else:
            print("User not found.")
        user_settings(user_type)
    elif choice == "6":
        super_admin_menu()
    else:
        print("Wrong choice!")
        user_settings(user_type)



"""     ADMIN     """


def admin_menu(id):
    print("""
        1. Groups
        2. Students
        3. Logout
        """)
    choice = input("Enter your choice:  ")
    if choice == "1":
        group_settings(id)
    elif choice == "2":
        user_settings(UserTypes.STUDENT.value)
    elif choice == "3":
        logout(id)
        print("You have successfully logged out")
        show_auth_menu()
    else:
        print("Wrong choice !")
        admin_menu(id)


def group_settings(id):
    print("""
    1. Create group
    2. Show groups
    3. Delete group
    4. Add student to group
    5. Back
    """)
    choice = input("Enter your choice: ")
    if choice == "1":
        if create_group():
            print(f"Successfully created new group.")
            group_settings(id)
    elif choice == "2":
        show_groups()
    elif choice == "3":
        if delete_group():
            print("Group successfully deleted")
    elif choice == "4":
        add_student_to_group()
    elif choice == "5":
        admin_menu(id)
    else:
        print("Wrong choice!")
        group_settings(id)


if __name__ == '__main__':
    show_auth_menu()
