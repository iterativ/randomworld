# -*- coding: utf-8 -*-
#
# ITerativ GmbH
# http://www.iterativ.ch/
#
# Copyright (c) 2012 ITerativ GmbH. All rights reserved.
#
# Created on Nov 24, 2013
# @author: maersu <me@maersu.ch>

import factory
import random
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.utils.encoding import force_unicode
from django.utils.text import slugify

from randomworld.names import name_factory


class DefaultFactoryMixin(object):
    @classmethod
    def get_defaults(cls):
        return {}

    @classmethod
    def _prepare(cls, create, **kwargs):
        cls.kwargs = kwargs
        args = cls.get_defaults()

        for key, value in args.items():
            kwargs[key] = kwargs.get(key, value)

        return super(DefaultFactoryMixin, cls)._prepare(create, **kwargs)


UserKlass = get_user_model()
_user = UserKlass()
DUMMY_PASSWORD = 'test'
_user.set_password(DUMMY_PASSWORD)
DUMMY_PASSWORD_HASH = _user.password
USER_NAME_MAX = 30


class UserFactory(DefaultFactoryMixin, factory.Factory):
    class Meta:
        model = UserKlass

    @classmethod
    def get_defaults(cls):
        first_name, last_name = name_factory.get_full_name(unique=True)
        # do not overwrite kwargs
        first_name = force_unicode(cls.kwargs.get('first_name', first_name))
        last_name = force_unicode(cls.kwargs.get('last_name', last_name))

        username = slugify(u'{0}-{1}'.format(first_name, last_name).lower())
        # check max length
        if len(username) > USER_NAME_MAX:
            username = '%s%s' % (username[:(USER_NAME_MAX - 1)], random.randint(1, 9))

        return {
            'first_name': first_name,
            'last_name': last_name,
            'password': DUMMY_PASSWORD_HASH,
            'username': username,
            'email': '%s@%s.dy' % (username, slugify(last_name))
        }


class StaffFactory(UserFactory):
    is_staff = True
    is_superuser = True

