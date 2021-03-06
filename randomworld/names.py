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
import datetime
import os
import random
import string
import glob

LOREM_IPSUM = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
LOREM_IPSUM_LIST = LOREM_IPSUM.split(' ')

BASE_WISH = [u'Ich möchte lernen wie man am besten %(verb)s kann',
             u'Wie kann ich sofort %(verb)s?',
             u'Wie %(verb)s wir richtig?',
             u'Grundkurs: %(verb)s',
             u'Wie mache ich %(noun)s selber',
             u'Anfängerkurs: %(noun)s',
             u'Ich möchte wissen wie man am besten %(noun)s %(verb)s kann',
             u'Crashkurs: %(noun)s %(verb)s',
             u'Intensivkurs in %(noun)skunde',
             u'Wie kann man zu hause am einfachsten %(verb)s?',
             u'Eine %(noun)s %(verb)s, ohne zu %(verb2)s',
             u'Wie man %(noun)s am einfachsten und besten %(verb)s kann',
             u'Tipps und Tricks fürs %(noun)s',
             u'Das Optimum aus meinem %(noun)s rausholen',
             u'Wie man %(noun)s genau %(verb)s muss',
             u'Vorgehen beim %(verb)s',
             u'%(verb)s für Dummies'
]


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


def make_method(cls, name):
    def _get_generic_name(self, unique=False):
        return self._get_name(name, unique)

    fn_name = 'get_%s' % name
    if not hasattr(cls, fn_name):
        setattr(cls, fn_name, _get_generic_name)


class NameFactory():
    names = {}
    _chosen = {'full_name': [],
               'string': [],
               'plz': [],
               'tel': [],
               'words': []}

    def __init__(self):
        for csv_file in glob.glob(os.path.join(os.path.dirname(__file__), "data/*.csv")):
            group = os.path.splitext(os.path.basename(csv_file))[0]
            self._load_file(group, csv_file)
            make_method(NameFactory, group)

    def _load_file(self, group, file):
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

    def get_random_datetime(self, start=None, end=None):

        if start is None:
            start = (end or datetime.datetime.now()) + datetime.timedelta(weeks=-102)

        if end is None:
            end = datetime.datetime.now()

        return start + datetime.timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

    def get_string(self, unique=False, size=6, chars=string.ascii_lowercase):
        if unique:
            while True:
                name = ''.join(random.choice(chars) for x in range(size + 1))
                if name not in self._chosen['string']:
                    break
            self._chosen['string'].append(name)
        else:
            name = ''.join(random.choice(chars) for x in range(size + 1))

        return name

    def get_words(self, unique=False, size=30, words=LOREM_IPSUM_LIST):
        if unique:
            while True:
                name = ' '.join([random.choice(words) for i in range(1, size + 1)])
                if name not in self._chosen['words']:
                    break
        else:
            name = ' '.join([random.choice(words) for i in range(1, size + 1)])

        self._chosen['words'].append(name)
        return name[0].upper() + name[1:]

    def get_html(self, unique=False, count=30, words=LOREM_IPSUM_LIST):

        HTML_ENTITIES = [('<b>%s</b>', (5, 10)),
                         ('<p>%s</p>', (30, 100)),
                         ('<p>%s</p>', (30, 100)),
                         ('<i>%s</i>', (5, 10)),
                         ('<h2>%s</h2>', (2, 4)),
                         ('<a href="http://notfound.org/" target="_blank">%s</a>', (1, 5)),
                         ('<ul>%s</ul>', '<li>%s</li>', (5, 10))]

        html = ''
        for c in range(1, count):
            h = random.choice(HTML_ENTITIES)
            if len(h) == 2:
                tmplate, ranges = h
                html += ' ' + tmplate % (
                ' '.join([random.choice(words) for i in range(ranges[0], ranges[1])]).capitalize())
            else:
                tmplate_base, tmplate, ranges = h
                sub_html = ''
                for i in range(ranges[0], ranges[1]):
                    sub_html += ' ' + tmplate % (
                    ' '.join([random.choice(words) for i in range(ranges[0], ranges[1])]).capitalize())
                html += ' ' + tmplate_base % sub_html

        return html

    def get_random_plz(self, unique=False):
        return random.randint(1000, 3000)

    def get_random_tel(self, unique=False):
        return '+4179%s' % random.randint(1000000, 9999999)

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
            self._chosen['full_name'].append(names)
        else:
            names = (self.get_first_name(unique), self.get_last_name(unique))

        return names

    def get_wish(self, unique=False):
        group = 'wish'
        if unique:
            available = filter(lambda x: x not in self._chosen[group], self.names[group])
            if len(available):
                name = random.choice(available)
            else:
                name = random.choice(BASE_WISH) % {'verb': self.get_verb(),
                                                   'verb2': self.get_verb(),
                                                   'noun': self.get_noun()}

            self._chosen[group].append(name)
        else:
            name = random.choice(self.names[group])

        return name

    def _get_name(self, group, unique=False):
        if unique:
            available = filter(lambda x: x not in self._chosen[group], self.names[group])
            if len(available):
                name = random.choice(available)
            else:
                name = random.choice(self.names[group]) + ' ' + self.get_string(unique=unique, size=4).title()

            self._chosen[group].append(name)
        else:
            name = random.choice(self.names[group])

        return name


name_factory = NameFactory()