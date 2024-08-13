from common import add_user, UserTypes, filter_users, get_user


def show_menu(user_type):
    return f"""
    1. Add {user_type}
    2. Delete {user_type}
    3. Edit {user_type}
    4. Show {user_type}s
    5. Search {user_type}
    6. Back
    """

def user_settings(user_type):
    print(show_menu(user_type))
    choice = input("Enter your choice: ")
    if choice == "1":
        if add_user(user_type):
            print("Successfully added new admin.")
            user_settings(user_type)
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        super_admin_menu()
    else:
        print("Wrong choice!")
        user_settings(user_type)


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
        pass
    elif choice == "4":
        pass
    else:
        print("Wrong choice !")
        super_admin_menu()


super_admin_menu()