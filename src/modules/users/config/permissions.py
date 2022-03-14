class Permissions:
    index = {
        "GET": ['users.index'],
        "POST": ['users.store']
    }
    self = {
        "GET": ['users.get_one'],
        "PATCH": ['users.update'],
        "DELETE": ['users.delete']
    }
    list = {
        "GET": ['users.list']
    }
