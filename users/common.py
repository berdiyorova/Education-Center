import re


def is_valid_email(email):
    """
    check email
    :param email:
    :return:
    """
    # Define the email pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # Use re.match to validate the email
    if re.match(pattern, email):
        return True
    return False


def print_enumerate(objs):
    for index, obj in enumerate(objs):
        print(f"{index + 1}. {obj}")
