# -*- coding: utf-8 -*-
#
# ITerativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2012 ITerativ GmbH. All rights reserved.
#
# Created on Jul 10, 2013
# @author: maersu <me@maersu.ch>

import csv, codecs
import os
import random
import string


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class NameFactory():

    names = {}
    _chosen = {'full_name':[], 'string':[], 'plz':[], 'tel':[]}

    def __init__(self):
        self._load_file('first_name')
        self._load_file('last_name')
        self._load_file('city')
        self._load_file('district')
        self._load_file('street')

    def _load_file(self, group):
        import __init__
        file =  os.path.join(os.path.dirname(__init__.__file__), 'data', '%s.csv' % group)

        names_list = []

        with open(file, 'rb') as f:
            reader = UnicodeReader(f)
            for row in reader:
                if len(row) == 1:
                    row = row[0].strip()
                else:
                    row = ' '.join(row)

                if len(row.strip()) > 0:
                    names_list.append(row)

        self.names[group] = list(set(names_list))
        self._chosen[group] = []

    def get_string(self, unique=False, size=6, chars=string.ascii_lowercase):
        if unique:
            while True:
                name = ''.join(random.choice(chars) for x in range(size))
                if name not in self._chosen['string']:
                    break
        else:
            name = ''.join(random.choice(chars) for x in range(size))

        self._chosen['string'].append(name)
        return name

    def get_random_plz(self, unique=False):
        return random.randint(1000, 3000)

    def get_random_tel(self, unique=False):
        return '+41 %s'  % random.randint(100000000, 999999999)

    def get_full_name(self, unique=False):
        if unique:
            i = 0
            while True:
                names = (self.get_first_name(unique=False), self.get_last_name(unique=False))
                if names not in self._chosen['full_name']:
                    break
                i += 1
                if i > 7:
                    names = (names[0], names[1] + ' ' + self.get_string(unique=unique, size=4).title())
                    break
        else:
            names = (self.get_first_name(unique), self.get_last_name(unique))

        self._chosen['full_name'].append(names)
        return names

    def get_first_name(self, unique=False):
        return self._get_name('first_name', unique)

    def get_last_name(self, unique=False):
        return self._get_name('last_name', unique)

    def get_city(self, unique=False):
        return self._get_name('city', unique)

    def get_district(self, unique=False):
        return self._get_name('district', unique)

    def get_street(self, unique=False):
        return self._get_name('street', unique)

    def _get_name(self, group, unique=False):
        if unique:
            available = filter(lambda x: x not in self._chosen[group], self.names[group])
            if len(available):
                name = random.choice(available)
            else:
                name = random.choice(self.names[group]) + ' ' + self.get_string(unique=unique, size=4).title()

        else:
            name = random.choice(self.names[group])

        self._chosen[group].append(name)
        return name





