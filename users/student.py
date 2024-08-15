from file_manager import group_manager
from users.user import get_user


def student_groups(id):
    my_groups = []
    groups = group_manager.read_data()
    for group in groups:
        data = group_data(id, group)
        my_groups.append(data)
    return my_groups


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


def show_balance(id):
    student = get_user(id)
    return student['balance']
