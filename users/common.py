import hashlib
import random
from datetime import datetime, timedelta
from enum import Enum

from Exam.logs import log_decorator
from Exam.file_manager import user_manager


class UserTypes(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:
    def __init__(self, first_name, last_name, user_type, phone, password, username=None, gender=None, age=None, email=None):
        self.id = random.randint(1000, 9999)
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = user_type
        self.username = username
        self.password = password
        self.gender = gender
        self.age = age
        self.email = email
        self.phone = phone
        self.balance = 0
        self.is_login = False
        self.is_active = False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def login(self):
        return f"ID{self.id}"

    def check_password(self, confirm_password):
        return self.password == confirm_password

    def hash_password(self):
        self.password = hashlib.sha256(self.password.encode()).hexdigest()

    def formatting_data(self):
        if self.user_type == 'admin':
            self.admin_data()
        elif self.user_type == 'teacher':
            self.teacher_data()
        else:
            self.student_data()

    def admin_data(self):
        return {
            'full_name': self.full_name,
            'username': self.username,
            'phone': self.phone,
            'user_type': self.user_type,
            'password': self.password,
            'is_login': self.is_login
        }

    def teacher_data(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'login': self.login,
            'password': self.password,
            'is_login': self.is_login
        }

    def student_data(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'login': self.login,
            'password': self.password,
            'balance': self.balance,
            'is_login': self.is_login,
            'is_active': self.is_active
        }



class Group:
    def __init__(self, name, description, teacher, max_student, duration, price):
        self.name = name
        self.description = description
        self.teacher = teacher
        self.max_student = max_student
        self.start_time = datetime.now()
        self.duration = duration
        self.price = price
        self.status = True
        self.students = []

    @property
    def end_time(self):
        return self.start_time + timedelta(days=30*self.duration)

    def change_status(self):
        if datetime.now() == self.end_time:
            self.status = False


@log_decorator
def add_admin():
    first_name: str = input("Enter first name: ").title().strip()
    last_name: str = input("Enter last name: ").title().strip()
    username: str = input("Enter username: ").lower().strip()
    phone: str = input("Enter phone number: ").strip()
    password: str = input("Enter password: ")
    confirm_password: str = input("Confirm password: ")

    admin = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        phone=phone,
        password=password,
        user_type=UserTypes.ADMIN.value
    )
    if not admin.check_password(confirm_password):
        add_admin()

    admin.hash_password()
    user_manager.add_data(admin)
    return admin
