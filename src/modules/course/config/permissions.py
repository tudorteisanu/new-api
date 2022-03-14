class Permissions:
    index = {
        "GET": ['courses.index'],
        "POST": ['courses.store']
    }
    self = {
        "GET": ['courses.get_one'],
        "PATCH": ['courses.update'],
        "DELETE": ['courses.delete']
    }
    list = {
        "GET": ['courses.list']
    }
    permissions = {
        "GET": ['courses.get_permissions'],
        "PUT": ['courses.update_permissions']
    }
