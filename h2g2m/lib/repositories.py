# -*- coding: utf-8 -*-

import json


class LanguageRepository:
    def __init__(self, filename):
        self.filename = filename

    def find_all(self):
        data = open(self.filename, 'r').read()
        data = json.loads(data.decode("utf-8-sig"))
        return [v['name'] for k, v in data.iteritems()]

