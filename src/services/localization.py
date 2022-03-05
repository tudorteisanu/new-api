
from flask import g


def translate(locale):
    try:
        locales_array = locale.split('.')

        module_name = locales_array[0]
        locales = locales_array[1:]

        mod = __import__(f'locales.{g.language}.{module_name}', fromlist=[f'Locales'])
        dictionary = getattr(mod, f'{module_name.capitalize()}Locales')

        return get_localization(dictionary.locales, locales)

    except FileNotFoundError:
        return locale

    except ModuleNotFoundError:
        return locale


def get_localization(_dict, locale):
    for key in locale:
        try:
            _dict = _dict[key]
        except KeyError:
            return locale[-1]
    return _dict
