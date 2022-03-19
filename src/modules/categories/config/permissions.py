class Permissions:
    module = 'categories'
    index = {
        "GET": [f'{module}.index'],
        "POST": [f'{module}.store']
    }
    self = {
        "GET": [f'{module}.get_one'],
        "PATCH": [f'{module}.update'],
        "DELETE": [f'{module}.delete']
    }
    list = {
        "GET": [f'{module}.list']
    }
