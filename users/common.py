import hashlib
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from logs import log_decorator
from file_manager import user_manager


class UserTypes(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:
    def __init__(self, full_name, user_type, phone, password, username=None, gender=None, age=None, email=None):
        self.id = str(uuid.uuid4())
        self.full_name = full_name
        self.user_type = user_type
        self.username = username
        self.phone = phone
        self.email = email
        self.password = password
        self.gender = gender
        self.age = age
        self.balance = Decimal(0)
        self.is_login = False
        self.is_active = False

    @property
    def login(self):
        return f"ID-{self.id[:5]}"

    def hashing_password(self, password):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()

    def check_password(self, confirm_password):
        return self.password == confirm_password

    def formatting_data(self):
        user_data = {
            'id': self.id,
            'full_name': self.full_name,
            'username': self.username,
            'phone': self.phone,
            'user_type': self.user_type,
            'login': self.login,
            'password': self.password,
            'is_login': self.is_login
        }
        if self.user_type in {UserTypes.TEACHER.value, UserTypes.STUDENT.value}:
            user_data.update({
                'age': self.age,
                'email': self.email,
                'balance': self.balance if self.user_type == UserTypes.STUDENT.value else None,
                'is_active': self.is_active if self.user_type == UserTypes.STUDENT.value else None
            })
        return user_data


class Group:
    def __init__(self, name, description, teacher, max_student, duration, price):
        self.name = name
        self.description = description
        self.teacher = teacher
        self.max_student = max_student
        self.start_time = datetime.now()
        self.duration = duration
        self.price = Decimal(price)
        self.status = True
        self.students = []

    @property
    def end_time(self):
        return self.start_time + timedelta(days=self.duration * 30)

    def change_status(self):
        if datetime.now() >= self.end_time:
            self.status = False


@log_decorator
def add_user(user_type):
    while True:
        full_name = input("Enter full name: ").title().strip()
        username = input("Enter username: ").lower().strip()
        email = validate_email().lower()
        phone = input("Enter phone number: ").strip()
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            password=password,
            user_type=user_type
        )

        if not user.check_password(confirm_password):
            print("\nPasswords do not match. Please try again.")
            continue

        user_manager.add_data(user.formatting_data())
        return user


def validate_email():
    while True:  # Validating email format
        email = input("Enter your email: ").strip()
        if email.endswith('@gmail.com') or email.endswith('@mail.ru'):
            return email
        else:
            print("Invalid input, try again!")


def filter_users(key, value):    # generator was used
    users = user_manager.read_data()
    for user in users:
        if user.get(key) == value:  # Use get to avoid KeyError
            yield user


def print_users(users):
    for index, user in enumerate(users):
        print(f"{index + 1}. {user}")


def get_user(users, id):
    for user in users:
        if user.get('id') == id:
            return user
    return None

def delete_user(users, id):
    user = get_user(users, id)
    if user:
        return user_manager.delete_data(user)
    return None

def update_user(users, id):
    user = get_user(users, id)
    if user:
        new = new_data()
        return user_manager.update_data(user, new)
    return None


def new_data():
    attributes = ["full_name", "username", "email", "phone", "password"]

    print_users(attributes)
    choice = int(input("Select the attribute you want to change: "))
    selected_attr = attributes[choice - 1]

    if selected_attr == 'password':
        new_value = password_change()
    else:
        new_value = input(f"Enter new value for {selected_attr}  ")

    return {
        selected_attr: new_value
    }

def password_change():
    while True:
        password = input(f"Enter new value for password  ")
        confirm = input("Enter again the password  ")
        if password != confirm:
            print("\nPasswords do not match. Please try again.")
            continue

        return password

def search_user(users, value):
    for user in users:
        if user['full_name'] == value:
            yield user
        elif user['username'] == value:
            yield user
        elif user['phone'] == value:
            yield user
        else:
            continue
