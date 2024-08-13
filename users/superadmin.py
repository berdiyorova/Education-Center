
def show_menu(user_type):
    return f"""
    1. Add {user_type}
    2. Delete {user_type}
    3. Edit {user_type}
    4. Show {user_type}s
    5. Search {user_type}
    6. Back
    """

def admin_settings():
    print(show_menu(user_type="admin"))
    choice = input("Enter your choice: ")
    if choice == "1":
        pass
        print("Successfully added new admin.")
        admin_settings()
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
        admin_settings()


def teacher_settings():
    print(show_menu(user_type="teacher"))
    choice = input("Enter your choice: ")
    if choice == "1":
        pass
        print("Successfully added new admin.")
        admin_settings()
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
        admin_settings()


def super_admin_menu():
    print("""
        1. Admins
        2. Teachers
        3. Send message
        4. Logout
        """)
    choice = input("Enter your choice:  ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    else:
        print("Wrong choice !")
        super_admin_menu()
