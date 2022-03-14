class Permissions:
    index = {
        "GET": ['teachers.index'],
        "POST": ['teachers.store']
    }
    self = {
        "GET": ['teachers.get_one'],
        "PATCH": ['teachers.update'],
        "DELETE": ['teachers.delete']
    }
    list = {
        "GET": ['teachers.list']
    }
