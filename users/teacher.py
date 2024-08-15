from file_manager import group_manager


def show_my_groups(id):
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
                'duration': group['duration'],
                'start_time': group['start_time'],
                'end_time': group['end_time']
            }
    return None
