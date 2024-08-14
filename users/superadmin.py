from common import add_user, UserTypes, filter_users, print_users, delete_user, update_user, search_user


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
    users = list(filter_users(key, value))
    print_users(users)
    choice = int(input("\nPlease, select the user you want to delete:  "))
    return delete_user(users, users[choice - 1]['id'])


def update(key, value):
    users = list(filter_users(key, value))
    print_users(users)
    choice = int(input("\nPlease, select the user you want to edit:  "))
    return update_user(users, users[choice - 1]['id'])


def show_users(key, value):
    users = list(filter_users(key, value))
    print_users(users)


def search(key, value):
    users = list(filter_users(key, value))
    text = input("Search:  ")
    users = list(search_user(users, text))
    return users


super_admin_menu()
