import hashlib
import random
import uuid
from decimal import Decimal
from enum import Enum
from logs import log_decorator
from file_manager import user_manager
from users.common import print_enumerate, is_valid_email


class UserTypes(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:
    def __init__(self, full_name, user_type, phone, username=None, gender=None, age=None, email=None):
        self.id = str(uuid.uuid4())
        self.full_name = full_name
        self.user_type = user_type
        self.username = username
        self.phone = phone
        self.email = email
        self.login = f"ID{self.id[:5]}"
        self.password = f"pass{random.randint(100, 999)}"
        self.gender = gender
        self.age = age
        self.balance = Decimal(0)
        self.is_login = False
        self.is_active = False

    def hashing_password(self, password):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()

    def formatting_data(self):
        """
        converting user data to json format
        :return:
        """
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
        if self.user_type == UserTypes.STUDENT.value:
            user_data.update({
                'gender': self.gender,
                'age': self.age,
                'email': self.email,
                'balance': str(self.balance),
                'is_active': self.is_active
            })

        return user_data





@log_decorator
def add_user(user_type):
    """
    to register admin and teacher by super_admin,
    student by admin
    :param user_type:
    :return:
    """
    while True:
        full_name = input("Enter full name: ").title().strip()
        username = input("Enter username: ").lower().strip()
        email = get_email(user_type)
        phone = input("Enter phone number: ").strip()
        gender = _gender(user_type)

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            phone=phone,
            gender=gender,
            user_type=user_type
        )

        user_manager.add_data(user.formatting_data())
        return user


def get_email(user_type):
    """
    Get a validated email address
    """
    if user_type == UserTypes.STUDENT.value:
        while True:
            email = input("Enter an email:  ")
            if is_valid_email(email.lower()):
                return email
    return None


def _gender(user_type):
    """
    enter and retrieve the user's gender
    """
    if user_type == UserTypes.STUDENT.value:
        choice = input("""
        1. Male
        2. Female
        Enter choice:  
        """)
        if choice == '1':
            gender = 'male'
        else:
            gender = 'female'
    else:
        gender = None

    return gender


def filter_users(key, value):    # generator was used
    """
    filtering users using key and value
    """
    users = []
    all_users = user_manager.read_data()
    for user in all_users:
        if user.get(key) == value:
            users.append(user)
    return users


def get_user(id):
    """
    get user from users by id
    :param id:
    :return:
    """
    users = user_manager.read_data()
    for user in users:
        if user.get('id') == id:
            return user
    return None


@log_decorator
def delete_user(id):
    """
        delete user from users by id
        :param id:
        :return:
        """
    user = get_user(id)
    if user:
        return user_manager.delete_data(user)
    return None


@log_decorator
def update_user(id):
    """
        update user from users by id
        :param id:
        :return:
        """
    user = get_user(id)
    if user:
        new = new_data()
        return user_manager.update_data(user, new)
    return None


def new_data():
    """
    get new data to update user
    :return:
    """
    attributes = ["full_name", "username", "phone", 'password']

    print_enumerate(attributes)
    choice = int(input("Select the attribute you want to change: "))
    selected_attr = attributes[choice - 1]

    if selected_attr == "password":
        new_value = change_password()
    else:
        new_value = input(f"Enter new value for {selected_attr}:  ")

    return {
        selected_attr: new_value
    }


def confirm_password(password):
    confirm_pass = input("Confirm password:  ")
    return password == confirm_pass


@log_decorator
def change_password():
    while True:
        new_value = input(f"Enter new value for password:  ")
        if confirm_password(new_value):
            return new_value
        else:
            print("\nPasswords do not match. Try again.\n")