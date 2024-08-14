import smtplib
import threading
from contextlib import contextmanager

from common import add_user, UserTypes, filter_users, print_users, delete_user, update_user, search_user
from file_manager import user_manager
from logs import log_decorator


def show_menu(user_type):
    return f"""
    1. Add {user_type}
    2. Delete {user_type}
    3. Edit {user_type}
    4. Show {user_type}s
    5. Search {user_type}
    6. Back
    """

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
        return None
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


@contextmanager
def smtp_connection():
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_sender, smtp_password)
    yield server
    server.quit()


def email_to_users():
    users = list(filter_users('user_type', 'student'))
    while True:
        print("""  
        1. To all  
        2. To guys  
        3. To girls  
        """)
        choice = input("Choose an option who you want to send email:  ")

        if choice == '1':
            return users
        if choice == '2':
            return list(filter_users('gender', 'male'))
        elif choice == '3':
            return list(filter_users('gender', 'female'))
        else:
            print("Invalid input! Try again.")


def send_message(users):
    subject = input("Subject: ")
    message = input("Message: ")
    for user in users:
        t = threading.Thread(target=send_mail, args=(user['email'], subject, message))
        t.start()
    print(f"Email is sent to users")


def send_mail(to_user, subject, message):
    email_content = f"Subject: {subject}\n\n{message}"
    try:
        with smtp_connection() as server:
            server.sendmail(smtp_sender, to_user, email_content)
    except smtplib.SMTPException as e:
        print(f"Failed to send email to {to_user}: {e}")



smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_sender = 'rano.baxromovna@gmail.com'
smtp_password = 'iwnd wsls azqg bphk'




super_admin_menu()
