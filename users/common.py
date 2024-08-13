import hashlib
import random
from datetime import datetime, timedelta
from enum import Enum



class UserTypes(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:

    def __init__(self, first_name, last_name, user_type, phone, username=None, gender=None, age=None, email=None):
        self.id = random.randint(1000, 9999)
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = user_type
        self.username = username
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

    @property
    def password(self):
        return f"{random.randint(10000, 99999)}"

    @staticmethod
    def is_only_letters(s):
        return s.isalpha()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

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
