import hashlib
import random
from enum import Enum


class UserTypes(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User:

    def __init__(self, first_name, last_name, user_type, username=None, gender=None, age=None, email=None):
        self.id = random.randint(1000, 9999)
        self.first_name = first_name
        self.last_name = last_name
        self.user_type = user_type
        self.username = username
        self.gender = gender
        self.age = age
        self.email = email
        self.balance = 0
        self.is_login = False
        self.is_activ = False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def login(self):
        return f"ID{self.id}"

    @property
    def password(self):
        return f"{self.first_name[:3]}{random.randint(100, 999)}"

    @classmethod
    def is_only_letters(s):
        return s.isalpha()

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
