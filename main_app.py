from authentication import check_superadmin, check_user, log_in, logout
from logs import log_decorator
from users.admin import fill_balance, add_student_to_group, search_result, change_all_students_statuses
from users.common import print_enumerate
from users.teacher import show_my_groups, show_group_students
from users.user import add_user, UserTypes
from users.group import add_group, show_groups, delete_group
from users.superadmin import send_message, show_menu, delete, update, show_users


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
            elif user_type == UserTypes.TEACHER.value:
                teacher_menu(id)
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




"""     SUPER ADMIN MENU     """


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
        send_message()
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
        super_admin_menu()

    else:
        print("Wrong choice!")
        user_settings(user_type)





"""     ADMIN MENU     """


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
        student_settings(id)

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
        if add_group():
            print(f"Successfully created new group.")
        group_settings(id)

    elif choice == "2":
        show_groups()
        group_settings(id)

    elif choice == "3":
        if delete_group():
            print("Group successfully deleted")
        group_settings(id)

    elif choice == "4":
        if add_student_to_group():
            print("Successfully added student to the group.")
        else:
            print("Sorry, places are reserved in the group.")
        group_settings(id)

    elif choice == "5":
        admin_menu(id)

    else:
        print("Wrong choice!")
        group_settings(id)


def student_settings(id):
    print("""
    1. Create student
    2. Show students
    3. Delete student
    4. Search student
    5. Fill balance
    6. Change students statuses
    7. Back
    """)
    choice = input("Enter your choice: ")
    user_type = UserTypes.STUDENT.value

    if choice == "1":
        if add_user(user_type):
            print(f"Successfully added new {user_type}.")
        student_settings(id)

    elif choice == "2":
        show_users('user_type', user_type)
        student_settings(id)

    elif choice == "3":
        if delete('user_type', user_type):
            print(f"{user_type} successfully deleted.")
        student_settings(id)

    elif choice == "4":
        print(search_result())
        student_settings(id)

    elif choice == "5":
        if fill_balance():
            print("Balance was successfully replenished.")
        student_settings(id)

    elif choice == "6":
        change_all_students_statuses()
        print("Successfully changed students' statuses.")
        student_settings(id)

    elif choice == "7":
        admin_menu(id)

    else:
        print("Wrong choice!")
        student_settings(id)





"""     TEACHER MENU    """


def teacher_menu(id):
    print("""
    1. Show my groups
    2. Show group students
    3. Start lesson
    4. Back
    """)
    choice = input("Enter your choice: ")

    if choice == "1":
        print_enumerate(list(show_my_groups(id)))
        teacher_menu(id)

    elif choice == "2":
        show_group_students(id)
        teacher_menu(id)

    elif choice == "3":
        pass
        teacher_menu(id)

    elif choice == "4":
        show_auth_menu()

    else:
        print("Wrong choice!")
        teacher_menu(id)


if __name__ == '__main__':
    show_auth_menu()
