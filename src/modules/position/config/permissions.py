class Permissions:
    index = {
        "GET": ['positions.index'],
        "POST": ['positions.store']
    }
    self = {
        "GET": ['positions.get_one'],
        "PATCH": ['positions.update'],
        "DELETE": ['positions.delete']
    }
    list = {
        "GET": ['positions.list']
    }
