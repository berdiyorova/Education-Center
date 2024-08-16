from file_manager import group_manager
from logs import log_decorator
from users.user import get_user

@log_decorator
def student_groups(id):
    my_groups = []
    groups = group_manager.read_data()
    for group in groups:
        data = group_data(id, group)
        my_groups.append(data)
    return my_groups

@log_decorator
def group_data(id, group):
    for student in group['students']:
        if id == student['id']:
            return {
                    'id': group['id'],
                    'name': group['name'],
                    'teacher': group['teacher'],
                    'start_time': group['start_time'],
                }
    return None

@log_decorator
def show_balance(id):
    student = get_user(id)
    return student['balance']
