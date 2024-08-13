from common import add_user, UserTypes, filter_users, ordered_users, get_user, print_users, delete_user


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
            print(f"Successfully added new {user_type}.")
            user_settings(user_type)
    elif choice == "2":
        if delete('user_type', user_type):
            print(f"{user_type} successfully deleted.")
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


def delete(key, value):
    users1 = ordered_users(filter_users(key, value))
    print_users(users1)
    choice = input("\nPlease, select a user:  ")
    for obj in users1:
        if obj.get('index') == choice:
            return delete_user(filter_users(key, value), obj.get('user').get('id'))


