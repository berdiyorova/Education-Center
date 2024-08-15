from file_manager import user_manager

superadmin_login = "superadmin"
superadmin_password = "sA0101"



def check_superadmin(login, password):
    if login == superadmin_login and password == superadmin_password:
        return True
    return False


def check_user(login, password):
    all_users = user_manager.read_data()
    for user in all_users:
        if user['login'] == login and user['password'] == password:
            return True
    return False

def log_in(login, password):
    if check_user(login, password):
        all_users = user_manager.read_data()
        for user in all_users:
            if user['login'] == login and user['password'] == password:
                user['is_login'] = True
                user_manager.write_data(all_users)
                return user['user_type'], user['id']
        return None


def logout(id):
    all_users = user_manager.read_data()
    for user in all_users:
        if user['id'] == id:
            user['is_login'] = False
            user_manager.write_data(all_users)
            return True
    return False
