import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from file_manager import group_manager
from logs import log_decorator
from users.common import print_enumerate
from users.user import filter_users, UserTypes


class Group:
    def __init__(self, name, description, teacher, max_student, duration, price):
        self.id = str(uuid.uuid4())
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

    def formatting_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'teacher': self.teacher,
            'max_student': self.max_student,
            'duration': self.duration,
            'price': str(self.price),
            'start_time': str(self.start_time),
            'end_time': str(self.end_time),
            'status': self.status,
            'students': self.students
        }





@log_decorator
def add_group():
    """
    to create admin by admin
    :return:
    """
    while True:
        name = input("Enter group name: ").title().strip()
        description = input("Enter description (What is taught in this group): ")
        teacher = choose_teacher()
        max_student = int(input("Enter the maximum number of students:  "))
        duration = int(input("How long is the course (months):  "))
        price = float(input("How much is the course price (monthly):  "))

        group = Group(
            name=name,
            description=description,
            teacher=teacher,
            max_student=max_student,
            duration=duration,
            price=price
        )

        group_manager.add_data(group.formatting_data())
        return group


def choose_teacher():
    teachers = filter_users('user_type', UserTypes.TEACHER.value)
    print_enumerate(teachers)
    choice = int(input("\nPlease, select the teacher:  "))
    return teachers[choice - 1]['id']


def show_groups():
    groups = group_manager.read_data()
    print_enumerate(groups)
    return groups


def get_group():
    """
    choose a group
    :return:
    """
    groups = show_groups()
    choice = int(input("\nPlease, select the group:  "))
    return groups[choice - 1]


def delete_group():
    group = get_group()
    return group_manager.delete_data(group)

