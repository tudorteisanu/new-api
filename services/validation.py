from flask import request


def validate():
    data = request.json
    module_name = request.url_rule.rule.split("/")[1]
    mod = __import__(f'apps.{module_name}.models', fromlist=['Validation'])
    validation = getattr(mod, 'Validation')
    validations = validation.validators
    errors = {}
    
    for key in validations:
        field_validations = validations[key].split(',')
        
        for validation in field_validations:
            if validation == 'required' and key not in data:
                errors[key] = f'Field {key} is required'
            
            elif key in data:
                field = data[key]
                
                if validation == 'str':
                    if type(data[key]) != str:
                        errors[key] = f'Field {key} must be an string!'
                
                if validation == 'list':
                    if type(data[key]) != list:
                        errors[key] = f'Field {key} must be an array!'
                
                if validation == 'int':
                    if type(data[key]) != int:
                        errors[key] = f'Field {key} must be an integer!'
                
                if validation.startswith('min:'):
                    minimal_length = int(validation.split(':')[1])
                    
                    if len(field) < minimal_length:
                        errors[key] = f'Minimal length is {minimal_length}'
                
                if validation.startswith('max:'):
                    maximal_length = int(validation.split(':')[1])
                    
                    if len(field) > maximal_length:
                        errors[key] = f'Maximal length is {maximal_length}'
                
                if validation.startswith('exact:'):
                    exact = int(validation.split(':')[1])
                    
                    if len(field) != exact:
                        errors[key] = f'Length must be {exact}'
                
                if validation.startswith('in:'):
                    string_items = validation.split(':')[1]
                    items = string_items.split('|')
                    
                    if data[key] not in items:
                        errors[key] = f'Not allowed value for field {key}'
    return errors
