class Permissions:
    index = {
        "GET": ['permissions.index'],
        "POST": ['permissions.store']
    }
    self = {
        "GET": ['permissions.get_one'],
        "PATCH": ['permissions.update'],
        "DELETE": ['permissions.delete']
    }
    list = {
        "GET": ['permissions.list']
    }
