class Permissions:
    index = {
        "GET": ['roles.index'],
        "POST": ['roles.store']
    }
    self = {
        "GET": ['roles.get_one'],
        "PATCH": ['roles.update'],
        "DELETE": ['roles.delete']
    }
    list = {
        "GET": ['roles.list']
    }
    permissions = {
        "GET": ['roles.get_permissions'],
        "PUT": ['roles.update_permissions']
    }
