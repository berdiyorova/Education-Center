from file_manager import group_manager


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
