class Permissions:
    module = 'positions'
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
    permissions = {
        "GET": [f'{module}.get_permissions'],
        "PUT": [f'{module}.update_permissions']
    }
