import datetime
from decimal import Decimal

from file_manager import group_manager, user_manager
from users.common import filter_users, UserTypes, print_users


def show_groups():
    groups = group_manager.read_data()
    for index, group in enumerate(groups):
        print(f"{index + 1}. {group}")

    return groups


def get_group(groups, id):
    for group in groups:
        if group.get('id') == id:
            return group
    return None

def delete_group():
    groups = show_groups()
    choice = int(input("\nPlease, select the group you want to delete:  "))
    return group_manager.delete_data(groups[choice - 1])


def add_student_to_group():
    groups = show_groups()
    index_gr = int(input("Select the group:  "))
    while True:
        students = show_students()
        index_st = int(input("Select the student (input 0 to exit):  "))
        if index_st == 0:
            break
        else:
            groups[index_gr - 1]['students'].append(students[index_st - 1])

    group_manager.write_data(groups)


def show_students():
    students = list(filter_users('user_type', UserTypes.STUDENT.value))
    print_users(students)

    return students

def search_student(name_or_login):
    student = list(filter_users('full_name', name_or_login))
    if not student:
        student = list(filter_users('login', name_or_login))

    return student[0]


def fill_balance(text):
    student = search_student(text)
    print(student)
    amount = input("Enter amount you want to add balance:  ")
    new_balance = str(Decimal(float(student['balance'])) + Decimal(float(amount)))
    if user_manager.update_data(student, {"balance": new_balance}):
        return user_manager.update_data(student, {"is_active": True})
    return None


def check_balance(balance, group):
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    diff = datetime.datetime.now() - datetime.strptime(group['start_time'], date_format)
    month = diff.days//30 + 1
    return balance >= float(group['price']) * month

def change_students_status(group):
    for student in group['students']:
        value = False
        if check_balance(student['balance'], group):
            value = True
        user_manager.update_data(student, {'is_active': value})


