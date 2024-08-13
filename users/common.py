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
    def __init__(self, first_name, last_name, user_type, phone, password, username=None, gender=None, age=None, email=None):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
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
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

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
            'password': self.password,
            'is_login': self.is_login
        }
        if self.user_type in {UserTypes.TEACHER.value, UserTypes.STUDENT.value}:
            user_data.update({
                'email': self.email,
                'login': self.login,
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
        first_name = input("Enter first name: ").title().strip()
        last_name = input("Enter last name: ").title().strip()
        username = input("Enter username: ").lower().strip()
        email = input("Enter email: ").lower().strip()
        phone = input("Enter phone number: ").strip()
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        user = User(
            first_name=first_name,
            last_name=last_name,
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


def filter_users(key, value):    # generator was used
    users = user_manager.read_data()
    for user in users:
        if user.get(key) == value:  # Use get to avoid KeyError
            yield user

def ordered_users(users):
    return [{'index': str(index + 1), 'user': user} for index, user in enumerate(users)]

def print_users(users):
    users1 = ordered_users(users)
    for user in users1:
        print(f"{user['index']}. {user['user']}")

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
