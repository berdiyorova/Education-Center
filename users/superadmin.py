import smtplib
import threading
from contextlib import contextmanager

from users.user import filter_users, print_enumerate, delete_user, update_user, UserTypes


def show_menu(user_type):
    return f"""
    1. Add {user_type}
    2. Delete {user_type}
    3. Edit {user_type}
    4. Show {user_type}s
    5. Back
    """


def delete(key, value):
    users = filter_users(key, value)
    print_enumerate(users)
    choice = int(input("\nPlease, select the user you want to delete:  "))
    return delete_user(users[choice - 1]['id'])


def update(key, value):
    users = filter_users(key, value)
    print_enumerate(users)
    choice = int(input("\nPlease, select the user you want to edit:  "))
    return update_user(users[choice - 1]['id'])


def show_users(key, value):
    users = filter_users(key, value)
    print_enumerate(users)


@contextmanager
def smtp_connection():
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_sender, smtp_password)
    yield server
    server.quit()


def email_to_users():
    users = filter_users('user_type', UserTypes.STUDENT.value)
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
            return [user for user in users if user['gender'] == 'male']
        elif choice == '3':
            return [user for user in users if user['gender'] == 'female']
        else:
            print("Invalid input! Try again.")


def send_message():
    users = email_to_users()
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
