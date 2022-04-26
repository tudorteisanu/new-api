class Permissions:
    index = {
        "GET": ['degrees.index'],
        "POST": ['degrees.store']
    }
    self = {
        "GET": ['degrees.get_one'],
        "PATCH": ['degrees.update'],
        "DELETE": ['degrees.delete']
    }
    list = {
        "GET": ['degrees.list']
    }
    permissions = {
        "GET": ['degrees.get_permissions'],
        "PUT": ['degrees.update_permissions']
    }
