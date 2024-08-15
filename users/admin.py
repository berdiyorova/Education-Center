from datetime import datetime
from decimal import Decimal

from file_manager import user_manager, group_manager
from logs import log_decorator
from users.common import print_enumerate
from users.user import UserTypes, get_user
from users.group import get_group
from users.user import filter_users


def show_students():
    students = filter_users('user_type', UserTypes.STUDENT.value)
    print_enumerate(students)

    return students


@log_decorator
def add_student_to_group():
    students = []
    group = get_group()

    data = get_student_data()
    students.append(data)

    return group_manager.update_data(group, {"students": students})


def get_student_data():
    new_student = search_result()
    return {
        'id': new_student['id'],
        'name': new_student['full_name']
    }


def search_student(value):
    """
    search for user by login
    :param value:
    :return:
    """
    students = filter_users('user_type', UserTypes.STUDENT.value)

    for student in students:
        if student['full_name'] == value or student['login'] == value:
            return student


@log_decorator
def search_result():
    """
    search student by full_name and login
    :return:
    """
    value = input("Enter full_name or login:  ")
    return search_student(value)


@log_decorator
def fill_balance():
    """
    filling the student balance
    :return:
    """
    student = search_result()
    print(student)
    new_balance = str(add_balance(student))

    return user_manager.update_data(student, {"balance": new_balance, "is_active": True})


def add_balance(student):
    amount = input("Enter amount you want to add balance:  ")
    return Decimal(student['balance']) + Decimal(amount)


def check_balance(balance, group):
    """
    balance check with group price and current time
    :param balance:
    :param group:
    :return:
    """
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    diff = datetime.now() - datetime.strptime(group['start_time'], date_format)
    month = diff.days//30 + 1
    return Decimal(balance) >= Decimal(group['price']) * month


def change_group_students_statuses(group):
    for st_id in group['students']:
        student = get_user(st_id)
        value = False
        if check_balance(student['balance'], group):
            value = True
        user_manager.update_data(student, {'is_active': value})


@log_decorator
def change_all_students_statuses():
    """
    check all students balances and change their statuses
    :return:
    """
    groups = group_manager.read_data()
    for group in groups:
        change_group_students_statuses(group)
