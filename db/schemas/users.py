def user_create_schema(data) -> dict:
    return {
        "id"       : str(data["_id"]),
        "name"     : str(data["name"]).title().strip(),
        "surname"  : str(data["surname"]).title().strip(),
        "username": str(data["username"]).title().strip(),
        "age"      : int(data["age"]),
        "mail"     : str(data["mail"]).strip(),
        "password" : str(data["password"]).strip,
        "estado"   : bool(data["estado"])
    }

def user_schema(data) -> dict:
    return {
        "id"       : str(data["_id"]),
        "name"     : str(data["name"]).title().strip(),
        "surname"  : str(data["surname"]).title().strip(),
        "username": str(data["username"]).title().strip(),
        "age"      : int(data["age"]),
        "mail"     : str(data["mail"]).strip(),
        "estado"   : bool(data["estado"])
    }
        
def user_login_schema(data) ->dict:
    return{
        "mail"     : str(data["mail"]).strip(),
        "password" : str(data["password"]).strip,
        "estado"   : bool(data["estado"])
    }
    
def user_password_schema(data) -> dict:
    return{
        "password" : str(data["password"])
    }
        
def users_create_schema(datas)->list:
    return [user_create_schema(data) for data in datas]




