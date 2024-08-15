from file_manager import group_manager
from users.common import print_enumerate
from users.group import get_group_by_id


def teacher_groups(id):
    my_groups = []
    groups = group_manager.read_data()
    for group in groups:
        data = group_data(id, group)
        my_groups.append(data)
    return my_groups


def group_data(id, group):
    if id == group['teacher']:
        return {
                'id': group['id'],
                'name': group['name'],
                'duration (month)': group['duration'],
                'start_time': group['start_time'],
                'end_time': group['end_time'],
                'lesson_status': group['lesson_status']
            }
    return None


def show_group_students(id):
    group = get_my_group(id)
    group = get_group_by_id(group['id'])
    print_enumerate(group['students'])



def get_my_group(id):
    my_groups = show_my_groups(id)
    print_enumerate(my_groups)
    choice = int(input("\nPlease, select your group:  "))
    return my_groups[choice - 1]


def start_lesson(group):
    return group_manager.update_data(group, {'lesson_status': True})


def finish_lesson(group):
    return group_manager.update_data(group, {'lesson_status': False})


def lesson(id):
    group1 = get_my_group(id)
    group = get_group_by_id(group1['id'])
    if start_lesson(group):
        print("Lesson has started.")

    return lesson_menu(group)


def lesson_menu(group):
    print("""
    1. Finish the lesson
    2. Back
    """)
    while True:
        choice = input("\nEnter your choice:  ")
        if choice == '1':
            return finish_lesson(group)
        elif choice == '2':
            return None
        else:
            print("Invalid input! Try again.")
