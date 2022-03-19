import json
import logging
from os import listdir, path
from flask import g


class Locales:
    dictionary = {}

    def __init__(self):
        self.get_translates()

    def __call__(self, locale, lang):
        if lang is not None:
            language = lang
        else:
            language = g.language

        return self.translate(locale, language)

    def get_translates(self):
        self.load_global_locales()
        main_dir = 'src/modules'

        for directory in listdir(main_dir):
            self.load_module_locales(f'{main_dir}/{directory}/locales')

    def load_global_locales(self):
        self.load_module_locales('src/locales')

    def load_module_locales(self, locale_dir):
        if path.exists(locale_dir):
            for item in listdir(locale_dir):
                if item.endswith('.json'):
                    with open(f'{locale_dir}/{item}') as file:
                        content = json.loads(file.read())
                        key = item.split('.')[0]

                        if self.dictionary.get(key, None) is None:
                            self.dictionary[key] = {}
                        self.dictionary[key] = {**self.dictionary[key], **content}

    def translate(self, locale, lang=None):
        try:
            locales = locale.split('.')
            return self.get_localization(locales, lang)

        except Exception as e:
            logging.error(e)
            print(e, 'error')
            return locale

    def get_localization(self, locale, lang):

        if lang is not None:
            language = lang
        else:
            language = g.language

        _dict = self.dictionary[language]
        for key in locale:
            try:
                _dict = _dict[key]
                print(_dict)
            except KeyError:
                return locale[-1]
        return _dict
