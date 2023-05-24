from scripts.dbms import DBHelper


def auth_module(data: list) -> any:
    db = DBHelper()
    profile = db.user_authentication(data)

    if not profile:
        return None
    elif profile[0][1] == data[0] \
    and profile[0][2] == data[1]:
        return profile[0][0]
